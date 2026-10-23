import math

C = 299792458  # Velocidad de la luz en m/s

def ganancia_parabolica(diametro_m, frecuencia_hz, eficiencia=0.55):
    """Calcula la ganancia de una antena parabólica en dBi."""
    lam = C / frecuencia_hz
    return 10 * math.log10(eficiencia * (math.pi * diametro_m / lam)**2)

def main_ej2():
    diametros = [0.3, 0.6, 1.2]
    frecuencias = [5.8e9, 11e9]
    
    print(f"{'Diámetro [m]':<15} | {'5.8 GHz [dBi]':<15} | {'11 GHz [dBi]':<15}")
    print("-" * 50)
    for d in diametros:
        g_58 = ganancia_parabolica(d, frecuencias[0])
        g_11 = ganancia_parabolica(d, frecuencias[1])
        print(f"{d:<15.1f} | {g_58:<15.2f} | {g_11:<15.2f}")

if __name__ == "__main__":
    main_ej2()