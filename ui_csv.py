import csv
import os
import re

import ui_barcodes
import ui_global
from datetime import datetime


def get_query_text(q_name='') -> str:
    if q_name == 'RS_goods':
        return 'REPLACE INTO RS_goods (id_elem, code, art, name, unit, type_good, description) VALUES (?,?,?,?,?,?,?)'
    elif q_name == 'RS_properties':
        return 'REPLACE INTO RS_properties (id_elem , id_owner, name) VALUES '
    elif q_name == 'RS_units':
        return 'REPLACE INTO RS_units (id_elem,id_owner, code, name, nominator, denominator, int_reduction) VALUES (?,?,?,?,?,?,?)'
    elif q_name == 'RS_types_goods':
        return 'REPLACE INTO RS_types_goods (id_elem, name) VALUES (?,?)'  # (?,?)
    elif q_name == 'RS_series':
        return 'REPLACE INTO RS_series (id_elem, name, best_before, type_goods, number, production_date) VALUES'
    elif q_name == 'RS_countragents':
        return 'REPLACE INTO RS_countragents (id_elem, name, full_name, inn, kpp) VALUES '
    elif q_name == 'RS_warehouses':
        return 'REPLACE INTO RS_warehouses (id_elem, name) VALUES (?,?)'
    elif q_name == 'RS_price_types':
        return 'REPLACE INTO RS_price_types (id, name) VALUES (?,?)'
    elif q_name == 'RS_barcodes':
        return 'REPLACE INTO RS_barcodes (barcode, id_good, id_property, id_series, id_unit) VALUES (?,?,?,?,?)'
    elif q_name == 'RS_prices':
        return 'REPLACE INTO RS_prices (id_price_types, id_goods, id_properties, price, id_unit) VALUES '
    elif q_name == 'RS_docs':
        return 'REPLACE INTO RS_docs (id_doc, doc_type, doc_n, doc_data, id_countragents, id_warehouse) VALUES (?,?,?,?,?,?)'
    elif q_name == 'RS_docs_table':
        return 'REPLACE INTO RS_docs_table (id_doc, id_good, id_properties, id_series, id_unit, qtty, qtty_plan, price, id_price) VALUES (?,?,?,?,?,?,?,?,?)'
    elif q_name == 'RS_docs_barcodes':
        return 'REPLACE INTO RS_docs_barcodes (id_doc, barcode, id_barcode,id_good, is_plan) VALUES (?,?,?,?,?)'


def get_query_text_export():
    return '''
    SELECT 
'0' AS GTIN,
RS_docs_barcodes.id_good,
RS_goods.name,
1 as DeclaredQuantity,
CASE approved
    WHEN '1' THEN 1
    ELSE 0
END AS CurrentQuantity,
barcode_from_scanner as Марка,
barcode AS МаркаИСМП,
RS_docs_barcodes.id_doc as Инвойс,
'Чужой' as Принадлежность 
FROM RS_docs_barcodes 
LEFT JOIN RS_docs_table
ON RS_docs_table.id_doc =RS_docs_barcodes.id_doc 
AND  RS_docs_table.id_good =RS_docs_barcodes.id_good
 
LEFT JOIN RS_goods 
ON RS_goods.id_elem = RS_docs_barcodes.id_good
'''

def normalize_gtin(gtin: str) -> str:
    a = len(gtin)
    if a > 14:
        return gtin[:-14]
    else:
        return '0' * (14 - a) + gtin


