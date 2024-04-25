from sqlalchemy import Column,Integer, String, Float, ForeignKey, DATE, DATETIME
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True, nullable=False)
    username = Column(String(50),nullable=False,unique=True)
    password = Column(String(255),nullable=False)
    role = Column(String(10), nullable=False)
    email = Column(String(255), nullable=True)
    nama_lengkap = Column(String(255),nullable=True)
    tgl_lahir = Column(DATE,nullable=True)

    rekam_relation = relationship("Rekams",back_populates="user_relation")

class Rekams(Base):
    __tablename__ = 'rekams'
    id = Column(Integer,primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'),nullable=False)
    gejala_id = Column(Integer,ForeignKey('gejalas.id'),nullable=False)
    nama_pasien = Column(String(255),nullable=False)
    tgl_lahir_pasien = Column(DATE,nullable=False)
    image = Column(String(255),nullable=True)
    jenis_katarak = Column(String(255),nullable=True)
    akurasi_cf = Column(Float)
    createAt = Column(DATETIME,nullable=False)

    user_relation = relationship("Users", back_populates="rekam_relation")
    gejala_relation = relationship("Gejalas", back_populates="rekam_relation")


class Gejalas(Base):
    __tablename__ = 'gejalas'
    id = Column(Integer,primary_key=True)
    gejala1 = Column(Float)
    gejala2 = Column(Float)
    gejala3 = Column(Float)
    gejala4 = Column(Float)
    gejala5 = Column(Float)
    gejala6 = Column(Float)
    gejala7 = Column(Float)
    gejala8 = Column(Float)
    gejala9 = Column(Float)
    gejala10 = Column(Float)
    gejala11 = Column(Float)
    gejala12 = Column(Float)
    gejala13 = Column(Float)
    gejala14 = Column(Float)
    gejala15 = Column(Float)
    gejala16 = Column(Float)
    gejala17 = Column(Float)

    rekam_relation = relationship("Rekams", back_populates="gejala_relation")
