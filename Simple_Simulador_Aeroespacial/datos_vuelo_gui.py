import math
import matplotlib.pyplot as plt  # <-- para la gráfica

def mostrar_datos_trayectoria(historia):
    t = [r["tiempo"] for r in historia]
    T = [r["T"] for r in historia]
    pitch = [r["pitch"] for r in historia] 
    h = [r["altitud"] for r in historia]
    vz = [r["vz"] for r in historia]
    vx = [r["vx"] for r in historia]
    x = [r["distancia"] for r in historia]
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
    axs[0, 1].set_ylabel("Pitch [º]")
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
    plt.show(block=False)

