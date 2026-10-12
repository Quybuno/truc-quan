"""Reproduce legacy intermediate data table illustrations for Chapter 3.

Run from the project root: python outputs/minh_hoa_chuong3/tao_hinh_du_lieu.py
This script never changes source datasets or the notebook.
The Matplotlib illustrations are saved separately from the current report figures.
Current report figures are genuine VS Code cell captures; see cat_anh_cell.py.
"""
from pathlib import Path
import hashlib
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from steel_analysis import LABELS, LABEL_MAP, KEYS, clean_faults, add_fault_features

OUT = ROOT / "outputs/minh_hoa_chuong3"
FIG = OUT / "bang_minh_hoa_cu"
OUT.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)
source_paths = [ROOT / "data/raw/practice/data_chua_sach_ko_sua.xlsx",
                ROOT / "data/raw/uci/steel_plates_faults_original.csv"]
hashes_before = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in source_paths}

practice = pd.read_excel(source_paths[0], sheet_name="Faults (2)",
                         dtype=object, keep_default_na=False)
uci = pd.read_csv(source_paths[1])
features = [c for c in uci if c not in LABELS]
raw = practice.copy(deep=True)
raw.insert(0, "Source_Row", np.arange(2, len(raw) + 2))
normalized = raw.copy(deep=True)
label_key = normalized["Faults"].astype(str).str.lower().str.replace(r"[^a-z0-9]", "", regex=True)
normalized["Fault_Type_Clean"] = label_key.map(LABEL_MAP)
invalid_count = 0
for column in features:
    original = normalized[column]
    numeric = pd.to_numeric(original.mask(original.eq("")), errors="coerce")
    invalid_count += int((original.notna() & original.ne("") & numeric.isna()).sum())
    normalized[column] = numeric
duplicate_columns = features + ["Production_Date", "Fault_Type_Clean"]
duplicate = normalized.duplicated(duplicate_columns, keep="first")
retained = normalized.loc[~duplicate].copy()
reference = uci[features].copy()
reference["Source_Row_UCI"] = np.arange(2, len(uci) + 2)
merged = retained.merge(reference, on=KEYS, how="left", suffixes=("", "_UCI"),
                        validate="one_to_one", indicator=True)
assert merged["_merge"].eq("both").all()
cleaned, quality = clean_faults(practice, uci)
analysis = add_fault_features(cleaned)

saved_clean = pd.read_csv(ROOT / "data/clean/loi_thep_sach.csv")
saved_analysis = pd.read_csv(ROOT / "data/analysis/loi_thep_phan_tich.csv")
cleaned = cleaned.sort_values("Source_Row").reset_index(drop=True)
analysis = analysis.sort_values("Source_Row").reset_index(drop=True)
saved_clean = saved_clean.sort_values("Source_Row").reset_index(drop=True)
saved_analysis = saved_analysis.sort_values("Source_Row").reset_index(drop=True)
assert cleaned["Source_Row"].equals(saved_clean["Source_Row"])
assert np.allclose(cleaned[features].to_numpy(float), saved_clean[features].to_numpy(float),
                   rtol=0, atol=1e-9)
assert cleaned["Fault_Type_Clean"].equals(saved_clean["Fault_Type_Clean"])
derived = ["X_Range", "Y_Range", "Luminosity_Range", "Log_Pixels_Areas"]
assert np.allclose(analysis[derived].to_numpy(float), saved_analysis[derived].to_numpy(float),
                   rtol=0, atol=1e-9)
assert analysis["Steel_Type"].equals(saved_analysis["Steel_Type"])

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                     "savefig.dpi": 300, "figure.facecolor": "white"})
INK = "#20313c"
HEAD = "#e7eef2"
BASE = "#ffffff"
STRIPE = "#f6f8f9"
WARN = "#fff0dc"
GOOD = "#e3f2e8"

def number(value, decimals=4):
    if value == "" or pd.isna(value):
        return "[thiếu]"
    if isinstance(value, (int, float, np.integer, np.floating)):
        return str(int(value)) if float(value).is_integer() else f"{float(value):.{decimals}f}".rstrip("0").rstrip(".")
    return str(value)

def raw_value(value):
    if value == "" or pd.isna(value):
        return "[thiếu]"
    if isinstance(value, str):
        return repr(value)
    return number(value)

