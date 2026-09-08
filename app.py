import os

from flask import Flask, jsonify, request
import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data.csv")

df = pd.read_csv(CSV_PATH)

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"status": 'OK',
                    "entorno": 'Listo'} )

@app.route('/songs')
def songs():
    cantidad = request.args.get('cantidad')
    top_tracks = request.args.get('top_tracks', '')
    filtered_df = df.copy()

    if top_tracks not in ['', 'true', 'false', '1', '0', 'yes', 'no', 'si', 'no']:
        return jsonify({"error": "top_tracks debe ser true o false"}), 400

    if top_tracks in ['true', '1', 'yes', 'si']:
        filtered_df = filtered_df.sort_values(by='track_popularity', ascending=False)

    if cantidad is not None:
        try:
            filtered_df = filtered_df.head(int(cantidad))
        except ValueError:
            return jsonify({"error": "cantidad debe ser un número entero"}), 400
    else:
        filtered_df = filtered_df.head(10)

    return jsonify(filtered_df.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)
