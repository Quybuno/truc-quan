"""Create and insert the eight analytical figures specified in the supplied chapter.

Run from the project root. Source data are read only; original TeX files are backed
up before the first replacement. Dashboard screenshots remain explicit pending
items because a real browser capture was unavailable.
"""
from pathlib import Path
import hashlib
import json
import re
import shutil
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter, MultipleLocator
import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
FIG = ROOT / "latex/figures/chuong4"
OUT = ROOT / "outputs/minh_hoa_chuong4/anh_da_ghep"
BACKUP = ROOT / "tmp/pdfs/truoc_ghep_anh_chuong4"
for folder in (FIG, OUT, BACKUP):
    folder.mkdir(parents=True, exist_ok=True)
ATTACHMENT = Path(r"C:\Users\Admin\.codex\attachments\f95a1186-76e3-418b-8046-a990e3f180e8\Pasted text.txt")
DATA = ROOT / "data/analysis/loi_thep_phan_tich.csv"
data_hash = hashlib.sha256(DATA.read_bytes()).hexdigest()
d = pd.read_csv(DATA)
LABEL = "Fault_Type_Clean"
K = "K_Scatch"
PRIMARY, SECONDARY, GRAY = "#D55E00", "#0072B2", "#BDBDBD"
counts = d[LABEL].value_counts()
labels = counts.index.to_list()
assert len(d) == 1941 and len(labels) == 7
assert counts.to_dict() == {"Other_Faults": 673, "Bumps": 402, K: 391,
                           "Z_Scratch": 190, "Pastry": 158, "Stains": 72, "Dirtiness": 55}
cross = pd.crosstab(d[LABEL], d["Steel_Type"]).reindex(labels)
assert cross.sum().to_dict() == {"A300": 777, "A400": 1164}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 13,
                     "axes.labelsize": 13, "xtick.labelsize": 11.5,
                     "ytick.labelsize": 12, "legend.fontsize": 11,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "axes.unicode_minus": False, "savefig.dpi": 300,
                     "svg.fonttype": "none"})


def vn(value, decimals=0):
    return f"{value:,.{decimals}f}".replace(",", "_").replace(".", ",").replace("_", ".")


def base(ax, axis="y"):
    ax.grid(axis=axis, alpha=.2)
    ax.set_axisbelow(True)
    ax.tick_params(length=0, pad=8)


manifest = []


def save(fig, name, note, table):
    fig.text(.015, .018, note, fontsize=10, color="#555555", va="bottom")
    for ext in ("png", "svg"):
        fig.savefig(FIG / f"{name}.{ext}", bbox_inches="tight", facecolor="white", dpi=300)
    plt.close(fig)
    table.to_csv(OUT / f"{name}.csv", index=False, encoding="utf-8-sig")
    manifest.append({"figure": name, "image": f"figures/chuong4/{name}.png", "note": note})


# 4.1: counts and cumulative share, with the 80% reference on the right axis.
fig, ax = plt.subplots(figsize=(9, 5.3))
x = np.arange(7)
colors = [PRIMARY if label == K else SECONDARY if i < 2 else GRAY
          for i, label in enumerate(labels)]
bars = ax.bar(x, counts, color=colors, width=.66)
ax.set_xticks(x, labels, rotation=22, ha="right")
ax.set_ylabel("Số bản ghi lỗi")
ax.set_ylim(0, 790)
base(ax)
for bar in bars:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+10,
            str(int(bar.get_height())), ha="center", fontsize=11.5)
right = ax.twinx()
cum = counts.cumsum() / len(d) * 100
right.plot(x, cum, color="#333333", marker="o", lw=1.8, markersize=5)
right.axhline(80, color="#777777", ls="--", lw=1.1)
right.set_ylim(0, 108)
right.set_ylabel("Tỷ trọng lũy kế (%)")
right.yaxis.set_major_locator(MultipleLocator(20))
right.annotate("75,53%", (2, cum.iloc[2]), xytext=(1.25, 92),
               arrowprops={"arrowstyle": "-", "color": "#666666"},
               fontsize=11.5, bbox={"facecolor": "white", "edgecolor": "none", "alpha": .95})
right.annotate("85,32%\nvượt 80%", (3, cum.iloc[3]), xytext=(3.4, 61),
               arrowprops={"arrowstyle": "-", "color": "#666666"}, fontsize=11.5,
               bbox={"facecolor": "white", "edgecolor": "none", "alpha": .95})
