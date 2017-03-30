# coding: utf-8
"""
ZeroDB application example
"""
from flask import (Flask, render_template, redirect,
                   url_for, request, jsonify, abort, make_response)
from flask_bootstrap import Bootstrap
import models
from database import ZeroDBStorage
import json
app = Flask(__name__)
Bootstrap(app)


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


@app.route("/api/addPost", methods=["POST"])
def addPost():
    print (request.json)
    if 'title' not in request.json and 'content' not in request.json:
        abort(400)
    else:
        zero = ZeroDBStorage()
        print (request.json)
        if zero._create(post=request.json):
            return jsonify({'result': 'Add Post successful'})
        else:
            return jsonify({'result': 'Add Post error'})


@app.route("/api/delPost", methods=["POST"])
def delPost():
    if 'post_id' not in request.json:
        abort(400)
    else:
        zero = ZeroDBStorage()
        if zero._delete(post=request.json):
            return jsonify({'result': 'Deleted post successful'})
        else:
            return jsonify({'result': 'Deleted post error'})


@app.route("/api/getPosts", methods=['GET'])
def getPosts():
    zero = ZeroDBStorage()
    posts = zero._get()
    # result = json.
    return jsonify(posts)

@app.route("/")
def index():
    """
    Index Page
    """
    return render_template("index.html")


@app.route("/add")
def add_post(methods=["POST"]):
    """
    Add new post to database
    """
    return render_template("add.html")


if __name__ == '__main__':
    app.run(debug=True)
