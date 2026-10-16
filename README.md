# Evaluacion2 - Planificador de rutas (GraphHopper)

## Descripcion
Script en Python que consume la API REST de GraphHopper Directions para calcular rutas
entre dos ubicaciones. Todos los textos estan en espanol, las distancias se muestran con
dos decimales, entrega la narrativa del viaje paso a paso y permite salir escribiendo
"s" o "salir".

## Requisitos
- Python 3
- Libreria requests (pip3 install requests)
- Una API key de GraphHopper (https://graphhopper.com/dashboard)

## Como ejecutar
1. Abrir geolocalizacion.py y reemplazar TU_API_KEY_DE_GRAPHHOPPER por la API key propia.
2. Ejecutar en la terminal: python3 geolocalizacion.py
3. Ingresar el tipo de transporte (auto, bicicleta o a pie), el origen y el destino.
4. Para terminar, ingresar "s" o "salir".
