"""Chạy: python -m streamlit run app.py"""
from pathlib import Path
import time
import pandas as pd
import streamlit as st

import steel_analysis as analysis
from dashboard_charts import (structure_chart, pareto_chart, steel_charts, brightness_chart,
                              box_chart, trade_charts)

st.set_page_config(page_title="Lỗi bề mặt thép", page_icon="📊", layout="wide")
ROOT = Path(__file__).resolve().parent
st.title("Phân tích lỗi bề mặt thép")
st.caption("Steel Plates Faults · 7 nhãn lỗi · A300 / A400 · Bối cảnh thương mại Việt Nam")


def format_number(value, decimals=0):
    """Định dạng số tiếng Việt cho các KPI và phạm vi đang chọn."""
    return f"{value:,.{decimals}f}".translate(str.maketrans({",": ".", ".": ","}))


@st.cache_data(ttl=900, show_spinner=False)
def cached_api_pack():
    return analysis.fetch_trade_pack()


def update_data(use_api=False, force_api=False):
    previous = st.session_state.get("snapshot")
    try:
        if force_api:
            cached_api_pack.clear()
        pack = cached_api_pack() if use_api else None
        snapshot, error = analysis.refresh_snapshot(previous, ROOT, pack)
    except Exception as exc:
        snapshot, error = previous, f"Không cập nhật được nguồn dữ liệu: {exc}"
    st.session_state["last_attempt"] = time.monotonic()
    st.session_state["update_error"] = error
    if snapshot is not None:
        st.session_state["snapshot"] = snapshot
    if snapshot is None:
        try:
            saved = analysis.read_saved_snapshot(ROOT)
            if saved is not None:
                st.session_state["snapshot"] = saved
        except (OSError, ValueError, KeyError):
            pass


if "snapshot" not in st.session_state:
    update_data()

with st.sidebar:
    st.header("Cập nhật dữ liệu")
    auto_refresh = st.checkbox("Tự đọc lại mỗi 5 phút", value=True, key="auto_refresh")
    use_api = st.checkbox("Gọi lại UN Comtrade khi làm mới", value=False, key="use_api")
    st.caption("Mặc định đọc Excel, UCI và JSON đã lưu. Gọi API cần mạng và gồm 20 truy vấn.")
    if st.button("Làm mới dữ liệu", key="refresh", width="stretch"):
        with st.spinner("Đọc nguồn và kiểm tra dữ liệu…"):
            update_data(use_api=use_api, force_api=use_api)
    st.caption("API tự động dùng bộ nhớ đệm 15 phút; nút làm mới gọi lại trực tiếp.")

if "snapshot" not in st.session_state:
    st.error(f"Chưa có bản dữ liệu hợp lệ. {st.session_state.get('update_error', '')}")
    st.stop()


