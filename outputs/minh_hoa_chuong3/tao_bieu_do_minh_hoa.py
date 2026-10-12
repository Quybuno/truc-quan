"""Reproduce three notebook charts for Chapter 3 without embedded figure numbers.

Run from the project root:
    python outputs/minh_hoa_chuong3/tao_bieu_do_minh_hoa.py

The original datasets, notebook and step-5 figures remain unchanged. Plot logic,
style, axes and annotations follow the notebook's Pareto, scatter and area-boxplot
cells. Only the old "Hinh N." prefix is removed from each chart title, so LaTeX
can provide the report's figure numbering.
"""
from pathlib import Path
import hashlib
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, StrMethodFormatter, LogLocator
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs/minh_hoa_chuong3"
FIG = ROOT / "latex/figures/chuong3"
OUT.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)
DATA = ROOT / "data/analysis/loi_thep_phan_tich.csv"
STATS = ROOT / "outputs/buoc_5"
NOTEBOOK = ROOT / "buoc_1_2_3_4_5_6_loi_be_mat_thep.ipynb"
protected = [DATA, NOTEBOOK, STATS / "co_cau_loi.csv",
             STATS / "tuong_quan_do_sang.csv", STATS / "thong_ke_dien_tich.csv"]
protected += list((STATS / "hinh").glob("*.png"))
protected += list((STATS / "hinh").glob("*.svg"))
before = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
          for p in protected}

d = pd.read_csv(DATA)
co_cau_loi = pd.read_csv(STATS / "co_cau_loi.csv")
so_ban_ghi = len(d)
assert so_ban_ghi == 1941
THU_TU_LOI = co_cau_loi["Fault_Type_Clean"].tolist()
co_mau_loi = d["Fault_Type_Clean"].value_counts()
assert co_mau_loi.reindex(THU_TU_LOI).to_list() == co_cau_loi["Count"].to_list()
np.testing.assert_allclose(co_cau_loi["Percent"],
                           co_cau_loi["Count"] / so_ban_ghi * 100)
np.testing.assert_allclose(co_cau_loi["Cumulative_Percent"],
                           co_cau_loi["Count"].cumsum() / so_ban_ghi * 100)
cot_min = "Minimum_of_Luminosity"
cot_max = "Maximum_of_Luminosity"
pearson_chung = d[cot_min].corr(d[cot_max])
saved_corr = pd.read_csv(STATS / "tuong_quan_do_sang.csv")
np.testing.assert_allclose(pearson_chung, saved_corr.iloc[0]["Pearson_r"])
assert d["Pixels_Areas"].gt(0).all()
area_stats = pd.read_csv(STATS / "thong_ke_dien_tich.csv").set_index("Fault_Type_Clean")
for label, group in d.groupby("Fault_Type_Clean"):
    area = group["Pixels_Areas"]
    np.testing.assert_allclose(
        [len(area), area.median(), area.quantile(.25), area.quantile(.75)],
        area_stats.loc[label, ["N", "Median", "Q1", "Q3"]].to_numpy(dtype=float))

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11,
    "axes.titlesize": 15, "axes.labelsize": 11,
    "figure.dpi": 120, "savefig.dpi": 300,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.unicode_minus": False, "svg.fonttype": "none",
})
MAU_LOI = {"Other_Faults": "#737373", "Bumps": "#0072B2", "K_Scatch": "#E69F00",
           "Z_Scratch": "#9B59B6", "Pastry": "#009E73", "Stains": "#D55E00", "Dirtiness": "#8C564B"}
manifest = []


def save_chart(fig, name, question, note, notebook_title):
    fig.text(0.01, 0.01, note, fontsize=9, color="#555555", va="bottom")
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    paths = []
    for extension in ("png", "svg"):
        path = FIG / f"{name}.{extension}"
        fig.savefig(path, bbox_inches="tight", facecolor="white")
        paths.append(str(path.relative_to(ROOT)))
    plt.close(fig)
    manifest.append({"name": name, "question": question, "files": paths,
                     "source_notebook_title": notebook_title,
                     "change": "Remove embedded figure-number prefix only",
                     "scope": note})


