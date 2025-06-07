from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for,request  # noqa; F401

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

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data)
    

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    res = list(filter(lambda x:x["id"]==id,data))
    if len(res)>0 :
        return res[0]
    else :
        return "bad",404
    


################ictRE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    pic = request.get_json()
    res = list(filter(lambda x:x["id"]==pic["id"],data))
    if len(res)>0 :
        return {"Message": f"picture with id {pic['id']} already present"},302
    else :
        data.append(pic)
        return pic,201
   
######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    pic = request.get_json()
    res = list(filter(lambda x:x["id"] == id,data))
    if len(res)==0 :
        return {"Message": "picture not found"},404
    else :
        index = data.index(res[0])
        data[index]=pic
        return pic,200
   

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    res = list(filter(lambda x:x["id"]==id,data))
    if len(res)==0 :
        return {"Message": "picture not found"},404
    else :
        index = data.index(res[0])
        data.pop(index)
        return {},204
