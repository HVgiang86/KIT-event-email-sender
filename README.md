# For Test:

- Bước 1: Truy cập https://myaccount.google.com/apppasswords . Tạo một mật khẩu cho ứng dụng "Thư", trên thiết bị Windows. COpy cái mật khẩu đó
- Bước 2: Sửa danh sách attendee trong file information.csv
- Bước 3: Run script. Nhập email của mình  (email sẽ gửi thư), mật khẩu là mật khẩu ứng dụng vừa tạo
- Bước 4: Kiểm tra email xem được chưa nhé


# For deployment

- Bước 1: Export danh sách đăng ký từ google form, sửa lại danh sách, chỉ giữ lại các trường: Họ tên, msv, email theo đúng format của file information.csv
- Bước 2: Custom nội dung email trong file content.html
- Bước 3: Đặt các text_holder trong file html, việc này nhằm truyền các tham số như tên, email của người nhận vào nội dung email. Đồng thời viết các hàm String Replace tương ứng
- Bước 4: Custom lại background của QR code trong file qrbackground.png
- Bước 5: Sửa tiêu đề email (sửa trong code, biến tên là subject)
- Bước 6: Chạy script để gửi mail