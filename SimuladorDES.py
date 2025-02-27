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
RAM_CAPACITY = 100   
CPU_SPEED = 3   
CPU_COUNT = 1   
PROCESS_COUNT = [25, 50, 100, 150, 200]
ARRIVAL_INTERVAL = 10   
RANDOM_SEED = 10


random.seed(RANDOM_SEED)

# define process
def process(env, name, ram, cpu, total_instruction, times):
    requiredMemory = random.randint(1, 10)
    arrivalTime = env.now
    yield ram.get(requiredMemory)
    #queue of ready
    with cpu.request() as req:
        yield req
        while total_instruction > 0:
            yield env.timeout(1)
            executed = min(CPU_SPEED, total_instruction)
            total_instruction -= executed
            #time of the instruction - executed time
            if total_instruction > 0:
                decision = random.randint(1, 21)
                if decision == 1:
                    yield env.timeout(random.randint(1, 3))
                elif decision == 2:
                    with cpu.request() as req2:
                        yield req2 #return to ready
    #end process
    ram.put(requiredMemory)
    times.append(env.now - arrivalTime)
    

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