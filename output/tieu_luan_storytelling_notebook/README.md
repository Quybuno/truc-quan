# Chương 4 theo hướng data storytelling

`tieu_luan.tex` là bản gộp toàn bộ báo cáo, với Chương 4 đã được viết lại.
`chuong4.tex` là bản chương riêng để thay vào cây thư mục LaTeX hiện có.
Giữ thư mục `figures` cạnh tệp chính. Biên dịch bằng XeLaTeX hoặc Tectonic.

Chương 4 sử dụng bảy biểu đồ lỗi thép thực sự hiển thị trong output đã lưu
của notebook. Các ảnh được giải mã trực tiếp, không vẽ lại ở một script ngoài.
Mỗi hình dẫn tên mục và mã hình notebook; JSON đối chiếu ghi thêm số ô,
execution count, cell ID và mã băm. Notebook đã chạy được kèm trong gói để
đọc mã và output; chạy lại từ thư mục dự án có đầy đủ dữ liệu.
Thư mục `minh_chung` kèm audit Q0, bảng ngoài râu Q5 và kết quả kiểm thử.

Hình 4.8 chụp giao diện Streamlit thật với A400 + K_Scatch, khoảng độ dày
40–300. Bốn KPI là 390; 1; 6.281,5; 40,0. Ảnh chỉ cắt vùng giao diện cần
đọc, không dựng lại nội dung. Thông tin chụp được lưu trong JSON minh chứng.

Mạch phân tích đi từ chất lượng dữ liệu đến cơ cấu nhãn, dòng thép, độ sáng,
độ dày, diện tích và hàm ý kiểm chứng tiếp theo. Các bảng làm rõ số liệu cần đọc
cùng biểu đồ. Q0 phân biệt rà soát nội tại bổ sung trước khôi phục với kiểm
tra sau khôi phục trong notebook; Q5 đưa cả hai cách đếm ngoài râu và cờ IQR.

Các đặc trưng chưa xác nhận đơn vị được trình bày trên thang nguồn. Tỷ trọng
mô tả cơ cấu bản ghi lỗi, chưa phải tỷ lệ sản phẩm lỗi. Thông tin thương mại
không được dùng để giải thích nguyên nhân các bản ghi lỗi.
