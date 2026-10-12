# ĐỀ CƯƠNG TIỂU LUẬN

## TRỰC QUAN HÓA VÀ PHÂN TÍCH DỮ LIỆU LỖI BỀ MẶT THÉP BẰNG PYTHON

## A. Nguyên tắc tổ chức theo khung mẫu

Giữ cấu trúc **phần mở đầu → bốn chương → kết luận → tài liệu tham khảo → phụ lục** của khung mẫu, đồng thời điều chỉnh nội dung theo bài toán trực quan hóa dữ liệu. Không đưa các công nghệ Big Data, LLM, Dagster hay dbt vào báo cáo vì chúng không thuộc phần thực hiện của đề tài.

Mạch trình bày: **giới thiệu bài toán → giải thích kiến thức cần dùng → khảo sát dữ liệu và lựa chọn công cụ → thực hiện bằng Python → trình bày kết quả, kiểm thử và thảo luận**.

| Phần | Vai trò | Nội dung được trình bày |
|---|---|---|
| Phần mở đầu | Xác định đề tài | Lý do lựa chọn, mục tiêu, phạm vi, câu hỏi phân tích và bố cục |
| Chương 1 | Cung cấp nền tảng lý thuyết | Bài toán lỗi bề mặt thép; chất lượng dữ liệu; thống kê mô tả; biểu đồ và dashboard |
| Chương 2 | Khảo sát đầu vào và xác định yêu cầu | Nguồn, cấu trúc, tình trạng dữ liệu; công cụ; tiêu chí phân tích và yêu cầu sản phẩm |
| Chương 3 | Trình bày cách thực hiện | Đọc dữ liệu, làm sạch, kết hợp, tạo biến, xây dựng biểu đồ và dashboard bằng Python |
| Chương 4 | Trình bày kết quả và đánh giá | Kết quả xử lý; trả lời Q1–Q5; giao diện dashboard; kiểm thử; thảo luận và hạn chế |

**Cách nối các chương:** Chương 1 giải thích phương pháp; Chương 2 xác định vấn đề cần áp dụng phương pháp; Chương 3 thể hiện thao tác thực hiện; Chương 4 cho biết kết quả và phạm vi kết luận. Ví dụ: Chương 1 giải thích dữ liệu thiếu; Chương 2 ghi nhận 70 ô thiếu ở đầu vào; Chương 3 trình bày cách loại trùng và khôi phục có truy vết; Chương 4 tổng hợp số ô khôi phục cùng kết quả kiểm tra sau xử lý.

**Phân biệt Chương 3 và Chương 4:** Chương 3 có thể đưa đoạn mã, cấu trúc bảng và đầu ra minh họa để giải thích cách làm. Biểu đồ hoàn chỉnh, bảng kết quả tổng hợp và nhận xét định lượng đặt chủ yếu ở Chương 4. Không chèn lại cùng một hình hoặc cùng một bảng dài ở cả hai chương.

XLSX chỉ là định dạng tệp đầu vào. Toàn bộ thao tác xử lý, tính toán, trực quan hóa và xây dựng dashboard sử dụng Python. Diễn đạt theo dạng tiểu luận ứng dụng, dùng các từ **mục tiêu, câu hỏi phân tích, phạm vi thực hiện, kết quả và nhận xét**; không cần đặt tên mục là “mục tiêu nghiên cứu” hoặc “giả thuyết nghiên cứu”.

### Phân bổ dung lượng dự kiến

| Phần | Số trang dự kiến |
|---|---:|
| Phần mở đầu | 2 |
| Chương 1. Tổng quan bài toán và cơ sở lý thuyết | 3 |
| Chương 2. Khảo sát dữ liệu, công cụ và yêu cầu thực hiện | 4 |
| Chương 3. Xây dựng quy trình xử lý và trực quan hóa bằng Python | 5 |
| Chương 4. Kết quả phân tích, kiểm thử và thảo luận | 10 |
| Kết luận và hướng phát triển | 1 |
| **Tổng phần nội dung chính** | **25** |

Đây là kế hoạch dung lượng, không phải giới hạn cứng. Chương 4 có thể tăng lên 11–12 trang khi chèn hình. Bìa, mục lục, danh mục, tài liệu tham khảo và phụ lục bố trí riêng; cách tính trang cuối cùng theo quy định môn học. Không thu nhỏ chữ hoặc hình để ép đủ 25 trang.

## B. Phần đầu báo cáo

1. Bìa theo mẫu của môn học/khoa.
2. Mục lục.
3. Danh mục hình vẽ.
4. Danh mục bảng biểu.
5. Danh mục thuật ngữ và từ viết tắt.
6. Phần mở đầu.

Có thể thêm tóm tắt và từ khóa trước mục lục nếu mẫu môn học yêu cầu. Không bắt buộc thêm lời cam đoan, lời cảm ơn hoặc các mục khác chỉ để giống hình thức luận văn.

Danh mục viết tắt chỉ gồm thuật ngữ thực sự xuất hiện, chẳng hạn UCI, EDA, IQR, SD, KPI, API, CSV và JSON. Tên thư viện không cần coi là từ viết tắt.

## C. Phần mở đầu — khoảng 2 trang

### 1. Bối cảnh và lý do lựa chọn đề tài

Trình bày nhu cầu đọc và so sánh dữ liệu lỗi bề mặt thép chứa nhiều đặc trưng; khó khăn khi chỉ quan sát bảng số liệu; vai trò của làm sạch dữ liệu và trực quan hóa trong việc nhận diện cơ cấu nhãn, đặc trưng từng nhóm và giá trị cần xem xét.

Giới thiệu ngắn đề tài và lựa chọn Python để tổ chức quy trình có thể chạy lại. Các thông tin về sản xuất thép hoặc nguồn dữ liệu cần có tài liệu dẫn; không mô tả thiết bị, nhà máy hay quy trình thu thập của bộ dữ liệu khi chưa được xác nhận.

### 2. Mục tiêu thực hiện

**Mục tiêu chung:** xây dựng quy trình xử lý và trực quan hóa dữ liệu lỗi bề mặt thép bằng Python, trình bày kết quả bằng biểu đồ và dashboard tương tác.

**Mục tiêu cụ thể:**

