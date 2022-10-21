from pony.orm import Database, Required, PrimaryKey, Optional
import datetime
import sqlite3
from sqlite3 import Error
import ui_barcodes
import os

import ui_form_data

# Вот таким незатейливым методом определяем, мы запустились на компе или на ТСД
# Ну и в зависимости от, используем базу
if os.path.exists('//data/data/ru.travelfood.simple_ui/databases/'):
    db_path = '//data/data/ru.travelfood.simple_ui/databases/SimpleWMS'
else:
    db_path = 'D:\PythonProjects\RightScan\SUImain\SimpleWMS.db'

db = Database()
db.bind(provider='sqlite', filename=db_path, create_db=True)


# Штрихкоды barcode, id_good, id_property, id_unit
class RS_barcodes(db.Entity):
    barcode = Required(str)  # , lenght=200)
    id_good = Required(str)  # , lenght=36)
    id_property = Optional(str)  # , lenght=36)
    id_series = Optional(str)
    id_unit = Optional(str)  # , lenght=36)


# Номенклатура
class RS_goods(db.Entity):
    id_elem = PrimaryKey(str)  # , lenght=36)
    code = Required(str)
    name = Optional(str)
    art = Optional(str)
    unit = Optional(str)
    type_good = Optional(str)  # Вид номенклатуры
    description = Optional(str)


# Характеристики номенклатуры
class RS_properties(db.Entity):
    id_elem = Required(str)  # , lenght=36)
    id_owner = Required(str)  # , lenght=36)  # id Номенклатуры
    name = Optional(str)


# Упаковки Единицы измерения
class RS_units(db.Entity):
    id_elem = PrimaryKey(str)
    id_owner = Required(str)  # , lenght=36)  # id Номенклатуры
    code = Required(str)
    name = Optional(str)
    nominator = Required(int)  # Числитель
    denominator = Required(int)  # Знаменатель
    int_reduction = Optional(str)  # Международное сокращение


# Виды номенклатуры
class RS_types_goods(db.Entity):
    id_elem = PrimaryKey(str)  # , lenght=36)
    name = Optional(str)


# Серии номенклатуры
class RS_series(db.Entity):
    id_elem = PrimaryKey(str)
    name = Optional(str)
    best_before = Optional(str)  # Годен до
    type_goods = Optional(str)  # Вид номенклатуры (id RS_types_goods )
    number = Optional(str)
    production_date = Optional(str)  # Дата производства


# Контрагенты
class RS_countragents(db.Entity):
    id_elem = PrimaryKey(str)
    name = Optional(str)
    full_name = Optional(str)
    inn = Optional(str)
    kpp = Optional(str)


# Склады
class RS_warehouses(db.Entity):
    id_elem = PrimaryKey(str)
    name = Optional(str)


# Классификатор единиц измерения
class RS_classifier_units(db.Entity):
    id_elem = PrimaryKey(str)  # , lenght=36)
    code = Required(str)
    name = Required(str)


# Виды цен номенклатуры
class RS_price_types(db.Entity):
    id = PrimaryKey(str)
    name = Required(str)


# Цены номенклатуры
class RS_prices(db.Entity):
    id_price_types = Required(str)
    id_goods = Required(str)
    id_properties = Optional(str)
    price = Optional(float)
    id_unit = Optional(str)


# Все документы списком
class RS_docs(db.Entity):
    # id_doc, doc_type, doc_n, doc_data, good_id, good_mame, ed_izm, qtty, qtty_fact
    id_doc = PrimaryKey(str)
    doc_type = Required(str)
    doc_n = Required(str)
    doc_data = Required(str)
    id_countragents = Optional(str)
    id_warehouse = Optional(str)
    verified = Optional(int, sql_default=0)
    sent = Optional(int, sql_default=0)
    created_at = Optional(datetime.datetime, sql_default='CURRENT_TIMESTAMP')


# Табличная часть документов
class RS_docs_table(db.Entity):
    id_doc = Required(str)
    id_good = Optional(str)
    id_properties = Optional(str)
    id_series = Optional(str)
    id_unit = Optional(str)
    qtty = Optional(float, sql_default=0)
    qtty_plan = Optional(float, sql_default=0)
    price = Optional(float, sql_default=0)
    id_price = Optional(str)
    sent = Optional(int, sql_default=0)


class RS_docs_barcodes(db.Entity):
    id_doc = Required(str)
    barcode = Required(str)
    id_barcode = Required(str)
    barcode_from_scanner = Optional(str, nullable=True)
    id_good = Optional(str,nullable=True)
    is_plan = Required(str, sql_default='0')
    approved = Optional(str, sql_default='0', nullable=True)


class RS_constants(db.Entity):
    use_series = Required(str, sql_default='0')
    use_properties = Required(str, sql_default='0')
    use_mark = Required(str, sql_default='0')
    path = Required(str)  # Путь к папке обмена
    delete_files = Required(str, sql_default='0')  # Признак, удалять файлы обмена после обмена из папки обмена
    reserved = Optional(str)


