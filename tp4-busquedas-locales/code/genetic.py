import random
import numpy as np
from view_board import print_board

def init_board(n):
    return [random.randint(0, n - 1) for _ in range(n)]

def fitness(tablero):
    n = len(tablero)
    ataques = 0
    for i in range(n):
        for j in range(i + 1, n):
            if tablero[i] == tablero[j] or abs(tablero[i] - tablero[j]) == abs(i - j):
                ataques += 1
    return -ataques

def seleccion(poblacion, aptitudes):
    total_aptitud = sum(aptitudes)
    probabilidades = [a / total_aptitud for a in aptitudes]
    return poblacion[np.random.choice(len(poblacion), p=probabilidades)]

def cruzar(parent1, parent2):
    n = len(parent1)
    punto_cruce = random.randint(1, n - 1)
    child = parent1[:punto_cruce] + parent2[punto_cruce:]
    return child

def mutar(child, tasa_mutacion=0.1):
    n = len(child)
    for i in range(n):
        if random.random() < tasa_mutacion:
            child[i] = random.randint(0, n - 1)
    return child

def algoritmo_genetico(n, tamaño_poblacion=50, generaciones=1000):
    poblacion = [init_board(n) for _ in range(tamaño_poblacion)]
    for generacion in range(generaciones):
        fitnesses = [fitness(tablero) for tablero in poblacion]
        # Encuentra el mejor individuo actual
        mejor_tablero = max(poblacion, key=fitness)
        nueva_poblacion = [mejor_tablero[:]]  # Elitismo: copia el mejor
        # Genera el resto de la población
        for _ in range(tamaño_poblacion - 1):
            parent1 = seleccion(poblacion, fitnesses)
            parent2 = seleccion(poblacion, fitnesses)
            child = cruzar(parent1, parent2)
            child = mutar(child)
            nueva_poblacion.append(child)
        poblacion = nueva_poblacion
    # Devuelve el mejor de la última generación
    fitnesses = [fitness(tablero) for tablero in poblacion]
    mejor_tablero = max(poblacion, key=fitness)
    return mejor_tablero, -fitness(mejor_tablero)

if __name__ == "__main__":
    for n in [4, 8, 10]:
        solución, ataques = algoritmo_genetico(n)
        print(f"Número de ataques: {ataques}")
        print_board(solución)