- Khảo sát cấu trúc, chất lượng và giới hạn của dữ liệu đầu vào.
- Làm sạch, chuẩn hóa và kết hợp nguồn tham chiếu có kiểm tra, có nhật ký thay đổi.
- Tạo biến, tính các chỉ số mô tả và xây dựng biểu đồ trả lời câu hỏi phân tích.
- Xây dựng dashboard có bộ lọc, bảng, chỉ số tổng hợp và chức năng cập nhật nguồn; kiểm thử tính nhất quán của số liệu.

### 3. Đối tượng và phạm vi thực hiện

Đối tượng phân tích là các bản ghi có nhãn lỗi trong bộ dữ liệu Steel Plates Faults và tệp thực hành tương ứng. Một bản ghi không mặc định là một tấm thép độc lập.

Phạm vi gồm chất lượng dữ liệu, cơ cấu bảy nhãn lỗi, dòng thép A300/A400, độ sáng, độ dày và diện tích. Phân tích mang tính mô tả và khám phá; thiếu sản lượng và biến vận hành nên chưa xác định tỷ lệ sản phẩm lỗi hoặc quan hệ nhân quả.

`Production_Date` là ngày mô phỏng, phục vụ chuẩn hóa và hồ sơ dữ liệu; không dùng để suy ra xu hướng sản xuất thật. Phần UN Comtrade, mang mã Q6 trong notebook, là nội dung bổ sung ở phụ lục, độc lập với các bản ghi lỗi.

### 4. Các câu hỏi phân tích

| Mã | Câu hỏi |
|---|---|
| Q0 | Những vấn đề nào được phát hiện trước khi tham chiếu giá trị UCI; việc khôi phục có truy vết và dữ liệu sau xử lý có đáp ứng các điều kiện toàn vẹn không? |
| Q1 | Cơ cấu bảy nhãn lỗi như thế nào; mức tập trung và mất cân bằng giữa các nhãn ra sao? |
| Q2 | Cơ cấu nhãn khác nhau thế nào giữa A300/A400; nhãn nào có trên 90% bản ghi tập trung ở cùng một dòng thép? |
| Q3 | Phân bố độ sáng tối thiểu/tối đa khác nhau thế nào giữa các nhãn; nhãn nào có khoảng P25–P75 của độ sáng tối thiểu không chồng lấn với mọi nhãn khác? |
| Q4 | Phân bố độ dày khác nhau thế nào giữa các nhãn và giữa A300/A400 trong cùng nhãn? |
| Q5 | Diện tích Pixels_Areas khác nhau thế nào giữa các nhãn về trung vị, IQR và các giá trị ngoài râu boxplot? |

Q0 là điều kiện kiểm tra đầu vào và xác nhận kết quả xử lý. Q1–Q5 là các câu hỏi phân tích chính. Tiêu chí, mẫu số và loại biểu đồ được cụ thể hóa ở mục 2.4.

### 5. Giá trị của đề tài và sản phẩm đầu ra

Nêu giá trị học tập và ứng dụng: kết nối sáu bước môn học trong một quy trình Python; giúp người đọc quan sát cơ cấu và phân bố đặc trưng; cho phép lọc và đối chiếu số liệu trên dashboard.

Sản phẩm gồm notebook, dữ liệu sau xử lý, nhật ký, bảng thống kê, hình trực quan, dashboard và minh chứng kiểm thử. Chỉ đánh giá hiệu quả ra quyết định hoặc trải nghiệm người dùng nếu có phép đo thực tế.

### 6. Bố cục của báo cáo

Giới thiệu mỗi chương bằng một hoặc hai câu theo vai trò tại phần A. Không lặp toàn bộ mục lục hoặc phần mục tiêu.

## D. Đề cương chi tiết bốn chương

## CHƯƠNG 1. TỔNG QUAN BÀI TOÁN VÀ CƠ SỞ LÝ THUYẾT — khoảng 3 trang

### 1.1. Tổng quan bài toán phân tích lỗi bề mặt thép

#### 1.1.1. Đặc điểm dữ liệu lỗi bề mặt thép

Giới thiệu các nhóm thông tin thường dùng trong bài: vị trí/kích thước, diện tích, độ sáng, dòng thép, độ dày và nhãn lỗi. Giải thích vì sao cần kết hợp biến định lượng và biến phân loại để so sánh các nhóm. Chưa liệt kê toàn bộ cột hoặc tình trạng cụ thể của tệp thực hành.

#### 1.1.2. Vai trò của phân tích khám phá và trực quan hóa

Giải thích vai trò của EDA trong phát hiện đặc điểm phân bố, cơ cấu nhãn, mức chồng lấn và giá trị đáng chú ý. Giới thiệu ngắn tài liệu liên quan sử dụng Steel Plates Faults để đặt phạm vi của bài vào bối cảnh phân tích dữ liệu; chẳng hạn tài liệu phân loại/XAI của Kharal (2020). Chỉ dẫn nội dung đã đọc và có liên quan.

### 1.2. Cơ sở về chất lượng và xử lý dữ liệu

#### 1.2.1. Dữ liệu thiếu, trùng lặp và không nhất quán

Trình bày khái niệm, tác động tới phép đếm và thống kê; phân biệt sai kiểu, nhãn biểu diễn không thống nhất và giá trị vi phạm quan hệ logic. Một giá trị lớn hoặc ngoài râu boxplot chưa đủ để coi là nhập sai.

#### 1.2.2. Chuẩn hóa, kết hợp và kiểm tra dữ liệu

Nêu nguyên tắc chuẩn hóa nhãn/kiểu số; xác định tiêu chí trùng; kiểm tra khóa trước ghép; sử dụng nguồn tham chiếu; lưu giá trị cũ/mới và căn cứ thay đổi. Phân biệt **phát hiện vấn đề → chọn giá trị sửa → kiểm tra sau sửa**. Liên hệ mục 2.2 và 3.3.

### 1.3. Cơ sở thống kê mô tả và tạo biến

#### 1.3.1. Các chỉ số thống kê sử dụng

Trình bày số đếm, tỷ trọng, tỷ trọng lũy kế, N, trung vị, P25/P75, IQR, độ lệch chuẩn mẫu và hệ số tương quan Pearson. Chọn vài công thức cần thiết; ghi ý nghĩa và điều kiện diễn giải.

Phân biệt tỷ trọng một nhãn **trong một dòng thép** với tỷ trọng một dòng thép **trong một nhãn**. Pearson giữa hai biến định lượng không đo khả năng phân loại nhãn.

