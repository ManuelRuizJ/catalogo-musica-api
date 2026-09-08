from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"status": 'OK',
                    "entorno": 'Listo'} )



if __name__ == '__main__':
    app.run(debug=True)
