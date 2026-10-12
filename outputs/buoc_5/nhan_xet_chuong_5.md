# Nhận xét Chương 5

Nguồn: notebook bước 1–5, số liệu tự tính từ bảng sạch.

## 01_co_cau_loi

**Quan sát:** Other_Faults nhiều nhất, Dirtiness ít nhất.
**Số liệu:** 673 (34.67%) so với
55 (2.83%); cỡ mẫu lớn nhất gấp 12.24 lần nhỏ nhất.
**Ý nghĩa:** dữ liệu mất cân bằng; khi so sánh đặc trưng cần đọc cả cỡ mẫu từng nhãn.
**Giới hạn:** Other_Faults là nhãn gộp; số lượng lớn không chứng minh lỗi nghiêm trọng hơn hoặc gây thiệt hại lớn hơn.

## 02_pareto_loi

**Quan sát:** số bản ghi tập trung ở một số nhãn đầu.
**Số liệu:** Other_Faults, Bumps, K_Scatch có tổng 1,466 bản ghi,
chiếm 75.53%; cần 4 nhãn đầu để lũy kế đạt ít nhất 80%.
**Ý nghĩa:** ưu tiên các nhóm này khi mô tả phần lớn tập dữ liệu, đồng thời giữ các nhãn ít mẫu để tránh bỏ sót.
**Giới hạn:** Pareto mô tả mức tập trung bản ghi; chưa có chi phí hoặc mức hạ cấp để xếp ưu tiên xử lý sản xuất.

## 03_loi_theo_thep_so_luong

**Quan sát:** K_Scatch tập trung trên A400; Z_Scratch tập trung trên A300.
**Số liệu:** K_Scatch có 390/391 bản ghi trên A400
(99.74%); Z_Scratch có 172/190
trên A300 (90.53%). Stains có 98.61% trên A400.
**Trả lời Q2:** các nhãn vượt mốc tập trung 90% của PDF là
K_Scatch, Z_Scratch, Stains.
Mẫu số ở đây là toàn bộ bản ghi của từng nhãn; cần kiểm chứng riêng các tổ hợp nhãn–dòng thép.
**Giới hạn:** A300 có 777, A400 có 1,164 bản ghi lỗi.
Thiếu sản lượng nên chưa kết luận dòng nào dễ lỗi hơn; liên hệ chưa xác định nguyên nhân.

## 04_loi_theo_thep_ty_trong

**Quan sát:** cơ cấu của hai dòng thép khác nhau dù Other_Faults có tỷ trọng gần nhau.
**Số liệu:** trong A300, Bumps chiếm 35.91% và Z_Scratch 22.14%;
trong A400, K_Scatch chiếm 33.51% và Bumps 10.57%.
Other_Faults chiếm lần lượt 34.23% và 34.97%.
**Ý nghĩa:** chuẩn hóa về 100% giúp so sánh cơ cấu khi tổng bản ghi hai dòng khác nhau.
**Giới hạn:** đây là tỷ trọng trong tập lỗi, không phải tỷ lệ lỗi trên tổng sản lượng của A300/A400.

## 05_scatter_do_sang

**Quan sát:** K_Scatch nghiêng về phía Min thấp; các nhóm khác còn chồng lấn ở vùng trung tâm.
**Số liệu:** Pearson toàn tập = 0.4296; trung vị Min của K_Scatch là 41,
trong khi sáu nhãn khác nằm từ 80 đến 115.
IQR Min của K_Scatch là 35–49;
Q1 nhỏ nhất của sáu nhãn khác là 64.
Trung vị Max của Z_Scratch là 124, so với Bumps 127.
**Trả lời Q3:** có dấu hiệu phân tách trung tâm ở Min của K_Scatch, đủ để ưu tiên kiểm chứng
đặc trưng này. Pearson mô tả quan hệ giữa Min và Max, không đo khả năng phân loại nhãn.
**Giới hạn:** IQR chỉ chứa 50% trung tâm; scatter vẫn có điểm chồng lấn.
Chưa có precision/recall hoặc hiệu năng trên tập kiểm tra độc lập.

## 06_boxplot_do_day

