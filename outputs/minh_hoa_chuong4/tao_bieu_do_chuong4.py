"""Create Chapter 4 result charts from the project's actual cleaned data.

Run from the project root:
    python outputs/minh_hoa_chuong4/tao_bieu_do_chuong4.py

The PNGs are 300 dpi and the SVGs retain editable text. The generator writes only
new Chapter 4 figures and their data/manifest; hashes guard the original data,
notebook, step-5 statistics and earlier illustrations.
"""
from pathlib import Path
import hashlib
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter, LogLocator, PercentFormatter
import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs/minh_hoa_chuong4"
FIG = ROOT / "latex/figures/chuong4"
OUT.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)
DATA = ROOT / "data/analysis/loi_thep_phan_tich.csv"
STATS = ROOT / "outputs/buoc_5"
protected = [DATA, ROOT / "buoc_1_2_3_4_5_6_loi_be_mat_thep.ipynb",
             ROOT / "data/raw/practice/data_chua_sach_ko_sua.xlsx",
             ROOT / "data/raw/uci/steel_plates_faults_original.csv"]
protected += list(STATS.glob("*.csv"))
protected += list((STATS / "hinh").glob("*"))
protected += list((ROOT / "latex/figures/chuong3").glob("*"))
before = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
          for p in protected if p.is_file()}

d = pd.read_csv(DATA)
counts = pd.read_csv(STATS / "co_cau_loi.csv")
labels = counts["Fault_Type_Clean"].to_list()
N = len(d)
assert N == 1941
assert set(d["Steel_Type"]) == {"A300", "A400"}
assert not d["Fault_Type_Clean"].isna().any()
np.testing.assert_array_equal(
    d["Fault_Type_Clean"].value_counts().reindex(labels), counts["Count"])
np.testing.assert_allclose(counts["Percent"], counts["Count"] / N * 100)
steel_counts = d["Steel_Type"].value_counts()
assert steel_counts.to_dict() == {"A400": 1164, "A300": 777}
cross = pd.crosstab(d["Fault_Type_Clean"], d["Steel_Type"]).reindex(
    index=labels, columns=["A300", "A400"], fill_value=0)
within_steel = cross.div(cross.sum(axis=0), axis=1) * 100
np.testing.assert_allclose(within_steel.sum(axis=0), 100)


def summaries(variable):
    return d.groupby("Fault_Type_Clean")[variable].agg(
        N="size", Q1=lambda x: x.quantile(.25), Median="median",
        Q3=lambda x: x.quantile(.75)).reindex(labels)


brightness = summaries("Minimum_of_Luminosity")
area = summaries("Pixels_Areas")
saved_brightness = pd.read_csv(STATS / "dau_hieu_do_sang.csv").set_index("Fault_Type_Clean")
saved_area = pd.read_csv(STATS / "thong_ke_dien_tich.csv").set_index("Fault_Type_Clean")
for computed, saved in [(brightness, saved_brightness), (area, saved_area)]:
    np.testing.assert_allclose(computed[["N", "Q1", "Median", "Q3"]],
                               saved.reindex(labels)[["N", "Q1", "Median", "Q3"]])
saved_thickness = pd.read_csv(STATS / "do_day_theo_nhan_thep.csv").set_index(
    ["Fault_Type_Clean", "Steel_Type"])
for (label, steel), group in d.groupby(["Fault_Type_Clean", "Steel_Type"]):
    values = group["Steel_Plate_Thickness"]
    np.testing.assert_allclose(
        [len(values), values.quantile(.25), values.median(), values.quantile(.75)],
        saved_thickness.loc[(label, steel), ["N", "Q1", "Median", "Q3"]].to_numpy(dtype=float))
assert d["Pixels_Areas"].gt(0).all()

COLORS = {"Other_Faults": "#737373", "Bumps": "#0072B2", "K_Scatch": "#E69F00",
          "Z_Scratch": "#9B59B6", "Pastry": "#009E73", "Stains": "#D55E00", "Dirtiness": "#8C564B"}
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11.5,
    "axes.titlesize": 14, "axes.labelsize": 11.5,
    "figure.dpi": 120, "savefig.dpi": 300,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.unicode_minus": False, "svg.fonttype": "none",
})
integer_fmt = FuncFormatter(lambda x, _: f"{x:,.0f}".replace(",", "."))
manifest = []


def save(fig, name, question, note, formula, table):
    fig.text(.01, .015, note, fontsize=9, color="#555555", va="bottom")
    paths = []
    for ext in ["png", "svg"]:
        path = FIG / f"{name}.{ext}"
        fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
        paths.append(str(path.relative_to(ROOT)))
    plt.close(fig)
    table_path = OUT / f"{name}.csv"
    table.to_csv(table_path, index=False, encoding="utf-8-sig")
    manifest.append({"name": name, "question": question, "files": paths,
                     "data": str(table_path.relative_to(ROOT)),
                     "formula": formula, "scope": note,
                     "embedded_figure_number": False})


