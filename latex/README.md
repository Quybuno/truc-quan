# Mã LaTeX tiểu luận

## Nội dung hiện tại

Bản hiện tại bắt đầu từ mục lục, gồm phần mở đầu và bốn chương, kèm tài liệu tham khảo đã sử dụng:

- `main.tex`: tệp chính để biên dịch.
- `phan-dau/danh-muc.tex`: mục lục, danh mục hình vẽ và danh mục bảng biểu tự động.
- `phan-dau/thuat-ngu.tex`: thuật ngữ và từ viết tắt.
- `phan-dau/mo-dau.tex`: bối cảnh, mục tiêu, phạm vi, Q0–Q5, giá trị và bố cục báo cáo.
- `chuong/chuong1.tex`: Tổng quan bài toán và cơ sở lý thuyết.
- `chuong/chuong2.tex`: Khảo sát dữ liệu, công cụ và yêu cầu thực hiện.
- `chuong/chuong3.tex`: Xây dựng quy trình xử lý và trực quan hóa bằng Python; các đoạn mã minh họa cốt lõi và hình trích bảng dữ liệu tại từng giai đoạn.
- `chuong/chuong4.tex`: Kết quả Q0–Q5 theo mạch kể chuyện từ dữ liệu: cơ cấu nhãn → dòng thép → độ sáng → độ dày → diện tích → đối chiếu bằng dashboard; kèm kiểm thử chức năng và thảo luận giới hạn. Mỗi biểu đồ có thông điệp chính, số liệu làm căn cứ và đoạn nối sang góc nhìn tiếp theo.
- `figures/chuong3/`: sáu ảnh chụp cell Python và đầu ra Pandas trên VS Code nền tối, cùng ba biểu đồ minh họa (Pareto, scatter độ sáng, boxplot diện tích trục log). Giữ nguyên thư mục này khi sao chép hoặc tải lên Overleaf.
- Chương 4 sử dụng **bảy biểu đồ đã hiển thị trong notebook chính**: cơ cấu nhãn, Pareto, số lượng theo dòng thép, cơ cấu trong dòng thép, scatter độ sáng, boxplot độ dày và boxplot diện tích. Ảnh `figures/chuong4/notebook_*.png` được trích nguyên từ output PNG đã lưu; mỗi hình dẫn tên mục và mã hình notebook để đối chiếu. Hình 4.8 chụp dashboard Streamlit thật ở phạm vi A400 + K_Scatch.
- `tailieu-thamkhao.tex`: các nguồn đã dẫn trong nội dung.

Phần đầu dùng số trang La Mã; Chương 1 bắt đầu lại từ trang 1. Mục lục chỉ liệt kê phần đã viết. Bố cục của toàn báo cáo gồm bốn chương được giới thiệu trong phần mở đầu. Bìa và thông tin sinh viên/giảng viên bổ sung theo mẫu môn học khi có thông tin chính xác.

## Biên dịch

Chọn **XeLaTeX** trên Overleaf hoặc trình soạn thảo LaTeX. Tải nguyên thư mục này lên Overleaf, chọn `main.tex` làm tệp chính. Bản local dùng Times New Roman khi máy có phông; môi trường không có phông này tự dùng TeX Gyre Termes.

Chạy tại thư mục `latex`:

