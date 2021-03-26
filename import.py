#! python
import requests
import pandas
import smtplib
import os
import configparser
from bs4 import BeautifulSoup
from datetime import date, timedelta
from sys import exit
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

yesterday_date = str(date.today() - timedelta(days=1)).replace('-', '')
today_date = str(date.today()).replace('-', '')

yesterday_filename = 'oil_xls_' + yesterday_date + '.xlsx'
today_filename = 'oil_xls_' + today_date + '.xlsx'

if os.path.exists('import.ini'):
  config = configparser.RawConfigParser()
  config.read('import.ini')
  smtp_server_ip = config.get('main', 'smtp_server_ip')
  mail_from = config.get('main', 'mail_from')
  mail_to = config.get('main', 'mail_to')
else:
  smtp_server_ip = 'change_me_please'
  mail_from = 'mail@from.me'
  mail_to = 'rcpt@to.you'

if os.path.exists(yesterday_filename):
  os.remove(yesterday_filename)

if os.path.exists(today_filename):
  exit('File already have been processed today - stopping')

site = 'https://spimex.com/'

page_url = site + 'markets/oil_products/trades/results/'
req = requests.get(page_url, allow_redirects=True)
soup = BeautifulSoup(req.text, 'html.parser')

file_url = ''
links = soup.select("[class~=xls]")
for link in soup.find_all('a'):
  if today_date in str(link.get('href')):
    file_url = site + str(link.get('href'))

if file_url == '':
  exit('No link found on site - stopping (maybe later?)')

req = requests.get(file_url, allow_redirects=True)

with open(today_filename, 'wb') as dstfile: 
  dstfile.write(req.content) 

xl = pandas.ExcelFile(today_filename)

data_frame = xl.parse(xl.sheet_names[0])

basises = [
  'АО Антипинский НПЗ',
  'Пермь',
  'Самара-группа станций',
  'ст. Сургут', 
  'ст. Тобольск',
  'УТНГП ПАО Татнефть',
  'УПГ Сургутнефтегаз', 
  'ПАО Нижнекамскнефтехим',
  'ст. Сургут',
  'Астрахань БП',
  'Липецк-Тамбов-Волгоград БП', 
  'ГНС Минеральные Воды',
  'УН ООО ОСК',
  'Ростов-25 БП',
  'УППНГ на Приразломном месторождении'
]

for row in data_frame.iterrows():
  if row[0] > 6:
    if 'азы углево' in str(row):
      is_found = False
      for basis in basises:
        if basis in str(row):
          is_found = True
          break
      if not is_found:
        data_frame.drop(axis=1, index=row[0], inplace=True)
    else:
      data_frame.drop(axis=1, index=row[0], inplace=True)

data_frame.reset_index(drop=True, inplace=True)  

# https://github.com/PyCQA/pylint/issues/3060 pylint: disable=abstract-class-instantiated
xls_writer = pandas.ExcelWriter(today_filename, engine = 'xlsxwriter')
data_frame.to_excel(xls_writer, header=False, index=False, sheet_name='s1')
ws = xls_writer.sheets['s1']
ws.set_column('A:A',1)
ws.set_column('B:B',15)
ws.set_column('D:D',29)
ws.set_column('F:F',14)
xls_writer.save()

msg = MIMEMultipart()
body = 'Бюллетень по итогам торгов от ' + str(date.today())
msg['From'] = mail_from
msg['To'] = mail_to
msg['Subject'] = 'Бюллетень по итогам торгов от ' + str(date.today())
msg.attach(MIMEText(body, "plain"))
with open(today_filename, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
encoders.encode_base64(part)
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {today_filename}",
)
msg.attach(part)

s = smtplib.SMTP(smtp_server_ip)
s.send_message(msg)
s.quit()
