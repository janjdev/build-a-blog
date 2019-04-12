from flask import Blueprint, render_template

site = Blueprint('site', __name__, template_folder="templates\\site", static_folder="static")