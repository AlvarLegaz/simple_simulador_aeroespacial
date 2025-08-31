# trayectoria.py
# Integración iterativa de la trayectoria 2D (plano x–z, z hacia arriba) de un cohete.
# Unidades: SI

import math
import fuerzas_aerodinamicas as fa
import vehiculo as dv
import matplotlib.pyplot as plt  # <-- para la gráfica

# -------------------------------
# Configuración del vehículo
# -------------------------------
veh = {
    "m_seco": 1000.0,                 # kg
    "m_prop": 1600.0,                # kg
    "Aref": math.pi * (0.4**2),     # m^2 (Ø=10 m)
    "empuje_vacio": 30_000.0,       # N
    "empuje_nivel_mar": 30_000.0,   # N
    "tiempo_quemado": 90.0          # s
}

vehiculo = dv.Vehiculo(veh)

# -------------------------------
# Estado inicial
# -------------------------------
t0 = 0.0           # s
h0 = 0           # m (altitud)
V0 = 0.0           # m/s (reposo)
gamma0_deg = 80.0  # deg (vertical)
gamma0 = math.radians(gamma0_deg)

# Componentes iniciales de velocidad
Vx = V0 * math.cos(gamma0)
Vz = V0 * math.sin(gamma0)

# Posición horizontal inicial
x = 0.0  # m

# -------------------------------
# Leyes de guiado (puedes editarlas)
# -------------------------------
def ley_pitch(t, h):
    if t < 2.0:
        deg = 90.0
    elif t < 60.0:
        deg = 80
    else:
        deg = 75.0
    return math.radians(deg)

def ley_throttle(t, h):
    return 1.0



# -------------------------------
# Integrador: paso a paso (Euler explícito)
# -------------------------------
def simular(dt=0.01, t_max=60.0):
    """
    Devuelve la lista 'historia' con los estados temporales.
    Bucle: while (t <= t_max) or (h > 0.0)
    """
    t = t0
    h = h0
    vx = Vx
    vz = Vz
    xx = x

    historia = []

    # --- Bucle principal ---
    while (t <= t_max) or (h > 0.0):
        # Estado actual
        V = math.hypot(vx, vz)
        gamma = math.atan2(vz, vx) if V < 1e-12 else ley_pitch(t, h)
        estado = {"t": t, "altitud": h, "Vz": vx, "Vx": vz}
        pitch = gamma
        throttle = ley_throttle(t, h)

        # Fuerzas/aceleraciones en estado actual
        out = vehiculo.dinamica_vehiculo(pitch, throttle, estado)
        ax = out["ax"]
        az = out["az"]
        T  = out["T"]
        Dx  = out["Dx"]
        Dz  = out["Dz"]
        m = out["m"]

        # --- Registro del estado ACTUAL (antes del paso) ---
        historia.append({
            "t": t, "x": xx, "h": h, "V": V,
            "vx": vx, "vz": vz, "az": az, "pitch": pitch, "gamma": gamma,
            "T": T, "Dz": Dz, "Dx": Dx, "m": m
        })

        # Predicción (semi-implícito en posición para algo más de estabilidad)
        vx_next = vx + ax * dt
        vz_next = vz + az * dt
        xx_next = xx + vx_next * dt
        h_next  = h  + vz_next * dt
        t_next  = t  + dt

        # -----------------------------
        # Eventos dentro del paso
        # -----------------------------

        # 1) Impacto con suelo: cruza h=0 del lado positivo
        if h > 0.0 and h_next <= 0.0:
            V  = math.hypot(vx, vz)
            qi = fa.q(h, V)

            # Sustituye el último registro por el de contacto exacto
            historia[-1] = {
                "t": t, "x": xx, "h": h, "V": V,
                "vx": vx, "vz": vz, "az": az, "ax": ax, "pitch": pitch, "gamma": gamma,
                "T": T, "Dz": Dz, "Dx": Dx, "m": m
            }
            print(f"Impacto con el suelo en t={t:.2f} s")
            break
        else:
            vx = vx_next
            vz = vz_next
            xx = xx_next
            h = h_next
            t = t_next 

    # Resumen consola
    if historia:
        final = historia[-1]
        print(f"Simulación terminada en t={final['t']:.2f} s, h={final['h']:.1f} m, x={final['x']:.1f} m, V={final['V']:.1f} m/s")
        

    return historia

# -------------------------------
# Gráfica h(t)
# -------------------------------


def graficar_altitud(historia):
    t = [r["t"] for r in historia]
    h = [r["h"] for r in historia]

    plt.figure()
    plt.plot(t, h)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Altitud h [m]")
    plt.title("Altitud vs. tiempo")
    plt.grid(True)
    plt.show()

def graficar_velocidad(historia):
    t = [r["t"] for r in historia]
    V = [r["V"] for r in historia]

    plt.figure()
    plt.plot(t, V)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Velocidad V [m/s]")
    plt.title("Velocidad vs. tiempo")
    plt.grid(True)
    plt.show()