manifest = {"image_kind": "actual pandas table previews rendered with Matplotlib",
            "source_row_definition": "Source_Row = original zero-based Excel row index + 2 (header is row 1)",
            "reference_row_definition": "Source_Row_UCI = zero-based CSV record index + 2 (header is row 1)",
            "sources": list(hashes_before), "figures": [], "checks": quality}

def save_csv(name, table):
    table.to_csv(OUT / name, index=False, encoding="utf-8-sig")

def draw_table(ax, table, widths, highlights=None, font=10.5):
    ax.axis("off")
    cells = [[str(x) for x in row] for row in table.itertuples(index=False, name=None)]
    tbl = ax.table(cellText=cells, colLabels=list(table.columns), cellLoc="left",
                   colLoc="left", colWidths=widths, bbox=[0, 0, 1, 1])
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(font)
    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor("#d5dee3")
        cell.set_linewidth(0.45)
        cell.PAD = 0.08
        cell.get_text().set_color(INK)
        if r == 0:
            cell.set_facecolor(HEAD)
            cell.get_text().set_weight("bold")
        else:
            cell.set_facecolor(STRIPE if r % 2 == 0 else BASE)
            if highlights and (r-1, c) in highlights:
                cell.set_facecolor(highlights[(r-1, c)])
    return tbl

def make_figure(filename, title, panels, footer, caption, csvs, row_ids, mapping):
    # Six-inch width is close to the final 16 cm insertion width. Fonts remain
    # readable at that size; PNG resolution is 300 dpi.
    heights = [0.40 + 0.29 * (len(p[1]) + 1) for p in panels]
    height = 0.70 + sum(heights) + 0.28 * (len(panels)-1) + 0.57
    fig = plt.figure(figsize=(6.6, height))
    fig.text(0.035, 1-0.27/height, title, va="top", color=INK, size=12, weight="bold")
    cursor = height - 0.74
    for (subtitle, table, widths, highlights), ph in zip(panels, heights):
        fig.text(0.035, cursor/height, subtitle, va="top", size=10, color=INK)
        table_h = ph - 0.25
        ax = fig.add_axes([0.035, (cursor - 0.24 - table_h)/height, 0.93, table_h/height])
        draw_table(ax, table, widths, highlights)
        cursor -= ph + 0.25
    fig.text(0.035, 0.09/height, footer, va="bottom", size=9, color="#52616b",
             linespacing=1.4)
    fig.savefig(FIG / filename, dpi=300)
    plt.close(fig)
    manifest["figures"].append({"file": str((FIG / filename).relative_to(ROOT)),
                                "caption": caption, "source_rows": row_ids,
                                "table_csvs": csvs, "column_mapping": mapping,
                                "image_size_inches": [6.6, height], "dpi": 300})

# 01: Representative rows actually contain a blank, a numeric string, dirty
# label spelling, and malformed decimal values. These are deliberately selected,
# not a random sample or a screenshot of all 29 columns.
ids = [7, 10, 16, 101, 1331]
sample = raw.set_index("Source_Row").loc[ids,
    ["Faults", "Pixels_Areas", "X_Perimeter", "Empty_Index", "Log_Y_Index"]].reset_index()
save_csv("01_du_lieu_tho.csv", sample)
display = sample.copy()
for c in display.columns[1:]:
    display[c] = display[c].map(raw_value)
display.columns = ["Dòng\nnguồn", "Faults", "Pixels\n_Areas", "Chu vi\nX", "Empty\n_Index", "Log_Y\n_Index"]
high = {(0, 2): WARN, (1, 1): WARN, (1, 3): WARN, (2, 5): WARN,
        (3, 4): WARN, (4, 1): WARN, (4, 3): WARN}
make_figure("01_du_lieu_tho.png", "Dữ liệu đầu vào: các dòng cần chú ý",
            [("Trích 5 bản ghi từ bảng dữ liệu thực hành", display,
              [.10, .26, .16, .15, .16, .17], high)],
            "Ô màu cam: ví dụ cần xử lý. Dấu nháy chỉ giá trị kiểu chuỗi.\n[thiếu] biểu diễn ô trống; đây là bảng do Python kết xuất.",
            "Trích các dòng có nhãn chưa chuẩn, chuỗi số, ô thiếu và giá trị bất thường trong tệp đầu vào.",
            ["01_du_lieu_tho.csv"], ids,
            {"Dòng nguồn": "Source_Row", "Chu vi X":"X_Perimeter", "all_other_headers": "Original feature names split into two lines"})

