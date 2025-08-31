"""
Modulo: dinamica_vehiculo.py
Descripción: Dinámica traslacional 2D (plano x–z, z hacia arriba) de un cohete.
Unidades: SI

Autor: Álvar Ginés Legaz Aparicio
"""

import math
import fuerzas_aerodinamicas as fa  # requiere: g(h), empuje(...), arrastre(...)

class Vehiculo:

    def __init__(self, datos_vehiculo):
        self.empuje_vacio = float(datos_vehiculo["empuje_vacio"])
        self.empuje_nivel_mar= float(datos_vehiculo["empuje_nivel_mar"])
        self.tiempo_quemado = float(datos_vehiculo["tiempo_quemado"])
        self.area_efectiva = float(datos_vehiculo["Aref"])
        self.m_seco = float(datos_vehiculo["m_seco"])
        self.m_prop = float(datos_vehiculo["m_prop"])
        self.m_prop_max = float(datos_vehiculo["m_prop"]) 

    # ------------------------------------------------------------
    # Dinámica (fuerzas → aceleraciones)
    # Control del vehículo a trevés de pitch y procentaje_empuje
    # Posicion actual
    # ------------------------------------------------------------
    def actualizar_dinamica(self, pitch: float, porcentaje_empuje: float, estado: dict):
        # Control del vehículo con ángulo de trayectoria (≈ actitud) y porcentaje empuje
        thr =  max(0.0, float(porcentaje_empuje))

        # Estado actual
        t_actual = float(estado["t"])
        xx_actual = float(estado["distancia"])
        h_actual = ( float(estado["altitud"]))
        vz_actual = (float(estado["vz"]))
        vx_actual = (float(estado["vx"]))
        v_actual = math.sqrt(vx_actual**2 + vz_actual**2)
        dt_actual = float(estado["dt"])

        # Empuje (con corrección por presión ambiente implementada en fa.empuje)
        T = fa.empuje(self.empuje_vacio, self.empuje_nivel_mar, self.tiempo_quemado, thr, self.m_prop,h_actual)
        # Peso y masa
        m = max(self.masa_instantanea(dt_actual, porcentaje_empuje), 1e-9)  # evita división por cero
        W= fa.peso(h_actual, m)

        # Arrastre (con corrección por presión ambiente implementada en fa.empuje)
        if v_actual > 1e-9:
            Dx = fa.arrastre_x(h_actual, vx_actual, v_actual, self.area_efectiva)
            Dz = fa.arrastre_z(h_actual, vz_actual, v_actual, self.area_efectiva)
        else:
            Dx = 0.0
            Dz = 0.0

        # Ecuaciones de movimiento (traslación)
        ax = (T * math.cos(pitch) - Dx) / m
        az = (T * math.sin(pitch) - Dz - W) / m
        
        vx = vx_actual + ax * dt_actual
        vz = vz_actual + az * dt_actual
        xx = xx_actual + vx * dt_actual
        hh  = h_actual  + vz * dt_actual
        tt  = t_actual  + dt_actual
        v = math.sqrt(vx**2 + vz**2)
        angulo_elevacion_trayectoria = math.degrees(math.atan2(vx, vz))

        if(h_actual == 0 and hh < 0):
            hh = h_actual
        
        return {"tiempo":tt, "distancia":xx, "altitud":hh, "v":v, "vx":vx, "vz":vz, "angulo_elevacion_trayectoria":angulo_elevacion_trayectoria, "ax": ax, "az": az, "T": T, "Dz": Dz, "Dx": Dx, "W": W, "m": m}

    # ------------------------------------------------------------
    # Masa instantánea (consumo lineal medio)
    # ------------------------------------------------------------
    def masa_instantanea(self, dt: float, porcentaje_empuje) -> float:
        """
        veh: dict con claves:
            'm_seco' [kg], 'm_prop' [kg], 'tiempo_quemado' [s]
        """
       
        tburn   = self.tiempo_quemado
        mdot    = (porcentaje_empuje/100)*(self.m_prop_max / tburn) 
        self.m_prop  = max(self.m_prop - mdot * dt, 0.0)
        #print(f"Tiempo quemado at {tburn:.2f} dt = {dt:.2f}º")
        return self.m_seco + self.m_prop
    
    def get_porcentaje_combustible(self):
        #print(f"Porcentaje quemado {(self.m_prop/self.m_prop_max)*100:.2f}")
        return (self.m_prop/self.m_prop_max)*100
        