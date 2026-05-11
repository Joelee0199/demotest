from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models import Post

posts_bp = Blueprint("posts", __name__)


@posts_bp.route("/")
def index():
    posts = (
        Post.query
        .filter_by(is_deleted=0)
        .order_by(Post.created_at.desc())
        .all()
    )
    return render_template("index.html", posts=posts)


@posts_bp.route("/post/<int:post_id>")
def detail(post_id):
    post = db.session.get(Post, post_id)
    if post is None or post.is_deleted:
        abort(404)
    return render_template("post_detail.html", post=post)


@posts_bp.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()

        if not title or not body:
            flash("标题和正文不能为空。", "error")
            return render_template("post_new.html"), 400

        post = Post(
            title=title,
            body=body,
            author_id=current_user.id,
        )
        db.session.add(post)
        db.session.commit()

        flash("文章发布成功！", "success")
        return redirect(url_for("posts.index"))

    return render_template("post_new.html")


@posts_bp.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = db.session.get(Post, post_id)
    if post is None or post.is_deleted:
        abort(404)

    if post.author_id != current_user.id:
        abort(403)

    post.is_deleted = 1
    db.session.commit()

    flash("文章已删除。", "success")
    return redirect(url_for("posts.index"))
