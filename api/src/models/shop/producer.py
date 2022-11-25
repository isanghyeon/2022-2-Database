import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.modelObj import shop as shopDB


class producer(shopDB.Model):
    __tablename__ = 'producer'

    idxProducer = shopDB.Column(shopDB.Integer, autoincrement=True, primary_key=True)
    ProducerEmail = shopDB.Column(shopDB.VARCHAR(45), nullable=False)
    ProducerPWD = shopDB.Column(shopDB.CHAR(100), nullable=False)
    ProducerName = shopDB.Column(shopDB.VARCHAR(45), nullable=False)
    Address = shopDB.Column(shopDB.VARCHAR(45), nullable=False)
    PhoneNumber = shopDB.Column(shopDB.VARCHAR(45), nullable=False)
    ClassificationNumber = shopDB.Column(shopDB.INTEGER, nullable=True, default=1)
    IdentifyNumber = shopDB.Column(shopDB.VARCHAR(100), nullable=False)
    LastLogin = shopDB.Column(shopDB.DATETIME, nullable=True)
    CreateTime = shopDB.Column(shopDB.DATETIME, nullable=True)

    def __init__(self, ProducerEmail, ProducerPWD, ProducerName, Address, PhoneNumber, ClassificationNumber, IdentifyNumber, LastLogin, CreateTime, **kwargs):
        self.ProducerEmail = ProducerEmail
        self.ProducerPWD = ProducerPWD
        self.ProducerName = ProducerName
        self.Address = Address
        self.PhoneNumber = PhoneNumber
        self.ClassificationNumber = ClassificationNumber
        self.IdentifyNumber = IdentifyNumber
        self.LastLogin = LastLogin
        self.CreateTime = CreateTime

    def __repr__(self):
        return f"<producer('{self.ProducerEmail}', '{self.ProducerPWD}', '{self.ProducerName}', '{self.Address}', '{self.PhoneNumber}', '{self.ClassificationNumber}', '{self.IdentifyNumber}', '{self.LastLogin}', '{self.CreateTime}')>"
