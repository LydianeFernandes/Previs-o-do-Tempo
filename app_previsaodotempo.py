import requests

IP_API_URL = 'http://ip-api.com/json/?fields=regionName,lat,lon'
ESTACAO_API_URL = "https://api.ipma.pt/open-data/distrits-islands.json"
HOJE_IPMA_API_URL = "https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/hp-daily-forecast-day0.json"
AMANHA_IPMA_API_URL = "https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/hp-daily-forecast-day1.json"
DEPOIS_IPMA_API_URL = "https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/hp-daily-forecast-day2.json"

def minha_localizacao():
    resposta = requests.get(IP_API_URL)
    dados = resposta.json()
    regiao = dados["regionName"]
    minha_latitude = dados["lat"]
    minha_longitude = dados["lon"]
    print(f"Você está na região: {regiao}, Latitude: {minha_latitude}, Longitude: {minha_longitude}")
    return(minha_latitude, minha_longitude)

def id_estacao(minha_latitude, minha_longitude):
    resposta2 = requests.get(ESTACAO_API_URL)
    data = resposta2.json()["data"]
    
    globalId = []
    estacao_latitude = []
    estacao_longitude = []
    distancia = []

    for i in data:
        globalId.append(i["globalIdLocal"])
        estacao_latitude.append(i["latitude"])
        estacao_longitude.append(i["longitude"])

    rows = len(estacao_latitude)
    for i in range(rows):
        distancia.append(((float(estacao_latitude[i]) - minha_latitude)**2+(float(estacao_longitude[i]) - minha_longitude)**2)**0.5)  #fórmula euclidiana
        menor_distancia = min(distancia)

    ind_menordistancia = distancia.index(menor_distancia)
    id_estacao_mais_prox = globalId[ind_menordistancia]
    return(id_estacao_mais_prox)

def temperatura(escolha, id_estacao_mais_prox):
    if escolha == 1:
        resposta3 = requests.get(HOJE_IPMA_API_URL)
        dados1 = resposta3.json()["data"]
        for item in dados1:
            if item["globalIdLocal"]==id_estacao_mais_prox:
                print(f"Data: {resposta3.json()["forecastDate"]}, Id da Estação: {item["globalIdLocal"]}, Temperatura mínima: {item["tMin"]}, Temperatura máxima: {item["tMax"]}")
    elif escolha == 2:
        resposta4 = requests.get(AMANHA_IPMA_API_URL)
        dados2 = resposta4.json()["data"]
        for item in dados2:
            if item["globalIdLocal"]==id_estacao_mais_prox:
                print(f"Data: {resposta4.json()["forecastDate"]}, Id da Estação: {item["globalIdLocal"]}, Temperatura mínima: {item["tMin"]}, Temperatura máxima: {item["tMax"]}")
    elif escolha == 3:
        resposta5 = requests.get(DEPOIS_IPMA_API_URL)
        dados3 = resposta5.json()["data"]
        for item in dados3:
            if item["globalIdLocal"]==id_estacao_mais_prox:
                print(f"Data: {resposta5.json()["forecastDate"]}, Id da Estação: {item["globalIdLocal"]}, Temperatura mínima: {item["tMin"]}, Temperatura máxima: {item["tMax"]}")

def main():

    print("\nEscolha uma opção para o dia que pretende saber a previsão:")
    print("1 - Hoje")
    print("2 - Amanhã")
    print("3 - Depois de amanhã")

    escolha = int(input("Digite o número da sua escolha: "))

    while escolha <= 0 or escolha >3:
        print("Ops! Esse não é um número válido. Tente novamente...")
        break
    
    minha_latitude, minha_longitude = minha_localizacao()
    id_estacao_mais_prox = id_estacao(minha_latitude,minha_longitude)
    temperatura(escolha, id_estacao_mais_prox)

if __name__ == "__main__":
    main()