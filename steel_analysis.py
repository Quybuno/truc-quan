"""Xử lý dùng chung cho Chương 6 trong notebook và dashboard.

Các bước giữ riêng thành hàm ngắn: đọc nguồn, làm sạch, tạo biến, tổng hợp.
Không sửa dữ liệu thô hoặc các kết quả notebook bước 1–5.
"""
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from io import StringIO
from pathlib import Path
import hashlib
import json
import re
import time
from uuid import uuid4

import numpy as np
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent
VN_TIME = timezone(timedelta(hours=7))
YEARS = list(range(2015, 2025))
KEYS = ["X_Minimum", "X_Maximum", "Y_Minimum", "Y_Maximum"]
LABELS = ["Pastry", "Z_Scratch", "K_Scratch", "Stains", "Dirtiness", "Bumps", "Other_Faults"]
COLORS = {"Other_Faults": "#737373", "Bumps": "#0072B2", "K_Scatch": "#E69F00",
          "Z_Scratch": "#9B59B6", "Pastry": "#009E73", "Stains": "#D55E00", "Dirtiness": "#8C564B"}
LABEL_MAP = {"pastry": "Pastry", "pastrry": "Pastry", "pasty": "Pastry",
             "zscratch": "Z_Scratch", "zsccratch": "Z_Scratch",
             "kscatch": "K_Scatch", "kkscatch": "K_Scatch", "kscratch": "K_Scatch",
             "stains": "Stains", "dirtiness": "Dirtiness", "dirttiness": "Dirtiness",
             "dirtinesss": "Dirtiness", "bumps": "Bumps", "otherfaults": "Other_Faults",
             "otherrfaults": "Other_Faults"}
DATE_MAP = {f"nov{day}2025": f"2025-11-{day:02d}" for day in [2, 3, 10, 21, 30]}
DATE_MAP.update({"21/11/2025": "2025-11-21", "30/11/2025": "2025-11-30"})
API_URL = "https://comtradeapi.un.org/public/v1/preview/C/A/HS"


class DataError(ValueError):
    """Nguồn chưa đạt điều kiện để thay bản dữ liệu đang hiển thị."""


def require(condition, message):
    if not condition:
        raise DataError(message)


def now_text():
    return datetime.now(VN_TIME).isoformat(timespec="seconds")


def clean_simulated_date(value):
    if isinstance(value, (datetime, pd.Timestamp)):
        if value.year == 2025 and value.month == 11 and value.day in [2, 3, 10, 21, 30]:
            return pd.Timestamp(value)
        if value.year == 2025 and value.day == 11 and value.month in [2, 3, 10]:
            return pd.Timestamp(year=2025, month=11, day=value.month)
    if isinstance(value, str):
        key = value.lower().replace("november", "nov")
        key = re.sub(r"st|nd|rd|th", "", key)
        key = re.sub(r"[\s,]", "", key)
        if key in DATE_MAP:
            return pd.Timestamp(DATE_MAP[key])
    raise DataError(f"Ngày mô phỏng ngoài quy tắc: {value!r}.")


