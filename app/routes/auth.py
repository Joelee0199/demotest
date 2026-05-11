from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user

from app.extensions import db
from app.models import User
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            flash("邮箱和密码不能为空。", "error")
            return render_template("register.html"), 400

        if len(password) < 6:
            flash("密码长度不能少于 6 个字符。", "error")
            return render_template("register.html"), 400

        if User.query.filter_by(email=email).first():
            flash("该邮箱已被注册。", "error")
            return render_template("register.html"), 400

        user = User(
            email=email,
            password_hash=generate_password_hash(password, method="pbkdf2:sha256"),
        )
        db.session.add(user)
        db.session.commit()

        flash("注册成功，请登录。", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash("邮箱或密码错误。", "error")
            return render_template("login.html"), 401

        login_user(user)
        flash("登录成功。", "success")
        return redirect(url_for("posts.index"))

    return render_template("login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    flash("已退出登录。", "success")
    return redirect(url_for("posts.index"))
