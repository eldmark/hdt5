import simpy
import random
import statistics

# Parámetros de simulación
RAM_CAPACITY = 100  # Se puede cambiar según prueba
CPU_SPEED = 3  # Se puede cambiar según prueba
CPU_COUNT = 1  # Se puede cambiar según prueba
PROCESS_COUNT = [25, 50, 100, 150, 200]
ARRIVAL_INTERVAL = 10  # Se puede cambiar según prueba
RANDOM_SEED = 10

random.seed(RANDOM_SEED)

def proceso(env, nombre, ram, cpu, instruccion_total, tiempos):
    memoria_requerida = random.randint(1, 10)
    tiempo_llegada = env.now
    yield ram.get(memoria_requerida)
    while instruccion_total > 0:
        with cpu.request() as req:
            yield req
            yield env.timeout(1)
            ejecutadas = min(CPU_SPEED, instruccion_total)
            instruccion_total -= ejecutadas
            if instruccion_total > 0:
                decision = random.randint(1, 2)
                if decision == 1:
                    yield env.timeout(random.randint(1, 3))
    ram.put(memoria_requerida)
    tiempos.append(env.now - tiempo_llegada)

def correr_simulacion(num_procesos, intervalo, ram_capacity, cpu_speed, cpu_count):
    tiempos = []
    env = simpy.Environment()
    ram = simpy.Container(env, init=ram_capacity, capacity=ram_capacity)
    cpu = simpy.Resource(env, capacity=cpu_count)
    
    def generar_procesos(env):
        for i in range(num_procesos):
            env.process(proceso(env, f"Proceso-{i}", ram, cpu, random.randint(1, 10), tiempos))
            yield env.timeout(random.expovariate(1.0 / intervalo))
    
    env.process(generar_procesos(env))
    env.run(until=10000)
    
    if tiempos:
        promedio = statistics.mean(tiempos)
        desviacion = statistics.stdev(tiempos) if len(tiempos) > 1 else 0
    else:
        promedio, desviacion = 0, 0
    
    return promedio, desviacion

# Ejecutar simulación para un caso específico
def ejecutar_prueba():
    proceso = PROCESS_COUNT[0]
    promedio, desviacion = correr_simulacion(proceso, ARRIVAL_INTERVAL, RAM_CAPACITY, CPU_SPEED, CPU_COUNT)
    print(f"Procesos: {proceso}, Intervalo: {ARRIVAL_INTERVAL}, RAM: {RAM_CAPACITY}, CPU Speed: {CPU_SPEED}, CPUs: {CPU_COUNT}\nTiempo promedio: {promedio:.2f}, Desviación estándar: {desviacion:.2f}")

# Llamar a la función para ejecutar la prueba
ejecutar_prueba()