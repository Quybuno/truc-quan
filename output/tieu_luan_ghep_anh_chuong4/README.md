# Báo cáo đã ghép ảnh Chương 4

`tieu_luan.tex` là bản gộp gồm phần đầu, bốn chương và tài liệu tham khảo.
`chuong4.tex` là phần chương riêng để thay vào dự án LaTeX hiện có.
Giữ thư mục `figures` cạnh tệp chính; biên dịch bằng XeLaTeX hoặc Tectonic.

Đã chèn đúng vị trí tám biểu đồ của bản Chương 4 được gửi: Pareto, số lượng theo
dòng thép, cơ cấu trong dòng thép, scatter độ sáng, IQR độ sáng, độ dày theo dòng
thép, boxplot diện tích và cơ cấu trước/sau giả định xóa cờ ngoại lai.
Các hình PNG có độ phân giải 300 dpi; SVG đi kèm cho phép chỉnh sửa.

Hai vị trí Hình 4.9 và 4.10 còn chờ ảnh dashboard thật. Công cụ điều khiển trình
duyệt bị dừng vì không xác định được URL hiện tại đủ chắc chắn. Không dùng giao
diện dựng lại để thay cho ảnh chụp thực tế.

Khi có ảnh, lưu tại `figures/chuong4/ch4_09_dashboard_toan_bo.png` và
`figures/chuong4/ch4_10_dashboard_a400_kscatch.png`, rồi thay từng lệnh
`\ghiChuHinh{...}` tương ứng bằng `\includegraphics[width=\linewidth]{...}`.
Giữ nguyên caption và label. Chương đã giữ đủ 10 vị trí hình và các tham chiếu.