# Q1: counts and proportions across the complete set of defect records.
fig, ax = plt.subplots(figsize=(8.6, 4.8))
positions = np.arange(7)
ax.barh(positions, counts["Count"], color=[COLORS[label] for label in labels], height=.7)
ax.set_yticks(positions, labels)
ax.invert_yaxis()
ax.set_xlim(0, 840)
ax.set(title="Cơ cấu bản ghi lỗi bề mặt thép", xlabel="Số bản ghi lỗi", ylabel="Loại lỗi")
ax.xaxis.set_major_formatter(integer_fmt)
ax.grid(axis="x", alpha=.18)
ax.set_axisbelow(True)
for i, row in counts.iterrows():
    percent = f"{row['Percent']:.2f}".replace(".", ",")
    ax.text(row["Count"] + 8, i, f"{int(row['Count'])} | {percent}%", va="center", fontsize=10.5)
fig.tight_layout(rect=(0, .07, 1, 1))
save(fig, "01_co_cau_loi", "Q1",
     "Nguồn: bảng lỗi đã đối chiếu UCI | Mẫu số: 1.941 bản ghi lỗi; chưa có số sản phẩm đạt chất lượng.",
     "Count by label; Percent = Count / 1941 * 100", counts)

# Q2a: absolute counts; steel class is encoded by hatch, label by color.
fig, ax = plt.subplots(figsize=(8.6, 4.8))
x = np.arange(7)
for j, steel in enumerate(["A300", "A400"]):
    xpos = x + (j - .5) * .37
    bars = ax.bar(xpos, cross[steel], width=.35,
                  color=[COLORS[label] for label in labels],
                  edgecolor="#444444", linewidth=.6, hatch="///" if j == 0 else None)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 7,
                str(int(bar.get_height())), ha="center", va="bottom", fontsize=9.5)
ax.set_xticks(x, labels, rotation=20, ha="right")
ax.set_ylim(0, 500)
ax.set(title="Số bản ghi lỗi theo dòng thép", xlabel="Loại lỗi", ylabel="Số bản ghi lỗi")
ax.grid(axis="y", alpha=.18)
ax.set_axisbelow(True)
ax.legend(handles=[Patch(facecolor="white", edgecolor="#444444", hatch="///", label="A300 (n=777)"),
                   Patch(facecolor="#dddddd", edgecolor="#444444", label="A400 (n=1.164)")],
          title="Dòng thép", loc="upper right", fontsize=10)
fig.tight_layout(rect=(0, .07, 1, 1))
save(fig, "02_loi_theo_thep_so_luong", "Q2",
     "Nguồn: bảng lỗi đã đối chiếu UCI | n=1.941; màu: nhãn lỗi, họa tiết: dòng thép.",
     "Count = cross-tab of defect label and steel type", cross.reset_index())

# Q2b: composition within each steel type, not the distribution within each label.
fig, ax = plt.subplots(figsize=(8.6, 4.8))
bottom = np.zeros(2)
for label in labels:
    vals = within_steel.loc[label].to_numpy()
    ax.bar([0, 1], vals, bottom=bottom, color=COLORS[label], width=.55, label=label)
    for j, value in enumerate(vals):
        if value >= 5:
            color = "#202020" if label == "K_Scatch" else "white"
            ax.text(j, bottom[j] + value / 2, f"{value:.1f}%".replace(".", ","),
                    ha="center", va="center", color=color, fontsize=11)
    bottom += vals
ax.set_xticks([0, 1], ["A300 (n=777)", "A400 (n=1.164)"])
ax.set_ylim(0, 100)
ax.set_xlim(-.6, 1.6)
ax.yaxis.set_major_formatter(PercentFormatter(100))
ax.set(title="Cơ cấu nhãn lỗi trong từng dòng thép", xlabel="Dòng thép", ylabel="Tỷ trọng trong dòng thép (%)")
ax.legend(title="Loại lỗi", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=10)
fig.tight_layout(rect=(0, .07, 1, 1))
save(fig, "03_co_cau_trong_dong_thep", "Q2",
     "Mẫu số: A300=777; A400=1.164 bản ghi lỗi. Mỗi cột=100%; phần dưới 5% không in nhãn.",
     "Percent within steel = cross-tab count / number of defect records in that steel type * 100",
     within_steel.reset_index())

# Q3: show the operational criterion as intervals rather than claiming all-point separation.
brightness_order = brightness.sort_values("Median").index.to_list()
fig, ax = plt.subplots(figsize=(8.6, 4.8))
for i, label in enumerate(brightness_order):
    row = brightness.loc[label]
    ax.hlines(i, row["Q1"], row["Q3"], color=COLORS[label], linewidth=10, alpha=.8)
    ax.plot(row["Median"], i, "o", color="#202020", markersize=5.5)
ax.set_yticks(range(7), [f"{label} (n={int(brightness.loc[label, 'N'])})" for label in brightness_order])
ax.invert_yaxis()
ax.set_xlim(20, 130)
ax.set(title="Khoảng P25–P75 của độ sáng tối thiểu theo nhãn",
       xlabel="Minimum_of_Luminosity (thang đo nguồn)", ylabel="Loại lỗi và cỡ mẫu")
