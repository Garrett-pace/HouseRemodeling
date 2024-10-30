import os
from flask import Flask, render_template, request, redirect, url_for
from models.model import *
import seaborn as sns
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.secret_key = "stdyfugihjfhgfyu"
session = SS()
supply = Supply('drill', 300, 1.59)
supply_total = supply.calc_total_supply_cost()
room = Room('hi',149.54, "HardWood", 5,'y','Ceramic',5.43, 20, supply_total)
session.add(room)
session.commit()
session.close()
@app.route("/")
def index():
    return render_template('index.html', All_Rooms = get_all_rooms_being_Remodeled() )



def get_all_rooms_being_Remodeled():
    return session.query(Room).join(Supply).filter(Room.is_tiling_needed == 'y').all()

if __name__ == "__main__":
    app.run(debug=True)