ax.text(.99, .98, "N = 1.941", transform=ax.transAxes, ha="right", va="top", fontsize=11.5)
fig.tight_layout(rect=(0, .09, 1, 1))
save(fig, "ch4_01_pareto", "Mẫu số: 1.941 bản ghi lỗi. Đường nét đứt: mốc 80% trên trục lũy kế.",
     pd.DataFrame({LABEL: labels, "Count": counts.values, "Percent": counts.values / len(d)*100,
                   "Cumulative_Percent": cum.values}))

# 4.2: absolute count by steel, keeping singleton observations visible.
fig, ax = plt.subplots(figsize=(9, 5.3))
for j, steel in enumerate(("A300", "A400")):
    cs = [PRIMARY if label == K else SECONDARY if label in ("Z_Scratch", "Stains") else GRAY
          for label in labels]
    bars = ax.bar(x + (j-.5)*.37, cross[steel], width=.35, color=cs,
                  edgecolor="#555555", linewidth=.5, hatch="///" if j == 0 else None)
    for bar in bars:
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+6,
                str(int(bar.get_height())), ha="center", va="bottom", fontsize=10.5)
ax.set_xticks(x, labels, rotation=22, ha="right")
ax.set_ylim(0, 465)
ax.set_ylabel("Số bản ghi lỗi")
base(ax)
ax.legend(handles=[Patch(facecolor="white", edgecolor="#555555", hatch="///", label="A300 (n = 777)"),
                   Patch(facecolor=GRAY, edgecolor="#555555", label="A400 (n = 1.164)")],
          loc="upper right", frameon=False)
fig.tight_layout(rect=(0, .09, 1, 1))
save(fig, "ch4_02_thep_so_luong", "Màu nhấn: K_Scatch; xanh: Z_Scratch và Stains. Họa tiết phân biệt dòng thép.", cross.reset_index())

# 4.3: composition within each steel, with a denominator for each bar.
shares = cross.div(cross.sum(axis=0), axis=1) * 100
palette = {K: PRIMARY, "Bumps": SECONDARY, "Other_Faults": "#636363",
           "Z_Scratch": "#969696", "Pastry": "#BDBDBD", "Stains": "#D9D9D9", "Dirtiness": "#EFEFEF"}
fig, ax = plt.subplots(figsize=(9, 4.1))
left = np.zeros(2)
for label in labels:
    values = shares.loc[label, ["A300", "A400"]].to_numpy()
    ax.barh([0, 1], values, left=left, height=.6, color=palette[label], edgecolor="white", linewidth=.7)
    for row, value in enumerate(values):
        if value >= 9:
            title = f"{label}\n{vn(value, 2)}%" if label in (K, "Bumps", "Other_Faults") else f"{vn(value, 2)}%"
            ax.text(left[row]+value/2, row, title, ha="center", va="center", fontsize=11,
                    color="white" if label in (K, "Bumps", "Other_Faults", "Z_Scratch") else "#222222")
    left += values
ax.set_yticks([0, 1], ["A300\nn = 777", "A400\nn = 1.164"])
ax.set_ylim(1.7, -.65)
ax.set_xlim(0, 100)
ax.set_xlabel("Tỷ trọng trong từng dòng thép (%)")
ax.xaxis.set_major_locator(MultipleLocator(20))
ax.legend(handles=[Patch(facecolor=palette[label], label=label) for label in labels],
          loc="lower left", bbox_to_anchor=(-.01, -.48), ncol=4, frameon=False,
          columnspacing=1.2, handlelength=1.2)
base(ax, "x")
fig.subplots_adjust(left=.13, right=.99, top=.98, bottom=.37)
save(fig, "ch4_03_thep_ty_trong", "Mẫu số: A300 = 777; A400 = 1.164. Tỷ trọng mô tả cơ cấu của các bản ghi lỗi.", shares.reset_index())

# 4.4: grey background points followed by the highlighted class.
fig, ax = plt.subplots(figsize=(9, 5.5))
other, k = d.loc[d[LABEL].ne(K)], d.loc[d[LABEL].eq(K)]
ax.scatter(other["Minimum_of_Luminosity"], other["Maximum_of_Luminosity"],
           color="#A8A8A8", alpha=.25, s=19, edgecolors="none", label="Các nhãn khác (n = 1.550)")
ax.scatter(k["Minimum_of_Luminosity"], k["Maximum_of_Luminosity"],
           color=PRIMARY, alpha=.7, s=20, edgecolors="none", label="K_Scatch (n = 391)")
