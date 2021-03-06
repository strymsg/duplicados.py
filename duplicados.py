#!/usr/bin/python3
'''
Buscador de archivos duplicados en un árbol de directorios
Copyright (C) 2018 Rodrigo Garcia <strysg@riseup.net>
'''
import hashlib
import os
import sys

# helpers
def getList(directory="."):
    ''' retorna una lista con los nombres de todos los archivos dentro el 
    directorio actual.
    * basado en https://stackoverflow.com/questions/120656/directory-tree-listing-in-python#120701
    '''
    files = []
    for dirname, dirnames, filenames in os.walk(directory):
        # for subdirname in dirnames:
        #     files.append(os.apth.join(dirname, subdirname))
        for filename in filenames:
            files.append(os.path.join(dirname,filename))
    return files

def digest(filename, algorithm='sha1'):
    ''' returns hexdigest of the given filename using the gibe algorithm '''
    with open(filename, 'r+b') as fil:
        if (algorithm == 'sha1'):
            return hashlib.sha1(fil.read()).hexdigest()
        elif (algorithm == 'sha224'):
            return hashlib.sha224(fil.read()).hexdigest()
        elif (algorithm == 'sha256'):
            return hashlib.sha256(fil.read()).hexdigest()
        elif (algorithm == 'sha384'):
            return hashlib.sha384(fil.read()).hexdigest()
        elif (algorithm == 'sha512'):
            return hashlib.sha512(fil.read()).hexdigest()
        elif (algorithm == 'md5'):
            return hashlib.md5(fil.read()).hexdigest()
        print ('Invalid algorithm')
        return ""
            
def digests(fileList, algorithm='sha1'):
    ''' Retorna un diccionario con los digestos calculados de la lista de
    archivos `fileList'.
    '''
    dict = {}
    for file in fileList:
        d = digest(file)
        if d in dict:
            l = dict[d]
            l.append(file)
            dict[d] = l
        
    for file in fileList:
        d = digest(file)
        if d in dict:
            # duplicado encontrado
            l = dict[d]
            l.append(file)
            dict[d] = l
        else:
            l = []
            l.append(file)
            dict[d] = l
    return dict

def eliminarArchivo(archivo):
    ''' elimina el archivo con ruta absoluta 
    -- return: True si lo logra.
    '''
    if os.path.exists(archivo):
        os.remove(archivo)
    else:
        print('El archivo no existe:', archivo)

def crearEnlaceSimbolico(fuente, destino):
    ''' crea un enlace simbolico que hace que `destino' apunte a `fuente' 
    -- return: True si lo logra.
    '''
    if not os.path.exists(fuente):
        print ('El archivo no existe:', fuente)
        return False
    if not os.path.exists(destino):
        print ('El archivo no existe:', destino)
        False
    try:
        os.symlink(fuente, destino)
        return True
    except ex:
        print ('Excepcion generada:', str(ex))

def eliminarYCrearEnlaceSimbolico(fuente, destino):
    ''' Elimina el archivo `destino' y en el mismo directorio crea un enlace simbolico
    que apunta al archivo `fuente'.
    -- return: True si lo logra.
    '''
    if not eliminarArchivo(destino):
        return False
    if not crearEnlaceSimbolico(fuente, destino):
        return False
    return True

def use():
    print ('Obtiene un lista de archivos duplicados desde un directorio raíz')
    print ('Cada linea contiene los archivos que se ha detectado iguales')
    print ()
    print ('  python3 duplicados.py [DIR] [ALGORITMO]')
    print ()
    print (' - DIR: Directorio raíz donde realizar la búsqueda usa "." por defecto')
    print (' - ALGORITMO: Algoritmo para obtener digestos "sha1" por defecto')
    print ('              permitidos; md5,sha1,sha224,sha256,sha384,sha512')

# main
files = []
directory='.'
hashAlgorithm = "sha1"
separador = "\t"

if (len(sys.argv) > 1):
    if (sys.argv[1] != ''):
        if (sys.argv[1]=='-h' or sys.argv[1]=='--help'):
            use()
            exit(0)

        directory=sys.argv[1]
if (len(sys.argv) > 2):
    if (sys.argv[2] != ''):
        if (sys.argv[2]=='sha1' or sys.argv[2]=='md5' or sys.argv[2]=='sha224'
            or sys.argv[2]=='sha256' or sys.argv[2]=='sha512'):
            hashAlgorithm = sys.argv[2]
        else:
            use()
            exit(0)

files = getList(directory)
digests = digests(files, hashAlgorithm)
for digest, lista in digests.items():
    # verbose
    #print (digest, lista)
    
    if len(lista) > 1:
        s = ''
        for file in lista:
            s += file + separador
        print(s[:-1])
exit(0)

