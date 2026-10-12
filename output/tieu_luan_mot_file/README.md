# Bản LaTeX gộp bốn chương

`tieu_luan.tex` là tệp LaTeX duy nhất, chứa phần đầu, mở đầu, bốn chương và tài liệu tham khảo. Nội dung các chương được giữ nguyên. Không cần các tệp chương riêng hoặc tệp thư mục tài liệu tham khảo.

## Biên dịch

Giải nén toàn bộ gói ZIP vào cùng một thư mục. Giữ thư mục `figures` cạnh `tieu_luan.tex`.

- Trên Overleaf: tải toàn bộ gói lên, chọn `tieu_luan.tex` làm Main document và chọn XeLaTeX làm Compiler.
- Trên VS Code với LaTeX Workshop: mở `tieu_luan.tex` và chọn recipe XeLaTeX. Biên dịch lại nếu mục lục hoặc tham chiếu chưa được cập nhật.
- Nếu dùng Tectonic: chạy `tectonic --synctex tieu_luan.tex` tại thư mục vừa giải nén.

Mã dùng tiếng Việt UTF-8. Khi máy có Times New Roman, bản gộp dùng phông này; nếu không có, mã tự chọn TeX Gyre Termes.

## Ảnh đi kèm

`figures/chuong3/` gồm sáu ảnh cell Python/Pandas và ba biểu đồ đã chèn vào bài. Các biểu đồ có thêm bản SVG để chỉnh sửa hoặc xuất lại.

Chương 4 vẫn giữ tám khung ghi chú để người viết tự thêm ảnh. Sáu biểu đồ kết quả đã được chuẩn bị trong `figures/chuong4/`, mỗi biểu đồ có PNG và SVG:

| Vị trí | Ảnh PNG tương ứng |
|---|---|
| Hình 4.1 – Cơ cấu bảy nhãn | `figures/chuong4/01_co_cau_loi.png` |
| Hình 4.2 – Số lượng theo dòng thép | `figures/chuong4/02_loi_theo_thep_so_luong.png` |
| Hình 4.3 – Cơ cấu trong từng dòng thép | `figures/chuong4/03_co_cau_trong_dong_thep.png` |
| Hình 4.4 – IQR độ sáng tối thiểu | `figures/chuong4/04_iqr_do_sang_toi_thieu.png` |
| Hình 4.5 – Độ dày theo nhãn và dòng thép | `figures/chuong4/05_do_day_theo_nhan_va_thep.png` |
| Hình 4.6 – IQR diện tích | `figures/chuong4/06_iqr_dien_tich.png` |

Để chèn một ảnh, thay riêng lệnh `\ghiChuHinh{...}` tại đúng vị trí bằng lệnh sau, giữ nguyên `\captionof{figure}{...}` và `\label{...}` ngay bên dưới:

```latex
\includegraphics[width=\linewidth]{figures/chuong4/01_co_cau_loi.png}
```

Thay đường dẫn bằng ảnh tương ứng. Hai vị trí Hình 4.7 và Hình 4.8 dành cho ảnh dashboard do người viết tự chụp; gói này chưa có hai ảnh đó.

Các thư mục `data/...` và `outputs/...` được nhắc trong nội dung chỉ mô tả quy trình thực hành, không phải tài nguyên cần có để biên dịch báo cáo.
