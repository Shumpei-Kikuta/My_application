from flask import Flask,render_template,request,session, redirect, make_response,url_for
import psycopg2
import psycopg2.extras
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, UserMixin,logout_user,current_user

app=Flask(__name__)
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/diary'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ufawifyagwer1742yncs1'
db = SQLAlchemy(app)
migrate = Migrate(app,db)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


#モデルの定義エリア
class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True)
    password = db.Column(db.String(20))

class Diary_table(db.Model):
    id = db.Column(db.Integer,primary_key=False)
    diary_id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(40))
    contents = db.Column(db.String(400))
    file_path = db.Column(db.String(100))

#ルーティングエリア
@app.route("/")
def home():
    all_past_post = Diary_table.query.filter(Diary_table.id == 1)
    return render_template("home.html",all_past_post = all_past_post)

#rooting of sign_in and sign_up
@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")

@app.route("/register", methods=["POST"])
def register():
    if request.form["username"] and request.form["password"]:
        username = request.form["username"]
        password = request.form["password"]
        newUser = User(username=username,password=password)
        db.session.add(newUser)
        db.session.commit()
        login_user(newUser,True) # ユーザが新規登録されたときは，ログイン状態にする．
        return redirect("/")
    else:
        return "エラーです"

@app.route("/sign_in")
def sign_in():
    return render_template("sign_in.html")

@app.route("/login",methods=["POST"])
def log_in():
    if request.form["username"] and request.form["password"]:
        posted_username = request.form["username"]

        user_in_database = User.query.filter_by(username=posted_username).first()
        if user_in_database and request.form["password"] == user_in_database.password: # 入力されたpasswordが正しい場合
            login_user(user_in_database,True)
            return redirect("/")
        else:
            return "エラーが発生しました．"
    else:
        return "エラーが発生しました．"

@app.route("/logout")
def log_out():
    logout_user()
    return redirect("/")

# end sign_in or sign_up rooting

# rooting of post
@app.route("/posting_page")
def top_page():
    return render_template("posting_page.html")

@app.route("/posted_page",methods=["POST"])
def post_page():
    title = request.form["title"]
    contents = request.form["contents"]
    file = request.files["image"]
    file_path = "post_img/" + secure_filename(file.filename)
    file.save(file_path)
    #　dbのインスタンスを作成
    # とりえあず
    # idをみんな1にしておく
    new_page = Diary_table(id=1,title=title, contents=contents,file_path=file_path)
    # dbにインスタンスを挿入
    db.session.add(new_page)
    db.session.commit()
    return redirect("/")
# end post rooting

#DBのコマンド
@app.cli.command("initdb")
def initdb_command():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8088)
