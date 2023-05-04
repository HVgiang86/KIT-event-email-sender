import qrcode
import json
import os
from PIL import Image
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

filename = "email_senders/input/information.csv"
attendees = []
count  = 0

# Tạo mã QR
def qrcodeGeneration(content,email):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    

    qr.add_data(content)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color='black', back_color='white')


    # Mở file hình ảnh nền
    img_bg = Image.open('email_senders/input/qrbackground.png')

    # Điều chỉnh kích thước của hình ảnh mã QR
    img_qr = img_qr.resize((300, 300))

    # Chèn hình ảnh mã QR vào hình nền
    pos = ((img_bg.width - img_qr.width) // 2, (img_bg.height - img_qr.height) // 2)
    img_bg.paste(img_qr, pos)

    qrcode_generated_path = "email_senders/qrcodegenerated/"

    isExist = os.path.exists(qrcode_generated_path)
    if not isExist:
        os.makedirs(qrcode_generated_path)
        print("QR generated folder created")

    # Lưu hình ảnh mới
    email = (email+"").replace('.','_')
    img_bg.save("email_senders/qrcodegenerated/"+(email+"").replace('.','_')+".png")


def CSVReader():
    with open(filename, "r", encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)  # Đọc tiêu đề cột đầu tiên
        for row in csvreader:
            mssv = row[0]
            hoten = row[1]
            email = row[2]
            print("MSSV: ", mssv, " - Họ tên: ", hoten, "Email: ", email)
            attendee = {
                "email": email,
                "name": hoten,
                "code": mssv
            }

            attendees.append(attendee)
            
            attendeeJSONObj = {
                "email": email,
                "code": mssv
            }
            attendeeJSON = json.dumps(attendeeJSONObj)
            qrcodeGeneration(attendeeJSON, email)

    
def sendEmail():

    recipient_emails = emails

    # Define email parameters
    print("Nhập Email: ")
    sender_email = input()
    print("Nhap Password")
    sender_password = input()
    subject = "Phản hồi đăng ký tham dự Techtalk"  #Nhập tên tiêu đề của thư tại đây
    # custom template tại đây
    
    html_file = open("email_senders/input/content.html", "r",encoding='utf-8')
    html = html_file.read()

    # Connect to Gmail's SMTP server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
    smtp_connection.starttls()
    smtp_connection.login(sender_email, sender_password)

    # Construct email message
    for attendee in attendees:
        
        email = attendee["email"]
        name = attendee["name"]
        code = attendee["code"]

        print("Sending email to {0}".format(email))
        
        #replace with our content
        html = html.replace("$$email_holder", name)

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = email
        message["Subject"] = subject
        message.attach(MIMEText(html, 'html'))

        attachment_path = "email_senders/qrcodegenerated/"+(email+"").replace('.','_')+".png"  

        # Attach attachment to message, if any
        if attachment_path:
            attachment = open(attachment_path, "rb")
            attachment_part = MIMEBase("application", "octet-stream")
            attachment_part.set_payload(attachment.read())
            encoders.encode_base64(attachment_part)
            attachment_part.add_header(
                "Content-Disposition", f"attachment; filename= {attachment_path.split('/')[-1]}"
            )
            message.attach(attachment_part)

        # Send email
        smtp_connection.sendmail(sender_email, email, message.as_string())
        
        count += 1

    # Close SMTP connection
    smtp_connection.quit()

print("START")
print("Reading cvs file ...")
CSVReader()
print("Created QRcode Successfully")
sendEmail()
print("Sent Email to ",count," attendees")
print("Sent Email Successfully")
print("END")
