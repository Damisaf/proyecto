'''
Proyecto [Python]
-----------------------------
Autor: Damian Safdie
Version: 1.0


'''

import csv


def generar_id(archivo):
    with open(archivo, 'r') as csvarch:
        data = list(csv.DictReader(csvarch))
        if len(data) > 0:
            ultima_fila = data[-1]
            ultimo_id = int(ultima_fila.get('id'))
        else:
            ultimo_id = 0
    return ultimo_id + 1


def ingresar_nuevo_usuario():
    # Solicitar valores al usuario
    id = generar_id("usuarios.csv")
    while True:
        # nombre = str(input('Nombre: '))
        nombre = " "
        # apellido = str(input('Apellido: '))
        apellido = " "
        usuario = str(input('Usuario: '))
        # contra = str(input('Password: '))
        contra = " "
        lista_apuesta = ""
        for i in range(64):
            lista_apuesta += "."
        with open("usuarios.csv", 'r') as csvarch:
            data = list(csv.DictReader(csvarch))
        existe = False
        for i in range(len(data)):
            if usuario == data[i].get("usuario"):
                existe = True
        if existe:
            print("usario existenete")
        else:
            break

    # Construir usuario  insertar en nuestro usuarios.csv
    nuevo = {
        "id": id,
        "nombre": nombre,
        "apellido": apellido,
        "usuario": usuario,
        "contra": contra,
        "apuesta": lista_apuesta
    }

    # Abrir archivo CSV y agregar el nuevo usuario
    with open('usuarios.csv', 'a', newline='') as csvfile:
        header = ['id', 'nombre', 'apellido', 'usuario', 'contra', 'apuesta']
        writer = csv.DictWriter(csvfile, header)
        writer.writerow(nuevo)
    pass


def muestro_partidos(opcion, apuesta):
    with open("partidos.csv", 'r') as csvarch:
        partidos = list(csv.DictReader(csvarch))
    for i in range(64):
        un_partido = partidos[i]
        equipo1 = un_partido.get('equipo1')
        equipo2 = un_partido.get('equipo2')
        if opcion == 2:
            resul = un_partido.get('resultado')
        else:
            resul = apuesta[i]
        if resul == "L":
            apu = equipo1
        elif resul == "E":
            apu = "EMPATE"
        elif resul == "V":
            apu = equipo2
        else:
            apu = "--------"
        num = str(i+1).zfill(2)
        if opcion == 1:
            print (num, equipo1.ljust(15), "VS", equipo2.ljust(15), "tu apuesta: ", apu)
        else:
            print (num, equipo1.ljust(15), "VS", equipo2.ljust(15), "Resultado: ", apu)


def valido_usuario():
    id = 0
    apuesta = ""
    while True:
        with open("usuarios.csv", 'r') as csvarch:
            data = list(csv.DictReader(csvarch))
        existe = False
        if len(data) > 0:
            quien = input("ingrese nombre de usuario: ")
            for i in range(len(data)):
                if quien == data[i].get("usuario"):
                    existe = True
                    id = data[i].get("id")
                    apuesta = data[i].get("apuesta")
                    break
            if existe:
                break
            else:
                print("usario inexistenete")
        else:
            print ("no hay usuarios generados")
            break
    return id, apuesta


def refresco_usuario(id):
    with open("usuarios.csv", 'r') as csvarch:
        data = list(csv.DictReader(csvarch))
    for i in range(len(data)):
        if id == data[i].get("id"):
            apuesta = data[i].get("apuesta")
    return id, apuesta


def guardo_apuesta(id_usuario, i_partido, pronostico):
    with open("usuarios.csv", 'r') as csvarch:
        data = list(csv.DictReader(csvarch))
        for i in range(len(data)):
            if id_usuario == data[i].get("id"):
                lista = data[i].get("apuesta")
                nueva_lista = ""
                for j in range(64):
                    if j != i_partido:
                        nueva_lista += lista[j]
                    else:
                        nueva_lista += pronostico
                data[i]['apuesta'] = nueva_lista
                break
    with open('usuarios.csv', 'w', newline='') as csvfile:
        header = ['id', 'nombre', 'apellido', 'usuario', 'contra', 'apuesta']
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)


