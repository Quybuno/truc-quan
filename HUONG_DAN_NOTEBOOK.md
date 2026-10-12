# Notebook dữ liệu lỗi bề mặt thép

Chỉ sử dụng `buoc_1_2_3_4_5_6_loi_be_mat_thep.ipynb` — notebook cuối cùng chứa toàn bộ sáu bước.
Bản này đã gộp bước 1 và 5 được cập nhật, tiêu chí Q0–Q6, mức độ chắc chắn A/B/C,
kế hoạch kiểm chứng, các cell đã sắp xếp lại và chương dashboard với đối chiếu hàm xử lý dùng chung.
Notebook đã kèm kết quả chạy. Chọn Python 3 và **Run All** để chạy lại từ thư mục dự án.
Các notebook trung gian bước 1–2, 1–3, 1–4 và 1–5 đã được xóa.

Nếu cần cài môi trường:

```powershell
python -m pip install -r requirements.txt
python -m notebook
```

Chạy notebook từ thư mục chứa file `.ipynb` để các đường dẫn tương đối trỏ đúng dữ liệu.
Ở bước 2, CSV/Excel đã tải chỉ trình bày nguồn, vị trí file, quy mô và mục đích; không có mã tải/đọc file.
Mã API chia thành từng ô ngắn: tham số, gửi GET, đọc JSON, tạo bảng và lưu kết quả.
Mặc định `GOI_LAI_API = False` dùng JSON API đã thu thập, giúp chạy lại khi không có mạng.
Đặt `GOI_LAI_API = True` trong phần API để gọi lại UCI và UN Comtrade.
Kết quả phần API đơn giản được lưu riêng trong `outputs/buoc_1_2/api_don_gian/`;
xem `trang_thai_truy_van.csv` để phân biệt kết quả rỗng, lỗi và trường hợp cần kiểm tra.

- `data/raw/`: Excel thực hành, CSV/metadata biến UCI, danh sách tên nhãn gốc và JSON UN Comtrade.
- `outputs/buoc_1_2/`: hồ sơ nguồn, câu hỏi, cấu trúc dữ liệu, mã băm và minh chứng lần thu thập trước.
- `outputs/buoc_1_2/api_don_gian/`: JSON, bảng API và nhật ký của phiên bản mã đơn giản hiện tại.
- `data/clean/loi_thep_sach.csv`: 1.941 bản ghi lỗi đã làm sạch, có dòng nguồn và cờ diện tích lớn.
- `data/clean/thuong_mai_theo_nam_sach.csv`: 9 năm 2015–2023, xuất và nhập khẩu thành hai cột.
- `outputs/buoc_3/thuong_mai_dang_dai.csv`: bảng thương mại dạng dài hỗ trợ truy vết, giữ các trường nguồn.
- `outputs/buoc_3/`: nhật ký thay đổi, dòng trùng bị loại và dòng giữ lại, đối chiếu UCI,
  kiểm tra logic/công thức, bảng trước/sau, từ điển dữ liệu và ghi chú phiên bản HS.
- `data/analysis/loi_thep_phan_tich.csv`: 1.941 bản ghi, bổ sung dòng thép, kích thước
  khung bao, khoảng độ sáng và logarit diện tích.
- `data/analysis/thuong_mai_phan_tich.csv`: trị giá xuất nhập khẩu, chênh lệch,
  thay đổi tuyệt đối, tăng trưởng và cờ thay đổi phiên bản HS.
- `outputs/buoc_4/`: bốn nhóm bảng tổng hợp, từ điển biến/chỉ số và kết quả kiểm tra.
- `outputs/buoc_5/hinh/`: 9 biểu đồ, mỗi hình có PNG 300 dpi và SVG để đưa vào tiểu luận.
- `outputs/buoc_5/`: bảng số liệu hỗ trợ Q0–Q6, tiêu chí, nhận định A/B/C,
  kế hoạch kiểm chứng, danh mục hình, nhận xét và kết quả kiểm tra.
- `outputs/buoc_5/nhan_xet_chuong_5.md`: nhận xét từng hình theo quan sát, số liệu,
  ý nghĩa và giới hạn diễn giải.
- `outputs/buoc_6/`: bảng đối chiếu notebook/dashboard, KPI theo bộ lọc và kết quả kiểm thử.
- `outputs/buoc_1_2/metadata_nguon/`: thời điểm tải, URL và mã băm; nằm riêng với dữ liệu đầu vào.
- `outputs/buoc_6/runtime/`: bản hợp lệ gần nhất và bộ API mới đã được dashboard chấp nhận.

File thực hành công khai hiện có sheet `Faults (2)`; mã đọc đã ghi nhận sự khác biệt
với tên `Faults` trong PDF. UCI CSV dùng `K_Scratch`, gói gốc dùng `K_Scatch`;
notebook giữ nguyên tên theo từng nguồn và xuất bảng ghi chú để đối chiếu ở bước 3.
UN Comtrade đã thu được 18 bản ghi cho 2015–2023; hai truy vấn 2024 trả kết quả rỗng.
Phạm vi phân tích thương mại chốt là 2015–2023; JSON 2024 vẫn được giữ làm bằng chứng,
không thay dữ liệu thiếu bằng 0.
`Production_Date` là biến mô phỏng. Không dùng số liệu UN Comtrade để suy luận
nguyên nhân lỗi trong UCI.