def load_from_csv(path='', file=''):
    # re.fullmatch(r'\d{13}', barcode).string == barcode:
    current_date = datetime.now().strftime("%d-%m-%Y")
    #file = file + (" " * 15) #чтобы не натыкаться на out of range в текстовом имени - добавим 15 пробелов
    if file[:6] == 'doc_in':
        # Загружаем документы
        with open(path, 'r', newline='', encoding='utf-8') as csvfile:

            my_reader = csv.reader(csvfile, dialect='excel', delimiter=';', quotechar='"')

            rs_doc_data = []
            rs_doc_table_data = []
            rs_doc_barcode = []
            temp_doc_n = ''
            temp_good =''
            doc_num = ui_global.Rs_doc.get_new_id()
            for row in my_reader:
                if my_reader.line_num > 5:  # Заголовки таблицы
                    if temp_doc_n != row[8]:
                        # RS_docs (id_doc, doc_type, doc_n, doc_data, id_countragents, id_warehouse)
                        rs_doc_data.append((doc_num, 'Инвойс', doc_num, current_date, '001', '001'))
                        temp_doc_n = row[8]
                    # RS_docs_table(id_doc, id_good, id_properties, id_series, id_unit, qtty, qtty_plan, price, id_price)
                    if temp_good != row[0]:
                        rs_doc_table_data.append((temp_doc_n, row[0], '', '', row[1], int(row[7]), int(row[6]), '', ''))
                        curr_count = rs_doc_table_data.__len__()-1
                        temp_good = row[0]
                    else:
                        #добавим количество в строку, для этого преобразуем ее в Лист, поменяем количество и засунем обратно в кортеж
                        lst = list(rs_doc_table_data[curr_count])
                        lst[6]=int(lst[6])+int(row[6])
                        rs_doc_table_data[curr_count] = tuple(lst)
                        #rs_doc_table_data[curr_count][6]=int(rs_doc_table_data[curr_count][6]) + int(row[6])

                    # RS_docs_barcodes (id_doc, barcode, id_barcode, id_good,  approved)
                    rs_doc_barcode.append((temp_doc_n, row[5], row[5], row[0], '1'))

                elif my_reader.line_num == 5:
                    list_headers = row.copy()

        # Заполняем таблицы
        ui_global.bulk_query_replace(get_query_text('RS_docs'), rs_doc_data)
        ui_global.bulk_query_replace(get_query_text('RS_docs_table'), rs_doc_table_data)
        ui_global.bulk_query_replace(get_query_text('RS_docs_barcodes'), rs_doc_barcode)

    elif file[:14] == 'initial_dicts_':
        with open(path, 'r', newline='', encoding='utf-8') as csvfile:

            my_reader = csv.reader(csvfile, dialect='excel', delimiter=';', quotechar='"')

            rs_goods_data = []
            rs_barcodes_data = []
            rs_units_data = []
            # RS_warehouses(id_elem, name)
            rs_warehouses = [['001', 'Основной']]
            # RS_types_goods (id_elem, name)
            rs_types_goods_data = [['001', 'Товар']]
            part_count = 1000

            for row in my_reader:
                if my_reader.line_num == 1:  # Заголовки таблицы
                    list_headers = row.copy()
                elif my_reader.line_num == part_count:
                    part_count += 1000
                    ui_global.bulk_query_replace(get_query_text('RS_goods'), rs_goods_data)
                    ui_global.bulk_query_replace(get_query_text('RS_units'), rs_units_data)
                    ui_global.bulk_query_replace(get_query_text('RS_barcodes'), rs_barcodes_data)
                    rs_goods_data = []
                    rs_barcodes_data = []
                    rs_units_data = []

                else:  # заполняем таблицы параметров запроса к SQL
                    # id_elem, code, art, name, unit, type_good, description
                    rs_goods_data.append((row[2], row[3], row[5], row[4], row[1], '001', row[15]))
                    # id_elem, id_owner, code, name, nominator, denominator, int_reduction
                    rs_units_data.append((row[2], row[2], row[1], row[1], 1, 1, row[1]))
                    # barcode, id_good, id_property, id_series, id_unit
                    rs_barcodes_data.append((normalize_gtin(row[0]), row[2], '', '', row[1]))

        ui_global.bulk_query_replace(get_query_text('RS_goods'), rs_goods_data)
        ui_global.bulk_query_replace(get_query_text('RS_units'), rs_units_data)
        ui_global.bulk_query_replace(get_query_text('RS_barcodes'), rs_barcodes_data)


        return 200

def list_folder(path: str, delete_files: bool):
    #try:
    aa=0
    total = 0
    for file in os.listdir(path):
        total += 1
        if file.endswith(".csv"):
            filename = file + (" " * 15)  #чтобы не натыкаться на out of range в текстовом имени - добавим 15 пробелов
            if filename[:6] == 'doc_in' or filename[:14] == 'initial_dicts_':
                aa +=1
                ans = load_from_csv(path+file,file)
                if ans == 200 and delete_files=='true':
                    os.remove(path + file )

    return 'Загрузка завершена, загружено '+ str(aa)+' файлов из ' + str(total)
    #except:
     #   return 'Ошибка при загрузке файла'


def export_csv(path, IP, AndroidID):
    qtext = get_query_text_export()
    res = ui_global.get_query_result(qtext,'',True)

    with open(path + 'doc_out.csv', 'w', newline='', encoding='utf-8') as csvfile:
        my_reader = csv.writer(csvfile, dialect='excel', delimiter=';', quotechar='"')
        my_reader.writerow(('Name','UserName','DeviceId','DeviceIP'))
        my_reader.writerow(('Приход на склад 13862', 'Москва1',AndroidID,IP))
        my_reader.writerow(('GTIN','КодВУчетнойСистеме','Наименование','DeclaredQuantity','CurrentQuantity','Коробка','Марка','МаркаИСМП','Инвойс','Принадлежность'))
        for el in res:
            gtin = ui_barcodes.get_gtin_serial_from_datamatrix(el['МаркаИСМП'])
            el['GTIN']=gtin['GTIN']
            my_reader.writerow((el['GTIN'],el['id_good'],el['name'],el['DeclaredQuantity'], el['CurrentQuantity'], el['Марка'],el['МаркаИСМП'], el['Инвойс'],el['Принадлежность']))


#export_csv('ОбменТСД/НА/') #'





# open_files_net('', 'D:/PythonProjects/RightScan/SUImain/ОбменТСД/НА/initial_dicts_01.csv', 'initial_dicts_01.csv')
# open_files_net('', 'D:/PythonProjects/RightScan/SUImain/ОбменТСД/НА/doc_1.csv','doc_1.csv')
