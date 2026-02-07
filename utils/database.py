from flask_sqlalchemy import SQLAlchemy
from extensions import db


def init_db(app):
    """Initialize database with app context"""
    db.init_app(app)

    # Create tables
    with app.app_context():
        db.create_all()

    return db


def get_or_create(model, **kwargs):
    """Get or create a database record"""
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance, True


def bulk_create(model, data_list):
    """Bulk create records"""
    instances = [model(**data) for data in data_list]
    db.session.bulk_save_objects(instances)
    db.session.commit()
    return instances


def paginate_query(query, page=1, per_page=20):
    """Paginate SQLAlchemy query"""
    return query.paginate(page=page, per_page=per_page, error_out=False)