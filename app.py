import os
import routes
from flask import Flask, request, make_response, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def helloworld():
    return make_response(jsonify(message="API eyecheck"),200)

app.register_blueprint(routes.auth.router, url_prefix="/auth")
app.register_blueprint(routes.dokter.router, url_prefix="/dokter")
app.register_blueprint(routes.pasien.router, url_prefix="/pasien")
app.register_blueprint(routes.deteksi.router, url_prefix="/deteksi")
app.register_blueprint(routes.klasifikasi.router, url_prefix="/klasifikasi")

if __name__ == "__main__":
    app.run(host=os.getenv("HOST"), port=os.getenv("PORT"))