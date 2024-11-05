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
        total_supply_cost=0
    )

    test_session.add(new_room)
    test_session.commit()

    room = test_session.query(Room).first()
    assert room.name == "BedRoom"
    assert room.surface_area == 25.5
    assert room.flooring_type == "hardwood"
    assert room.flooring_cost_per_sqft == 1.25
    assert room.is_tiling_needed == "1"
    assert room.tile_type == "glass"
    assert room.tile_cost_per_sqft == 3.75
    assert room.tiling_area == 3.00
    assert room.total_supply_cost == 0