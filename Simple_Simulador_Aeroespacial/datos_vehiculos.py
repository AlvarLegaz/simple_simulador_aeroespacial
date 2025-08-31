import math

VEHICULOS = {
    "falconito": {
        "m_seco": 1000.0,                 # kg
        "m_prop": 1600.0,                 # kg
        "Aref": math.pi * (0.4**2),       # m^2 (Ø=0.8 m)
        "empuje_vacio": 30_000.0,         # N
        "empuje_nivel_mar": 30_000.0,     # N
        "tiempo_quemado": 90.0            # s
    },
    "falcon9": {
        "m_seco": 100_200.0,               # kg (masa en seco primera etapa)
        "m_prop": 411_000.0,              # kg (propelente RP-1/LOX)
        "Aref": math.pi * (3.66/2)**2,    # m^2 (diámetro = 3.66 m)
        "empuje_vacio": 7_607_000.0,      # N (9 Merlin 1D en vacío)
        "empuje_nivel_mar": 7_607_000.0,  # N (aprox al nivel del mar)
        "tiempo_quemado": 162.0           # s (≈2 min 42 s)
    },
    "miura1": {
        "m_seco": 1000.0,
        "m_prop": 1600.0,
        "Aref": math.pi * (0.4**2),
        "empuje_vacio": 30_000.0,
        "empuje_nivel_mar": 30_000.0,
        "tiempo_quemado": 90.0
    },
    "sondaX": {
        "m_seco": 800.0,
        "m_prop": 1200.0,
        "Aref": math.pi * (0.3**2),
        "empuje_vacio": 20_000.0,
        "empuje_nivel_mar": 19_000.0,
        "tiempo_quemado": 70.0
    },
    "testV": {
        "m_seco": 800.0,
        "m_prop": 1200.0,
        "Aref": math.pi * (0.3**2),
        "empuje_vacio": 25_000.0,
        "empuje_nivel_mar": 25_000.0,
        "tiempo_quemado": 10.0
    }
}
