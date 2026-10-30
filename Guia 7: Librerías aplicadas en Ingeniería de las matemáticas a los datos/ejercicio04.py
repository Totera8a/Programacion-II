import numpy as np
import math

C = 299792458

def main_ej4():
    distancias_km = np.array([2.5, 8.0, 12.0, 3.0, 15.0, 20.0, 6.5, 28.0])
    frecuencias_ghz = np.array([5.8, 5.8, 5.8, 2.4, 2.4, 2.4, 5.8, 2.4])
    
    # Parámetros fijos
    p_tx = 23.0
    g_tx = 15.0
    g_rx = 15.0
    umbral = -75.0
    
    # 1. Cálculo de FSPL y P_rx
    # Pasar a metros y hertz
    d_m = distancias_km * 1000
    f_hz = frecuencias_ghz * 1e9
    
    fspl = 20 * np.log10(4 * np.pi * d_m * f_hz / C)
    p_rx = p_tx + g_tx + g_rx - fspl
    
    # 2. Margen
    margen = p_rx - umbral
    
    # 3. Estado (OK / FALLA)
    estado = np.where(margen >= 0, "OK", "FALLA")
    
    # 4. Mostrar resultados
    print(f"{'Enlace':<8} | {'P_rx [dBm]':<12} | {'Margen [dB]':<12} | {'Estado':<6}")
    print("-" * 46)
    for i in range(len(distancias_km)):
        print(f"E{i+1:<7} | {p_rx[i]:<12.2f} | {margen[i]:<12.2f} | {estado[i]:<6}")
    
    fallas = np.sum(estado == "FALLA")
    print(f"\nCantidad de enlaces que fallan: {fallas}")

if __name__ == "__main__":
    main_ej4()