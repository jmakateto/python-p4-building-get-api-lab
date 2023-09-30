from app import app, db
from models import Bakery, BakedGood

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        bakery1 = Bakery(name='Bakery 1')
        bakery2 = Bakery(name='Bakery 2')
        db.session.add_all([bakery1, bakery2])
        db.session.commit()

        baked_good1 = BakedGood(name='Baked Good 1', price=10, bakery=bakery1)
        baked_good2 = BakedGood(name='Baked Good 2', price=15, bakery=bakery1)
        baked_good3 = BakedGood(name='Baked Good 3', price=8, bakery=bakery2)
        db.session.add_all([baked_good1, baked_good2, baked_good3])
        db.session.commit()
