"""Kiểm tra các tình huống của bước 6, không gọi API thật."""
from pathlib import Path
import copy
import hashlib
import os
import shutil
import tempfile
import time
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
import requests

import steel_analysis as analysis
from dashboard_charts import box_chart

ROOT = Path(__file__).resolve().parents[1]
TEST_TEMP = ROOT / "outputs/buoc_6/test-tmp"
TEST_TEMP.mkdir(parents=True, exist_ok=True)
# AppTest dùng thư mục tạm trong workspace trên Windows.
os.environ["TMP"] = os.environ["TEMP"] = str(TEST_TEMP)
tempfile.tempdir = str(TEST_TEMP)
from streamlit.testing.v1 import AppTest


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.snapshot = analysis.load_snapshot(ROOT)

    def test_matches_notebook(self):
        source = pd.read_csv(ROOT / "data/analysis/loi_thep_phan_tich.csv")
        actual = self.snapshot.faults
        np.testing.assert_allclose(actual.select_dtypes("number"), source[actual.select_dtypes("number").columns])
        for column in ["Fault_Type_Clean", "Faults", "Steel_Type", "Area_Outlier_Flag", "Source_File"]:
            self.assertTrue(actual[column].equals(source[column]))
        for name, frame in [("co_cau_loi", analysis.fault_structure(actual)),
                            ("loi_theo_dong_thep", analysis.fault_by_steel(actual)),
                            ("dac_trung_theo_nhan", analysis.feature_summary(actual))]:
            pd.testing.assert_frame_equal(frame, pd.read_csv(ROOT / f"outputs/buoc_4/{name}.csv"), check_dtype=False)
        trade = pd.read_csv(ROOT / "data/analysis/thuong_mai_phan_tich.csv")
        trade["HS_Comparison_Note"] = trade["HS_Comparison_Note"].fillna("")
        pd.testing.assert_frame_equal(self.snapshot.trade, trade, check_dtype=False)

    def test_reload_changed_source_and_keep_valid_on_failure(self):
        original = ROOT / "data/raw/practice/data_chua_sach_ko_sua.xlsx"
        original_hash = hashlib.sha256(original.read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory(dir=TEST_TEMP) as folder:
            root = Path(folder)
            shutil.copytree(ROOT / "data/raw", root / "data/raw")
            previous, error = analysis.refresh_snapshot(root=root)
            self.assertIsNone(error)
            path = root / "data/raw/practice/data_chua_sach_ko_sua.xlsx"
            raw = pd.read_excel(path, sheet_name="Faults (2)", dtype=object, keep_default_na=False)
            chosen_key = previous.faults.iloc[0][analysis.KEYS]
            remove = pd.Series(True, index=raw.index)
            for column in analysis.KEYS:
                remove &= pd.to_numeric(raw[column]).eq(chosen_key[column])
            raw.loc[~remove].to_excel(path, sheet_name="Faults (2)", index=False)
            updated, error = analysis.refresh_snapshot(previous, root)
            self.assertIsNone(error)
            self.assertEqual(len(updated.faults), len(previous.faults) - 1)
            self.assertEqual(len(analysis.read_saved_snapshot(root).faults), 1940)
            saved = root / "outputs/buoc_6/runtime/last_valid_snapshot.json"
            saved_hash = hashlib.sha256(saved.read_bytes()).hexdigest()
            raw.drop(columns="Faults").to_excel(path, sheet_name="Faults (2)", index=False)
            failed, error = analysis.refresh_snapshot(updated, root)
            self.assertIs(failed, updated)
            self.assertIsNotNone(error)
            self.assertEqual(hashlib.sha256(saved.read_bytes()).hexdigest(), saved_hash)
        self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(), original_hash)

    def test_api_scope_error_and_partial_missing(self):
        pack = copy.deepcopy(analysis.read_trade_pack(ROOT))
        query = next(q for q in pack["queries"] if q["year"] == 2023 and q["flow"] == "M")
        query["payload"]["data"] = []
        clean, coverage, _ = analysis.clean_trade(pack)
        result = analysis.add_trade_metrics(clean).set_index("Year")
        self.assertTrue(pd.isna(result.loc[2023, "Import_USD"]))
        self.assertTrue(pd.isna(result.loc[2023, "Trade_Balance_USD"]))
        self.assertTrue(pd.notna(result.loc[2023, "Export_USD"]))
        self.assertFalse(coverage.loc[coverage.Year.eq(2023), "Du_hai_luong"].iloc[0])
        query = next(q for q in pack["queries"] if q["year"] == 2023 and q["flow"] == "X")
        query["payload"]["data"][0]["reporterCode"] = 156
        with self.assertRaises(analysis.DataError):
            analysis.clean_trade(pack)

    def test_growth_gaps_and_zero(self):
        source = pd.DataFrame({"Year": [2015, 2016, 2017, 2019, 2020],
            "Export_USD": [100, 0, 50, 100, 130], "Import_USD": [80, 100, 120, 100, 0],
            "classificationCode": ["H4", "H4", "H5", "H5", "H6"]})
        result = analysis.add_trade_metrics(source).set_index("Year")
        self.assertEqual(result.loc[2016, "Export_Growth_Percent"], -100)
        self.assertEqual(result.loc[2017, "Export_Change_USD"], 50)
        self.assertTrue(pd.isna(result.loc[2017, "Export_Growth_Percent"]))
        self.assertTrue(result.loc[[2018, 2019], ["Export_Growth_Percent", "Import_Growth_Percent"]].isna().all().all())
        self.assertEqual(result.loc[2020, "Export_Growth_Percent"], 30)
        self.assertEqual(result.loc[2020, "Import_Growth_Percent"], -100)

    def test_api_failure_and_retry(self):
        with self.assertRaises(requests.ConnectionError):
            analysis.fetch_trade_pack(get=lambda *args, **kwargs: (_ for _ in ()).throw(requests.ConnectionError("Mất mạng")))
        class Response:
            status_code = 429
            def raise_for_status(self):
                raise requests.HTTPError("429")
        attempts = []
        def get(*args, **kwargs):
            attempts.append(kwargs["params"])
            return Response()
        with self.assertRaises(requests.HTTPError):
            analysis.fetch_trade_pack(get=get, pause=lambda seconds: None)
        self.assertEqual(len(attempts), 2)

    def test_boxplot_uses_original_linear_quantiles(self):
        fig = box_chart(self.snapshot.faults, "Pixels_Areas", "Diện tích", "Diện tích", True)
        self.assertEqual(fig.layout.xaxis.type, "log")
        trace = next(t for t in fig.data if t.type == "box" and t.name == "K_Scatch")
        values = self.snapshot.faults.loc[self.snapshot.faults.Fault_Type_Clean.eq("K_Scatch"), "Pixels_Areas"]
        np.testing.assert_allclose([trace.q1[0], trace.median[0], trace.q3[0]], np.quantile(values, [.25, .5, .75]))


