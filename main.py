import os
import csv

import ui_barcodes
import ui_csv
import ui_global
import ui_form_data
import socket
import json
import requests

#0100608940553886215,iPGSQpBt!&B
def settings_on_start(hashMap, _files=None, _data=None):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        aa = (s.getsockname()[0])
        # aa = hashMap.get('ip_adr')
        hashMap.put('ip_adr', aa)
        # hashMap.put('toast', aa)
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

    if not hashMap.containsKey('ip_host'):
        hashMap.put('ip_host', '192.168.0.45')

    return hashMap


def settings_on_click(hashMap, _files=None, _data=None):
    use_series = hashMap.get('use_series')
    use_properties = hashMap.get('use_properties')
    use_mark = hashMap.get('use_mark')
    delete_files = hashMap.get('delete_files')
    path = hashMap.get('path')

    if use_series is None: use_series = '0'
    if use_properties is None: use_properties = '0'
    if use_mark is None: use_mark = '0'
    if delete_files is None: delete_files = '0'
    if path is None: path = '//storage/emulated/0/download/'

    ui_global.put_constants((use_series, use_properties, use_mark, path, delete_files))
    listener = hashMap.get('listener')
    if listener == 'btn_copy_base':
        ip_host = hashMap.get('ip_host')
        with open('//data/data/ru.travelfood.simple_ui/databases/SimpleWMS', 'rb') as f:
            r = requests.post('http://' + ip_host + ':2444/post', files={'SimpleWMS': f})
        if r.status_code == 200:
            hashMap.put('toast', 'База SQLite успешно выгружена')
        else:
            hashMap.put('toast', 'Ошибка соединения')

    elif listener == 'btn_local_files':
        # path = hashMap.get('localpath')
        path = hashMap.get('path')
        delete_files = hashMap.get('delete_files')
        if not delete_files: delete_files = '0'
        if not path: path = '//storage/emulated/0/download/'
        ret_text = ui_csv.list_folder(path, delete_files)

        hashMap.put('toast', ret_text)
    elif listener == 'btn_export':
        ui_csv.export_csv(path, hashMap.get('ip_adr'), hashMap.get('ANDROID_ID'))
        hashMap.put('toast', 'Данные выгружены')

    elif listener == 'ON_BACK_PRESSED':

        hashMap.put('FinishProcess', '')

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
            'GTIN': str(record[0]),
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

    if results:
        hashMap.put('id_doc', str(results[0][1]))
        for record in results:
            product_row = {
                'key': str(record[0]),
                'good_name': str(record[3]),
                'id_good': str(record[2]),
                'id_properties': str(record[4]),
                'properties_name': str(record[5]),
                'id_series': str(record[6]),
                'series_name': str(record[7]),
                'id_unit': str(record[8]),
                'units_name': str(record[9]),
                'code_art': 'Код: ' + str(record[2]),

                'qtty': str(record[10] if record[10] is not None else 0),
                'qtty_plan': str(record[11] if record[11] is not None else 0),
                'price': str(record[12] if record[12] is not None else 0),
                'price_name': str(record[13]),
                'picture': '#f02a' if record[14] != 0 else '#f00c'
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

    elif listener == 'ON_BACK_PRESSED':

        hashMap.put('FinishProcess', '')

        #hashMap.put('ShowScreen', 'Новый документ')
    return hashMap


def doc_details_listener(hashMap, _files=None, _data=None):
    # Находим ID документа
    # current_str = hashMap.get("selected_card_position")
    # current_card_list = hashMap.get("doc_goods")
    # jl = jlist['customcards']['cardsdata']
    # if not current_card_list == None:
    #     jlist = json.loads(hashMap.get("doc_goods"))
    #     current_elem = jlist['customcards']['cardsdata'][int(current_str) - 1]
    # else:
    #     current_elem = None
    listener = hashMap.get('listener')
    if listener == "CardsClick":

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
        # Формируем таблицу QR кодов------------------
        query_text = ui_form_data.get_doc_barcode_query()
        args = dict(id_good=current_elem['id_good'], id_property=current_elem['id_properties'],
                    id_series=current_elem['id_series'], id_unit=current_elem['id_unit'], id_doc=hashMap.get('doc_n'))

        cards = ui_form_data.get_barcode_card()
        res = ui_global.get_query_result(query_text, args, True)
        # Формируем список карточек баркодов
        cards['customcards']['cardsdata'] = []
        for el in res:
            # barcode_data = ui_barcodes.get_gtin_serial_from_datamatrix(el['barcode'])
            if el['approved'] == '1':
                picture = '#f00c'
            else:
                picture = ''
            row = {
                'barcode': el['mark_code'],
                'picture': picture
            }
            cards['customcards']['cardsdata'].append(row)
        hashMap.put("barcode_cards", json.dumps(cards))

        hashMap.put("ShowScreen", "Товар")

    elif listener == "BACK_BUTTON":
        hashMap.put("ShowScreen", "Документы")
    elif listener == "btn_barcodes":

        hashMap.put("ShowScreen", "Документ штрихкоды")


    elif listener == 'barcode':
        doc = ui_global.Rs_doc
        doc.id_doc = hashMap.get('id_doc')
        barcode = hashMap.get('barcode_camera')
        res = doc.find_barcode_on_doc(doc, barcode)
        if res == None:
            hashMap.put('toast',
                        'Штрих код не зарегистрирован в базе данных. Проверьте товар или выполните обмен данными')
        elif res['Error']:
            if res['Error'] == 'AlreadyScanned':

                hashMap.put('barcode', json.dumps({'barcode': res['Barcode'], 'doc_info': res['doc_info']}))
                hashMap.put('ShowScreen', 'Удаление штрихкода')
            else:
                hashMap.put('toast', res['Descr'])
        else:
            hashMap.put('toast', 'Товар добавлен в документ')
        # hashMap.put('toast','1')

    elif listener == 'btn_doc_mark_verified':
        doc = ui_global.Rs_doc
        doc.id_doc = hashMap.get('id_doc')
        doc.mark_verified(doc, 1)
        hashMap.put("ShowScreen", "Документы")

    elif listener == 'ON_BACK_PRESSED':
        hashMap.put("ShowScreen", "Документы")

    return hashMap


def delete_barcode_screen_start(hashMap, _files=None, _data=None):
    # Находим ID документа
    barcode_data = json.loads(hashMap.get('barcode'))['barcode']
    # Найдем нужные поля запросом к базе
    qtext = ui_form_data.get_markcode_query()
    args = {'id_doc': hashMap.get('id_doc'),
            'id_barcode': '01' + barcode_data['GTIN'] + '21' + barcode_data['SERIAL']}

    res = ui_global.get_query_result(qtext, args, True)

    hashMap.put('currentStr', json.dumps(res[0]))
    hashMap.put("CurStr", str(res[0]['CurStr']))
    hashMap.put("good", res[0]['good_name'])
    hashMap.put("'code_art'", res[0]['good_code'])
    hashMap.put("unit_name", str(res[0]['unit']))
    hashMap.put('barcode_value', '01' + barcode_data['GTIN'] + '21' + barcode_data['SERIAL'])

    return hashMap


def delete_barcode_screen_click(hashMap, _files=None, _data=None):
    listener = hashMap.get("listener")
    if listener == "btn_barcode_cancel":

        hashMap.put("ShowScreen", "Документ товары")

    elif listener == "btn_barcode_delete":
        doc = ui_global.Rs_doc
        doc.id_doc = hashMap.get('id_doc')
        current_barcode_str = int(hashMap.get("CurStr"))
        el = json.loads(hashMap.get('currentStr'))

        # doc.id_str = int(current_elem['key'])
        # doc.qtty = float(hashMap.get('qtty'))
        # doc.update_doc_str(doc, hashMap.get('price'))
        query_text = 'Update  RS_docs_barcodes SET approved=? Where id=?'
        ui_global.get_query_result(query_text, ('0', current_barcode_str))
        doc.update_doc_table_data_from_barcode(doc, el, -1)

        hashMap.put("ShowScreen", "Документ товары")

    elif listener == "BACK_BUTTON":
        hashMap.put("ShowScreen", "Документ товары")
    elif listener == 'ON_BACK_PRESSED':
        hashMap.put("ShowScreen", "Документ товары")

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
        qtty = hashMap.get('qtty')
        doc.qtty = float(qtty) if qtty else 0
        doc.update_doc_str(doc, hashMap.get('price'))

        hashMap.put("ShowScreen", "Документ товары")
    elif listener == "btn_cancel":

        hashMap.put("ShowScreen", "Документ товары")
    elif listener == "BACK_BUTTON":
        hashMap.put("ShowScreen", "Документ товары")
    elif listener == "":
        hashMap.put("qtty", str(float(hashMap.get('qtty'))))
    elif listener == 'ON_BACK_PRESSED':
        hashMap.put("ShowScreen", "Документ товары")

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

    elif listener == 'ON_BACK_PRESSED':

        hashMap.put('FinishProcess', '')

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
            'good_name': str(record[3]),
            # 'id_properties': str(record[3]),
            'properties_name': str(record[5]),
            # 'id_series': str(record[5]),
            'series_name': str(record[7])}
    return hashMap


