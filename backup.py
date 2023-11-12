    for entry in response_blackmarket:
        item = entry['item_id']
        value = entry['buy_price_max']
        qualities = [x for x in range(entry['quality'], 6)]
        items_to_purchase = [item+"#"+str(x) for x in qualities]
        city_values = []
    
        for item_key in items_to_purchase:
            if item_key in offer_dict.keys():
                item_city_value = offer_dict[item_key][0]
                city_values.append(item_city_value)
    
        if len(city_values) > 0:
            offer_dict[items_to_purchase[0]] = [min(city_values), value]
        
    full_list = sorted(offer_dict.items(), key=lambda x:(x[0], -x[1][1]+x[1][0]))
    profit_list = []

    for item in full_list:
        name = item[0]
        values_pair = item[1]
        profit = round(values_pair[1]*(1-tax) - values_pair[0])
    
        if profit > 0:
            profit_list.append([name, values_pair, profit])


    for widget in frame.winfo_children()[10:]:
        widget.destroy()
    frame.pack_forget()

    i = 0
    for item in profit_list[::-1]:
        _id, _quality = item[0].split('#')

        enchant = item[0][-1] if "@" in item[0] else '0'
        tier = _id[1]
        quality = quality_list[int(_quality) -1]
        if _id in listaItens['UniqueName']:
            #translated_name = id_to_name[_id]
            translated_name = listaItens[_id]
            print(translated_name)
        else:
            tier = ''
            enchant = ''
            translated_name = _id
            

        name = f'{tier}.{enchant} {translated_name}, {quality}'

        item_id = item[0].split('#')[0]
        price = human_readable_value(item[1][0])
        blackmarket = human_readable_value(item[1][1])
        profit = human_readable_value(item[2])

        img = PhotoImage(file='img/'+item_id+'.png')
        label = Label(frame, image=img)
        label.image = img
        label.grid(row=3+i, column=0, sticky=W)
        Label(frame, text=name).grid(row=3+i, column=1, sticky=W)
        Label(frame, text=price, padx=15).grid(row=3+i, column=2, sticky=W)
        Label(frame, text=blackmarket, padx=15).grid(row=3+i, column=3, sticky=W)
        Label(frame, text=profit, padx=15).grid(row=3+i, column=4, sticky=W)
        i += 1