corr = d["Minimum_of_Luminosity"].corr(d["Maximum_of_Luminosity"])
assert abs(corr-.4296) < .00005
ax.set(xlabel="Minimum_of_Luminosity (thang nguồn)", ylabel="Maximum_of_Luminosity (thang nguồn)",
       xlim=(-5, 215), ylim=(30, 265))
ax.legend(loc="lower right", frameon=True, facecolor="white", framealpha=.9)
ax.text(.02, .96, f"Pearson toàn tập: r = {vn(corr, 4)}", transform=ax.transAxes, va="top", fontsize=11.5)
ax.annotate("Dải K_Scatch ở Min 20-50", (38, 141), xytext=(5, 215),
            arrowprops={"arrowstyle": "->", "color": PRIMARY}, fontsize=11.5, color=PRIMARY)
ax.annotate("Một phần K_Scatch\nvẫn có Min cao", (170, 198), xytext=(111, 248),
            arrowprops={"arrowstyle": "->", "color": PRIMARY}, fontsize=11.5, color=PRIMARY)
base(ax, "both")
fig.tight_layout(rect=(0, .09, 1, 1))
save(fig, "ch4_04_scatter_do_sang", "Giữ toàn bộ quan sát; độ sáng tối thiểu và tối đa của các nhóm vẫn có vùng chồng lấn.",
     d[[LABEL, "Minimum_of_Luminosity", "Maximum_of_Luminosity"]])

# 4.5: central intervals, with the fifteen-unit separation shaded.
bright = d.groupby(LABEL)["Minimum_of_Luminosity"].agg(
    N="size", Q1=lambda s: s.quantile(.25), Median="median", Q3=lambda s: s.quantile(.75)).sort_values("Median")
assert bright.loc[K, ["Q1", "Median", "Q3"]].to_list() == [35, 41, 49]
fig, ax = plt.subplots(figsize=(9, 5))
ax.axvspan(49, 64, color="#FFE5D6", alpha=.65)
for i, (label, row) in enumerate(bright.iterrows()):
    color = PRIMARY if label == K else GRAY
    ax.hlines(i, row.Q1, row.Q3, color=color, lw=9)
    ax.plot(row.Median, i, "o", color="#303030", ms=6)
    if label == K:
        ax.text(row.Median, i+.34, "35-49; trung vị 41", color=PRIMARY, fontsize=11.5, ha="center")
ax.text(56.5, -.65, "Khoảng trống\n15 đơn vị", ha="center", fontsize=11, color=PRIMARY)
ax.set_yticks(np.arange(7), [f"{label} (n = {int(row.N)})" for label, row in bright.iterrows()])
ax.set_ylim(6.6, -1.05)
ax.set_xlim(20, 130)
ax.set_xlabel("Minimum_of_Luminosity (thang nguồn)")
base(ax, "x")
fig.tight_layout(rect=(0, .09, 1, 1))
save(fig, "ch4_05_iqr_do_sang", "Đoạn: P25-P75; chấm: trung vị. Chỉ mô tả 50% trung tâm; toàn phạm vi vẫn chồng lấn.", bright.reset_index())

# 4.6: two adjacent panels; singletons are actual points, not boxes.
fig, axes = plt.subplots(1, 2, figsize=(12.2, 6.3), sharex=True)
thickness_rows = []
for ax, steel in zip(axes, ("A300", "A400")):
    ns = []
    for i, label in enumerate(labels):
        values = d.loc[d[LABEL].eq(label) & d["Steel_Type"].eq(steel), "Steel_Plate_Thickness"].to_numpy()
        ns.append(len(values))
        color = PRIMARY if label == K else SECONDARY if label in ("Bumps", "Other_Faults") else GRAY
        if len(values) == 1:
            ax.plot(values[0], i, "D", color=color, ms=7)
            ax.text(values[0]+12, i-.16, "n = 1", fontsize=11)
        else:
            box = ax.boxplot([values], positions=[i], vert=False, widths=.52, patch_artist=True,
                             medianprops={"color": "#222222", "lw": 1.6},
                             boxprops={"edgecolor": color}, whiskerprops={"color": color},
                             capprops={"color": color},
                             flierprops={"marker": ".", "markersize": 4, "markeredgecolor": color, "alpha": .55})
            box["boxes"][0].set_facecolor(color)
            box["boxes"][0].set_alpha(.8)
        thickness_rows.append({LABEL: label, "Steel_Type": steel, "N": len(values), "Median": np.median(values)})
    ax.set_yticks(np.arange(7), [f"{label} (n={n})" for label, n in zip(labels, ns)], fontsize=15)
    ax.set_ylim(6.6, -.75)
    ax.set_xlim(25, 315)
    ax.set_xticks([40, 100, 175, 240, 300])
    ax.set_title(f"{steel} (n = {vn(cross[steel].sum())})", fontsize=18, pad=17)
    ax.set_xlabel("Độ dày (thang nguồn)", fontsize=15)
    ax.tick_params(axis="x", labelsize=14)
    base(ax, "x")
    if steel == "A400":
        ax.annotate("387/391 K_Scatch\nthuộc A400 và dày 40", (40, 2), xytext=(145, 2.45),
                    arrowprops={"arrowstyle": "->", "color": PRIMARY}, color=PRIMARY, fontsize=11)
        ax.annotate("Bumps: trung vị 40", (40, 1), xytext=(115, .58),
                    arrowprops={"arrowstyle": "->", "color": SECONDARY}, color=SECONDARY, fontsize=11)
    else:
        ax.annotate("Bumps: trung vị 70", (70, 1), xytext=(143, .58),
                    arrowprops={"arrowstyle": "->", "color": SECONDARY}, color=SECONDARY, fontsize=11)