#### 1.3.2. Biến phái sinh và phép biến đổi logarit

Giới thiệu tổng hợp biến phân loại từ cờ nhị phân, lấy hiệu cực đại–cực tiểu, logarit cơ số 10 và mục đích sử dụng. Biến tính lại từ thông tin đã có không được coi là đặc trưng độc lập mới. Công thức trên tên cột thực tế và mã nằm ở 3.4.

### 1.4. Cơ sở lựa chọn biểu đồ và dashboard

#### 1.4.1. Biểu đồ cơ cấu và so sánh nhóm

Giải thích thanh ngang, Pareto, cột nhóm và cột 100%; liên hệ Q1/Q2. Cột số lượng và cột tỷ trọng phục vụ hai cách đọc khác nhau; cần ghi mẫu số.

#### 1.4.2. Biểu đồ phân bố và mối liên hệ

Giải thích scatter, boxplot, râu hộp, điểm ngoài râu và trục log; liên hệ Q3–Q5. Với quy tắc 1,5 × IQR, râu kết thúc ở giá trị quan sát nằm trong hàng rào; không mặc định râu chính là hai hàng rào. Nêu vai trò của N, độ trong suốt và kích thước điểm khi các điểm chồng lấn.

#### 1.4.3. Dashboard tương tác

Giới thiệu các thành phần: bộ lọc, KPI, biểu đồ, bảng, tải dữ liệu và cập nhật nguồn. Nguyên tắc: các thành phần của cùng phần phân tích dùng cùng tập con sau lọc; có trạng thái phù hợp khi tập con rỗng.

### 1.5. Tiểu kết chương

Tóm lược kiến thức sẽ được dùng để khảo sát đầu vào ở Chương 2 và triển khai ở Chương 3. Khoảng một đoạn; chưa đưa kết quả định lượng của từng nhãn.

**Minh chứng đề xuất:** Bảng 1.1 loại biểu đồ–mục đích–câu hỏi áp dụng; công thức thống kê chọn lọc. Bảng nguồn và sơ đồ triển khai để ở các chương sau.

## CHƯƠNG 2. KHẢO SÁT DỮ LIỆU, CÔNG CỤ VÀ YÊU CẦU THỰC HIỆN — khoảng 4 trang

### 2.1. Nguồn và cấu trúc dữ liệu

#### 2.1.1. Tệp dữ liệu thực hành

Giới thiệu tệp đầu vào 1.961 dòng × 29 cột: 27 đặc trưng, ngày mô phỏng và nhãn văn bản. Mô tả nguồn tệp, định dạng, vai trò và thời điểm tiếp nhận nếu có hồ sơ. Chưa gọi đây là dữ liệu sạch.

#### 2.1.2. Nguồn tham chiếu UCI

Giới thiệu Steel Plates Faults: 1.941 bản ghi, 27 đặc trưng và 7 cột nhãn one-hot trong tệp nguồn; dẫn Buscema, Terzi và Tastle (2010), DOI `10.24432/C5J88N`, giấy phép CC BY 4.0.

Nêu rõ hai vai trò: tệp thực hành dùng để thực hiện quy trình làm sạch; UCI cung cấp metadata và giá trị tham chiếu cho các bản ghi tương ứng. Bốn tọa độ chỉ được dùng làm khóa sau khi kiểm tra không thiếu, nguyên, duy nhất và khớp một–một.

#### 2.1.3. Nhóm biến và giới hạn thông tin

Mô tả nhóm tọa độ/kích thước, độ sáng, dòng thép/độ dày, chỉ số và nhãn. Giữ nguyên thang đo khi metadata chưa xác nhận đơn vị. Từ điển đầy đủ ở Phụ lục A.

Nêu những giới hạn cần tính đến khi chọn phương pháp: Other_Faults là nhãn gộp; không có sản lượng, mã tấm/cuộn hoặc biến vận hành đầy đủ; ngày là mô phỏng; một số biến chứa thông tin phái sinh trùng nhau. UN Comtrade không có khóa nối với UCI, nên không kết hợp ở cấp bản ghi.

### 2.2. Khảo sát tình trạng dữ liệu trước xử lý

| Nội dung | Tình trạng đã ghi nhận | Yêu cầu phát sinh |
|---|---|---|
| Quy mô/kiểu dữ liệu | 1.961 dòng; một số cột số có biểu diễn hỗn hợp | Kiểm tra kiểu và chuyển đổi có theo dõi |
| Ô thiếu trong 27 đặc trưng | 70 ô: Pixels_Areas 32; Steel_Plate_Thickness 30; Log_Y_Index 4; Orientation_Index 4 | Xác định vị trí và căn cứ khôi phục |
| Trùng lặp | 20 dòng trùng theo 27 đặc trưng + ngày gốc + nhãn chuẩn | Xác định dòng giữ/dòng loại và ghi nhật ký |
| Biểu diễn nhãn | 28 biểu diễn cho 7 nhãn chuẩn | Chuẩn hóa theo ánh xạ đã kiểm tra |
| Chỉ số bất thường | Ví dụ Empty_Index = 2031; Log_Y_Index = 18129 | Kiểm tra quan hệ nội tại và đối chiếu nguồn khi sửa |
| Ngày | Định dạng hỗn hợp, giá trị mô phỏng | Chuẩn hóa hồ sơ; không dùng phân tích thời gian sản xuất |
| Diện tích | Dải giá trị rộng, có giá trị rất lớn | Gắn cờ để xem xét; cân nhắc trục log khi hiển thị |

Kèm giải thích tác động của từng vấn đề lên tổng hợp và biểu đồ. Số trùng được xác định sau chuẩn hóa nhãn, không phải 20 dòng giống hệt mọi giá trị thô. 28 biểu diễn không có nghĩa 28 loại lỗi hoặc tất cả đều sai.

Mục này chỉ mô tả đầu vào và yêu cầu. Số ô đã khôi phục, số giá trị đã sửa và chất lượng cuối cùng đặt ở 4.1.

### 2.3. Công cụ và môi trường thực hiện

#### 2.3.1. Công cụ xử lý và trực quan hóa

