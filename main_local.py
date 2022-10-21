import ui_barcodes
import ui_csv
import ui_global
import socket
import json
import sqlite3
from sqlite3 import Error
import ui_form_data
import requests
from flask import Flask
from flask import request

app = Flask(__name__)



def settings_on_start(hashMap, _files=None, _data=None):

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        aa = (s.getsockname()[0])
        # aa = hashMap.get('ip_adr')
        hashMap.put('ip_adr', aa)
        #hashMap.put('toast', aa)
    except:
        hashMap.put('ip_adr', 'нет сети')

    # Значения констант и настроек
    res = ui_global.get_constants()
    if not res is None:
        hashMap.put('use_series', str(res[1]))
        hashMap.put('use_properties', str(res[2]))
        hashMap.put('use_mark', str(res[3]))
        hashMap.put('path', str(res[4]))
        hashMap.put('delete_files', str(res[5]))
    return hashMap


def settings_on_click(hashMap, _files=None, _data=None):
    use_series = hashMap.get('use_series')
    use_properties = hashMap.get('use_properties')
    use_mark = hashMap.get('use_mark')
    delete_files = hashMap.get('delete_files')
    path = hashMap.get('path')

    if use_series == None: use_series = '0'
    if use_properties == None: use_properties = '0'
    if use_mark == None: use_mark = '0'
    if delete_files == None: delete_files = '0'
    if path == None: path = '//storage/emulated/0/download/'

    ui_global.put_constants((use_series, use_properties, use_mark, path, delete_files))

    if hashMap.get('listener') == 'btn_copy_base':
        pass
        # with open('//data/data/ru.travelfood.simple_ui/databases/SimpleWMS', 'rb') as f:
        #     r = requests.post('http://192.168.0.45:2444/post', files={'SimpleWMS': f})
        # if r.status_code == 200:
        #     hashMap.put('toast', 'База SQLite успешно выгружена')
        # else:
        #     hashMap.put('toast', 'Ошибка соединения')

    elif hashMap.get('listener') == 'btn_local_files':
        # path = hashMap.get('localpath')
        path = hashMap.get('path')
        delete_files = hashMap.get('delete_files')
        if not delete_files: delete_files = '0'
        if not path: path = 'ОбменТСД/НА/'
        path = 'ОбменТСД/НА/'
        ret_text = ui_csv.list_folder(path,delete_files)

        hashMap.put('toast', ret_text)
    elif hashMap.get('listener') == 'btn_export':
        ui_csv.export_csv(path, hashMap.get('ip_adr'), hashMap.get('AndriodID'))
        hashMap.put('toast', 'Данные выгружены')

    return hashMap


def init_on_start(hashMap, _files=None, _data=None):

    return hashMap


def goods_on_start(hashMap, _files=None, _data=None):
    # hashMap.put("mm_local", "")
    # hashMap.put("mm_compression", "70")
    # hashMap.put("mm_size", "65")
    list = ui_form_data.get_goods_card()
    list['customcards']['cardsdata'] = []
    query_text = ui_form_data.get_goods_query()

    results = ui_global.get_query_result(query_text)

    for record in results:
        product_row = {
            'key': str(record[0]),
            'name': str(record[3]),
            'code': str(record[1]),
            'type_name': str(record[5]),
            'unit_name': str(record[7])
        }
        list['customcards']['cardsdata'].append(product_row)
    # **********************
    hashMap.put("goods_cards", json.dumps(list))

    return hashMap


# Заполнение списка документов
def refill_docs_list(filter=''):
    doc_list = ui_form_data.get_doc_card()
    doc_list['customcards']['cardsdata'] = []

    query_text = ui_form_data.get_doc_query(filter)

    if filter == '' or filter == 'Все':
        results = ui_global.get_query_result(query_text)
    else:
        results = ui_global.get_query_result(query_text, (filter,))

    for record in results:
        if record[8] == 1:
            completed = 'true'
        else:
            completed = 'false'
        product_row = {
            'completed': completed,
            'type': str(record[1]),
            'number': str(record[2]),
            'data': str(record[3]),
            'key': record[0],
            'warehouse': record[7],
            'countragent': record[6]
        }
        doc_list['customcards']['cardsdata'].append(product_row)

    return json.dumps(doc_list)


