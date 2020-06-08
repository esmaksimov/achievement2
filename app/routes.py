from app import app
from app.dbhandler import DBHandler, NumberExists, NumberPlusOneExists
from flask import request, make_response
import json
from logging import getLogger

db_handler = DBHandler()
logger_err = getLogger('file')
logger_cons = getLogger('console')


@app.route('/', methods=['POST', 'GET'])
def process_number():
    raw = request.data
    try:
        number = json.loads(raw)
    except json.JSONDecodeError:
        return make_response('Give an JSON format', 400)

    number = number.get('data', None)

    try:
        number = int(number)

        # Если число существует в базе то проверяем меньше ли оно последнего обработанного числа на 1
        if db_handler.exist_in_db(number+1):
            raise NumberPlusOneExists
        elif db_handler.exist_in_db(number):
            raise NumberExists

        # Если число никогда не поступало в базу, то вставляем его
        else:
            db_handler.insert_numb(number)
            return make_response('Digit is eaten', 200)

    except (ValueError, TypeError):
        text = 'Give an number in "data" of the sending JSON'
        # в файл
        logger_err.error(text)
        # в консоль
        logger_cons.error(text)

        return make_response('Give an number in "data" of the sending JSON')

    except NumberExists:
        text = 'Number exists'
        # в файл
        logger_err.error(text)
        # в консоль
        logger_cons.error(text)

        return make_response(text)

    except NumberPlusOneExists:
        text = 'Number + 1 exists'
        # в файл
        logger_err.error(text)
        # в консоль
        logger_cons.error(text)

        return make_response(text)
