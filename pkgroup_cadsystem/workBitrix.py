from fast_bitrix24 import Bitrix
import os
from dotenv import load_dotenv
from pprint import pprint
from dataclasses import dataclass
from datetime import datetime
# import urllib3
import urllib.request
import time
import asyncio
load_dotenv()
webhook = os.getenv('WEBHOOK')
bit = Bitrix(webhook)

@dataclass
class Lead:
    userName:str
    title:str='TITLE'
    userID:str='UF_CRM_1709220784686'
    photos:str='UF_CRM_1709223951925'
    urlUser:str='UF_CRM_1709224894080'
    messageURL:str='UF_CRM_1709293438392'

    description:str='COMMENTS'

@dataclass
class Deal:
    id:str='ID'
    title:str='TITLE'
    categoryID:str='CATEGORY_ID'
    statusID:str='STATUS_ID'
    comments:str='COMMENTS'
    responsibleID:str='ASSIGNED_BY_ID'


# async def te
def find_deal(dealID:str):
    deal = bit.call('crm.deal.get', params={'id': dealID})
    return deal

def find_lead(leadID:str):
    lead = bit.call('crm.lead.get', params={'id': leadID})
    return lead


def get_deals():
    prepareDeal=[]
    deals = bit.call('crm.deal.list', items={'filter': 
                                             {'STAGE_SEMANTIC_ID':'S'}}, raw=True)['result']
    for deal in deals:
        
        product=bit.call('crm.deal.productrows.get', items={'id': int(deal['ID'])}, raw=True)['result']
        
        a={'deal':deal,
            'product':product}
        
        prepareDeal.append(a)
    pprint(prepareDeal)
    return prepareDeal

def get_products(poductID):
    products=bit.call('crm.product.get', items={'ID':poductID}, raw=True)['result']

    pprint(products)

    return products

def get_users():
    prepareUser = []
    # users = bit.call('user.get', items={'filter' :{'ACTIVE':False}})
    users = bit.call('user.get', raw=True)['result']
    # for user in users:
        # prepareUser.append(f'[{user["ID"]}] {user["NAME"]} {user["LAST_NAME"]}')
    # pprint(users)
    # print(prepareUser)
    return users

def get_departments():
    departments = bit.call('department.get', raw=True)['result']
    pprint(departments)
    return departments

def get_task_work_time(id)->list:
    # task=bit.call('tasks.task.get', items={'taskId': id}, raw=True)['result']
    task=bit.call('task.elapseditem.getlist', items={'ID': id}, raw=True)['result']
    # pprint(task)
    return task

def create_item(duretion,taskID, comment, dateClose):
    bit.call('crm.item.add', items={
                            'entityTypeId':179, #биллинг
                            'fields': {'title': comment,
                                'ufCrm9_1713363122': duretion,
                                'ufCrm9_1713363093': dateClose.split('+')[0],}})

def add_new_post_timeline(itemID, entityID, entityType):
    bit.call('crm.timeline.comment.add', items={
                            'fields': {'ENTITY_ID': entityID,
                                'ENTITY_TYPE': entityType,
                                'COMMENT': """Создан новый пост
                                Test comment [URL=/crm/deal/details/26/]test123[/URL]""",}}) #для ссылки в нутри битрикса



def update_product(productID, fields:dict):
    bit.call('crm.product.update', items={'ID':productID, 'fields':fields})

def create_product(fields:dict):
    bit.call('crm.product.add', items={'fields':fields})

if __name__ == '__main__':

    
   a=get_products(1)

    
    





