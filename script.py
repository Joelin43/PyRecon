# Libreria SYS, para poder acceder al argumento que me pasen
import sys
# Subprocess para ejecutar comandos aparte del script
import subprocess
# Para poder usar expresiones regulares
import re
# Para crear hilos aparte del programa principal
import threading
# Para usar el sleep
import time



def spinner_animacion():
    # Los caracteres que rotarán
    caracteres = ['[-]', '[\\]', '[|]', '[/]']
    i = 0
    while animar:
        # \r vuelve al inicio, end="" evita el salto de línea
        sys.stdout.write(f"\r{caracteres[i % len(caracteres)]} Cargando...")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1


try:
############### Arguments ###############
    if len(sys.argv) == 2:
        ip = sys.argv[1]

    elif len(sys.argv) > 2:
        raise Exception ("To many arguments, example: script.py [x.x.x.x]")
    else:
        raise Exception ("The program requires an argument: script.py [x.x.x.x]")

############### Correct Ip ###############
    ip_separada = ip.split(".")

    for i in ip_separada:
        i = int(i)
        if i > 255:
            raise Exception ("The ip isn't correct")
 
############### Ping ###############
    animar = True
    hilo = threading.Thread(target=spinner_animacion)
    hilo.start()

    try:
        ping = subprocess.run(["ping", ip, "-c 1"], capture_output=True, text=True)

    finally:
        # Detener la animación
        animar = False
        hilo.join()

        if ping.returncode == 1:
            raise Exception ("\r[X] There's not conection with the machine")
    
    print(("\r[✓] Ping correcto"))

############### Sistema Operativo ###############
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
            
    animar = True
    hilo = threading.Thread(target=spinner_animacion)
    hilo.start()

    try:
########## NMAP ##########
        escaneo = subprocess.run(["nmap", "-p-", "--open", "-sS", "--min-rate", "5000", "-n", "-Pn", ip], capture_output=True, text=True)

        escaneo = escaneo.stdout

        # # (\d{1,5}) captura un número entre 1 y 5 cifras, /tcp justo después debe haber “/tcp”, \s+open uno o más espacios y luego la palabra “open”
        encontrados = re.findall(r"(\d{1,5})/tcp\s+open", escaneo)

        # # Toma solo la parte numérica antes del /
        puertos = [e.split("/")[0] for e in encontrados]

        # # Une con comas
        puertos =  ",".join(puertos)

        print(puertos)
# Guardar output  en archivo (Open)
        escaneo2 = subprocess.run(["nmap", "-p", puertos, "-sCV", ip, "-oN targeted"], capture_output=True, text=True)

    finally:
        # Detener la animación
        animar = False
        hilo.join()
        print("\r Escaneo completado ")



except Exception as e:

    print(e)

    # ########## NMAP ##########
    # escaneo = subprocess.run(["nmap", "-p-", "--open", "-sS", "--min-rate", "5000", "-n", "-Pn", ip], capture_output=True, text=True)

    # escaneo = escaneo.stdout

    # # (\d{1,5}) captura un número entre 1 y 5 cifras, /tcp justo después debe haber “/tcp”, \s+open uno o más espacios y luego la palabra “open”
    # encontrados = re.findall(r"(\d{1,5})/tcp\s+open", escaneo)

    # # Toma solo la parte numérica antes del /
    # puertos = [e.split("/")[0] for e in encontrados]

    # # Une con comas
    # puertos =  ",".join(puertos)

    # print(puertos)

    # escaneo2 = subprocess.run(["nmap", "-p", puertos, "-sCV", ip, "-oN targeted"], capture_output=True, text=True)