db.generate_mapping(create_tables=True)
db.disconnect


# Описание объектов базы и их изменение

class Rs_doc():
    id_doc = Optional(str)
    id_str = Optional(str)
    qtty = Optional(float)

    def update_doc_str(self, price=0):
        query = """
        UPDATE RS_docs_table
        SET qtty=?, price=?
        Where id=? """
        res = get_query_result(query, (self.qtty, price, self.id_str))
        return res

    def delete_doc(self):
        query_doc_table = 'DELETE FROM RS_docs_table WHERE id_doc = ?'
        get_query_result(query_doc_table, (self.id_doc,))
        query_doc = 'DELETE FROM RS_docs WHERE id_doc = ?'
        res = get_query_result(query_doc, (self.id_doc,))

        return res

    def mark_for_upload(self):
        query = """
        UPDATE RS_docs_table
        SET sent=1
        Where id=? """
        res = get_query_result(query, (self.id_doc))

        return res

    def mark_verified(self, key):
        query = """
                UPDATE RS_docs
                SET verified=?
                Where id_doc=? """
        res = get_query_result(query, (int(key), self.id_doc))

    def find_barcode_in_table(self, search_value: str, func_compared='=?') -> object:

        query = '''
                 SELECT
                 RS_barcodes.id_good,
                 RS_barcodes.id_property,
                 RS_barcodes.id_unit,
                 RS_docs_table.id,
                 RS_docs_table.qtty        
                 FROM RS_barcodes
                 Left join RS_docs_table ON
                 RS_docs_table.id_good= RS_barcodes.id_good and
                 RS_docs_table.id_properties= RS_barcodes.id_property and
                 RS_docs_table.id_unit= RS_barcodes.id_unit And
                 RS_docs_table.id_doc=?
                 where barcode ''' + func_compared
        # query = query + func_compared

        return get_query_result(query, (self.id_doc, search_value))

    def update_rs_doc_table(self, tbl_struct):
        pass

    def update_doc_table_data_from_barcode(self, el: dict):
        # Сначала определим, есть ли в списке товаров документа наш товар:
        qtext = 'Select * from RS_docs_table Where id_doc=? and id_good = ? and id_properties = ? and id_series = ? and id_unit = ?'
        args = (self.id_doc, el['id_good'],el['id_property'],el['id_series'], el['id_unit'])
        res = get_query_result(qtext,args, True)
        if res: #Нашли строки документа, добавляем количество
            el = res[0]
            qtext = 'UPDATE RS_docs_table SET qtty=qtty+? WHERE id = ?'
            get_query_result(qtext, (1, el['id']))
        else: #Такой строки нет, надо добавить
            qtext = 'REPLACE INTO RS_docs_table(id_doc, id_good, id_properties,id_series, id_unit, qtty, price, id_price) VALUES (?,?,?,?,?,?,?,?)'
            get_query_result(qtext, (self.id_doc, el['id_good'],el['id_properties'],el['id_series'], el['id_unit'], 1, 0, ''))


        return res

    def find_barcode_on_doc(self, barcode):
        # Получим структуру баркода
        barcode_info = ui_barcodes.parse_barcode(barcode)
        # ... и найдем по нему все что есть в базе
        shema = barcode_info['SCHEME']

        if get_constants('use_mark') == 'true':
            if shema == 'GS1':
                barcode_info['FullBarcode'] = barcode
                res = find_barcode_in_barcode_table(self, barcode_info)  # получает несколько строк:
                # 1 - по полному совпадению GTIN и серия, ссылка на товар
                # 2 - по совпадению GTIN и ссылка на товар
                if res:  # нашли записи по баркоду в документе
                    for el in res:
                        if el['TypeOfUnion'] == 'FullMatch' and el['GTIN'] and el['id_good']:  # нашли строку по полному совпадению GTIN и серия, ссылка на товар
                            if el['approved'] == '1':  # Такая марка уже была отсканирована
                                return {'Error': 'Такая марка уже была отсканирована', 'Barcode': barcode_info}
                            if el['is_plan'] == '1':  # товар был выгружен из учетной системы, надо только подтвердить строку и заполнить код со сканера
                                query_text = 'Update  RS_docs_barcodes SET approved=?, barcode_from_scanner=? Where id=?'
                                get_query_result(query_text, ('1', barcode, int(el['id'])))
                                self.update_rs_doc_table(self,self.update_doc_table_data_from_barcode(self, el))
                                return {'Result':'Все ок', 'Error':None}
                            else:
                                pass  # Добавляем строку


                        elif el['TypeOfUnion'] == 'On_GTIN' and el['GTIN']:  # нашли строку только по  совпадению GTIN ,
                            pass  # Ситуация, когда надо добавить GTIN и серию в строку, пока не делаем
                        else:  # Ничего в таблице не нашли, добавляем строку
                            pass  # реализовать
                else: #Записей в документе нет, добавляем
                    return {'Error': 'Марка не найдена в документе', 'Barcode': barcode_info}




        else:

            search_value = ''
            if shema in ['EAN13', 'UNKNOWN']:
                search_value = barcode_info['BARCODE']
                res = self.find_barcode_in_table(self, search_value)
            elif shema == 'GS1':

                search_value = '01' + barcode_info['GTIN'] + '21' + barcode_info['SERIAL']
                res = self.find_barcode_in_table(self, search_value)

            if not len(res) == 0:
                elem = res[0]
            else:  # Ничего не нашли, пробуем искать только по GTIN
                #            search_value = '01' + barcode_info['GTIN'][1:14] # + '%' #'21%'
                search_value = barcode_info['GTIN'] + '%'
                res = self.find_barcode_in_table(self, search_value, 'LIKE ?')
                if not len(res) == 0:

                    elem = res[0]
                else:  # Такого товара в базе нет
                    return None

            if elem[3] == None:
                query = 'REPLACE INTO RS_docs_table(id_doc, id_good, id_properties,id_series, id_unit, qtty, price, id_price) VALUES (?,?,?,?,?,?,?,?)'
                get_query_result(query, (self.id_doc, elem[0], elem[1], '', elem[2], 1, 0, ''))
            else:
                query = 'UPDATE RS_docs_table SET qtty=qtty+? WHERE id = ?'
                get_query_result(query, (1, elem[3]))
            return {'Result':'Все ок', 'Error':None}

    def add(self, args):
        query = 'INSERT INTO RS_docs(id_doc, doc_type, doc_n, doc_data, id_countragents, id_warehouse, verified, sent) VALUES (?,?,?,?,?,?,1,1)'
        res = get_query_result(query, args)

    def get_new_id(self):
        query = 'Select max(id_doc) From(Select id_doc from RS_docs WHERE id_doc<10000)'
        res = get_query_result(query)
        if len(res) == 0:
            return '001'
        else:
            return str(int(res[0][0]) + 1)


