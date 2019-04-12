from flask import Blueprint, request, redirect, render_template, session, escape, url_for, flash
from app import db

from blog.blog.models import User, Post, Published_Post, Term, Term_Taxonomy, Term_Taxonomy_Relationship

admin_mod = Blueprint('admin', __name__, url_prefix = "/admin", template_folder="templates\\admin\\examples", static_folder="static")

@admin_mod.route('/')
def admin():
    return  render_template('dashboard.html')