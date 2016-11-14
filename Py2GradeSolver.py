#!/usr/bin/env python3.5

# -------------------------------------------------------------------------------------------------------------------------
# Método de resolução de equações de segundo grau pelo método de Bhaskara utilizando programação paralela e banco de dados.
# Matheus Calixto - calixtinn@gmail.com
# IFMG - Campus Formiga / Desenvolvimento Rápido no Linux e Python
# -------------------------------------------------------------------------------------------------------------------------

import time
import os
import sqlite3
import math
import threading as threads
import re

coeficientes = []  # Lista onde a primeira thread vai salvar os coeficientes digitados pelo usuário.
stop = 0  # Variável que controla a execução da segunda thread.


# Função que salva os dados calculados em um arquivo texto.
def salva_dados(conn):
    file = open("saida.txt", "w")
    flag_exibir = False

    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM raizes;""")

    for i in cursor.fetchall():
        if i[4] == 1:
            saida = "Equação: " + str(i[1]) + "\t| Resultado: " + "x1 = " + str(i[2]) + "\tx2 = " + str(i[3]) + "\n"
        elif i[4] == 2:
            saida = "Equação: " + str(i[1]) + "\t| Resultado: " + "x1 = " + str(i[2]) + "\n"
        else:
            saida = "Equação: " + str(i[1]) + "\t| Esta quação não possui solução Real!" + "\n"
        file.write(saida)

    file.close()
    conn.close()

    os.system("clear")

    while not flag_exibir:

        x = input("Os resultados estão presentes no arquivo 'saida.txt'.\nDeseja exibí-los na tela? [S/N] ")

        if x == 's' or x == 'S':
            flag_exibir = True
            os.system("clear")
            os.system("cat saida.txt")
        elif x == 'n' or x == 'N':
            flag_exibir = True
        else:
            print("Opção Inválida!")
    # End While

    os.system("rm raizes.db")


# Função que cria o banco de dados
def cria_banco(conn):
    cursor = conn.cursor()
    cursor.execute("""

    CREATE TABLE raizes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        equation TEXT,
        raiz1 VARCHAR(100),
        raiz2 VARCHAR(100),
        tipo INTEGER
    );

    """)


# Função que insere os dados calculados no banco de Dados raizes.db
def inserir_no_banco(equation, raiz1, raiz2, conn):
    cursor = conn.cursor()

    if raiz2 == 'zero':

        cursor.execute("""

        INSERT INTO raizes (equation, raiz1, tipo)
        VALUES (?, ?, ?)
        """, (equation, raiz1, 2))

    elif raiz1 == 'Delta < 0':

        cursor.execute("""

        INSERT INTO raizes (equation, raiz1, raiz2, tipo)
        VALUES (?, ?, ?, ?)
        """, (equation, raiz1, raiz2, 3))


    else:

        cursor.execute("""

        INSERT INTO raizes (equation, raiz1, raiz2, tipo)
        VALUES (?, ?, ?, ?)
        """, (equation, raiz1, raiz2, 1))

    conn.commit()


# Função que resolve a equação de segundo grau utilizando o método de Bhaskara
def solve_equation(a, b, c):
    delta = math.pow(b, 2) - (4 * a * c)
    denominador = (2 * a)


    if delta < 0:
        return 'erro', 'erro'

    elif delta == 0:

        x = (-b) / denominador
        return x, 'zero'

    else:

        x1 = ((-b) + math.sqrt(delta)) / denominador
        x2 = ((-b) - math.sqrt(delta)) / denominador
        return x1, x2


# Função que recebe os dados do usuário.
def coleta_dados(conn):
    flag = False
    sair = False

    while not sair:

        while flag == False:

            a = input("Digite o coeficiente a: ")

            if a.isdigit():
                flag = True
                a = int(a)

            elif a[0] == '-':

                coef = re.match('-([0-9])+', a)

                if coef is None:
                    print("Você não digitou um número válido...")
                    time.sleep(1.5)
                    os.system("clear")
                else:
                    a = int(coef.group(0))
                    flag = True

            else:
                print("Você não digitou um número válido...")
                time.sleep(1.5)
                os.system("clear")

        # end While coef A

        flag = False

        while flag == False:

            b = input("Digite o coeficiente b: ")

            if b.isdigit():
                flag = True
                b = int(b)

            elif b[0] == '-':

                coef = re.match('-([0-9])+', b)

                if coef is None:
                    print("Você não digitou um número válido...")
                    time.sleep(1.5)
                    os.system("clear")
                else:
                    b = int(coef.group(0))
                    flag = True

            else:
                print("Você não digitou um número válido...")
                time.sleep(1.5)
                os.system("clear")

        # end While coef B

        flag = False

        while flag == False:

            c = input("Digite o coeficiente c: ")

            if c.isdigit():
                flag = True
                c = int(c)

            elif c[0] == '-':

                coef = re.match('-([0-9])+', c)

                if coef is None:
                    print("Você não digitou um número válido...")
                    time.sleep(1.5)
                    os.system("clear")
                else:

                    c = int(coef.group(0))
                    flag = True


            else:
                print("Você não digitou um número válido...")
                time.sleep(1.5)
                os.system("clear")

        # end While coef C

        invalida = True
        coeficientes.append(a)
        coeficientes.append(b)
        coeficientes.append(c)

        while invalida:

            opcao = input("Você deseja calcular outra equação? [S/N] ")

            if opcao == 's' or opcao == 'S':
                invalida = False
                sair = False
                flag = False

            elif opcao == 'n' or opcao == 'N':
                sair = True
                invalida = False
                global stop
                stop = 1

            else:
                print("Opção Inválida!")


# Função onde a Thread 2 verifica se há equações a serem resolvidas, resolve-as e as insere no banco de dados,
def insere_resultado(conn):
    global stop

    while stop == 0:

        x = len(coeficientes)

        if x >= 3:

            a = coeficientes.pop(0)
            b = coeficientes.pop(0)
            c = coeficientes.pop(0)

            x1, x2 = solve_equation(a, b, c)
            x1 = str(x1)
            x2 = str(x2)

            if x1 == 'erro':
                if b > 0:
                    b2 = "+ " + str(b)
                else:
                    b2 = str(b)
                if c > 0:
                    c2 = "+ " + str(c)
                else:
                    c2 = str(c)

                equation = str(a) + "x^2 " + b2 + "x " + c2
                x1 = "Delta < 0"
                x2 = "Não há solução!"
                inserir_no_banco(equation, x1, x2, conn)

            elif x2 == 0:
                # Solução Única
                if b > 0:
                    b2 = "+ " + str(b)
                else:
                    b2 = str(b)
                if c > 0:
                    c2 = "+ " + str(c)
                else:
                    c2 = str(c)

                equation = str(a) + "x^2 " + b2 + "x " + c2
                inserir_no_banco(equation, x1, x2, conn)
            else:
                # 2 Raízes
                if b > 0:
                    b2 = "+ " + str(b)
                else:
                    b2 = str(b)
                if c > 0:
                    c2 = "+ " + str(c)
                else:
                    c2 = str(c)

                equation = str(a) + "x^2 " + b2 + "x " + c2
                inserir_no_banco(equation, x1, x2, conn)
    # end while.
    salva_dados(conn)


# Função principal do Programa.
if __name__ == '__main__':
    print("Bem vindo ao Solver de equações de 2 grau!\n")

    conn = sqlite3.connect('raizes.db', check_same_thread=False)

    cria_banco(conn)

    t1 = threads.Thread(target=coleta_dados, args=(conn,))
    t2 = threads.Thread(target=insere_resultado, args=(conn,))

    t1.start()
    t2.start()
