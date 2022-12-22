import zmq
import string
import random

context = zmq.Context()
clientes=context.socket(zmq.REP)
clientes.bind('tcp://*:5550')
listaArchivoNombres=[]
generadorLink=[] #almacena los link

length_of_string = 8


while True:
    bandL=False
    data,nombre,opcion,nombreArchivo,nombreUsua,nombreAsig=clientes.recv_multipart()
    print(opcion)
    clientes.send_json("ok")
    
    if int(opcion.decode("utf-8"))==1:
        bd={'nombreArchivo':nombreArchivo.decode("utf-8"),'nombreUsua':nombreUsua.decode("utf-8"),'chubk':nombre.decode("utf-8"),'nombreAsig':nombreAsig.decode("utf-8")}
        listaArchivoNombres.append(bd)
        with open(nombre.decode("utf-8"), "wb") as f:
            f.write(data)
    

    if int(opcion.decode("utf-8"))==3:
        rds=clientes.recv_json()
        lN=[]
        print(listaArchivoNombres)
        print(nombre.decode("utf-8"))
        for x in listaArchivoNombres:
            

            print(nombre.decode("utf-8"))
            if x['nombreUsua']==nombreUsua.decode("utf-8"):
                lN.append(x['nombreAsig'])
            else:
                pass
        
        clientes.send_json(lN)



    if int(opcion.decode("utf-8"))==2:
        oka=clientes.recv_json()
        listaCuEnv=[]
        
        for xl in listaArchivoNombres:
            if xl['nombreUsua']==nombreUsua.decode("utf-8") and xl['nombreAsig']==nombreAsig.decode("utf-8"):
                bandL=True
                listaCuEnv.append(xl['chubk'])

        if bandL==True:

            clientes.send_json(listaCuEnv)
            print(listaCuEnv)
            recs=clientes.recv_json()
            for lisC in listaCuEnv:
                with open(lisC, "rb") as f:
                    contenidoArchivo=f.read()
                    clientes.send_multipart([contenidoArchivo,lisC.encode("utf-8")])
                    wok=clientes.recv_json()
            clientes.send_json("fin")
            vac=[]
            listaConChunk=vac
            
        else:
            clientes.send_json("error")

    if int(opcion.decode("utf-8"))==4:
        bandLs=False
        oka=clientes.recv_json()
        listaPart=[]
    
        for xl in listaArchivoNombres:
            if xl['nombreUsua']==nombreUsua.decode("utf-8") and xl['nombreAsig']==nombreAsig.decode("utf-8"):
                bandLs=True
                listaPart.append(xl['chubk'])
        if bandLs==True:
            token=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
            clientes.send_json(token)
            almacenas={'archivo':nombreAsig.decode("utf-8"),'link':token, 'todosCunk':listaPart}
            generadorLink.append(almacenas)
        else:
            clientes.send_json("error")
    


    if int(opcion.decode("utf-8"))==5:
        bandLsL=False
        listCR=[]
        soloChunk=[]
        oka=clientes.recv_json()
        for v in generadorLink:
            if v['link']==nombreAsig.decode("utf-8"):
                listCR=v
                soloChunk=v['todosCunk']
                bandLsL=True
        if bandLsL==True:
            clientes.send_json(listCR)
            print(listCR)
            recsl=clientes.recv_json()
            
            for lisCl in soloChunk:
                with open(lisCl, "rb") as f:
                    contenidoArchivo=f.read()
                    clientes.send_multipart([contenidoArchivo,lisCl.encode("utf-8")])
                    wokl=clientes.recv_json()
            clientes.send_json("fin")
            vacl=[]
            lisCl=vacl
        else:
            clientes.send_json("error")