class AppTests(unittest.TestCase):
    def setUp(self):
        self.at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()
        self.assertFalse(self.at.exception)

    def check_clean(self):
        self.assertFalse(self.at.exception, [item.message for item in self.at.exception])
        self.assertFalse(any("default value" in item.value and "Session State" in item.value
                             for item in self.at.warning),
                         [item.value for item in self.at.warning])

    def test_first_load(self):
        self.assertEqual([tab.label for tab in self.at.tabs], ["Phân tích lỗi thép", "Bối cảnh ngành", "Dữ liệu và chất lượng"])
        self.assertEqual(self.at.metric[0].value, "1.941")
        self.assertEqual(self.at.metric[4].value, "8.51")
        self.assertEqual(len(self.at.get("plotly_chart")), 9)
        self.assertEqual(len(self.at.get("download_button")), 2)

    def test_filters_trade_independence_and_reset(self):
        trade_before = self.at.session_state["selected_trade"].copy()
        self.at.multiselect(key="steel_filter").set_value(["A300"]).run()
        self.check_clean()
        self.assertEqual(self.at.metric[0].value, "777")
        pd.testing.assert_frame_equal(self.at.session_state["selected_trade"], trade_before)
        self.at.multiselect(key="fault_filter").set_value(["K_Scatch"]).run()
        self.check_clean()
        self.assertEqual(self.at.metric[0].value, "1")
        self.at.button(key="reset_filters").click().run()
        self.check_clean()
        self.assertEqual(self.at.metric[0].value, "1.941")
        self.at.multiselect(key="steel_filter").set_value(["A400"]).run()
        self.check_clean()
        self.assertEqual(self.at.metric[0].value, "1.164")
        self.at.multiselect(key="fault_filter").set_value(["K_Scatch"]).run()
        self.check_clean()
        self.assertEqual([metric.value for metric in self.at.metric[:4]],
                         ["390", "1", "6.281,5", "40,0"])
        pd.testing.assert_frame_equal(self.at.session_state["selected_trade"], trade_before)
        self.at.multiselect(key="fault_filter").set_value(self.at.multiselect(key="fault_filter").options).run()
        self.check_clean()
        self.at.slider(key="thickness_filter").set_value((50, 80)).run()
        self.check_clean()
        actual = self.at.session_state["selected_faults"]
        self.assertFalse(actual.empty)
        self.assertTrue(actual.Steel_Type.eq("A400").all() and actual.Steel_Plate_Thickness.between(50, 80).all())

    def test_empty_filter_and_missing_year(self):
        self.at.multiselect(key="fault_filter").set_value([]).run()
        self.check_clean()
        self.assertEqual(self.at.metric[0].value, "0")
        self.assertEqual(self.at.metric[2].value, "—")
        self.assertTrue(any("Không có bản ghi" in item.value for item in self.at.info))
        self.at.selectbox(key="kpi_year").set_value(2024).run()
        self.check_clean()
        self.assertEqual(self.at.metric[4].value, "Chưa có dữ liệu")
        self.at.slider(key="year_range").set_value((2023, 2023)).run()
        self.check_clean()
        self.assertEqual(self.at.session_state["selected_trade"].Year.tolist(), [2023])

    def test_api_failure_keeps_last_data(self):
        before = self.at.session_state["snapshot"]
        self.at.checkbox(key="use_api").set_value(True).run()
        with patch.object(analysis, "fetch_trade_pack", side_effect=requests.ConnectionError("Mất mạng thử nghiệm")):
            self.at.button(key="refresh").click().run()
        self.check_clean()
        self.assertEqual(self.at.session_state["snapshot"].checked_at, before.checked_at)
        self.assertTrue(any("Giữ bản hợp lệ" in item.value for item in self.at.warning))
        self.assertEqual(self.at.metric[0].value, "1.941")

    def test_manual_and_periodic_refresh_read_sources(self):
        with patch.object(analysis, "load_snapshot", wraps=analysis.load_snapshot) as loader:
            self.at.button(key="refresh").click().run()
            self.check_clean()
            self.assertEqual(loader.call_count, 1)
        self.at.session_state["last_attempt"] = time.monotonic() - 301
        with patch.object(analysis, "load_snapshot", wraps=analysis.load_snapshot) as loader:
            self.at.run()
            self.check_clean()
            self.assertEqual(loader.call_count, 1)
        self.at.checkbox(key="auto_refresh").set_value(False).run()
        self.at.session_state["last_attempt"] = time.monotonic() - 301
        with patch.object(analysis, "load_snapshot", wraps=analysis.load_snapshot) as loader:
            self.at.run()
            self.assertEqual(loader.call_count, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
