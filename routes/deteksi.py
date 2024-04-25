from flask import make_response, jsonify, request, Blueprint
from sqlalchemy import select
from middleware.authorization import token_required
from models.database import session
from models import model
from datetime import datetime

import cv2
import numpy as np
import pypickle
import pandas as pd

from package_system import detection



router = Blueprint("deteksi",__name__)

@router.route("/", methods=["GET"])
def testrouter():
    return make_response(jsonify(message="test deteksi route"))

@router.route("/upload", methods=["POST"])
@token_required(["dokter","pasien"])
def upload(current_user):
    if (("image" in request.files) == False) or (("Idrekam" in request.headers)==False):
        return make_response(jsonify(message="bad request image key)"),400)
    idRekams = request.headers['Idrekam']
    image = request.files['image']
    if (image) == False :
        return make_response(jsonify(message="empty image)"),400)
    filename = datetime.now().strftime("%Y%m%d%H%M%S")
    pathFile = "./APIfile/"+filename+".jpg"
    try:
        image.save(pathFile)
        stmt = select(model.Rekams).where(model.Rekams.id  == idRekams)
        rekamSession = session.scalars(stmt).one()
        rekamSession.image = pathFile
        session.commit()
        session.close()
        return make_response(jsonify(url=pathFile),200)
    except Exception as e:
        return make_response(jsonify(message="error :" + str(e)),500)


@router.route("/svm",methods=["POST"])
@token_required(["dokter","pasien"])
def svm(current_user):
    if ("Idrekam" in request.headers) == False:
        return make_response(jsonify(message="bad request Idrekam)"),400)
    idRekams = request.headers['Idrekam']
    try:
        rekaman = session.query(model.Rekams).filter_by(id=idRekams).first()
        img = cv2.imread(rekaman.image)
        img = cv2.resize(img,(300,300),interpolation=cv2.INTER_CUBIC)
        img = detection.removeFlare(img)
        img = detection.claheFilterContrast(img)
        roi_pupil = detection.ROI_segmentation(img)
        roi_pupil = cv2.resize(roi_pupil,(50,50),interpolation=cv2.INTER_CUBIC)
        x_array = []
        x_array.append(roi_pupil.flatten())
        x_data = np.array(x_array)
        x = pd.DataFrame(x_data)
        modelload = pypickle.load("./APIfile/model2.pkl")
        result = modelload.predict(x)
        if result[0] == 0:
            rekaman.gejala_relation.gejala17 = 1.0
            session.commit()
            session.close()
            return make_response(jsonify({
                "message":"success",
                "Result":"Katarak",
            }),200)
        else: 
            rekaman.gejala_relation.gejala17 = 0.0
            session.commit()
            session.close()
            return make_response(jsonify({
                "message":"success",
                "Result":"Normal",
            }),200)
    except Exception as e:
        session.rollback()
        return make_response(jsonify(error=str(e)),500)