def clean_faults(practice, uci, filename="data_chua_sach_ko_sua.xlsx"):
    """Ghép từng dòng Excel với UCI bằng khóa tọa độ duy nhất."""
    features = [c for c in uci.columns if c not in LABELS]
    require(len(features) == 27 and set(LABELS).issubset(uci.columns), "UCI không đúng cấu trúc 27 đặc trưng/7 nhãn.")
    require(set(features + ["Faults", "Production_Date"]).issubset(practice.columns), "Excel thiếu cột bắt buộc.")
    require(not practice.empty, "Excel không có bản ghi.")
    require(uci[features].notna().all().all() and np.isfinite(uci[features].to_numpy(dtype=float)).all(), "UCI có giá trị thiếu/vô hạn.")
    require(uci[LABELS].isin([0, 1]).all().all() and uci[LABELS].sum(axis=1).eq(1).all(), "Nhãn UCI không đúng one-hot.")
    data = practice.copy(deep=True)
    original_columns = practice.columns.tolist()
    data.insert(0, "Source_Row", np.arange(2, len(data) + 2))
    data.insert(1, "Source_File", filename)
    label_key = data["Faults"].astype(str).str.lower().str.replace(r"[^a-z0-9]", "", regex=True)
    data["Fault_Type_Clean"] = label_key.map(LABEL_MAP)
    require(data["Fault_Type_Clean"].notna().all(), "Excel có nhãn lỗi chưa được ánh xạ.")
    for column in features:
        original = data[column]
        numeric = pd.to_numeric(original.mask(original.eq("")), errors="coerce")
        invalid = original.notna() & original.ne("") & numeric.isna()
        require(not invalid.any(), f"{column} có chuỗi số không hợp lệ.")
        data[column] = numeric
    duplicate_columns = features + ["Production_Date", "Fault_Type_Clean"]
    duplicate = data.duplicated(duplicate_columns, keep="first")
    data = data.loc[~duplicate].copy()
    reference = uci[features].copy()
    reference["Source_Row_UCI"] = np.arange(2, len(uci) + 2)
    reference["Fault_Type_UCI"] = uci[LABELS].idxmax(axis=1).replace({"K_Scratch": "K_Scatch"})
    for table in [data, reference]:
        require(table[KEYS].notna().all().all() and not table.duplicated(KEYS).any(), "Khóa tọa độ thiếu hoặc trùng; chưa thể ghép.")
        require(table[KEYS].mod(1).eq(0).all().all(), "Khóa tọa độ không phải số nguyên.")
    merged = data.merge(reference, on=KEYS, how="left", suffixes=("", "_UCI"), validate="one_to_one", indicator=True)
    unmatched = int(merged["_merge"].ne("both").sum())
    require(unmatched == 0, f"Có {unmatched} dòng chưa ghép được với UCI.")
    require(merged["Fault_Type_Clean"].eq(merged["Fault_Type_UCI"]).all(), "Nhãn Excel không khớp nhãn UCI.")
    restored, corrected = 0, 0
    for column in [c for c in features if c not in KEYS]:
        missing = merged[column].isna()
        different = ~missing & ~np.isclose(merged[column], merged[column + "_UCI"], rtol=0, atol=1e-9)
        restored += int(missing.sum())
        corrected += int(different.sum())
        merged[column] = merged[column + "_UCI"]
    merged["Production_Date_Clean"] = pd.to_datetime(merged["Production_Date"].map(clean_simulated_date))
    merged["Date_Is_Simulated"] = True
    q1, q3 = merged["Pixels_Areas"].quantile([0.25, 0.75])
    iqr = q3 - q1
    merged["Area_Outlier_Flag"] = merged["Pixels_Areas"].lt(q1 - 1.5 * iqr) | merged["Pixels_Areas"].gt(q3 + 1.5 * iqr)
    extras = ["Fault_Type_Clean", "Production_Date_Clean", "Date_Is_Simulated", "Area_Outlier_Flag"]
    cleaned = merged[["Source_Row", "Source_File", "Source_Row_UCI"] + original_columns + extras].copy()
    quality = {"input_rows": len(practice), "input_columns": len(practice.columns), "clean_rows": len(cleaned),
               "duplicates_removed": int(duplicate.sum()), "missing_restored": restored,
               "numeric_corrected": corrected, "unmatched_rows": unmatched, "feature_mismatches": 0,
               "labels_match": True, "area_flags_retained": int(cleaned["Area_Outlier_Flag"].sum()),
               "reference_rows": len(uci), "reference_coverage_percent": len(cleaned) / len(uci) * 100}
    return cleaned, quality


def add_fault_features(cleaned):
    data = cleaned.copy(deep=True)
    flags = data[["TypeOfSteel_A300", "TypeOfSteel_A400"]]
    require(flags.isin([0, 1]).all().all() and flags.sum(axis=1).eq(1).all(), "Hai cờ dòng thép không hợp lệ.")
    data["Steel_Type"] = np.where(data["TypeOfSteel_A300"].eq(1), "A300", "A400")
    data["X_Range"] = data["X_Maximum"] - data["X_Minimum"]
    data["Y_Range"] = data["Y_Maximum"] - data["Y_Minimum"]
    data["Luminosity_Range"] = data["Maximum_of_Luminosity"] - data["Minimum_of_Luminosity"]
    require(data[["X_Range", "Y_Range", "Pixels_Areas", "Steel_Plate_Thickness"]].gt(0).all().all(), "Kích thước, diện tích hoặc độ dày không dương.")
    require(data["Luminosity_Range"].ge(0).all(), "Độ sáng nhỏ nhất lớn hơn độ sáng lớn nhất.")
    require(data["Minimum_of_Luminosity"].ge(0).all() and data["Maximum_of_Luminosity"].le(255).all(), "Độ sáng ngoài 0–255.")
    require(data["X_Minimum"].ge(0).all() and data["X_Maximum"].le(data["Length_of_Conveyer"]).all(), "Tọa độ ngoài vùng quét.")
    data["Log_Pixels_Areas"] = np.log10(data["Pixels_Areas"].astype(float))
    require((data["Log_Pixels_Areas"] - data["LogOfAreas"]).abs().le(0.00010001).all(), "Log diện tích không khớp nguồn.")
    return data