# 02: Same records before and after normalization; blank remains missing.
label_ids = [10, 1331]
labels = pd.DataFrame({"Source_Row": label_ids,
                       "Faults_raw": [raw.set_index("Source_Row").at[i, "Faults"] for i in label_ids],
                       "Fault_Type_Clean": [normalized.set_index("Source_Row").at[i, "Fault_Type_Clean"] for i in label_ids]})
numeric_rows = []
for row, field in [(10, "X_Perimeter"), (1331, "X_Perimeter"), (7, "Pixels_Areas")]:
    old = raw.set_index("Source_Row").at[row, field]
    new = normalized.set_index("Source_Row").at[row, field]
    numeric_rows.append({"Source_Row": row, "Field": field, "Before": old,
                         "Type_before": type(old).__name__, "After": new,
                         "Type_after": "missing" if pd.isna(new) else "numeric"})
nums = pd.DataFrame(numeric_rows)
save_csv("02_chuan_hoa_nhan.csv", labels)
save_csv("02_chuan_hoa_so.csv", nums)
dl = labels.copy(); dl["Faults_raw"] = dl["Faults_raw"].map(repr)
dl.columns = ["Dòng\nnguồn", "Nhãn gốc", "Nhãn chuẩn"]
dn = pd.DataFrame({"Dòng\nnguồn": nums.Source_Row, "Trường": nums.Field,
                   "Trước (kiểu)": ["chuỗi rỗng" if v=="" else f"{raw_value(v)} ({t})" for v,t in zip(nums.Before,nums.Type_before)],
                   "Sau": nums.After.map(number)})
make_figure("02_chuan_hoa.png", "Chuẩn hóa nhãn và chuyển kiểu số",
            [("a) Nhãn của cùng bản ghi", dl, [.15,.43,.42], {(0,2):GOOD,(1,2):GOOD}),
             ("b) Chuyển số không đồng nghĩa với điền ô thiếu", dn,
              [.15,.27,.35,.23], {(0,3):GOOD,(1,3):GOOD,(2,3):WARN})],
            "28 cách viết nhãn → 7 nhãn chuẩn; 0 chuỗi số không trống chuyển thất bại.\nÔ trống vẫn thiếu ở giai đoạn này, chưa được khôi phục.",
            "Chuẩn hóa nhãn và chuyển kiểu số trên cùng các dòng; ô thiếu chưa được điền.",
            ["02_chuan_hoa_nhan.csv", "02_chuan_hoa_so.csv"], [7,10,1331],
            {"Nhãn gốc":"Faults", "Nhãn chuẩn":"Fault_Type_Clean"})

# 03: Two genuinely duplicate pairs. Assert full duplicate criteria, not just
# the abbreviated columns shown in the figure.
pair_ids = [(645,1943), (748,1947)]
dup_rows = []
for keeper, removed in pair_ids:
    a = normalized.set_index("Source_Row").loc[keeper, duplicate_columns]
    b = normalized.set_index("Source_Row").loc[removed, duplicate_columns]
    assert all((pd.isna(x) and pd.isna(y)) or x == y for x,y in zip(a,b))
    assert not bool(duplicate.loc[normalized.index[normalized.Source_Row.eq(keeper)][0]])
    assert bool(duplicate.loc[normalized.index[normalized.Source_Row.eq(removed)][0]])
    for row, state in [(keeper,"Giữ"), (removed,"Loại")]:
        s=normalized.set_index("Source_Row").loc[row]
        dup_rows.append({"Source_Row":row,"Kept_Source_Row":keeper,"X_Minimum":s.X_Minimum,
                         "X_Maximum":s.X_Maximum,"Y_Minimum":s.Y_Minimum,"Y_Maximum":s.Y_Maximum,
                         "Fault_Type_Clean":s.Fault_Type_Clean,"Action":state})
dups=pd.DataFrame(dup_rows);save_csv("03_cap_trung.csv",dups)
dd=pd.DataFrame({"Dòng\nnguồn":dups.Source_Row,
                 "X_min →\nX_max":[f"{int(a)} → {int(b)}" for a,b in zip(dups.X_Minimum,dups.X_Maximum)],
                 "Y_min → Y_max":[f"{int(a)} → {int(b)}" for a,b in zip(dups.Y_Minimum,dups.Y_Maximum)],
                 "Nhãn chuẩn":dups.Fault_Type_Clean,"Xử lý":dups.Action})