**Quan sát:** độ dày K_Scatch tập trung ở mức thấp, Other_Faults phân tán rộng hơn.
**Số liệu:** K_Scatch có trung vị 40,
Q1–Q3 = 40–40,
độ lệch chuẩn mẫu 2.20; Other_Faults có Q1–Q3 =
40–130.
Toàn tập có trung bình 78.74, trung vị 70 và độ lệch chuẩn mẫu 55.09.
Có 1,481/1,941 bản ghi nằm ở độ dày 40–80
(76.30%).
**Trả lời Q4:** phân bố độ dày khác nhau theo nhãn; K_Scatch tập trung hẹp.
Cần đọc tiếp nhãn × dòng thép để chọn tổ hợp cần kiểm chứng.
**Giới hạn:** chưa có sản lượng theo độ dày nên không suy ra tấm mỏng dễ lỗi hơn; số liệu chưa xác nhận đơn vị vật lý.

## 07_boxplot_dien_tich_log

**Quan sát:** diện tích K_Scatch lớn hơn rõ về trung vị; Stains có trung vị nhỏ nhất.
**Số liệu:** trung vị lần lượt 6,281.0 và
16.5; Q1–Q3 của K_Scatch là
3,948.5–10,908.5.
Toàn tập có 395 bản ghi vượt ngưỡng IQR toàn tập, được giữ lại.
**Ý nghĩa:** trục log giúp so sánh những nhóm khác nhau nhiều về quy mô; trung vị ít bị kéo bởi các vết rất lớn.
**Giới hạn:** diện tích lớn không tự chứng minh lỗi gây thiệt hại nặng hơn; cờ toàn tập khác với điểm ngoài râu của từng nhãn.

## 08_xuat_nhap_khau

**Quan sát:** nhập khẩu lớn hơn xuất khẩu trong các năm có dữ liệu; cả hai luồng đạt trị giá cao nhất vào 2021.
**Số liệu:** xuất khẩu cực đại 11.94 tỷ USD (2021),
nhập khẩu cực đại 14.74 tỷ USD (2021).
Năm 2023, xuất khẩu 8.51 tỷ USD
(+3.90% so với năm trước), nhập khẩu
12.43 tỷ USD (-13.28%).
**Ý nghĩa:** cung cấp bối cảnh biến động trị giá thương mại của ngành theo năm.
**Giới hạn:** chưa tách tác động giá, lượng hoặc phiên bản HS; không dùng biến động này giải thích lỗi của dữ liệu UCI.

## 09_chenh_lech_thuong_mai

**Quan sát:** chênh lệch âm trong 9/9 năm có dữ liệu.
**Số liệu:** âm lớn nhất năm 2018: -7.38 tỷ USD;
gần 0 nhất năm 2021: -2.81 tỷ USD.
Năm 2023 là -3.91 tỷ USD,
thay đổi +2.22 tỷ USD so với năm trước.
**Ý nghĩa:** nhập khẩu vượt xuất khẩu trong phạm vi HS 72; mức chênh lệch thay đổi theo năm.
**Giới hạn:** chênh lệch này không phải lợi nhuận ngành hoặc chỉ số chất lượng thép; năm đổi HS cần xem xét phạm vi phân loại.

## Trả lời Q0–Q6

