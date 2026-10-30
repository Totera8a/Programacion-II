"""Módulo integrador para evaluación y diagnóstico completo de enlaces punto a punto."""

import math
import matplotlib.pyplot as plt
import numpy as np

# Datos de entrada fijos
DISTANCIA_KM = 18.0
FRECUENCIA_GHZ = 5.8
P_TX_DBM = 23.0
DIAMETRO_ANTENAS_M = 0.6
ALTURA_TORRES_M = 35.0
UMBRAL_DBM = -75.0
ANCHO_BANDA_HZ = 40e6
FIGURA_RUIDO_DB = 6.0

VELOCIDAD_LUZ = 299792458
K_BOLTZMANN = 1.380649e-23
TEMPERATURA_K = 290.0


def calcular_antena(diametro_m, frecuencia_hz):
    """Calcula longitud de onda y ganancia parabólica.

    Retorna:
    Tupla (longitud_onda_m, ganancia_dbi).
    """
    longitud_onda = VELOCIDAD_LUZ / frecuencia_hz
    ganancia = 10 * math.log10(0.55 * ((math.pi * diametro_m) / longitud_onda) ** 2)
    return longitud_onda, ganancia


def evaluar_enlace(distancia_km, altura_torres_m, frecuencia_ghz, p_tx_dbm, diametro_m, umbral_dbm, bw_hz, nf_db):
    """Realiza todos los cálculos técnicos del informe de ingeniería."""
    frecuencia_hz = frecuencia_ghz * 1e9
    longitud_onda, ganancia_dbi = calcular_antena(diametro_m, frecuencia_hz)

    # 2. Horizonte de radio
    horizonte_max_km = 4.12 * (math.sqrt(altura_torres_m) + math.sqrt(altura_torres_m))

    # 3. Zona de Fresnel en punto medio
    r_fresnel_m = 17.32 * math.sqrt(((distancia_km / 2) ** 2) / (frecuencia_ghz * distancia_km))

    # 4. FSPL, Potencia Recibida y Margen
    distancia_m = distancia_km * 1000.0
    fspl = 20 * math.log10((4 * math.pi * distancia_m * frecuencia_hz) / VELOCIDAD_LUZ)
    p_rx_dbm = p_tx_dbm + (2 * ganancia_dbi) - fspl
    margen_db = p_rx_dbm - umbral_dbm

    # 5. SNR y Capacidad de Shannon
    piso_ruido_dbm = 10 * math.log10(K_BOLTZMANN * TEMPERATURA_K * bw_hz * 1000.0) + nf_db
    snr_db = p_rx_dbm - piso_ruido_dbm
    snr_lineal = 10 ** (snr_db / 10)
    capacidad_bps = bw_hz * math.log2(1 + snr_lineal)

    # 6. Veredicto
    fallas = []
    if distancia_km > horizonte_max_km:
        fallas.append("Distancia supera el horizonte de radio (sin línea de vista).")
    if margen_db < 0:
        fallas.append("Potencia recibida por debajo del umbral de recepción.")

    estado = "VIABLE" if len(fallas) == 0 else "NO VIABLE"

    return {
        "ganancia_dbi": ganancia_dbi,
        "horizonte_km": horizonte_max_km,
        "fresnel_m": r_fresnel_m,
        "fspl_db": fspl,
        "p_rx_dbm": p_rx_dbm,
        "margen_db": margen_db,
        "piso_ruido_dbm": piso_ruido_dbm,
        "snr_db": snr_db,
        "capacidad_mbps": capacidad_bps / 1e6,
        "veredicto": estado,
        "fallas": fallas,
    }


def graficar_enlace(distancia_evaluar_km, p_rx_actual_dbm, ganancia_dbi):
    """Grafica la potencia recibida en función de la distancia de 1 a 60 km."""
    distancias_km = np.linspace(1.0, 60.0, 500)
    distancias_m = distancias_km * 1000.0
    frecuencia_hz = FRECUENCIA_GHZ * 1e9

    fspl_vec = 20 * np.log10((4 * np.pi * distancias_m * frecuencia_hz) / VELOCIDAD_LUZ)
    p_rx_vec = P_TX_DBM + (2 * ganancia_dbi) - fspl_vec

    plt.figure(figsize=(10, 5))
    plt.plot(distancias_km, p_rx_vec, label="Potencia Recibida", color="blue", linewidth=2)
    plt.axhline(y=UMBRAL_DBM, color="red", linestyle="--", label="Umbral (-75 dBm)")
    plt.axvline(x=distancia_evaluar_km, color="green", linestyle=":", label=f"Distancia Enlace ({distancia_evaluar_km} km)")

    plt.title(f"Planificador Punto a Punto ({FRECUENCIA_GHZ} GHz)")
    plt.xlabel("Distancia [km]")
    plt.ylabel("Potencia Recibida [dBm]")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    """Ejecuta el informe integrador para la configuración principal y la alternativa."""
    print("==========================================================")
    print("     INFORME TÉCNICO: PLANIFICADOR DE ENLACE MICROONDAS   ")
    print("==========================================================")

    res = evaluar_enlace(
        DISTANCIA_KM, ALTURA_TORRES_M, FRECUENCIA_GHZ,
        P_TX_DBM, DIAMETRO_ANTENAS_M, UMBRAL_DBM,
        ANCHO_BANDA_HZ, FIGURA_RUIDO_DB
    )

    print(f"Ganancia de Antenas:       {res['ganancia_dbi']:.2f} dBi")
    print(f"Horizonte de Radio:         {res['horizonte_km']:.2f} km")
    print(f"Radio Zona Fresnel (50%):   {res['fresnel_m']:.2f} m")
    print(f"Pérdida Espacio Libre:      {res['fspl_db']:.2f} dB")
    print(f"Potencia Recibida:          {res['p_rx_dbm']:.2f} dBm")
    print(f"Margen de Enlace:           {res['margen_db']:.2f} dB")
    print(f"Piso de Ruido Receptor:     {res['piso_ruido_dbm']:.2f} dBm")
    print(f"Relación Signal/Noise SNR:  {res['snr_db']:.2f} dB")
    print(f"Capacidad Canal Shannon:    {res['capacidad_mbps']:.2f} Mbit/s")
    print(f"\nVEREDICTO FINAL:           >>> {res['veredicto']} <<<")

    if res["fallas"]:
        for f in res["fallas"]:
            print(f" - Motivo: {f}")

    graficar_enlace(DISTANCIA_KM, res["p_rx_dbm"], res["ganancia_dbi"])

    # Prueba alternativa
    print("\n==========================================================")
    print(" PRUEBA ALTERNATIVA: Distancia = 45 km | Torres = 20 m")
    print("==========================================================")
    res_alt = evaluar_enlace(
        45.0, 20.0, FRECUENCIA_GHZ,
        P_TX_DBM, DIAMETRO_ANTENAS_M, UMBRAL_DBM,
        ANCHO_BANDA_HZ, FIGURA_RUIDO_DB
    )
    print(f"VEREDICTO ALTERNATIVO:     >>> {res_alt['veredicto']} <<<")
    for f in res_alt["fallas"]:
        print(f" - Motivo: {f}")


if __name__ == "__main__":
    main()