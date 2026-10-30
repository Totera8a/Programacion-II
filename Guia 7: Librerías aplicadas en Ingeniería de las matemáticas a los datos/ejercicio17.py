"""Módulo de simulación de balance energético de batería con límites físicos."""

import matplotlib.pyplot as plt
import numpy as np

CAPACIDAD_BATERIA_WH = 1200.0


def simular_bateria(balance_wh, carga_inicial_wh):
    """Simula la carga paso a paso aplicando saturación al 100%.

    Parámetros:
    balance_wh -- Vector NumPy con el balance energético horario en Wh.
    carga_inicial_wh -- Carga inicial en Wh.

    Retorna:
    Vector NumPy con el nivel de carga real hora a hora.
    """
    carga = np.zeros_like(balance_wh, dtype=float)
    actual = carga_inicial_wh

    for i in range(len(balance_wh)):
        actual += balance_wh[i]
        actual = min(actual, CAPACIDAD_BATERIA_WH)
        carga[i] = actual

    return carga


def main():
    """Compara simulación ideal (cumsum) contra simulación acotada por bucle."""
    balance_wh = np.array([
        -45, -45, -45, -45, -45, -45, -20, 30, 90, 150, 190, 210,
        220, 210, 180, 130, 70, 10, -30, -45, -45, -45, -45, -45
    ])

    carga_inicial = 0.40 * CAPACIDAD_BATERIA_WH

    # 1. Carga ideal con cumsum
    carga_ideal = carga_inicial + np.cumsum(balance_wh)
    print(f"Carga ideal máxima alcanzada: {np.max(carga_ideal):.1f} Wh")
    print("Explicación: La suma acumulada simple no respeta el límite físico de almacenamiento del 100%.")

    # 2. Carga real mediante función acotada
    carga_real = simular_bateria(balance_wh, carga_inicial)

    # 3. Análisis
    hora_min = np.argmin(carga_real)
    min_pct = (carga_real[hora_min] / CAPACIDAD_BATERIA_WH) * 100.0
    horas_llena = np.where(carga_real == CAPACIDAD_BATERIA_WH)[0]

    print(f"\nMínimo de batería: {min_pct:.1f}% a las {hora_min}:00 h")
    print(f"¿Baja del 20% en algún momento?: {min_pct < 20.0}")
    print(f"Hora a la que se llena por primera vez: {horas_llena[0]}:00 h")

    # 4. Gráfico
    horas = np.arange(24)
    plt.figure(figsize=(10, 5))
    plt.plot(horas, (carga_ideal / CAPACIDAD_BATERIA_WH) * 100, label="Carga Ideal (np.cumsum)", linestyle="--", color="gray")
    plt.plot(horas, (carga_real / CAPACIDAD_BATERIA_WH) * 100, label="Carga Real (Simulada)", color="green", linewidth=2)
    plt.axhline(y=100.0, color="red", linestyle="--", label="Límite 100%")
    plt.axhline(y=20.0, color="orange", linestyle="--", label="Seguridad 20%")

    plt.title("Evolución Horaria de Batería de Estación Solar")
    plt.xlabel("Hora del día")
    plt.ylabel("Estado de Carga [%]")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()