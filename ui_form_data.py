def get_doc_card():
    doc_list = {"customcards": {
        "options": {
            "search_enabled": True,
            "save_position": True
        },
        "layout": {
            "Value": "",
            "Variable": "",
            "type": "LinearLayout",
            "weight": "0",
            "height": "wrap_content",
            "width": "match_parent",
            "orientation": "vertical",
            "Elements": [
                {
                    "type": "LinearLayout",
                    "height": "wrap_content",
                    "width": "match_parent",
                    "weight": "0",
                    "Value": "",
                    "Variable": "",
                    "orientation": "horizontal",
                    "Elements": [
                        {
                            "type": "CheckBox",
                            "Value": "@completed",
                            "Variable": "CheckBox1",
                            "TextSize": "32",
                            "NoRefresh": False,
                            "document_type": "",
                            "mask": "",
                            "BackgroundColor": "#DB7093",
                            "width": "match_parent",
                            "height": "wrap_content",
                            "weight": 2
                        },
                        {
                            "type": "TextView",
                            "height": "wrap_content",
                            "width": "wrap_content",
                            "weight": "0",
                            "Value": "@type",
                            "Variable": "",
                            "TextSize": "18"
                        },
                        {
                            "type": "PopupMenuButton",
                            "show_by_condition": "",
                            "Value": "Удалить;Подтвердить",
                            "NoRefresh": False,
                            "document_type": "",
                            "mask": "",
                            "Variable": "menu_delete"

                        }

                    ]
                },
                {
                    "type": "LinearLayout",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "",
                    "Variable": "",
                    "orientation": "horizontal",
                    "Elements": [
                        {
                            "type": "TextView",
                            "height": "wrap_content",
                            "width": "wrap_content",
                            "weight": "0",
                            "Value": "@number",
                            "Variable": "",
                            "TextBold": True,
                            "TextSize": "20"
                        },
                        {
                            "type": "TextView",
                            "height": "wrap_content",
                            "width": "wrap_content",
                            "weight": "0",
                            "Value": "@data",
                            "Variable": ""
                        }
                    ]
                },
                {
                    "type": "LinearLayout",
                    "height": "wrap_content",
                    "width": "wrap_content",
                    "weight": "0",
                    "Value": "",
                    "Variable": "",
                    "orientation": "vertical",
                    "Elements": [
                        {
                            "type": "TextView",
                            "height": "wrap_content",
                            "width": "wrap_content",
                            "weight": "0",
                            "Value": "@countragent",
                            "Variable": ""
                        },
                        {
                            "type": "TextView",
                            "height": "wrap_content",
                            "width": "wrap_content",
                            "weight": "0",
                            "Value": "@warehouse",
                            "Variable": ""
                        }
                    ]
                }
            ]
        }
    }}

    return doc_list


def get_doc_query(arg=''):
    query_text = """
    SELECT RS_docs.id_doc,
    RS_docs.doc_type,
    RS_docs.doc_n,
    RS_docs.doc_data,
    RS_docs.id_countragents,
    RS_docs.id_warehouse,
    ifnull(RS_countragents.full_name,'') as RS_countragent,
    ifnull(RS_warehouses.name,'') as RS_warehouse,
    RS_docs.verified,
    RS_docs.sent,
    RS_docs.add_mark_selection
    
     FROM RS_docs
     LEFT JOIN RS_countragents as RS_countragents
     ON RS_countragents.id_elem = RS_docs.id_countragents
     LEFT JOIN RS_warehouses as RS_warehouses
     ON RS_warehouses.id_elem=RS_docs.id_warehouse
     """
    if not (arg == '' or arg == 'Все'):
        query_text = query_text + '''
        Where RS_docs.doc_type=?'''

    query_text = query_text + """
    ORDER
    BY
    RS_docs.doc_data"""
    return query_text


def get_doc_type_query():
    ls = 'SELECT DISTINCT doc_type from RS_docs'
    return ls


