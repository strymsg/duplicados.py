# Duplicados.py

Busca archivos duplicados en un árbol de directorios (directorio actual por defecto).

 - Permite eliminar los archivos duplicados
 - Permite enlaces simbólicos cuando se eliminan archivos duplicados, así se puede ahorrar espacio de almacenamiento.


**LICENCIA**: GPLv3

### Uso

```bash
# mostrar los archivos duplicados
python3 archivosDuplicados.py [DIR] [ALGORITMO]
# eliminar los archivos duplicados
python3 archivosDuplicados.py -d [DIR] [ALGORITMO]
# reemplazar los archivos duplicados eliminados por un enlace simbólico que apunta a un archivo origen
python3 archivosDuplicados.py -s [DIR] [ALGORITMO]

# Ejemplos
python3 archivosDuplicados.py /home/joand/directoriof 
python3 archivosDuplicados.py -d /home/joand/ArchivosC
python3 archivosDuplicados.py -s /home/joand/Documentos 
python3 archivosDuplicados.py -h
```
<h6 id='en'>.</h6>
## ENGLISH

Searches for duplicate files in a directory tree (current default directory).

 - Can delete duplicated files.
 - Can create symbolic links in place where a duplicated file has been deleted by this script, use this to save data storage.

### Use

```bash
# Show duplicated files
python3 archivosDuplicados.py [DIR] [ALGORITMO]
# Delete Duplicated Files
python3 archivosDuplicados.py -d [DIR] [ALGORITMO]
# Replace duplicated files by a symbolic link pointing to a source file.
python3 archivosDuplicados.py -s [DIR] [ALGORITMO]

# Examples
python3 archivosDuplicados.py /home/joand/directoriof 
python3 archivosDuplicados.py -d /home/joand/ArchivosC
python3 archivosDuplicados.py -s /home/joand/Documentos 
python3 archivosDuplicados.py -h
```