def docs_on_start(hashMap, _files=None, _data=None):
    # Заполним поле фильтра по виду документов
    result = ui_global.get_query_result(ui_form_data.get_doc_type_query())
    if hashMap.get('doc_type_select') == None:
        doc_type_list = 'Все'
        for record in result:
            doc_type_list = doc_type_list + (';' + record[0])
        hashMap.put('doc_type_select', doc_type_list)

    # hashMap.put('doc_type_click', 'Все')

    # Перезаполним список документов
    if hashMap.get('doc_type_click') == None:
        ls = refill_docs_list()
    else:
        ls = refill_docs_list(hashMap.get('doc_type_click'))
    hashMap.put("docCards", ls)

    return hashMap


def doc_details_on_start(hashMap, _files=None, _data=None):
    id_doc = hashMap.get('id_doc')
    # Формируем таблицу карточек и запрос к базе
    res = ui_global.get_constants()
    use_series = res[1]
    use_properties = res[2]
    hashMap.put('use_properties', res[2])
    doc_detail_list = ui_form_data.get_doc_detail_cards(use_series, use_properties)
    doc_detail_list['customcards']['cardsdata'] = []

    query_text = ui_form_data.get_doc_details_query()

    results = ui_global.get_query_result(query_text, (id_doc,))
    hashMap.put('id_doc', str(results[0][1]))
    for record in results:
        product_row = {
            'key': str(record[0]),
            'good_name': str(record[3]),
            # 'id_properties': str(record[3]),
            'properties_name': str(record[5]),
            # 'id_series': str(record[5]),
            'series_name': str(record[7]),
            # 'id_unit': str(record[7]),
            'code_art': 'Код: ' + str(record[2]),
            'units_name': str(record[9]),
            'qtty': str(record[10] if record[10] is not None else 0),
            'qtty_plan': str(record[11] if record[11] is not None else 0),
            'price': str(record[12] if record[12] is not None else 0),
            'price_name': str(record[13]),
            'picture':'#f02a'
        }

        doc_detail_list['customcards']['cardsdata'].append(product_row)

    hashMap.put("doc_goods", json.dumps(doc_detail_list))

    return hashMap


def docs_on_select(hashMap, _files=None, _data=None):
    listener = hashMap.get("listener")

    if listener == "CardsClick":
        # Находим ID документа
        current_str = hashMap.get("selected_card_position")
        jlist = json.loads(hashMap.get("docCards"))
        current_doc = jlist['customcards']['cardsdata'][int(current_str)]

        # id_doc = current_doc['key']
        hashMap.put('id_doc', current_doc['key'])
        hashMap.put('doc_type', current_doc['type'])
        hashMap.put('doc_n', current_doc['number'])
        hashMap.put('doc_date', current_doc['data'])
        hashMap.put('warehouse', current_doc['warehouse'])
        hashMap.put('countragent', current_doc['countragent'])

        hashMap.put("ShowScreen", "Документ товары")

    elif listener == "doc_type_click":
        ls = refill_docs_list(hashMap.get('doc_type_click'))
        hashMap.put('docCards', ls)
        hashMap.put('ShowScreen', 'Документы')
    elif listener == 'LayoutAction':
        layout_listener = hashMap.get('layout_listener')
        # Находим ID документа
        current_doc = json.loads(hashMap.get("card_data"))
        doc = ui_global.Rs_doc
        doc.id_doc = current_doc['key']

        if layout_listener == 'CheckBox1':
            if current_doc['completed'] == 'false':
                doc.mark_verified(doc, 1)
            else:
                doc.mark_verified(doc, 0)

        elif layout_listener == 'Подтвердить':
            doc.mark_verified(doc, 1)
            hashMap.put('ShowScreen', 'Документы')
        elif layout_listener == 'Удалить':
            doc.delete_doc(doc)
            hashMap.put('ShowScreen', 'Документы')
    elif listener == "btn_add_doc":
        hashMap.put('ShowScreen', 'Новый документ')
    return hashMap


