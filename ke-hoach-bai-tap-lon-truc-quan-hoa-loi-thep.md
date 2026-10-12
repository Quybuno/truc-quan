# Kế hoạch bài tập lớn môn Trực quan hóa dữ liệu

**Đề tài: Trực quan hóa và phân tích dữ liệu lỗi bề mặt trong dây chuyền sản xuất thép**

Bài tiểu luận tổ chức thành **6 chương tương ứng với 6 bước của hướng dẫn**, sử dụng báo cáo có sẵn làm tài liệu nền và thực hiện lại quy trình bằng Python.

## Tài liệu nền và nguyên tắc sử dụng

- Khung yêu cầu: `Bài tập lơn trực quan hóa dữ liệu.pdf`, tại `C:/Users/Admin/Downloads/Bài tập lơn trực quan hóa dữ liệu.pdf`.
- Báo cáo tham khảo: `[Reading]-Data-Analytics-in-Manufacturing.pdf`, tại `C:/Users/Admin/Downloads/[Reading]-Data-Analytics-in-Manufacturing.pdf`.
- Các số liệu của báo cáo mẫu dùng làm **mốc đối chiếu**; số liệu trong bài nộp phải được tính lại từ chương trình của người thực hiện.
- Kế hoạch này là đề xuất triển khai; chưa phải kết quả thực nghiệm hay báo cáo đã chạy trên dữ liệu.

## Cách chuyển báo cáo mẫu sang khung bài tập

| Bước của hướng dẫn | Nội dung lấy làm nền từ báo cáo mẫu | Phần cần thực hiện trong bài |
|---|---|---|
| 1. Xác định yêu cầu | Mục I–V, trang 4–20 | Chốt mục tiêu, câu hỏi, phạm vi và đầu ra |
| 2. Thu thập dữ liệu | Mục IV, trang 14–18; nguồn ở trang 51 | Đọc CSV/Excel, lấy bản gốc qua UCI API và dữ liệu bổ sung qua UN Comtrade |
| 3. Làm sạch và kết hợp | Mục VI.1, trang 21–33 | Thực hiện bằng Pandas/NumPy; ghi nhật ký xử lý và kiểm chứng |
| 4. Tạo cột và chỉ số mới | Mục VI.2, trang 33; các chỉ số ở mục VII | Tạo biến phân tích và bảng tổng hợp bằng Pandas |
| 5. Vẽ đồ thị bằng Python | Mục VII, trang 34–44; nhận định ở trang 47–50 | Vẽ lại, phân tích và viết kết luận từ kết quả tự chạy |
| 6. Dashboard tự động | Mục VIII, trang 45–46 | Xây dựng Streamlit + Plotly, có bộ lọc và cơ chế đọc lại dữ liệu |

Phần API bổ sung được đề xuất sử dụng **UN Comtrade cho bối cảnh thương mại sắt thép**. Phân tích lỗi vẫn là trọng tâm của đề tài.

---

## 1. Xác định yêu cầu

*Công cụ theo hướng dẫn: Word hoặc Google Docs.*

### 1.1. Viết phần giới thiệu đề tài

Phần này cần trả lời ba vấn đề:

- Vì sao dữ liệu lỗi bề mặt có ý nghĩa trong kiểm soát chất lượng sản xuất thép?
- Vì sao cần trực quan hóa thay vì chỉ xem bảng dữ liệu?
- Bài làm sẽ giúp người đọc hiểu được những đặc điểm nào của tập lỗi?

Có thể triển khai theo trình tự: bối cảnh chất lượng bề mặt thép → nhu cầu hiểu cơ cấu và đặc điểm lỗi → vai trò của Python và dashboard.

Tham khảo bối cảnh trong báo cáo mẫu, nhưng phân biệt rõ **bối cảnh chung của ngành** với **thông tin đã được xác nhận về bộ dữ liệu**.

### 1.2. Xác định mục tiêu

Đặt bốn mục tiêu cụ thể:

1. Thu thập, kiểm tra và làm sạch dữ liệu lỗi thép.
2. Phân tích cơ cấu lỗi và mối liên hệ giữa loại lỗi với dòng thép, độ sáng, độ dày và diện tích.
3. Xây dựng biểu đồ có khả năng trả lời các câu hỏi phân tích.
4. Xây dựng dashboard tương tác, có chức năng cập nhật dữ liệu và phần bối cảnh ngành lấy từ API ngoài.

### 1.3. Chốt câu hỏi phân tích