ax.grid(axis="x", alpha=.18)
ax.set_axisbelow(True)
fig.tight_layout(rect=(0, .07, 1, 1))
save(fig, "04_iqr_do_sang_toi_thieu", "Q3",
     "n=1.941 | Đoạn màu: P25–P75; chấm: trung vị. Khoảng này chỉ mô tả 50% trung tâm mỗi nhãn.",
     "Linear quantiles at p=.25 and .75, and median; labels ordered by median ascending",
     brightness.loc[brightness_order].reset_index())

# Q4: the two steel classes are separated; each cell retains its actual N.
fig, axes = plt.subplots(2, 1, figsize=(8.6, 8.25), sharex=True)
for ax, steel in zip(axes, ["A300", "A400"]):
    vals, ns = [], []
    for label in labels:
        group = d.loc[d["Fault_Type_Clean"].eq(label) & d["Steel_Type"].eq(steel), "Steel_Plate_Thickness"]
        vals.append(group.to_numpy())
        ns.append(len(group))
    # Groups with one observation are plotted as points, rather than implying an estimable spread.
    for i, (label, values) in enumerate(zip(labels, vals), start=1):
        if len(values) == 1:
            ax.plot(values[0], i, "D", color=COLORS[label], markersize=5, zorder=4)
        else:
            box = ax.boxplot([values], positions=[i], vert=False, widths=.6,
                             patch_artist=True, whis=1.5,
                             medianprops={"color": "black", "linewidth": 1.5},
                             flierprops={"marker": ".", "markersize": 4, "alpha": .5,
                                         "markeredgecolor": COLORS[label]})
            box["boxes"][0].set_facecolor(COLORS[label])
            box["boxes"][0].set_alpha(.75)
    ax.set_yticks(range(1, 8), [f"{label} (n={n})" for label, n in zip(labels, ns)])
    ax.invert_yaxis()
    ax.set_ylim(7.6, .4)
    ax.set_title(f"{steel} — {int(steel_counts[steel]):,} bản ghi lỗi".replace(",", "."), fontsize=13)
    ax.set_xlim(30, 310)
    ax.set_xticks([40, 80, 120, 160, 200, 240, 280, 300])
    ax.grid(axis="x", alpha=.18)
    ax.set_axisbelow(True)
axes[1].set_xlabel("Steel_Plate_Thickness (giá trị nguồn; chưa xác nhận đơn vị)")
fig.suptitle("Phân bố độ dày theo nhãn và dòng thép", fontsize=15, y=.985)
fig.tight_layout(rect=(0, .065, 1, .96), h_pad=2)
save(fig, "05_do_day_theo_nhan_va_thep", "Q4",
     "Hộp: P25–P75; râu: 1,5 IQR trong nhóm. ♦: nhóm n=1, không so sánh độ phân tán. Giữ mọi bản ghi.",
     "Separate raw-scale boxplots by label × steel type; whiskers 1.5 IQR; singleton groups drawn as diamonds",
     saved_thickness.reset_index())

# Q5: quantiles computed on original areas; only the display axis is logarithmic.
area_order = area.sort_values("Median").index.to_list()
fig, ax = plt.subplots(figsize=(8.6, 4.8))
for i, label in enumerate(area_order):
    row = area.loc[label]
    ax.hlines(i, row["Q1"], row["Q3"], color=COLORS[label], linewidth=10, alpha=.8)
    ax.plot(row["Median"], i, "o", color="#202020", markersize=5.5)
ax.set_yticks(range(7), [f"{label} (n={int(area.loc[label, 'N'])})" for label in area_order])
ax.invert_yaxis()
ax.set_xscale("log")
ax.set_xlim(10, 16000)
ax.xaxis.set_major_locator(LogLocator(base=10))
ax.xaxis.set_major_formatter(integer_fmt)
ax.set(title="Khoảng P25–P75 của diện tích theo nhãn",
       xlabel="Pixels_Areas (giá trị nguồn; trục log cơ số 10)", ylabel="Loại lỗi và cỡ mẫu")
ax.grid(axis="x", which="major", alpha=.18)
ax.set_axisbelow(True)
fig.tight_layout(rect=(0, .07, 1, 1))
save(fig, "06_iqr_dien_tich", "Q5",
     "n=1.941 | Đoạn màu: P25–P75; chấm: trung vị. Thống kê tính trên thang gốc; trục log chỉ để hiển thị.",
     "Linear original-scale quantiles at p=.25 and .75, median; display x-axis logarithmic base 10",
     area.loc[area_order].reset_index())

after = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
         for p in protected if p.is_file()}
assert before == after, "An original input or earlier output changed"
report = {"input": str(DATA.relative_to(ROOT)), "N": N,
          "original_files_unchanged": before == after,
          "original_file_sha256": before,
          "steel_sample_sizes": {key: int(value) for key, value in steel_counts.items()},
          "quantile_interpolation": "linear", "png_dpi": 300,
          "charts": manifest}
(OUT / "manifest_bieu_do.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"N": N, "charts": [item["name"] for item in manifest],
                  "original_files_unchanged": before == after}, ensure_ascii=False))
