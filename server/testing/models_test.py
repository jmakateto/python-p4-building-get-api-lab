from datetime import date
import pytest
from app import app, db
from models import Bakery, BakedGood


@pytest.fixture
def clean_up_bakery():
    with app.app_context():
        b = Bakery.query.filter(Bakery.name == "Mr. Bakery")
        for mb in b:
            db.session.delete(mb)
        db.session.commit()


@pytest.fixture
def clean_up_baked_good():
    with app.app_context():
        bg = BakedGood.query.filter(BakedGood.name == "Madeleine")
        for m in bg:
            db.session.delete(m)
        db.session.commit()


class TestBakery:
    @pytest.fixture(autouse=True)
    def cleanup(self, clean_up_bakery):
        yield
        clean_up_bakery()

    def test_can_instantiate(self):
        b = Bakery(name="Mr. Bakery")
        assert b

    def test_can_be_created(self):
        with app.app_context():
            b = Bakery(name="Mr. Bakery")
            db.session.add(b)
            db.session.commit()
            assert b.id is not None

    def test_can_be_retrieved(self):
        with app.app_context():
            b = Bakery.query.all()
            assert b

    def test_can_be_serialized(self):
        with app.app_context():
            b = Bakery(name="Mr. Bakery")
            db.session.add(b)
            db.session.commit()
            bs = Bakery.query.first().to_dict()
            assert bs["id"] is not None
            assert bs["created_at"] is not None

    def test_can_be_deleted(self):
        with app.app_context():
            b = Bakery(name="Mr. Bakery")
            db.session.add(b)
            db.session.commit()
            bakery_id = b.id

            db.session.delete(b)
            db.session.commit()

            b = Bakery.query.get(bakery_id)
            assert b is None


class TestBakedGood:
    @pytest.fixture(autouse=True)
    def cleanup(self, clean_up_baked_good):
        yield
        clean_up_baked_good()


class TestBakedGood:
    @pytest.fixture(autouse=True)
    def cleanup(self, clean_up_baked_good):
        yield
        clean_up_baked_good()

    def test_can_instantiate(self):
        bg = BakedGood(name="Madeleine", price=4)
        assert bg

    def test_can_be_created(self):
        with app.app_context():
            bg = BakedGood(name="Madeleine", price=4)
            db.session.add(bg)
            db.session.commit()
            assert bg.id is not None

    def test_can_be_retrieved(self):
        with app.app_context():
            bg = BakedGood.query.all()
            assert bg

    def test_can_be_serialized(self):
        with app.app_context():
            bg = BakedGood(name="Madeleine", price=4)
            db.session.add(bg)
            db.session.commit()
            bgs = BakedGood.query.first().to_dict()
            assert bgs["id"] is not None
            assert bgs["created_at"] is not None

    def test_can_be_deleted(self):
        with app.app_context():
            bg = BakedGood(name="Madeleine", price=4)
            db.session.add(bg)
            db.session.commit()
            baked_good_id = bg.id

            db.session.delete(bg)
            db.session.commit()

            bg = BakedGood.query.get(baked_good_id)
            assert bg is None