| Mã | Câu hỏi | Dữ liệu sử dụng | Cách trả lời |
|---|---|---|---|
| Q0 | Dữ liệu có đủ tin cậy để phân tích không? | Dữ liệu thực hành và bản UCI | Kiểm tra thiếu, trùng, nhãn, kiểu dữ liệu và đối chiếu |
| Q1 | Bảy loại lỗi phân bố như thế nào? | Nhãn lỗi | Số lượng, tỷ trọng, tỷ trọng lũy kế |
| Q2 | Cơ cấu lỗi khác nhau thế nào giữa A300 và A400? | Nhãn lỗi, dòng thép | Bảng chéo, số lượng và tỷ trọng |
| Q3 | Độ sáng có giúp phân biệt các loại lỗi không? | Độ sáng nhỏ nhất/lớn nhất, nhãn | Scatter plot, tương quan và thống kê theo nhóm |
| Q4 | Phân bố độ dày khác nhau thế nào giữa các loại lỗi? | Độ dày, nhãn, dòng thép | Boxplot và thống kê mô tả |
| Q5 | Diện tích vết lỗi khác nhau thế nào giữa các loại lỗi? | Diện tích, nhãn | Boxplot, trung vị và phân bố |
| Q6 | Xuất nhập khẩu sắt thép Việt Nam thay đổi thế nào qua các năm? | UN Comtrade | Biểu đồ thời gian và chênh lệch xuất nhập khẩu |

Q1–Q4 bám sát ba trục phân tích chính của báo cáo mẫu. Q5 bổ sung một góc nhìn trực quan từ dữ liệu sẵn có. Q6 là phần bối cảnh ngành, không dùng để giải thích nguyên nhân của các lỗi trong UCI.

### 1.4. Xác định phạm vi

Ghi rõ trong tiểu luận:

- Đơn vị phân tích là **bản ghi được gán nhãn lỗi**, không mặc định là một tấm thép.
- Không tính tỷ lệ sản phẩm bị lỗi vì không có tổng sản lượng.
- Không kết luận nguyên nhân từ các mối liên hệ quan sát được.
- `Production_Date` là ngày mô phỏng, không dùng để phân tích xu hướng sản xuất thực tế.
- Không tự gắn đơn vị đo cho những biến nguồn chưa công bố đơn vị.
- Số liệu thương mại quốc gia được phân tích ở phạm vi riêng.

### 1.5. Nội dung viết trong Chương 1

- 1.1. Lý do chọn đề tài.
- 1.2. Mục tiêu nghiên cứu.
- 1.3. Câu hỏi phân tích.
- 1.4. Đối tượng và phạm vi dữ liệu.
- 1.5. Công cụ và quy trình thực hiện.
- 1.6. Sản phẩm dự kiến.

**Đầu ra:** phần mô tả đề tài, bảng câu hỏi và danh sách sản phẩm.

**Điều kiện hoàn thành:** mỗi câu hỏi đều có dữ liệu, phương pháp và đầu ra để trả lời.

---

## 2. Thu thập dữ liệu

*Công cụ theo hướng dẫn: Python.*

### 2.1. Xác định ba nguồn đầu vào

| Nguồn | Vai trò | Cách lấy |
|---|---|---|
| File CSV/Excel thực hành | Đầu vào để làm sạch và phân tích | Đọc file bằng Pandas |
| Bản gốc Steel Plates Faults | Đối chiếu và khôi phục giá trị | UCI API và file dữ liệu được API chỉ tới |
| UN Comtrade | Bổ sung bối cảnh ngành sắt thép | Gọi API trả về JSON |

Nếu CSV ban đầu được xuất từ Excel thực hành, giữ lại cả Excel gốc và ghi rõ cách chuyển đổi. Nếu CSV là bản sạch tải trực tiếp từ UCI, cần kiểm tra trước: các lỗi trong báo cáo mẫu có thể không tồn tại ở file đó.

### 2.2. Thu thập dữ liệu thực hành

Thực hiện các công việc:

- Đọc file bằng Pandas; với Excel, chọn sheet `Faults`.
- Kiểm tra dấu phân cách và mã hóa nếu sử dụng CSV.
- Ghi số dòng, số cột, tên cột và kiểu dữ liệu.
- Hiển thị một số dòng đầu để kiểm tra cấu trúc.
- Lưu bản đầu vào nguyên trạng.
- Tạo cột chỉ vị trí dòng nguồn để truy lại các trường hợp cần sửa.

Không làm sạch ngay trong bước thu thập.

### 2.3. Thu thập dữ liệu gốc từ UCI

