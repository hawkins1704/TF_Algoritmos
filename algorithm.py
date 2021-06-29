import json
import pandas as pd

url = "../data/poblaciones.csv"

def algorithm1(departamento):
    data = pd.read_csv(url)
    data2 = data[data["DEPARTAMENTO"] == departamento]
    responsePath = []
    for i, row in data2.iterrows():
        responsePath.append({"idx": i,
                             "lat": float(row["LATITUD"]),
                             "lon": float(row["LONGITUD"])})

    return json.dumps(responsePath)

def algorithm():
    data = pd.read_csv(url)
    responsePath = []
    for i, row in data.iterrows():
        responsePath.append({"idx": i,
                             "lat": float(row["LATITUD"]),
                             "lon": float(row["LONGITUD"])})

    return json.dumps(responsePath)

def estandar():
    data = pd.read_csv(url)
    responsePath = []
    for i, row in data.iterrows():
        responsePath.append({"cp": row["CENTRO POBLADO"],
                             "lat": float(row["LATITUD"]),
                             "lon": float(row["LONGITUD"])})

    return json.dumps(responsePath)

def peru1():
    data = pd.read_csv(url)
    responsePath = []


    #Almacenando departamentos
    nomDepartamentos = data['DEPARTAMENTO'].unique()
    departamentos = dict()
    for nom in nomDepartamentos:
        departamentos[nom] = data[data['DEPARTAMENTO'] == nom]
        #print(nom, len(provincias[nom]))
    #print(departamentos)

    #Definiendo matriz de calculo 

    def matrizCalculo(distrito):
        Matriz=[[] for _ in range(len(distrito))]
        cont1=0
        cont2=0
        col = 'CENTRO POBLADO'
        for i, cp1 in distrito.iterrows():
            for j, cp2 in distrito.iterrows():
                if cp1[col] == cp2[col]:
                    Matriz[cont1].append((0,cp2[col]))
                elif cp1[col] != cp2[col]:
                    Matriz[cont1].append((distancia(cp1, cp2),cp2[col]))

            cont1+=1
        #for fil in Matriz:
            #print(fil)

        return Matriz


        #Generando matriz y ejecutando algoritmo

    def Nexo(distrito):
        #print(f"Recibi el distrito: {distrito}")
        matrizGenerada=matrizCalculo(distrito)
        recorridoFinal=tsp(matrizGenerada, distrito)
        return recorridoFinal

    #Almacenando los distritos de X provincia
    def recorridoDistrito(provincia,provincias):
        nomDistritos = provincias[provincia]['DISTRITO'].unique()
        #print(f'Nombre de distritos de la provincia {provincia}: {nomDistritos}')
        distritos = dict()
        resultadosRecorridos=[]
        for nom in nomDistritos:
            distritos[nom] = provincias[provincia][provincias[provincia]['DISTRITO'] == nom]
            
        for distrito in distritos:
            print(Nexo(distritos[distrito]))


    def obtencionLatLong(recorrido,departamentos):
        nomCP = departamentos['LIMA']['CENTRO POBLADO'].unique()
        recorridoOficial=[]
        for cp in recorrido:
            recorridoOficial.append({
                "cp":cp[1],
                "lat":departamentos['LIMA'][departamentos['LIMA']['CENTRO POBLADO']==cp[1]]['LATITUD'].values[0],
                "lon":departamentos['LIMA'][departamentos['LIMA']['CENTRO POBLADO']==cp[1]]['LONGITUD'].values[0]
            })

        return recorridoOficial


    #prueba-----------------------
    recorrido=[(0, 'ILLAPASCA'), (0.0176, 'LANCA'), (0.0156, 'TULLPAYOC'), (0.0564, 'TISCOCOCHA'), (0.0151, 'PARIONA'), (0.0107, 'PUCACHUCLLA'), (0.0329, 'MISME'), (0.0078, 'ILLAPASCA')]
    responsePath=obtencionLatLong(recorrido,departamentos)
    print(f"Response path: {responsePath}   ")
    #-----------------------------


    #Almacenando las provincias de X departamento
    def recorridoProvincia(departamento,departamentos):
        nomProvincias = departamentos[departamento]['PROVINCIA'].unique()
        provincias = dict()
        for nom in nomProvincias:
            provincias[nom] = departamentos[departamento][departamentos[departamento]['PROVINCIA'] == nom]
        for provincia in provincias:
            recorridoDistrito(provincia,provincias)


    def recorridoMaestro():
        for departamento in departamentos:
            recorridoProvincia(departamento, departamentos)


    return json.dumps(responsePath)

