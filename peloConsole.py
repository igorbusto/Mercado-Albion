import requests
from tkinter import *
import tkinter as tk
from tkinter import simpledialog
from datainfo import (
    city_list, file_list, client_title, quality_list, tier_list,
    category_list, enchant_list
)
import json


tax = 0.07

def scroll(event):
    canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

def human_readable_value(value):
    if 1e3 <= value < 1e6:
        return str(round(value/1e3)) + ' k'
    elif 1e6 <= value:
        return str(round(value/1e6, 1)) + ' m'
    else:
        return str(value)

def buscar():
    
    base_url = "https://west.albion-online-data.com/api/v2/stats/prices/"
    #codigoNome = "https://gameinfo.albiononline.com/api/gameinfo/items/"

    #       Base
    #   nome do item = T2_2H_BOW 
    #   encatamento se tiver = @2
    #   cidade = ?locations=martlock
    #   qualidade = &qualities=2

    buscaNome = str(search_entry.get())
    cityCompra = var_cityCompra.get() 
    cityVenda = var_cityVenda.get()
    category = var_category.get()
    quality = var_quality.get()
    tier = var_tier.get()
    enchant = var_enchant.get()

    listaPrint = []

    categorias = {
        'bolsa': "bags",
        'capa': "capes",
        'arcano': "arcane",
        'espada': "sword",
        'machado': "axe",
        'arco': "bow",
        'crossbow': "crossbow",
        'amaldiçoado': "cursed",
        'adaga': "dagger",
        'fogo': "fire",
        'gelo': "frost",
        'martelo': "hammer",
        'sagrado': "holy",
        'hunter': "hunter",
        'maça': "mace",
        'mago': "mage",
        'natureza': "nature",
        'mão secundaria': "offhands",
        'lança': "spear",
        'tank': "tank",
    }

    qualidades={
        '1':'normal',
        '2':'bom',
        '3':'excepcional',
        '4':'excelente',
        '5':'obra-prima',
    }

    qualidadeStringNum={
        'normal':'1',
        'bom':'2',
        'excepcional':'3',
        'excelente':'4',
        'obra-prima':'5',
    }

    # Filtra categoria
    if(category != 'todos'):
        if category in categorias:
            arquivo = categorias[category]+'.json'
            with open('itens/Categoria/'+str(arquivo), encoding='utf-8') as meu_json:
                listaCategoria = json.load(meu_json)

            lista = ''
            for entry in listaCategoria:
                if(buscaNome != ''):
                    localized_names = entry
                   
                    for localized in localized_names['LocalizedNames']:
                        if(str(localized['Key'])=='PT-BR') and buscaNome.lower() in str(localized['Value']).lower():
                            listaPrint.append(entry['UniqueName'])
                else:
                    listaPrint.append(entry['UniqueName'])
        
    
    # Filtra pelo nome
    elif buscaNome != '':
        with open("nomesTraduzidos.json", encoding='utf-8') as meu_jsonTodos:
           listaTodosItens = json.load(meu_jsonTodos)
        for todos in listaTodosItens['itens']:   # Nome PT-BR em idItem
            if buscaNome.lower() in str(todos['nome']).lower():
                #print(todos['idItem'])
                listaPrint.append(todos['idItem'])   

    # Filtra por Tier
    if tier != 'todos':
        new_list = [tiers for tiers in listaPrint if tiers[1] == tier]
        listaPrint = new_list
        #print('tier ' ,listaPrint)
    
    # Filtra por Encantamento
    if enchant != 'todos':
        new_list = []
        for item in listaPrint:
            parts = str(item).split('@')
            if len(parts) == 2 and parts[1] == enchant:
                new_list.append(item)
            elif len(parts) == 1 and enchant == '0':
                #print('encatamento ', enchant)
                new_list.append(item)
        listaPrint = new_list
        #print('encatamento ' , listaPrint)

    qualidadeBusca = ''
    if quality != 'todos':
        if quality in qualidadeStringNum:
            qualidadeBusca = '&qualities='+qualidadeStringNum[quality]
            #print(qualidadeBusca)
            #arquivo = categorias[category]+'.json'


    fazBusca = ','.join(listaPrint)

    print(base_url + fazBusca + '?locations=' + cityCompra + qualidadeBusca)
    #exit()
    respostaCityCompra = requests.get(base_url + fazBusca + '?locations=' + cityCompra + qualidadeBusca).json()
    respostaCityVenda = requests.get(base_url + fazBusca + '?locations=' + cityVenda + qualidadeBusca).json()
    #print(base_url + listaDoJson + '?locations=' + city)
    #print(listaDoJson)



    
    offer_dict = {}
    tierEncQuali = ''
    listaParaExibir = [] # idItem | valorCompra | valorVenda | qualiadde | lucro

    # insere idItem, valor de venda e qualidade
    for entry in respostaCityCompra:
        item = entry['item_id']
        value = entry['sell_price_min']
        qualidade = entry['quality']
        listaParaExibir.append([item,value,0,qualidade,0,0])

    # insere o valor de venda
    for i, entry in enumerate(respostaCityVenda):
        value = entry['sell_price_min']
        listaParaExibir[i][2] = value

    # insere apenas o lucro de cada item
    for i in range(len(listaParaExibir)):
        try:
            idItem = listaParaExibir[i][0]
            valorCompra = listaParaExibir[i][1]
            valorVenda = listaParaExibir[i][2]

            historico_url = 'https://west.albion-online-data.com/api/v2/stats/history/'
            historicoVenda = requests.get(historico_url + idItem + '?locations=' + cityCompra + '&time-scale=24'+ qualidadeBusca).json()
            #print(historico_url + idItem + '?locations=' + cityCompra + '&time-scale=24'+ qualidadeBusca)


            for entry in historicoVenda:
                diaria = entry['data']
                if diaria:  # Verificar se a lista não está vazia
                    quantidadeDiaria = diaria[-2]['item_count']
                else:
                    quantidadeDiaria = 0


            if valorCompra != 0 and valorVenda != 0:
                #lucro = ((valorVenda - valorCompra) * quantidadeDiaria) 
                #lucro = (lucro / valorVenda) * 100
                lucro = ((valorVenda - valorCompra)/ valorCompra)  # Porcentagem
            else:
                lucro = 0
            listaParaExibir[i][4] = lucro
            listaParaExibir[i][5] = quantidadeDiaria
        except:
            pass
        


    



    # Ordena do menor para o maior com base no lucro para listar os que dao o maior lucro
    listaParaExibir = sorted(listaParaExibir, key=lambda x: x[-1], reverse=True)    
    i=0
    for entry in listaParaExibir:
        idDoItem = entry[0]
        valorCompra = entry[1]
        valorVenda = entry[2]
        qualidade = str(entry[3])
        lucro = entry[4]
        quantidadePorDia = entry[5]

        encantamento = idDoItem[-1] if "@" in idDoItem else '0'
        tier = idDoItem[1]
        tierEncQuali = str(tier)+'.'+str(encantamento)

        if qualidade in qualidades:
            qualidade = qualidades[qualidade]
            tierEncQuali = tierEncQuali + ' ('+qualidade+')'

        nomeTraduzido = ''
        with open("nomesTraduzidos.json", encoding='utf-8') as meu_jsonTodos:
           listaTodosItens = json.load(meu_jsonTodos)
        for todos in listaTodosItens['itens']:
            if idDoItem == todos['idItem']:
                nomeTraduzido = todos['nome']+' '+ tierEncQuali
                
                #lucro = valorVenda-valorCompra
                #precoCompra = human_readable_value(valorCompra)
                #precoVenda = human_readable_value(valorVenda)
                #lucro = human_readable_value(lucro)

                img = PhotoImage('img/T1_MAIN_SWORD.png')
                try:
                    img = PhotoImage(file='img/'+idDoItem+'.png')
                except:
                    pass
                label = Label(frame, image=img)
                label.image = img
                label.grid(row=4+i, column=0, sticky=W)
                print(entry)
                Label(frame, text=nomeTraduzido).grid(row=4+i, column=1, columnspan=3,sticky=W)
                Label(frame, text=valorCompra, padx=15).grid(row=4+i, column=3, sticky=W)
                Label(frame, text=valorVenda, padx=15).grid(row=4+i, column=5, sticky=W)
                Label(frame, text="{:.0%}".format(lucro), padx=15).grid(row=4+i, column=6, sticky=W)
                Label(frame, text=quantidadePorDia, padx=15).grid(row=4+i, column=7, sticky=W)
                i += 1
    gui.update()
    canvas.config(scrollregion=canvas.bbox('all'))
    