| Cau_hoi | Phat_hien | Bang_chung | Gioi_han | Muc_do_chac_chan |
| --- | --- | --- | --- | --- |
| Q0 | 1,941 bản ghi; 52,407 ô đặc trưng có 0 lệch UCI; nhãn khớp | Kiểm tra hoàn thành bước 3; đối chiếu UCI | Đạt cho phân tích bộ dữ liệu hiện tại; phụ thuộc độ đúng của nguồn và khóa ghép | A — mô tả kiểm chứng được trong mẫu |
| Q1 | Ba nhãn đầu 75.53%; cỡ mẫu lớn nhất/nhỏ nhất=12.24 | Hình 1–2; co_cau_loi | Mất cân bằng trong tập lỗi; chưa xếp hạng thiệt hại | A — mô tả kiểm chứng được trong mẫu |
| Q2 | Vượt mốc 90%: K_Scatch, Z_Scratch, Stains | Hình 3–4; tap_trung_theo_nhan | Tập trung theo dòng thép trong mẫu; thiếu sản lượng và biến vận hành | A — mô tả kiểm chứng được trong mẫu |
| Q3 | Pearson=0.4296; IQR Min tách mọi nhãn khác: K_Scatch | Hình 5; dau_hieu_do_sang | Dấu hiệu ở 50% trung tâm; chưa xác nhận phân loại trên toàn bộ điểm | A — mô tả kiểm chứng được trong mẫu |
| Q4 | K_Scatch: trung vị 40, SD 2.20; 76.30% toàn tập ở 40–80 | Hình 6; do_day_theo_nhan_thep | Đọc kèm dòng thép và N; N=1 không so sánh độ phân tán; chưa có đơn vị | A — mô tả kiểm chứng được trong mẫu |
| Q5 | Trung vị K_Scatch=6,281.0; Stains=16.5 | Hình 7; thong_ke_dien_tich | Khác biệt quy mô trong mẫu; diện tích chưa đo mức thiệt hại | A — mô tả kiểm chứng được trong mẫu |
| Q6 | Xuất−nhập âm 9/9 năm; năm cuối -3.91 tỷ USD | Hình 8–9; thuong_mai_theo_nam | Bối cảnh riêng; trị giá danh nghĩa và phiên bản HS chưa quy đổi | A — mô tả kiểm chứng được trong mẫu |

## Tiêu chí đánh giá

| Cau_hoi | Tieu_chi_danh_gia | Huong_su_dung_ket_qua |
| --- | --- | --- |
| Q0 | Không thiếu đặc trưng; khóa duy nhất; nhãn và 27 biến có 0 ô lệch UCI; logic đạt | Đạt: phân tích; chưa đạt: xử lý và kiểm tra lại trước khi xuất bảng |
| Q1 | Đọc thứ hạng, tỷ trọng ba nhãn đầu, lũy kế 80% và tỷ số cỡ mẫu lớn nhất/nhỏ nhất | Mất cân bằng: giữ cỡ mẫu, kiểm tra nhãn gộp; nếu mô hình hóa sau này dùng F1 từng lớp/macro |
| Q2 | Tập trung khi trên 90% bản ghi của một nhãn nằm ở cùng một dòng thép | Vượt mốc: kiểm chứng riêng tổ hợp nhãn–dòng thép; không vượt: khảo sát cả hai dòng |
| Q3 | IQR của Min không chồng lấn với mọi nhãn khác là dấu hiệu phân tách trung tâm; xem cả scatter và Max | Có dấu hiệu: ưu tiên đặc trưng để kiểm chứng độc lập; còn chồng lấn: cần thêm đặc trưng |
| Q4 | So sánh N, trung vị, IQR, SD theo nhãn và dòng thép; N=1 chỉ mô tả bản ghi | Có tập trung: kiểm tra tổ hợp dòng thép–độ dày; chồng lấn: giữ nhiều chiều khi mô tả |
| Q5 | So sánh trung vị, IQR và điểm cực đoan; trục log chỉ đổi hiển thị; giữ bản ghi khớp nguồn | Khác biệt quy mô: khảo sát kích thước và nhãn; chồng lấn: diện tích đơn lẻ chưa đủ |
| Q6 | Dấu xuất−nhập so với 0; cực trị và tăng trưởng từng năm đủ dữ liệu; đánh dấu đổi HS | Đọc chiều biến động; khi HS thay đổi phải đối chiếu phân loại trước khi giải thích |

## Nhận định khám phá và giới hạn

