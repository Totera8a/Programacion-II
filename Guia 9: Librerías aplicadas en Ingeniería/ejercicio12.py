"""Módulo para la detección sistemática de caídas de telemetría (silencios)."""

import pandas as pd


def detectar_huecos(df, intervalo_min):
    """Detecta interrupciones de comunicación en registros temporales.

    Parámetros:
    df -- DataFrame con los registros de telemetría.
    intervalo_min -- Intervalo esperado entre reportes en minutos.

    Retorna:
    DataFrame con el detalle de los huecos encontrados.
    """
    registros_huecos = []

    for estacion, grupo in df.groupby("estacion"):
        grupo_ordenado = grupo.sort_values("timestamp").reset_index(drop=True)
        diferencias = grupo_ordenado["timestamp"].diff()
        
        # Filtrar diferencias mayores al intervalo esperado
        idx_huecos = diferencias[diferencias > pd.Timedelta(minutes=intervalo_min)].index
        
        for idx in idx_huecos:
            siguiente = grupo_ordenado.loc[idx, "timestamp"]
            anterior = grupo_ordenado.loc[idx - 1, "timestamp"]
            duracion_min = (siguiente - anterior).total_seconds() / 60.0
            
            # Cantidad de reportes que debieron llegar en ese lapso
            reportes_faltantes = int(duracion_min / intervalo_min) - 1
            
            registros_huecos.append({
                "estacion": estacion,
                "ultimo_reporte": anterior,
                "siguiente_reporte": siguiente,
                "duracion": duracion_min,
                "reportes_faltantes": reportes_faltantes
            })

    return pd.DataFrame(registros_huecos)


def main():
    """Ejecuta el detector de huecos sobre el conjunto de telemetría."""
    df = pd.read_csv("telemetria.csv", parse_dates=["timestamp"])

    # Prueba simulando huecos artificiales para validar detección generalizada
    df_prueba = df.copy()
    # Eliminar E05 el 6/10 entre 08:00 y 09:45
    mask_e05 = (df_prueba["estacion"] == "E05") & (df_prueba["timestamp"] >= "2026-10-06 08:00:00") & (df_prueba["timestamp"] <= "2026-10-06 09:45:00")
    # Eliminar E09 el 10/10 entre 20:00 y 20:30
    mask_e09 = (df_prueba["estacion"] == "E09") & (df_prueba["timestamp"] >= "2026-10-10 20:00:00") & (df_prueba["timestamp"] <= "2026-10-10 20:30:00")
    
    df_prueba = df_prueba[~mask_e05 & ~mask_e09]

    huecos = detectar_huecos(df_prueba, intervalo_min=15)
    print("--- Huecos de Comunicación Detectados ---")
    print(huecos)


if __name__ == "__main__":
    main()