```powershell
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

Hoặc, nếu có Tectonic:

```powershell
tectonic --synctex main.tex
```

Tectonic tự chạy lại để cập nhật mục lục, danh mục và trích dẫn. Với XeLaTeX, chạy lại đến khi không còn thông báo cần cập nhật tham chiếu, thường 2–3 lần cho bản mới.

Trong workspace hiện tại, có thể chạy tại thư mục `latex` bằng bộ Tectonic đã chuẩn bị:

```powershell
$env:TECTONIC_CACHE_DIR = (Resolve-Path '..\tmp\latex-tools\tectonic-cache').Path
& '..\tmp\latex-tools\tectonic.exe' --synctex main.tex
```

Không cần BibTeX/Biber; danh mục tham khảo dùng `thebibliography`. Mọi tệp nguồn lưu UTF-8. Các tệp thành phần có chỉ dẫn `% !TeX root` về `main.tex`. Trong VS Code dùng LaTeX Workshop, chọn recipe XeLaTeX hoặc Tectonic phù hợp với trình biên dịch đã cài; tệp chính luôn là `main.tex`.

## Biên dịch ngay trong VS Code tại workspace hiện tại

Cấu hình `.vscode/settings.json` của thư mục `Baocao` đã có recipe Tectonic dùng bộ công cụ local. Tiện ích LaTeX Workshop đã có trên máy hiện tại.

1. Mở cả thư mục `Baocao` bằng **File → Open Folder** để VS Code nhận cấu hình workspace.
2. Mở `latex/main.tex`.
3. Nhấn **Ctrl+Alt+B** để build; **Ctrl+Alt+V** để xem PDF trong VS Code.
4. Những lần sau, lưu tệp `.tex` bằng **Ctrl+S** để tự build lại. PDF của recipe nằm ở `latex/build/main.pdf`.

Các phím tắt và cơ chế recipe được mô tả trong [tài liệu chính thức LaTeX Workshop](https://github.com/James-Yu/LaTeX-Workshop/wiki/Compile). Cấu hình trên dành cho cây thư mục workspace hiện tại, nơi có `tmp/latex-tools/tectonic.exe`; khi chuyển mã nguồn sang máy khác, dùng XeLaTeX hoặc Tectonic đã cài tại máy đó theo hướng dẫn bên trên.

## Nội dung và bằng chứng

Phần mở đầu là tệp riêng; Chương 2 trình bày tình trạng và yêu cầu, Chương 3 trình bày cách thực hiện, Chương 4 tập trung đọc kết quả. Số chương, mục và hình/bảng được đánh tự động. Khi bổ sung kết luận hoặc phụ lục riêng, đặt các lệnh nhập tệp tương ứng theo mẫu môn học; không đưa tiêu đề chưa viết vào mục lục.

Các khối Python trong Chương 3 là đoạn trích để giải thích thao tác; không thay thế toàn bộ notebook hay các hàm kiểm tra và ghi nhật ký. Sáu hình dữ liệu là ảnh chụp giao diện VS Code của notebook minh chứng đã thực thi, giữ cả lệnh `display(...)` và đầu ra Pandas. Các bảng chọn một số dòng và cột từ dữ liệu thực tế; hình kiểm tra nội tại là lượt bổ sung trước khôi phục theo UCI. Ảnh chỉ được cắt theo vùng cell, không vẽ lại bảng hoặc sửa giá trị hiển thị.

Trong workspace, notebook đã thực thi, các CSV đối chiếu và hồ sơ nguồn nằm tại `outputs/minh_hoa_chuong3`. `tao_notebook_minh_chung.py` tạo và thực thi notebook minh chứng; sau khi mở và chụp các cell trên VS Code, `cat_anh_cell.py` cắt các ảnh gốc theo vùng ghi trong `captures/manifest.json`. Script `tao_hinh_du_lieu.py` chỉ lưu bảng minh họa cũ vào thư mục riêng, không ghi đè ảnh cell hiện tại. Biên dịch LaTeX chỉ cần các ảnh PNG đã kèm trong thư mục `figures/chuong3`.

Ảnh Chương 4 được trích bằng `outputs/minh_hoa_chuong4/xuat_hinh_tu_notebook.py` từ `buoc_1_2_3_4_5_6_loi_be_mat_thep.ipynb`. Script chỉ đọc notebook và giải mã các output PNG; `outputs/minh_hoa_chuong4/notebook_bieu_do.json` ghi tên mục, tên hình, số ô từ 1, cell ID, execution count, kích thước và SHA256 từng ảnh. Notebook đã chạy lại toàn bộ 113 ô mã; bảy hình phân tích bỏ tiêu đề và nguồn trong ảnh, dùng chữ 13–14 pt. Bảng diện tích có `Group_Flier_Count` tổng 209 và cờ toàn tập tổng 395. Bản chương có bảy biểu đồ cùng một ảnh chụp dashboard thật, không có khung chờ hình. Minh chứng ảnh dashboard nằm ở `outputs/minh_hoa_chuong4/dashboard_capture.json`.

Kết quả kiểm thử dashboard trong `outputs/buoc_6/test_results.json` ghi 11 ca đạt ở lần chạy lại ngày 12/10/2026. Ca bộ lọc kiểm tra thêm bốn KPI A400 + K_Scatch và cảnh báo session state. API, thời gian và lỗi nguồn được mô phỏng; thao tác thay nguồn thực hiện trên bản sao riêng.

Thiết lập hiện tại: A4, chữ thân bài 13 pt, giãn dòng 1,25, lề trái 3 cm/phải 2 cm/trên dưới 2,5 cm. Đây là thiết lập trình bày ban đầu; có thể điều chỉnh theo mẫu chính thức của môn học.
