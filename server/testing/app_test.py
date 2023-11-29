import json
from flask import Flask
from models import db, Bakery, BakedGood


class TestApp:
    """Flask application in flask_app.py"""

    @classmethod
    def setup_class(cls):
        cls.app = Flask(__name__)
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        cls.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        cls.app.json.compact = False

        db.init_app(cls.app)
        with cls.app.app_context():
            db.create_all()

    @classmethod
    def teardown_class(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_bakeries_route(self):
        """has a resource available at "/bakeries"."""
        with self.app.app_context():
            response = self.app.test_client().get("/bakeries")
            assert response.status_code == 200

    def test_bakeries_route_returns_json(self):
        '''provides a response content type of application/json at "/bakeries"'''
        with self.app.app_context():
            response = self.app.test_client().get("/bakeries")
            assert response.content_type == "application/json"

    def test_bakeries_route_returns_list_of_bakery_objects(self):
        """returns JSON representing models.Bakery objects."""
        with self.app.app_context():
            b = Bakery(name="Mr. Bakery")
            db.session.add(b)
            db.session.commit()

            response = self.app.test_client().get("/bakeries")
            data = json.loads(response.data.decode())
            assert type(data) == list
            for record in data:
                assert type(record) == dict
                assert record["id"]
                assert record["name"]
                assert record["created_at"]

            db.session.delete(b)
            db.session.commit()

    def test_bakery_by_id_route(self):
        """has a resource available at "/bakeries/<int:id>"."""
        with self.app.app_context():
            b = Bakery(name="Mr. Bakery")
            db.session.add(b)
            db.session.commit()

            response = self.app.test_client().get("/bakeries/1")
            assert response.status_code == 200

            db.session.delete(b)
            db.session.commit()

    def test_bakery_by_id_route_returns_json(self):
        '''provides a response content type of application/json at "/bakeries/<int:id>"'''
        with self.app.app_context():
            b = Bakery(name="Mr. Bakery")
            db.session.add(b)
            db.session.commit()

            response = self.app.test_client().get("/bakeries/1")
            assert response.content_type == "application/json"

            db.session.delete(b)
            db.session.commit()

    def test_bakery_by_id_route_returns_one_bakery_object(self):
        """returns JSON representing one models.Bakery object."""
        with self.app.app_context():
            b = Bakery(name="Mr. Bakery")
            db.session.add(b)
            db.session.commit()

            response = self.app.test_client().get("/bakeries/1")
            data = json.loads(response.data.decode())
            assert type(data) == dict
            assert data["id"]
            assert data["name"]
            assert data["created_at"]

            db.session.delete(b)
            db.session.commit()

    def test_baked_goods_by_price_route(self):
        """has a resource available at "/baked_goods/by_price"."""
        response = self.app.test_client().get("/baked_goods/by_price")
        assert response.status_code == 200

    def test_baked_goods_by_price_route_returns_json(self):
        '''provides a response content type of application/json at "/baked_goods/by_price"'''
        response = self.app.test_client().get("/baked_goods/by_price")
        assert response.content_type == "application/json"

    def test_baked_goods_by_price_returns_list_of_baked_goods(self):
        """returns JSON representing one models.Bakery object."""
        with self.app.app_context():
            bg = BakedGood(name="Madeleine", price=10)
            db.session.add(bg)
            db.session.commit()

            response = self.app.test_client().get("/baked_goods/by_price")
            data = json.loads(response.data.decode())
            assert type(data) == list
            for record in data:
                assert record["id"]
                assert record["name"]
                assert record["price"]
                assert record["created_at"]

            db.session.delete(bg)
            db.session.commit()

    def test_most_expensive_baked_good_route(self):
        """has a resource available at "/baked_goods/most_expensive"."""
        response = self.app.test_client().get("/baked_goods/most_expensive")
        assert response.status_code == 200

    def test_most_expensive_baked_good_route_returns_json(self):
        '''provides a response content type of application/json at "/bakeries/<int:id>"'''
        response = self.app.test_client().get("/baked_goods/most_expensive")
        assert response.content_type == "application/json"

    def test_most_expensive_baked_good_route_returns_one_baked_good_object(self):
        """returns JSON representing one models.BakedGood object."""
        with self.app.app_context():
            bg = BakedGood(name="Madeleine", price=10)
            db.session.add(bg)
            db.session.commit()

            response = self.app.test_client().get("/baked_goods/most_expensive")
            data = json.loads(response.data.decode())
            assert type(data) == dict
            assert data["id"]
            assert data["name"]
            assert data["price"]
            assert data["created_at"]

            db.session.delete(bg)
            db.session.commit()

    def test_most_expensive_baked_good_route_returns_most_expensive_baked_good_object(
        self,
    ):
        """returns JSON representing one models.BakedGood object."""
        with self.app.app_context():
            bg = BakedGood(name="Madeleine", price=10)
            db.session.add(bg)
            db.session.commit()

            response = self.app.test_client().get("/baked_goods/most_expensive")
            data = json.loads(response.data.decode())
            prices = [baked_good["price"] for baked_good in data]
            highest_price = max(prices)

            assert data["price"] == highest_price

            db.session.delete(bg)
            db.session.commit()
