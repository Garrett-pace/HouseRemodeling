import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from sqlalchemy import update
from models.model import *
import seaborn as sns
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.secret_key = "stdyfugihjfhgfyu"
ss = SS()

@app.route("/")
def index():
    room_names = [room.name for room in ss.query(Room).all()]
    remodel_costs = [room.total_remodel_cost for room in ss.query(Room).all()]
    plt.figure(figsize=(10, 6))
    sns.barplot(x=room_names, y=remodel_costs, palette="viridis")
    plt.title("Total Remodeling Cost per Room")
    plt.xlabel("Room")
    plt.ylabel("Total Remodel Cost ($)")

    img_path = os.path.join(app.root_path, "static", "plot.png")
    plt.savefig(img_path)
    plt.close()
    return render_template('index.html', All_Rooms=get_all_rooms_being_Remodeled(),
                           plot_url=url_for('static', filename='plot.png'))

@app.route("/supply_details", methods=['GET', 'POST'])
def supply_details():
    if request.method == 'POST':
        supply_name = request.form['supply_name']
        All_supplies = Get_all_supplies()

        for supply in All_supplies:
            if supply.name == supply_name:
                Supply_details = Get_supply_by_name(supply_name)
                return render_template('supply_details.html', Supply_details=Supply_details)
    return render_template("supply_details.html")

@app.route("/room_details", methods=['GET', 'POST'])
def room_details():
    if request.method == 'POST':
        session['room_name'] = request.form['name']
        print(session['room_name'])
        All_rooms = Get_all_rooms()

        for room in All_rooms:
            print(room.name + session['room_name'])
            if room.name == session['room_name']:
                session['roomID'] = room.id
                RoomDetails = Get_Room_by_name(session['room_name'])
                return render_template('room_details.html', RoomDetails=RoomDetails)
    return render_template('room_details.html')


@app.route("/edit_room", methods=['GET', 'POST'])
def edit_room():
    if request.method == 'POST':
        name = request.form['name']
        surface_area = request.form['surface_area']
        flooring_type = request.form['flooring_type']
        is_tiling_needed = request.form['is_tiling_needed']
        tiling_area = request.form['tiling_area']
        tile_type = request.form['tile_type']
        print(session['roomID'])
        stmt = update(Room).where(Room.id == session['roomID']).values(
            name=name,
            surface_area=surface_area,
            flooring_type=flooring_type,
            is_tiling_needed=is_tiling_needed,
            tiling_area=tiling_area,
            tile_type=tile_type
        )

        # Execute the statement
        ss.execute(stmt)
        ss.commit()
        ss.close()

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

def Get_supply_by_name(supply_name):
    return ss.query(Supply).filter(Supply.name == supply_name).first()

def Get_all_supplies():
    return ss.query(Supply).all()

def Get_all_rooms():
    return ss.query(Room).all()

def Get_supply_where_supply_id_equals_room_id(room_id):
    return ss.query(Supply).filter(Supply.id == room_id).all()

def Get_Room_by_name(room_name):
    return ss.query(Room).filter(Room.name == room_name).first()

def get_all_rooms_being_Remodeled():
    return ss.query(Room).filter(Room.is_tiling_needed == True).all()


if __name__ == "__main__":
    app.run(debug=True)