from curses import reset_prog_mode
from unicodedata import name
from urllib import request, response
import requests
import pandas as pd 
import smtplib
from email.message import EmailMessage


# defining addresses with token

EMAIL_ADDRESS = "kalisadoe@gmail.com"
EMAIL_PASSWORD = "drmpovaameczbgot"
TO_ADDR = ['nyayihakevin@gmail.com','kalisadoe@gmail.com','gashemasteven89@gmail.com']



df = pd.read_excel("/Users/kevinnyayiha/Desktop/site_monitor/sites.xlsx")
# print(websites)
for index,websites in df.iterrows():
    # print(index,websites['names'])
    try:
        response = requests.get(websites['names'])
        df.at[index,'status_code'] = 'site is still availabe'
        # print(response.status_code)
    except:
        # answer = 'website {} is not available'.format(websites['names'])
        df.at[index,'status_code'] = 'site is not availabe'

print(df)
