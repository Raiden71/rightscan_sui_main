class RS_barcodes(db.Entity):
    barcode = Required(str)  # , lenght=200) Также GTIN
    id_good = Required(str)  # , lenght=36)
    id_property = Optional(str)  # , lenght=36)
    id_series = Optional(str)
    id_unit = Optional(str)  # , lenght=36)


#
class RS_marking_codes(db.Entity):
    id = PrimaryKey(str)
    mark_code = Required(str)  # КОд маркировки формата 01+GTIN+21+SERIAL
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
    add_mark_selection = Optional(int,sql_default=0)
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
    last_updated = Optional(datetime.datetime, sql_default='CURRENT_TIMESTAMP')


class RS_docs_barcodes(db.Entity):
    id_doc = Required(str)
    #    barcode = Required(str)
    id_barcode = Required(str)
    barcode_from_scanner = Optional(str, nullable=True)
    #    id_good = Optional(str,nullable=True)
    is_plan = Required(str, sql_default='0')
    approved = Optional(str, sql_default='0', nullable=True)


class RS_constants(db.Entity):
    use_series = Required(str, sql_default='0')
    use_properties = Required(str, sql_default='0')
    use_mark = Required(str, sql_default='0')
    path = Required(str)  # Путь к папке обмена
    delete_files = Required(str, sql_default='0')  # Признак, удалять файлы обмена после обмена из папки обмена
    reserved = Optional(str)