| Công cụ | Vai trò trong đề tài |
|---|---|
| Python, Jupyter Notebook | Tổ chức mã, thực hiện quy trình và lưu kết quả |
| Pandas, NumPy | Đọc nguồn, chuẩn hóa, ghép, tạo biến và thống kê |
| Matplotlib, Seaborn | Xây dựng biểu đồ tĩnh cho báo cáo |
| Streamlit, Plotly | Xây dựng dashboard và biểu đồ tương tác |
| requests, json | Đọc nguồn/API và xử lý phản hồi theo mã thực tế |

Chỉ liệt kê công cụ thực sự được sử dụng. Không thêm công nghệ có trong khung mẫu nhưng không có trong notebook/ứng dụng.

#### 2.3.2. Căn cứ lựa chọn Python

Giải thích sự phù hợp với dữ liệu dạng bảng, khả năng thống nhất xử lý và vẽ hình, chạy lại quy trình và dùng chung kết quả với dashboard. Không khẳng định nhanh hơn hoặc tốt hơn Excel nếu chưa thực hiện phép so sánh. Phiên bản và hướng dẫn cài đặt chuyển Phụ lục C; môi trường kiểm thử cụ thể nêu lại ở 4.4.

### 2.4. Yêu cầu phân tích và tiêu chí đọc kết quả

#### 2.4.1. Đầu ra cho Q0–Q5

| Mã | Đầu ra cần có | Tiêu chí/cách đọc | Kết quả |
|---|---|---|---|
| Q0 | Bảng phát hiện, nhật ký thay đổi, bảng kiểm tra sau xử lý | Tách ô/dòng; phát hiện nội tại; căn cứ sửa; độ khớp sau khôi phục | 4.1 |
| Q1 | Thanh ngang, Pareto, bảng cơ cấu | Thứ hạng, tỷ trọng ba nhãn đầu, lũy kế 80%, tỷ số cỡ mẫu lớn nhất/nhỏ nhất | 4.2.1 |
| Q2 | Cột nhóm, cột 100%, bảng tỷ trọng hai chiều | Nhãn g tập trung nếu max_s n(g,s)/n(g) > 0,90; cơ cấu trong dòng thép dùng mẫu số riêng | 4.2.2 |
| Q3 | Scatter và bảng N/trung vị/P25/P75 | Với mỗi nhãn h khác g: P75_g < P25_h hoặc P25_g > P75_h của độ sáng tối thiểu; chạm đầu mút không đạt | 4.2.3 |
| Q4 | Boxplot, bảng nhãn × dòng thép | Trung vị, IQR, SD trong cùng nhãn; luôn đọc kèm N | 4.2.4 |
| Q5 | Boxplot diện tích trục log, bảng thống kê | Trung vị, IQR, min/max và các điểm ngoài râu theo nhóm | 4.2.5 |

Mốc >90% được dẫn từ tài liệu đọc, mục V.3, và dùng như mốc khám phá, không phải chuẩn kỹ thuật của ngành. Tiêu chí Q3 đã được bổ sung sau khi xem kết quả, vì vậy không trình bày như giả thuyết được xác định trước. IQR không chồng lấn chỉ mô tả phần trung tâm, không chứng minh toàn bộ phân bố tách biệt. Q5 dùng đại lượng thống kê thay cho khái niệm “khác biệt rõ” chưa được định nghĩa.

#### 2.4.2. Yêu cầu dashboard và kiểm thử

Yêu cầu gồm bộ lọc phù hợp, KPI/biểu đồ/bảng nhất quán, xử lý tập rỗng, tải CSV, đọc lại nguồn và giữ bản dữ liệu hợp lệ khi nguồn lỗi. Bộ lọc lỗi và phạm vi năm thương mại độc lập. Mỗi yêu cầu phải có chức năng ở 3.6 và tình huống kiểm thử ở 4.4.

### 2.5. Định hướng thực hiện và tiểu kết

Lập bảng ngắn nối vấn đề ở 2.2 với thao tác ở Chương 3 và minh chứng ở Chương 4. Chỉ nêu hướng giải quyết: chuẩn hóa, loại trùng, kiểm tra nội tại, ghép nguồn, tạo biến, vẽ hình và triển khai dashboard; chưa đưa mã hoặc diễn giải kết quả cuối cùng.

**Minh chứng đề xuất:** Bảng 2.1 nguồn và nhóm biến; Bảng 2.2 tình trạng đầu vào; Bảng 2.3 yêu cầu–đầu ra–tiêu chí. Có thể gộp bảng định hướng vào Bảng 2.2 để giảm lặp.

## CHƯƠNG 3. XÂY DỰNG QUY TRÌNH XỬ LÝ VÀ TRỰC QUAN HÓA BẰNG PYTHON — khoảng 5 trang

### 3.1. Quy trình thực hiện tổng thể

Trình bày sơ đồ sáu bước: **xác định yêu cầu → thu thập/đọc dữ liệu → làm sạch và kết hợp → tạo biến/chỉ số → vẽ biểu đồ → xây dựng dashboard có cập nhật nguồn**.

Giải thích đầu vào, đầu ra và mối liên hệ giữa notebook, tệp dữ liệu sạch, bảng/hình và ứng dụng. Tệp thô được giữ riêng; kết quả xuất ra có thể đối chiếu khi chạy lại.

### 3.2. Đọc và tổ chức dữ liệu đầu vào

Minh họa đọc XLSX/CSV bằng Pandas và đọc nguồn/phản hồi lưu sẵn theo cách thực tế trong mã. Kiểm tra tên cột, kiểu và khóa; dẫn bảng khảo sát ở 2.2 thay vì chép lại. Ghi hồ sơ nguồn và tổ chức thư mục dữ liệu/kết quả.

Chi tiết API thương mại ở Phụ lục D; không biến phần này thành luồng thu thập chính của đề tài.

### 3.3. Thực hiện làm sạch, kết hợp và kiểm chứng dữ liệu

#### 3.3.1. Chuẩn hóa nhãn, kiểu số và loại trùng

Đưa đoạn mã chọn lọc cho ánh xạ nhãn và chuyển kiểu có kiểm tra. Tiêu chí trùng: 27 đặc trưng + ngày gốc + nhãn chuẩn; lưu liên kết dòng giữ/dòng loại. Không gọi các dòng có chung tọa độ nhưng khác thông tin là trùng chỉ vì chung khóa.

#### 3.3.2. Kiểm tra nội tại trước khôi phục

