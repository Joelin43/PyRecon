# Libreria SYS, para poder acceder al argumento que me pasen
import sys
# Subprocess para ejecutar comandos aparte del script
import subprocess
import re

# Comprobamos que si haya un argumento
ip = "127.0.0.1"

def comprobarArgs():
    if len(sys.argv) == 2:
        ip = sys.argv
    elif len(sys.argv) > 2:
        print("Demasiados argumentos, que sea solo: script.py [x.x.x.x]")
    else:
        print("El programa requiere de un argumento: script.py [x.x.x.x]")

# Comprobar que es una ip correcta

ip_separada = ip.split(".")

funciona = True

for i in ip_separada:
    i = int(i)
    if i > 255:
        funciona = False
        break
    else:
        funciona = True

if funciona:
    #Hacemos ping
    ping = subprocess.run(["ping", ip, "-c 1"], capture_output=True, text=True)
    
    #Separamos los resultados
    ping = ping.stdout.split()

    #Sacamos el valor del ttl
    ping = ping[12]
    #Esta expresion regular busca: \d cualquier numero, {1,3} que tenga entre 1 y 3 digitos
    ttl = int(re.findall(r"\d{1,3}", ping)[0])

    #Comprobamos que sistema es por su ttl
    if ttl >= 0 and ttl <= 64:
        print("Linux")
    elif ttl >= 65 and ttl <= 128:
        print("Windows")
    else:
        print("Not found")

#NMAP
    escaneo = subprocess.run(["nmap", "-p-", "--open", "-sS", "--min-rate", "5000", "-n", "-Pn", ip], capture_output=True, text=True)

    escaneo = escaneo.stdout

    # (\d{1,5}) captura un número entre 1 y 5 cifras, /tcp justo después debe haber “/tcp”, \s+open uno o más espacios y luego la palabra “open”
    encontrados = re.findall(r"(\d{1,5})/tcp\s+open", escaneo)


    # Toma solo la parte numérica antes del /
    puertos = [e.split("/")[0] for e in encontrados]

    # Une con comas
    puertos =  ",".join(puertos)

    print(puertos)

    escaneo2 = subprocess.run(["nmap", "-p", puertos, "-sCV", ip, "-oN targeted"], capture_output=True, text=True)

