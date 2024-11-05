import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship


# Get the current directory of the script
basedir = os.path.abspath(os.path.dirname(__file__))

# Modify the path to store the database inside a folder named 'database'
database_path = os.path.join(basedir, 'database', 'remodels.db')

# Ensure the 'database' folder exists
os.makedirs(os.path.dirname(database_path), exist_ok=True)

engine = create_engine('sqlite:///remodels.db')
SS = sessionmaker(bind=engine)


Base = declarative_base()

class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surface_area = Column(Float)
    flooring_type = Column(String)
    flooring_cost_per_sqft = Column(Float)

    # New Fields
    is_tiling_needed = Column(Boolean)  # boolean
    tile_type = Column(String)  # "Ceramic", "Porcelain"
    tile_cost_per_sqft = Column(Float)
    tiling_area = Column(Float)
    total_tile_cost = Column(Float)
    total_flooring_cost = Column(Float)
    total_remodel_cost = Column(Float)
    total_supply_cost = Column(Float)

    def __init__(self, name, surface_area, flooring_type, is_tiling_needed, tile_type, tiling_area):
        self.name = name
        self.surface_area = float(surface_area)
        self.flooring_type = flooring_type
        self.flooring_cost_per_sqft = self.match_flooring_cost_per_sqft()
        self.is_tiling_needed = is_tiling_needed

        if self.is_tiling_needed:
            self.tile_type = tile_type
            self.tile_cost_per_sqft = self.match_tiling_cost_per_sqft()
            self.tiling_area = float(tiling_area) if is_tiling_needed else 0.0  # Handle tiling correctly
            self.total_tile_cost = self.calc_total_tile_cost()

        self.total_flooring_cost = self.calc_flooring_cost()
        self.total_remodel_cost = self.calc_total_remodel_cost()

    def match_flooring_cost_per_sqft(self):
        price = 0

        match self.flooring_type:
            case 'stone':
                price = 20.00
            case 'hardwood':
                price = 15.00
            case 'laminate':
                price = 4.00
            case 'linoleum':
                price = 8.00
            case 'vinyl':
                price = 4.00
            case _:
                price = 0.00

        return price

    def match_tiling_cost_per_sqft(self):
        price = 0

        match self.tile_type:
            case 'stone':
                price = 13.00
            case 'ceramic':
                price = 19.00
            case 'porcelain':
                price = 15.00
            case 'glass':
                price = 35.00
            case 'metal':
                price = 45.00
            case _:
                price = 0.00

        return price

    def calc_total_tile_cost(self):
        total_tile_cost = self.tiling_area * self.tile_cost_per_sqft

        return total_tile_cost

    def calc_flooring_cost(self):
        if self.is_tiling_needed:
            total_flooring_cost = (self.surface_area - self.tiling_area) * self.flooring_cost_per_sqft
        else:
            total_flooring_cost = self.surface_area * self.flooring_cost_per_sqft

        return total_flooring_cost

    def calc_total_remodel_cost(self):
        if self.is_tiling_needed:
            total_remodel_cost = self.total_tile_cost + self.total_flooring_cost
        else:
            total_remodel_cost = self.total_flooring_cost

        return total_remodel_cost


    def add_supply_cost(self, supply_cost):
        self.total_remodel_cost += supply_cost



    def __repr__(self):
        return (f"ID: {self.id}\n"
                f"Name: {self.name}\n"
                f"Surface Area: {self.surface_area:,.2f}\n"
                f"Flooring Type: {self.flooring_type}\n"
                f"Flooring Cost Per Sq Ft: ${self.flooring_cost_per_sqft:,.2f}")

class Supply(Base):
    __tablename__ = 'supplies'

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    name = Column(String)
    quantity = Column(Integer)
    cost_per_item = Column(Float)
    total_supply_cost = Column(Float)

    def __init__(self, name, quantity, cost_per_item):
        self.name = name
        self.quantity = quantity
        self.cost_per_item = cost_per_item
        self.total_supply_cost = self.calc_total_supply_cost()

    def calc_total_supply_cost(self):
       return self.quantity * self.cost_per_item

    room = relationship("Room")

# Uses models and create the tables
Base.metadata.create_all(engine)