assert ((d[LABEL].eq(K)) & d["Steel_Type"].eq("A400") & d["Steel_Plate_Thickness"].eq(40)).sum() == 387
fig.tight_layout(rect=(0, .08, 1, 1), w_pad=2.4)
save(fig, "ch4_06_do_day_theo_thep", "Hộp: P25-P75; râu: 1,5 IQR trong nhóm; điểm rời: ngoài râu. ♦: nhóm chỉ có một quan sát.",
     pd.DataFrame(thickness_rows))

# 4.7: original-scale box statistics, logarithmic display only.
area = d.groupby(LABEL)["Pixels_Areas"].agg(N="size", Median="median").sort_values("Median")
fig, ax = plt.subplots(figsize=(9, 5.4))
for i, (label, row) in enumerate(area.iterrows()):
    values = d.loc[d[LABEL].eq(label), "Pixels_Areas"].to_numpy()
    color = PRIMARY if label == K else SECONDARY if label == "Stains" else GRAY
    box = ax.boxplot([values], positions=[i], vert=False, widths=.55, patch_artist=True,
                     medianprops={"color": "#222222", "lw": 1.5},
                     boxprops={"edgecolor": color}, whiskerprops={"color": color},
                     capprops={"color": color},
                     flierprops={"marker": ".", "markersize": 4, "markeredgecolor": color, "alpha": .5})
    box["boxes"][0].set_facecolor(color)
    box["boxes"][0].set_alpha(.85)
    if label in (K, "Stains"):
        ax.text(row.Median, i-.37, f"Trung vị {vn(row.Median, 0 if label == K else 1)}",
                fontsize=11.5, color=color, ha="center")
ax.set_yticks(np.arange(7), [f"{label} (n = {int(row.N)})" for label, row in area.iterrows()])
ax.set_ylim(6.75, -.95)
ax.set_xscale("log")
ax.set_xlim(1.4, 220000)
ax.set_xticks([10, 100, 1000, 10000, 100000])
ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: vn(value)))
ax.set_xlabel("Pixels_Areas (giá trị gốc; trục log cơ số 10)")
ax.annotate("", (6281, 6.6), xytext=(16.5, 6.6),
            arrowprops={"arrowstyle": "<->", "color": PRIMARY, "lw": 1.4})
ax.text(np.sqrt(6281*16.5), 6.6, " Khoảng 381 lần ", ha="center", va="center",
        fontsize=11.5, color=PRIMARY, bbox={"facecolor": "white", "edgecolor": "none", "pad": 2})
base(ax, "x")
fig.tight_layout(rect=(0, .09, 1, 1))
save(fig, "ch4_07_boxplot_dien_tich", "Phân vị và râu tính trên diện tích gốc. Trục log chỉ thay hiển thị; giữ mọi điểm ngoài râu.", area.reset_index())

