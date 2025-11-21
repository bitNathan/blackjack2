from flask import Blueprint, request, jsonify

api_bp = Blueprint("api", __name__)

@api_bp.get("/")
def root():
    return "Hello World"

