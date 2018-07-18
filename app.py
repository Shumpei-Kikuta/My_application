from flask import Flask,render_template,request,session, redirect, make_response,url_for
import psycopg2
import psycopg2.extras
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, UserMixin,logout_user,current_user

app=Flask(__name__)
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ufawifyagwer1742yncs1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/diary'
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User_table.query.get(id)


#モデルの定義エリア
class User_table(UserMixin,db.Model):
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
    if current_user.is_authenticated:
        all_past_post = Diary_table.query.filter(Diary_table.id == current_user.id)
        return render_template("home.html",all_past_post = all_past_post)
    else:
        return render_template("home.html")

#rooting of sign_in and sign_up
@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    is_already_used_username = User_table.query.filter(User_table.username==username).first()
    if not is_already_used_username:
        newUser = User_table(username=username,password=password)
        db.session.add(newUser)
        db.session.commit()
        login_user(newUser,True) # ユーザが新規登録されたときは，ログイン状態にする．
        return redirect("/")

    else: # すでにユーザーネームが使われている場合
        already = True
        return render_template("/sign_up.html",already=already)


@app.route("/sign_in")
def sign_in():
    return render_template("sign_in.html")

@app.route("/login",methods=["POST"])
def log_in():
    if request.form["username"] and request.form["password"]:
        posted_username = request.form["username"]

        user_in_database = User_table.query.filter_by(username=posted_username).first()
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
    if current_user.is_authenticated:
        return render_template("posting_page.html")
    else:
        return redirect("/")

# end post rooting

# rooting of past posted
@app.route("/posted_page",methods=["POST"])
def post_page():
    title = request.form["title"]
    contents = request.form["contents"]
    file = request.files["image"]
    file_path = "static/post_img/" + secure_filename(file.filename)
    file.save(file_path)
    new_page = Diary_table(id=current_user.id,title=title, contents=contents,file_path=file_path)
    db.session.add(new_page)
    db.session.commit()
    return redirect("/")

@app.route("/detailed_past_post/<int:diary_id>")
def detailed_past_post(diary_id):
    page = Diary_table.query.filter(Diary_table.diary_id == diary_id).first()
    return render_template("detailed_page.html",page=page)


# the end of past posted

#DBのコマンド
@app.cli.command("initdb")
def initdb_command():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
