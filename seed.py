from models.database import session,engine
from models.model import Users,Rekams,Gejalas,Base
from datetime import datetime


def seed():
    dokter1 = Users(
        username = "dokter1",
        password = "$2a$10$NbWsRmV.f9xQrRI1wLDHEOpATTQUESggwUCreuok8gPwyRCLAqXb2",
        role = 'dokter',
        email = "dokter1@gmail.com",
        nama_lengkap = "dokter1 testing",
        tgl_lahir = "2020-02-01",
    )
    rekam1 = Rekams(
        nama_pasien = "pasien 1 dokter",
        tgl_lahir_pasien = "2011-02-01",
        image = "fakeurl",
        jenis_katarak = "katarak",
        akurasi_cf = 90.0,
        createAt = datetime.now(),
    )
    rekam2 = Rekams(
        nama_pasien = "pasien 2 dokter",
        tgl_lahir_pasien = "2012-04-11",
        image = "fakeurl",
        jenis_katarak = "katarak",
        akurasi_cf = 90.0,
        createAt = datetime.now(),
    )
    gejala1 = Gejalas(
        gejala1 = 0.12,
        gejala2 = 0,
        gejala3 = 0.1,
        gejala4 = 0.23,
        gejala5 = 0.12,
        gejala6 = 0.53,
        gejala7 = 1,
        gejala8 = 0.12,
        gejala9 = 0.23,
        gejala10 = 0.23,
        gejala11 = 0.12,
        gejala12 = 0.54,
        gejala13 = 0.8,
        gejala14 = 0.9,
        gejala15 = 0.11,
        gejala16 = 0.23,
        gejala17 = 0.34,
    )
    gejala2 = Gejalas(
        gejala1 = 0.12,
        gejala2 = 0,
        gejala3 = 0.1,
        gejala4 = 0.23,
        gejala5 = 0.12,
        gejala6 = 0.53,
        gejala7 = 1,
        gejala8 = 0.12,
        gejala9 = 0.23,
        gejala10 = 0.23,
        gejala11 = 0.12,
        gejala12 = 0.54,
        gejala13 = 0.8,
        gejala14 = 0.9,
        gejala15 = 0.11,
        gejala16 = 0.23,
        gejala17 = 0.34
    )
    pasien1 = Users(
        username = "pasien1",
        password = "$2a$10$fvxZlg6eJEUHPLlIJ4U3X.L9fvISUFCG50Qk3/.t6KKhKrBQm1dce",
        role = 'pasien',
        email = "pasien1@gmail.com",
        nama_lengkap = "pasien1 testing",
        tgl_lahir = "2002-02-01",
        rekam_relation = [
            Rekams(
                nama_pasien = "pasien 1 ",
                tgl_lahir_pasien = "2022-02-01",
                image = "fakeurl",
                jenis_katarak = "katarak",
                akurasi_cf = 90.0,
                createAt = datetime.now(),
                gejala_relation = Gejalas(
                    gejala1 = 0.12,
                    gejala2 = 0,
                    gejala3 = 0.1,
                    gejala4 = 0.23,
                    gejala5 = 0.12,
                    gejala6 = 0.53,
                    gejala7 = 1,
                    gejala8 = 0.12,
                    gejala9 = 0.23,
                    gejala10 = 0.23,
                    gejala11 = 0.12,
                    gejala12 = 0.54,
                    gejala13 = 0.8,
                    gejala14 = 0.9,
                    gejala15 = 0.11,
                    gejala16 = 0.23,
                    gejala17 = 0.34
                )
            ),Rekams(
                nama_pasien = "pasien 2",
                tgl_lahir_pasien = "2021-04-11",
                image = "fakeurl",
                jenis_katarak = "katarak",
                akurasi_cf = 90.0,
                createAt = datetime.now(),
                gejala_relation = Gejalas(
                    gejala1 = 0.12,
                    gejala2 = 0,
                    gejala3 = 0.1,
                    gejala4 = 0.23,
                    gejala5 = 0.12,
                    gejala6 = 0.53,
                    gejala7 = 1,
                    gejala8 = 0.12,
                    gejala9 = 0.23,
                    gejala10 = 0.23,
                    gejala11 = 0.12,
                    gejala12 = 0.54,
                    gejala13 = 0.8,
                    gejala14 = 0.9,
                    gejala15 = 0.11,
                    gejala16 = 0.23,
                    gejala17 = 0.34
                )
            ),
        ],
    )

    session.add_all([dokter1,pasien1])

    rekam1.gejala_relation = gejala1
    rekam2.gejala_relation = gejala2

    dokter1.rekam_relation = [rekam1,rekam2]

    try:
        session.add(dokter1)
        session.add(pasien1)
        session.commit()
        session.close()
    except Exception as e:
        print(e)

def migrate():
    Base.metadata.create_all(engine)

def drop():
    Base.metadata.drop_all(engine)