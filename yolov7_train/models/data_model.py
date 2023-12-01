from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from ..config.connect_db import db


class Dulieu(db.Model):
    __tablename__ = 'dulieu'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    train_path = Column(String(255), nullable=False)
    test_path = Column(String(255), nullable=False)

    def __init__(self, ten, train_path, test_path):
        self.ten = ten
        self.train_path = train_path
        self.test_path = test_path


class Thuattoan(db.Model):
    __tablename__ = 'thuattoan'

    id = Column(Integer, primary_key=True)
    ten = Column(String(255), nullable=False)
    mota = Column(String(255))

    def __init__(self, ten, mota):
        self.ten = ten
        self.mota = mota


class Mohinh(db.Model):
    __tablename__ = 'mohinh'

    id = Column(Integer, primary_key=True)
    dulieu_id = Column(Integer, ForeignKey('dulieu.id'), nullable=False)
    thuattoan_id = Column(Integer, ForeignKey('thuattoan.id'), nullable=False)
    ten = Column(String(255), nullable=False)
    ngayhl = Column(DateTime)
    duongdan = Column(String(255), nullable=False)
    mota = Column(String(255))
    soluongmau = Column(Integer)
    acc = Column(Float)
    pre = Column(Float)
    re = Column(Float)
    f1 = Column(Float)
    # hoatdong = Column(Boolean)
    hoatdong = Column(Integer)

    dulieu = relationship('Dulieu', backref='mohinhs')
    thuattoan = relationship('Thuattoan', backref='mohinhs')

    def __init__(self, dulieu_id, thuattoan_id, ten, ngayhl, duongdan, mota, soluongmau, acc, pre, re, f1, hoatdong):
        self.dulieu_id = dulieu_id
        self.thuattoan_id = thuattoan_id
        self.ten = ten
        self.ngayhl = ngayhl
        self.duongdan = duongdan
        self.mota = mota
        self.soluongmau = soluongmau
        self.acc = acc
        self.pre = pre
        self.re = re
        self.f1 = f1
        self.hoatdong = hoatdong
