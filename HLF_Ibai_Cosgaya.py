from tabulate import tabulate
from colorama import Fore, Back, Style, init
init(autoreset=True)
import string
import random
import os
import time

class Tablero:

    def __init__(self):
        #tablero vacio
        self.tablero = []
        for x in range(10):
            #añadir 10 puntos por cada numero del 0 al 9
            fila =  ["."] * 10
            #append de los puntos al tablero
            self.tablero.append(fila)

        # self.barcos = []

    def convertir_letra_numero(self,letra):
        # metodo para convertir la letra de la columna a numero para la colocacion y disparo
        letras = []
        for x in string.ascii_uppercase[0:len(self.tablero)]:
            letras.append(x)
        #devolvemos el indice de la letra a buscar
        return letras.index(letra)

    def colocar_barcos_usuario_manual(self):
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
                        self.colocacion_usuario_manual(fila, columna, eslora, orientacion)
                        self.mostrar_tablero_usuario()
                        break
                    except Exception as e:
                        print(f"Error: {e}. Intenta de nuevo.")

    def colocar_barcos_usuario_aleatorio(self):
        # {4: 1, 3: 2, 2: 3, 1: 4}
        barcos_usuario = {4: 1, 3: 2, 2: 3, 1: 4}  # Barcos con eslora:cantidad
        for eslora, cantidad in barcos_usuario.items():
            for _ in range(cantidad):  # Coloca la cantidad necesaria de cada tipo
                # intentos = 0
                # max_intentos = 1000  # Límite de intentos para colocar un barco
                while True:#intentos < max_intentos:
                    try:
                        fila = random.randint(0, 9)
                        columna = random.randint(0, 9)
                        orientacion = random.choice(["H", "V"])

                        # Validar la posición del barco
                        if not self.validar_posicion(fila, columna, eslora, orientacion):
                            # intentos += 1
                            continue

                        # Colocar el barco en el tablero
                        self.colocacion_usuario_aleatorio(fila, columna, eslora, orientacion)
                        break
                    except Exception as e:
                        #intentos += 1  # Incrementar intentos en caso de error
                        continue

                # if intentos == max_intentos:  # Si no se puede colocar el barco
                #     print(f"Error: No se pudo colocar un barco de eslora {eslora}.")
                #     return
        time.sleep(2)
        # self.mostrar_tablero_usuario()

    def colocar_barcos_pc(self):
        barcos_pc = {4: 1, 3: 2, 2: 3, 1: 4}

        for eslora, cantidad in barcos_pc.items():
            for _ in range(cantidad): # Coloca la cantidad necesaria de cada tipo
                # intentos = 0
                # max_intentos = 1000
                while True:#intentos < max_intentos:
                    try:
                        fila = random.randint(0, 9)
                        columna = random.randint(0, 9)
                        orientacion = random.choice(["H", "V"])

                        # Validar la posición del barco
                        if not self.validar_posicion(fila, columna, eslora, orientacion):
                            # intentos += 1
                            continue

                        # Colocar el barco en el tablero
                        self.colocacion_pc(fila, columna, eslora, orientacion)
                        break
                    except Exception as e:
                        # intentos += 1  # Incrementar intentos en caso de error
                        continue

                # if intentos == 100:  # Si no se puede colocar el barco
                #     print(f"Error: No se pudo colocar un barco de eslora {eslora}.")
                #     return

        time.sleep(2)
        # self.mostrar_tablero_pc()

    def colocacion_usuario_manual(self, fila, columna, eslora, orientacion):
        if orientacion == "H":
            for i in range(eslora):
                self.tablero[fila][columna + i] = Fore.RED + str("B") + Style.RESET_ALL
        elif orientacion == "V":
            for i in range(eslora):
                self.tablero[fila + i][columna] = Fore.RED + str("B") + Style.RESET_ALL
        print("Barco colocado correctamente.")
        self.mostrar_tablero_usuario()

    def colocacion_usuario_aleatorio(self, fila, columna, eslora, orientacion):
        if orientacion == "H":
            for i in range(eslora):
                self.tablero[fila][columna + i] = Fore.RED + str("B") + Style.RESET_ALL
        elif orientacion == "V":
            for i in range(eslora):
                self.tablero[fila + i][columna] = Fore.RED + str("B") + Style.RESET_ALL

    def colocacion_pc(self, fila, columna, eslora, orientacion):
        if orientacion == "H":
            for i in range(eslora):
                self.tablero[fila][columna + i] =  Fore.GREEN + str("B") + Style.RESET_ALL
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
                if self.tablero[fila][columna + i] != "." or self.barcos_alrededor(fila, columna+i):
                    return False
        elif orientacion == "V":
            # Comprobar si cabe verticalmente
            if fila + eslora > 10:
                return False
            # Comprobar que no haya otros barcos
            for i in range(eslora):
                if self.tablero[fila + i][columna] != "." or self.barcos_alrededor(fila+i, columna):
                    return False
        return True

    def barcos_alrededor(self, fila, columna):

        for x in range(fila-1, fila+2):
            for i in range(columna-1, columna+2):
                if 0 <= x <10 and 0 <= i <10:
                    if "B" in self.tablero[x][i]:
                        return True
        return False

    def disparar_usuario(self, tablero_pc):
        while True:
            try:
                print("Dispara")
                fila = int(input("Introduce la fila (0-9): "))
                columna = input("Introduce la letra (A-J): ").upper()
                columna = self.convertir_letra_numero(columna)

                if not (0<=fila<10) or not (0<=columna<10):
                    print("Fuera del tablero")
                    continue
                if tablero_pc.tablero[fila][columna] in ["X", "o"]:
                    print("Espabila, ya has disparado ahí")
                    continue

                if "B" in tablero_pc.tablero[fila][columna]:
                    print("¡Tocado! Sigue disparando.")
                    tablero_pc.tablero[fila][columna] = Fore.YELLOW + str("X") + Style.RESET_ALL
                    tablero_pc.mostrar_tablero_pc()
                    return True

                else:
                    miss_choices = ["Pringao", "Fallaste", "Tolay", "Melon", "Agua"]
                    print(random.choice(miss_choices))
                    tablero_pc.tablero[fila][columna] = Fore.CYAN + str("o") + Style.RESET_ALL
                return False

            except Exception as e:
                print(f"Error: {e}. Intenta de nuevo.")

    def disparar_pc(self, tablero_usuario):
        while True:
            fila = random.randint(0,9)
            columna = random.randint(0,9)
            # columna = self.convertir_letra_numero(columna)

            if tablero_usuario.tablero[fila][columna] in ["X", "o"]:
                print("Fallé")
                continue

            if "B" in tablero_usuario.tablero[fila][columna]:
                print("¡Acerté! Vuelvo a disparar.")
                tablero_usuario.tablero[fila][columna] = Fore.YELLOW + str("X") + Style.RESET_ALL
                tablero_usuario.mostrar_tablero_usuario()
                return True

            else:
                tablero_usuario.tablero[fila][columna] = Fore.CYAN + str("o") + Style.RESET_ALL

            return False

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

    def mostrar_tablero_usuario(self):
        # os.system("cls")
        self.mostrar_tablero()

    def mostrar_tablero_pc(self):
        # os.system("cls")
        self.mostrar_tablero()

    def mostrar_tablero_pc_oculto(self):
        headers = []
        for x in string.ascii_uppercase[0:len(self.tablero)]:  # IMPORTAMOS EL ALFABETO Y HACEMOS QUE VAYA DE LA 'A' A LA 'J'
            headers.append(x)

        columna_numeros = []
        for x in range(len(self.tablero)):  # CHECKEAMOS LA LONGITUD DE LOS ELEMENTOS DE TABLERO
            fila_oculta = [str(x)]  # METEMOS CADA ELEMENTO EN UNA LISTA TIPO STRING EN VEZ DE INT
            for elemento in self.tablero[x]:  # RECORREMOS LOS ELEMENTOS LA FILA ORIGINAL
                if elemento == Fore.YELLOW + "X" + Style.RESET_ALL:  # Acierto
                    fila_oculta.append(elemento)
                elif elemento == Fore.CYAN + "o" + Style.RESET_ALL:  # Agua
                    fila_oculta.append(elemento)
                else:  # Celdas no reveladas
                    fila_oculta.append(" ")  # Espacio vacío para ocultar barcos
            columna_numeros.append(fila_oculta)  #

        print(Style.BRIGHT + tabulate(columna_numeros, headers=[""] + headers, stralign="center",tablefmt="rounded_grid"))


