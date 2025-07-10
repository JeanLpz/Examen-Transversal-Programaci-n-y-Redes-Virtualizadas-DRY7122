import requests

# Configuración
API_KEY_GRAPHHOPPER = "22010d2f-4e55-4f3e-824f-4e9a3101df9d"  
BASE_URL = "https://graphhopper.com/api/1/route"

# Diccionario de coordenadas predefinidas 
CIUDADES = {
    "santiago, chile": "-33.4489,-70.6693",
    "mendoza, argentina": "-32.8908,-68.8272",
    "buenos aires, argentina": "-34.6037,-58.3816",
    "valparaíso, chile": "-33.0472,-71.6127"
}

def obtener_coordenadas(ciudad):
    """Busca coordenadas en nuestro diccionario"""
    ciudad = ciudad.lower().strip()
    return CIUDADES.get(ciudad)

def obtener_ruta(origen, destino, transporte):
    # Obtener coordenadas
    punto_origen = obtener_coordenadas(origen)
    punto_destino = obtener_coordenadas(destino)
    
    if not punto_origen:
        print(f"Error: Ciudad de origen '{origen}' no encontrada. Ciudades disponibles:")
        for ciudad in CIUDADES:
            print(f"- {ciudad.title()}")
        return None
        
    if not punto_destino:
        print(f"Error: Ciudad de destino '{destino}' no encontrada. Ciudades disponibles:")
        for ciudad in CIUDADES:
            print(f"- {ciudad.title()}")
        return None

    params = {
        "point": [punto_origen, punto_destino],
        "vehicle": transporte,
        "locale": "es",
        "key": API_KEY_GRAPHHOPPER,
        "instructions": True,
        "calc_points": True
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        if "paths" not in data:
            print("Error al obtener la ruta:", data.get("message", "Error desconocido"))
            return None
            
        return data["paths"][0]
    except Exception as e:
        print("Error de conexión:", str(e))
        return None

def mostrar_resultados(ruta):
    if not ruta:
        return
        
    distancia_km = ruta["distance"] / 1000
    distancia_millas = distancia_km * 0.621371
    duracion_horas = ruta["time"] / 3600000
    
    print("\n=== RESULTADOS ===")
    print(f"Distancia: {distancia_km:.2f} km ({distancia_millas:.2f} millas)")
    print(f"Duración: {duracion_horas:.2f} horas")
    
    print("\n=== INSTRUCCIONES ===")
    for instruccion in ruta["instructions"]:
        print(f"{instruccion['text']} ({instruccion['distance']/1000:.2f} km)")

def main():
    print("=== CALCULADORA DE RUTAS CHILE-ARGENTINA ===")
    print("Ciudades predefinidas disponibles:")
    for ciudad in CIUDADES:
        print(f"- {ciudad.title()}")
    
    print("\nIngrese 's' para salir\n")
    
    while True:
        origen = input("Ciudad de Origen (Chile): ")
        if origen.lower() == 's':
            break
            
        destino = input("Ciudad de Destino (Argentina): ")
        if destino.lower() == 's':
            break
            
        print("\nMedios de transporte:")
        print("1 - Auto")
        print("2 - Bicicleta")
        print("3 - Caminando")
        opcion = input("Elija (1-3): ")
        
        transporte = {
            "1": "car",
            "2": "bike",
            "3": "foot"
        }.get(opcion, "car")
        
        ruta = obtener_ruta(origen, destino, transporte)
        if ruta:
            mostrar_resultados(ruta)
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()