from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
    ForeignKey,
    Date,
    Enum,
    Table,
    MetaData,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text
from sqlalchemy_views import CreateView
import enum

Base = declarative_base()
metadata = Base.metadata

SAMPLE_FIELDS = "run_accession,instrument_platform,read_count,fastq_md5,fastq_ftp,collection_date,host,country"
SAMPLE_RESULT = "read_run"
SAMPLE_LIMIT = 0
SAMPLE_FORMAT = "tsv"
SAMPLE_DOWNLOAD = "true"


class Sample_Status(enum.Enum):
    available = 1
    downloaded = 2
    error = 3


class Project(Base):

    __tablename__ = "projects"

    accession = Column(String(20), nullable=False, primary_key=True)
    name = Column(String(255))


class Sample(Base):

    __tablename__ = "samples"

    accession = Column(String(20), nullable=False, primary_key=True)
    project_acession = Column(String(20), ForeignKey("projects.accession"))
    instrument_platform = Column(String(30), nullable=False)
    read_count = Column(Integer)
    fastq_md5 = Column(String(255))
    fastq_ftp = Column(String(255))
    collection_date = Column(Date)
    host = Column(String(255))
    country = Column(String(30))
    json_metadata = Column(Text)
    status = Column(Enum(Sample_Status), server_default="available")
    error_text = Column(Text)
    project = relationship("projects", back_populates="samples")


Project.samples = relationship(
    "samples", order_by=Sample.accession, back_populates="projects"
)

sample_view = Table("sample_view", MetaData())
sample_view_sql = text(
    """select accession 
                       from samples 
                       where status = 'available'
                       order by collection_date desc
                       fetch first 10 rows only
                       """
)
CreateView(sample_view, sample_view_sql)
