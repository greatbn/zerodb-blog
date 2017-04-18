# coding: utf-8
"""
ZeroDB application example
"""
from flask import (Flask, render_template, redirect,
                   url_for, request, jsonify, abort, make_response, flash)
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import models
from database import ZeroDBStorage
import json
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
Bootstrap(app)
csrf = CSRFProtect(app)
app.config["SECRET_KEY"] = "oanh123"

class PageDownEditor(Form):
    title = StringField("title", validators=[DataRequired()])
    text = TextAreaField("text", validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def not_found(error):
    """
    404 Error
    """
    return make_response(jsonify({"error": "Not Found"}))


@app.errorhandler(400)
def error_in_data(error):
    """
    400 Error
    """
    return make_response(jsonify({"error": "Your data not true"}))


@app.route("/")
def index():
    """
    Index Page
    """
    try:
        zero = ZeroDBStorage()
        posts = zero._get()
        return render_template("index.html", posts=posts)
    except Exception as e:
        flash('Cannot get posts in database: ' + str(e))
        return render_template("index.html", alert=error)


@app.route("/add", methods=["GET", "POST"])
def add_post():
    """
    Add new post to database
    """
    form = PageDownEditor()
    if form.validate_on_submit():
        title = form.title.data
        content = form.text.data
        post = {
            'title': title,
            'content': content
        }
        zero = ZeroDBStorage()
        if zero._create(post=post):
            return redirect('/')
        else:
            flash('Cannot add post')
            return render_template('editor.html', form=form)
    return render_template('editor.html', form=form)


@app.route("/post/id=<string:post_id>", methods=['GET', 'POST'])
def get_post(post_id):
    try:
        zero = ZeroDBStorage()
        post = zero._get(pid=post_id)
        return render_template("post.html", post=post[0])
    except Exception as e:
        flash('Cannot get the post with id: '+str(post_id))
        return redirect("/")


@app.route("/del/id=<string:post_id>", methods=['GET'])
def del_post(post_id):
    try:
        zero = ZeroDBStorage()
        result = zero._delete(post_id=post_id)
        if result:
            return redirect('/')
    except Exception as e:
        flash('Cannot delete this post: ' + str(e))
        return redirect(url_for("get_post", post_id=post_id))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