# -----------------------------------------Товары
def get_goods_card():
    list = {"customcards": {
        "options": {
            "search_enabled": True,
            "save_position": True
        },
        "layout": {
            "type": "LinearLayout",
            "orientation": "vertical",
            "height": "match_parent",
            "width": "match_parent",
            "weight": "0",
            "Elements": [
                {
                    "type": "LinearLayout",
                    "orientation": "horizontal",
                    "height": "match_parent",
                    "width": "match_parent",
                    "weight": "0",
                    "Elements": [

                        {
                            "type": "LinearLayout",
                            "orientation": "vertical",
                            "height": "wrap_content",
                            "width": "match_parent",
                            "weight": "1",
                            "Elements": [
                                {
                                    "type": "TextView",
                                    "TextSize": "18",
                                    "TextBold": True,
                                    "show_by_condition": "",
                                    "Value": "@name",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": ""
                                },
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@code",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": ""
                                },
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@GTIN",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": ""
                                },
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@type_name",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": ""
                                },
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@unit_name",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": ""
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    }
    }
    return list


def get_goods_query():
    query_text = """
    SELECT RS_goods.id_elem,
    RS_goods.code,
    RS_goods.art,
    RS_goods.name,
    RS_goods.type_good,
    RS_types_goods.name AS types_goods,
    RS_goods.unit,
    RS_units.name
    FROM RS_goods
    LEFT JOIN RS_types_goods
    ON RS_types_goods.id_elem = RS_goods.type_good
    LEFT JOIN RS_units
    ON RS_units.id_owner = RS_goods.id_elem"""
    return query_text


def get_price_card():
    txt = {"customcards": {
        "options": {
            "search_enabled": False,
            "save_position": True
        },
        "type": "LinearLayout",
        "weight": "0",
        "height": "wrap_content",
        "width": "match_parent",
        "orientation": "vertical",
        "Elements": [
            {
                "type": "LinearLayout",
                "height": "wrap_content",
                "width": "match_parent",
                "weight": "0",
                "Value": "",
                "Variable": "",
                "orientation": "vertical",
                "Elements": [
                    {
                        "type": "TextView",
                        "height": "wrap_content",
                        "width": "wrap_content",
                        "weight": "2",
                        "Value": "@price_type",
                        "Variable": ""
                    },
                    {
                        "type": "TextView",
                        "height": "wrap_content",
                        "width": "wrap_content",
                        "weight": "1",
                        "Value": "@price",
                        "Variable": ""
                    }
                ]
            }
        ]
    }
    }
    return txt


def get_doc_details_query():
    query_text = """
    SELECT
    RS_docs_table.id,
    RS_docs_table.id_doc,
    RS_docs_table.id_good,
    RS_goods.name,
    RS_docs_table.id_properties,
    RS_properties.name,
    RS_docs_table.id_series,
    RS_series.name,
    RS_docs_table.id_unit,
    RS_units.name,
    RS_docs_table.qtty,
    RS_docs_table.qtty_plan,
    RS_docs_table.price,
    RS_price_types.name as price_name,
    RS_docs_table.qtty_plan - RS_docs_table.qtty as IsDone
    FROM RS_docs_table 
    
    
    
    LEFT JOIN RS_goods 
    ON RS_goods.id_elem=RS_docs_table.id_good
    LEFT JOIN RS_properties
    ON RS_properties.id_elem = RS_docs_table.id_properties
    LEFT JOIN RS_series
    ON RS_series.id_elem = RS_docs_table.id_series
    LEFT JOIN RS_units
    ON RS_units.id_elem=RS_docs_table.id_unit
    LEFT JOIN RS_price_types
    ON RS_price_types.id = RS_docs_table.id_price
    WHERE id_doc = $arg1
    ORDER BY RS_docs_table.last_updated DESC 
    """
    return query_text


def get_doc_detail_cards(use_series, use_properties):

    list = {
        "customcards": {
            "options": {
                "search_enabled": True,
                "save_position": True
            },
            "layout": {
                "type": "LinearLayout",
                "orientation": "vertical",
                "height": "match_parent",
                "width": "match_parent",
                "weight": "0",
                "Elements": [
                    {
                        "type": "LinearLayout",
                        "orientation": "horizontal",
                        "height": "match_parent",
                        "width": "match_parent",
                        "weight": "0",
                        "Elements": [

                            {
                                "type": "LinearLayout",
                                "orientation": "vertical",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "1",
                                "Elements": [
                                    {
                                        "type": "LinearLayout",
                                        "orientation": "horizontal",
                                        "height": "match_parent",
                                        "width": "match_parent",
                                        "weight": "0",
                                        "Elements": [
                                            {
                                                "type": "TextView",
                                                "TextSize": "18",
                                                "TextBold": True,
                                                "show_by_condition": "",
                                                "Value": "@good_name",
                                                "NoRefresh": False,
                                                "document_type": "",
                                                "mask": "",
                                                "weight": "1",
                                                "Variable": ""
                                            },
                                            {
                                                "type": "Button",
                                                "show_by_condition": "",
                                                "Value": "@picture",
                                                "TextColor": "#DB7093",
                                                "BackgroundColor": "#FFFFFF",
                                                "Variable": "btn_tst1",
                                                "NoRefresh": False,
                                                "document_type": "",
                                                "cardCornerRadius": "15dp",
                                                "weight": "1",
                                                "mask": ""
                                            }]
                                    },

                                    {
                                        "type": "TextView",
                                        "show_by_condition": "",
                                        "Value": "@code_art",
                                        "NoRefresh": False,
                                        "document_type": "",
                                        "mask": "",
                                        "Variable": ""
                                    },

                                    {
                                        "type": "TextView",
                                        "show_by_condition": "",
                                        "Value": "@unit_name",
                                        "NoRefresh": False,
                                        "document_type": "",
                                        "mask": "",
                                        "Variable": ""
                                    },
                                    {
                                        "type": "LinearLayout",
                                        "orientation": "gorizontal",
                                        "height": "match_parent",
                                        "width": "match_parent",
                                        "weight": "1",
                                        "Elements": [
                                            {
                                                "type": "LinearLayout",
                                                "orientation": "vertical",
                                                "height": "wrap_content",
                                                "width": "match_parent",
                                                "weight": "1",
                                                "Elements": [
                                                    {
                                                        "type": "TextView",
                                                        "show_by_condition": "",
                                                        "Value": "План",
                                                        "NoRefresh": False,
                                                        "document_type": "",
                                                        "mask": "",
                                                        "Variable": ""
                                                    },
                                                    {
                                                        "type": "TextView",
                                                        "show_by_condition": "",
                                                        "Value": "@qtty_plan",
                                                        "NoRefresh": False,
                                                        "document_type": "",
                                                        "TextSize": "18",
                                                        "mask": "",
                                                        "Variable": ""
                                                    }
                                                ]
                                            },
                                            {
                                                "type": "LinearLayout",
                                                "orientation": "vertical",
                                                "height": "wrap_content",
                                                "width": "match_parent",
                                                "weight": "1",
                                                "Elements": [
                                                    {
                                                        "type": "TextView",
                                                        "show_by_condition": "",
                                                        "Value": "Факт",
                                                        "NoRefresh": False,
                                                        "document_type": "",
                                                        "mask": "",
                                                        "Variable": ""
                                                    },
                                                    {
                                                        "type": "TextView",
                                                        "show_by_condition": "",
                                                        "Value": "@qtty",
                                                        "NoRefresh": False,
                                                        "document_type": "",
                                                        "TextSize": "18",
                                                        "mask": "",
                                                        "Variable": ""
                                                    }
                                                ]
                                            },
                                            {
                                                "type": "LinearLayout",
                                                "orientation": "vertical",
                                                "height": "wrap_content",
                                                "width": "match_parent",
                                                "weight": "1",
                                                "Elements": [
                                                    {
                                                        "type": "TextView",
                                                        "show_by_condition": "",
                                                        "Value": "Цена",
                                                        "NoRefresh": False,
                                                        "document_type": "",
                                                        "mask": "",
                                                        "Variable": ""
                                                    },
                                                    {
                                                        "type": "TextView",
                                                        "show_by_condition": "",
                                                        "Value": "@price",
                                                        "NoRefresh": False,
                                                        "document_type": "",
                                                        "TextSize": "18",
                                                        "mask": "",
                                                        "Variable": ""
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    }

    if use_series == 'true' or use_series == '1':
        list['customcards']['layout']['Elements'][0]['Elements'][0]['Elements'].insert(1, {'type': 'TextView',
                                                                                           'TextSize': '16',
                                                                                           'show_by_condition': '',
                                                                                           'Value': '@series_name',
                                                                                           'NoRefresh': False,
                                                                                           'document_type': '',
                                                                                           'mask': '', 'Variable': ''})
    if use_properties == 'true' or use_properties == '1':
        list['customcards']['layout']['Elements'][0]['Elements'][0]['Elements'].insert(1, {'type': 'TextView',
                                                                                           'TextSize': '16',
                                                                                           'show_by_condition': '',
                                                                                           'Value': '@properties_name',
                                                                                           'NoRefresh': False,
                                                                                           'document_type': '',
                                                                                           'mask': '', 'Variable': ''})

    return list


def get_price_query():
    txt = """
    SELECT *,
    RS_price_types.name
     from RS_prices 
     LEFT JOIN RS_price_types ON RS_price_types.id=RS_prices.id_price_types
     where id_goods=?"""
    return txt


# Современное поле ввода, не используется
def get_num_field_descr(qtty):
    json_descr = {
        "hint": 'количество',
        "default_text": qtty,
        'inputType ': 'TYPE_CLASS_NUMBER'
    }
    return json_descr


# -----------------------------------------Товары
def get_barcode_card():
    list = {"customcards": {
        "options": {
            "search_enabled": False,
            "save_position": True
        },
        "layout": {
            "type": "LinearLayout",
            "orientation": "vertical",
            "height": "match_parent",
            "width": "match_parent",
            "weight": "0",
            "Elements": [
                {
                    "type": "LinearLayout",
                    "orientation": "horizontal",
                    "height": "match_parent",
                    "width": "match_parent",
                    "weight": "0",
                    "Elements": [

                        {
                            "type": "TextView",
                            "height": "wrap_content",
                            "width": "wrap_content",
                            "weight": "0",
                            "Value": "@barcode_value",
                            "Variable": "barcode"
                        },
                        {
                            "type": "TextView",
                            "height": "wrap_content",
                            "width": "wrap_content",
                            "weight": "0",
                            "Value": "@approved",
                            "Variable": ""
                        }
                    ]
                }
            ]
        }

    }
    }
    return list


def get_barcode_query():
    query_text = 'SELECT * FROM RS_docs_barcodes Where RS_docs_barcodes.id_doc = ?'
    return query_text


# Запрос находит все записи таблицы документа RS_docs_barcodes по полному совпадению штрихкода или только по GTIN
def get_query_mark_find_in_doc():
    query = '''
SELECT * FROM (

SELECT 
RS_docs_barcodes.id,
RS_docs_barcodes.id_doc,

RS_docs_barcodes.id_barcode,

IFNULL(RS_marking_codes.mark_code, '0') AS mark_code,
IFNULL(RS_marking_codes.id_good, '') AS id_good,
IFNULL(RS_marking_codes.id_property, '') AS id_property ,
IFNULL(RS_marking_codes.id_series, '') AS id_series,
IFNULL(RS_marking_codes.id_unit, '')  AS id_unit,

RS_docs_barcodes.is_plan,
RS_docs_barcodes.approved

FROM RS_docs_barcodes
    
    LEFT JOIN RS_marking_codes As RS_marking_codes
    ON RS_marking_codes.id = RS_docs_barcodes.id_barcode

WHERE id_doc = :id_doc  and RS_marking_codes.mark_code = :set_barcode)
'''
    #
    # SELECT * FROM (
    #     SELECT
    #     'on_GTIN' as TypeOfUnion,
    #     RS_docs_barcodes.id,
    #     RS_docs_barcodes.id_doc,
    #     RS_docs_barcodes.barcode,
    #     RS_docs_barcodes.id_barcode,
    #     RS_barcodes.GTIN,
    #     RS_barcodes.id_good,
    #     RS_barcodes.id_property,
    #     RS_barcodes.id_series,
    #     RS_barcodes.id_unit,
    #     RS_docs_barcodes.is_plan,
    #     RS_docs_barcodes.approved
    #     FROM RS_docs_barcodes
    #         LEFT JOIN (Select RS_barcodes.barcode as GTIN,
    #         RS_barcodes.id_good,
    #         RS_barcodes.id_property,
    #         RS_barcodes.id_series,
    #         RS_barcodes.id_unit FROM RS_barcodes
    #         WHERE RS_barcodes.barcode=:gtin LIMIT 1) AS RS_barcodes
    #         ON TRUE
    #         LEFT JOIN RS_barcodes as FullBarcode
    #         ON FullBarcode.barcode = RS_docs_barcodes.barcode
    #
    #     WHERE id_doc = :id_doc  and RS_docs_barcodes.barcode Like '%'+:gtin + '%'
    #
    #     UNION ALL
    #
    #     SELECT
    #     'FullMatch',
    #     RS_docs_barcodes.id,
    #     RS_docs_barcodes.id_doc,
    #     RS_docs_barcodes.barcode,
    #     RS_docs_barcodes.id_barcode,
    #     IFNULL(RS_barcodes.barcode,RS_barcodes_inaccurate.GTIN),
    #     IFNULL(RS_barcodes.id_good,RS_barcodes_inaccurate.id_good),
    #     IFNULL(RS_barcodes.id_property,RS_barcodes_inaccurate.id_property),
    #     IFNULL(RS_barcodes.id_series,RS_barcodes_inaccurate.id_series),
    #     IFNULL(RS_barcodes.id_unit,RS_barcodes_inaccurate.id_unit),
    #     RS_docs_barcodes.is_plan,
    #     RS_docs_barcodes.approved
    #     FROM RS_docs_barcodes
    #         LEFT JOIN RS_barcodes
    #         ON RS_barcodes.barcode = RS_docs_barcodes.barcode
    #         LEFT JOIN (Select RS_barcodes.barcode as GTIN,
    #         RS_barcodes.id_good,
    #         RS_barcodes.id_property,
    #         RS_barcodes.id_series,
    #         RS_barcodes.id_unit FROM RS_barcodes
    #         WHERE RS_barcodes.barcode Like '%'+:gtin + '%' LIMIT 1) AS RS_barcodes_inaccurate
    #         ON TRUE
    #         LEFT JOIN RS_barcodes as FullBarcode
    #         ON FullBarcode.barcode = RS_docs_barcodes.barcode
    #
    #     WHERE id_doc = :id_doc  and RS_docs_barcodes.barcode = :set_barcode)
    #
    # ORDER  BY TypeOfUnion
    # '''
    return query


def get_barcode_card():
    ls = {"customcards": {
        "options": {
            "search_enabled": False,
            "save_position": True
        },
        "layout": {
            "type": "LinearLayout",
            "orientation": "vertical",
            "height": "match_parent",
            "width": "match_parent",
            "weight": "0",
            "Elements": [
                {
                    "type": "LinearLayout",
                    "orientation": "horizontal",
                    "height": "match_parent",
                    "width": "match_parent",
                    "weight": "0",
                    "Elements": [
                        {"type": "TextView",
                         "height": "wrap_content",
                         "width": "match_parent",
                         "weight": "1",
                         "Value": "@barcode",
                         "Variable": ""
                         },
                        {
                            "type": "Button",
                            "show_by_condition": "",
                            "Value": "@picture",
                            "TextColor": "#DB7093",
                            "BackgroundColor": "#FFFFFF",
                            "Variable": "btn_tst1",
                            "NoRefresh": False,
                            "document_type": "",
                            "cardCornerRadius": "15dp",
                            "weight": "1",
                            "mask": ""
                        }]}


            ]
        }}
    }
    return ls

def get_doc_barcode_query():
    ls = '''
    SELECT 
    id_barcode,
    RS_marking_codes.mark_code as mark_code,
    approved
    FROM RS_docs_barcodes

    JOIN RS_marking_codes 
    ON RS_marking_codes.id = RS_docs_barcodes.id_barcode AND
    RS_marking_codes.id_good = :id_good AND
    RS_marking_codes.id_property = :id_property AND
    RS_marking_codes.id_series = :id_series AND
    RS_marking_codes.id_unit = :id_unit 
    
     WHERE RS_docs_barcodes.id_doc = :id_doc '''
    return ls

def get_markcode_query():
    return '''
    SELECT 
    Temp_query.CurStr as CurStr,
    Temp_query.id_barcode,
    Temp_query.mark_code,
    Temp_query.approved,
    Temp_query.id_good,
    Temp_query.id_properties as id_property,
    Temp_query.id_series,
    Temp_query.id_unit,
    RS_goods.name as good_name,
    RS_properties.name as properties,
    RS_series.name as series,
    RS_units.name as unit,
    RS_goods.code AS good_code,
    Temp_query.is_plan
    
    
 FROM (
SELECT 
    RS_docs_barcodes.id as CurStr,
    id_barcode,
    RS_marking_codes.mark_code,
    approved,
    RS_marking_codes.id_good,
    RS_marking_codes.id_property as id_properties,
    RS_marking_codes.id_series,
    RS_marking_codes.id_unit,
    RS_docs_barcodes.is_plan
    
    FROM RS_docs_barcodes

    JOIN RS_marking_codes 
    ON RS_marking_codes.id = RS_docs_barcodes.id_barcode 
    
     WHERE RS_docs_barcodes.id_doc = :id_doc AND id_barcode = :id_barcode) AS Temp_query
     
 LEFT JOIN RS_goods 
    ON RS_goods.id_elem=Temp_query.id_good
    LEFT JOIN RS_properties
    ON RS_properties.id_elem = Temp_query.id_properties
    LEFT JOIN RS_series
    ON RS_series.id_elem = Temp_query.id_series
    LEFT JOIN RS_units
    ON RS_units.id_elem=Temp_query.id_unit
    '''

def get_mark_qtty_conformity():
    return '''
    SELECT ifnull(doc_table.qtty_plan,0) - ifnull(tmp.qtty_of_mark,0)  FROM 
    
    (SELECT qtty_plan
    FROM RS_docs_table
    WHERE 
    id_doc = :idDoc 
    AND id_good = :id_good
    AND id_properties = :id_properties
    AND id_series = :id_series
    AND id_unit = :id_unit) As doc_table
       LEFT JOIN (SELECT Count(id_barcode) As qtty_of_mark
        FROM RS_docs_barcodes 
        WHERE id_doc=:idDoc 
        AND id_barcode LIke :barcode AND approved = :approved) As tmp
        ON TRUE
    '''