def doc_details_listener(hashMap, _files=None, _data=None):
    # Находим ID документа
    # current_str = hashMap.get("selected_card_position")
    # current_card_list = hashMap.get("doc_goods")
    # jl = jlist['customcards']['cardsdata']
    # if not current_card_list == None:
    #     jlist = json.loads(current_card_list)
    #     current_elem = jlist['customcards']['cardsdata'][int(current_str)-1]
    # else:
    #     current_elem = None

    if hashMap.get("listener") == "CardsClick":

        # Находим ID документа
        current_str = hashMap.get("selected_card_position")
        jlist = json.loads(hashMap.get("doc_goods"))
        current_elem = jlist['customcards']['cardsdata'][int(current_str)]
        hashMap.put("Doc_data",
                    hashMap.get('doc_type') + ' №' + hashMap.get('doc_n') +
                    ' от' + hashMap.get('doc_date'))
        hashMap.put("Good", current_elem['good_name'])
        hashMap.put("qtty_plan", str(current_elem['qtty_plan']))
        if float(current_elem['qtty']) == 0:
            hashMap.put("qtty", '')
        else:
            hashMap.put("qtty", str(current_elem['qtty']))
        hashMap.put('key', current_elem['key'])
        hashMap.put('price', current_elem['price'])
        hashMap.put('price_type', current_elem['price_name'])
        #Формируем таблицу QR кодов------------------
        query_text = ui_form_data.get_doc_barcode_query()
        args = {'id_doc':hashMap.get('doc_n'), 'name_good':current_elem['good_name']}
        cards = ui_form_data.get_barcode_card()
        res = ui_global.get_query_result(query_text,args,True)
        #Формируем список карточек баркодов
        cards['customcards']['cardsdata'] = []
        for el in res:
            #barcode_data = ui_barcodes.get_gtin_serial_from_datamatrix(el['barcode'])
            if el['approved']=='1':
                picture = '#f00c'
            else:
                picture = ''
            row = {
                'barcode': el['barcode'],
                'picture': picture
            }
            cards['customcards']['cardsdata'].append(row)
        hashMap.put("barcode_cards", json.dumps(cards))

        hashMap.put("ShowScreen", "Товар")

    elif hashMap.get("listener") == "BACK_BUTTON":
        hashMap.put("ShowScreen", "Документы")
    elif hashMap.get("listener") == "btn_barcodes":

        hashMap.put("ShowScreen", "Документ штрихкоды")


    elif hashMap.get('listener') == 'barcode':
        doc = ui_global.Rs_doc
        doc.id_doc = hashMap.get('id_doc')
        barcode = hashMap.get('barcode_camera')
        res = doc.find_barcode_on_doc(doc, barcode)
        if res == None:
            hashMap.put('toast',
                        'Штрих код не зарегистрирован в базе данных. Проверьте товар или выполните обмен данными')
        elif res['Error']:
            hashMap.put('toast',res['Error'])
        else:
            hashMap.put('toast', 'Товар добавлен в документ')
        # hashMap.put('toast','1')

    elif hashMap.get('listener') == 'btn_doc_mark_verified':
        doc = ui_global.Rs_doc
        doc.id_doc = hashMap.get('id_doc')
        doc.mark_verified(doc, 1)
        hashMap.put("ShowScreen", "Документы")

    return hashMap


def elem_on_click(hashMap, _files=None, _data=None):
    listener = hashMap.get("listener")
    if listener == "btn_ok":
        # получим текущую строку документа
        current_str = hashMap.get("selected_card_position")
        jlist = json.loads(hashMap.get("doc_goods"))
        current_elem = jlist['customcards']['cardsdata'][int(current_str)]
        key = int(current_elem['key'])
        # ... и запишем ее в базу

        doc = ui_global.Rs_doc
        doc.id_str = int(current_elem['key'])
        doc.qtty = float(hashMap.get('qtty'))
        doc.update_doc_str(doc, hashMap.get('price'))

        hashMap.put("ShowScreen", "Документ товары")
    elif listener == "btn_cancel":

        hashMap.put("ShowScreen", "Документ товары")
    elif listener == "BACK_BUTTON":
        hashMap.put("ShowScreen", "Документ товары")
    elif listener == "":
        hashMap.put("qtty", str(float(hashMap.get('qtty'))))

    return hashMap


def goods_on_click(hashMap, _files=None, _data=None):
    listener = hashMap.get("listener")

    if listener == "CardsClick":
        # Находим ID документа
        current_str = hashMap.get("selected_card_position")
        jlist = json.loads(hashMap.get("goods_cards"))
        current_good = jlist['customcards']['cardsdata'][int(current_str)]

        # id_doc = current_doc['key']
        hashMap.put('id_good', current_good['key'])
        hashMap.put('name', current_good['name'])
        hashMap.put('code', current_good['code'])
        hashMap.put('type_name', current_good['type_name'])
        #        hashMap.put('unit_name', current_good['unit_name'])

        hashMap.put("ShowScreen", "Цены товара")

    return hashMap


