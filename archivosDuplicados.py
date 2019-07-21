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
        return True
    else:
        print('El archivo no existe:', archivo)
        return False

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
        print ('creado enlace simbolico')
        return True
    except ex:
        print ('Excepcion generada:', str(ex))
        return False

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
    print ('  python3 duplicados.py [opcion] [DIR] [ALGORITMO]')
    print ()
    print (' - DIR: Directorio raíz donde realizar la búsqueda usa "." por defecto')
    print (' - ALGORITMO: Algoritmo para obtener digestos "sha1" por defecto')
    print ('              permitidos; md5,sha1,sha224,sha256,sha384,sha512')
    print (' opcion:')
    print ('   d: Elimina los archivos duplicados dejando solo un archivo fuente.')
    print ('   s: Elimina los archivos duplicados y crea un enlace simbolico hacia el archivo fuente en lugar de los archivos eliminados.')
    print ('EJEMPLO')
    print ('    python3 duplicados.py /tmp/dir1')
    print ('    python3 duplicados.py -d /tmp/dir1')
    print ('    python3 duplicados.py -s /tmp/dir1')

# main
files = []
directory='.'
hashAlgorithm = "sha1"

eliminar_duplicados = False
crear_enlaces_simbolicos = False

if (len(sys.argv) > 1):
    if (sys.argv[1] != ''):
        if (sys.argv[1]=='-h' or sys.argv[1]=='--help'):
            use()
            exit(0)
        if (sys.argv[1]=='-d'):
            eliminar_duplicados = True
            directory=sys.argv[2]
        elif (sys.argv[1]=='-s'):
            crear_enlaces_simbolicos = True
            directory=sys.argv[2]
        else:
            directory=sys.argv[1]

if (len(sys.argv) > 3):
    if (eliminar_duplicados or crear_enlaces_simbolicos and sys.argv[3] != ''):
        if (sys.argv[3]=='sha1' or sys.argv[3]=='md5' or sys.argv[3]=='sha224'
            or sys.argv[3]=='sha256' or sys.argv[3]=='sha512'):
            hashAlgorithm = sys.argv[3]
        else:
            use()
            exit(0)

############## Programa principal             
files = getList(directory)
digests = digests(files, hashAlgorithm)
duplicados = 0
completados = []
erroneos = []

for digest, lista in digests.items():
    # verbose
    #print (digest, lista)
    
    if len(lista) > 1:
        # significa que hay archivos duplicados
        listaDuplicados = []
        duplicados += 1
        fuente = lista[0]
        c = 0
        for file in lista:
            listaDuplicados.append(file)
            if eliminar_duplicados and c > 0:
                if eliminarArchivo(file):
                    completados.append(file)
                else:
                    erroneos.append(file)
            if crear_enlaces_simbolicos and c > 0:
                if eliminarYCrearEnlaceSimbolico(fuente, file):
                    completados.append(file)
                else:
                    erroneos.append(file)
            c += 1
        # mostrando
        for file in listaDuplicados:
            print (file)
        print (len(listaDuplicados))
        print ()

print ('')
print ('# completados satisfactoriamente #')
for file in completados:
    print (file)
print ('')
print ('# errores generados #')
for file in erroneos:
    print (file)
print ('----')
print (' - Total Duplicados:', str(duplicados))
print (' - Completados:', str(len(completados)))
print (' - Erroneos:', str(len(erroneos)))
exit(0)

