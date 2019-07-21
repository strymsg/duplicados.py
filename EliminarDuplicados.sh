#!/bin/bash
# Eliminar archivos duplicados en contenido dejando una copia

DIR=$1
SALIDA_TEMP1='/tmp/duplicados.txt'

C1='/tmp/duplicados-f1.txt'
C2='/tmp/duplicados-f2.txt'

veces='0'

# Elimina repetidos
eliminar_repetidos_de_linea () {
    linea=$1
    veces=$2
    echo "=>($veces): $linea"
    # para iterar desde el segundo argumento (dejando el primero como la fuente)
    #for((i=2;i<$veces+1;i++))
    i=0
    while [ $i -lt $veces ]
    do
	let "e = i+2"
	echo "   . $i . $e"
	echo $linea | cut -f$e
	#archivo_eliminar=$(echo $linea | cut -f$e)
    	#echo "eliminando: $archivo_eliminar"
	((i++))
    	# ls "$archivo_eliminar"
    	# aqui los comandos para eliminar
    	#rm "$archivo_eliminar"
    done
}

python3 duplicados.py $DIR > $SALIDA_TEMP1

# Recorriendo linea por linea
while read -r linea
do
    # contando numero de duplicados
    # echo "$linea"
    veces=$(echo "$linea" | grep -o "$(printf '\t')" | wc --line)
    # echo "$linea --> $veces"
    eliminar_repetidos_de_linea "$linea" "$veces"
    # ls $linea
    # rm -f "$linea"; # eliminando el archivo
done < $SALIDA_TEMP1

echo "Archivos duplicados eliminados: $(wc --lines $C1)"

