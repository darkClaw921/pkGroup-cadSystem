from flask import Flask, request, render_template
from flask_restx import Api, Resource, fields
from pprint import pprint  
from datetime import datetime
# from workBitrix import get_task_work_time, create_item, get_crm_task, prepare_crm_task
# from collections import deque
from workBitrix import get_products, update_product
from dotenv import load_dotenv
import os
import requests 
from pprint import pformat

load_dotenv()
PORT=os.getenv('PORT')
HOST=os.getenv('HOST')
app = Flask(__name__)
api = Api(app, version='1.0', title='CAD system API',description='A pkGroup API\nЛоги можно посмотреть по пути /logs\nОчистить логи можно по пути /clear_logs\n',)
logs = []

def log_counts_by_level(logs:list)->dict:
        counts = {'DEBUG': 0, 'INFO': 0, 'WARNING': 0, 'ERROR': 0}
        for log in logs:
            counts[log['level']] += 1
        return counts

def log_counts_by_minute(logs:list)->dict:
        counts_by_minute = {}
        for log in logs:
            timestamp_minute = log['timestamp'][:16]  # Обрезаем до минут
            if timestamp_minute in counts_by_minute:
                counts_by_minute[timestamp_minute][log['level']] += 1
            else:
                counts_by_minute[timestamp_minute] = {'DEBUG': 0, 'INFO': 0, 'WARNING': 0, 'ERROR': 0}
                counts_by_minute[timestamp_minute][log['level']] += 1
        return counts_by_minute

def send_log(message, level='INFO'):
    requests.post(f'http://{HOST}:{PORT}/logs', json={'log_entry': message, 'log_level': level})

@api.route('/task')
class task_entity(Resource):
    def post(self,):
        """Обновление сущности"""
        data = request.get_json() 
        pprint(data)
        
        # pprint(a)

        return 'OK'
    
    def get(self,):
        """Обновление сущности"""
        pprint(request)
        data = request.get_json() 
        pprint(data)
        return 'OK'
    
@api.route('/tasks')
class tasks_entity(Resource):
    def get(self,):
        """Обновление сущности"""
        pprint(request)
        data = request.get_json() 
        pprint(data)
        return 'OK'
    
    def post(self,):
        """Обновление сущности"""
        data = request.get_json() 
        pprint(data)
    
        
        return 'OK'

@api.route('/product')
class product_entity(Resource):
    def get(self,):
        """Обновление сущности"""
        # pprint(request.__dict__)
        data = request.get_json() 
        pprint(data)
        
        return 'OK'
    
    def post(self,):
        """Обновление сущности"""
        pprint(request.__dict__)
        data = request.get_json() 
        pprint(data)
        productID=data['a'][1].split('=')[1]
        product=get_products(productID)
        
        fields={
            'NAME': 'Test product',
            'DESCRIPTION': 'Test product',
            'PRICE': 100,
        }
        update_product(productID, fields=fields)

        # tasks=get_crm_task(13)
        # p=prepare_crm_task(tasks)
        
        return 'OK'

# Очередь для хранения логов
# logs_queue = deque(maxlen=10)  # Максимум 10 последних логов

@app.route("/logs", methods=['GET', 'POST'])
def index1():
    global logs
    if request.method == 'POST':
        logR=request.get_json()
        # pprint(log)
        log_entry = logR.get('log_entry')
        # log_entry = request.form.get('log_entry')
        if log_entry:
            # log_level = request.form.get('log_level', 'INFO')  # По умолчанию INFO
            log_level = logR.get('log_level', 'INFO')
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            if len(logs) >= 100:
                logs.pop(0)
            logs.append({'timestamp': timestamp, 'level': log_level, 'message': log_entry})
            return 'Лог записан!'
        else:
            return 'Нет данных для записи в лог!'
    else:
        pprint(logs)
        for log in logs:
            if isinstance(log['message'], dict) or isinstance(log['message'], list):
                log['message'] = pformat(log['message'])

        logs.reverse()
        countsLog=log_counts_by_level(logs)
        countsLog=log_counts_by_minute(logs)
        pprint(countsLog)
        return render_template('index.html', logs=logs, log_counts=countsLog)
    
@app.route('/clear_logs', methods=['POST'])
def clear_logs():
    logs.clear()
    return 'Логи очищены!'

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
    
