import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models.model import *
from sqlalchemy import delete

import seaborn as sns
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.secret_key = "stdyfugihjfhgfyu"
ss = SS()
@app.route("/")
def index():
    return render_template('index.html', All_Rooms = get_all_rooms_being_Remodeled() )

@app.route("/supply_details", methods=['GET', 'POST'])
def supply_details():
    if request.method == 'POST':
        supply_name = request.form['supply_name']
        All_supplies = Get_all_supplies()

        for supply in All_supplies:
            if supply.name == supply_name:
                Supply_details = Get_supply_by_name(supply_name)
                return render_template('supply_details.html', Supply_details=Supply_details)
            else:
                flash("This Supply does not exist")
                return redirect(url_for('supply_details'))
    return render_template("supply_details.html")

@app.route("/room_details", methods=['GET', 'POST'])
def room_details():
    if request.method == 'POST':
        session['room_name'] = request.form['name']
        All_rooms = Get_all_rooms()

        for room in All_rooms:
            if room.name == session['room_name']:
                RoomDetails = Get_Room_by_name(session['room_name'])
                return render_template('room_details.html', RoomDetails=RoomDetails)
            else:
                flash("This Supply does not exist")
                return redirect(url_for('room_details'))
    return render_template('room_details.html')


@app.route("/edit_room", methods=['GET', 'POST'])
def edit_room():
    return render_template('edit_room.html', RoomDetails=Get_Room_by_name(session['room_name']))


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
            supply = Supply(name, quantity, cost)
            ss.add(supply)
            ss.commit()
            ss.close()

            flash("Your supply has been added")
            return redirect(url_for('add_supply'))
    return render_template('add_supply.html')

@app.route('/add_room', methods=['GET', 'POST'])
def add_room():
    if request.method == 'POST':
        name = request.form['name']
        surface_area = request.form['surface_area']
        flooring_type = request.form['flooring_type']

    return render_template("add_room.html")

def Get_supply_by_name(supply_name):
    return ss.query(Supply).filter(Supply.name == supply_name).all()

def Get_all_supplies():
    return ss.query(Supply).all()

def Get_all_rooms():
    return ss.query(Room).all()

def Get_supply_where_supply_id_equals_room_id(room_id):
    return ss.query(Supply).filter(Supply.id == room_id).all()

def Get_Room_by_name(room_name):
    return ss.query(Room).filter(Room.name == room_name).all()

def delete_item():
    return delete(Room).where(Room.name == session['room_name'])
def get_all_rooms_being_Remodeled():
    return ss.query(Room).filter(Room.is_tiling_needed == 'y').all()


if __name__ == "__main__":
    app.run(debug=True)