# 4.8: a slope chart with explicit before and hypothetical-after columns.
q1, q3 = d["Pixels_Areas"].quantile([.25, .75])
flags = d["Pixels_Areas"].gt(q3+1.5*(q3-q1)) | d["Pixels_Areas"].lt(q1-1.5*(q3-q1))
assert flags.sum() == 395
assert np.array_equal(flags.to_numpy(), d["Area_Outlier_Flag"].astype(bool).to_numpy())
remaining = d.loc[~flags, LABEL].value_counts().reindex(labels)
before, after = counts / len(d) * 100, remaining / (~flags).sum() * 100
assert remaining[K] == 65 and counts[K]-remaining[K] == 326
fig, ax = plt.subplots(figsize=(9, 5.6))
before_text = {"Other_Faults": 34.67, "Bumps": 22.1, K: 18.8,
               "Z_Scratch": 10.6, "Pastry": 7.5, "Stains": 4.6, "Dirtiness": 1.6}
after_text = {"Other_Faults": 40.82, "Bumps": 25.68, K: 4.4,
              "Z_Scratch": 12.5, "Pastry": 9.7, "Stains": 7.1, "Dirtiness": 1.4}
for label in labels:
    color, lw = (PRIMARY, 3.2) if label == K else ("#B0B0B0", 1.4)
    text_color = PRIMARY if label == K else "#656565"
    ax.plot([0, 1], [before[label], after[label]], color=color, lw=lw, marker="o", ms=7 if label == K else 5)
    ax.plot([-.085, 0], [before_text[label], before[label]], color=color, lw=1)
    ax.plot([1, 1.085], [after[label], after_text[label]], color=color, lw=1)
    ax.text(-.10, before_text[label], f"{label}   {vn(before[label], 2)}%", ha="right", va="center", color=text_color,
            fontsize=12 if label == K else 11.5, weight="bold" if label == K else "normal")
    ax.text(1.10, after_text[label], f"{vn(after[label], 2)}%   {label}", ha="left", va="center", color=text_color,
            fontsize=12 if label == K else 11.5, weight="bold" if label == K else "normal")
