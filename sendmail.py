import os
import smtplib
from email.message import EmailMessage
import requests
import imghdr

# defining addresses with token

EMAIL_ADDRESS = "kalisadoe@gmail.com"
EMAIL_PASSWORD = "wozdspsvmljvrery"
TO_ADDR = ['nyayihakevin@gmail.com','kalisadoe@gmail.com','gashemasteven89@gmail.com']

# accessing websites 

websites = ['https://google.com','https://igihe.com']
for web in websites:
    r = requests.get(web,timeout=5)
    
message = f'web: {websites[0]} and {websites[1]} websites are now down pleas visit see what\'s happening to it   '
# print(message)


# sending email using smtp

msg = EmailMessage()
msg['Subject'] = 'website defaced'
msg['From'] =  EMAIL_ADDRESS
msg['To'] = ','.join(TO_ADDR)
msg.set_content (message)

# adding jpg attachments 
files = ['img.jpg','img2.jpg']
for file in files:
    with open(file, 'rb') as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f.name


    msg.add_attachment(file_data,maintype='image',subtype=file_type,filename = file_name )


# adding pdf files 

pdf_files = ['scanning.pdf']
for f in pdf_files:
    with open(f,'rb') as dpf:
        filedata = dpf.read()
        fname = dpf.name
        
    msg.add_attachment(filedata,maintype='application',subtype='octet-stream',filename = fname)


# adding html email files 

# msg.add_alternative("""\
    
#     <!Doctype html>
#     <html>
#         <body>
#             <h1 style = "color:SlateGray;">This is an html email</h1>
#         </body>

#     </html>
    
#      """, subtype="html")




# reading status code of the websites 
# and sending email 

if r.status_code == 200:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    # smtp.ehlo()
    # smtp.starttls()
    # smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    # subject = ""
    # body = "t"
    # msg = f'Subject: {subject} \n\n\n{body}'
        smtp.send_message(msg)

