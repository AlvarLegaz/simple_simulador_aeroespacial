"""
Modulo: dinamica_vehiculo.py
Descripción: Escenario donde se va a mover el vehículo
Unidades: SI

Autor: Álvar Ginés Legaz Aparicio
"""

import math
import fuerzas_aerodinamicas as fa
import vehiculo as dv
import matplotlib.pyplot as plt  # <-- para la gráfica
from datos_vehiculos import VEHICULOS

class Escenario:
    def __init__(self, nombre_vehiculo="falcon9"):
        self.veh = VEHICULOS[nombre_vehiculo]  # carga el diccionario del vehículo elegido

        # -------------------------------
        # Estado inicial
        # -------------------------------
        
        t0 = 0.0           # s
        h0 = 0           # m (altitud)
        x0 = 0           # m (distancia)
        Vx = 0.0           # m/s (reposo)
        Vz = 0.0           # m/s (reposo)

        self.t = t0
        self.hh = h0
        self.xx = x0
        self.vx = Vx
        self.vz = Vz
        
        self.vehiculo = dv.Vehiculo(self.veh)

        self.historia =[]

    def reset(self):
        # -------------------------------
        # Estado inicial
        # -------------------------------
        t0 = 0.0           # s
        h0 = 0           # m (altitud)
        x0 = 0           # m (distancia)
        Vx = 0.0           # m/s (reposo)
        Vz = 0.0           # m/s (reposo)

        self.t = t0
        self.hh = h0
        self.xx = x0
        self.vx = Vx
        self.vz = Vz

        self.vehiculo = dv.Vehiculo(self.veh)

        self.historia =[]
    
    def update(self, pitch, porcentaje_empuje, dt):

        estado = {"t": self.t, "dt":dt, "altitud": self.hh, "distancia":self.xx, "vz": self.vz, "vx": self.vx}
        h_actual = self.hh

        # Fuerzas/aceleraciones en estado actual
        out = self.vehiculo.actualizar_dinamica(pitch, porcentaje_empuje, estado)
        self.t = out["tiempo"]
        self.hh = out["altitud"]
        self.xx = out["distancia"]
        self.vx = out["vx"]
        self.vz = out["vz"]
        v = out["v"]
        angulo_elevacion_trayectoria = out["angulo_elevacion_trayectoria"]
        ax = out["ax"]
        az = out["az"]
        T  = out["T"]
        Dx  = out["Dx"]
        Dz  = out["Dz"]
        W = out["W"]
        m = out["m"]

        # Nivel combustible
        fuel_var = self.vehiculo.get_porcentaje_combustible()

        # -----------------------------
        # Eventos dentro del paso
        # -----------------------------
        # 1) Posado en el suelo sin empuje
        if h_actual > 0.0 and self.hh <= 0.0:
            V  = math.hypot(self.vx, self.vz)
            qi = fa.q(self.hh, V)
            print(f"Impacto con el suelo en t={self.t:.2f} s")
            raise RuntimeError(f"Impacto con el suelo en t={self.t:.2f} s, V={V:.2f} m/s, q={qi:.2f} Pa")

        self.historia.append({"tiempo":self.t, "altitud":self.hh, "distancia":self.xx, "v":v, "vx":self.vx, "vz":self.vz, "angulo_elevacion_trayectoria":angulo_elevacion_trayectoria, "ax": ax, "az": az, "T": T, "Dz": Dz, "Dx": Dx, "W": W, "m": m, "pitch":pitch, "nivel_combustible":fuel_var})
        
        return {"tiempo":self.t, "altitud":self.hh, "distancia":self.xx, "v":v, "vx":self.vx, "vz":self.vz, "angulo_elevacion_trayectoria":angulo_elevacion_trayectoria, "ax": ax, "az": az, "T": T, "Dz": Dz, "Dx": Dx, "W": W, "m": m, "pitch":pitch, "nivel_combustible":fuel_var}
    
    def obtener_datos_vuelo(self):
        return self.historia


