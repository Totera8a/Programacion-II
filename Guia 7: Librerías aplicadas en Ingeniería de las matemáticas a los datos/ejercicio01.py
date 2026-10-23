import math

def w_a_dbm(p_w):
    """Convierte potencia de Watts a dBm."""
    return 10 * math.log10(p_w * 1000)

def dbm_a_w(p_dbm):
    """Convierte potencia de dBm a Watts."""
    return (10 ** (p_dbm / 10)) / 1000

def dbm_a_dbw(p_dbm):
    """Convierte potencia de dBm a dBW."""
    return p_dbm - 30

def main_ej1():
    equipos = {
        "Punto de acceso WiFi": 0.1,
        "Teléfono celular": 2,
        "Estación base celular": 40,
        "Emisora de FM": 10000
    }
    
    print(f"{'Equipo':<25} | {'W':<8} | {'dBm':<8} | {'dBW':<8}")
    print("-" * 55)
    for nombre, pot_w in equipos.items():
        pot_dbm = w_a_dbm(pot_w)
        pot_dbw = dbm_a_dbw(pot_dbm)
        print(f"{nombre:<25} | {pot_w:<8.1f} | {pot_dbm:<8.1f} | {pot_dbw:<8.1f}")

if __name__ == "__main__":
    main_ej1()