@st.fragment(run_every="5m" if auto_refresh else None)
def live_dashboard():
    # Bộ lọc chỉ vẽ lại; hết 5 phút mới đọc lại nguồn.
    if auto_refresh and time.monotonic() - st.session_state.get("last_attempt", 0) >= 300:
        update_data(use_api=use_api)
    snapshot = st.session_state["snapshot"]
    if st.session_state.get("update_error"):
        st.warning(f"Lần làm mới chưa thành công: {st.session_state['update_error']}. Giữ bản hợp lệ kiểm tra lúc {snapshot.checked_at}.")
    else:
        st.caption(f"Bản dữ liệu hợp lệ kiểm tra lúc {snapshot.checked_at} (UTC+07:00)")
    fault_tab, trade_tab, quality_tab = st.tabs(["Phân tích lỗi thép", "Bối cảnh ngành", "Dữ liệu và chất lượng"])

    with fault_tab:
        data = snapshot.faults
        all_labels = analysis.fault_structure(data)["Fault_Type_Clean"].tolist()
        thickness_min = int(data["Steel_Plate_Thickness"].min())
        thickness_max = int(data["Steel_Plate_Thickness"].max())
        st.subheader("Chọn phạm vi phân tích")
        if st.button("Đặt lại bộ lọc", key="reset_filters"):
            for key in ["steel_filter", "fault_filter", "thickness_filter"]:
                st.session_state.pop(key, None)
        # Loại giá trị bộ lọc không còn hợp lệ khi nguồn thay đổi.
        for key, options in [("steel_filter", ["A300", "A400"]), ("fault_filter", all_labels)]:
            if key in st.session_state:
                valid_values = [v for v in st.session_state[key] if v in options]
                if valid_values != st.session_state[key]:
                    st.session_state[key] = valid_values
            else:
                st.session_state[key] = list(options)
        if "thickness_filter" in st.session_state:
            low, high = st.session_state["thickness_filter"]
            if low < thickness_min or high > thickness_max:
                st.session_state.pop("thickness_filter")
        c1, c2, c3 = st.columns([1.3, 1.7, 2])
        with c1:
            steels = st.multiselect("Dòng thép", ["A300", "A400"], key="steel_filter")
        with c2:
            labels = st.multiselect("Loại lỗi", all_labels, key="fault_filter")
        with c3:
            if thickness_min < thickness_max:
                if "thickness_filter" not in st.session_state:
                    st.session_state["thickness_filter"] = (thickness_min, thickness_max)
                thickness = st.slider("Khoảng độ dày (giá trị nguồn)", thickness_min, thickness_max,
                                      key="thickness_filter")
            else:
                thickness = (thickness_min, thickness_max)
                st.caption(f"Độ dày duy nhất trong nguồn: {thickness_min}")
        selected = analysis.filter_faults(data, steels, labels, thickness)
        st.session_state["selected_faults"] = selected
        kpi = analysis.fault_kpis(selected)
        st.caption(f"Đang xem {format_number(len(selected))} / {format_number(len(data))} bản ghi lỗi. Các tỷ trọng dưới đây được tính trong phạm vi đang chọn.")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Bản ghi đang chọn", format_number(kpi['N']))
        m2.metric("Loại lỗi xuất hiện", str(kpi["Labels"]))
        m3.metric("Trung vị diện tích", format_number(kpi['Median_Area'], 1) if pd.notna(kpi["Median_Area"]) else "—")
        m4.metric("Trung vị độ dày", format_number(kpi['Median_Thickness'], 1) if pd.notna(kpi["Median_Thickness"]) else "—")
        if selected.empty:
            st.info("Không có bản ghi phù hợp. Hãy mở rộng bộ lọc hoặc đặt lại bộ lọc.")
        else:
            left, right = st.columns(2)
            with left:
                st.plotly_chart(structure_chart(selected), width="stretch", key="structure")
            with right:
                st.plotly_chart(pareto_chart(selected), width="stretch", key="pareto")
            counts, shares = steel_charts(selected)
            left, right = st.columns(2)
            with left:
                st.plotly_chart(counts, width="stretch", key="steel_counts")
            with right:
                st.plotly_chart(shares, width="stretch", key="steel_shares")
            st.caption("Số lượng: màu theo loại lỗi, họa tiết theo dòng thép. Tỷ trọng: mẫu số là bản ghi lỗi của từng dòng trong phạm vi đang chọn; dòng không có mẫu chưa có tỷ trọng.")
            st.plotly_chart(brightness_chart(selected), width="stretch", key="brightness")
            left, right = st.columns(2)
            with left:
                st.plotly_chart(box_chart(selected, "Steel_Plate_Thickness", "Độ dày theo loại lỗi", "Độ dày (chưa xác nhận đơn vị)"), width="stretch", key="thickness")
            with right:
                st.plotly_chart(box_chart(selected, "Pixels_Areas", "Diện tích theo loại lỗi", "Pixels_Areas (trục log cơ số 10)", True), width="stretch", key="area")
            st.caption("Boxplot tính trên thang gốc, Q1/Q3 nội suy tuyến tính; giữ điểm ngoài râu từng nhóm. Trục log chỉ thay cách hiển thị diện tích.")
            with st.expander("Bảng số liệu hỗ trợ và giới hạn diễn giải"):
                st.dataframe(analysis.feature_summary(selected).round(2), width="stretch", hide_index=True)
                st.dataframe(analysis.fault_by_steel(selected).round(2), width="stretch", hide_index=True)
                st.write("Các quan sát mô tả mẫu lỗi. Thiếu sản lượng, biến vận hành và chi phí; chưa kết luận rủi ro sản phẩm, nguyên nhân hoặc mức thiệt hại. Ngày là mô phỏng.")

    with trade_tab:
        st.subheader("Thương mại sắt và thép Việt Nam")
        st.caption("Việt Nam (704) · HS 72 · Toàn thế giới (0) · Trị giá danh nghĩa theo năm")
        years = snapshot.coverage["Year"].astype(int).tolist()
        if "year_range" in st.session_state:
            low, high = st.session_state["year_range"]
            if low < min(years) or high > max(years):
                st.session_state.pop("year_range")
        year_range = st.slider("Khoảng năm", min(years), max(years), (min(years), max(years)), key="year_range")
        available_years = list(range(year_range[0], year_range[1] + 1))
        old_year = st.session_state.get("kpi_year")
        if old_year is not None and old_year not in available_years:
            st.session_state.pop("kpi_year")
        complete_years = snapshot.coverage.loc[snapshot.coverage["Du_hai_luong"] & snapshot.coverage["Year"].between(*year_range), "Year"].tolist()
        default_year = max(complete_years) if complete_years else max(available_years)
        kpi_year = st.selectbox("Năm cho KPI", available_years, index=available_years.index(default_year), key="kpi_year")
        # Dùng coverage để giữ năm/luồng thiếu trên biểu đồ; không điền thành 0.
        trade = snapshot.coverage[["Year"]].merge(snapshot.trade, on="Year", how="left")
        trade["HS_Version_Changed"] = trade["HS_Version_Changed"].eq(True)
        selected_trade = trade.loc[trade["Year"].between(*year_range)].copy()
        st.session_state["selected_trade"] = selected_trade
        row = trade.loc[trade["Year"].eq(kpi_year)].iloc[0]
        m1, m2, m3 = st.columns(3)
        for container, label, column in [(m1, "Xuất khẩu (tỷ USD)", "Export_USD"), (m2, "Nhập khẩu (tỷ USD)", "Import_USD"), (m3, "Xuất − nhập (tỷ USD)", "Trade_Balance_USD")]:
            container.metric(label, f"{row[column] / 1e9:,.2f}" if pd.notna(row[column]) else "Chưa có dữ liệu")
        missing_years = snapshot.coverage.loc[snapshot.coverage["Year"].between(*year_range) & ~snapshot.coverage["Du_hai_luong"], "Year"].tolist()
        if missing_years:
            st.info(f"Các năm chưa đủ hai luồng: {', '.join(map(str, missing_years))}. Dữ liệu thiếu được giữ trống.")
        receipts = snapshot.receipts
        st.caption(f"Thời điểm lấy dữ liệu API gần nhất: {receipts['retrieved_at'].max()} · Lần lấy cũ nhất trong bộ đang dùng: {receipts['retrieved_at'].min()}")
        lines, balance = trade_charts(selected_trade)
        st.plotly_chart(lines, width="stretch", key="trade_lines")
        st.plotly_chart(balance, width="stretch", key="trade_balance")
        st.warning("Chuỗi H4/H5/H6 chưa quy đổi về cùng phiên bản HS. Trị giá danh nghĩa không phải khối lượng; số liệu thương mại cung cấp bối cảnh riêng, không giải thích nguyên nhân lỗi trong UCI.")
        st.dataframe(selected_trade, width="stretch", hide_index=True)
        st.download_button("Tải CSV thương mại đang chọn", selected_trade.to_csv(index=False).encode("utf-8-sig"),
                           "thuong_mai_dang_chon.csv", "text/csv", key="download_trade")

    with quality_tab:
        st.subheader("Chất lượng toàn bộ nguồn lỗi thép")
        quality = snapshot.quality
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Dòng đầu vào", f"{quality['input_rows']:,}")
        c2.metric("Dòng sau làm sạch", f"{quality['clean_rows']:,}")
        c3.metric("Dòng trùng đã loại", str(quality["duplicates_removed"]))
        c4.metric("Ô thiếu khôi phục / giá trị sửa", f"{quality['missing_restored']} / {quality['numeric_corrected']}")
        st.success(f"Đối chiếu: {quality['feature_mismatches']} ô đặc trưng lệch UCI sau xử lý; {quality['unmatched_rows']} dòng chưa ghép; nhãn khớp UCI.")
        st.caption(f"Excel {quality['input_rows']:,} × {quality['input_columns']} cột; giữ {quality['area_flags_retained']} bản ghi gắn cờ diện tích. Bao phủ {quality['reference_coverage_percent']:.2f}% bản ghi UCI.")
        st.dataframe(snapshot.sources, width="stretch", hide_index=True)
        with st.expander("Trạng thái và nguồn từng truy vấn API"):
            st.dataframe(snapshot.receipts, width="stretch", hide_index=True)
        st.subheader("Dữ liệu lỗi theo bộ lọc hiện tại")
        st.caption(f"{len(selected):,} / {len(snapshot.faults):,} bản ghi. Production_Date là biến mô phỏng.")
        st.dataframe(selected.assign(Production_Date=selected["Production_Date"].map(str)), width="stretch", hide_index=True)
        st.download_button("Tải CSV lỗi đang chọn", selected.to_csv(index=False).encode("utf-8-sig"),
                           "loi_thep_dang_chon.csv", "text/csv", key="download_faults")
        with st.expander("Chi tiết kết quả làm sạch"):
            st.json(quality)


live_dashboard()
