import os
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from models.model import *
import seaborn as sns
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.secret_key = "RunCurrentFile"

if __name__ == "__main__":
    app.run(debug=True)