def graficar_trayectoria(historia):
    t = [r["t"] for r in historia]
    T = [r["T"] for r in historia]
    pitch = [math.degrees(r["pitch"]) for r in historia] 
    h = [r["h"] for r in historia]
    vz = [r["vz"] for r in historia]
    vx = [r["vx"] for r in historia]
    x = [r["x"] for r in historia]
    vz_kmh = [v * 3.6 for v in vz]
    vx_kmh = [v * 3.6 for v in vx]

    fig, axs = plt.subplots(3, 2, figsize=(12, 12))

    # --- Fila 1 ---
    axs[0, 0].plot(t, T, color="black")
    axs[0, 0].set_title("Empuje vs. tiempo")
    axs[0, 0].set_ylabel("Empuje [N]")
    axs[0, 0].set_xlabel("Tiempo [s]")
    axs[0, 0].grid(True)

    axs[0, 1].plot(t, pitch, color="brown")
    axs[0, 1].set_title("Pitch vs. tiempo")
    axs[0, 1].set_ylabel("Pitch [rad]")
    axs[0, 1].set_xlabel("Tiempo [s]")
    axs[0, 1].grid(True)

    # --- Fila 2 ---
    axs[1, 0].plot(t, h, color="green")
    axs[1, 0].set_title("Altitud vs. tiempo")
    axs[1, 0].set_ylabel("h [m]")
    axs[1, 0].set_xlabel("Tiempo [s]")
    axs[1, 0].grid(True)

    axs[1, 1].plot(t, x, label="X (horizontal)", color="orange")
    axs[1, 1].set_title("Distancia en x")
    axs[1, 1].set_ylabel("x [m]")
    axs[1, 1].set_xlabel("Tiempo [s]")
    axs[1, 1].legend()
    axs[1, 1].grid(True)

    # --- Fila 3 ---
    axs[2, 0].plot(t, vz_kmh, label="Vz (vertical)", color="blue")
    axs[2, 0].set_title("Velocidad vertical")
    axs[2, 0].set_ylabel("Vz [km/h]")
    axs[2, 0].set_xlabel("Tiempo [s]")
    axs[2, 0].legend()
    axs[2, 0].grid(True)

    axs[2, 1].plot(t, vx_kmh, label="Vx (horizontal)", color="red")
    axs[2, 1].set_title("Velocidad horizontal")
    axs[2, 1].set_ylabel("Vx [km/h]")
    axs[2, 1].set_xlabel("Tiempo [s]")
    axs[2, 1].legend()
    axs[2, 1].grid(True)


    plt.tight_layout()
    plt.show()

def graficar_velocidad_z(historia):
    t = [r["t"] for r in historia]
    vz = [r["vz"] for r in historia]

    plt.figure()
    plt.plot(t, vz, label="Vz (vertical)")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Velocidad [m/s]")
    plt.title("Velocidad en z vs. tiempo")
    plt.legend()
    plt.grid(True)
    plt.show()

def graficar_velocidad_x(historia):
    t = [r["t"] for r in historia]
    vx = [r["vx"] for r in historia]

    plt.figure()
    plt.plot(t, vx, label="Vx (horizontal)")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Velocidad [m/s]")
    plt.title("Velocidad en x vs. tiempo")
    plt.legend()
    plt.grid(True)
    plt.show()

def graficar_aceleracion_z(historia):
    t = [r["t"] for r in historia]
    az = [r["az"] for r in historia]

    plt.figure()
    plt.plot(t, az, label="Az (vertical)")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Aceleracion [m/s^2]")
    plt.title("Aceleracion en z vs. tiempo")
    plt.legend()
    plt.grid(True)
    plt.show()    

def graficar_aceleracion_x(historia):
    t = [r["t"] for r in historia]
    ax = [r["x"] for r in historia]

    plt.figure()
    plt.plot(t, ax, label="Ax (horizontal)")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Aceleracion [m/s^2]")
    plt.title("Aceleracion en x vs. tiempo")
    plt.legend()
    plt.grid(True)
    plt.show()   
    
def graficar_empuje(historia):
    t = [r["t"] for r in historia]
    T = [r["T"] for r in historia]

    plt.figure()
    plt.plot(t, T)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Empuje T [N]")
    plt.title("Empuje vs. tiempo")
    plt.grid(True)
    plt.show()

def graficar_arrastre_x(historia):
    t = [r["t"] for r in historia]
    D = [r["Dx"] for r in historia]

    plt.figure()
    plt.plot(t, D)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Arrastre D en X [N]")
    plt.title("Arrastre vs. tiempo")
    plt.grid(True)
    plt.show()

def graficar_pitch(historia):
    t = [r["t"] for r in historia]
    pitch = [r["pitch"] for r in historia]
    pitch_deg = [r["pitch"]*180/math.pi for r in historia]

    plt.figure()
    plt.plot(t, pitch_deg)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Pitch [grados]")
    plt.title("Pitch vs. tiempo")
    plt.grid(True)
    plt.show()

def graficar_masa(historia):
    t = [r["t"] for r in historia]
    m = [r["m"] for r in historia]

    plt.figure()
    plt.plot(t, m)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Masa vehiculo [kg]")
    plt.title("Masa vehiculo vs. tiempo")
    plt.grid(True)
    plt.show()

# -------------------------------
# Ejecución directa
# -------------------------------
if __name__ == "__main__":
    dt = 0.1
    tmax = 600.0

    hist = simular(dt=dt, t_max=tmax)
    graficar_trayectoria(hist)
    graficar_velocidad(hist)

    

