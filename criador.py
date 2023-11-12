import json



itens = {'itens': []}    
idItem = ''
nome = ''
with open("itens/items.json", encoding='utf-8') as meu_jsonTodos:
    listaTodosItens = json.load(meu_jsonTodos)
for todos in listaTodosItens:
    try:
        idItem = todos['UniqueName']
        nome = todos['LocalizedNames']['PT-BR']
        print(idItem + " " + nome)
        itens['itens'].append(
            {
                'idItem': idItem,
                'nome': nome
            }
        )
    except:
        pass
with open("nomesTraduzidos.json", "w") as arquivo:     
    json.dump(itens, arquivo, indent=4)