ax.text(.48, 17, "K_Scatch: hạng 3 → hạng 6\nMất 326/391 bản ghi", ha="center", fontsize=12, color=PRIMARY,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": .95})
ax.set_xticks([0, 1], ["Giữ đủ dữ liệu\nN = 1.941", "Giả định xóa cờ\nN = 1.546"], fontsize=12)
ax.set_xlim(-.1, 1.1)
ax.set_ylim(-1.3, 44)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_visible(False)
fig.subplots_adjust(left=.29, right=.71, bottom=.2, top=.98)
save(fig, "ch4_08_truoc_sau_xoa_co", "Kịch bản giả định để đối chiếu; dữ liệu phân tích thực tế vẫn giữ toàn bộ 1.941 bản ghi.",
     pd.DataFrame({LABEL: labels, "Before_N": counts.values, "Before_Percent": before.values,
                   "Flags": (counts-remaining).values, "After_N": remaining.values, "After_Percent": after.values}))

# Replace balanced-brace notes one at a time, without touching captions or labels.
source = ATTACHMENT.read_text(encoding="utf-8")
source = source.split("% ===== BEGIN: chuong/chuong4 =====", 1)[1].split("% ===== END: chuong/chuong4 =====", 1)[0].strip()
source = re.sub(r"% -{10,}.*?\\newcommand\{\\ghiChuHinh\}", r"\\newcommand{\\ghiChuHinh}", source, count=1, flags=re.S)


def replace_note(text, replacement):
    start = text.index("\\ghiChuHinh{")
    pos = start + len("\\ghiChuHinh{")
    depth = 1
    while depth:
        if text[pos] in "{}" and (pos == 0 or text[pos-1] != "\\"):
            depth += 1 if text[pos] == "{" else -1
        pos += 1
    return text[:start] + replacement + text[pos:]


for row in manifest:
    source = replace_note(source, r"\includegraphics[width=\linewidth]{" + row["image"] + "}")
dashboard_notes = [
    r"\ghiChuHinh{Ảnh chụp dashboard thật đang chờ bổ sung: chọn A300 và A400, cả bảy nhãn, toàn khoảng độ dày. Cần hiển thị bộ lọc và KPI 1.941; 7; 174,0; 70,0. Tệp: \maCot{figures/chuong4/ch4_09_dashboard_toan_bo.png}.",
    r"\ghiChuHinh{Ảnh chụp dashboard thật đang chờ bổ sung: chỉ chọn A400 và K\_Scatch, giữ toàn khoảng độ dày. Cần hiển thị bộ lọc và KPI 390; 1; 6.281,5; 40,0. Tệp: \maCot{figures/chuong4/ch4_10_dashboard_a400_kscatch.png}."
]
# Avoid replacing the first retained note twice by handling both notes via offsets.
positions = []
cursor = 0
while True:
    start = source.find("\\ghiChuHinh{", cursor)
    if start < 0:
        break
    pos, depth = start+len("\\ghiChuHinh{"), 1
    while depth:
        if source[pos] in "{}" and source[pos-1] != "\\":
            depth += 1 if source[pos] == "{" else -1
        pos += 1
    positions.append((start, pos))
    cursor = pos
assert len(positions) == 2
for (start, end), note in reversed(list(zip(positions, dashboard_notes))):
    source = source[:start]+note+"}"+source[end:]
source = "% !TeX root = ../main.tex\n% Tám biểu đồ đã chèn; hai ảnh dashboard thật đang chờ bổ sung.\n"+source+"\n"
chapter = ROOT / "latex/chuong/chuong4.tex"
backup = BACKUP / "chuong4.tex"
if not backup.exists():
    shutil.copy2(chapter, backup)
chapter.write_text(source, encoding="utf-8")

# Expand the existing report into a portable single-file version.
target = ROOT / "output/tieu_luan_ghep_anh_chuong4"
target.mkdir(parents=True, exist_ok=True)


def expand(path):
    content = path.read_text(encoding="utf-8")
    result = []
    for line in content.splitlines(keepends=True):
        match = re.fullmatch(r"\s*\\input\{([^}]+)\}\s*", line)
        if match:
            relative = match.group(1)
            result += [f"% ===== BEGIN: {relative} =====\n",
                       expand(ROOT / "latex" / (relative+".tex")),
                       f"\n% ===== END: {relative} =====\n"]
        else:
            result.append(line)
    return "".join(result)


merged = re.sub(r"^%\s*!TeX root\s*=.*\n?", "", expand(ROOT / "latex/main.tex"), flags=re.M)
(target / "tieu_luan.tex").write_text(merged, encoding="utf-8")
shutil.copytree(ROOT / "latex/figures", target / "figures", dirs_exist_ok=True)
shutil.copy2(chapter, target / "chuong4.tex")
readme = """# Báo cáo đã ghép ảnh Chương 4

`tieu_luan.tex` là bản gộp gồm phần đầu, bốn chương và tài liệu tham khảo.
`chuong4.tex` là phần chương riêng để thay vào dự án LaTeX hiện có.
Giữ thư mục `figures` cạnh tệp chính; biên dịch bằng XeLaTeX hoặc Tectonic.

Đã chèn đúng vị trí tám biểu đồ của bản Chương 4 được gửi: Pareto, số lượng theo
dòng thép, cơ cấu trong dòng thép, scatter độ sáng, IQR độ sáng, độ dày theo dòng
thép, boxplot diện tích và cơ cấu trước/sau giả định xóa cờ ngoại lai.
Các hình PNG có độ phân giải 300 dpi; SVG đi kèm cho phép chỉnh sửa.

Hai vị trí Hình 4.9 và 4.10 còn chờ ảnh dashboard thật. Công cụ điều khiển trình
duyệt bị dừng vì không xác định được URL hiện tại đủ chắc chắn. Không dùng giao
diện dựng lại để thay cho ảnh chụp thực tế.

Khi có ảnh, lưu tại `figures/chuong4/ch4_09_dashboard_toan_bo.png` và
`figures/chuong4/ch4_10_dashboard_a400_kscatch.png`, rồi thay từng lệnh
`\\ghiChuHinh{...}` tương ứng bằng `\\includegraphics[width=\\linewidth]{...}`.
Giữ nguyên caption và label. Chương đã giữ đủ 10 vị trí hình và các tham chiếu.
"""
(target / "README.md").write_text(readme, encoding="utf-8")
(OUT / "manifest.json").write_text(json.dumps({"dataset_sha256": data_hash, "figures": manifest,
                                            "inserted": 8, "pending_real_dashboard_captures": 2},
                                           ensure_ascii=False, indent=2), encoding="utf-8")
assert hashlib.sha256(DATA.read_bytes()).hexdigest() == data_hash
active = "\n".join(line for line in source.splitlines() if not line.lstrip().startswith("%"))
assert active.count(r"\includegraphics[") == 8
assert sum(line.startswith(r"\ghiChuHinh{") for line in active.splitlines()) == 2
assert active.count(r"\captionof{figure}") == 10
print(json.dumps({"inserted": 8, "pending_dashboard": 2, "target": str(target),
                  "source_data_unchanged": True}, ensure_ascii=False, indent=2))
