"""
Modulo: fuerzas_aerodinamicas.py
Descripción: Funciones que modelan fuerzas aerodinámicas en vuelo de un cohete
Autor: Álvar Ginés Legaz Aparicio

IMPORTANTE: LAS MAGNITUDES SIEMPRE EN SISTEMA INTERNACIÓNAL.
"""

import math

g0 = 9.80665 # gravedad estándar [m/s²]
Re = 6371e3 # radio terrestre [m]
rho0 = 1.225 # densidad a nivel del mar [kg/m³]
H = 7200.0 # escala atmósfera [m]
p0 = 101325.0 # presión al nivel del mar [Pa]


def empuje(empuje_vacio, empuje_nivel_mar, tiempo_quemado, procentaje_empuje, masa_propelente, altitud):
    empuje_nivel_mar_actual = (procentaje_empuje/100)*empuje_nivel_mar
    #Ae = (empuje_vacio - empuje_nivel_mar)/p0
    if masa_propelente > 0.0:
        return empuje_nivel_mar_actual
    else:
        return 0



def arrastre_x(altitud, vx, V, area_efectiva):
    return 0.5*rho(altitud)*(vx/V+0.000001)*Cd(altitud, vx)*area_efectiva

def arrastre_z(altitud, vz, V, area_efectiva):
    return 0.5*rho(altitud)*(vz/V +0.000001)*Cd(altitud, vz)*area_efectiva

def peso(altitud, masa):
    g_actual = g0 * (Re / (Re + altitud))**2
    return masa*g_actual


def Cd(altitud: float, velocidad: float) -> float:
    """
    Coeficiente de arrastre Cd en función de altitud y velocidad.
    Modelo simplificado dependiente de Mach.
    - Supone atmósfera ISA con velocidad del sonido ~340 m/s a nivel del mar,
      decreciendo con la altitud de forma muy simplificada.
    - Retorna Cd reducido a cero por encima de la línea de Kármán (100 km).
    """
    # Línea de Kármán: por encima se ignora la atmósfera
    if altitud >= 100e3:
        return 0.0

    # Modelo muy simplificado para velocidad del sonido con altitud
    # (lineal 340 m/s a nivel del mar → 300 m/s a 20 km, constante después)
    if altitud < 20e3:
        a = 340.0 - (40.0/20e3) * altitud
    else:
        a = 300.0
    if a <= 0:
        a = 300.0

    # Número de Mach
    M = abs(velocidad) / a

    # Modelo piecewise del Cd típico de un cuerpo romo/cohete delgado
    if M < 0.3:         # régimen incompresible
        Cd_val = 0.3
    elif M < 0.8:       # caída suave en transónico bajo
        Cd_val = 0.3 - 0.05*(M-0.3)/0.5
    elif M < 1.2:       # pico transónico
        Cd_val = 0.35
    elif M < 5.0:       # supersónico: caída progresiva
        Cd_val = 0.35 - 0.1*(M-1.2)/(5.0-1.2)
    else:               # hipersónico: Cd bajo ~0.2
        Cd_val = 0.2

    return Cd_val

def gravedad(altitud):
    return g0 * (Re / (Re + altitud))**2

# Estrés aerodinamico
def q(altitud, velocidad):
    return 0.5*rho(altitud)*(velocidad**2)
    

# Modelo presión
def pa(altitud, velocidad): # presión ambiente
    return p0 * math.exp(-altitud /H)


# Modelo densidad
def rho(altitud): 
    return rho0 * math.exp(-altitud/H)

