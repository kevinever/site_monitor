from cmath import nan
from email import message
from urllib import response
import requests
import bs4
import smtplib
import os
import pandas as pd 
# from email.message import EmailMessage

EMAIL_ADDRESS = "kalisadoe@gmail.com"
EMAIL_PASSWORD = "wozdspsvmljvrery"
TO_ADDR = ['nyayihakevin@gmail.com','kalisadoe@gmail.com','gashemasteven89@gmail.com']

def sendmail():
     s =    smtplib.SMTP('smtp.gmail.com',587)
     s.starttls()
     s.login(EMAIL_ADDRESS,EMAIL_PASSWORD )
    #  msg = EmailMessage()
     Subject = 'website defaced'
    #  From =  EMAIL_ADDRESS
     body = df
     message = f'Subject : {Subject} \n\n {body}'
     s.sendmail(EMAIL_ADDRESS,TO_ADDR,message)
     s.quit()



df = pd.read_excel("/Users/kevinnyayiha/Desktop/site_monitor/sites.xlsx")
for index,websites in df.iterrows():
    try:
        response = requests.get(websites['names'],timeout=5)
        status = response.status_code
        df.at[index,'status_code'] = f'website is still on status code is {status}'
        # print(response.status_code)
        if response.status_code == 200:
            sendmail()
        # elif response.status_code == NAN:
        #     df.at[index,'status_code'] = f'website is still on status code is {status}'

        soup = bs4.BeautifulSoup(response.text,'html.parser')
        elems = soup.select('#gradient')
        if elems[0].text != 'Simple solutions for complex connections!':
            df.at[index,'status_code'] = 'site content has been changed'
            sendmail()
    except Exception as e:
        # df.at[index,'status_code'] = 'site is not availabe'
        sendmail()

print(df)