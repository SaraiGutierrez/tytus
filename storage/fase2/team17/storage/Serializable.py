# File:         Archivo con metodos para crear y cargar archivos binarios.
# Developer:    Andree Avalos

import pickle, os

def commit(objeto, nombre):
    initCheck()
    file = open("Data/storageManager/"+nombre.lower() + ".bin", "wb+")
    file.write(pickle.dumps(objeto))
    file.close()

def rollback(nombre):
    file = open("Data/storageManager/"+nombre.lower() + ".bin", "rb")
    b = file.read()
    file.close()
    return pickle.loads(b)

def initCheck():
    if not os.path.exists('Data/storageManager'):
        os.makedirs('Data/storageManager')
