from flask import Flask, jsonify, request
import json
from pathlib import Path


def cargar_canciones():
    RUTA_DATOS = Path("data/canciones.json")
    with open(RUTA_DATOS, 'r') as f:
        return json.load(f)


canciones = cargar_canciones()
app = Flask(__name__)


@app.route('/health')
def health_check():
    return jsonify({"status": "ok", "entorno": "Listo"})


@app.get("/canciones")
def listar_canciones():
    print(f"Canciones: {canciones}")
    return jsonify(canciones)


@app.get('/canciones/<int:cancion_id>')
def consultar_cancion(cancion_id):
    cancion = next((c for c in canciones if c['id'] == cancion_id), None)
    if cancion is not None:
        print(f"Canción consultada: {cancion}")
        return jsonify(cancion)
    return jsonify({"error": "Canción no encontrada"}), 404


@app.post("/canciones")
def agregar_cancion():
    nueva_cancion = request.get_json()
    if not nueva_cancion:
        return jsonify({"error": "Datos de la canción no proporcionados"}), 400

    nueva_cancion['id'] = max(c['id'] for c in canciones) + 1 if canciones else 1
    canciones.append(nueva_cancion)
    print(f"Canción agregada: {nueva_cancion}")

    RUTA_DATOS = Path("data/canciones.json")
    with open(RUTA_DATOS, 'w') as f:
        json.dump(canciones, f, indent=4)

    return jsonify(nueva_cancion), 201


@app.put('/canciones/<int:cancion_id>')
def actualizar_cancion(cancion_id):
    cancion = next((c for c in canciones if c['id'] == cancion_id), None)
    if cancion is None:
        return jsonify({"error": "Canción no encontrada"}), 404

    datos_actualizados = request.get_json()
    if not datos_actualizados:
        return jsonify({"error": "Datos de la canción no proporcionados"}), 400

    cancion.update(datos_actualizados)
    print(f"Canción actualizada: {cancion}")

    RUTA_DATOS = Path("data/canciones.json")
    with open(RUTA_DATOS, 'w') as f:
        json.dump(canciones, f, indent=4)

    return jsonify(cancion)


@app.delete('/canciones/<int:cancion_id>')
def eliminar_cancion(cancion_id):
    cancion = next((c for c in canciones if c['id'] == cancion_id), None)
    if cancion is None:
        return jsonify({"error": "Canción no encontrada"}), 404

    canciones.remove(cancion)
    print(f"Canción eliminada: {cancion}")

    RUTA_DATOS = Path("data/canciones.json")
    with open(RUTA_DATOS, 'w') as f:
        json.dump(canciones, f, indent=4)

    return jsonify({"mensaje": "Canción eliminada correctamente"})


if __name__ == '__main__':
    app.run(debug=True)