def fault_structure(data):
    result = data["Fault_Type_Clean"].value_counts().rename_axis("Fault_Type_Clean").reset_index(name="Count")
    result = result.sort_values(["Count", "Fault_Type_Clean"], ascending=[False, True]).reset_index(drop=True)
    result["Percent"] = result["Count"] / len(data) * 100 if len(data) else pd.Series(dtype=float)
    result["Cumulative_Count"] = result["Count"].cumsum()
    result["Cumulative_Percent"] = result["Percent"].cumsum()
    return result


def fault_by_steel(data):
    order = fault_structure(data)["Fault_Type_Clean"].tolist()
    cross = pd.crosstab(data["Fault_Type_Clean"], data["Steel_Type"]).reindex(index=order, columns=["A300", "A400"], fill_value=0)
    result = cross.reset_index().melt(id_vars="Fault_Type_Clean", var_name="Steel_Type", value_name="Count")
    result["N_Steel"] = result["Steel_Type"].map(cross.sum(axis=0))
    result["N_Fault"] = result["Fault_Type_Clean"].map(cross.sum(axis=1))
    result["Percent_Within_Steel"] = result["Count"] / result["N_Steel"].where(result["N_Steel"].gt(0)) * 100
    result["Percent_Within_Fault"] = result["Count"] / result["N_Fault"].where(result["N_Fault"].gt(0)) * 100
    return result


def feature_summary(data):
    order = fault_structure(data)["Fault_Type_Clean"].tolist()
    tables = []
    for column in ["Minimum_of_Luminosity", "Maximum_of_Luminosity", "Steel_Plate_Thickness", "Pixels_Areas"]:
        table = data.groupby("Fault_Type_Clean")[column].agg(N="count", Mean="mean", Median="median", Std="std",
            Q1=lambda group: group.quantile(.25), Q3=lambda group: group.quantile(.75), Min="min", Max="max")
        table = table.reindex(order).reset_index()
        table.insert(1, "Variable", column)
        tables.append(table)
    return pd.concat(tables, ignore_index=True)


def filter_faults(data, steel_types, fault_types, thickness_range):
    condition = (data["Steel_Type"].isin(steel_types) & data["Fault_Type_Clean"].isin(fault_types)
                 & data["Steel_Plate_Thickness"].between(*thickness_range))
    return data.loc[condition].copy()


def fault_kpis(data):
    return {"N": len(data), "Labels": data["Fault_Type_Clean"].nunique(),
            "Median_Area": data["Pixels_Areas"].median(), "Median_Thickness": data["Steel_Plate_Thickness"].median()}


def validate_query(payload, year, flow):
    require(isinstance(payload, dict) and not payload.get("error") and isinstance(payload.get("data"), list), "API không trả danh sách data hợp lệ.")
    rows = payload["data"]
    require(len(rows) < 500, "Phản hồi chạm giới hạn 500 dòng; chưa thể xác nhận đầy đủ.")
    require(len(rows) <= 1, f"Có nhiều bản ghi cho {year}/{flow}; không tự cộng.")
    expected = {"reporterCode": "704", "partnerCode": "0", "partner2Code": "0", "cmdCode": "72",
                "typeCode": "C", "freqCode": "A", "customsCode": "C00", "motCode": "0", "period": str(year), "flowCode": flow}
    for row in rows:
        require(all(str(row.get(c)) == v for c, v in expected.items()), f"API trả sai phạm vi {year}/{flow}.")
        require(row.get("isOriginalClassification") is True and row.get("classificationCode") in ["H4", "H5", "H6"], "Phân loại HS cần được kiểm tra.")
        value = pd.to_numeric(row.get("primaryValue"), errors="coerce")
        require(pd.notna(value) and np.isfinite(value) and value >= 0, "Trị giá thương mại thiếu/âm/vô hạn.")
    return rows