Trình bày các quan hệ làm việc dùng phát hiện chỉ số bất thường, điều kiện đủ toán hạng và cách lưu ô bị gắn cờ. Phân biệt phép phát hiện trước sửa với kiểm tra công thức sau sửa. Không cộng cùng một ô vi phạm nhiều quy tắc thành nhiều lỗi độc lập.

Notebook hiện kiểm tra công thức sau khôi phục. Phép kiểm tra trước tham chiếu đã được thực hiện bổ sung trong `outputs/ra_soat_de_cuong/`; khi viết, phải ghi rõ nguồn kết quả bổ sung hoặc tích hợp phép kiểm tra vào đúng thứ tự trong notebook.

#### 3.3.3. Ghép UCI và khôi phục có truy vết

Trình bày kiểm tra bốn tọa độ làm khóa, xác nhận ghép một–một và nhãn tương ứng; cách điền ô thiếu, sửa chỉ số và lưu giá trị cũ/mới/dòng nguồn. Đưa một đoạn mã ghép hoặc một mẫu nhật ký nhỏ.

Các công thức nội tại là quan hệ làm việc đã đối chiếu, không tự gọi là định nghĩa chính thức UCI. Việc đối chiếu sau khôi phục xác nhận ghép và sử dụng nguồn đúng; không dùng độ khớp với chính nguồn đã điền làm precision/recall phát hiện lỗi.

#### 3.3.4. Chuẩn hóa ngày, gắn cờ diện tích và kiểm tra đầu ra

Giữ ngày gốc và cờ mô phỏng; nêu lý do chuẩn hóa dù không phân tích thời gian. Gắn cờ diện tích theo IQR toàn tập để xem xét, giữ bản ghi khi chưa có căn cứ loại. Kiểm tra nhãn, logic, quan hệ phái sinh, số dòng và xuất/đọc lại. Các số tổng hợp cuối cùng đặt ở 4.1.

### 3.4. Tạo biến phái sinh và các bảng thống kê

| Biến/chỉ số | Công thức hoặc cách thực hiện | Mục đích |
|---|---|---|
| Steel_Type | Tổng hợp cờ A300/A400 sau kiểm tra hợp lệ | Q2/Q4 |
| X_Range, Y_Range | Tọa độ cực đại − cực tiểu theo từng trục | Mô tả khung bao, không đồng nhất với diện tích lỗi |
| Luminosity_Range | Maximum_of_Luminosity − Minimum_of_Luminosity | Khoảng độ sáng |
| Log_Pixels_Areas | log10(Pixels_Areas), với diện tích dương | Kiểm chứng với LogOfAreas và hỗ trợ diễn giải |
| Số đếm/tỷ trọng/lũy kế | Tổng hợp theo nhãn/dòng thép | Q1/Q2 |
| Thống kê đặc trưng | N, trung vị, P25/P75, IQR, SD mẫu, min/max | Q3–Q5 |
| Pearson Min–Max | Tương quan hai biến độ sáng | Thông tin bổ trợ Q3 |

Giải thích rõ mẫu số trong các bảng tỷ trọng. `Log_Pixels_Areas` tính lại thông tin của `LogOfAreas` với độ chính xác chưa làm tròn, không phải một đặc trưng độc lập mới. Notebook dùng cơ số 10 và dung sai đối chiếu `0,00010001`.

`Luminosity_Range` được định nghĩa bằng hiệu Max−Min; chưa có căn cứ để gọi tương đương với `Luminosity_Index`. Boxplot Q5 tính tứ phân vị/râu trên Pixels_Areas gốc, sau đó đổi trục hiển thị sang log.

### 3.5. Xây dựng biểu đồ theo câu hỏi phân tích

Nêu cách chuyển bảng thống kê thành biểu đồ, lựa chọn sắp xếp, màu nhãn, chú thích, N và thang đo. Minh họa bằng một hoặc hai đoạn mã tiêu biểu, không đưa toàn bộ mã của mọi biểu đồ.

- Q1: thanh ngang và Pareto.
- Q2: cột nhóm, cột 100% và bảng tỷ trọng trong từng nhãn.
- Q3: scatter Min–Max theo màu nhãn, kết hợp bảng tứ phân vị.
- Q4: boxplot độ dày và bảng so sánh trong cùng nhãn theo dòng thép.
- Q5: boxplot diện tích trên trục log và bảng thống kê.

Các hình kết quả và câu trả lời hoàn chỉnh đặt ở 4.2. Nêu cách xuất hình và bảng để chèn báo cáo; không dùng ảnh chụp toàn bộ notebook.

### 3.6. Xây dựng dashboard tương tác

#### 3.6.1. Kiến trúc và tổ chức giao diện

Trình bày Streamlit/Plotly, luồng đọc nguồn–xử lý–lọc–tổng hợp–hiển thị và ba tab hiện có. Tab thương mại là chức năng bổ sung. Nêu cách sử dụng dữ liệu sạch hoặc tái lập kết quả bằng module dùng chung; căn cứ theo mã thực tế.

#### 3.6.2. Bộ lọc, KPI, biểu đồ và bảng dữ liệu

Trình bày cách áp dụng bộ lọc và dùng cùng tập con để tính số liệu; xử lý tập rỗng; chức năng tải CSV. Ảnh giao diện thực tế và ví dụ sử dụng ở 4.3.

#### 3.6.3. Cập nhật nguồn và xử lý lỗi

Giải thích đọc lại nguồn/làm mới, cache và giữ bản hợp lệ khi nguồn lỗi theo chức năng đã triển khai. Phân biệt cập nhật tệp nguồn với dữ liệu cảm biến thời gian thực; ngày mô phỏng không điều khiển chu kỳ cập nhật.

### 3.7. Tổ chức thực thi và tiểu kết

Nêu trình tự chạy notebook, tạo đầu ra và khởi động dashboard; các tệp cần thiết và điểm kiểm tra chính. Mã đầy đủ, lệnh cài đặt và hướng dẫn chạy chi tiết ở Phụ lục C.

Tiểu kết dẫn sang Chương 4 để đối chiếu kết quả với các yêu cầu ở 2.4.

**Minh chứng đề xuất:** Hình 3.1 quy trình sáu bước; Hình 3.2 luồng dữ liệu dashboard; Bảng 3.1 biến/chỉ số; đoạn mã then chốt và mẫu nhật ký nhỏ. Không đặt các hình kết quả Q1–Q5 ở đây rồi lặp lại ở Chương 4.

