#!/usr/bin/env python

from flask import Blueprint
main = Blueprint('main', __name__)
import views
import index
import qassert
import project
import pojmanager