def iniciar_juego():
    #preguntas iniciales para inicializar el juego
    nombre_usuario = input("Dime tu nombre, humano: ").capitalize()
    pregunta_empezar = input(f"Hola, {nombre_usuario}, ¿Quieres jugar a 'Hundir la Flota'? ")

    while pregunta_empezar.lower() not in ["si", "no"]:
        pregunta_empezar = input("Por favor, responde con 'si' o 'no'")

    if pregunta_empezar.lower() == "no":
        print("Cobarde, ¡Hasta luego!")
        return

    elif pregunta_empezar.lower() == "si":
        print(f"Genial, que empiece el juego, mucha suerte, {nombre_usuario}")

    tablero_usuario = Tablero()
    tablero_pc = Tablero()

    print("Estoy colocando mis barcos...\n")
    tablero_pc.colocar_barcos_pc()

    aleatorio = int(input(f"{nombre_usuario} Pulsa '1' para colocacion manual o '2' para colocacion aleatoria\n"))
    if aleatorio == 1:
        tablero_usuario.colocar_barcos_usuario_manual()
    elif aleatorio == 2:
        print("Colocando tus barcos...\n")
        tablero_usuario.colocar_barcos_usuario_aleatorio()

    turno_usuario = True


    while True:
        print(f"Tu tablero, {nombre_usuario}: \n")
        tablero_usuario.mostrar_tablero_usuario()

        print("Mi tablero:")
        tablero_pc.mostrar_tablero_pc()
        tablero_pc.mostrar_tablero_pc_oculto()

        if turno_usuario:
            print(f"Tu turno, {nombre_usuario}")
            repite_turno = tablero_usuario.disparar_usuario(tablero_pc)

            if not any("B" in "".join(fila) for fila in tablero_pc.tablero):
                print("¡Felicidades! Has hundido todos mis barcos")
                break

            if not repite_turno:
                turno_usuario = False  # Cambiar turno al PC

        else:
            print("Me toca")
            repite_turno = tablero_pc.disparar_pc(tablero_usuario)

            if not any("B" in "".join(fila) for fila in tablero_usuario.tablero):  # Verificar si quedan tus barcos
                print("He ganado, he hundido todos tus barcos")
                break

            if not repite_turno:
                turno_usuario = True  # Cambiar turno al usuario


iniciar_juego()