## CHƯƠNG 4. KẾT QUẢ PHÂN TÍCH, KIỂM THỬ VÀ THẢO LUẬN — khoảng 10 trang hoặc hơn khi chèn hình

### 4.1. Kết quả xử lý và kiểm chứng dữ liệu — Q0

#### 4.1.1. Kết quả chuẩn hóa và khôi phục

Đưa bảng trước/sau xử lý: loại 20 dòng trùng; còn 1.941 bản ghi; khôi phục 67 ô thiếu sau loại trùng; sửa 16 giá trị; đưa các biểu diễn nhãn về 7 nhãn chuẩn. Chuyển kiểu số có 0 chuỗi chuyển đổi thất bại; không tạo thêm lỗi giả để minh họa.

70 ô thiếu là số ở đầu vào, 67 là số còn cần khôi phục sau loại trùng. Không gộp các số ở hai thời điểm thành một kết quả.

#### 4.1.2. Kết quả phát hiện trước tham chiếu và kiểm tra sau xử lý

Phép rà soát bổ sung phát hiện 10 ô Empty_Index và 6 ô Log_Y_Index vi phạm quan hệ nội tại. Tập 16 ô này trùng tập ô đã sửa theo UCI; trong phạm vi bốn quan hệ được rà soát có 0 ô thuộc nhật ký sửa chỉ được phát hiện qua tham chiếu. Ghi phạm vi, số đã kiểm tra và điều kiện đủ toán hạng; không khái quát thành khả năng phát hiện mọi lỗi dữ liệu.

52.407 ô đặc trưng sau xử lý khớp UCI và nhãn khớp. Đây là minh chứng khôi phục/ghép đúng nguồn. 395 bản ghi có diện tích bị gắn cờ IQR toàn tập được giữ vì chưa có căn cứ coi là nhập sai.

Nhật ký chi tiết ở Phụ lục B; dẫn minh chứng bổ sung từ `outputs/ra_soat_de_cuong/` theo trạng thái thực tế của notebook.

### 4.2. Kết quả trực quan hóa và trả lời câu hỏi phân tích

Mỗi tiểu mục theo mạch **câu hỏi → bảng/hình → nhận xét có số liệu → câu trả lời trong phạm vi dữ liệu**. Dẫn cách thực hiện ở Chương 3, không lặp phần lý thuyết hoặc mã dài.

#### 4.2.1. Cơ cấu và mức tập trung của các nhãn lỗi — Q1

Hình 4.1a–b: thanh ngang và Pareto. Đọc thứ hạng, tỷ trọng và lũy kế; Other_Faults có 673 bản ghi; ba nhãn đầu gồm Other_Faults, Bumps, K_Scatch có tổng 1.466/1.941, khoảng 75,53%. Nhận xét mất cân bằng, ý nghĩa của nhãn gộp và điểm đạt lũy kế 80% dựa trên bảng thực tế. Không dùng số đếm để xếp hạng thiệt hại.

#### 4.2.2. Cơ cấu lỗi theo dòng thép A300/A400 — Q2

Hình 4.2a–b: cột nhóm và cột 100%; kèm bảng tỷ trọng trong từng nhãn. A300 có 777, A400 có 1.164 bản ghi lỗi. Với K_Scatch, phân biệt 390/391 tập trung ở A400, khoảng 99,74%, với 390/1.164 bản ghi A400 mang nhãn đó, khoảng 33,51%.

Nhận xét các nhãn vượt mốc >90% theo bảng đầy đủ và cơ cấu trong từng dòng thép. Các tỷ trọng này không phải tỷ lệ lỗi trên tổng sản lượng.

#### 4.2.3. Đặc điểm độ sáng theo nhãn — Q3

Hình 4.3: scatter Min–Max; bảng N/trung vị/P25/P75. Pearson khoảng 0,4296. Khoảng P25–P75 của độ sáng tối thiểu ở K_Scatch là 35–49, trong khi P25 nhỏ nhất của sáu nhãn còn lại là 64; đáp ứng tiêu chí tách phần trung tâm ở 2.4.

Nhận xét thêm độ sáng tối đa và vùng chồng lấn nhìn thấy trên hình; không suy thành hiệu năng phân loại. Vùng Min > 120 chỉ nêu nếu giúp diễn giải Other_Faults và có bảng kiểm tra.

#### 4.2.4. Đặc điểm độ dày theo nhãn và dòng thép — Q4

Hình 4.4: boxplot độ dày; kèm bảng nhãn × dòng thép có N. K_Scatch có trung vị 40, SD khoảng 2,20; Bumps có trung vị 70 trên A300 và 40 trên A400.

Giải thích trường hợp hộp thu thành đường khi P25 = trung vị = P75. Nhóm N=1 chỉ mô tả bản ghi, không đủ đánh giá biến thiên hoặc suy rộng. Không tự gắn đơn vị mm khi nguồn chưa xác nhận.

#### 4.2.5. Đặc điểm diện tích theo nhãn — Q5

Hình 4.5: boxplot diện tích trục log; bảng thống kê rút gọn. Trung vị K_Scatch là 6.281, Stains là 16,5; đọc thêm IQR và cực trị trong bảng.

Tứ phân vị/râu được tính trên thang gốc, log chỉ thay đổi hiển thị. Phân biệt điểm ngoài râu theo từng nhãn với cờ IQR toàn tập ở 4.1; không mặc định các điểm đó là sai dữ liệu.

#### 4.2.6. Tổng hợp câu trả lời Q0–Q5

Bảng ngắn gồm câu hỏi, kết quả chính, hình/bảng minh chứng và phạm vi kết luận. Q0 tách phát hiện/khôi phục; Q2 và Q4 trả lời đủ các vế. Q6 dẫn sang Phụ lục D, không đưa vào kết quả trung tâm.

### 4.3. Kết quả xây dựng dashboard và tình huống sử dụng

#### 4.3.1. Giao diện tổng quan

Đưa ảnh chụp ứng dụng thực tế, thể hiện KPI, biểu đồ, bảng và bộ lọc. Chú thích trạng thái nguồn/phạm vi dữ liệu và thời điểm chụp. Không dùng hình mô phỏng thay cho ảnh sản phẩm đang chạy.

#### 4.3.2. Minh họa lọc dữ liệu và khai thác kết quả