Nguồn chính thức là [Steel Plates Faults trên UCI](https://archive.ics.uci.edu/dataset/198/steel+plates+faults), gồm 1.941 bản ghi, 27 đặc trưng và 7 nhãn lỗi.

Quy trình dự kiến:

1. Gọi [UCI API cho bộ dữ liệu 198](https://archive.ics.uci.edu/api/dataset?id=198).
2. Đọc thông tin nguồn và đường dẫn `data_url`.
3. Tải dữ liệu dạng bảng từ đường dẫn đó.
4. Kiểm tra cấu trúc và lưu một bản dùng để đối chiếu.
5. Chuyển 7 cột nhãn nhị phân thành một cột nhãn văn bản, sau khi xác nhận mỗi dòng có đúng một nhãn được kích hoạt.

### 2.4. Thu thập dữ liệu UN Comtrade

Đề xuất phạm vi ban đầu:

- Quốc gia báo cáo: Việt Nam.
- Nhóm hàng: HS 72 — sắt và thép.
- Đối tác: toàn thế giới.
- Luồng thương mại: xuất khẩu và nhập khẩu.
- Tần suất: năm.
- Khoảng thời gian dự kiến: 2015–2024, kiểm tra mức độ sẵn có trước khi chốt.

API Preview có thể sử dụng không cần tài khoản hoặc API key, nhưng có giới hạn truy cập. [Tài liệu UN Comtrade](https://uncomtrade.org/docs/un-comtrade-api/).

Ví dụ truy vấn: [xuất khẩu sắt thép Việt Nam năm 2023](https://comtradeapi.un.org/public/v1/preview/C/A/HS?reporterCode=704&period=2023&cmdCode=72&flowCode=X&partnerCode=0&maxRecords=500).

Khi thu thập cần:

- Lưu JSON gốc.
- Ghi tham số và thời điểm gọi.
- Kiểm tra trạng thái phản hồi.
- Phân biệt truy vấn không có dữ liệu với lỗi kết nối.
- Kiểm tra kết quả có bị giới hạn số bản ghi hay không.
- Tạo bảng dữ liệu từ phần kết quả trong JSON.

### 2.5. Lập hồ sơ nguồn

Mỗi nguồn cần có: tên, đơn vị công bố, URL, ngày lấy, định dạng, quy mô, phạm vi thời gian và mục đích sử dụng.

### 2.6. Nội dung viết trong Chương 2

- 2.1. Tổng quan các nguồn dữ liệu.
- 2.2. Thu thập dữ liệu từ file.
- 2.3. Thu thập và đọc dữ liệu UCI.
- 2.4. Thu thập dữ liệu UN Comtrade.
- 2.5. Mô tả cấu trúc dữ liệu ban đầu.
- 2.6. Khả năng kết hợp giữa các nguồn.

**Đầu ra:** dữ liệu thô, JSON API, bảng hồ sơ nguồn và phần thu thập trong notebook.

**Điều kiện hoàn thành:** đọc được dữ liệu bằng Python và truy được nguồn của từng bảng.

---

## 3. Làm sạch và kết hợp dữ liệu

*Công cụ theo hướng dẫn: Pandas/NumPy.*

Đây là phần cần trình bày rõ nhất về phương pháp. Mỗi thao tác phải có **vấn đề → cách xử lý → bằng chứng kiểm tra**.

### 3.1. Khảo sát chất lượng trước xử lý

Tạo bảng kiểm kê:

| Hạng mục | Nội dung kiểm tra |
|---|---|
| Cấu trúc | Số dòng, số cột, tên cột |
| Kiểu dữ liệu | Các cột số bị đọc thành chuỗi |
| Nhãn | Danh sách và tần suất nhãn lỗi |
| Dữ liệu thiếu | Số ô thiếu theo cột |
| Trùng lặp | Số bản ghi trùng theo tiêu chí được xác định |
| Miền giá trị | Giá trị âm, cực lớn hoặc không hợp lệ |
| Ngày | Định dạng và các trường hợp mơ hồ |

### 3.2. Chuẩn hóa nhãn lỗi

- Giữ nguyên nhãn thô.
- Loại khoảng trắng và ký tự thừa.
- Tạo khóa đối chiếu để xử lý khác biệt chữ hoa/thường, dấu phân cách.
- Lập bảng ánh xạ các biến thể về 7 nhãn chuẩn.
- Tạo `Fault_Type_Clean`.
- Liệt kê nhãn chưa ánh xạ được để kiểm tra riêng.

Giữ tên nhãn chính thức `K_Scatch` khi đối chiếu với UCI. Không tự đổi nhãn chỉ vì tên trông giống lỗi chính tả.

### 3.3. Kiểm tra và loại bản ghi trùng

Bám theo báo cáo mẫu: so sánh các trường dữ liệu và nhãn đã chuẩn hóa, loại nhãn thô khỏi tiêu chí so sánh.

Không chỉ dựa vào số thứ tự dòng. Với các trường hợp cùng tọa độ nhưng khác giá trị, phải kiểm tra trước khi quyết định loại.

Lưu danh sách dòng bị loại và dòng được giữ lại tương ứng.

### 3.4. Ghép với dữ liệu UCI

Khóa dự kiến:

`X_Minimum + X_Maximum + Y_Minimum + Y_Maximum`

Trước khi ghép:

1. Xác nhận bốn cột khóa không thiếu.
2. Kiểm tra tính duy nhất ở hai bảng sau khi xử lý trùng.
3. Kiểm tra kiểu dữ liệu của khóa tương thích.
4. Ghép với điều kiện quan hệ một–một.
5. Đếm số dòng khớp, không khớp và số dòng sau ghép.

Không lấy giá trị từ nguồn đối chiếu cho những dòng chưa xác định được ghép đúng.

### 3.5. Khôi phục ô thiếu và kiểm tra giá trị sai

Ưu tiên lấy giá trị từ bản gốc đối với bản ghi đã ghép chắc chắn.

Với các cột phái sinh, có thể tính lại để kiểm chứng thêm. Công thức được suy ra trong báo cáo mẫu cần tiếp tục đối chiếu với UCI, không mặc định là định nghĩa chính thức.

Đặc biệt, không điền độ dày bằng giá trị dòng phía trên hoặc trung bình chỉ để làm hết ô trống khi đã có bản gốc để khôi phục.

### 3.6. Chuẩn hóa ngày và kiểu dữ liệu

- Chuyển cột số sang kiểu số.
- Ghi lại những giá trị chuyển đổi thất bại.
- Xử lý ngày theo định dạng đã xác định.
- Không để phần mềm tự quyết định ngày/tháng đối với chuỗi mơ hồ.
- Đánh dấu rõ ngày mô phỏng trong từ điển dữ liệu.

### 3.7. Kiểm tra logic và ngoại lai

Kiểm tra tối thiểu:

- `X_Maximum ≥ X_Minimum`.
- `Y_Maximum ≥ Y_Minimum`.
- Diện tích hợp lệ và dương.
- Độ sáng lớn nhất không nhỏ hơn độ sáng nhỏ nhất.
- Hai cờ A300/A400 chỉ nhận 0 hoặc 1 và có tổ hợp phù hợp.
- Các chỉ số phái sinh khớp với nguồn đối chiếu.

Áp dụng quy tắc IQR để **gắn cờ** diện tích lớn. Không tự động xóa các giá trị này nếu chúng có trong bản UCI.

### 3.8. Đối chiếu với các mốc trong báo cáo mẫu

| Hạng mục | Mốc tham khảo |
|---|---:|
| Dữ liệu thực hành ban đầu | 1.961 dòng |
| Bản ghi trùng bị loại | 20 |
| Dữ liệu sau làm sạch | 1.941 dòng |
| Số loại lỗi chuẩn | 7 |
| Ô thiếu sau loại trùng | 67 |
| Giá trị sai được báo cáo ở các cột phái sinh | 16 |

Các mốc này chỉ áp dụng nếu sử dụng đúng phiên bản thực hành. Nếu kết quả khác, kiểm tra nguồn và quy trình; không điều chỉnh dữ liệu để ép khớp.

### 3.9. Làm sạch và kết hợp dữ liệu thương mại

- Giữ mã quốc gia, năm, mã hàng, luồng thương mại, phân loại và giá trị USD.
- Kiểm tra bản ghi trùng và phạm vi tổng hợp.
- Phân biệt thiếu dữ liệu với giá trị bằng 0.
- Chọn cùng phạm vi quốc gia, nhóm hàng, đối tác và tần suất.
- Đưa xuất khẩu và nhập khẩu thành hai cột trong một bảng theo năm.
- Kiểm tra tính nhất quán của phân loại HS khi so sánh nhiều năm.

**Hai phép kết hợp cần thể hiện trong bài:**

| Phép kết hợp | Mục đích |
|---|---|
| Dữ liệu lỗi thực hành ↔ UCI | Đối chiếu và khôi phục |
| Xuất khẩu ↔ nhập khẩu UN Comtrade | Tạo bảng thương mại theo năm |

Không ghép số liệu thương mại quốc gia vào từng vết lỗi vì hai nguồn không có khóa liên hệ được xác nhận.

### 3.10. Nội dung viết trong Chương 3

- 3.1. Khảo sát chất lượng dữ liệu.
- 3.2. Chuẩn hóa nhãn và kiểu dữ liệu.
- 3.3. Xử lý trùng.
- 3.4. Ghép và đối chiếu với UCI.
- 3.5. Khôi phục dữ liệu thiếu, sửa giá trị sai.
- 3.6. Kiểm tra ngày, logic và ngoại lai.
- 3.7. Làm sạch và kết hợp dữ liệu API.
- 3.8. Đánh giá dữ liệu sau xử lý.

**Đầu ra:** hai bảng sạch, nhật ký thay đổi, bảng trước/sau xử lý và kết quả đối chiếu.

**Điều kiện hoàn thành:** các vấn đề còn tồn tại đều được xác định rõ; số dòng sau ghép không tăng ngoài dự kiến; dữ liệu phân tích có thể kiểm chứng.

---

## 4. Tạo cột và chỉ số mới

*Công cụ theo hướng dẫn: Pandas.*

### 4.1. Tạo biến phục vụ phân tích lỗi

| Biến mới | Cách xác định | Mục đích |
|---|---|---|
| `Fault_Type_Clean` | Nhãn đã chuẩn hóa | Phân nhóm lỗi |
| `Steel_Type` | Suy ra A300/A400 từ cờ loại thép | So sánh dòng thép |
| `X_Range` | `X_Maximum − X_Minimum` | Kích thước theo trục X |
| `Y_Range` | `Y_Maximum − Y_Minimum` | Kích thước theo trục Y |
| `Luminosity_Range` | Độ sáng lớn nhất − nhỏ nhất | Khoảng biến thiên độ sáng |
| `Log_Pixels_Areas` | Logarit cơ số 10 của diện tích dương | Hiển thị dữ liệu lệch mạnh |
| `Area_Outlier_Flag` | Cờ theo quy tắc IQR | Theo dõi giá trị lớn cần xem xét |

Không cần tạo quá nhiều cột nếu chúng không phục vụ câu hỏi hoặc việc kiểm tra dữ liệu.

### 4.2. Tạo bảng chỉ số tổng hợp

Chuẩn bị bốn bảng:

- **Cơ cấu lỗi:** số lượng, tỷ trọng, tỷ trọng lũy kế theo loại lỗi.
- **Loại lỗi × dòng thép:** số lượng và tỷ trọng theo từng nhóm.
- **Đặc điểm theo nhãn:** cỡ mẫu, trung bình, trung vị, độ lệch chuẩn, Q1, Q3, min và max.
- **Thương mại theo năm:** xuất khẩu, nhập khẩu, chênh lệch và mức thay đổi so với năm trước.

Phải phân biệt hai mẫu số trong phân tích dòng thép:

- Tỷ trọng một loại lỗi **trong toàn bộ lỗi của A300/A400**.
- Tỷ trọng A300/A400 **trong một loại lỗi cụ thể**.

Hai chỉ số này trả lời hai câu hỏi khác nhau.

### 4.3. Tạo chỉ số thương mại

- Chênh lệch thương mại = xuất khẩu − nhập khẩu.
- Thay đổi năm sau so với năm trước = giá trị năm sau − giá trị năm trước.
- Tăng trưởng năm = thay đổi / giá trị năm trước × 100%.

Nếu năm trước thiếu dữ liệu hoặc bằng 0, không tính tỷ lệ tăng trưởng theo công thức thông thường; hiển thị là chưa xác định.

### 4.4. Nội dung viết trong Chương 4

- 4.1. Lý do bổ sung biến và chỉ số.
- 4.2. Công thức tạo biến.
- 4.3. Các bảng tổng hợp phục vụ phân tích.
- 4.4. Cách xác định mẫu số và xử lý trường hợp đặc biệt.
- 4.5. Kiểm tra kết quả tính toán.

**Đầu ra:** dữ liệu sẵn sàng trực quan hóa, bảng tổng hợp và từ điển biến mới.

**Điều kiện hoàn thành:** mỗi biến có cách tính và cách sử dụng; tổng các nhóm khớp tổng dữ liệu; tỷ trọng trong từng phạm vi cộng lại khoảng 100%.

---

## 5. Vẽ đồ thị bằng Python và phân tích kết quả

*Công cụ theo hướng dẫn: Matplotlib/Seaborn/Plotly.*

Đề xuất dùng Plotly cho dashboard và xuất các hình cần thiết cho tiểu luận.

### 5.1. Danh mục biểu đồ

| Hình | Biểu đồ | Câu hỏi phục vụ | Nội dung phân tích |
|---|---|---|---|
| 1 | Thanh ngang cơ cấu lỗi | Q1 | Nhãn lớn nhất, nhỏ nhất và mức mất cân bằng |
| 2 | Pareto số lượng và tỷ trọng lũy kế | Q1 | Một số nhóm chiếm bao nhiêu phần trăm mẫu |
| 3 | Cột nhóm theo loại lỗi và dòng thép | Q2 | So sánh số lượng tuyệt đối |
| 4 | Cột chồng 100% theo dòng thép | Q2 | So sánh cơ cấu lỗi trong A300/A400 |
| 5 | Scatter độ sáng nhỏ nhất × lớn nhất | Q3 | Vùng phân bố, chồng lấn và nhóm tách biệt |
| 6 | Boxplot độ dày theo loại lỗi | Q4 | Trung vị, độ phân tán và giá trị lớn |
| 7 | Boxplot diện tích theo loại lỗi, dùng trục log phù hợp | Q5 | Khác biệt kích thước vết lỗi |
| 8 | Đường xuất khẩu/nhập khẩu theo năm | Q6 | Biến động thương mại sắt thép |
| 9 | Cột chênh lệch xuất nhập khẩu | Q6 | Những năm có chênh lệch dương hoặc âm |

Đây là danh mục đề xuất. Có thể đưa một số hình bổ sung vào phụ lục để phần chính không bị dàn trải.

### 5.2. Phân tích cơ cấu lỗi

Bám theo mục VII.1 của báo cáo mẫu:

- Tính số lượng và tỷ trọng.
- Sắp xếp giảm dần.
- Xác định nhóm chiếm tỷ trọng lớn.
- Phân tích sự mất cân bằng.
- Đọc Pareto như mức tập trung của số bản ghi, không coi đó là thứ tự thiệt hại kinh tế.

### 5.3. Phân tích dòng thép

- So sánh số lượng tuyệt đối bằng cột nhóm.
- So sánh tỷ trọng bằng cột chồng 100%.
- Ghi số bản ghi của mỗi dòng thép.
- Nhận diện loại lỗi tập trung vào một dòng thép.

Cách diễn giải phù hợp: “Nhóm lỗi này tập trung trên A400 trong mẫu quan sát”. Không chuyển thành “A400 dễ bị lỗi hơn” khi thiếu sản lượng làm mẫu số.

### 5.4. Phân tích độ sáng

Bám theo mục VII.2:

- Tính tương quan giữa độ sáng nhỏ nhất và lớn nhất.
- Vẽ scatter, màu theo nhãn.
- Giảm độ đậm của điểm để quan sát vùng chồng lấn.
- Tính trung vị và khoảng tứ phân vị theo loại lỗi.
- Nhận xét nhóm có vùng đặc trưng và nhóm còn chồng lấn.

Tương quan giữa hai biến độ sáng không tự chứng minh khả năng phân loại lỗi. Nếu thử quy tắc ngưỡng như báo cáo mẫu, đặt ở phần mở rộng và nói rõ đó là kết quả khám phá trên dữ liệu đã quan sát.

### 5.5. Phân tích độ dày và diện tích

Bám theo mục VII.3 và phần ngoại lai của báo cáo:

- So sánh trung vị và độ phân tán.
- Hiển thị cỡ mẫu.
- Tách theo dòng thép khi cần.
- Kiểm tra nhóm có ít bản ghi trước khi so sánh trung bình.
- Dùng trục log cho diện tích khi phân bố lệch mạnh và ghi rõ cách hiển thị.

### 5.6. Phân tích bối cảnh ngành từ API

- Chốt khoảng năm có dữ liệu phù hợp.
- Vẽ xuất khẩu, nhập khẩu và chênh lệch.
- Phân tích biến động trong phạm vi dữ liệu thương mại.
- Giải thích phần này cung cấp bối cảnh về ngành, không thể hiện kết quả của dây chuyền trong UCI.

### 5.7. Viết nhận xét cho từng hình

Mỗi nhận xét theo trình tự:

**Quan sát chính → con số hỗ trợ → ý nghĩa → giới hạn diễn giải.**

Ví dụ cấu trúc: nhóm nào chiếm nhiều nhất; chiếm bao nhiêu phần trăm; điều đó cho thấy cơ cấu tập dữ liệu ra sao; dữ liệu chưa cho phép kết luận điều gì.

Không sao chép kết luận của báo cáo mẫu trước khi có kết quả tính lại.

### 5.8. Nội dung viết trong Chương 5

- 5.1. Nguyên tắc lựa chọn và thiết kế biểu đồ.
- 5.2. Phân tích cơ cấu lỗi.
- 5.3. So sánh theo dòng thép.
- 5.4. Phân tích đặc trưng độ sáng.
- 5.5. Phân tích độ dày và diện tích.
- 5.6. Bối cảnh thương mại sắt thép.
- 5.7. Tổng hợp phát hiện và giới hạn.

**Đầu ra:** biểu đồ, bảng số liệu hỗ trợ và phần phân tích trả lời Q1–Q6.

**Điều kiện hoàn thành:** biểu đồ có tiêu đề, trục, chú giải, phạm vi dữ liệu; các nhận xét có bằng chứng; màu loại lỗi nhất quán giữa các hình.

---

## 6. Dashboard tự động

*Công cụ theo hướng dẫn: Streamlit + Plotly.*

### 6.1. Thiết kế ba tab

| Tab | Nội dung | Mục đích |
|---|---|---|
| Phân tích lỗi thép | KPI, cơ cấu lỗi, dòng thép, độ sáng, độ dày, diện tích | Trình bày kết quả chính |
| Bối cảnh ngành | Xuất nhập khẩu sắt thép theo năm | Sử dụng nguồn API bổ sung |
| Dữ liệu và chất lượng | Nguồn, bảng đã lọc, thống kê làm sạch, trạng thái đối chiếu | Giúp người đọc kiểm chứng |

### 6.2. Thiết kế tab phân tích lỗi

Bộ lọc:

- Dòng thép.
- Loại lỗi.
- Khoảng độ dày.
- Nút đặt lại bộ lọc.

Bốn KPI đề xuất:

- Tổng số bản ghi đang được chọn.
- Số loại lỗi đang xuất hiện.
- Trung vị diện tích.
- Trung vị độ dày.

Biểu đồ cập nhật theo bộ lọc. Hiển thị cả số bản ghi đã chọn và tổng dữ liệu để người đọc biết phạm vi đang xem.

Không cần dùng ngày mô phỏng làm bộ lọc chính. Nếu giữ để minh họa kỹ thuật, phải gắn nhãn rõ.

### 6.3. Thiết kế tab bối cảnh ngành

- Chọn khoảng năm.
- Hiển thị phạm vi Việt Nam, HS 72, đối tác toàn thế giới.
- KPI xuất khẩu, nhập khẩu và chênh lệch của năm đang chọn.
- Biểu đồ đường và biểu đồ chênh lệch.
- Thời điểm lấy dữ liệu gần nhất.
- Thông báo nếu thiếu một số năm.

Các bộ lọc loại lỗi hoặc dòng thép không được tác động đến số liệu thương mại.

### 6.4. Thiết kế tab chất lượng dữ liệu

Hiển thị:

- Quy mô đầu vào và sau làm sạch.
- Số dòng trùng đã loại.
- Số giá trị đã khôi phục hoặc sửa.
- Số dòng chưa ghép được với UCI.
- Kết quả đối chiếu.
- Bảng dữ liệu đang lọc.
- Chức năng tải CSV.

### 6.5. Xây dựng luồng cập nhật

Quy trình chung:

**Đọc nguồn → kiểm tra → làm sạch → tạo biến → tổng hợp → áp dụng bộ lọc → tính KPI → hiển thị.**

Notebook và dashboard dùng chung phần xử lý để hạn chế khác biệt giữa báo cáo và ứng dụng.

Cơ chế cập nhật dự kiến:

- Nút **“Làm mới dữ liệu”** để đọc lại nguồn.
- Tự đọc lại định kỳ, đề xuất mỗi 5 phút khi phiên dashboard đang hoạt động.
- Có bộ nhớ đệm để hạn chế gọi API lặp lại.
- Khi làm mới, bảo đảm thực sự đọc lại nguồn thay vì chỉ vẽ lại dữ liệu cũ.
- Chỉ thay thế dữ liệu đang hiển thị sau khi bản mới qua kiểm tra.

Streamlit hỗ trợ chạy lại một phần ứng dụng theo chu kỳ bằng `st.fragment(run_every=...)` trong phiên đang hoạt động. [Tài liệu Streamlit](https://docs.streamlit.io/develop/api-reference/execution-flow/st.fragment).

Dữ liệu UCI là bộ dữ liệu tĩnh; chức năng này chứng minh khả năng đọc lại và cập nhật, không có nghĩa các vết lỗi mới sẽ được phát sinh liên tục.

### 6.6. Kiểm tra dashboard

| Tình huống | Kết quả cần đạt |
|---|---|
| Mở ứng dụng lần đầu | Dữ liệu và biểu đồ hiển thị đúng |
| Chọn A300 hoặc A400 | KPI và biểu đồ cùng thay đổi |
| Chọn một loại lỗi | Bảng và biểu đồ phản ánh đúng tập con |
| Bộ lọc không có dữ liệu | Có thông báo, không chia cho 0 |
| API lỗi | Có thông báo và thời điểm của dữ liệu lưu gần nhất |
| Thay file đầu vào hợp lệ rồi làm mới | Kết quả phản ánh phiên bản mới |
| Đối chiếu notebook với dashboard | Cùng bộ lọc cho cùng kết quả |

### 6.7. Nội dung viết trong Chương 6

- 6.1. Mục tiêu và người sử dụng.
- 6.2. Kiến trúc xử lý dữ liệu.
- 6.3. Thiết kế giao diện và các tab.
- 6.4. Bộ lọc, KPI và biểu đồ.
- 6.5. Cơ chế cập nhật.
- 6.6. Kiểm tra ứng dụng.
- 6.7. Hướng dẫn sử dụng.

**Đầu ra:** ứng dụng Streamlit, ảnh dashboard, mã nguồn và hướng dẫn chạy.

**Điều kiện hoàn thành:** ứng dụng chạy được, bộ lọc hoạt động đồng bộ, cập nhật thực sự đọc lại dữ liệu và có cách xử lý khi nguồn lỗi.

---

## Cấu trúc bài tiểu luận để bắt đầu viết

Sau bìa, mục lục và danh mục hình/bảng, sử dụng đúng sáu chương trên. Cuối bài bổ sung:

- **Kết luận:** trả lời mục tiêu, tổng hợp những phát hiện có bằng chứng.
- **Giới hạn và hướng phát triển:** thiếu sản lượng, ngày thật, thông số vận hành; đề xuất dữ liệu cần bổ sung.
- **Tài liệu tham khảo:** báo cáo mẫu, UCI, UN Comtrade và tài liệu công cụ.
- **Phụ lục:** từ điển dữ liệu, bảng ánh xạ nhãn, nhật ký xử lý, bảng đối chiếu và hướng dẫn chạy.

Đề xuất khoảng **25–35 trang nội dung chính**, nhưng đây là gợi ý để cân đối bài viết; hình hướng dẫn chưa quy định số trang. Dành nhiều dung lượng nhất cho **Chương 3 và Chương 5**.

## Lịch triển khai đề xuất

| Giai đoạn | Thời lượng | Công việc và mốc hoàn thành |
|---|---:|---|
| Bước 1 | 1–2 buổi | Chốt đề tài, câu hỏi, phạm vi và cấu trúc báo cáo |
| Bước 2 | 2 buổi | Đọc file, lấy UCI và UN Comtrade, lưu nguồn |
| Bước 3 | 3–4 buổi | Làm sạch, ghép, đối chiếu; có bảng sạch và nhật ký |
| Bước 4 | 1–2 buổi | Tạo biến, chỉ số và bảng tổng hợp |
| Bước 5 | 3–4 buổi | Vẽ biểu đồ, phân tích và viết Chương 5 |
| Bước 6 | 3–4 buổi | Xây dashboard, cập nhật và kiểm tra |
| Hoàn thiện | 2 buổi | Chạy lại toàn bộ, chỉnh báo cáo, chuẩn bị trình bày |

Mỗi buổi có thể khoảng 2–3 giờ; điều chỉnh lịch theo thời gian còn lại trước hạn **tuần 10**. Nên viết từng chương ngay sau khi hoàn thành bước tương ứng.

## Bộ sản phẩm cần chuẩn bị để nộp

| Nhóm sản phẩm | Thành phần |
|---|---|
| Dữ liệu thô | File CSV/Excel đầu vào, bản UCI, JSON UN Comtrade |
| Dữ liệu sạch | Bảng lỗi thép sạch và bảng thương mại theo năm |
| Minh chứng xử lý | Nhật ký thay đổi, bảng trước/sau, kết quả đối chiếu |
| Phân tích Python | Notebook có thể chạy lại từ đầu đến cuối |
| Dashboard | Ứng dụng Streamlit và các thành phần xử lý dùng chung |
| Báo cáo | Word/PDF tổ chức theo 6 bước |
| Hướng dẫn | Thư viện cần cài, cách chạy và cách làm mới dữ liệu |

Điểm xuyên suốt của bài là: **tham khảo nội dung và phương pháp từ báo cáo mẫu, thực hiện lại bằng Python, rồi dùng kết quả tự tính để viết tiểu luận theo đúng sáu bước.**