# Q1: count bars with cumulative percentage on a separate right-hand axis.
fig, ax = plt.subplots(figsize=(11, 6))
x = np.arange(len(co_cau_loi))
ax.bar(x, co_cau_loi["Count"], color=[MAU_LOI[nhan] for nhan in THU_TU_LOI])
ax.set_xticks(x, THU_TU_LOI, rotation=20, ha="right")
ax.set(title="Pareto số bản ghi lỗi", xlabel="Loại lỗi, sắp theo số lượng giảm dần", ylabel="Số bản ghi lỗi")
ax.set_ylim(0, co_cau_loi["Count"].max() * 1.3)
ax.grid(axis="y", alpha=0.2)
ax.set_axisbelow(True)
ax_luy_ke = ax.twinx()
ax_luy_ke.plot(x, co_cau_loi["Cumulative_Percent"], color="#202020", marker="o", label="Tỷ trọng lũy kế")
ax_luy_ke.axhline(80, color="#888888", linestyle="--", linewidth=1, label="Mốc tham khảo 80%")
ax_luy_ke.set_ylim(0, 105)
ax_luy_ke.set_ylabel("Tỷ trọng lũy kế (%)")
ax_luy_ke.yaxis.set_major_formatter(PercentFormatter(100))
for vi_tri, ty_trong in enumerate(co_cau_loi["Cumulative_Percent"]):
    ax_luy_ke.annotate(f"{ty_trong:.1f}%", (vi_tri, ty_trong), xytext=(0, 9), textcoords="offset points", ha="center", fontsize=9)
ax_luy_ke.legend(loc="upper left", fontsize=9)
save_chart(fig, "07_pareto_loi", "Q1",
           f"Nguồn: bảng lỗi đối chiếu UCI | n={so_ban_ghi:,} | Lũy kế theo số lượng, không theo thiệt hại",
           "Hình 2. Pareto số bản ghi lỗi")

# Q3: actual observations; translucent points and original per-label colors.
fig, ax = plt.subplots(figsize=(11, 7))
for nhan in THU_TU_LOI:
    nhom = d.loc[d["Fault_Type_Clean"].eq(nhan)]
    ax.scatter(nhom[cot_min], nhom[cot_max], s=22, alpha=0.35, color=MAU_LOI[nhan],
               edgecolors="none", label=f"{nhan} (n={len(nhom):,})")
ax.set(title=f"Độ sáng nhỏ nhất và lớn nhất | Pearson r={pearson_chung:.4f}",
       xlabel="Độ sáng nhỏ nhất (thang đo nguồn)", ylabel="Độ sáng lớn nhất (thang đo nguồn)")
ax.grid(alpha=0.2)
ax.set_axisbelow(True)
ax.legend(title="Loại lỗi", bbox_to_anchor=(1.02, 1), loc="upper left", markerscale=1.6, fontsize=10)
save_chart(fig, "08_scatter_do_sang", "Q3",
           f"Nguồn: bảng lỗi đối chiếu UCI | n={so_ban_ghi:,} | Mỗi điểm là một bản ghi; các điểm có thể chồng lên nhau",
           f"Hình 5. Độ sáng nhỏ nhất và lớn nhất | Pearson r={pearson_chung:.4f}")

# Q5: compute boxes/whiskers from untransformed areas, then set the display log axis.
du_lieu_hop = [d.loc[d["Fault_Type_Clean"].eq(nhan), "Pixels_Areas"] for nhan in THU_TU_LOI]
fig, ax = plt.subplots(figsize=(11, 6))
hop = ax.boxplot(du_lieu_hop, vert=False, patch_artist=True, whis=1.5,
                 medianprops={"color": "black", "linewidth": 1.5},
                 flierprops={"marker": ".", "markersize": 4, "alpha": 0.5})
for nhan, than_hop, diem_ngoai in zip(THU_TU_LOI, hop["boxes"], hop["fliers"]):
    than_hop.set_facecolor(MAU_LOI[nhan])
    than_hop.set_alpha(0.75)
    diem_ngoai.set_markeredgecolor(MAU_LOI[nhan])
ax.set_xscale("log")
ax.xaxis.set_major_locator(LogLocator(base=10))
ax.xaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
ax.set_yticks(np.arange(1, 8), [f"{nhan} (n={co_mau_loi[nhan]:,})" for nhan in THU_TU_LOI])
ax.invert_yaxis()
ax.set(title="Phân bố diện tích theo loại lỗi", xlabel="Pixels_Areas (giá trị nguồn; trục log cơ số 10)", ylabel="Loại lỗi và cỡ mẫu")
ax.grid(axis="x", which="major", alpha=0.2)
save_chart(fig, "09_boxplot_dien_tich_log", "Q5",
           f"Nguồn: bảng lỗi đối chiếu UCI | n={so_ban_ghi:,} | Boxplot tính trên thang gốc; trục log; giữ mọi bản ghi",
           "Hình 7. Phân bố diện tích theo loại lỗi")

after = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
         for p in protected}
assert before == after, "An original input or step-5 chart changed"
report = {"input": str(DATA.relative_to(ROOT)), "N": so_ban_ghi,
          "counts": {k: int(v) for k, v in co_mau_loi.items()},
          "pearson_r": float(pearson_chung), "charts": manifest,
          "original_files_unchanged": before == after,
          "original_file_sha256": before}
(OUT / "manifest_bieu_do.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"N": so_ban_ghi, "charts": [item["name"] for item in manifest],
                  "original_files_unchanged": before == after}, ensure_ascii=True))
