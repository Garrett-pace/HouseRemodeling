import os
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship


# Get the current directory of the script
basedir = os.path.abspath(os.path.dirname(__file__))

# Modify the path to store the database inside a folder named 'database'
database_path = os.path.join(basedir, 'database', 'remodels.db')

# Ensure the 'database' folder exists
os.makedirs(os.path.dirname(database_path), exist_ok=True)

engine = create_engine('sqlite:///remodels.db')
Session = sessionmaker(bind=engine)


Base = declarative_base()

# Uses models and create the tables
Base.metadata.create_all(engine)


class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surface_area = Column(Float)
    flooring_type = Column(String)
    flooring_cost_per_sqft = Column(Float)

    # New Fields
    is_tiling_needed = Column(String) # boolean
    tile_type = Column(String) # "Ceramic", "Porcelain"
    tile_cost_per_sqft = Column(Float)
    tiling_area = Column(Float)
    total_tile_cost = Column(Float)
    total_flooring_cost = Column(Float)
    total_remodel_cost = Column(Float)
    total_supply_cost = Column(Float)

    def calc_total_tile_cost(self):
        self.total_tile_cost = self.tiling_area * self.tile_cost_per_sqft

    def calc_flooring_cost(self):
        self.total_flooring_cost = self.surface_area * self.flooring_cost_per_sqft

    def calc_total_remodel_cost(self):
        self.total_remodel_cost = self.total_tile_cost + self.total_flooring_cost + self.total_supply_cost

    supply = relationship("Supply")

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

    def calc_total_supply_cost(self):
        self.total_supply_cost = self.quantity * self.cost_per_item

    room = relationship("Room")

    def __repr__(self):
        return (f"ID: {self.id}\n"
                f"Room_ID: {self.room_id}\n"
                f"Name: {self.name}\n"
                f"Quantity: {self.quantity}\n"
                f"Cost Per Item: {self.cost_per_item}\n"
                f"Total Supply Cost: {self.total_supply_cost:,.2f}")
