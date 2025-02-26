import simpy
import random
import statistics

'''
Universidad del Valle de Guatemala
Algoritmos y Estructuras de Datos
Ing. Douglas Barrios
Autores: Marcelo Detlefsen, Marco Diaz, Diego Calderón
Creación: 26/02/2025
Última modificación: 26/02/2025
Nombre del Archivo: SimuladorDES.py
Descripción: Este archivo contiene la implementación de un simulador de un sistema de procesamiento de procesos
             utilizando el paradigma de simulación de eventos discretos (DES).
'''

# Parámetros de simulación
RAM_CAPACITY = 100  # Se puede cambiar según prueba
CPU_SPEED = 3  # Se puede cambiar según prueba
CPU_COUNT = 1  # Se puede cambiar según prueba
PROCESS_COUNT = [25, 50, 100, 150, 200]
ARRIVAL_INTERVAL = 10  # Se puede cambiar según prueba
RANDOM_SEED = 10

random.seed(RANDOM_SEED)

# Definir proceso
def proceso(env, nombre, ram, cpu, instruccion_total, tiempos):
    memoria_requerida = random.randint(1, 10)
    tiempo_llegada = env.now
    

# Iniciar simulación
def correr_simulacion(num_procesos, intervalo, ram_capacity, cpu_speed, cpu_count):
    tiempos = []
    env = simpy.Environment()
    ram = simpy.Container(env, init=ram_capacity, capacity=ram_capacity)
    cpu = simpy.Resource(env, capacity=cpu_count)

# Ejecutar simulación para un caso específico
def ejecutar_prueba():
    promedio, desviacion = correr_simulacion(PROCESS_COUNT[0], ARRIVAL_INTERVAL, RAM_CAPACITY, CPU_SPEED, CPU_COUNT)
    print(f"Procesos: {PROCESS_COUNT[0]}, Intervalo: {ARRIVAL_INTERVAL}, RAM: {RAM_CAPACITY}, CPU Speed: {CPU_SPEED}, CPUs: {CPU_COUNT}")
    print(f"Tiempo promedio: {promedio:.2f}, Desviación estándar: {desviacion:.2f}")

ejecutar_prueba()