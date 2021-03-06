import json
from datetime import datetime

from ckan import model
from ckan.common import config
from ckan.model import meta, package_table, domain_object
from ckan.model import types as _types
from sqlalchemy import orm, types, Column, Table, ForeignKey, or_, and_, text, Integer, String, inspect, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from ckan.model.user import User
import ckan.plugins.toolkit as tk
# Session = sessionmaker(bind=engine)
from ckanext.servicehub.model.BaseModel import Base


class Call(Base):
    __tablename__ = 'app_call'

    call_id = Column(types.UnicodeText,
                     primary_key=True,
                     default=_types.make_uuid)
    app_id = Column(types.UnicodeText, ForeignKey('app_info.app_id', onupdate="CASCADE", ondelete="CASCADE"))
    user_id = Column(types.UnicodeText)
    # container_id = Column(types.UnicodeText)
    call_status = Column(types.UnicodeText)
    logs = Column(types.UnicodeText)
    elapsed_seconds = Column(types.BIGINT)
    # output = Column(types.UnicodeText)
    created_at = Column(DateTime(timezone=True),default=func.now())

    def __init__(self, user_id, app_id, call_status="PENDING"):
        self.call_id = _types.make_uuid()
        self.user_id = user_id
        self.app_id = app_id
        self.call_status = call_status
        # self.container_id = container_id
        # self.create_at=datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def setOption(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class App(Base):
    __tablename__ = 'app_info'

    app_id = Column(types.UnicodeText,
                    primary_key=True,
                    default=_types.make_uuid)
    app_name = Column(types.UnicodeText)
    avatar_path = Column(types.UnicodeText)
    type = Column(types.UnicodeText)
    slug_name = Column(types.UnicodeText, unique=True)
    code_path = Column(types.UnicodeText)  # optional batch
    image = Column(types.UnicodeText)
    image_id = Column(types.UnicodeText)
    owner = Column(types.UnicodeText)
    organization = Column(types.UnicodeText)  # optional both
    description = Column(types.UnicodeText,default='No description')
    language = Column(types.UnicodeText)  # optional batch
    created_at = Column(DateTime(timezone=True),default=func.now())# optional both
    sys_status = Column(types.UnicodeText)  # optional both
    app_status = Column(types.UnicodeText)  # optional both

    def __init__(self, app_name, slug_name, image, owner, description, app_status="PENDING", sys_status="PENDING"):
        self.app_id = _types.make_uuid()
        self.app_name = app_name
        self.slug_name = slug_name
        self.image = image
        self.app_status = app_status
        self.description = description
        self.owner = owner
        self.sys_status = sys_status
        self.created_at = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def setOption(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def strftime(self):
        self.created_at = self.created_at.strftime("%d-%m-%Y %H:%M:%S")

    def as_dict(self):
        _dict = {c.key: getattr(self, c.key)
                 for c in inspect(self).mapper.column_attrs}
        _dict['dataset_related'] = [dataset.as_dict() for dataset in meta.Session.query(AppRelatedDataset).filter(
            AppRelatedDataset.app_id == self.app_id).all()]
        _dict['category'] = [tag.as_dict() for tag in
                             meta.Session.query(AppCategory).filter(AppCategory.app_id == self.app_id).all()]
        return _dict


class AppParam(Base):
    __tablename__ = 'app_param'

    app_id = Column(ForeignKey('app_info.app_id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    name = Column(types.UnicodeText, primary_key=True)
    type = Column(types.UnicodeText)
    label = Column(types.UnicodeText)
    description = Column(types.UnicodeText)


class CallInput(Base):
    __tablename__ = 'call_input'

    call_id = Column(ForeignKey('app_call.call_id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    name = Column(types.UnicodeText, primary_key=True)
    type = Column(types.UnicodeText)
    value = Column(types.UnicodeText)


class CallOutput(Base):
    __tablename__ = 'call_output'

    call_id = Column(ForeignKey('app_call.call_id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    name = Column(types.UnicodeText, primary_key=True)
    type = Column(types.UnicodeText)
    value = Column(types.UnicodeText)


class AppCategory(Base):
    __tablename__ = 'app_category'
    id = Column(types.UnicodeText,
                primary_key=True,
                default=_types.make_uuid)
    app_id = Column(types.UnicodeText, ForeignKey('app_info.app_id', onupdate="CASCADE", ondelete="CASCADE"))
    tag_name = Column(types.UnicodeText)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def setOption(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def as_dict(self):
        _dict = {c.key: getattr(self, c.key)
                 for c in inspect(self).mapper.column_attrs}
        return _dict


class AppRelatedDataset(Base):
    __tablename__ = 'app_related_dataset'
    id = Column(types.UnicodeText,
                primary_key=True,
                default=_types.make_uuid)
    app_id = Column(types.UnicodeText, ForeignKey('app_info.app_id', onupdate="CASCADE", ondelete="CASCADE"))
    package_id = Column(types.UnicodeText,
                        ForeignKey(package_table.columns['id'], onupdate="CASCADE", ondelete="CASCADE"))

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def setOption(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def as_dict(self):
        # _dict = {c.key: getattr(self, c.key)
        #          for c in inspect(self).mapper.column_attrs}
        # del _dict['package_id']
        return dict(app_id=self.app_id,package_name=model.Package.get(self.package_id).name)


from ckanext.servicehub.model.BaseModel import Base, engine
Base.metadata.create_all(engine)