| Muc | Nhan_dinh_hoac_cau_hoi | Bang_chung_con_thieu |
| --- | --- | --- |
| B | Min thấp có thể hỗ trợ nhận diện K_Scatch | IQR tách chỉ là dấu hiệu; cần tập kiểm tra độc lập và precision/recall |
| B | K_Scatch cần kiểm chứng ở tổ hợp A400–độ dày 40 | Dòng thép và độ dày cùng tập trung; chưa tách được yếu tố nào đi kèm |
| B | Other_Faults có thể chứa những nhóm con khác nhau | Cần ảnh lỗi, định nghĩa QC và kiểm chứng nhóm con trên dữ liệu mới |
| C | Tỷ lệ sản phẩm bị lỗi hoặc dòng thép nào dễ lỗi hơn | Thiếu tổng sản lượng theo dòng thép và độ dày |
| C | Nguyên nhân vật lý hoặc thiết bị gây lỗi | Thiếu mã tấm/cuộn, thiết bị, ca và biến vận hành; cần xác nhận hiện trường |
| C | Loại lỗi gây thiệt hại nghiêm trọng nhất | Thiếu chi phí, mức hạ cấp và định nghĩa mức độ nghiêm trọng |
| C | Xu hướng lỗi theo thời gian sản xuất | Production_Date là ngày mô phỏng |
| C | Độ dày có đơn vị mm; thương mại Việt Nam giải thích lỗi UCI | Nguồn chưa xác nhận đơn vị hoặc quan hệ giữa hai tập dữ liệu |

## Kế hoạch kiểm chứng

| Giai_doan | Cau_hoi_lien_quan | Viec_can_lam | Du_lieu_can_bo_sung | Dieu_kien_hoan_tat |
| --- | --- | --- | --- | --- |
| 1 — nền dữ liệu (0–30 ngày) | Q0, Q1–Q5 | Lưu hồ sơ nguồn, mã ghép, nhật ký và bảng đối chiếu; xác nhận đơn vị, định nghĩa nhãn | File nguồn có hash; nhật ký giá trị cũ/mới; metadata và định nghĩa QC | Người khác chạy lại ra 0 ô lệch; mỗi thay đổi truy được căn cứ; điểm chưa xác nhận ghi rõ |
| 2 — hiện trường (1–3 tháng) | Q2, Q4 | Ưu tiên kiểm chứng khuôn K_Scatch trên A400 ở độ dày 40; thu thập mẫu số sản lượng | Sản lượng theo dòng/độ dày; mã tấm/cuộn, thiết bị, ca; tốc độ, nhiệt độ, tuổi con lăn; ngày thật | Có đối chiếu hiện trường bằng dữ liệu và đủ mẫu số; chưa đưa ra điều chỉnh vật lý khi thiếu bằng chứng |
| 2 — nhãn lỗi (1–3 tháng) | Q1, Q3, Q5 | Cùng QC kiểm tra tính không đồng nhất của Other_Faults và hướng tách nhóm con | Ảnh lỗi; định nghĩa nhãn; bản ghi nhóm Min > 120 và nhóm đối chiếu | QC xác nhận định nghĩa, nhãn mới và ví dụ minh họa; kiểm tra nhất quán giữa người gán nhãn |
| 3 — dự báo (3–6 tháng; có điều kiện) | Q3 | Tách tập kiểm tra độc lập trước chọn ngưỡng; đánh giá quy tắc hoặc mô hình nếu dữ liệu cho phép | Dữ liệu mới, mã tấm/cuộn để tránh rò rỉ giữa tập; nhãn được QC xác nhận | Báo precision/recall trên tập chưa chọn ngưỡng; nếu đa lớp, thêm F1 từng lớp/macro và cỡ mẫu |
| Bổ sung — thương mại | Q6 | Đối chiếu phiên bản HS trước khi giải thích biến động và bổ sung giá/khối lượng nếu có | Bảng quy đổi HS, tài liệu phạm vi, dữ liệu lượng/giá có nguồn | Chuỗi so sánh có phạm vi nhất quán hoặc giới hạn ghi rõ; chỉ kết luận ở cấp ngành |

## Kết luận phân tích

Mức A xác nhận mô tả trong mẫu; mức B cần bằng chứng bên ngoài; mức C chưa đủ dữ liệu để kết luận. Ưu tiên giữ hồ sơ chạy lại, xác nhận định nghĩa/đơn vị, thu thập sản lượng và kiểm chứng hiện trường. Dự báo chỉ đánh giá trên tập độc lập; thương mại là bối cảnh riêng. Các công việc này là đề xuất, chưa thực hiện.
