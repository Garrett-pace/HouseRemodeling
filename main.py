import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models.model import *
import seaborn as sns
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.secret_key = "stdyfugihjfhgfyu"
session = SS()
@app.route("/")
def index():
    return render_template('index.html', All_Rooms = get_all_rooms_being_Remodeled() )



def get_all_rooms_being_Remodeled():
    return session.query(Room).filter(Room.is_tiling_needed == 'y').all()

@app.route("/supply_details", methods=['GET', 'POST'])
def supply_details():
    if request.method == 'POST':
        supply_name = request.form['supply_name']
        All_supplies = Get_all_supplies()
        for x in All_supplies:
            if x.name != supply_name or supply_name == '':
                flash("This Supply does not exist")
            else:
                Supply_details = Get_supply_by_name(supply_name)
                return redirect(url_for('supply_details', Supply_details=Supply_details))
    return render_template("supply_details.html")


def Get_supply_by_name(supply_name):
    return session.query(Supply).filter(Supply.name == supply_name).all()

def Get_all_supplies():
    return session.query(Supply).all()

@app.route('/add_room', methods=['GET', 'POST'])
def add_room():
    if request.method == 'POST':
        name = request.form['name']
        surface_area = request.form['surface_area']
        flooring_type = request.form['flooring_type']

    return render_template("add_room.html")

if __name__ == "__main__":
    app.run(debug=True)