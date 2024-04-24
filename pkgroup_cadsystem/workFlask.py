from flask import Flask, request, render_template
from flask_restx import Api, Resource, fields
from pprint import pprint  
from datetime import datetime
# from workBitrix import get_task_work_time, create_item, get_crm_task, prepare_crm_task
from workBitrix import get_products, update_product
app = Flask(__name__)
api = Api(app, version='1.0', title='pkGroup API',description='A pkGroup API',)


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


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5007',debug=True)
    
