from tabulate import tabulate
from colorama import Fore, Back, Style, init
init(autoreset=True)
import string
import random
import os

def iniciar_juego():
    #preguntas iniciales para inicializar el juego
    nombre_usuario = input("Dime tu nombre, humano: ").capitalize()

    pregunta_empezar = input(f"Hola, {nombre_usuario}, ¿Quieres jugar a 'Hundir la Flota'? ")
    while pregunta_empezar.lower() not in ["si", "no"]:
        print("Por favor, responde con 'si' o 'no'")
        pregunta_empezar = input("Quieres jugar a 'Hundir la Flota'? ")

    if pregunta_empezar.lower() == "no":
        print("Cobarde, ¡Hasta luego!")
        return None

    elif pregunta_empezar.lower() == "si":
        print(f"Genial, que empiece el juego, mucha suerte, {nombre_usuario}")
        return nombre_usuario

class Tablero:

    def __init__(self):
        #tablero vacio
        self.tablero = []
        for x in range(10):
            #añadir 10 puntos por cada numero del 0 al 9
            fila =  ["."] * 10
            #append de los puntos al tablero
            self.tablero.append(fila)
            
        self.barcos = []

    def convertir_letra_numero(self,letra):
        # metodo para convertir la letra de la columna a numero para la colocacion y disparo
        letras = []
        for x in string.ascii_uppercase[0:len(self.tablero)]:
            letras.append(x)
        #devolvemos el indice de la letra a buscar
        return letras.index(letra)

    def colocar_barcos_usuario(self):
        print("Coloca tus barcos")
        barcos_usuario = {1: 4, 2: 3, 3: 2, 4: 1}  # GENERAMOS DICCIONARIO DE BARCOS CON ESLORA:CANTIDAD

        for eslora, cantidad in barcos_usuario.items():
            for _ in range(cantidad):  # Coloca la cantidad necesaria de cada tipo
                while True:
                    print(f"Coloca un barco de {eslora} casilla(s).")
                    try:
                        fila = int(input("Introduce la fila (0-9): "))
                        columna = input("Introduce la letra (A-J): ").upper()
                        columna = self.convertir_letra_numero(columna)  # CONVERTIMOS A INT LA LETRA CON EL METODO DE CONVERTIR LETRA
                        orientacion = "H"
                        if eslora > 1:
                            orientacion = input("Introduce la orientación (H para horizontal, V para vertical): ").upper()

                        # Validar la posición del barco
                        if not self.validar_posicion(fila, columna, eslora, orientacion):
                            print("Posición inválida. Intenta de nuevo.")
                            continue

                        # Colocar el barco en el tablero
                        self.colocacion_usuario(fila, columna, eslora, orientacion)
                        break
                    except Exception as e:
                        print(f"Error: {e}. Intenta de nuevo.")

    def colocar_barcos_pc(self):
        barcos_pc = {1: 4, 2: 3, 3: 2, 4: 1}

        for eslora, cantidad in barcos_pc.items():
            for _ in range(cantidad):  # Coloca la cantidad necesaria de cada tipo
                while True:
                    try:
                        fila = random.randint(1,9)
                        random_num = random.randint(1,9)
                        letras = string.ascii_uppercase[0:len(self.tablero)]
                        columna = letras[random_num]
                        columna = self.convertir_letra_numero(columna)  # CONVERTIMOS A INT LA LETRA CON EL METODO DE CONVERTIR LETRA
                        orientacion = "H"
                        if eslora > 1:
                            opciones_letra = ["H", "V"]
                            random_opciones = random.randint(0,1)
                            orientacion = opciones_letra[random_opciones]

                        # Validar la posición del barco
                        if not self.validar_posicion(fila, columna, eslora, orientacion):
                            continue

                        # Colocar el barco en el tablero
                        self.colocacion_pc(fila, columna, eslora, orientacion)
                        break
                    except Exception as e:
                        pass

    def colocacion_usuario(self, fila, columna, eslora, orientacion):
        if orientacion == "H":
            for i in range(eslora):
                self.tablero[fila][columna + i] = Fore.RED + str("B") + Style.RESET_ALL
        elif orientacion == "V":
            for i in range(eslora):
                self.tablero[fila + i][columna] = Fore.RED + str("B") + Style.RESET_ALL
        print("Barco colocado correctamente.")
        self.mostrar_tablero()

    def colocacion_pc(self, fila, columna, eslora, orientacion):
        if orientacion == "H":
            for i in range(eslora):
                self.tablero[fila][columna + i] = Fore.GREEN + str("B") + Style.RESET_ALL
        elif orientacion == "V":
            for i in range(eslora):
                self.tablero[fila + i][columna] = Fore.GREEN + str("B") + Style.RESET_ALL

    def validar_posicion(self, fila, columna, eslora, orientacion):

        if orientacion == "H":
            # Comprobar si cabe horizontalmente
            if columna + eslora > 10:
                return False
            # Comprobar que no haya otros barcos
            for i in range(eslora):
                if self.tablero[fila][columna + i] != "." or self.barcos_alrededor(fila, columna+1):
                    return False
        elif orientacion == "V":
            # Comprobar si cabe verticalmente
            if fila + eslora > 10:
                return False
            # Comprobar que no haya otros barcos
            for i in range(eslora):
                if self.tablero[fila + i][columna] != "." or self.barcos_alrededor(fila+1, columna):
                    return False
        return True

    def barcos_alrededor(self, fila, columna):

        for x in range(fila-1, fila+2):
            for i in range(columna-1, columna+2):
                if 0<=x<10 and 0<=i<10:
                    if self.tablero[x][i] == "B":
                        return True
        return False

    def disparar_usuario(self,fila,columna):
        print("Tu turno")
        fila = int(input("Introduce la fila (0-9): "))
        columna = input("Introduce la letra (A-J): ").upper()
        columna = self.convertir_letra_numero(columna)

        tocado = False
        if self.tablero[fila][columna] == "B":
            print("Tocado")
            tocado = True
        elif self.tablero[fila][columna] == ".":
            print("Agua")
            tocado = False
        else:
            print("Introduce las coordenadas correctas")

        while True:
            self.tablero[fila][columna] = "X"

        if not tocado:
            self.tablero[fila][columna] = "o"

    def disparar_pc(self):
        pass

    def mostrar_tablero(self):
        headers = []
        for x in string.ascii_uppercase[0:len(self.tablero)]:    # IMPORTAMOS EL ALFABETO Y HACEMOS QUE VAYA DE LA 'A' A LA 'J'
            headers.append(x)                                    # APPEND A LA LISTA 'HEADERS'

        columna_numeros = []
        for x in range(len(self.tablero)):  # CHECKEAMOS LA LONGITUD DE LOS ELEMENTOS DE TABLERO
            columna_modificada = [str(x)]  # METEMOS CADA ELEMENTO EN UNA LISTA TIPO STRING EN VEZ DE INT
            for elemento in self.tablero[x]:  # RECORREMOS LOS ELEMENTOS LA FILA ORIGINAL
                columna_modificada.append(elemento)  #
            columna_numeros.append(columna_modificada) #

        print(Style.BRIGHT+tabulate(columna_numeros,headers=[""]+ headers, stralign="center", tablefmt="rounded_grid"))  # 'HEADERS' ES EL HEADERS DE LA TABLA


# iniciar_juego()
tablero_usuario = Tablero()
tablero_pc = Tablero()

tablero_usuario.mostrar_tablero()
tablero_usuario.colocar_barcos_usuario()
# os.system("cls")
# tablero_usuario.mostrar_tablero()


# tablero_pc.colocar_barcos_pc()
# tablero_pc.mostrar_tablero()

# tablero_pc.barcos_alrededor(0,0)







