import sys, os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.modelObj import shop as shopDB


class cart(shopDB.Model):
    __tablename__ = 'cart'

    idxCart = shopDB.Column(shopDB.INTEGER, autoincrement=True, primary_key=True)
    CartID = shopDB.Column(shopDB.VARCHAR(100), nullable=False)
    CartProductName = shopDB.Column(shopDB.VARCHAR(45), nullable=False)
    CartProductCategory = shopDB.Column(shopDB.VARCHAR(45), nullable=False)
    CartProductID = shopDB.Column(shopDB.VARCHAR(45), nullable=False)
    CartProductRemaining = shopDB.Column(shopDB.INTEGER, nullable=False, default=0)
    CartProductCost = shopDB.Column(shopDB.INTEGER, nullable=False, default=0)
    CartProductInformation = shopDB.Column(shopDB.TEXT, nullable=False)
    ProducerIdentifyNumber = shopDB.Column(shopDB.VARCHAR(100), nullable=False)
    ConsumerIdentifyNumber = shopDB.Column(shopDB.VARCHAR(100), nullable=False)
    CartBuyChecked = shopDB.Column(shopDB.BOOLEAN, nullable=True, default=1)
    UpdateTimestamp = shopDB.Column(shopDB.DATETIME, nullable=True, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def __init__(self, CartID, CartProductName, CartProductCategory, CartProductID, CartProductRemaining, CartProductCost, CartProductInformation, ProducerIdentifyNumber, ConsumerIdentifyNumber, CartBuyChecked, **kwargs):
        self.CartID = CartID
        self.CartProductName = CartProductName
        self.CartProductCategory = CartProductCategory
        self.CartProductID = CartProductID
        self.CartProductRemaining = CartProductRemaining
        self.CartProductCost = CartProductCost
        self.CartProductInformation = CartProductInformation
        self.ProducerIdentifyNumber = ProducerIdentifyNumber
        self.ConsumerIdentifyNumber = ConsumerIdentifyNumber
        self.CartBuyChecked = CartBuyChecked

    def __repr__(self):
        return f"<cart('{self.CartID}', '{self.CartProductName}', '{self.CartProductCategory}', '{self.CartProductID}', '{self.CartProductRemaining}', '{self.CartProductCost}', '{self.CartProductInformation}', '{self.ProducerIdentifyNumber}', '{self.ConsumerIdentifyNumber}', '{self.CartBuyChecked}')>"