make_figure("03_loai_trung.png", "Loại bản ghi trùng, giữ dấu vết dòng nguồn",
            [("Hai cặp minh họa (các tọa độ chỉ là cột trích)", dd,
              [.105,.185,.35,.235,.125], {(0,4):GOOD,(1,4):WARN,(2,4):GOOD,(3,4):WARN})],
            "Đối chiếu đủ 27 đặc trưng + ngày gốc + nhãn chuẩn; giữ dòng đầu.\n1.961 dòng → loại 20 dòng trùng → còn 1.941 dòng.",
            "Hai cặp bản ghi trùng được xác nhận bằng toàn bộ tiêu chí; cột tọa độ được trích để minh họa.",
            ["03_cap_trung.csv"], [645,1943,748,1947],
            {"X_min → X_max":"X_Minimum, X_Maximum", "Y_min → Y_max":"Y_Minimum, Y_Maximum", "Xử lý":"Action"})

# 04: Supplementary audit, computed exclusively from each retained raw row.
dx=retained.X_Maximum-retained.X_Minimum
dy=retained.Y_Maximum-retained.Y_Minimum
expected={"Empty_Index":1-retained.Pixels_Areas/(dx*dy), "Log_Y_Index":np.log10(dy)}
audit_rows=[]
for row, field in [(101,"Empty_Index"),(238,"Empty_Index"),(16,"Log_Y_Index"),(61,"Log_Y_Index")]:
    idx=retained.index[retained.Source_Row.eq(row)][0]
    old=retained.at[idx,field];computed=expected[field].loc[idx]
    assert abs(old-round(computed,4))>0.00010001
    audit_rows.append({"Source_Row":row,"Field":field,"Before":old,
                       "Computed_same_row":computed,"Flag":True})
aud=pd.DataFrame(audit_rows);save_csv("04_kiem_tra_noi_tai.csv",aud)
da=pd.DataFrame({"Dòng\nnguồn":aud.Source_Row,"Trường":aud.Field,
                 "Giá trị gốc":aud.Before.map(number),
                 "Tính từ\ncùng dòng":aud.Computed_same_row.map(lambda x:f"{x:.6f}"),
                 "Gắn cờ":["Có"]*len(aud)})
make_figure("04_kiem_tra_noi_tai.png", "Kiểm tra quan hệ nội tại trước khôi phục",
            [("Rà soát bổ sung: 4 trong 16 ô được gắn cờ", da,
              [.12,.27,.19,.27,.15], {(i,2):WARN for i in range(len(da))})],
            "Empty_Index = 1 − diện tích/(ΔX·ΔY); Log_Y_Index = log10(ΔY).\nGiá trị tính dùng phát hiện; chưa tự thay thế bằng kết quả tính.",
            "Ví dụ từ phép rà soát bổ sung bằng quan hệ nội tại, thực hiện trước khi lấy giá trị khôi phục từ UCI.",
            ["04_kiem_tra_noi_tai.csv"], [101,238,16,61],
            {"Giá trị gốc":"Before", "Tính từ cùng dòng":"Computed_same_row"})

# 05: Logs are independently checked against the reproduced merged records.
restore_rows=[]
for row,field in [(7,"Pixels_Areas"),(26,"Pixels_Areas"),(101,"Empty_Index"),(16,"Log_Y_Index")]:
    s=merged.set_index("Source_Row").loc[row]
    old=s[field];new=s[field+"_UCI"]
    assert cleaned.set_index("Source_Row").at[row,field]==new
    restore_rows.append({"Source_Row":row,"Source_Row_UCI":int(s.Source_Row_UCI),"Field":field,
                         "Before":old,"After":new,"Operation":"restore" if pd.isna(old) else "correct"})
res=pd.DataFrame(restore_rows);save_csv("05_khoi_phuc_uci.csv",res)
dr=pd.DataFrame({"Dòng\nnguồn":res.Source_Row,"Dòng\nUCI":res.Source_Row_UCI,
                 "Trường":res.Field,"Trước":res.Before.map(number),"Sau (UCI)":res.After.map(number)})
