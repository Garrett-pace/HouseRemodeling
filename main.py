import os
from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/add_room', methods=['GET', 'POST'])
def add_room():
    if request.method == 'POST':
        name = request.form['name']
        surface_area = request.form['surface_area']
        flooring_type = request.form['flooring_type']

    return render_template("add_room.html")

if __name__ == "__main__":
    app.run(debug=True)