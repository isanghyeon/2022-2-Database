import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.modelObj import shop as shopDB


class product(shopDB.Model):
    __tablename__ = 'product'

    idxProduct = shopDB.Column(shopDB.INTEGER, autoincrement=True, primary_key=True)
    ProductName = shopDB.Column(shopDB.VARCHAR(45), nullable=False)
    ProductCategory = shopDB.Column(shopDB.VARCHAR(45), nullable=False)
    ProductID = shopDB.Column(shopDB.VARCHAR(45), nullable=False)
    ProductOwnerID = shopDB.Column(shopDB.VARCHAR(45), nullable=False)
    ProductRemaining = shopDB.Column(shopDB.INTEGER, nullable=True, default=0)
    ProductCost = shopDB.Column(shopDB.INTEGER, nullable=True, default=0)
    ProductInformation = shopDB.Column(shopDB.TEXT, nullable=False)
    ProductImage = shopDB.Column(shopDB.JSON, nullable=True)

    def __init__(self, ProductName, ProductCategory, ProductID, ProductOwnerID, ProductRemaining, ProductCost, ProductInformation, ProductImage, **kwargs):
        self.ProductName = ProductName
        self.ProductCategory = ProductCategory
        self.ProductID = ProductID
        self.ProductOwnerID = ProductOwnerID
        self.ProductRemaining = ProductRemaining
        self.ProductCost = ProductCost
        self.ProductInformation = ProductInformation
        self.ProductImage = ProductImage

    def __repr__(self):
        return f"<product('{self.ProductName}', '{self.ProductCategory}', '{self.ProductID}', '{self.ProductOwnerID}', '{self.ProductRemaining}', '{self.ProductCost}', '{self.ProductInformation}', '{self.ProductImage}')>"
