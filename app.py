from dotenv import load_dotenv
import os
import routes
from flask import Flask, request, make_response, jsonify,send_file

load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def helloworld():
    return make_response(jsonify(message="API eyecheck"),200)

@app.route("/image/<img_name>",methods= ["GET"])
def imageSend(img_name):
    img_path = f"APIfile/{img_name}"
    try:
        return make_response(send_file(img_path,mimetype='image/jpeg'),200)
    except Exception as e:
        return make_response(jsonify(error=str(e)),500)

app.register_blueprint(routes.auth.router, url_prefix="/auth")
app.register_blueprint(routes.dokter.router, url_prefix="/dokter")
app.register_blueprint(routes.pasien.router, url_prefix="/pasien")
app.register_blueprint(routes.deteksi.router, url_prefix="/deteksi")
app.register_blueprint(routes.klasifikasi.router, url_prefix="/klasifikasi")


if __name__ == "__main__":
    app.run(host=os.getenv("HOST"), port=os.getenv("PORT"),debug=True)