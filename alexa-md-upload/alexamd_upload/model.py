import sqlite3
import flask
import alexamd_upload


def dict_factory(cursor, row):
    output = {}
    for idx, col in enumerate(cursor.description):
        output[col[0]] = row[idx]
    return output


def get_db():
    if not hasattr(flask.g, 'sqlite_db'):
        flask.g.sqlite_db = sqlite3.connect(
            alexamd_upload.app.config['DATABASE_FILENAME'])
        flask.g.sqlite_db.row_factory = dict_factory

        # Foreign keys have to be enabled per-connection.  This is an sqlite3
        # backwards compatibility thing.
        flask.g.sqlite_db.execute("PRAGMA foreign_keys = ON")

    return flask.g.sqlite_db


@alexamd_upload.app.teardown_appcontext
def close_db(error):
    if hasattr(flask.g, 'sqlite_db'):
        flask.g.sqlite_db.commit()
        flask.g.sqlite_db.close()