def read_trade_pack(root=ROOT, prefer_cached=True):
    accepted = root / "outputs/buoc_6/runtime/comtrade_accepted.json"
    if prefer_cached and accepted.exists():
        return json.loads(accepted.read_text(encoding="utf-8"))
    queries = []
    for year in YEARS:
        for flow in ["X", "M"]:
            path = root / f"data/raw/comtrade/vnm_hs72_{year}_{flow}.json"
            metadata_path = root / "outputs/buoc_1_2/metadata_nguon" / path.relative_to(root / "data/raw").with_suffix(".download.json")
            metadata = json.loads(metadata_path.read_text(encoding="utf-8")) if metadata_path.exists() else {}
            queries.append({"year": year, "flow": flow, "payload": json.loads(path.read_text(encoding="utf-8")),
                            "retrieved_at": metadata.get("retrieved_at", "Không có hồ sơ thời điểm tải"),
                            "source_url": metadata.get("source_url", API_URL),
                            "source_file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    return {"queries": queries}


def clean_trade(pack):
    require(isinstance(pack, dict) and isinstance(pack.get("queries"), list), "Bộ JSON thương mại không hợp lệ.")
    expected = {(year, flow) for year in YEARS for flow in ["X", "M"]}
    keys = [(item["year"], item["flow"]) for item in pack["queries"]]
    require(len(keys) == len(set(keys)) and set(keys) == expected, "Chưa có trạng thái của đủ 20 truy vấn thương mại.")
    rows, receipts = [], []
    for query in pack["queries"]:
        year, flow = query["year"], query["flow"]
        records = validate_query(query["payload"], year, flow)
        receipts.append({"Year": year, "Flow": flow, "Status": "Có dữ liệu" if records else "Không có dữ liệu",
                         "retrieved_at": query["retrieved_at"], "source_url": query["source_url"], "sha256": query["sha256"]})
        for row in records:
            rows.append({"Year": year, "reporterCode": 704, "partnerCode": 0, "cmdCode": 72,
                         "classificationCode": row["classificationCode"], "Flow": flow,
                         "Value": float(row["primaryValue"]), "Source_File": query["source_file"]})
    columns = ["Year", "reporterCode", "partnerCode", "cmdCode", "classificationCode", "Flow", "Value", "Source_File"]
    long = pd.DataFrame(rows, columns=columns)
    join_keys = columns[:5]
    export = long.loc[long["Flow"].eq("X"), join_keys + ["Value", "Source_File"]].rename(columns={"Value": "Export_USD", "Source_File": "Export_Source_File"})
    imports = long.loc[long["Flow"].eq("M"), join_keys + ["Value", "Source_File"]].rename(columns={"Value": "Import_USD", "Source_File": "Import_Source_File"})
    combined = export.merge(imports, on=join_keys, how="outer", validate="one_to_one").sort_values("Year")
    require(combined["Year"].is_unique, "Hai luồng cùng năm khác phiên bản HS.")
    coverage = pd.DataFrame({"Year": YEARS}).merge(combined, on="Year", how="left", validate="one_to_one")
    coverage["Du_hai_luong"] = coverage[["Export_USD", "Import_USD"]].notna().all(axis=1)
    # Cho phép một luồng thiếu; không thay bằng 0 hoặc bỏ luồng còn lại.
    return combined.reset_index(drop=True), coverage, pd.DataFrame(receipts)


def add_trade_metrics(cleaned):
    data = cleaned.copy(deep=True).sort_values("Year")
    if data.empty:
        data = pd.DataFrame({"Year": YEARS}).merge(data, on="Year", how="left")
    else:
        data = data.set_index("Year").reindex(range(int(data["Year"].min()), int(data["Year"].max()) + 1)).rename_axis("Year").reset_index()
    consecutive = data["Year"].diff().eq(1)
    data["Trade_Balance_USD"] = data["Export_USD"] - data["Import_USD"]
    for flow, column in [("Export", "Export_USD"), ("Import", "Import_USD")]:
        previous = data[column].shift(1)
        valid = consecutive & data[column].notna() & previous.notna()
        change = (data[column] - previous).where(valid)
        data[f"{flow}_Change_USD"] = change
        data[f"{flow}_Growth_Percent"] = change / previous.where(previous.ne(0)) * 100
    data["Trade_Balance_Change_USD"] = data["Trade_Balance_USD"].diff().where(consecutive)
    current_hs, previous_hs = data["classificationCode"], data["classificationCode"].shift(1)
    data["HS_Version_Changed"] = consecutive & current_hs.notna() & previous_hs.notna() & current_hs.ne(previous_hs)
    data["HS_Comparison_Note"] = np.where(data["HS_Version_Changed"], "Khác phiên bản HS năm trước; chưa quy đổi", "")
    return data


@dataclass
class Snapshot:
    faults: pd.DataFrame
    trade: pd.DataFrame
    coverage: pd.DataFrame
    receipts: pd.DataFrame
    sources: pd.DataFrame
    quality: dict
    checked_at: str


def load_snapshot(root=ROOT, trade_pack=None):
    """Mỗi lần gọi đều đọc lại Excel, UCI và JSON; chỉ trả bản hoàn chỉnh đã kiểm tra."""
    root = Path(root)
    practice_file = root / "data/raw/practice/data_chua_sach_ko_sua.xlsx"
    uci_file = root / "data/raw/uci/steel_plates_faults_original.csv"
    practice = pd.read_excel(practice_file, sheet_name="Faults (2)", dtype=object, keep_default_na=False)
    uci = pd.read_csv(uci_file)
    cleaned, quality = clean_faults(practice, uci, practice_file.name)
    faults = add_fault_features(cleaned)
    pack = read_trade_pack(root) if trade_pack is None else trade_pack
    trade_clean, coverage, receipts = clean_trade(pack)
    trade = add_trade_metrics(trade_clean)
    sources = []
    for path, label in [(practice_file, "Excel thực hành"), (uci_file, "UCI đối chiếu")]:
        metadata_path = root / "outputs/buoc_1_2/metadata_nguon" / path.relative_to(root / "data/raw").with_suffix(".download.json")
        metadata = json.loads(metadata_path.read_text(encoding="utf-8")) if metadata_path.exists() else {}
        sources.append({"Nguon": label, "File": str(path.relative_to(root)), "SHA256_hien_tai": hashlib.sha256(path.read_bytes()).hexdigest(),
                        "Lan_tai_goc": metadata.get("retrieved_at", "Xem hồ sơ bước 2"),
                        "URL": metadata.get("source_url", "https://archive.ics.uci.edu/dataset/198/steel+plates+faults")})
    return Snapshot(faults, trade, coverage, receipts, pd.DataFrame(sources), quality, now_text())


def fetch_trade_pack(get=requests.get, pause=time.sleep):
    """20 truy vấn rõ tham số; lỗi bất kỳ truy vấn nào thì chưa chấp nhận bộ mới."""
    queries = []
    for year in YEARS:
        for flow in ["X", "M"]:
            params = {"reporterCode": 704, "period": str(year), "cmdCode": "72", "flowCode": flow,
                      "partnerCode": 0, "partner2Code": 0, "customsCode": "C00", "motCode": 0,
                      "maxRecords": 500, "includeDesc": "true"}
            response = get(API_URL, params=params, timeout=20)
            if response.status_code == 429:
                pause(5)
                response = get(API_URL, params=params, timeout=20)
            response.raise_for_status()
            payload = response.json()
            validate_query(payload, year, flow)
            serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
            queries.append({"year": year, "flow": flow, "payload": payload, "retrieved_at": now_text(),
                            "source_url": response.url, "source_file": f"vnm_hs72_{year}_{flow}.json",
                            "sha256": hashlib.sha256(serialized).hexdigest()})
            pause(1)
    return {"queries": queries}


def atomic_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.stem}.{uuid4().hex}.tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)


