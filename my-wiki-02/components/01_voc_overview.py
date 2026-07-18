import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 한글 폰트 설정 (Windows 기본 한글 폰트)
font_path = "C:/Windows/Fonts/malgun.ttf"
if os.path.exists(font_path):
    font_name = "Malgun Gothic"
    plt.rcParams["font.family"] = font_name
    plt.rcParams["axes.unicode_minus"] = False
else:
    # 대체 폰트
    plt.rcParams["font.family"] = "Arial"
    plt.rcParams["axes.unicode_minus"] = False

# 데이터 읽기
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(base_dir, "raw", "data_voc.csv")
df = pd.read_csv(csv_path, encoding="utf-8-sig")

# 카테고리별 집계
category_stats = (
    df.groupby("category")
      .agg(total_count=("voc_id", "size"), negative_count=("sentiment", lambda s: (s == "부정").sum()))
      .reset_index()
      .sort_values("total_count", ascending=False)
)

# 월별 집계
monthly_stats = (
    df.assign(month=df["received_date"].str.slice(0, 7))
      .groupby("month")
      .agg(total_count=("voc_id", "size"), negative_count=("sentiment", lambda s: (s == "부정").sum()))
      .reset_index()
      .sort_values("month")
)

# 시각화: 2개 패널
fig, axes = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={"height_ratios": [1.15, 1]})

# ① 카테고리별 전체 건수 / 부정 건수
bars1 = axes[0].bar(category_stats["category"], category_stats["total_count"], color="#5DA5DA", alpha=0.8, label="전체 건수")
bars2 = axes[0].bar(category_stats["category"], category_stats["negative_count"], color="#E74C3C", alpha=0.9, label="부정 건수")
axes[0].set_title("카테고리별 VOC 전체 건수와 부정 건수", fontsize=14, weight="bold")
axes[0].set_ylabel("건수")
axes[0].legend()
axes[0].tick_params(axis="x", rotation=30)

# 막대 위 값 표시
for bars in [bars1, bars2]:
    for bar in bars:
        h = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2, h, int(h), ha="center", va="bottom", fontsize=9)

# ② 월별 추이
axes[1].plot(monthly_stats["month"], monthly_stats["total_count"], marker="o", linewidth=2.5, color="#4C78A8", label="전체 건수")
axes[1].plot(monthly_stats["month"], monthly_stats["negative_count"], marker="s", linewidth=2.5, color="#F58518", label="부정 건수")
axes[1].set_title("월별 VOC 전체 건수와 부정 건수 추이", fontsize=14, weight="bold")
axes[1].set_ylabel("건수")
axes[1].tick_params(axis="x", rotation=30)
axes[1].legend()

plt.tight_layout()

output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(output_dir, exist_ok=True)
out_path = os.path.join(output_dir, "01_voc_overview.png")
plt.savefig(out_path, dpi=300, bbox_inches="tight")
print(f"Saved: {out_path}")
plt.close(fig)
