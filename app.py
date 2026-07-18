from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="CS 이탈 원인 대시보드", layout="wide")

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "my-wiki-02" / "raw"
PROFILE_PATH = BASE_DIR / "my-wiki-02" / "components" / "output" / "06_customers_full_profile.csv"

REF_DATE = pd.Timestamp("2024-12-31")

# 색상 토큰 (dataviz 방식: 요금제는 순서형 -> 한 계열 밝기 단계, 이탈여부는 상태값 -> 고정된 상태색)
PLAN_ORDER = ["베이직", "스탠다드", "프리미엄"]
PLAN_COLORS = {"베이직": "#6da7ec", "스탠다드": "#2a78d6", "프리미엄": "#184f95"}
HIGHLIGHT_COLOR = "#d03b3b"
MUTED_COLOR = "#b0aea6"
STATUS_GOOD = "#0ca30c"      # 비이탈(N)
STATUS_CRITICAL = "#d03b3b"  # 이탈(Y)
SINGLE_SERIES_COLOR = "#2a78d6"
CHURN_COLOR_MAP = {"N": STATUS_GOOD, "Y": STATUS_CRITICAL}
CHURN_LABEL_MAP = {"N": "비이탈", "Y": "이탈"}


@st.cache_data
def load_profile():
    df = pd.read_csv(PROFILE_PATH)
    df["join_date"] = pd.to_datetime(df["join_date"])
    df["tenure_months"] = (REF_DATE - df["join_date"]).dt.days / 30.44
    df["tenure_years"] = df["tenure_months"] / 12
    df["churn_label"] = df["churn_yn"].map(CHURN_LABEL_MAP)
    return df


@st.cache_data
def load_channel_summary(customers_attr):
    consultations = pd.read_csv(RAW_DIR / "data_consultations.csv")
    satisfaction = pd.read_csv(RAW_DIR / "data_satisfaction.csv")

    consultations = consultations.merge(customers_attr, on="customer_id", how="left")
    sat_joined = satisfaction.merge(
        consultations[["consult_id", "channel", "is_recontact", "plan", "region"]],
        on="consult_id",
        how="left",
    )
    return consultations, sat_joined


def apply_filters(df, plans, regions):
    return df[df["plan"].isin(plans) & df["region"].isin(regions)]


profile = load_profile()

# ---------------- 사이드바 필터 ----------------
st.sidebar.header("필터")
selected_plans = st.sidebar.multiselect("요금제", PLAN_ORDER, default=PLAN_ORDER)
region_options = sorted(profile["region"].unique().tolist())
selected_regions = st.sidebar.multiselect("지역", region_options, default=region_options)
st.sidebar.caption("필터를 바꾸면 아래 모든 차트가 즉시 다시 계산됩니다. 표본 30건 미만 구간은 참고용으로만 해석하세요.")

if not selected_plans or not selected_regions:
    st.warning("요금제와 지역을 하나 이상 선택해주세요.")
    st.stop()

fdf = apply_filters(profile, selected_plans, selected_regions)

if len(fdf) < 10:
    st.warning(f"필터 결과 표본이 {len(fdf)}명뿐입니다. 결과를 참고용으로만 보세요.")

customers_attr = profile[["customer_id", "plan", "region"]]

# ================= 헤더 =================
st.title("이래서 고객이 떠난다 — CS 데이터로 본 이탈 원인")
st.markdown(
    "요금제·지역·가입기간 같은 고객 속성부터 상담 채널 품질, VOC, 실제 이용 패턴까지 "
    "순서대로 짚어가며 **이탈이 어디서, 왜 시작되는지** 확인합니다."
)

n_total = len(fdf)
n_churn = int((fdf["churn_yn"] == "Y").sum())
churn_rate = n_churn / n_total * 100 if n_total else 0

c1, c2, c3 = st.columns(3)
c1.metric("고객 수 (필터 적용)", f"{n_total:,}명")
c2.metric("이탈 고객 수", f"{n_churn:,}명")
c3.metric("전체 이탈률", f"{churn_rate:.1f}%")

st.divider()

# ================= 2. 고객 속성별 이탈률 =================
st.header("1. 고객 속성별 이탈률 — 어떤 축이 진짜 원인에 가까운가")

col_plan, col_region, col_tenure = st.columns(3)

