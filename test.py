import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.model import *

@pytest.fixture(scope='module')
def test_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_room(test_session):
    new_room = Room(
        name="BedRoom",
        surface_area=25.50,
        flooring_type="hardwood",
        flooring_cost_per_sqft=1.25,
        is_tiling_needed=True,
        tile_type="glass",
        tile_cost_per_sqft=3.75,
        tiling_area=3.00,
        total_supply_cost=
    )