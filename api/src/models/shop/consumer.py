import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.modelObj import shop as shopDB


class consumer(shopDB.Model):
    __tablename__ = 'consumer'

    idxConsumer = shopDB.Column(shopDB.INTEGER, autoincrement=True, primary_key=True, )
    ConsumerEmail = shopDB.Column(shopDB.VARCHAR(45), nullable=False)
    ConsumerPWD = shopDB.Column(shopDB.CHAR(100), nullable=False)
    ConsumerName = shopDB.Column(shopDB.VARCHAR(45), nullable=False)
    Address = shopDB.Column(shopDB.VARCHAR(100), nullable=False)
    PhoneNumber = shopDB.Column(shopDB.VARCHAR(45), nullable=False)
    ClassificationNumber = shopDB.Column(shopDB.INTEGER, nullable=True, default=1)
    IdentifyNumber = shopDB.Column(shopDB.VARCHAR(100), nullable=False)
    LastLogin = shopDB.Column(shopDB.DATETIME, nullable=True)
    CreateTime = shopDB.Column(shopDB.DATETIME, nullable=True)

    def __init__(self, ConsumerEmail, ConsumerPWD, ConsumerName, Address, PhoneNumber, ClassificationNumber, IdentifyNumber, LastLogin, CreateTime, **kwargs):
        self.ConsumerEmail = ConsumerEmail
        self.ConsumerPWD = ConsumerPWD
        self.ConsumerName = ConsumerName
        self.Address = Address
        self.PhoneNumber = PhoneNumber
        self.ClassificationNumber = ClassificationNumber
        self.IdentifyNumber = IdentifyNumber
        self.LastLogin = LastLogin
        self.CreateTime = CreateTime

    def __repr__(self):
        return f"<consumer('{self.ConsumerEmail}', '{self.ConsumerPWD}', '{self.ConsumerName}', '{self.Address}', '{self.PhoneNumber}', '{self.ClassificationNumber}', '{self.IdentifyNumber}', '{self.LastLogin}', '{self.CreateTime}')>"
