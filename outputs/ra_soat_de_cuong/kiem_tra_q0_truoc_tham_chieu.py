"""Read-only audit of practice data before restoring any value from UCI.

The UCI header supplies the feature schema only. Detection rules use values
within each practice record; matching repair logs happens after detection.
This is a supplementary review, not an execution of the notebook pipeline.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from steel_analysis import LABEL_MAP

raw_path = ROOT / 'data/raw/practice/data_chua_sach_ko_sua.xlsx'
reference_path = ROOT / 'data/raw/uci/steel_plates_faults_original.csv'
source_paths = [raw_path, reference_path]
hashes_before = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths}
features = pd.read_csv(reference_path, nrows=0).columns[:27].tolist()
raw = pd.read_excel(raw_path, sheet_name='Faults (2)', dtype=object)
raw.insert(0, 'Source_Row', np.arange(2, len(raw) + 2))
raw['Fault_Type_Clean'] = raw['Faults'].str.lower().str.replace(r'[^a-z0-9]', '', regex=True).map(LABEL_MAP)
conversion_errors = 0
for column in features:
    values = raw[column]
    numeric = pd.to_numeric(values.mask(values.eq('')), errors='coerce')
    conversion_errors += int((values.notna() & values.ne('') & numeric.isna()).sum())
    raw[column] = numeric
duplicates = raw.duplicated(features + ['Production_Date', 'Fault_Type_Clean'], keep='first')
retained = raw.loc[~duplicates].copy()
rows = []

def record(name, unit, count, denominator, note):
    rows.append({'Kiem_tra': name, 'Don_vi_dem': unit, 'So_truong_hop': int(count),
                 'Pham_vi_kiem_tra': int(denominator), 'Dien_giai': note})

record('Ô thiếu trong 27 đặc trưng, trước loại trùng', 'ô', raw[features].isna().sum().sum(), raw[features].size,
       'Phát hiện bằng kiểm tra thiếu; chưa xác định giá trị cần điền.')
record('Chuyển đổi kiểu số thất bại', 'ô', conversion_errors, raw[features].size,
       'Chuỗi không trống nhưng không chuyển được thành số; không gồm ô vốn thiếu.')
record('Biểu diễn nhãn gốc', 'biểu diễn', raw['Faults'].nunique(), len(raw),
       'Số cách biểu diễn; không phải số lỗi hoặc số nhãn ngữ nghĩa.')
record('Dòng trùng theo tiêu chí chuẩn hóa', 'dòng', duplicates.sum(), len(raw),
       '27 đặc trưng + ngày gốc + nhãn chuẩn; giữ dòng đầu.')
record('Ô thiếu sau loại trùng', 'ô', retained[features].isna().sum().sum(), retained[features].size,
       'Tập bản ghi dùng cho kiểm tra trước khôi phục.')

dx = retained['X_Maximum'] - retained['X_Minimum']
dy = retained['Y_Maximum'] - retained['Y_Minimum']
area = retained['Pixels_Areas']
formulas = {
    'Empty_Index': 1 - area / (dx * dy),
    'Log_Y_Index': np.log10(dy),
    'LogOfAreas': np.log10(area),
    'Orientation_Index': (dy - dx) / np.maximum(dx, dy),
}
detected = []
for column, expected in formulas.items():
    eligible = retained[column].notna() & expected.notna() & np.isfinite(expected)
    failed = eligible & (retained[column] - expected.round(4)).abs().gt(0.00010001)
    record(f'Quan hệ nội tại: {column}', 'ô', failed.sum(), eligible.sum(),
           'Quan hệ làm việc đã kiểm chứng trong notebook; kiểm tra trước điền/sửa; không khẳng định định nghĩa chính thức UCI.')
    for _, row in retained.loc[failed].iterrows():
        detected.append({'Source_Row': int(row['Source_Row']), 'Truong': column,
                         'Gia_tri_truoc': row[column], 'Gia_tri_tinh_tu_cung_dong': expected.loc[row.name],
                         'Quy_tac': f'Quan hệ nội tại {column}'})
range_failed = retained['Empty_Index'].notna() & ~retained['Empty_Index'].between(0, 1)
record('Empty_Index ngoài [0, 1]', 'ô', range_failed.sum(), retained['Empty_Index'].notna().sum(),
       'Ràng buộc theo công thức làm việc; có thể trùng ô đã gắn cờ bởi quan hệ nội tại.')

repair = pd.read_csv(ROOT / 'outputs/buoc_3/gia_tri_sua_theo_uci.csv')
detected_table = pd.DataFrame(detected)
intrinsic_pairs = set(zip(detected_table.Source_Row, detected_table.Truong))
reference_pairs = set(zip(repair.Source_Row, repair.Truong))
summary = {
    'audit_stage': 'after normalization and deduplication, before UCI value restoration',
    'raw_rows': len(raw), 'retained_rows': len(retained),
    'intrinsic_formula_flagged_cells': len(intrinsic_pairs),
    'cells_changed_using_uci_in_existing_notebook': len(reference_pairs),
    'overlap_flagged_then_changed_using_uci': len(intrinsic_pairs & reference_pairs),
    'changed_using_uci_not_flagged_by_these_intrinsic_rules': len(reference_pairs - intrinsic_pairs),
    'intrinsic_flags_not_in_existing_repair_log': len(intrinsic_pairs - reference_pairs),
    'notebook_status': 'Supplementary audit; current notebook checks these formulas after restoration.',
    'sources_unchanged': all(hashlib.sha256(p.read_bytes()).hexdigest() == hashes_before[str(p.relative_to(ROOT))] for p in source_paths),
}
out = ROOT / 'outputs/ra_soat_de_cuong'
out.mkdir(parents=True, exist_ok=True)
pd.DataFrame(rows).to_csv(out / 'q0_kiem_tra_truoc_tham_chieu.csv', index=False, encoding='utf-8-sig')
detected_table.to_csv(out / 'q0_o_vi_pham_quan_he_noi_tai.csv', index=False, encoding='utf-8-sig')
(out / 'q0_tom_tat_ra_soat.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(summary, ensure_ascii=True, indent=2))
