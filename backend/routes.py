from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"Message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return data, 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:pic_id>", methods=["GET"])
def get_picture_by_id(pic_id):
    for picture in data:
        if picture["id"] == pic_id:
            return picture, 200
    return {"Message": "Picture not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    for picture in data:
        if request.json["id"] == picture["id"]:
            return {"Message": f"picture with id {request.json['id']} already present"}, 302
    data.append(request.json)
    return request.json, 201


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:pic_id>", methods=["PUT"])
def update_picture(pic_id):
    if pic_id:
        for index, picture in enumerate(data):
            if picture["id"] == request.json["id"]:
                data[index] = request.json
                return picture, 201
        return {"Message": "picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:pic_id>", methods=["DELETE"])
def delete_picture(pic_id):
    for picture in data:
        if picture["id"] == pic_id:
            data.remove(picture)
            return "", 204
    return {"Message": "picture not found"}, 404
