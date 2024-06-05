from middleware.authorization import token_required
from flask import Blueprint,make_response, jsonify, request
from models.database import session
from models import model
from datetime import datetime

router = Blueprint("pasien",__name__)

@router.route("/", methods=["GET"])
@token_required(["pasien"])
def testrouter(current_user):
    return make_response(jsonify(message="test pasien route"))

@router.route("/new_rekaman", methods=["POST"])
@token_required(["pasien"])
def addRekaman(current_user):
    print(current_user.nama_lengkap, current_user.tgl_lahir)
    if (current_user.nama_lengkap and current_user.tgl_lahir) == False:
        return make_response(jsonify(message="request tidak cocok"),422)
    try:
        addRekaman = model.Rekams(
                user_id = current_user.id,
                nama_pasien = current_user.nama_lengkap,
                tgl_lahir_pasien = current_user.tgl_lahir,
                createAt = datetime.now(),
                gejala_relation = model.Gejalas()
            )
        session.add(addRekaman)
        session.commit()
        response = {
            "message":"success",
            "id":addRekaman.id
        }
        session.close()
        return make_response(jsonify(response),200)
    except Exception as e:
        session.rollback()
        return make_response(jsonify(error=str(e)),500)

@router.route("/all_rekaman",methods=['GET'])
@token_required(["pasien"])
def allrekaman(current_user):
    try:
        datas = session.query(model.Rekams).filter_by(user_id=current_user.id)
        all_data = [{
            'id':data.id, 
            'nama_pasien':data.nama_pasien,
            'tgl_lahir_pasien':data.tgl_lahir_pasien,
            'image_url':data.image,
            'jenis_katarak':data.jenis_katarak,
            'akurasi_cf':data.akurasi_cf,
            'tgl_cek':data.createAt,
            'gejala':{
                'g1':data.gejala_relation.gejala1,
                'g2':data.gejala_relation.gejala2,
                'g3':data.gejala_relation.gejala3,
                'g4':data.gejala_relation.gejala4,
                'g5':data.gejala_relation.gejala5,
                'g6':data.gejala_relation.gejala6,
                'g7':data.gejala_relation.gejala7,
                'g8':data.gejala_relation.gejala8,
                'g9':data.gejala_relation.gejala9,
                'g10':data.gejala_relation.gejala10,
                'g11':data.gejala_relation.gejala11,
                'g12':data.gejala_relation.gejala12,
                'g13':data.gejala_relation.gejala13,
                'g14':data.gejala_relation.gejala14,
                'g15':data.gejala_relation.gejala15,
                'g16':data.gejala_relation.gejala16,
                'g17':data.gejala_relation.gejala17,
            }
        } for data in datas]
        return make_response(jsonify(all_data),200)
    except Exception as e:
        session.rollback()
        return make_response(jsonify(error=str(e)),500)

@router.route("/rekaman",methods=['GET'])
@token_required(["pasien"])
def rekamanbyid(current_user):
    try:
        id_get = request.args.get('id')
        rekaman = []
        data_pasiens = session.query(model.Users).filter_by(username = current_user.username).first().rekam_relation
        for data in data_pasiens:
            if (data.id == int(id_get)):
                rekaman.append(data)
        if len(rekaman)== 0:
            return make_response(jsonify(message = 'rekam medis tidak ada pada pasien'),400)
        rekaman = rekaman[0]
        all_data = {
            'id':rekaman.id, 
            'nama_pasien':rekaman.nama_pasien,
            'tgl_lahir_pasien':rekaman.tgl_lahir_pasien,
            'image_url':rekaman.image,
            'jenis_katarak':rekaman.jenis_katarak,
            'akurasi_cf':rekaman.akurasi_cf,
            'tgl_cek':rekaman.createAt,
            'gejala':{
                'g1':rekaman.gejala_relation.gejala1,
                'g2':rekaman.gejala_relation.gejala2,
                'g3':rekaman.gejala_relation.gejala3,
                'g4':rekaman.gejala_relation.gejala4,
                'g5':rekaman.gejala_relation.gejala5,
                'g6':rekaman.gejala_relation.gejala6,
                'g7':rekaman.gejala_relation.gejala7,
                'g8':rekaman.gejala_relation.gejala8,
                'g9':rekaman.gejala_relation.gejala9,
                'g10':rekaman.gejala_relation.gejala10,
                'g11':rekaman.gejala_relation.gejala11,
                'g12':rekaman.gejala_relation.gejala12,
                'g13':rekaman.gejala_relation.gejala13,
                'g14':rekaman.gejala_relation.gejala14,
                'g15':rekaman.gejala_relation.gejala15,
                'g16':rekaman.gejala_relation.gejala16,
                'g17':rekaman.gejala_relation.gejala17,
            }
        } 
        return make_response(jsonify(all_data),200)
    except Exception as e:
        session.rollback()
        return make_response(jsonify(error=str(e)),500)
    
@router.route("/profil",methods=['GET'])
@token_required(["pasien"])
def profilNow(current_user):
    try:
        data_user = session.query(model.Users).filter_by(username = current_user.username).first()
        profil_data = {
            'username' : data_user.username,
            'email' : data_user.email,
            'nama_lengkap' : data_user.nama_lengkap,
            'tgl_lahir' : data_user.tgl_lahir,
        }
        return make_response(jsonify(profil_data),200)
    except Exception as e:
        session.rollback()
        return make_response(jsonify(error=str(e)),500)

@router.route("/rekaman",methods=['DELETE'])
@token_required(["pasien"])
def deleteRekaman(current_user):
    try:
        id_get = request.args.get('id')
        id_gejala = 0
        data_pasiens = session.query(model.Users).filter_by(username = current_user.username).first().rekam_relation
        for data in data_pasiens:
            if (data.id == int(id_get)):
                id_gejala = data.gejala_id
        if id_gejala == 0:
            return make_response(jsonify(message = 'rekam medis tidak ada pada pasien'),400)    
        session.query(model.Rekams).filter_by(id = id_get).delete()
        session.query(model.Gejalas).filter_by(id = id_gejala).delete()
        session.commit()
        session.close()
        return make_response(jsonify(message="success delete id="+str(id_get)),200)
    except Exception as e:
        session.rollback()
        return make_response(jsonify(error=str(e)),500)