from flask import g
import sqlite3

def get_db(database):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database)
    return db
    
def execute_db(query, database, args=(), one=False):
    db = get_db(database)
    cur = db.execute(query, args)
    db.commit()
    cur.close()
    
def query_db(query, database, args=(), one=False):
    cur = get_db(database).execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def __init_db__(database, schema, app):
    with app.app_context():
        db = get_db(database)
        with app.open_resource(schema, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