make_figure("05_khoi_phuc_uci.png", "Khôi phục theo bản ghi UCI đã ghép đúng khóa",
            [("4 ví dụ: 2 ô thiếu và 2 giá trị sai",dr,[.13,.13,.30,.21,.23],
              {(i,c):(WARN if c==3 else GOOD) for i in range(len(dr)) for c in [3,4]})],
            "Ghép một–một bằng X_Minimum, X_Maximum, Y_Minimum, Y_Maximum.\nTổng cộng: khôi phục 67 ô thiếu; sửa 16 giá trị khác nguồn UCI.",
            "Các ô trước và sau khôi phục, cùng định danh dòng nguồn và dòng UCI; việc ghép dùng bốn tọa độ.",
            ["05_khoi_phuc_uci.csv"],[7,26,101,16],
            {"Dòng UCI":"Source_Row_UCI", "Sau (UCI)":"After"})

# 06: Only already-computed analysis fields are displayed. Raw values remain
# available alongside the new fields in the complete CSV.
final_ids=[7,10,16,101]
final=analysis.set_index("Source_Row").loc[final_ids,
    ["Steel_Type","Pixels_Areas","X_Range","Y_Range","Luminosity_Range","Log_Pixels_Areas"]].reset_index()
save_csv("06_bien_phan_tich.csv",final)
df=pd.DataFrame({"Dòng\nnguồn":final.Source_Row,"Dòng\nthép":final.Steel_Type,
                 "Diện\ntích":final.Pixels_Areas.map(number),"ΔX":final.X_Range.map(number),
                 "ΔY":final.Y_Range.map(number),"Δ sáng":final.Luminosity_Range.map(number),
                 "log10\ndiện tích":final.Log_Pixels_Areas.map(lambda x:f"{x:.4f}")})
date_ids=[2,5,7]
dates=pd.DataFrame({"Source_Row":date_ids,
    "Production_Date_raw":[str(raw.set_index("Source_Row").at[i,"Production_Date"]) for i in date_ids],
    "Production_Date_Clean":[cleaned.set_index("Source_Row").at[i,"Production_Date_Clean"].strftime("%Y-%m-%d") for i in date_ids],
    "Date_Is_Simulated":[True]*3})
save_csv("06_ngay_mo_phong.csv",dates)
dt=dates.iloc[:,:3].copy();dt.columns=["Dòng\nnguồn","Ngày gốc","Ngày chuẩn"]
make_figure("06_du_lieu_phan_tich.png", "Dữ liệu sau xử lý và các cột dùng để phân tích",
            [("a) Một số biến phái sinh trong bảng dữ liệu phân tích",df,
              [.11,.12,.15,.12,.12,.16,.22],{(i,c):GOOD for i in range(len(df)) for c in [3,4,5,6]}),
             ("b) Ngày chuẩn hóa theo lịch mô phỏng của tệp thực hành",dt,[.16,.54,.30],
              {(i,2):GOOD for i in range(len(dt))})],
            "ΔX, ΔY: hiệu tọa độ; Δ sáng: Maximum − Minimum_of_Luminosity.\nDate_Is_Simulated = True; ngày này không dùng kết luận xu hướng sản xuất.",
            "Trích dữ liệu phân tích sau xử lý: biến phái sinh và ngày chuẩn hóa có cờ mô phỏng.",
            ["06_bien_phan_tich.csv","06_ngay_mo_phong.csv"],final_ids+date_ids,
            {"Dòng thép":"Steel_Type","Diện tích":"Pixels_Areas","ΔX":"X_Range",
             "ΔY":"Y_Range","Δ sáng":"Luminosity_Range","log10 diện tích":"Log_Pixels_Areas",
             "Ngày gốc":"Production_Date","Ngày chuẩn":"Production_Date_Clean"})

manifest["checks"].update({"raw_label_representations":int(raw.Faults.nunique()),
    "normalized_labels":int(normalized.Fault_Type_Clean.nunique()),
    "numeric_conversion_failures":invalid_count,
    "raw_missing_feature_cells":int(normalized[features].isna().sum().sum()),
    "missing_after_deduplication":int(retained[features].isna().sum().sum()),
    "matches_saved_clean_features_and_labels":True,"matches_saved_analysis_derived_fields":True,
    "sources_unchanged":all(hashlib.sha256(p.read_bytes()).hexdigest()==hashes_before[str(p.relative_to(ROOT))]
                            for p in source_paths)})
manifest["source_sha256"]=hashes_before
manifest["regeneration_command"]="python outputs/minh_hoa_chuong3/tao_hinh_du_lieu.py"
(OUT/"manifest_bang_minh_hoa_cu.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"figures":len(manifest["figures"]),"checks":manifest["checks"]},ensure_ascii=True,indent=2))