def save_snapshot(snapshot, root=ROOT):
    tables = {name: getattr(snapshot, name).to_json(orient="table", date_format="iso", double_precision=15)
              for name in ["faults", "trade", "coverage", "receipts", "sources"]}
    atomic_json(Path(root) / "outputs/buoc_6/runtime/last_valid_snapshot.json",
                {"tables": tables, "quality": snapshot.quality, "checked_at": snapshot.checked_at})


def read_saved_snapshot(root=ROOT):
    path = Path(root) / "outputs/buoc_6/runtime/last_valid_snapshot.json"
    if not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    tables = {name: pd.read_json(StringIO(content), orient="table") for name, content in payload["tables"].items()}
    return Snapshot(**tables, quality=payload["quality"], checked_at=payload["checked_at"])


def refresh_snapshot(previous=None, root=ROOT, trade_pack=None):
    """Thất bại giữ nguyên bản cũ; chỉ lưu gói API sau khi toàn bộ pipeline đạt."""
    try:
        candidate = load_snapshot(root, trade_pack)
        save_snapshot(candidate, root)
        if trade_pack is not None:
            atomic_json(Path(root) / "outputs/buoc_6/runtime/comtrade_accepted.json", trade_pack)
        return candidate, None
    except (DataError, OSError, ValueError, KeyError, TypeError) as error:
        return previous, str(error)