def find_barcode_in_barcode_table(self, struct_barcode: list) -> object:
    query_text = ui_form_data.get_query_mark_find_in_doc()
    args_dict={}
    args_dict['set_barcode']  = '01' + struct_barcode['GTIN'] + '21' + struct_barcode['SERIAL']
    args_dict['gtin'] = struct_barcode['GTIN']
    args_dict['id_doc']= self.id_doc

    res = get_query_result(query_text, args_dict, True)
    return res


def get_query_result(query_text: object, args: object = "", return_dict = False) -> object:
    # **********************

    conn = None
    try:
        conn = sqlite3.connect(db_path)

    except Error:
        raise ValueError('No connection with database')

    cursor = conn.cursor()
    if args:
        cursor.execute(query_text, args)
    else:
        cursor.execute(query_text)
#Если надо - возвращаем не результат запроса, а словарь с импортированным результатом
    if return_dict:
        res = [dict(line) for line in
                        [zip([column[0] for column in cursor.description], row) for row in cursor.fetchall()]]
    else:
        res = cursor.fetchall()
    conn.commit()
    conn.close()
    return res


def bulk_query_replace(query_text: str, args: object = "") -> object:
    # **********************

    conn = None
    try:
        conn = sqlite3.connect(db_path)

    except Error:
        raise ValueError('No connection with database')

    cursor = conn.cursor()
    try:
        cursor.executemany(query_text, args)
        conn.commit()
    except sqlite3.Error as er:
        raise ValueError(er)

    res = cursor.fetchall()

    conn.close()
    return res


def get_name_list(str_entty):
    query = "SELECT name FROM " + str_entty
    res = get_query_result(query)
    list_el = []
    # list_el.append(name for name in res)
    for el in res:
        list_el.append(el[0])
    return ";".join(list_el)


def get_by_name(fld, table):
    query = "SELECT id_elem FROM " + table + ' WHERE name = ?'
    res = get_query_result(query, (fld,))

    if len(res) == 0:
        return ""
    else:
        return res[0][0]


def get_constants(need_const=''):
    sql_text = 'Select * from RS_constants'
    res = get_query_result(sql_text)

    # инициализируем константы
    if not res:  # len(res) == 0:
        get_query_result(
            'INSERT INTO RS_constants (use_series, use_properties, use_mark, path, delete_files, reserved) VALUES (?,?,?,?,?,?)',
            ('0', '0', '0', '//storage/emulated/0/download/', '0', '0'))

        res = get_query_result(sql_text)

    if res:  # len(res)>0:
        if need_const:
            ls = ['id', 'use_series', 'use_properties', 'use_mark', 'path', 'delete_files', 'reserved']
            x = ls.index(need_const)

            if x > 0:
                return res[0][x]
        else:
            return res[0]
    else:
        return None


def put_constants(args):
    sql_update_query = """Update RS_constants set use_series = ?, use_properties = ?, use_mark = ?, path = ?,
     delete_files = ? """
    res = get_query_result(sql_update_query, args)





