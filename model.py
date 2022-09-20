from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, text, JSON, Unicode, ForeignKey, Identity
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata

class Site(Base):

    __tablename__ = 'SITES'

    id = Column(Integer, Identity(on_null=True), primary_key = True)
    name = Column(String(255), nullable = False)
    code = Column(String(255), nullable = False)
    URL = Column(String(1000), nullable = False)

class Site_URL_field(Base):
    
    __tablename__ = "SITE_URL_FIELDS"

    id = Column(Integer, Identity(on_null=True), primary_key = True)
    site_id = Column(Integer, ForeignKey('SITES.id'))
    Key = Column(String(20), nullable = False)
    value = Column(String(20), nullable = False)
    site = relationship("SITES", back_populates = "SITE_URL_FIELDS")

Site.site_URL_fields = relationship("SITE_URL_FIELDS", order_by = Site_URL_field.id, back_populates = "SITES")

