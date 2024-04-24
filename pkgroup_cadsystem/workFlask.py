from flask import Flask, request, render_template
from flask_restx import Api, Resource, fields
from pprint import pprint  
from datetime import datetime
# from workBitrix import get_task_work_time, create_item, get_crm_task, prepare_crm_task
# from collections import deque
from workBitrix import get_products, update_product
from dotenv import load_dotenv
import os
# from pprint import pformat

load_dotenv()
PORT=os.getenv('PORT')
HOST=os.getenv('HOST')
app = Flask(__name__)
api = Api(app, version='1.0', title='CAD system API',description='A pkGroup API',)


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
logs = []
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        log_entry = request.form.get('log_entry')
        if log_entry:
            log_level = request.form.get('log_level', 'INFO')  # По умолчанию INFO
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if len(logs) >= 30:
                logs.pop(0)
            logs.append({'timestamp': timestamp, 'level': log_level, 'message': log_entry})
            return 'Лог записан!'
        else:
            return 'Нет данных для записи в лог!'
    else:
        for log in logs:
            log['message'] = log['message']
        logs.reverse()
        return render_template('index.html', logs=logs)
    
@app.route('/clear_logs', methods=['POST'])
def clear_logs():
    logs.clear()
    return 'Логи очищены!'

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
    