gui = Tk()
gui.title(client_title)
gui.geometry('1050x900')

scrollbar = Scrollbar(gui)
canvas = Canvas(gui, bg='white', yscrollcommand=scrollbar.set)
scrollbar.config(command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
frame = Frame(canvas)
canvas.pack(side=LEFT, fill=BOTH, expand=True)
canvas.create_window(0, 0, window=frame, anchor=NW)


var_cityCompra = StringVar(frame)
var_cityVenda = StringVar(frame)
var_quality = StringVar(frame)
var_tier = StringVar(frame)
var_category = StringVar(frame)
var_enchant = StringVar(frame)

var_cityCompra.set(city_list[0])
var_cityVenda.set(city_list[0])
var_quality.set(quality_list[0])
var_tier.set(tier_list[0])
var_category.set(category_list[0])
var_enchant.set(enchant_list[0])

Label(frame, text='Procurar:').grid(row=1, column=0, sticky=E)
search_entry = Entry(frame, width=50)
search_entry.grid(row=1, column=1, sticky=W)
Label(frame, text='Compra:').grid(row=1, column=2, sticky=E)
OptionMenu(frame, var_cityCompra, *city_list).grid(row=1, column=3, sticky=W)
Label(frame, text='Venda:').grid(row=2, column=2, sticky=E)
OptionMenu(frame, var_cityVenda, *city_list).grid(row=2, column=3, sticky=W)

Label(frame, text='Categoria:').grid(row=1, column=4, sticky=E)
OptionMenu(frame, var_category, *category_list).grid(row=1, column=5, sticky=W)
Label(frame, text='Tier:').grid(row=2, column=4, sticky=E)
OptionMenu(frame, var_tier, *tier_list).grid(row=2, column=5, sticky=W)
Label(frame, text='Encantamento:').grid(row=1, column=6, sticky=E)
OptionMenu(frame, var_enchant, *enchant_list).grid(row=1, column=7, sticky=W)
Label(frame, text='Qualidade:').grid(row=2, column=6, sticky=E)
OptionMenu(frame, var_quality, *quality_list).grid(row=2, column=7, sticky=W)

#Label(frame, text='Items', padx=15).grid(row=1, column=8, sticky=E)
#OptionMenu(frame, var_file, *file_list).grid(row=1, column=9, sticky=W)
Button(frame, text='Buscar', command=buscar).grid(row=1, column=8, sticky=W)

Label(frame, text='Item').grid(row=3, column=0, columnspan=3, sticky=W)
Label(frame, text='Preço Compra', padx=15).grid(row=3, column=3, sticky=W)
Label(frame, text='Preço Venda', padx=15).grid(row=3, column=5, sticky=W)
Label(frame, text='Lucro', padx=15).grid(row=3, column=6, sticky=W)
Label(frame, text='Quantidade Vendida p/ dia', padx=15).grid(row=3, column=7, sticky=W)

gui.update()
canvas.config(scrollregion=canvas.bbox('all'))
canvas.bind_all("<MouseWheel>", scroll)
gui.mainloop()
