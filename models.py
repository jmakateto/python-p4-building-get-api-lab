from database import db

class Bakery(db.Model):
    __tablename__ = 'bakeries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    baked_goods = db.relationship('BakedGood', backref='bakery', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'baked_goods': [good.serialize() for good in self.baked_goods]
        }

class BakedGood(db.Model):
    __tablename__ = 'baked_goods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id'), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'bakery_id': self.bakery_id
        }
