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

- Lệnh Standby sẽ khiến Agent (Máy bị nhiễm) ngủ trong khoảng thời gian được định bởi người điều khiển. Trong quá trình ngủ, máy chủ và máy nạn nhân không có bất kỳ giao tiếp nào. 
- Các lệnh cd, pwd, ls thực chất sử dụng thư viện os của python nên tương thích với cả hệ điều hành windows và linux
- Runcmd không sử dụng thư viện hệ thống của python nên người ra lệnh sẽ phải định dạng lệnh phù hợp với hệ điều hành
- Thực hiện DDoS sẽ tải script slowLoris.py từ server về và thực hiện tấn công vào một máy chủ đã định

## III. Phương thức tấn công.
- Người điều khiển biết được địa chỉ của máy chủ sẽ gửi lệnh điều khiển tới máy chủ bằng một HTTP request (Có thể qua những tool như curl hoặc Postman). Máy chủ thực hiện đặt lệnh đó làm lệnh hiện thời để chuyển lại cho máy bị nhiễm. 

## IV. Cách sử dụng
- Chuyển CommandCenter.py lên một máy chủ đã được forward IP và chạy
- Chuyển Agent.py lên máy bị điều khiển, sửa IP và port thành IP và port của máy chủ mà trên đó CommandCenter chạy
- Chạy agent.py. Quan sát cửa sổ dòng lệnh của CommandCenter có kết quả trả về của lệnh được thực hiện hiện tại. Lệnh mặt định ban đầu là pwd (in ra đường dẫn tuyệt đối của thư mục hiện tại)
- Muốn điều khiển các Agent, thực hiện gửi POST request lên endpoint set_action của CommandCenter. Nội dung của request gồm lệnh muốn máy bị điều khiển thực hiện và một số thông tin khác tùy theo lệnh. Để gửi các request có thể dùng các tool như Postman (GUI) hay curl (CLI)
- Body của các request đều phải để dưới dạng json. Định dạng các lệnh: <br />
pwd <br />
{ <br />
	"command":"pwd", <br />
}

cd <br />
{ <br />
	"command":"cd", <br />
	"extra" : "/home/abcde" //duong dan den thu muc muon chuyen den <br />
}

ls <br />
{ <br />
	"command":"ls", <br />
	"extra" : "/home/abcde" //duong dan den thu muc muon liet ke file <br />
}

upload <br />
{ <br />
	"command":"upload", <br />
	"extra" : "abc.txt" //tên file muốn upload. File phải ở trong thư mục hiện tại <br />
}

Standby <br />
{ <br />
	"command":"Standby", <br />
	"extra" : "0.0012" //Khoảng thời gian standby (tính bằng giờ. 0.0012h = 5s) <br />
}

runcmd <br />
{ <br />
	"command":"runcmd", <br />
	"extra" : "ten command" //Lệnh muốn thực hiện trên terminal/cmd <br />
}

![Screenshot from 2019-05-21 23-09-43](https://user-images.githubusercontent.com/32330003/58112692-36194680-7c1e-11e9-8ef1-be3d8b95f62d.png)

