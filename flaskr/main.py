import re
from flask import Flask, render_template, request
from tinydb import TinyDB, Query

app = Flask(__name__)

# Создадим локальную базу и заполним её тестовыми данными
DB = TinyDB('./forms.json')
Forms = DB.table("Forms")

Forms.insert({'name': 'Orders', 'customer_mail': 'email', 'order_date': 'date', 'customer_phone': 'phone'})
Forms.insert({'name': 'Returns', 'shop_phone': 'phone', 'stock_mail': 'email'})
Forms.insert({'name': 'Delivery', 'customer_phone': 'phone', 'second_phone': 'phone'})
Forms.insert({'name': 'Changes', 'change_date': 'date'})


# Функция преобразует форму, которая поступает на вход в виде словаря и с помощью регулярных выражений определяет
# типы данных в форме (почта, телефон, дата, текст)
def convert_form(form):
    result = {}
    pattern_email = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'
    pattern_phone = r'^\+7(\d{10})$'
    pattern_date1 = r'^\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})\s*$'
    pattern_date2 = r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))'
    for k, v in form.items():

        if type(v) is not str:
            raise ValueError('Value is not string')

        if re.fullmatch(pattern_date1, v):
            result[k] = 'date'

        elif re.fullmatch(pattern_date2, v):
            result[k] = 'date'

        elif re.fullmatch(pattern_email, v):
            result[k] = 'email'

        elif re.fullmatch(pattern_phone, v):
            result[k] = 'phone'

        else:
            result[k] = 'text'

    return result

# Функция ищет в базе данных все шаблоны форм в которых содержится хотя бы одно соответствие имени поля и типа поля
# из переданных параметров POST запроса
# Функция необходима для дальнейшей проверки шаблона на соответствие данным из POST запроса
def find_tables(**query):
    result = []
    for k, v in query.items():
        for i in (Forms.search(getattr(Query(), k) == v)):
            if i not in result:
                result.append(i)
    return result

# Функция отбрасывает имя формы и проверяет, все ли пары имя поля и тип значения присутствуют в данных из запроса
# и возвращает имя подходящей формы или форму с преобразованным типом значения
def form_conformity(forms_to_check, passed_form):
    for i in forms_to_check:
        dictcopy = i.copy()
        del dictcopy['name']
        if dictcopy.items() <= passed_form.items():
            return i['name']
    return passed_form


@app.route('/get_form', methods=['POST'])
def get_form():
    result = form_conformity(find_tables(**convert_form(request.form.to_dict())), convert_form(request.form.to_dict()))
    return result


app.debug = True

if __name__ == '__main__':
    app.run()


