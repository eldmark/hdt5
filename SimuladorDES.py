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
RAM_CAPACITY = 100   # Capacidad total de RAM disponible
CPU_SPEED = 3        # Velocidad de procesamiento del CPU (instrucciones por unidad de tiempo)
CPU_COUNT = 1        # Número de CPUs disponibles
PROCESS_COUNT = [25, 50, 100, 150, 200]  # Lista de números de procesos para diferentes pruebas
ARRIVAL_INTERVAL = 10   # Intervalo de tiempo entre la llegada de procesos
RANDOM_SEED = 10    # Semilla para generar números aleatorios reproducibles

# Inicializar generador de números aleatorios
random.seed(RANDOM_SEED)

# Define el proceso
def process(env, name, ram, cpu, total_instruction, times):
    requiredMemory = random.randint(1, 10)  # Memoria requerida por el proceso
    arrivalTime = env.now  # Tiempo de llegada del proceso
    
    # Solicita memoria
    yield ram.get(requiredMemory)
    
    # Cola de ready
    with cpu.request() as req:
        yield req
        while total_instruction > 0:
            yield env.timeout(1)
            executed = min(CPU_SPEED, total_instruction)  # Instrucciones ejecutadas en esta unidad de tiempo
            total_instruction -= executed  # Actualiza las instrucciones restantes
            
            # Tiempo de la instrucción - tiempo ejecutado
            if total_instruction > 0:
                decision = random.randint(1, 21)  # Decisión aleatoria para simular eventos
                if decision == 1:
                    yield env.timeout(random.randint(1, 3))  # Simula operación de I/O
                elif decision == 2:
                    with cpu.request() as req2:
                        yield req2  # Regresa a la cola de ready
    
    # Terminar proceso
    ram.put(requiredMemory)  # Liberar RAM
    times.append(env.now - arrivalTime)  # Registrar el tiempo total del proceso

# Iniciar simulación
def correr_simulacion(num_procesos, intervalo, ram_capacity, cpu_speed, cpu_count):
    tiempos = []  # Lista para almacenar los tiempos de cada proceso
    env = simpy.Environment()  # Crear el entorno de simulación
    ram = simpy.Container(env, init=ram_capacity, capacity=ram_capacity)  # Contenedor de RAM
    cpu = simpy.Resource(env, capacity=cpu_count)  # Recurso de CPU

    for i in range(num_procesos):
        env.process(process(env, f"Proceso-{i}", ram, cpu, random.randint(1, 10), tiempos))  # Crear y añadir procesos
        env.timeout(random.expovariate(1.0 / intervalo))  # Intervalo de llegada de nuevos procesos
    
    env.run(until=env.now + 1000)  # Ejecutar simulación hasta el tiempo especificado
    promedio = statistics.mean(tiempos)  # Calcular el tiempo promedio
    desviacion = statistics.stdev(tiempos) if len(tiempos) > 1 else 0  # Calcular la desviación estándar
    return promedio, desviacion

# Ejecutar simulación para un caso específico
def ejecutar_prueba():
    proceso = PROCESS_COUNT[0]
    promedio, desviacion = correr_simulacion(proceso, ARRIVAL_INTERVAL, RAM_CAPACITY, CPU_SPEED, CPU_COUNT)
    print(f"Procesos: {proceso}, Intervalo: {ARRIVAL_INTERVAL}, RAM: {RAM_CAPACITY}, CPU Speed: {CPU_SPEED}, CPUs: {CPU_COUNT}")
    print(f"Tiempo promedio: {promedio:.2f}, Desviación estándar: {desviacion:.2f}")

# Llamar a la función para ejecutar la prueba
ejecutar_prueba()