def price_on_click(hashMap, _files=None, _data=None):
    if hashMap.get('listener') == 'ON_BACK_PRESSED':
        hashMap.put("ShowScreen", "Товары список")
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
    type = hashMap.get('doc_type_click')
    if not type:
        type = 'Приход'
    fld_number = hashMap.get('fld_number')




    if listener == "btn_ok":
        if not fld_number:

            id = ui_global.Rs_doc.get_new_id(1)
            #id = (f'{id:04}')
            id = "{0:0>4}".format(id)
        else:
            id = fld_number

        try:
            ui_global.Rs_doc.add('01', (id,
                                        type,
                                        id, #hashMap.get('fld_number')
                                        hashMap.get('fld_data'),
                                        ui_global.get_by_name(hashMap.get('fld_countragent'), 'RS_countragents'),
                                        ui_global.get_by_name(hashMap.get('doc_warehouse'), 'RS_warehouses')))
            hashMap.put('ShowScreen', 'Документы')
        except:
            hashMap.put('toast', 'Номер документа неуникален!')


    elif listener == 'btn_cancel':
        hashMap.put('ShowScreen', 'Документы')
    elif listener == 'fld_data':
        hashMap.put('doc_date', hashMap.get('fld_data'))
    elif listener == 'ON_BACK_PRESSED':
        hashMap.put("ShowScreen", "Документы")
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

    if hashMap.get('listener') == 'ON_BACK_PRESSED':
        hashMap.put("ShowScreen", "Документ товары")
    return hashMap
