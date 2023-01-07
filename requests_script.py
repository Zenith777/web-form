import requests
# Простой скрипт, который отправляет POST запросы на локальный сервер с тремя формами для проверки соответствия форм

form = {'change_date' : '31.12.2014','order_date' : '2001-12-14'}
form2 = {'customer_phone': '+79851366632', 'second_phone': '+74951264359'}
form3 = {'stock_mail': 'zenith985@gmail.com', 'delivery_date': '2007-10-14'}


url = r'http://127.0.0.1:5000/get_form'
req1 = requests.post(url, data=form).text
assert req1 == 'Changes'

req2 = requests.post(url, data=form2).text
assert req2 == 'Delivery'

req3 = requests.post(url, data=form3).text
assert req3 == '{\n  "delivery_date": "date",\n  "stock_mail": "email"\n}\n'

