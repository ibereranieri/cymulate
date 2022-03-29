import requests
import json
from datetime import datetime
from termcolor import colored

#Exemplos para teste
#md5:ae17ce1eb59dd82f38efb9666f279044
#sha1:3b3acb4a55ba8e2da36223ae59ed420f856b0aaf
#sha256:a4fb20b15efd72f983f0fb3325c0352d8a266a69bb5f6ca2eba0556c3e00bd15
#dominio:http://transferwiser.io

data_inicial=None
data_final=None
link=None

#insira o token aqui
api=''

def main():
    opcao=0
    while opcao !=5:
        print('=-='*10)
        print('''
        [1] SHA256
        [2] MD5
        [3] SHA1
        [4] URL
        [5] sair do programa''')
        opcao = int(input('>>>> Escolha o tipo da busca? '))
        if opcao==1 or opcao==2 or opcao==3:
            link='https://api.app.cymulate.com/v1/immediate-threats/ioc/?'
            tipo=input('Pesquisar em toda a base? [s/n]: ')
            if tipo=='n' or tipo=='N':
                data_inicial=input('Data Inicial no formato AAAAMMDD:')
                data_final=input('Data final no formato AAAAMMDD: ') 
            else:
                print('A busca será feito por todos os IOCs disponiveis no Cymulate')
                data_inicial='20000101'
                data_final=datetime.today().strftime('%Y%m%d')

            link=f'{link}fromDate={data_inicial}&toDate={data_final}' 

            requisicao=requests.get(link,headers={'Accept':'*/*','x-token':api})
            busca_ioc=requisicao.json()
            busca_ioc2=busca_ioc['data']
        if opcao==1:
            xSHA256=input('Entre com o SHA256 ==> ')
            encontrado=0
            for busca_data in busca_ioc2:
                for ioc in busca_data['iocs']:
                    if xSHA256==ioc['sha256']:
                        dados_ioc(1,ioc['status'],ioc['timestamp'])
                        encontrado=1
                        break
            if encontrado==0:
                dados_ioc(0)   
        elif opcao==2:
            xMD5=input('Entre com o MD5 ==> ')
            encontrado=0
            for busca_data in busca_ioc2:
                for ioc in busca_data['iocs']:
                    if xMD5==ioc['md5']:
                        dados_ioc(1,ioc['status'],ioc['timestamp'])
                        encontrado=1
                        break
            if encontrado==0:
                dados_ioc(0) 
        elif opcao==3:
                xSHA1=input('Entre com o SHA1 ==> ')
                encontrado=0
                for busca_data in busca_ioc2:
                    for ioc in busca_data['iocs']:
                        if xSHA1==ioc['sha1']:
                            dados_ioc(1,ioc['status'],ioc['timestamp'])
                            encontrado=1
                            break
                if encontrado==0:
                    dados_ioc(0) 
        elif opcao==4:
            link='https://api.app.cymulate.com/v1/browsing/feed/url?type=json'
            requisicao=requests.get(link,headers={'Accept':'*/*','x-token':api})
            busca_ioc=requisicao.json()
            busca_ioc2=busca_ioc['data']
            xDominio=input('Entre com o dominio (http:// ou https://) ==> ')
            encontrado=0
            for busca_data in busca_ioc2:
                if xDominio==busca_data:
                    dados_ioc(1,ioc['status'],ioc['timestamp'])
                    encontrado=1
                    break
            if encontrado==0:
                dados_ioc(0) 
        elif opcao==5:
            print('Finalizado...')           
        else:
            print('Opcao invalida')
        print('=-='*10)
    print('Fim do programa')


def dados_ioc(encontrado,provado='',data=''):
    if encontrado==1:
        print(colored("IOC encontrado",'green'))
        print(provado)
        print(data)
    else:
       print(colored('Registro não encontrado','red')) 

if __name__=='__main__':
    main()
