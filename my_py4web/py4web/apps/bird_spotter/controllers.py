"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""
import logging
from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash

# @action("index")
# def index():
#     return "hello world"


# @action("index")
# @action.uses("index.html", auth, T)
# def index():
#     user = auth.get_user()
#     message = T("Hello {first_name}").format(**user) if user else T("Hello")
#     return dict(message=message)

@action("index")
def index():
    redirect(URL("static/index.html"))


@action('birds', method = ['GET', 'POST'])
@action.uses(db)
def read_bird():
    if request.method == 'GET':
        return dict(birds = db(db.bird).select())
    elif request.method == 'POST':
        logging.debug(request.json)
        bird = db.bird.validate_and_insert(name = request.json.get('name'))
        return dict(bird = bird)    

@action('birds/<bird_id>', method = ['PUT', 'DELETE'])
@action.uses(db)
def change_bird(bird_id):
    if request.method == 'PUT':
        db(db.bird.id == bird_id).validate_and_update(habitat = request.json.get('habitat'), weight = request.json.get('weight'), sightings = request.json.get('sightings'))
        return dict()
    elif request.method == 'DELETE':
        del db.bird[bird_id]
        return dict()


@action('birds/<bird_id>/increase_sightings', method = 'POST')
@action.uses(db)
def increase_sightings(bird_id):
    bird = db.bird[bird_id]
    bird.update_record(sightings = bird.sightings + 1)
    return dict(sightings = bird.sightings)