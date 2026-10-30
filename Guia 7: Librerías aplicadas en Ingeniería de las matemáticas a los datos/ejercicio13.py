"""Módulo de cálculo de disponibilidad y evaluación de SLA en enlaces de radio."""

import numpy as np


def main():
    """Evalúa la disponibilidad anual simulada de un enlace de telecomunicaciones."""
    rng = np.random.default_rng(13)
    mediciones_anuales = rng.normal(-68.0, 3.5, 8760)

    # 1. Disponibilidad con umbral -75 dBm
    horas_ok = np.sum(mediciones_anuales >= -75.0)
    disponibilidad = (horas_ok / 8760.0) * 100.0

    # 2. Horas fuera de servicio
    horas_down = 8760 - horas_ok

    # 3. Percentil 99% de disponibilidad (Percentil 1 de la distribución)
    rssi_99 = np.percentile(mediciones_anuales, 1.0)

    # Umbral requerido para SLA del 99.9% (Percentil 0.1)
    umbral_req_999 = np.percentile(mediciones_anuales, 0.1)

    print(f"Disponibilidad obtenida: {disponibilidad:.2f}%")
    print(f"Horas fuera de servicio al año: {horas_down} hs")
    print(f"RSSI superado el 99% del tiempo: {rssi_99:.2f} dBm")
    print(f"Umbral requerido para cumplir 99.9% SLA: {umbral_req_999:.2f} dBm")


if __name__ == "__main__":
    main()