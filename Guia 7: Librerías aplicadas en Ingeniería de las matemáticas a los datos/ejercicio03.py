import numpy as np

def main_ej3():
    rssi = np.array([-68.2, -67.9, -67.5, -67.8, -68.0, -68.9,
                     -70.4, -72.8, -74.1, -75.6, -76.3, -75.9,
                     -74.8, -75.2, -76.8, -77.1, -75.4, -73.9,
                     -72.2, -70.8, -69.9, -69.1, -68.7, -68.4])
    
    # 1. Promedios
    promedio_directo = np.mean(rssi)
    rssi_mw = 10**(rssi/10)
    promedio_potencia_dbm = 10 * np.log10(np.mean(rssi_mw))
    
    # 2. Mínimos y máximos
    min_val = np.min(rssi)
    max_val = np.max(rssi)
    hora_min = np.argmin(rssi)
    hora_max = np.argmax(rssi)
    
    # 3. Por debajo de -75 dBm
    horas_bajo_75 = np.where(rssi < -75)[0]
    
    # 4. Zona de riesgo [-75, -72)
    zona_riesgo = np.where((rssi >= -75) & (rssi <= -72))[0]
    
    print(f"Promedio directo: {promedio_directo:.2f} dBm")
    print(f"Promedio en potencia: {promedio_potencia_dbm:.2f} dBm")
    print(f"Mejor señal (máximo): {max_val} dBm a las {hora_max} h")
    print(f"Peor señal (mínimo): {min_val} dBm a las {hora_min} h")
    print(f"Horas bajo -75 dBm ({len(horas_bajo_75)}): {horas_bajo_75}")
    print(f"Horas en riesgo ({len(zona_riesgo)}): {zona_riesgo}")

if __name__ == "__main__":
    main_ej3()