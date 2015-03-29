# -*- coding: utf-8 -*-
"""
    fiddlersgreen.core
    ~~~~~~~~~~~~~~~~~

    Core modules contains basic classes that all
    applications depend on

"""
from .compat import basestring


# Create instances of all extensions
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask.ext.migrate import Migrate
migrate = Migrate()

from flask.ext.login import LoginManager
login_manager = LoginManager()


class CRUDMixin(object):
    """
    Mixin that adds convenience methods for CRUD (create, read, update, delete)
    operations.
    """

    @classmethod
    def _preprocess_params(cls, kwargs):
        """Returns a preprocessed dictionary of parameters. Used by default
        before creating a new instance or updating an existing instance.

        :param kwargs: a dictionary of parameters
        """
        for k in kwargs.keys():
            if not hasattr(cls, k):
                kwargs.pop(k, None)
        kwargs.pop('csrf_token', None)
        return kwargs

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls.new(**kwargs)
        return instance.save()

    @classmethod
    def new(cls, **kwargs):
        """Create a new, unsaved record"""
        return cls(**cls._preprocess_params(kwargs))

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in self._preprocess_params(kwargs).items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' colum named
    ``id`` to any declarative-mapped class.
    """
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, id):
        if any(
                (isinstance(id, basestring) and id.isdigit(),
                    isinstance(id, (int, float))),
        ):
            return cls.query.get(int(id))
        return None


class Model(CRUDMixin, SurrogatePK, db.Model):
    """Base model class that includes CRUD convenience methods."""
    __abstract__ = True


def ReferenceCol(tablename, nullable=False, pk_name='id', **kwargs):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = ReferenceCol('category')
        category = relationship('Category', backref='categories')
    """
    return db.Column(
        db.ForeignKey('{0}.{1}'.format(tablename, pk_name)),
        nullable=nullable, **kwargs)