Ví dụ lọc A400 + K_Scatch để đối chiếu KPI, bảng và biểu đồ cùng tập con; minh họa tải CSV hoặc làm mới nguồn nếu đủ chỗ. Ảnh tab nguồn và thương mại chuyển phụ lục. Không lặp mọi biểu đồ tĩnh dưới dạng ảnh dashboard.

### 4.4. Kiểm thử chức năng và đối chiếu số liệu

#### 4.4.1. Môi trường và cách kiểm thử

Ghi ngày chạy, phiên bản/môi trường, đầu vào và phạm vi kiểm thử. Phân biệt kiểm thử dữ liệu, Streamlit AppTest và kiểm tra giao diện trong trình duyệt. Nhánh API lỗi hoặc chu kỳ cập nhật được mô phỏng phải được ghi rõ.

#### 4.4.2. Kết quả các tình huống kiểm thử

Bảng gồm **yêu cầu → tình huống → kết quả mong đợi → quan sát → trạng thái**. Bao phủ đối chiếu notebook/dashboard khi cùng đầu vào, bộ lọc, tập rỗng, tải CSV, đọc lại nguồn và giữ bản hợp lệ khi nguồn lỗi theo các nhánh thực tế đã kiểm tra.

Tệp kết quả kiểm thử lưu sẵn không thay thế chạy kiểm thử mới nếu nội dung thực hiện đã thay đổi. Đạt kiểm thử chức năng chưa chứng minh trải nghiệm người dùng hoặc hiệu quả hỗ trợ quyết định.

### 4.5. Thảo luận, hạn chế và tiểu kết

#### 4.5.1. Nhận xét chung về các kết quả

Liên kết cơ cấu nhãn, tập trung theo dòng thép và đặc trưng độ sáng/độ dày/diện tích. Nêu biểu đồ làm rõ điều gì và còn khó đọc ở đâu: nhóm ít mẫu, hộp thu thành đường, chồng điểm, dải diện tích rộng.

Đề xuất nội dung nên kiểm tra thêm dựa trên bằng chứng trong mẫu. Ví dụ K_Scatch đồng thời tập trung ở A400 và độ dày 40, nên cần dữ liệu/thiết kế phân tích bổ sung để tách vai trò các yếu tố. Không đưa khuyến nghị điều chỉnh sản xuất như kết luận đã được kiểm chứng.

#### 4.5.2. Hạn chế và hướng khắc phục

Gắn mỗi hạn chế với kết luận bị ảnh hưởng: thiếu sản lượng → chưa có tỷ lệ sản phẩm lỗi; thiếu định danh → chưa kiểm tra độc lập của quan sát; ngày mô phỏng → không có xu hướng sản xuất thật; nhãn gộp/đơn vị chưa rõ → cần xác nhận khi diễn giải.

Chỉ so sánh với tài liệu liên quan ở nội dung có căn cứ. Không thêm mục so sánh độ chính xác với mô hình phân loại hoặc phương pháp Excel khi bài chưa thực hiện phép so sánh đó.

#### 4.5.3. Tiểu kết chương

Tóm lược kết quả nổi bật, mức đáp ứng yêu cầu và nội dung còn cần bổ sung. Không lặp nguyên bảng Q0–Q5.

**Minh chứng đề xuất:** Bảng 4.1 trước/sau xử lý; Bảng 4.2 phát hiện nội tại–sửa theo UCI; các bảng thống kê ngắn đi cùng Q1–Q5; bảng tổng hợp câu trả lời; bảng kiểm thử. Hình 4.1–4.5 cho các câu hỏi, Hình 4.6–4.7 cho dashboard. Đánh số bảng theo thứ tự thực tế khi dàn trang.

## E. Kết luận, tài liệu tham khảo và phụ lục

### KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN — khoảng 1 trang

Tóm tắt mục tiêu đã thực hiện, kết quả xử lý và trực quan hóa nổi bật, sản phẩm dashboard và phạm vi đáp ứng qua kiểm thử. Nêu hướng phát triển gần nhất: bổ sung thông tin vận hành/sản lượng/định danh, khảo sát nhóm con Other_Faults và mở rộng dự báo khi có dữ liệu phù hợp. Không thêm phát hiện mới trong kết luận.

### TÀI LIỆU THAM KHẢO

Chọn một kiểu trích dẫn thống nhất; dẫn nguồn dữ liệu, ngưỡng, công thức và kiến thức thực sự sử dụng. Không cần mô tả đề tài như một bản tái hiện tài liệu đọc, nhưng vẫn ghi nhận nguồn tại nơi dùng ý tưởng hoặc thông tin của nguồn đó.

Các nguồn cốt lõi đã kiểm tra trong quá trình chuẩn bị:

