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
#Para ver que gestor de paquetes esta usando
import shutil


# Funciones

def dependencias():
    #Comprobar si estan las herramientas instaladas
    dependencias=["efq"]
    installed=True
    for i in dependencias:
        if shutil.which("pacman"):
            pacman = subprocess.run(["pacman", "-Qi", i], capture_output=True)
            if pacman.returncode != 0:
                installed = False
        elif shutil.which("dpkg"):
            dpkg = subprocess.run(["dpkg", "-s", i], capture_output=True)
            if dpkg.returncode != 0:
                installed = False
# Tengo que mirar como ir comprobando paquete por paquete
dependencias()

if 7 != 0:
        print("nmap is not install")

        print("Sugerencias para instalarlo:")
        print("  • Debian/Ubuntu/Kali: sudo apt install nmap")
        print("  • Arch Linux:         sudo pacman -S nmap")


def spinner_animacion(stop_event):
    caracteres = ['[-]', '[\\]', '[|]', '[/]']
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{caracteres[i % len(caracteres)]} Cargando...")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

def argumentos(args):
    if len(args) == 2:
        ip = args[1]
    elif len(args) > 2:
        print("To many arguments, example: script.py [x.x.x.x]")
        sys.exit(1)
    else:
        print("The program requires an argument: script.py [x.x.x.x]")
        sys.exit(1)

def verificarIp(ip):
    ip_separada = ip.split(".")
    if len(ip_separada) == 4:
        for i in ip_separada:
            i = int(i)
            if i > 255:
                print("The ip isn't valid")
                sys.exit(1)
    else:
        print("The ip isn't valid")
        sys.exit(1)

def ping(ip):
    stop_event = threading.Event()
    hilo = threading.Thread(target=spinner_animacion, args=(stop_event,))
    hilo.start()  

    try:
        ping = subprocess.run(["ping", ip, "-c", "1"], capture_output=True, text=True)

    finally:
        # Detener la animación
        stop_event.set()
        hilo.join()

        if ping.returncode == 1:
            print("\r[X] There's not conection with the machine")
            sys.exit(1)
    
    print(("\r[✓] Ping correcto"))
    return ping.stdout

def whichOS(ping):
    ttl = int(re.findall(r"ttl=(\d+)", ping)[0])

    #Comprobamos que sistema es por su ttl
    if ttl >= 0 and ttl <= 64:
        print("Linux")
    elif ttl >= 65 and ttl <= 128:
        print("Windows")
    else:
        print("Not found")

def nmapscan(ip):
    stop_event = threading.Event()
    hilo = threading.Thread(target=spinner_animacion, args=(stop_event,))
    hilo.start()

    try:
        escaneo = subprocess.run(["nmap", "-p-", "--open", "-sS", "--min-rate", "5000", "-n", "-Pn", ip], capture_output=True, text=True)

        escaneo = escaneo.stdout

        #(\d{1,5}) captura un número entre 1 y 5 cifras, /tcp justo después debe haber “/tcp”, \s+open uno o más espacios y luego la palabra “open”
        encontrados = re.findall(r"(\d{1,5})/tcp\s+open", escaneo)

        #Toma solo la parte numérica antes del /
        puertos = [e.split("/")[0] for e in encontrados]

        #Une con comas
        puertos =  ",".join(puertos)

        print(f"\rThe open ports are:\n{puertos} ")
        
        #Guarda la info en el archivo nmapscan
        subprocess.run(["nmap", "-p", puertos, "-sCV", ip, "-oN", "nmapscan"], capture_output=True, text=True)
        

    finally:
        # Detener la animación
        stop_event.set()
        hilo.join()
        print("\rEscaneo completado, guardado en el archvio nmapscan. Recomendable visualizar con (bat nmapscan -l java)")

    


def main():
    #Verifica si se han dado argumentos
    argumentos(sys.argv)
    #Definimos la variable ip con el parametro que seria la ip
    ip = sys.argv[1]
    #Verificamos que la ip dada es correcta
    verificarIp(ip)
    
    whichOS(ping(ip))

    nmapscan(ip)

main()



# ########## NMAP ##########           
#     stop_event = threading.Event()
#     hilo = threading.Thread(target=spinner_animacion, args=(stop_event,))
#     hilo.start()

#     try:
#         escaneo = subprocess.run(["nmap", "-p-", "--open", "-sS", "--min-rate", "5000", "-n", "-Pn", ip], capture_output=True, text=True)

#         escaneo = escaneo.stdout

#         #(\d{1,5}) captura un número entre 1 y 5 cifras, /tcp justo después debe haber “/tcp”, \s+open uno o más espacios y luego la palabra “open”
#         encontrados = re.findall(r"(\d{1,5})/tcp\s+open", escaneo)

#         #Toma solo la parte numérica antes del /
#         puertos = [e.split("/")[0] for e in encontrados]

#         #Une con comas
#         puertos =  ",".join(puertos)

#         print(f"\rThe open ports are:\n{puertos} ")
        
#         #Guarda la info en el archivo nmapscan
#         subprocess.run(["nmap", "-p", puertos, "-sCV", ip, "-oN", "nmapscan"], capture_output=True, text=True)
        

#     finally:
#         # Detener la animación
#         stop_event.set()
#         hilo.join()
#         print("\rEscaneo completado, guardado en el archvio nmapscan. Recomendable visualizar con (bat nmapscan -l java)")
