"""Módulo de simulación de degradación de enlace por atenuación hidrometeórica."""

import matplotlib.pyplot as plt
import numpy as np

K_LLUVIA = 0.12
ALPHA_LLUVIA = 1.02
DISTANCIA_KM = 4.0
MARGEN_DESPEJADO_DB = 25.0


def main():
    """Calcula el efecto de lluvias extremas en el margen de un enlace a 23 GHz."""
    intensidades = np.linspace(0.0, 150.0, 500)  # mm/h

    # 1. Atenuación específica y total
    gamma = K_LLUVIA * (intensidades ** ALPHA_LLUVIA)  # dB/km
    atenuacion_total = gamma * DISTANCIA_KM
    margen_restante = MARGEN_DESPEJADO_DB - atenuacion_total

    # 2. Intensidad máxima tolerable
    idx_falla = np.where(margen_restante <= 0.0)[0]
    r_max = intensidades[idx_falla[0]] if len(idx_falla) > 0 else 150.0

    print(f"Intensidad máxima de lluvia soportada: {r_max:.1f} mm/h")

    # 3. Gráfico
    plt.figure(figsize=(9, 5))
    plt.plot(intensidades, margen_restante, label="Margen de Enlace", color="blue", linewidth=2)
    plt.axhline(y=0.0, color="red", linestyle="--", label="Corte de Servicio (Margen = 0 dB)")
    plt.axvline(x=r_max, color="green", linestyle=":", label=f"Lluvia Máxima ({r_max:.1f} mm/h)")

    plt.title("Margen de Enlace vs. Intensidad de Lluvia (23 GHz, 4 km)")
    plt.xlabel("Intensidad de Lluvia [mm/h]")
    plt.ylabel("Margen Restante [dB]")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()