with col_plan:
    plan_g = (
        fdf.groupby("plan")["churn_yn"]
        .apply(lambda s: (s == "Y").mean() * 100)
        .reindex([p for p in PLAN_ORDER if p in selected_plans])
        .reset_index(name="churn_rate")
    )
    n_g = fdf.groupby("plan").size().reindex(plan_g["plan"])
    plan_g["n"] = n_g.values
    colors = [HIGHLIGHT_COLOR if p == "베이직" else MUTED_COLOR for p in plan_g["plan"]]
    fig = px.bar(
        plan_g, x="plan", y="churn_rate", text="churn_rate",
        hover_data={"n": True, "churn_rate": ":.1f"},
        title="요금제별 이탈률",
    )
    fig.update_traces(marker_color=colors, texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(yaxis_title="이탈률 (%)", xaxis_title=None, showlegend=False)
    st.plotly_chart(fig, width='stretch')

with col_region:
    region_g = (
        fdf.groupby("region")["churn_yn"]
        .apply(lambda s: (s == "Y").mean() * 100)
        .reset_index(name="churn_rate")
        .sort_values("churn_rate", ascending=False)
    )
    n_g = fdf.groupby("region").size().reindex(region_g["region"])
    region_g["n"] = n_g.values
    fig = px.bar(
        region_g, x="region", y="churn_rate", text="churn_rate",
        hover_data={"n": True, "churn_rate": ":.1f"},
        title="지역별 이탈률 (표본 작음 주의)",
    )
    fig.update_traces(marker_color=SINGLE_SERIES_COLOR, texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(yaxis_title="이탈률 (%)", xaxis_title=None, showlegend=False)
    st.plotly_chart(fig, width='stretch')

with col_tenure:
    if len(fdf) >= 20:
        tenure_df = fdf.copy()
        tenure_df["tenure_bucket"] = pd.qcut(tenure_df["tenure_years"], q=4, duplicates="drop")
        tenure_g = (
            tenure_df.groupby("tenure_bucket", observed=True)["churn_yn"]
            .apply(lambda s: (s == "Y").mean() * 100)
            .reset_index(name="churn_rate")
        )
        tenure_g["label"] = tenure_g["tenure_bucket"].apply(
            lambda iv: f"{iv.left:.1f}~{iv.right:.1f}년"
        )
        n_g = tenure_df.groupby("tenure_bucket", observed=True).size()
        tenure_g["n"] = n_g.values
        fig = px.bar(
            tenure_g, x="label", y="churn_rate", text="churn_rate",
            hover_data={"n": True, "churn_rate": ":.1f"},
            title="가입기간(4분위)별 이탈률",
        )
        fig.update_traces(marker_color=SINGLE_SERIES_COLOR, texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(yaxis_title="이탈률 (%)", xaxis_title=None, showlegend=False)
        st.plotly_chart(fig, width='stretch')
    else:
        st.info("표본이 부족해 가입기간 구간 차트를 생략합니다.")

# eta-squared 요약 (필터가 전체일 때만 참고 수치로 고정 표기)
overall_mean = profile["churn_yn"].eq("Y").astype(int).mean()
sst = ((profile["churn_yn"].eq("Y").astype(int) - overall_mean) ** 2).sum()
eta2 = {}
for col in ["plan", "region"]:
    ssb = (profile.groupby(col)["churn_yn"].transform(lambda s: (s == "Y").mean()) - overall_mean).pow(2).sum()
    eta2[col] = ssb / sst
tmp = profile.copy()
tmp["tenure_bucket_full"] = pd.qcut(tmp["tenure_years"], q=4)
ssb_tenure = (tmp.groupby("tenure_bucket_full", observed=True)["churn_yn"].transform(lambda s: (s == "Y").mean()) - overall_mean).pow(2).sum()
eta2["tenure_bucket"] = ssb_tenure / sst

st.caption(
    f"**전체 데이터 기준 설명력(eta²)**: 요금제 {eta2['plan']*100:.2f}% > "
    f"가입기간 {eta2['tenure_bucket']*100:.2f}% > 지역 {eta2['region']*100:.2f}%. "
    "요금제가 가장 크고 안정적인 차이를 만들고, 가입기간은 중간 시점(3~5년차)에 이탈률이 정점을 찍는 "
    "비선형 패턴을 보이며, 지역은 표본이 작아 노이즈일 가능성이 큽니다."
)

st.divider()

# ================= 3. 채널별 서비스 품질 =================
st.header("2. 상담 채널별 서비스 품질 — CSAT와 재문의율")

consultations, sat_joined = load_channel_summary(customers_attr)
consultations_f = apply_filters(consultations, selected_plans, selected_regions)
sat_f = apply_filters(sat_joined, selected_plans, selected_regions)

col_csat, col_recontact = st.columns(2)

with col_csat:
    csat_g = sat_f.groupby("channel")["csat"].mean().reset_index().sort_values("csat")
    fig = px.bar(
        csat_g, x="csat", y="channel", orientation="h", text="csat",
        title="채널별 평균 CSAT",
    )
    fig.update_traces(marker_color=SINGLE_SERIES_COLOR, texttemplate="%{text:.2f}", textposition="outside")
    fig.update_layout(xaxis_title="평균 CSAT (0~5)", yaxis_title=None)
    st.plotly_chart(fig, width='stretch')

with col_recontact:
    recontact_g = (
        consultations_f.groupby("channel")["is_recontact"]
        .apply(lambda s: (s == "Y").mean() * 100)
        .reset_index(name="recontact_rate")
        .sort_values("recontact_rate")
    )
    fig = px.bar(
        recontact_g, x="recontact_rate", y="channel", orientation="h", text="recontact_rate",
        title="채널별 재문의율",
    )
    fig.update_traces(marker_color=SINGLE_SERIES_COLOR, texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(xaxis_title="재문의율 (%)", yaxis_title=None)
    st.plotly_chart(fig, width='stretch')

st.divider()

# ================= 4. 이탈 vs 비이탈 경험 비교 =================
st.header("3. 이탈 고객은 실제로 다른 경험을 했는가")

churn_compare = fdf.groupby("churn_label", observed=True).agg(
    avg_csat=("avg_csat", "mean"),
    avg_nps=("avg_nps", "mean"),
    negative_voc_rate=("negative_voc_rate", "mean"),
).reset_index()
order = ["비이탈", "이탈"]
churn_compare["churn_label"] = pd.Categorical(churn_compare["churn_label"], categories=order, ordered=True)
churn_compare = churn_compare.sort_values("churn_label")
color_map = {"비이탈": STATUS_GOOD, "이탈": STATUS_CRITICAL}

col_a, col_b, col_c = st.columns(3)
metric_specs = [
    (col_a, "avg_csat", "평균 CSAT (0~5)", "{:.2f}"),
    (col_b, "avg_nps", "평균 NPS (0~10)", "{:.2f}"),
    (col_c, "negative_voc_rate", "VOC 부정비율 (%)", "{:.1f}%"),
]
for col, metric, ylabel, fmt in metric_specs:
    with col:
        fig = px.bar(
            churn_compare, x="churn_label", y=metric, text=metric, color="churn_label",
            color_discrete_map=color_map, title=ylabel,
        )
        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig, width='stretch')

st.caption(
    "재문의율·미해결율은 이탈 여부와 뚜렷한 관련이 없었지만, "
    "**CSAT·NPS·VOC 부정비율은 요금제와 무관하게 이탈 고객군에서 일관되게 나쁩니다.**"
)

st.divider()

# ================= 5. 이용량 감소 =================
st.header("4. 이용량 감소 — 이탈의 선행 신호")

col_usage_change, col_scatter = st.columns([1, 2])

with col_usage_change:
    usage_g = fdf.groupby("churn_label", observed=True)["data_gb_change_pct"].mean().reindex(order).reset_index()
    fig = px.bar(
        usage_g, x="churn_label", y="data_gb_change_pct", text="data_gb_change_pct",
        color="churn_label", color_discrete_map=color_map,
        title="하반기 이용량 변화율 (완전 재직월만)",
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title="변화율 (%)")
    st.plotly_chart(fig, width='stretch')

with col_scatter:
    scatter_df = fdf.dropna(subset=["avg_data_gb"])
    fig = px.scatter(
        scatter_df, x="tenure_months", y="avg_data_gb", color="plan",
        category_orders={"plan": PLAN_ORDER},
        color_discrete_map=PLAN_COLORS,
        trendline="ols",
        opacity=0.55,
        title="가입기간과 월평균 이용량의 관계 (요금제 통제)",
        labels={"tenure_months": "가입기간 (개월)", "avg_data_gb": "월평균 이용량 (GB)", "plan": "요금제"},
    )
    st.plotly_chart(fig, width='stretch')

st.caption(
    "이탈 고객은 이탈 전 마지막 완전한 재직월 기준으로도 이용량이 뚜렷이 줄어 있었습니다. "
    "또한 요금제를 통제하면 세 요금제 모두 가입기간이 길수록 이용량이 줄어드는 "
    "공통 패턴(r ≈ -0.6~-0.7)이 나타납니다 — 전체로 뭉치면 이 관계가 상쇄되어 보이지 않습니다."
)

st.divider()

# ================= 6. 결론 =================
st.header("5. 결론")
st.markdown(
    """
**근거** — 요금제별 이탈률은 최대 3.8배 차이 나지만 설명력(eta²)은 가장 크더라도 3%대에 그치고,
반면 CSAT·NPS·VOC 부정비율·이용량 감소는 요금제·지역과 무관하게 이탈 고객군에서 일관되게 나쁩니다.

**해석** — 이탈은 "저가 요금제라서" 또는 "특정 지역이라서" 생기는 문제가 아니라,
**서비스 경험(만족도·VOC·이용 감소)이 누적된 결과**로 보입니다. 가입기간도 3~5년차에 이탈 위험이
정점을 찍는 비선형 패턴을 보여, 단순히 "오래될수록" 위험한 것도 아닙니다.

**시사점** — 요금제·지역 기준의 일괄 대응보다, **CSAT/NPS 하락, VOC 부정 전환, 이용량 감소**를
동시에 추적하는 조기경보 지표를 만들어 3~5년차 고객군을 우선 모니터링하는 편이 더 효과적일 것입니다.
"""
)
