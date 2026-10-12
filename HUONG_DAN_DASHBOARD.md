# Dashboard bước 6: lỗi bề mặt thép

Tại thư mục dự án, chạy:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py --server.address 127.0.0.1 --browser.gatherUsageStats false
```

Mở địa chỉ được in trong terminal, thường là `http://localhost:8501`.
Nhấn `Ctrl+C` trong terminal để dừng. Nếu cổng đã được dùng, thêm `--server.port 8502`.

## Ba tab

**Phân tích lỗi thép:** lọc dòng thép, loại lỗi và khoảng độ dày; đặt lại bộ lọc;
4 KPI gồm số bản ghi, số nhãn, trung vị diện tích và trung vị độ dày.
7 biểu đồ Plotly tương ứng Hình 1–7 trong notebook, có thể rê chuột, phóng to
và bật/tắt nhóm trong chú giải. KPI, bảng hỗ trợ và biểu đồ cùng dùng tập đang lọc.
Không chọn nhãn/dòng thép nào có nghĩa là tập rỗng; giao diện hiển thị thông báo.

**Bối cảnh ngành:** chọn khoảng năm và một năm cho KPI; mặc định KPI là năm gần nhất
có đủ hai luồng. Hai biểu đồ xuất nhập khẩu và chênh lệch dùng cùng phạm vi năm.
Năm 2024 được giữ trong bảng bao phủ, hiện thiếu cả hai luồng, không vẽ thành số 0.
Bộ lọc lỗi thép không ảnh hưởng đến tab thương mại. CSV tải xuống giữ USD gốc;
biểu đồ/KPI hiển thị tỷ USD. Chuỗi H4/H5/H6 chưa quy đổi chung.

**Dữ liệu và chất lượng:** quy mô nguồn, số dòng trùng, ô thiếu khôi phục, giá trị sửa,
đối chiếu UCI, cờ diện tích giữ lại, mã băm nguồn và thời điểm lấy từng truy vấn.
Bảng lỗi hiển thị và CSV tải xuống phản ánh bộ lọc hiện tại. Chỉ cột ngày gốc trong
bảng giao diện được chuyển sang chuỗi để hiển thị các cách biểu diễn hỗn hợp.

## Làm mới dữ liệu

- **Làm mới dữ liệu:** đọc lại Excel, UCI CSV và bộ JSON thương mại từ ổ đĩa,
  chạy làm sạch, kiểm tra, tạo biến và tổng hợp. Không chỉ vẽ lại biểu đồ cũ.
- **Tự đọc lại mỗi 5 phút:** mặc định bật; hoạt động khi phiên dashboard còn mở.
  Thay đổi bộ lọc tính lại kết quả trong bản đang dùng, không gọi API mỗi lần bấm.
- **Gọi lại UN Comtrade khi làm mới:** mặc định tắt để chạy được không có mạng.
  Bật tùy chọn rồi bấm làm mới để lấy lại 20 truy vấn cho 2015–2024 và hai luồng X/M.
  Có thời gian chờ giữa truy vấn và thử lại một lần khi gặp HTTP 429.
- Khi tự động gọi API, dùng cache 15 phút; bấm nút làm mới xóa cache API để gọi trực tiếp.
- Kiểm tra đủ trạng thái truy vấn, phạm vi, giá trị và phiên bản HS trước khi chấp nhận.
  Một luồng thiếu vẫn giữ luồng còn lại; chênh lệch chưa xác định khi thiếu một luồng.
- Nếu nguồn/API lỗi, giữ bản hợp lệ gần nhất và ghi rõ thời điểm của bản đó.
  Khởi động lại vẫn có thể đọc bản hợp lệ lưu trên ổ đĩa nếu nguồn hiện tại lỗi.

`outputs/buoc_6/runtime/last_valid_snapshot.json` lưu bản hợp lệ gần nhất.
`outputs/buoc_6/runtime/comtrade_accepted.json` chỉ được tạo sau khi bộ API mới qua kiểm tra.
Các tệp trong `data/raw/` và kết quả notebook bước 1–5 được giữ nguyên.
Khi thay file thực hành hợp lệ ở `data/raw/practice/data_chua_sach_ko_sua.xlsx`,
giữ sheet `Faults (2)` và cấu trúc nguồn. Khóa tọa độ phải ghép được một–một với UCI;
nhãn/ngày ngoài quy tắc sẽ bị từ chối. Nếu dùng tập con, dashboard ghi tỷ lệ bao phủ UCI.
UCI là dữ liệu tĩnh; làm mới không tự tạo thêm vết lỗi mới.

## Mã nguồn và notebook

| Tệp | Chức năng |
|---|---|
| `app.py` | Bố cục, bộ lọc, cache API, làm mới, trạng thái phiên và tải CSV |
| `steel_analysis.py` | Đọc nguồn, làm sạch, kiểm tra, tạo biến, lọc và tổng hợp dùng chung |
| `dashboard_charts.py` | 9 biểu đồ Plotly, màu nhãn và công thức boxplot |
| `buoc_1_2_3_4_5_6_loi_be_mat_thep.ipynb` | Toàn bộ 6 bước, thuyết minh dashboard và đối chiếu hàm chung |
| `tests/test_dashboard.py` | 11 kiểm thử pipeline và ứng dụng |

Chương 3–5 giữ cách trình bày từng thao tác đã thống nhất. Chương 6 gọi trực tiếp
module dùng chung với dashboard rồi đối chiếu bảng lỗi, thương mại và tổng hợp.
Đối chiếu notebook sử dụng JSON gốc để so sánh đúng cùng đầu vào; API mới trên
dashboard được lưu riêng, vì vậy số liệu sau một lần gọi mới có thể khác báo cáo tĩnh.

## Kiểm tra lại

```powershell
python -m unittest discover -s tests -v
```

Bộ kiểm thử kiểm tra mở ứng dụng, 3 tab/9 biểu đồ, bộ lọc A300/A400/nhãn/độ dày,
đặt lại bộ lọc, tập rỗng, năm thiếu, tải CSV, API lỗi giữ bản cũ, năm thiếu/mẫu số 0,
đọc lại file thay đổi và đối chiếu notebook. Lỗi API được mô phỏng để không phụ thuộc mạng.
Kiểm tra chu kỳ tự động mô phỏng thời gian đã trôi qua và xác nhận hàm đọc nguồn được gọi.
Không sửa file gốc trong kiểm thử; thao tác thay file diễn ra trên bản sao tạm.

Kết quả lần kiểm tra bàn giao nằm ở `outputs/buoc_6/test_results.json`.

## Ảnh giao diện để đưa vào báo cáo

Mở dashboard, giữ bộ lọc mặc định và chụp riêng ba tab để minh họa Chương 6.
Thêm một ảnh chọn A300 để minh họa KPI và biểu đồ thay đổi đồng bộ.
Trong phiên thực hiện này, công cụ trình duyệt và kết nối điều khiển máy tính
không khả dụng nên chưa có ảnh chụp giao diện thực tế. Ứng dụng đã được kiểm tra
bằng Streamlit AppTest và kiểm tra HTTP; chưa kiểm tra bố cục qua trình duyệt.

Tài liệu kỹ thuật: [Streamlit fragment](https://docs.streamlit.io/develop/api-reference/execution-flow/st.fragment),
[Streamlit AppTest](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest),
[Plotly box plots](https://plotly.com/python/box-plots/).
