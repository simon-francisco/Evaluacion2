import requests
import urllib.parse

URL_GEOCODIFICACION = "https://graphhopper.com/api/1/geocode?"
URL_RUTA = "https://graphhopper.com/api/1/route?"
KEY = "TU_API_KEY_DE_GRAPHHOPPER"

VEHICULOS = {"auto": "car", "bicicleta": "bike", "a pie": "foot"}


def es_salida(texto):
    return texto.strip().lower() in ("s", "salir")


def geocodificar(ubicacion):
    url = URL_GEOCODIFICACION + urllib.parse.urlencode({"q": ubicacion, "limit": "1", "key": KEY})
    respuesta = requests.get(url)
    datos = respuesta.json()
    if respuesta.status_code == 200 and len(datos["hits"]) != 0:
        lugar = datos["hits"][0]
        lat, lng = lugar["point"]["lat"], lugar["point"]["lng"]
        nombre = lugar["name"]
        pais = lugar.get("country", "")
        print(f"URL de geocodificación para {nombre}, {pais} -> {url}")
        return lat, lng, nombre
    print(f"Error de geocodificación: no se encontró '{ubicacion}' (código {respuesta.status_code}).")
    return None


print("=" * 60)
print("PLANIFICADOR DE RUTAS - BIBLIOTECA NACIONAL")
print("Ingrese 's' o 'salir' en cualquier momento para terminar.")
print("=" * 60)

while True:
    print("\nTipos de transporte disponibles: auto, bicicleta, a pie")
    transporte = input("Ingrese el tipo de transporte: ").strip().lower()
    if es_salida(transporte):
        break
    if transporte not in VEHICULOS:
        print("Transporte no válido. Se usará 'auto' por defecto.")
        transporte = "auto"

    origen = input("Ingrese la ubicación de origen: ")
    if es_salida(origen):
        break
    destino = input("Ingrese el destino: ")
    if es_salida(destino):
        break

    inicio = geocodificar(origen)
    fin = geocodificar(destino)
    if inicio is None or fin is None:
        continue

    parametros = [
        ("point", f"{inicio[0]},{inicio[1]}"),
        ("point", f"{fin[0]},{fin[1]}"),
        ("vehicle", VEHICULOS[transporte]),
        ("locale", "es"),
        ("key", KEY),
    ]
    url_ruta = URL_RUTA + urllib.parse.urlencode(parametros)
    respuesta = requests.get(url_ruta)
    datos = respuesta.json()

    print("=" * 60)
    print(f"Estado de la API de rutas: {respuesta.status_code}")
    print(f"URL de la ruta: {url_ruta}")
    print("=" * 60)

    if respuesta.status_code == 200:
        ruta = datos["paths"][0]
        km = ruta["distance"] / 1000
        millas = km / 1.609344
        segundos = int(ruta["time"] / 1000)
        horas = segundos // 3600
        minutos = (segundos % 3600) // 60
        seg = segundos % 60

        print(f"Ruta desde {inicio[2]} hasta {fin[2]} en {transporte}")
        print(f"Distancia: {millas:.2f} millas / {km:.2f} km")
        print(f"Duración del viaje: {horas:02d}:{minutos:02d}:{seg:02d}")
        print("=" * 60)
        print("NARRATIVA DEL VIAJE (instrucciones paso a paso)")
        print("=" * 60)
        for paso in ruta["instructions"]:
            distancia_paso = paso["distance"] / 1000
            print(f"{paso['text']} ( {distancia_paso:.2f} km )")
        print("=" * 60)
    else:
        print(f"Error: {datos.get('message', 'No se pudo calcular la ruta.')}")

print("Programa finalizado. ¡Hasta pronto!")