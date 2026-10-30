"""Módulo integrador para evaluación de KPIs y generación de reporte en formato Markdown."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Pesos de penalización constantes
P_ALARMA_PERSISTENTE = 2.0
P_ALARMA_SIMPLE = 0.5
P_PENDIENTE_MALA = 50.0
P_ALARMA_TEMP = 5.0
P_FALTANTE = 1.0
P_MARGEN_BAJO = 10.0


def promedio_potencia_dbm(serie):
    """Calcula el promedio de potencia (dBm)."""
    mw = 10 ** (serie.dropna() / 10)
    return 10 * np.log10(mw.mean()) if not mw.empty else -100.0


def analizar_estacion(grupo, total_reportes_semana=672):
    """Calcula todas las métricas requeridas para una única estación."""
    # Faltantes
    faltantes = total_reportes_semana - len(grupo)
    
    # Temperatura
    alarmas_temp = (grupo["temperatura"] > 60.0).sum()
    
    # RSSI y alarmas
    es_alarma = grupo["rssi"] < -75.0
    alarmas_simp = es_alarma.sum()
    alarmas_pers = (es_alarma.rolling(4).sum() == 4).sum()
    
    # Margen
    prom_rssi = promedio_potencia_dbm(grupo["rssi"])
    margen_bajo = 1 if (prom_rssi - (-75.0)) < 10.0 else 0
    
    # Pendiente
    grupo_cl = grupo.dropna(subset=["rssi"])
    pendiente_mala = 0
    if len(grupo_cl) > 2:
        x = (grupo_cl["timestamp"] - grupo_cl["timestamp"].min()).dt.total_seconds() / 86400.0
        p = np.polyfit(x, grupo_cl["rssi"], 1)[0]
        if p < -1.0:
            pendiente_mala = 1

    puntaje = (
        (alarmas_pers * P_ALARMA_PERSISTENTE) +
        (alarmas_simp * P_ALARMA_SIMPLE) +
        (pendiente_mala * P_PENDIENTE_MALA) +
        (alarmas_temp * P_ALARMA_TEMP) +
        (faltantes * P_FALTANTE) +
        (margen_bajo * P_MARGEN_BAJO)
    )

    return {
        "Puntaje": puntaje,
        "Faltantes": faltantes,
        "Temp_Alarmas": alarmas_temp,
        "RSSI_Simples": alarmas_simp,
        "RSSI_Persis": alarmas_pers,
        "Degradada": pendiente_mala,
        "Margen_Critico": margen_bajo
    }


def asignar_accion(fila):
    """Genera recomendación textual basándose en los indicadores."""
    acciones = []
    if fila["Degradada"] == 1:
        acciones.append("Verificar alineación de antena e infiltraciones de agua.")
    if fila["Temp_Alarmas"] > 0:
        acciones.append("Revisar ventilación, extractores térmicos y gabinete.")
    if fila["Faltantes"] > 0:
        acciones.append("Inspeccionar suministro eléctrico y conectividad de telemetría.")
    if fila["RSSI_Persis"] > 0 or fila["Margen_Critico"] == 1:
        acciones.append("Ajustar potencia de transmisión o limpiar trayecto de línea de vista.")
        
    return " ".join(acciones) if acciones else "Sin acciones urgentes."


def main():
    """Genera el informe final ponderado y exporta a Markdown y PNG."""
    df = pd.read_csv("telemetria.csv", parse_dates=["timestamp"])
    resultados = []

    for est, grp in df.groupby("estacion"):
        metricas = analizar_estacion(grp)
        metricas["Estacion"] = est
        resultados.append(metricas)

    df_puntos = pd.DataFrame(resultados).set_index("Estacion")
    
    # Asignar prioridad
    condiciones = [df_puntos["Puntaje"] >= 50, (df_puntos["Puntaje"] >= 10) & (df_puntos["Puntaje"] < 50)]
    df_puntos["Prioridad"] = np.select(condiciones, ["ALTA", "MEDIA"], default="BAJA")
    
    df_puntos["Diagnostico/Accion"] = df_puntos.apply(asignar_accion, axis=1)
    
    df_ordenado = df_puntos.sort_values(by="Puntaje", ascending=False)

    # Exportar Markdown
    with open("informe_mantenimiento.md", "w", encoding="utf-8") as file:
        file.write("# Informe de Mantenimiento Priorizado\n\n")
        
        relevantes = df_ordenado[df_ordenado["Prioridad"].isin(["ALTA", "MEDIA"])]
        
        file.write(relevantes[["Puntaje", "Prioridad"]].to_markdown())
        file.write("\n\n## Detalle de Acciones\n\n")
        
        for est, fila in relevantes.iterrows():
            file.write(f"**Estación {est}** (Prioridad {fila['Prioridad']})\n")
            file.write(f"- *Diagnóstico*: {fila['Diagnostico/Accion']}\n\n")
            
    print("Archivo 'informe_mantenimiento.md' generado con éxito.")

    # Gráfico de barras horizontales
    plt.figure(figsize=(8, 10))
    df_ordenado["Puntaje"].plot(kind="barh", color="steelblue")
    plt.gca().invert_yaxis()
    plt.title("Ranking de Prioridad de Mantenimiento (Puntaje Total)")
    plt.xlabel("Puntos Acumulados")
    plt.ylabel("Estación")
    plt.grid(True, axis="x")
    plt.tight_layout()
    plt.savefig("prioridad_mantenimiento.png", dpi=150)
    print("Gráfico 'prioridad_mantenimiento.png' guardado exitosamente.")


if __name__ == "__main__":
    main()