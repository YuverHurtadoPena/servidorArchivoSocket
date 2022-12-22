import zmq
import hashlib
from os import remove
import uuid
import os
context = zmq.Context()
servidor=context.socket(zmq.REQ)
servidor.connect('tcp://localhost:5550')
bandera=True

def subirArchivo():
    extension=input('Ingresa la extension de tu archivo seguido de un punto-->')
    archivoNombre=input('Nombre del archivo a subir sin la extension-->')
    nombreUsusario=input('Ingresa tu nombre-->')
    archivo=archivoNombre+extension
    nombreAsig=str(uuid.uuid1())+extension
    with open(archivo, "rb") as f:
        contenidoArchivo=f.read(1024)
        while contenidoArchivo:
            sha1Hash = hashlib.sha1(contenidoArchivo)
            ha1Hashed = sha1Hash.hexdigest()+extension
            servidor.send_multipart([contenidoArchivo,ha1Hashed.encode("utf-8"),opcion.encode("utf-8"),archivo.encode("utf-8"),nombreUsusario.encode("utf-8"),nombreAsig.encode("utf-8")])
            x=servidor.recv()
            contenidoArchivo= f.read(1024)
        print("-----------------------")
        print("Tu archivo se envio")
        print("Este es el nombre asignado: ",nombreAsig)
        print("-----------------------")

def descargarArchivo():
    nombreAsig=input('Nombre del archivo a descargar con la extension-->')
    nombreUsusario=input('Ingresa tu usuario-->')
    archivo=""
    contenidoArchivo=""
    s=contenidoArchivo.encode("utf-8")
        
    ha1Hashed=""
    servidor.send_multipart([s,ha1Hashed.encode("utf-8"),opcion.encode("utf-8"),archivo.encode("utf-8"),nombreUsusario.encode("utf-8"),nombreAsig.encode("utf-8")])
    x=servidor.recv()
    servidor.send_json("ok")
    listaConChunk=servidor.recv_json()
    if listaConChunk!="error":
        open(nombreAsig, "wb")
            
        servidor.send_json("listo")
        for xss in listaConChunk:
            datos,nom=servidor.recv_multipart()
            servidor.send_json("ok")
            with open(nom.decode("utf-8"), "wb") as f:
                f.write(datos)


        rsa=servidor.recv_json()
        for dd in listaConChunk:
            with open(dd, "rb") as f:
                Ptrozos=f.read()
            with open(nombreAsig, "ab") as fi:
                fi.write(Ptrozos)
                remove(dd)

    else:
        print("algo anda mal, quizas no subiste el archivo o tu nombre esta mal escrito")
    

def listarArchivos():
    nameUser=input('Ingresa tu nombre-->')
    contenidoArchi=""
    contenidoArchivo=contenidoArchi.encode("utf-8")
    nombre=""
    archivo=""
    nombreAsig=""   
        
    servidor.send_multipart([contenidoArchivo,nombre.encode("utf-8"),opcion.encode("utf-8"),archivo.encode("utf-8"),nameUser.encode("utf-8"),nombreAsig.encode("utf-8")])
    x=servidor.recv()
    servidor.send_json("ok")
    ListaFile=servidor.recv_json()
    print("--------------------------")
    
    result=[]
    for x in ListaFile:
        if x not in result:
            result.append(x)
    print(result)
    print("--------------------------")

def generarLink():
    
    nombreAsig=input('Nombre del archivo -->')
    nombreUsusario=input('Ingresa tu usuario-->')
    archivo=""
    contenidoArchivo=""
    s=contenidoArchivo.encode("utf-8")
    ha1Hashed=""
    servidor.send_multipart([s,ha1Hashed.encode("utf-8"),opcion.encode("utf-8"),archivo.encode("utf-8"),nombreUsusario.encode("utf-8"),nombreAsig.encode("utf-8")])
    x=servidor.recv()
    servidor.send_json("ok")
    linkGenerado=servidor.recv_json()
    if linkGenerado!="error":
        print("----------------------------")
        print("El link es: ",linkGenerado)
        print("----------------------------")
    else:
        print("aldo anda mal, quizas tu no susbiste el archivo o tu nombre esta mal")


def descargarArchivoCompartido():
        link=""
        #extension=input('Ingresa la extension de tu archivo seguido de un punto-->')
        nombreAsig=input('Link-->')
        nombreUsusario=""
        archivo=""
        contenidoArchivo=""
        s=contenidoArchivo.encode("utf-8")
        
        ha1Hashed=""
        servidor.send_multipart([s,ha1Hashed.encode("utf-8"),opcion.encode("utf-8"),archivo.encode("utf-8"),nombreUsusario.encode("utf-8"),nombreAsig.encode("utf-8")])
        x=servidor.recv()
        servidor.send_json("ok")

        reChunk=servidor.recv_json()
        open(reChunk['archivo'], "wb")
        print(reChunk)
        servidor.send_json("ok")

        chunkListaLink=reChunk['todosCunk']
        for save in chunkListaLink:
            datas,nombredeC=servidor.recv_multipart()
            servidor.send_json("ok")
            with open(nombredeC.decode("utf-8"), "wb") as f:
                f.write(datas)
        rsa=servidor.recv_json()
        for dd in chunkListaLink:
                with open(dd, "rb") as f:
                    Ptrozoss=f.read()
                with open(reChunk['archivo'], "ab") as fil:
                    fil.write(Ptrozoss)
                    remove(dd)
while bandera!=False:

    print('1.SUBIR ARCHIVO')
    print('2.DESCARGAR DE MIS ARCHIVOS')
    print('3.LISTAR MIS ARCHIVOS')
    print('4.GENERAR LINK')
    print('5.DESCARGAR ARCHIVOS COMPORTIDOS')
    print('6.SALIR')
    opcion=input('-->')
    if int(opcion)==1:
        subirArchivo()
    if int(opcion)==2:
        descargarArchivo()
    if int(opcion)==3:
        listarArchivos()
    if int(opcion)==4:
        generarLink()
    if int(opcion)==5:
        descargarArchivoCompartido()
    if int(opcion)==6:
        os.system ("cls")
        print('Gracias por usar la aplicacion!!!')
        bandera=False
    if int(opcion)>6 or  int(opcion)<1:
        print('opcion incorrecta!!!')
