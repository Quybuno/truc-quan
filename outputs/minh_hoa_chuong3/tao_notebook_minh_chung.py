"""Create and execute genuine notebook cells for the Chapter 3 data figures.

Run from the project root:
    python outputs/minh_hoa_chuong3/tao_notebook_minh_chung.py

Only minh_chung_cell_chuong3.ipynb is written. Source datasets, the original
analysis notebook, saved CSVs, and existing figures are read without changes.
The eight displayed tables use the native pandas/IPython representation.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from textwrap import dedent

import nbformat
from nbclient import NotebookClient


ROOT = Path(__file__).resolve().parents[2]
DESTINATION = Path(__file__).with_name("minh_chung_cell_chuong3.ipynb")
SOURCES = [
    ROOT / "data/raw/practice/data_chua_sach_ko_sua.xlsx",
    ROOT / "data/raw/uci/steel_plates_faults_original.csv",
    ROOT / "buoc_1_2_3_4_5_6_loi_be_mat_thep.ipynb",
]


def source_hashes():
    return {
        str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in SOURCES
    }


SETUP = r'''
from pathlib import Path
import sys

import numpy as np
import pandas as pd
from IPython.display import display

for candidate in [Path.cwd(), *Path.cwd().parents]:
    if (candidate / "steel_analysis.py").is_file() and (candidate / "data/raw").is_dir():
        ROOT = candidate
        break
else:
    raise FileNotFoundError("Mở notebook trong thư mục dự án có dữ liệu nguồn.")

sys.path.insert(0, str(ROOT))
from steel_analysis import LABELS, LABEL_MAP, KEYS, clean_faults, add_fault_features

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 20)
pd.set_option("display.show_dimensions", True)
pd.set_option("display.precision", 6)
pd.set_option("display.max_colwidth", None)

practice = pd.read_excel(
    ROOT / "data/raw/practice/data_chua_sach_ko_sua.xlsx",
    sheet_name="Faults (2)", dtype=object, keep_default_na=False,
)
uci = pd.read_csv(ROOT / "data/raw/uci/steel_plates_faults_original.csv")
features = [column for column in uci.columns if column not in LABELS]

# Giữ một bản dữ liệu tại từng trạng thái, không sửa nguồn đầu vào.
raw = practice.copy(deep=True)
raw.insert(0, "Source_Row", np.arange(2, len(raw) + 2))
normalized = raw.copy(deep=True)
label_key = normalized["Faults"].str.lower().str.replace(r"[^a-z0-9]", "", regex=True)
normalized["Fault_Type_Clean"] = label_key.map(LABEL_MAP)
assert normalized["Fault_Type_Clean"].notna().all()
conversion_failures = 0
for column in features:
    original = normalized[column].copy()
    numeric = pd.to_numeric(original.mask(original.eq("")), errors="coerce")
    conversion_failures += int((original.notna() & original.ne("") & numeric.isna()).sum())
    normalized[column] = numeric
assert conversion_failures == 0

duplicate_columns = features + ["Production_Date", "Fault_Type_Clean"]
duplicate_mask = normalized.duplicated(duplicate_columns, keep="first")
retained = normalized.loc[~duplicate_mask].copy()
assert len(raw) == 1961 and int(duplicate_mask.sum()) == 20 and len(retained) == 1941
assert int(normalized[features].isna().sum().sum()) == 70
assert int(retained[features].isna().sum().sum()) == 67

# Kiểm tra bổ sung TRƯỚC khi lấy giá trị khôi phục từ UCI.
dx = retained["X_Maximum"] - retained["X_Minimum"]
dy = retained["Y_Maximum"] - retained["Y_Minimum"]
expected = {
    "Empty_Index": 1 - retained["Pixels_Areas"] / (dx * dy),
    "Log_Y_Index": np.log10(dy),
}
internal_flags = {}
for field, computed in expected.items():
    eligible = retained[field].notna() & computed.notna() & np.isfinite(computed)
    internal_flags[field] = eligible & (retained[field] - computed.round(4)).abs().gt(0.00010001)
assert int(internal_flags["Empty_Index"].sum()) == 10
assert int(internal_flags["Log_Y_Index"].sum()) == 6

reference = uci[features].copy()
reference["Source_Row_UCI"] = np.arange(2, len(uci) + 2)
merged = retained.merge(
    reference, on=KEYS, how="left", suffixes=("", "_UCI"),
    validate="one_to_one", indicator=True,
)
assert merged["_merge"].eq("both").all()
cleaned, quality = clean_faults(practice, uci)
analysis = add_fault_features(cleaned)
assert quality["missing_restored"] == 67 and quality["numeric_corrected"] == 16

raw_indexed = raw.set_index("Source_Row")
normalized_indexed = normalized.set_index("Source_Row")
retained_indexed = retained.set_index("Source_Row")
merged_indexed = merged.set_index("Source_Row")
cleaned_indexed = cleaned.set_index("Source_Row")
analysis_indexed = analysis.set_index("Source_Row")

# Các bảng hiển thị được tạo từ bản ghi thực, theo cùng ví dụ trong bản thảo.
raw_rows = [7, 10, 16, 101, 1331]
raw_columns = ["Faults", "Pixels_Areas", "X_Perimeter", "Empty_Index", "Log_Y_Index"]
raw_preview = raw_indexed.loc[raw_rows, raw_columns].reset_index()

label_rows = [10, 1331]
labels_preview = pd.DataFrame({
    "Source_Row": label_rows,
    "Faults_goc": [repr(raw_indexed.at[row, "Faults"]) for row in label_rows],
    "Fault_Type_Clean": [normalized_indexed.at[row, "Fault_Type_Clean"] for row in label_rows],
})
numeric_rows = []
for row, field in [(10, "X_Perimeter"), (1331, "X_Perimeter"), (7, "Pixels_Areas")]:
    old = raw_indexed.at[row, field]
    new = normalized_indexed.at[row, field]
    numeric_rows.append({
        "Source_Row": row, "Truong": field, "Truoc": repr(old),
        "Kieu_goc": type(old).__name__, "Sau": new,
        "Kieu_sau": "missing" if pd.isna(new) else "numeric",
    })
numeric_preview = pd.DataFrame(numeric_rows)

duplicate_rows = []
for kept, removed in [(645, 1943), (748, 1947)]:
    first = normalized_indexed.loc[kept, duplicate_columns]
    second = normalized_indexed.loc[removed, duplicate_columns]
    assert all((pd.isna(a) and pd.isna(b)) or a == b for a, b in zip(first, second))
    for row, action in [(kept, "Giữ"), (removed, "Loại")]:
        item = normalized_indexed.loc[row]
        duplicate_rows.append({
            "Source_Row": row, "Kept_Source_Row": kept,
            "Fault_Type_Clean": item["Fault_Type_Clean"],
            "X_Minimum": item["X_Minimum"], "X_Maximum": item["X_Maximum"],
            "Xu_ly": action,
        })
duplicate_preview = pd.DataFrame(duplicate_rows)

audit_rows = []
for row, field in [(101, "Empty_Index"), (238, "Empty_Index"), (16, "Log_Y_Index"), (61, "Log_Y_Index")]:
    position = retained.index[retained["Source_Row"].eq(row)][0]
    assert bool(internal_flags[field].loc[position])
    audit_rows.append({
        "Source_Row": row, "Truong": field,
        "Gia_tri_goc": retained_indexed.at[row, field],
        "Tinh_tu_cung_dong": expected[field].loc[position], "Gan_co": True,
    })
audit_preview = pd.DataFrame(audit_rows)

restoration_rows = []
for row, field in [(7, "Pixels_Areas"), (26, "Pixels_Areas"), (101, "Empty_Index"), (16, "Log_Y_Index")]:
    item = merged_indexed.loc[row]
    assert cleaned_indexed.at[row, field] == item[field + "_UCI"]
    restoration_rows.append({
        "Source_Row": row, "Source_Row_UCI": int(item["Source_Row_UCI"]),
        "Truong": field, "Truoc": item[field], "Sau": item[field + "_UCI"],
    })
restoration_preview = pd.DataFrame(restoration_rows)

analysis_columns = ["Steel_Type", "Pixels_Areas", "X_Range", "Y_Range", "Luminosity_Range", "Log_Pixels_Areas"]
analysis_preview = analysis_indexed.loc[[7, 10, 16, 101], analysis_columns].reset_index()
date_rows = [2, 5, 7]
dates_preview = pd.DataFrame({
    "Source_Row": date_rows,
    "Production_Date": [str(raw_indexed.at[row, "Production_Date"]) for row in date_rows],
    "Production_Date_Clean": [cleaned_indexed.at[row, "Production_Date_Clean"].strftime("%Y-%m-%d") for row in date_rows],
    "Date_Is_Simulated": [True] * len(date_rows),
})

# Đối chiếu các ví dụ với CSV minh chứng hiện có; không ghi lại các CSV.
proof_dir = ROOT / "outputs/minh_hoa_chuong3"
def assert_numeric_equal(actual, saved, columns):
    np.testing.assert_allclose(
        actual[columns].apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float),
        saved[columns].apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float),
        rtol=0, atol=1e-9, equal_nan=True,
    )

saved_raw = pd.read_csv(proof_dir / "01_du_lieu_tho.csv", dtype=object, keep_default_na=False)
assert raw_preview["Faults"].tolist() == saved_raw["Faults"].tolist()
assert_numeric_equal(raw_preview, saved_raw, ["Source_Row", *raw_columns[1:]])
saved_labels = pd.read_csv(proof_dir / "02_chuan_hoa_nhan.csv")
assert labels_preview["Faults_goc"].tolist() == saved_labels["Faults_raw"].map(repr).tolist()
assert labels_preview["Fault_Type_Clean"].tolist() == saved_labels["Fault_Type_Clean"].tolist()
saved_numeric = pd.read_csv(proof_dir / "02_chuan_hoa_so.csv", dtype=object, keep_default_na=False)
assert numeric_preview["Truong"].tolist() == saved_numeric["Field"].tolist()
assert numeric_preview["Kieu_goc"].tolist() == saved_numeric["Type_before"].tolist()
assert numeric_preview["Kieu_sau"].tolist() == saved_numeric["Type_after"].tolist()
assert_numeric_equal(numeric_preview, saved_numeric.rename(columns={"After": "Sau"}), ["Source_Row", "Sau"])
for index, (row, field) in enumerate([(10, "X_Perimeter"), (1331, "X_Perimeter"), (7, "Pixels_Areas")]):
    assert str(raw_indexed.at[row, field]) == saved_numeric.loc[index, "Before"]

saved_duplicates = pd.read_csv(proof_dir / "03_cap_trung.csv")
assert_numeric_equal(duplicate_preview, saved_duplicates, ["Source_Row", "Kept_Source_Row", "X_Minimum", "X_Maximum"])
assert duplicate_preview["Fault_Type_Clean"].tolist() == saved_duplicates["Fault_Type_Clean"].tolist()
assert duplicate_preview["Xu_ly"].tolist() == saved_duplicates["Action"].tolist()
saved_audit = pd.read_csv(proof_dir / "04_kiem_tra_noi_tai.csv").rename(columns={
    "Before": "Gia_tri_goc", "Computed_same_row": "Tinh_tu_cung_dong", "Flag": "Gan_co", "Field": "Truong",
})
assert_numeric_equal(audit_preview, saved_audit, ["Source_Row", "Gia_tri_goc", "Tinh_tu_cung_dong"])
assert audit_preview["Truong"].tolist() == saved_audit["Truong"].tolist()
assert audit_preview["Gan_co"].tolist() == saved_audit["Gan_co"].tolist()
saved_restoration = pd.read_csv(proof_dir / "05_khoi_phuc_uci.csv").rename(columns={
    "Before": "Truoc", "After": "Sau", "Field": "Truong",
})
assert_numeric_equal(restoration_preview, saved_restoration, ["Source_Row", "Source_Row_UCI", "Truoc", "Sau"])
assert restoration_preview["Truong"].tolist() == saved_restoration["Truong"].tolist()
saved_analysis = pd.read_csv(proof_dir / "06_bien_phan_tich.csv")
assert analysis_preview["Steel_Type"].tolist() == saved_analysis["Steel_Type"].tolist()
assert_numeric_equal(analysis_preview, saved_analysis, ["Source_Row", *analysis_columns[1:]])
saved_dates = pd.read_csv(proof_dir / "06_ngay_mo_phong.csv").rename(columns={"Production_Date_raw": "Production_Date"})
pd.testing.assert_frame_equal(dates_preview, saved_dates, check_dtype=False)

# Toàn bộ đặc trưng sau xử lý và biến mới cũng phải khớp dữ liệu đã lưu.
saved_clean_full = pd.read_csv(ROOT / "data/clean/loi_thep_sach.csv").sort_values("Source_Row").reset_index(drop=True)
saved_analysis_full = pd.read_csv(ROOT / "data/analysis/loi_thep_phan_tich.csv").sort_values("Source_Row").reset_index(drop=True)
clean_sorted = cleaned.sort_values("Source_Row").reset_index(drop=True)
analysis_sorted = analysis.sort_values("Source_Row").reset_index(drop=True)
assert_numeric_equal(clean_sorted, saved_clean_full, ["Source_Row", *features])
assert clean_sorted["Fault_Type_Clean"].tolist() == saved_clean_full["Fault_Type_Clean"].tolist()
assert_numeric_equal(analysis_sorted, saved_analysis_full, ["Source_Row", "X_Range", "Y_Range", "Luminosity_Range", "Log_Pixels_Areas"])
assert analysis_sorted["Steel_Type"].tolist() == saved_analysis_full["Steel_Type"].tolist()
'''


STAGES = [
    (
        "01 - Dữ liệu thô",
        "Trích các dòng có ô trống, chuỗi số, nhãn chưa chuẩn và chỉ số cần kiểm tra. "
        "Source_Row là dòng nguồn, tính cả hàng tiêu đề. Không đưa tên tệp vào bảng hiển thị.",
        '# Hình 3.1 - Dữ liệu thô: các dòng cần chú ý\n'
        'display(raw_preview)\n',
    ),
    (
        "02 - Chuẩn hóa nhãn và kiểu số",
        "Đối chiếu cùng bản ghi trước và sau chuẩn hóa. Dấu nháy ở Faults_goc và Truoc "
        "do repr() làm rõ biểu diễn chuỗi; chuỗi rỗng chưa được khôi phục. "
        "Sau chuyển kiểu: 7 nhãn chuẩn, 0 chuỗi số không trống chuyển thất bại.",
        '# Hình 3.2 - Chuẩn hóa nhãn và chuyển kiểu số\n'
        'display(labels_preview)\n'
        'display(numeric_preview)\n',
    ),
    (
        "03 - Loại bản ghi trùng",
        "Hai cặp dòng giữ–loại đã được đối chiếu đủ 27 đặc trưng, ngày gốc và nhãn chuẩn. "
        "Các cột tọa độ X chỉ là phần trích để đọc rõ. Tổng cộng loại 20 dòng, còn 1.941 dòng.",
        '# Hình 3.3 - Các cặp bản ghi trùng và dòng được giữ\n'
        'display(duplicate_preview)\n',
    ),
    (
        "04 - Kiểm tra nội tại trước khôi phục",
        "Đây là lượt rà soát bổ sung trên bảng đã chuẩn hóa và loại trùng, trước khi dùng "
        "giá trị UCI để điền hoặc sửa. Tinh_tu_cung_dong được tính từ các cột của chính bản ghi. "
        "Bảng trích 4 trong 16 ô gắn cờ; kết quả tính chưa được tự dùng làm giá trị thay thế.",
        '# Hình 3.4 - Rà soát bổ sung trước khi dùng tham chiếu UCI\n'
        'display(audit_preview)\n',
    ),
    (
        "05 - Khôi phục theo nguồn tham chiếu",
        "Các bản ghi đã ghép một–một bằng bốn tọa độ. Bảng trích 2 ô thiếu và 2 giá trị sai; "
        "NaN biểu thị ô thiếu sau chuyển kiểu. Tổng cộng khôi phục 67 ô thiếu và sửa 16 giá trị.",
        '# Hình 3.5 - Giá trị trước và sau khôi phục theo UCI\n'
        'display(restoration_preview)\n',
    ),
    (
        "06 - Bảng phân tích",
        "Các biến phái sinh được tính từ dữ liệu sau làm sạch. Ngày mô phỏng được giữ cả "
        "biểu diễn gốc và giá trị chuẩn; Date_Is_Simulated=True. Những ngày này không dùng "
        "để kết luận xu hướng sản xuất.",
        '# Hình 3.6 - Các biến phái sinh và ngày mô phỏng\n'
        'display(analysis_preview)\n'
        'display(dates_preview)\n',
    ),
]


def main():
    before = source_hashes()
    cells = [
        nbformat.v4.new_markdown_cell(
            "# Minh chứng đầu ra cell cho Chương 3\n\n"
            "Notebook bổ sung này tái lập các trạng thái dữ liệu từ nguồn thực, chọn các "
            "dòng/cột đang được diễn giải trong bản thảo và hiển thị bằng Pandas. Các bảng "
            "là đầu ra thực thi của cell; không dựng lại bằng Matplotlib, không tạo HTML "
            "giả giao diện. Notebook gốc và các nguồn dữ liệu được giữ nguyên.\n\n"
            "Cell thiết lập cũng đối chiếu ví dụ với các CSV minh chứng đã lưu. "
            "Mục 04 là lượt kiểm tra bổ sung trước khôi phục, được phân biệt với kiểm tra "
            "công thức sau khôi phục trong notebook phân tích gốc."
        ),
        nbformat.v4.new_code_cell(dedent(SETUP).strip() + "\n", metadata={"tags": ["setup"]}),
    ]
    for number, (heading, description, code) in enumerate(STAGES, start=1):
        cells.append(nbformat.v4.new_markdown_cell(f"## {heading}\n\n{description}"))
        cells.append(nbformat.v4.new_code_cell(code, metadata={"tags": [f"figure-{number:02d}"]}))
    notebook = nbformat.v4.new_notebook(
        cells=cells,
        metadata={
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "file_extension": ".py", "mimetype": "text/x-python"},
            "provenance": {
                "purpose": "Executed supplementary notebook for Chapter 3 data-cell screenshots",
                "source_sha256": before,
                "original_notebook_modified": False,
                "figure_04": "Additional internal audit before reference restoration",
            },
        },
    )
    NotebookClient(
        notebook, timeout=180, kernel_name="python3", allow_errors=False,
        resources={"metadata": {"path": str(ROOT)}},
    ).execute()
    after = source_hashes()
    assert before == after, "A source dataset or original notebook changed during execution."
    code_cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
    assert len(code_cells) == 7 and all(cell.execution_count is not None for cell in code_cells)
    displays = [
        output for cell in code_cells for output in cell.outputs
        if output.output_type in {"display_data", "execute_result"}
        and "text/html" in output.get("data", {})
    ]
    assert len(displays) == 8
    assert all('class="dataframe"' in output.data["text/html"] for output in displays)
    assert all("Source_File" not in output.data["text/html"] for output in displays)
    notebook.metadata["verification"] = {
        "sources_and_original_notebook_unchanged": True,
        "saved_csv_previews_matched": True,
        "saved_clean_features_and_analysis_fields_matched": True,
        "executed_code_cells": len(code_cells),
        "native_pandas_dataframe_outputs": len(displays),
        "six_figure_cells": True,
    }
    nbformat.write(notebook, DESTINATION)
    print(json.dumps({
        "notebook": str(DESTINATION.relative_to(ROOT)),
        "verification": dict(notebook.metadata["verification"]),
        "selected_columns": {
            "01": ["Source_Row", "Faults", "Pixels_Areas", "X_Perimeter", "Empty_Index", "Log_Y_Index"],
            "02a": ["Source_Row", "Faults_goc", "Fault_Type_Clean"],
            "02b": ["Source_Row", "Truong", "Truoc", "Kieu_goc", "Sau", "Kieu_sau"],
            "03": ["Source_Row", "Kept_Source_Row", "Fault_Type_Clean", "X_Minimum", "X_Maximum", "Xu_ly"],
            "04": ["Source_Row", "Truong", "Gia_tri_goc", "Tinh_tu_cung_dong", "Gan_co"],
            "05": ["Source_Row", "Source_Row_UCI", "Truong", "Truoc", "Sau"],
            "06a": ["Source_Row", "Steel_Type", "Pixels_Areas", "X_Range", "Y_Range", "Luminosity_Range", "Log_Pixels_Areas"],
            "06b": ["Source_Row", "Production_Date", "Production_Date_Clean", "Date_Is_Simulated"],
        },
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
