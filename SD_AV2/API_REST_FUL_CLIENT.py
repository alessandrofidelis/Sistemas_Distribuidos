import requests
import urllib.parse
import json


def pesquisa_pais(pais):
    
    id_cli = []
    max_cli = []
    
    url="http://127.0.0.1:8080/lista_clientes/"+str(pais)
    lista_clientes=requests.get(url).json()
    
    for cli in lista_clientes:
        url="http://127.0.0.1:8080/lista_pedidos/"+str(cli['CustomerId'])
        pedido=requests.get(url).json()
        
        for ped in pedido:
            url="http://127.0.0.1:8080/get_valor/"+str(ped['InvoiceId'])
            total_ped=requests.get(url).json()
            
            for total in total_ped:
                if int(cli['CustomerId']) in id_cli:
                    ind = id_cli.index(int(cli['CustomerId']))
                    max_cli[ind] += total['total']
                else:
                    id_cli.append(int(cli['CustomerId']))
                    max_cli.append(total['total'])
    maior = max(max_cli)
    ind = max_cli.index(maior)
    
    for cli in lista_clientes:
        if cli['CustomerId'] == id_cli[ind]:
            nome_cli = cli['FirstName']+' '+cli['LastName']
            
            if cli['State']:
                 destino = cli['Address']+', '+cli['City']+', '+cli['State']+', '+cli['Country']
            else:
                destino = cli['Address']+', '+cli['City']+', '+cli['Country']




    api="https://geocoder.ls.hereapi.com/search/6.2/geocode.json?"
    api_key="FAW4UmM093w73v0vfDZsClzE_1cLVptxcXJa0jh2X6g"
    
    if pais == 'Brazil':
      origem = "Av. José de Souza Campos, 44, Campinas - SP"
    if pais == 'USA':
      origem = "213 Madison St, New York - NY"
    if pais == 'Canada':
      origem = "385 Ontario St, St. Catharines, ON"
    if pais == 'France':
      origem = "282 Avenue Daumesnil, Paris"
    
    url = api+urllib.parse.urlencode({"apiKey":api_key, "searchtext":origem})
    dados = requests.get(url).json()
    
    origem_lat = dados["Response"]["View"][0]["Result"][0]["Location"]["NavigationPosition"][0]["Latitude"]
    origem_long = dados["Response"]["View"][0]["Result"][0]["Location"]["NavigationPosition"][0]["Longitude"]
    
    url = api+urllib.parse.urlencode({"apiKey":api_key, "searchtext":destino})
    dados = requests.get(url).json()
    destino_lat = dados["Response"]["View"][0]["Result"][0]["Location"]["NavigationPosition"][0]["Latitude"]
    destino_long = dados["Response"]["View"][0]["Result"][0]["Location"]["NavigationPosition"][0]["Longitude"]
    
    
    route = "https://router.hereapi.com/v8/routes?"
    transportMode = "car"
    
    Origem = str(origem_lat) + "," + str(origem_long)
    Destino = str(destino_lat) + "," + str(destino_long)
    
    url = route+urllib.parse.urlencode({"transportMode":str(transportMode),"origin":str(Origem),"destination":str(Destino),"return":"summary","apiKey":str(api_key)})
    dados = requests.get(url).json()
    
    distancia = dados["routes"][0]["sections"][0]["summary"]["length"]/1000
    
    print('País: '+pais)
    print('Cliente que mais gastou na chinook, foi: '+nome_cli)
    print('Endereço do cliente: '+destino)
    custo = int(distancia)*0.01
    print("Custo do envio do brinde = US$ {:.2f} ".format(custo))
    print()
    

selecao_pais = ['Brazil', 'USA', 'Canada', 'France']
for pais_buscado in selecao_pais:
    pesquisa_pais(pais_buscado)
    
    