def price_on_start(hashMap, _files=None, _data=None):
    id_good = hashMap.get('id_good')
    # Формируем таблицу карточек и запрос к базе
    goods_price_list = ui_form_data.get_price_card()
    goods_price_list['customcards']['cardsdata'] = []

    query_text = ui_form_data.get_price_query()

    results = ui_global.get_query_result(query_text, (id_good,))
    for record in results:
        product_row = {
            'key': str(record[0]),
            'price_type': str(record[7]),
            'price': str(record[4])}
        goods_price_list['customcards']['cardsdata'].append(product_row)

    hashMap.put("good_prices", json.dumps(goods_price_list))

    return hashMap


def price_on_click(hashMap, _files=None, _data=None):
    return hashMap


def new_doc_on_start(hashMap, _files=None, _data=None):
    if hashMap.get('doc_type_select') == None:
        # Заполним поле фильтра по виду документов
        result = ui_global.get_query_result(ui_form_data.get_doc_type_query())
        doc_type_list = 'Все'
        for record in result:
            doc_type_list = doc_type_list + (';' + record[0])
        hashMap.put('doc_type_select', doc_type_list)

    if hashMap.get('countragent') == None:
        fld_countragent = ui_global.get_name_list('RS_countragents')
        hashMap.put('countragent', fld_countragent)

    if hashMap.get('warehouse') == None:
        fld_countragent = ui_global.get_name_list('RS_warehouses')
        hashMap.put('warehouse', fld_countragent)

    if not hashMap.containsKey('doc_date'):
        hashMap.put('doc_date', '01.01.2022')
    return hashMap


def new_doc_on_select(hashMap, _files=None, _data=None):
    listener = hashMap.get("listener")

    if listener == "btn_ok":
        ui_global.Rs_doc.add('01', ('001',
                                    hashMap.get('doc_type_click'),
                                    hashMap.get('fld_number'),
                                    hashMap.get('fld_data'),
                                    ui_global.get_by_name(hashMap.get('fld_countragent'), 'RS_countragents'),
                                    ui_global.get_by_name(hashMap.get('doc_warehouse'), 'RS_warehouses')))
        hashMap.put('ShowScreen', 'Документы')
    elif listener == 'btn_cancel':
        hashMap.put('ShowScreen', 'Документы')
    elif listener == 'fld_data':
        hashMap.put('doc_date', hashMap.get('fld_data'))
    return hashMap

def doc_barcodes_on_start(hashMap, _files=None, _data=None):
    doc_detail_list = ui_form_data.get_barcode_card()
    query_text = ui_form_data.get_barcode_query()
    id_doc = hashMap.get('id_doc')
    results = ui_global.get_query_result(query_text, (id_doc,))

    for record in results:
        product_row = {
            'key': str(record[0]),
            'barcode_value': str(record[3]),
            'approved': str(record[4])

        }

        doc_detail_list['customcards']['cardsdata'].append(product_row)

    hashMap.put("barc_cards", json.dumps(doc_detail_list))

    return hashMap


def doc_barcodes_listener(hashMap, _files=None, _data=None):
    return hashMap




@app.route('/set_input_direct/<method>', methods=['POST'])
def set_input(method):
    func = method.replace('_', '', 1)
    jdata = json.loads(request.data.decode("utf-8"))
    f = globals()[func]
    hashMap.d = jdata['hashmap']
    f(hashMap)
    jdata['hashmap'] = hashMap.export(hashMap)
    jdata['stop'] = False
    jdata['ErrorMessage'] = ""
    jdata['Rows'] = []

    return json.dumps(jdata)


@app.route('/post_screenshot', methods=['POST'])
def post_screenshot():
    d = request.data
    return "1"


class hashMap:
    d = {}

    def put(key, val):
        if key == 'toast':
            print(val)
        hashMap.d[key] = val

    def get(key):
        return hashMap.d.get(key)

    def remove(key):
        if key in hashMap.d:
            hashMap.d.pop(key)

    def containsKey(key):
        return key in hashMap.d

    def export(self):
        ex_hashMap = []
        for key in self.d.keys():
            ex_hashMap.append({"key": key, "value": hashMap.d[key]})
        return ex_hashMap


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=2075, debug=True)