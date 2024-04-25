from flask import make_response, jsonify, request, Blueprint
from sqlalchemy import select
from middleware.authorization import token_required
from models.database import session
from models import model

from package_system import expert_system
import numpy as np

router = Blueprint("klasifikasi",__name__)

@router.route("/", methods=["GET"])
def testrouter():
    return make_response(jsonify(message="klasifikasi route"))


@router.route("/cf", methods = ["POST"])
@token_required(['dokter','pasien'])
def CF(current_user):
    if ("Idrekam" in request.headers)==False:
        return make_response(jsonify(message="bad request id key)"),400)
    idRekams = request.headers['Idrekam']
    gejala = request.json['gejalas']
    try:
        rekamMedis = session.query(model.Rekams).filter_by(id = idRekams).first()
        rekamGejala = session.query(model.Gejalas).filter_by(id = rekamMedis.gejala_id).first()
        rekamGejala.gejala1 = gejala[0]
        rekamGejala.gejala2 = gejala[1]
        rekamGejala.gejala3 = gejala[2]
        rekamGejala.gejala4 = gejala[3]
        rekamGejala.gejala5 = gejala[4]
        rekamGejala.gejala6 = gejala[5]
        rekamGejala.gejala7 = gejala[6]
        rekamGejala.gejala8 = gejala[7]
        rekamGejala.gejala9 = gejala[8]
        rekamGejala.gejala10 = gejala[9]
        rekamGejala.gejala11 = gejala[10]
        rekamGejala.gejala12 = gejala[11]
        rekamGejala.gejala13 = gejala[12]
        rekamGejala.gejala14 = gejala[13]
        rekamGejala.gejala15 = gejala[14]
        rekamGejala.gejala16 = gejala[15]
        gejala.append(rekamGejala.gejala17)
        # session.commit()
        # session.close()
        
        # calculation
        gejala = np.array(gejala)
        CFgejalasMature = expert_system.K01 * gejala
        CFgejalasTraumatik = expert_system.K02 * gejala
        CFgejalasKomplikata = expert_system.K03 * gejala
        CFgejalasSenilis = expert_system.K04 * gejala
        CFgejalasJuvenile = expert_system.K05 * gejala

        resAll = {}

        # print("\n Mature: \n")
        res1 =  expert_system.CF(CFgejalasMature)
        resAll['mature'] = res1
        # print("\n Traumatik: \n")
        res2 =  expert_system.CF(CFgejalasTraumatik)
        resAll['traumatik'] = res2
        # print("\n komplikata: \n")
        res3 =  expert_system.CF(CFgejalasKomplikata)
        resAll['komplikata'] = res3
        # print("\n senilis: \n")
        res4 =  expert_system.CF(CFgejalasSenilis)
        resAll['senilis'] = res4
        # print("\n Juvenile: \n")
        res5 =  expert_system.CF(CFgejalasJuvenile)
        resAll['juvenile'] = res5

        print("Mature    :",res1)
        print("Traumatik :",res2)
        print("Komplikata:",res3)
        print("Senilis   :",res4)
        print("Juvenile  :",res5)
        # print(resAll)
        keys = list(resAll.keys())
        values = list(resAll.values())
        srt_value_i = np.argsort(values)
        resAll = {keys[i]: values[i] for i in srt_value_i}
        # print(resAll)
        katarak = list(resAll)[-1] 
        rekamMedis.jenis_katarak = katarak
        rekamMedis.akurasi_cf = resAll[katarak]*100

        session.commit()
        session.close()

        return make_response(jsonify({
            "katarak":katarak,
            "persentase":resAll[katarak]*100
        }),200)
    
    except Exception as e:
        return make_response(jsonify(error=str(e)),500)
    
