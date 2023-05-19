import json

import http_exchange
import ui_form_data
import ui_global
import rs_settings
import sqliteparser
import time
import requests
from requests.auth import HTTPBasicAuth

#
# qtext = '''SELECT id_doc FROM RS_docs WHERE verified = '1'
#             UNION
#             SELECT id_doc FROM RS_adr_docs WHERE verified = '1'
#             '''
# res  = ui_global.get_query_result(qtext,None,True)
#
#
# if res:
#
#     http_settings = {
#     'url' : 'http://192.168.1.77/Mark/hs/',
#     'user' : 'ADM',
#     'pass' : '1',
#     'device_model' : 'Python',
#     'android_id':'f0559476b8a26877',  # 'c51133488568c92b',
#     'user_name': 'Gerald'}
#     doc_list = []
#
#     doc_list = []
#     for el in res:
#         doc_list.append('"' + el['id_doc'] + '"')
#     doc_in_str = ','.join(doc_list)
#     http_exchange.post_changes_to_server(doc_in_str , http_settings)
#

#
# ------------------- Блок загрузки данных -------------------
# http_settings = {
# 'url' : 'http://192.168.1.77/Mark/hs/',
# 'user' : 'ADM',
# 'pass' : '1',
# 'device_model' : 'Python',
# 'android_id':'f0559476b8a26877', #'c51133488568c92b',
# 'user_name': 'Gerald'}
# x=0
# while x < 2:
#
#     # url =
#     # android_id = 'c51133488568c92b' #'7b1bc913358b7049'
#     result = http_exchange.server_load_data(http_settings)
#     #if not result == 'ok':
#     if result.get('res_for_sql') is not None:
#         error_pool =[]
#         for key in result['res_for_sql']:
#             try:
#                 ui_global.get_query_result(key)
#                 # return 'ok'
#             except Exception as e:
#                 sql_error = True
#                 error_pool.append(e.args[0])
#                 print(e.args[0])
#     else:
#         print(result)
#
#     x+=1
#     time.sleep(10)
#     print('Цикл: '+ str(x))

# Получим список полей таблицы
# table_name = 'RS_goods'
# res = ui_global.get_query_result(f"PRAGMA table_info({table_name})")
# fields = [f[1] for f in res]
# # Словарь русских имен полей
# aliases = ui_form_data.fields_alias_dict()
# # Словарь полей-ссылок на таблицы
# tables_dict = ui_form_data.table_names_dict()
#
# # Создадим запрос к таблице. Ссылочные поля заменим на наименование из связанных таблиц
# card_elem = ui_form_data.get_elem_dict(24)
# cards = ui_form_data.get_universal_card()
#
# qfield_text = []
# left_joins_list = []
# for el in fields:
#     link_table_name = tables_dict.get(el)
#     qfield_text.append(table_name +'.'+ el)
#
#     # Дополним выходную структуру полями таблицы:
#     card_elem['Value'] = '@'+el
#
#
#     if link_table_name:
#         # Это ссылка на таблицу
#         qfield_text.append(link_table_name + f'.name as {link_table_name}_name')
#         left_joins_list.append(f'''
#             LEFT JOIN {link_table_name}
#             ON {link_table_name}.id = {table_name}.{el}
#             ''')
#         card_elem['Value'] = f'@{link_table_name}_name'  #Так как поле ссылочное - переименуем его как в запросе
#
#     #Добавим поле в карточки
#     cards['customcards']['layout']['Elements'][0]['Elements'][0]['Elements'].append(card_elem.copy())
#
#
# qtext = 'Select ' + ','.join(qfield_text) + f' FROM {table_name} '+ ' '.join(left_joins_list)
# res_query =  ui_global.get_query_result(qtext,None,True)
# #settings_global.get
#
# cards['customcards']['cardsdata'] = []
#
# for i in res_query:
#     product_row = {}
#     for x in i:
#         product_row[x] = str(i[x])
#
#     cards['customcards']['cardsdata'].append(product_row)
#
# jcards= json.dumps(cards)
# pass
#
# fields = ('field1', 'field2')
# search_val = 'value_for_finding'
#
# # Create a list of OR conditions for each field
# conditions = [f"{field} = '{search_val}'" for field in fields]
#
# # Join the conditions with 'OR' to create the final SQL query
# query = f"SELECT * FROM my_table WHERE {' OR '.join(conditions)};"
# print(query)


#Tест соединения
http = {
    'url' : 'http://192.168.1.77/Mark/hs/',
    'user' : 'ADM',
    'pass' : '1',
    'device_model' : 'Python',
    'android_id':'f0559476b8a26877',  # 'c51133488568c92b',
    'user_name': 'Gerald'}
#http = get_http_settings(hashMap)
r = requests.get(http['url'] + '/simple_accounting/communication_test?android_id=' + http['android_id'],
                 auth=HTTPBasicAuth(http['user'], http['pass']),
                 headers={'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'},
                 params={'user_name': http['user_name'], 'device_model': http['device_model']})
if r.status_code == 200:
    print('Соединение установлено')
else:
    print(r.reason)
