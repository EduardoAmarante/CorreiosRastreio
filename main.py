import requests
import json
from time import sleep
from threading import Thread, Lock

global config
config = {'url': 'https://api.telegram.org/bot','lock': Lock()}

def del_update(data):
    global config

    config['lock'].acquire()
    requests.post(config['url'] + 'getUpdates', {'offset': data['update_id'] + 1})
    config['lock'].release()

def send_message(data,msg):
    global config

    config['lock'].acquire()
    requests.post(config['url'] + 'sendMessage', {'chat_id': data['message']['chat']['id'], 'text': str(msg)})
    config['lock'].release()

while True:

    while True:
        try:
            x = json.loads(requests.get(config['url'] + 'getUpdates').text)
            break
        except Exception as e:
            x = {'result': []}
            if 'Failed to estabilish a new connection' in str(e):
                print('Failed to estabilish a new connection, retrying...')
                sleep(1)
            else:
                print('Erro desconhecido: ' + str(e))
    if len(x['result']) > 0:
        for data in x['result']:
            Thread(target=del_update, args=(data,)).start()

            print(json.dumps(data, indent=1))
            cod = data['message']['text']
            if cod == '/start':
                send_message(data,'Bem vindo ao bot de Rastreio! Envie o codigo do rastreio para o bot.')
            elif len(cod) == 13:
                cod = data['message']['text']
                
                url = "https://proxyapp.correios.com.br/v1/sro-rastro/"

                r = requests.get(url+cod).json()

                r = r['objetos']
                r = r[0]
                r = r['eventos']
                v = r[0]

                Thread(target=send_message, args=(data,"product description" + v['descricao'])).start()
            else:
                Thread(target=send_message, args=(data,'Código inválido, Por favor envie o código de rastreio novamente')).start()
        sleep(2)

#codigo = input("Digite o código do produto: ")
codigo = 'QI828905992BR'
url = "https://proxyapp.correios.com.br/v1/sro-rastro/"

r = requests.get(url+codigo).json()

r = r['objetos']
r = r[0]
r = r['eventos']
v = r[0]


# for i in range(len(r)):
#     local = r[i]['unidade']
#     print(local['endereco'],'\n')

