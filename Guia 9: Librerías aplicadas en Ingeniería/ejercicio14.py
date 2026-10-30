"""Módulo para el filtrado de eventos transitorios y detección de fallas sostenidas."""

import pandas as pd


def main():
    """Identifica caídas de RSSI que perduran por 4 muestras o más (1 hora)."""
    df = pd.read_csv("telemetria.csv", parse_dates=["timestamp"])
    resultados = []

    for estacion, grupo in df.groupby("estacion"):
        grupo = grupo.sort_values("timestamp")
        es_alarma = grupo["rssi"] < -75.0
        
        # 1. Rolling sum para detectar 4 consecutivas
        alarmas_consecutivas = es_alarma.rolling(window=4).sum()
        persistente_mask = alarmas_consecutivas == 4.0
        
        # 2. Conteo total
        cantidad_persistentes = persistente_mask.sum()
        
        # 3. Fecha de la primera
        primera_fecha = None
        if cantidad_persistentes > 0:
            # Tomar el timestamp de la primera fila donde se cumplió la condición
            primera_fecha = grupo.loc[persistente_mask, "timestamp"].iloc[0]

        resultados.append({
            "estacion": estacion,
            "alarmas_simples": es_alarma.sum(),
            "alarmas_persistentes": cantidad_persistentes,
            "primera_ocurrencia": primera_fecha
        })

    df_alarmas = pd.DataFrame(resultados).set_index("estacion")
    
    print("--- Resumen de Alarmas Persistentes vs Simples ---")
    print(df_alarmas[df_alarmas["alarmas_simples"] > 0])

    print("\n--- Análisis Conceptual ---")
    print("El criterio rolling(4) ignora caídas breves (desvanecimientos temporales por un pájaro,")
    print("un reflejo rápido, o lluvia ligera). Esto evita saturar al operador con alertas inútiles")
    print("y enfoca el mantenimiento en los enlaces realmente rotos.")


if __name__ == "__main__":
    main()