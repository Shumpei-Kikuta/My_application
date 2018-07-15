from flask import Flask,render_template,request
import psycopg2
import psycopg2.extras
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/diary'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.secret_key = 'ufawifyagwer1742yncs2'
db = SQLAlchemy(app)


#モデルの定義エリア
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True)
    password = db.Column(db.String(20))

class Diary_table(db.Model):
    id = db.Column(db.Integer,primary_key=False)
    diary_id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(40))
    contents = db.Column(db.String(400))


#ルーティングエリア
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/posting_page")
def top_page():
    return render_template("posting_page.html")

@app.route("/posted_page",methods=["POST"])
def post_page():
    title = request.form["title"]
    contents = request.form["contents"]
    #　dbのインスタンスを作成
    とりえあず
    idをみんな1にしておく
    new_page = Diary_table(id=1,title=title, contents=contents)
    # dbにインスタンスを挿入
    db.session.add(new_page)
    db.session.commit()
    return render_template("posted_page.html", title=title,contents=contents)


#DBのコマンド
@app.cli.command("initdb")
def initdb_command():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8088)
