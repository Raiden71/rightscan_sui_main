def goods_on_click(hashMap, _files=None, _data=None):

    if hashMap.get("listener") == "CardsClick":
        # Находим ID документа
        current_str = hashMap.get("selected_card_position")
        jlist = json.loads(hashMap.get("goods_cards"))
        current_good = jlist['customcards']['cardsdata'][int(current_str)]

        # id_doc = current_doc['key']
        hashMap.put('selected_good_id', current_good['key'])
        # hashMap.put('type_name', current_good['name'])
        # hashMap.put('code', current_good['code'])
        # hashMap.put('type_name', current_good['type_name'])
        #        hashMap.put('unit_name', current_good['unit_name'])

        hashMap.put('noRefresh', '')
        hashMap.put("ShowScreen", "Карточка товара")

        # hashMap.put('toast', current_good['key'])

    elif hashMap.get("listener") == 'ON_BACK_PRESSED':

        hashMap.put('FinishProcess', '')

    return hashMap