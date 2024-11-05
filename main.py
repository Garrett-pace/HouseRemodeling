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

        for supply in All_supplies:
            if supply.name == supply_name:
                Supply_details = Get_supply_by_name(supply_name)
                return redirect(url_for('supply_details', Supply_details=Supply_details))
            else:
                flash("This Supply does not exist")
                return redirect(url_for('supply_details'))
    return render_template("supply_details.html")


def Get_supply_by_name(supply_name):
    return session.query(Supply).filter(Supply.name == supply_name).all()

def Get_all_supplies():
    return session.query(Supply).all()

@app.route("/add_supply", methods=['GET', 'POST'])
def add_supply():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        cost = float(request.form['cost'])

        if name == "":
            flash("Please enter your name")
            return redirect(url_for('add_supply'))
        elif quantity <= 0:
            flash("Please enter your quantity")
            return redirect(url_for('add_supply'))
        elif cost <= 0:
            flash("Please enter your cost")
            return redirect(url_for('add_supply'))
        else:
            supply=Supply(name, quantity, cost)
            session.add(supply)
            session.commit()
            session.refresh(supply)
            session.close()

            flash("Your supply has been added")
            return redirect(url_for('add_supply'))
    return render_template('add_supply.html')

@app.route('/add_room', methods=['GET', 'POST'])
def add_room():
    if request.method == 'POST':
        name = request.form['name']
        surface_area = float(request.form['surface_area'])
        flooring_type = request.form['flooring_type']

        # Use .get() to avoid KeyError if the checkbox is not checked
        is_tiling_needed = request.form.get('is_tiling_needed') == 'on'

        tiling_area = 0.0
        tile_type = ""

        if is_tiling_needed:
            tiling_area = float(request.form['tiling_area'])
            tile_type = request.form['tile_type']

        if tiling_area > surface_area:
            flash("Tiling area cannot be larger than total surface area.")
            return redirect(url_for('add_room'))

        room = Room(name, surface_area, flooring_type, is_tiling_needed, tile_type, tiling_area)
        session.add(room)
        session.commit()
        session.refresh(room)
        session.close()
        flash("Room has been added.")
        return redirect(url_for('add_room'))

    return render_template("add_room.html")

if __name__ == "__main__":
    app.run(debug=True)