Trong bước 3, mã đọc Excel/CSV, chuẩn hóa nhãn, loại 20 dòng trùng, ghép UCI một–một,
khôi phục 67 ô thiếu và sửa 16 giá trị khác nguồn. Có 395 dòng diện tích lớn được gắn cờ
IQR và giữ lại. Ngày mô phỏng được chuẩn hóa theo lịch tháng 11/2025 trong PDF.

Khi phân tích lỗi, dùng `Fault_Type_Clean`; `Faults` là nhãn gốc để truy vết.
`Production_Date_Clean` là ngày mô phỏng chuẩn hóa; `Production_Date` giữ giá trị gốc.
Hai cột ngày không được dùng để suy luận xu hướng sản xuất thực tế.
Các đặc trưng UCI chưa công bố đơn vị vẫn để nguyên, không tự gắn đơn vị vật lý.

UN Comtrade có các phiên bản HS H4, H5, H6, được giữ trong bảng sạch và kiểm kê theo năm.
Chuỗi thương mại chưa được quy đổi về một phiên bản chung; cần giữ ghi chú này khi so sánh.

Trong bước 4, tạo `Steel_Type`, `X_Range`, `Y_Range`, `Luminosity_Range` và
`Log_Pixels_Areas`; kiểm tra và dùng lại nhãn sạch cùng cờ ngoại lai ở bước 3.
Bốn nhóm bảng gồm cơ cấu lỗi, lỗi theo dòng thép, thống kê đặc trưng theo nhãn
và thương mại theo năm. Tỷ trọng theo dòng thép và theo nhãn có hai mẫu số riêng,
được ghi rõ trong notebook và từ điển chỉ số.

Tăng trưởng chưa xác định khi thiếu năm trước hoặc giá trị năm trước bằng 0.
Năm thiếu giữa chuỗi được giữ là dữ liệu thiếu. Không làm tròn số trước khi tổng hợp.
Các năm đổi phiên bản HS được đánh dấu để hỗ trợ diễn giải so sánh.

Trong bước 5, Matplotlib vẽ 9 hình theo kế hoạch: cơ cấu lỗi, Pareto, số lượng theo
dòng thép, cột chồng 100%, scatter độ sáng, boxplot độ dày, boxplot diện tích,
đường xuất nhập khẩu và cột chênh lệch thương mại. Hình hiển thị trong notebook và được lưu riêng.
Các nhãn lỗi giữ màu nhất quán; hình số lượng theo dòng thép phân biệt A300/A400 bằng họa tiết.

Bảng hỗ trợ có tương quan Pearson toàn tập/theo nhãn, trung vị và tứ phân vị,
độ dày tách theo nhãn và dòng thép cùng cỡ mẫu. Nhóm N=1 được ghi chú riêng.
Boxplot diện tích tính từ dữ liệu gốc rồi chuyển trục hiển thị sang log cơ số 10.
Điểm ngoài râu của từng nhãn khác với cờ IQR toàn tập ở bước 3; mọi bản ghi được giữ.
`Group_Flier_Count` trong bảng hỗ trợ Hình 7 đếm theo từng nhãn: tổng 209;
riêng K_Scatch có 6 điểm ngoài râu, so với 326 cờ theo hàng rào toàn tập.
Bảy biểu đồ lỗi dùng chữ 13–14 pt và bỏ tiêu đề, nguồn trong ảnh để phù hợp
caption tự đánh số của báo cáo. Notebook đã chạy lại đủ 113 ô mã, không có output lỗi.
Biểu đồ thương mại hiển thị tỷ USD, CSV giữ USD; không suy diễn trị giá danh nghĩa thành khối lượng.

Trong bước 6, notebook gọi module xử lý dùng chung với dashboard và kiểm tra
bảng lỗi, thương mại, cơ cấu, hai mẫu số tỷ trọng và thống kê đặc trưng khớp bước 3–5.
Đối chiếu dùng JSON gốc; dashboard có thể có bộ API mới lưu riêng trong `outputs/buoc_6/runtime/`.

Chạy dashboard từ terminal trong thư mục dự án:

```powershell
python -m streamlit run app.py --server.address 127.0.0.1 --browser.gatherUsageStats false
```

Ứng dụng có ba tab, bộ lọc, 4 KPI lỗi, 3 KPI thương mại, 9 biểu đồ tương tác,
tải CSV và đọc lại nguồn bằng nút làm mới/chu kỳ 5 phút. Mặc định chạy với dữ liệu đã lưu;
gọi API là tùy chọn. Nếu nguồn lỗi, giữ bản hợp lệ gần nhất.
Xem `HUONG_DAN_DASHBOARD.md` để biết cách vận hành và kiểm thử.

Ảnh chụp giao diện thật ở phạm vi A400 + K_Scatch được dùng tại Hình 4.8:
`latex/figures/chuong4/dashboard_a400_kscatch.png`. Ảnh thể hiện bộ lọc và bốn
KPI 390; 1; 6.281,5; 40,0; hồ sơ chụp ở `outputs/minh_hoa_chuong4/dashboard_capture.json`.
Kết quả chạy lại 11 kiểm thử dashboard và log nằm trong `outputs/buoc_6/`.
