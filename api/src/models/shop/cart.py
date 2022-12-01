import sys, os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.modelObj import shop as shopDB


class cart(shopDB.Model):
    __tablename__ = 'cart'

    idxCart = shopDB.Column(shopDB.INTEGER, autoincrement=True, primary_key=True)
    CartProductName = shopDB.Column(shopDB.VARCHAR(45), nullable=False)
    CartProductID = shopDB.Column(shopDB.VARCHAR(45), nullable=False)
    CartProductCost = shopDB.Column(shopDB.INTEGER, nullable=False, default=0)
    CartProductImage = shopDB.Column(shopDB.VARCHAR(45), nullable=False)
    ProducerIdentifyNumber = shopDB.Column(shopDB.VARCHAR(100), nullable=False, default='635265ac-6cb9-11ed-bef8-acde48001122')
    ConsumerIdentifyNumber = shopDB.Column(shopDB.VARCHAR(100), nullable=False)
    CartBuyChecked = shopDB.Column(shopDB.BOOLEAN, nullable=True, default=False)
    UpdateTimestamp = shopDB.Column(shopDB.DATETIME, nullable=True, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def __init__(self, CartProductName, CartProductID, CartProductCost, CartProductImage, ProducerIdentifyNumber, ConsumerIdentifyNumber, CartBuyChecked, **kwargs):
        self.CartProductName = CartProductName
        self.CartProductID = CartProductID
        self.CartProductCost = CartProductCost
        self.CartProductImage = CartProductImage
        self.ProducerIdentifyNumber = ProducerIdentifyNumber
        self.ConsumerIdentifyNumber = ConsumerIdentifyNumber
        self.CartBuyChecked = CartBuyChecked

    def __repr__(self):
        return f"<cart('{self.CartProductName}', '{self.CartProductID}', '{self.CartProductCost}', '{self.CartProductImage}', '{self.ProducerIdentifyNumber}', '{self.ConsumerIdentifyNumber}', '{self.CartBuyChecked}')>"