1. Buscema, M., Terzi, S., & Tastle, W. (2010). *Steel Plates Faults* [Dataset]. UCI Machine Learning Repository. [Hồ sơ dữ liệu và DOI](https://doi.org/10.24432/C5J88N). Nguồn cấu trúc, dữ liệu tham chiếu và giấy phép.
2. Kharal, A. (2020). *Explainable Artificial Intelligence Based Fault Diagnosis and Insight Harvesting for Steel Plates Manufacturing*. arXiv:2008.04448, bản v1. [Bản thảo](https://arxiv.org/abs/2008.04448). Tài liệu liên quan về phân loại/XAI; không tự gán tên tạp chí.
3. NIST/SEMATECH. *e-Handbook of Statistical Methods*, mục 1.3.3.7, *Box Plot*. [Tài liệu chính thức](https://www.itl.nist.gov/div898/handbook/eda/section3/boxplot.htm).
4. Đinh Nhật Anh, Nguyễn Thị Phương, Nguyễn Lê Ngọc Khôi. *Phân tích nguy cơ xảy ra lỗi trong dây chuyền sản xuất thép*, tài liệu trong `[Reading]-Data-Analytics-in-Manufacturing.pdf`. Năm chưa xác nhận; mục V.3 có mốc >90%; các mục liên quan trình bày quan hệ phái sinh. Dẫn tại nơi sử dụng.
5. Tài liệu chính thức của Pandas, Matplotlib, Streamlit và các thư viện thực sự cần dẫn; chọn trang hỗ trợ đúng thao tác/khái niệm, không chỉ đưa trang chủ để tăng số tài liệu.

Tufte hoặc nguồn về thiết kế biểu đồ có thể bổ sung sau khi đọc nội dung dùng thực tế. Phụ lục thương mại dẫn UN Comtrade và hồ sơ API riêng.

### PHỤ LỤC

- **Phụ lục A. Từ điển dữ liệu:** tên biến, nhóm biến, nhãn, thang đo/đơn vị đã xác nhận, quan hệ làm việc đã kiểm chứng và quy tắc ngày mô phỏng.
- **Phụ lục B. Minh chứng xử lý và thống kê chi tiết:** kiểm tra trước tham chiếu, nhật ký loại trùng/điền/sửa, khóa ghép, đối chiếu UCI và bảng dài.
- **Phụ lục C. Mã nguồn và hướng dẫn chạy:** cấu trúc tệp, môi trường/phiên bản, lệnh chạy notebook/dashboard/kiểm thử, kịch bản chi tiết và ảnh tab nguồn.
- **Phụ lục D. Phân tích bổ sung qua UN Comtrade — mã Q6:** minh họa API; Việt Nam, HS 72, World, xuất/nhập; dữ liệu trong bản thu thập 2015–2023; trị giá danh nghĩa; hai hình và ảnh tab thương mại. H4/H5/H6 chưa quy đổi. Truy vấn 2024 rỗng trong bản lưu không có nghĩa toàn nguồn thiếu dữ liệu. Phân tích độc lập với các bản ghi lỗi UCI.

## F. Ánh xạ sáu bước môn học vào báo cáo

| Bước | Cơ sở/yêu cầu | Thực hiện | Minh chứng/kết quả |
|---|---|---|---|
| 1. Xác định yêu cầu | Phần mở đầu; 2.4 | Quy trình tại 3.1 | Tổng hợp đáp ứng tại 4.2.6 và 4.4 |
| 2. Thu thập dữ liệu | Nguồn tại 2.1 | Đọc/tổ chức tại 3.2 | Hồ sơ nguồn, mẫu dữ liệu; chi tiết API ở Phụ lục D |
| 3. Làm sạch và kết hợp | Lý thuyết 1.2; tình trạng 2.2 | 3.3 | 4.1; Phụ lục B |
| 4. Tạo cột và chỉ số | Lý thuyết 1.3; yêu cầu 2.4 | 3.4 | Bảng thống kê tại 4.2; Phụ lục B |
| 5. Vẽ đồ thị bằng Python | Lý thuyết 1.4; tiêu chí 2.4 | 3.5 | 4.2.1–4.2.5 |
| 6. Dashboard tự động | Lý thuyết 1.4.3; yêu cầu 2.4.2 | 3.6 | 4.3–4.4 |

## G. Kế hoạch hình và lưu ý khi viết LaTeX

### Vị trí các hình hiện có

| Hình đề xuất | Nội dung/vị trí | Tệp trong `outputs/buoc_5/hinh/` |
|---|---|---|
| Hình 4.1a–b | Cơ cấu/Pareto, mục 4.2.1 | `01_co_cau_loi.png`; `02_pareto_loi.png` |
| Hình 4.2a–b | Theo dòng thép, mục 4.2.2 | `03_loi_theo_thep_so_luong.png`; `04_loi_theo_thep_ty_trong.png` |
| Hình 4.3 | Độ sáng, mục 4.2.3 | `05_scatter_do_sang.png` |
| Hình 4.4 | Độ dày, mục 4.2.4 | `06_boxplot_do_day.png` |
| Hình 4.5 | Diện tích, mục 4.2.5 | `07_boxplot_dien_tich_log.png` |
| Hình D.1a–b | Thương mại, Phụ lục D | `08_xuat_nhap_khau.png`; `09_chenh_lech_thuong_mai.png` |

Hình 3.1–3.2 và ảnh dashboard 4.6–4.7 cần chuẩn bị từ quy trình/ứng dụng thực tế. Kế hoạch subplot chưa đồng nghĩa đã tạo ảnh mới. Đồng bộ tiêu đề/chú thích vì các ảnh hiện tại còn dùng số hình cũ; ưu tiên dựng lại từ mã để chữ rõ.

### Điều chỉnh bản Chương 1 LaTeX đã viết

Bản hiện tại `latex/chuong/chuong1.tex` có tên “Giới thiệu đề tài và cơ sở lý thuyết”. Để khớp đề cương mới, lần viết tiếp theo cần:

- Chuyển lý do lựa chọn, mục tiêu/câu hỏi và phạm vi sang **Phần mở đầu**.
- Giữ và tổ chức lại phần lý thuyết thành **Chương 1. Tổng quan bài toán và cơ sở lý thuyết**.
- Chuyển giới thiệu vai trò công cụ sang **2.3**; giữ đoạn tài liệu liên quan phù hợp ở **1.1.2**.
- Cập nhật các dẫn chiếu, số chương, số hình/bảng và mục lục theo cấu trúc mới.

Đây là yêu cầu đồng bộ cho bước viết LaTeX tiếp theo. Lần chỉnh đề cương này chưa thay đổi mã LaTeX hoặc PDF đã biên dịch.

### Những việc cần hoàn thiện và kiểm tra mạch bài

Notebook đối chiếu: `buoc_1_2_3_4_5_6_loi_be_mat_thep.ipynb`. Cấu trúc báo cáo có thể khác thứ tự ô mã. Không ghi một thao tác dự kiến thành kết quả đã thực hiện.

Phép kiểm tra Q0 bổ sung có minh chứng ở `outputs/ra_soat_de_cuong/`: `q0_kiem_tra_truoc_tham_chieu.csv`, `q0_o_vi_pham_quan_he_noi_tai.csv`, `q0_tom_tat_ra_soat.json`, `kiem_tra_q0_truoc_tham_chieu.py`. Cần ghi rõ nguồn bổ sung hoặc tích hợp vào trước khôi phục trong notebook.

Chọn mã minh họa; chuẩn bị sơ đồ; tạo subplot nếu phù hợp; chụp dashboard; ghi ngày/môi trường kiểm thử. Với mỗi mục, kiểm tra: kiến thức Chương 1 có được dùng; vấn đề Chương 2 có thao tác Chương 3; đầu ra Chương 3 có minh chứng Chương 4; câu trả lời và kết luận có đúng mẫu số/phạm vi hay không.

**Phạm vi thay đổi lần này:** chỉnh đề cương và kế hoạch bố trí nội dung theo khung mẫu; không thay đổi notebook, dữ liệu, ứng dụng hoặc bản LaTeX hiện tại.
