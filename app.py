from flask import Flask, render_template,request
import psycopg2.extras
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app=Flask(__name__)
