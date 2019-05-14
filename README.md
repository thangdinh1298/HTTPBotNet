# Báo cáo bài tập lớn môn an toàn bảo mật hệ thống thông tin
## I. Sơ lược về hai kiểu tấn công.
1. Tấn công DoS Slow loris (SL).

- Nguyên tắc hoạt động: SL hoạt động bằng cách tạo nhiều hơn số connection mà một server có thể
xử lý. Với mỗi connection, kẻ tấn công sẽ gửi đi một phần của header sau mỗi khoảng thời gian chờ ngắn để không bị server 
chấm dứt connection đó. Nếu số lượng connection kẻ tấn công tạo được lớn hơn hoặc bằng số connection mà server có thể xử lý
thì hắn sẽ thành công trong việc ngăn không cho những người dùng khác connect đến server. SL hoạt động đặc biệt hiệu quả với
những server xử lý request bằng cách tạo ra một thread mới (threaded servers). Lý do là vì những server này thường sẽ giới hạn
số lượng thread được tạo ra để xử lý các request. Điều này cũng dễ hiểu vì khi có quá nhiều thread được tạo ra trên một máy tính
thì thời gian đáp ứng của hệ thống sẽ tương đối thấp. Để giải quyết vấn đề này có thể giảm lượng tử thời gian xuống. Nhưng
 nếu làm vậy có nguy cơ khiến tốc độ của hệ thống chậm do lượng tử quá bé không đáng công bỏ ra để bảo lưu và khôi phục bối cảnh
- Đặc điểm: Khác với những kiểu tấn công DoS trước nó, SL sử dụng tương đối ít tài nguyên. Tuy nhiên không vì vậy mà tính hiệu quả nó kém
.Thậm chí, khi những biện pháp đối phó với nó chưa ra đời, kẻ tấn công có thể sử dụng máy tính cá nhân để tấn công thành công một server cỡ vừa

2. Botnet

- Là hệ thống các máy tính bị nhiễm phần mềm độc hại và chịu sự điều khiển âm thầm của máy tính khác mà không bị phát hiện bởi
người sở hữu máy tính đó.
- Tổng quan về kiến trúc của botnet trong project này gồm 2 phần: một C&C server và các máy bị nhiễm. Tập các lệnh khả dụng được
định nghĩa sẵn trong code của C&C server. Kẻ điều khiển sẽ gửi lệnh đến C&C server bằng cách gửi các POST request, C&C server nhận lệnh và chuyển cho các máy bị nhiễm mỗi khi được hỏi.
Các máy bị nhiễm liên tục hỏi server xem lệnh tiếp theo cần thực hiện sau mỗi 5 giây và thực hiện chúng

## II. Tập chức năng khả dụng.
- Các chức năng được xây dựng cho hệ thống botnet này gồm có:
    + Lệnh chờ, máy nạn nhân không làm gì cả (Standby)
    + Thay đổi thư mục hiện tại (cd)
    + In đường dẫn của thư mục hiện tại (pwd)
    + Liệt kê danh sách file ở đường dẫn (ls)
    + upload file lên C&C server
    + Thực hiện tấn công DDoS lên một máy chủ
    + Thực hiện một lệnh command bất kỳ (runcmd)

- Các lệnh cd, pwd, ls thực chất sử dụng thư viện os của python nên tương thích với cả hệ điều hành windows và linux
- Runcmd không sử dụng thư viện hệ thống của python nên người ra lệnh sẽ phải định dạng lệnh phù hợp với hệ điều hành
- Thực hiện DDoS sẽ tải script slowLoris.py từ server về và thực hiện tấn công vào một máy chủ đã định

