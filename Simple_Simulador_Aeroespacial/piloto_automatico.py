from __future__ import annotations
import numpy as np


class PilotoAutomatico:
    # Keyframes (tiempo en s, pitch en grados)
    key_times = np.array([0.0, 12.0, 70.0, 100.0, 120.0])
    key_pitch = np.array([90.0, 88.0, 80.0, 30.0, 30.0])

    @staticmethod
    def _S(x: float) -> float:
        """Polinomio mínimo jerk (S-curve)."""
        return 10*x**3 - 15*x**4 + 6*x**5

    @classmethod
    def pitch_en(cls, time: float) -> float:
        """
        Devuelve el ángulo de pitch (grados) en un instante temporal dado.

        Parámetros:
            time (float): tiempo en segundos desde el lanzamiento.

        Retorna:
            float: ángulo de pitch en grados.
        """
        t = float(time)

        # Saturación por fuera del rango
        if t <= cls.key_times[0]:
            return float(cls.key_pitch[0])
        if t >= cls.key_times[-1]:
            return float(cls.key_pitch[-1])

        # Interpolación suave S-curve en el tramo correspondiente
        for i in range(len(cls.key_times) - 1):
            t0, t1 = cls.key_times[i], cls.key_times[i+1]
            if t0 <= t <= t1:
                θ0, θ1 = cls.key_pitch[i], cls.key_pitch[i+1]
                x = (t - t0) / (t1 - t0)
                return float(θ0 + (θ1 - θ0) * cls._S(x))

        # Fallback (no debería alcanzarse)
        return float(cls.key_pitch[-1])

    def empuje_en(cls, time: float) -> float:
        if time < 80:
            return 85
        elif time < 110:
            return 90
        else:
            return 95

    # --- Compatibilidad con la firma antigua (altitud ignorada) ---
    @classmethod
    def perfil_pitch(cls, time: float, altitude: float = 0.0) -> float:
        """Compatibilidad retro: delega en pitch_at(time)."""
        return cls.pitch_en(time)
    
    def perfil_empuje(cls, time: float, altitude: float = 0.0) -> float:
        """Compatibilidad retro: delega en pitch_at(time)."""
        return cls.empuje_en(time)