"""
This file defines the database models
"""

from .common import db, Field
from pydal.validators import *

## Define your table below
    # Field('id', 'integer', primary_key=True, autoincrement=True),
db.define_table('bird',
    Field('name', 'string', unique=True, requires=IS_NOT_EMPTY()), 
    Field('habitat', 'string', default=''), 
    Field('weight', 'integer', default=0),
    Field('sightings', 'integer', default=0)
    )

# always commit your models to avoid problems later

db.commit()
