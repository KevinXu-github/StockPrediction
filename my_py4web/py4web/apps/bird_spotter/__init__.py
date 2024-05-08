# check compatibility
import py4web

assert py4web.check_compatible("0.1.20190709.1")

# by importing db you expose it to the _dashboard/dbadmin
from .models import db

# by importing controllers you expose the actions defined in it
from . import controllers

# optional parameters
__version__ = "0.0.0"
__author__ = "you <you@example.com>"
__license__ = "anything you want"


# from py4web import action, request, abort, redirect, URL
# from yatl.helpers import A
# from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash


# @action("index")
# def index():
#     return "hello world"
# @action('testInit')
# def test():
#     return "Test testInit"

# # @action('api/birds', method='GET')
# # def get_birds():
# #     return {"birds": "test birds"}
# # get endpoint
# #db
# @action('api/birds', method='GET')
# @action.uses(db)
# def get_birds():
#     # return "flag"
#     rows = db(db.bird).select(db.bird.ALL)
#     return {"birds": rows.as_list()}