import json
import pandas as pd
import math

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



    def distancia(cp1,cp2):
        x1, y1 = float(cp1['LATITUD']), float(cp1['LONGITUD'])
        x2, y2 = float(cp2['LATITUD']), float(cp2['LONGITUD'])
        return round(math.sqrt((x1 - x2)**2 + (y1 - y2)**2),4)

    #ALGORITMO TSP

    #Calculando ruta menor mediante Backtracking

    def tsp(graph,distrito):
        costos = []
        recorridos=[]
        n = len(distrito)
        recorrido=[]
        visited = [False for i in range(n)]
        visited[0] = True
        recorrido.append(graph[0][0])
        HamCycle(graph,visited,0,n,1,0,recorrido,costos,recorridos)
        if (len(costos)!=0):
            minimo=min(costos)
            #print(f"minimo: {minimo}")
            ind=costos.index(minimo)
            for i,recorrido in enumerate(recorridos):
                if i==ind:
                    #print(f"recorrido: {recorrido}")
                    return recorrido
        else:
            return recorrido


    def HamCycle(graph, visited, currPos, n, count, cost,recorrido,costos,recorridos):
            if (count == n and graph[currPos][0][0]):
                costos.append(cost + graph[currPos][0][0])
                #se crea una copia porque la lista "recorrido" constantemente
                    #está agregando y quitando valores
                prueba=recorrido.copy()
                #prueba.append(graph[currPos][0])
                recorridos.append(prueba)
                return


            for i in range(n):
                if (visited[i] == False and graph[currPos][i][0]):
                    visited[i] = True
                    recorrido.append(graph[currPos][i])
                    HamCycle(graph, visited, i, n, count + 1,
                                cost + graph[currPos][i][0],recorrido,costos,recorridos)
                    recorrido.pop()
                    visited[i] = False



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

        recorridoTotal=[]
        nomDistritos = provincias[provincia]['DISTRITO'].unique()
        #print(f'Nombre de distritos de la provincia {provincia}: {nomDistritos}')
        distritos = dict()
        resultadosRecorridos=[]
        for nom in nomDistritos:
            distritos[nom] = provincias[provincia][provincias[provincia]['DISTRITO'] == nom]

        for distrito in distritos:
            #print(f"Nexo: {Nexo(distritos[distrito])}")
            recorridoTotal.extend(Nexo(distritos[distrito]))

        return recorridoTotal


    #Almacenando las provincias de X departamento 
    def recorridoProvincia(departamento,departamentos):

        recorridoTotal=[]


        nomProvincias = departamentos[departamento]['PROVINCIA'].unique()


        provincias = dict()
        for nom in nomProvincias:
            provincias[nom] = departamentos[departamento][departamentos[departamento]['PROVINCIA'] == nom]
        for provincia in provincias:
            recorridoTotal.extend(recorridoDistrito(provincia,provincias))

        return recorridoTotal

    def pruebaDepa(departamento,departamentos):

        recorridoTotal=[]
        nomProvincias = departamentos[departamento]['PROVINCIA'].unique()

        provincias = dict()
        for nom in nomProvincias:
            provincias[nom] = departamentos[departamento][departamentos[departamento]['PROVINCIA'] == nom]
        for provincia in provincias:
            recorridoTotal.extend(recorridoDistrito(provincia,provincias))

        return recorridoTotal

    def recorridoMaestro():

        recorridoTotal=[]

        for departamento in departamentos:
           recorridoTotal.extend(recorridoProvincia(departamento, departamentos))
        return recorridoTotal


    def obtencionLatLong(recorrido,departamentos,depa):
        nomCP = departamentos[depa]['CENTRO POBLADO'].unique()
        recorridoOficial=[]
        for cp in recorrido:
            recorridoOficial.append({
                "cp":cp[1],
                "lat":departamentos[depa][departamentos[depa]['CENTRO POBLADO']==cp[1]]['LATITUD'].values[0],
                "lon":departamentos[depa][departamentos[depa]['CENTRO POBLADO']==cp[1]]['LONGITUD'].values[0]
            })

        return recorridoOficial

    #prueba---------------------------------------------
    #nomProvincias = departamentos['LIMA']['PROVINCIA'].unique()
    #provincias = dict()
    #for nom in nomProvincias:
    #    provincias[nom] = departamentos['LIMA'][departamentos['LIMA']['PROVINCIA'] == nom]
    #print(provincias)

    #---------------------------------------------------

    #recorrido2=recorridoDistrito('YAUYOS',provincias)
    #recorridoFinal=obtencionLatLong(recorrido2)
    recorridoTotal=pruebaDepa('PASCO',departamentos)
    #recorridoTotal=recorridoMaestro()
    responsePath=obtencionLatLong(recorridoTotal,departamentos,'PASCO')
    print(f"Response path: {responsePath}   ")

    #-----------------------------
    return json.dumps(responsePath)