def generar_apuestas(id_usuario, apuesta):
    muestro_partidos(1, apuesta)
    while True:
        while True:
            op = input("Ingrese el numero del partido a pronosticar: ")
            if op.isdigit():
                break
        opcion = int(op)
        if opcion > 0 and opcion < 65:
            break
    while True:
        if opcion < 49:  # fase de grupos
            pronostico = input ("Ingrese L/E/V  (Local,Empate,Visitante): ")
            p = pronostico.upper()
            if p == "L" or p == "E" or p == "V":
                break
        else:
            pronostico = input ("Ingrese L/V  (Local,Visitante): ")
            p = pronostico.upper()
            if p == "L" or p == "V":
                break
    pronostico = p
    guardo_apuesta(id_usuario, opcion-1, pronostico)
    return pronostico


if __name__ == '__main__':
    while True:
        menu = '''\n
        Seleccione una opcion:
        1. Generar un nuevo usuario
        2. Registrar pronosticos
        3. Registrar resultados de los partidos
        4. Ver tabla de posiciones
        5. Salir
        Opcion elegida: '''
        while True:
            opcion = input(menu)
            if opcion.isdigit():
                break
            else:
                print("Opcion incorrecta")
        opcion = int(opcion)
        if opcion == 1:
            # nuevo usuario
            ingresar_nuevo_usuario()
        elif opcion == 2:
            id_usuario, apuesta = valido_usuario()
            if id_usuario != 0:
                while True:
                    generar_apuestas(id_usuario, apuesta)
                    while True:
                        otro = input("Desea Hacer otro pronostico [S/N]: ")
                        op = otro.upper()
                        if op == "N" or op == "S":
                            break
                    if op == "N":
                        break
                    id_usuario, apuesta = refresco_usuario(id_usuario)            
        elif opcion == 3:
            # registar resultados de los partidos del mundial
            muestro_partidos(2, "")
            while True:
                while True:
                    op = input("Ingrese el numero del partido: ")
                    if op.isdigit():
                        break
                opcion = int(op)
                if opcion > 0 and opcion < 65:
                    break
            if opcion < 49:  # fase de grupos
                while True:
                    resultado = input ("Ingrese L/E/V  (Local,Empate,Visitante): ")
                    p = resultado.upper()
                    if p == "L" or p == "V" or p == "E":
                        break
            else:
                while True:
                    resultado = input ("Ingrese L/V  (Local,Visitante): ")
                    p = resultado.upper()
                    if p == "L" or p == "V":
                        break
            with open("partidos.csv", 'r') as csvarch:
                data = list(csv.DictReader(csvarch))
                data[opcion-1]['resultado'] = resultado
            with open('partidos.csv', 'w', newline='') as csvfile:
                header = ['id', 'fecha', 'grupo', 'hora', 'equipo1', 'equipo2', 'gol1', 'gol2', 'resultado']
                writer = csv.DictWriter(csvfile, fieldnames=header)
                writer.writeheader()
                writer.writerows(data)

        elif opcion == 4:
            # genera tabla de posiciones
            with open("partidos.csv", 'r') as csvarch:
                resultados = []
                data = list(csv.DictReader(csvarch))
                for i in range(len(data)):
                    resultado = data[i].get("resultado")
                    resultados.append(resultado)
            with open("usuarios.csv", 'r') as csvarch:
                data = list(csv.DictReader(csvarch))
                posiciones = []
                for i in range(len(data)):
                    usuario = data[i].get("usuario")
                    apuesta = data[i].get("apuesta")
                    puntos = 0
                    for p in range(64):
                        if apuesta[p] == resultados[p]:
                            puntos += 1
                    apostador = (str(puntos).zfill(4), usuario)
                    posiciones.append(apostador)
                tabla = sorted(posiciones, reverse=True)
                print("-------------------")
                print("TABLA DE POSICIONES  ")
                print("-------------------")
                for i in range(len(tabla)):
                    item = tabla[i]
                    usuario = item[1]
                    puntos = int(item[0])
                    print(usuario.ljust(15, "."), puntos)
        elif opcion == 5:
            break
