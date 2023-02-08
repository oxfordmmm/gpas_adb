"""
The models that represent the database objects
"""
import enum
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

Base = declarative_base()
metadata = Base.metadata

SAMPLE_FIELDS = (
    "run_accession,instrument_platform,read_count,fastq_md5,"
    "fastq_ftp,collection_date,host,country"
)
SAMPLE_RESULT = "read_run"
SAMPLE_LIMIT = 0
SAMPLE_FORMAT = "tsv"
SAMPLE_DOWNLOAD = "true"


class SampleStatus(enum.Enum):
    """
    Enum of the status for the samples.

    UNPROCESSED - The files have not been downloaded yet and the metadata
    has not been checked

    DOWNLOADED - The files have been downloaded and the metadata has been
    checked

    ERROR - Any error occured either during the download of the data or the
    checking of the metadata
    """

    UNPROCESSED = 1
    DOWNLOADED = 2
    ERROR = 3


class Project(Base):
    """
    Holds the details of the projects from which we wish to download samples
    """

    __tablename__ = "projects"

    accession = Column(String(20), nullable=False, primary_key=True)
    name = Column(String(255))
    samples = relationship("Sample", backref="project")

    def __init__(self, accession: str, name: str = None) -> None:
        self.accession = accession
        self.name = name


class Sample(Base):
    """
    Holds the details of the samples, metadata from the ENA and the JSON
    to pass to APEX
    """

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
    status = Column(Enum(SampleStatus), server_default="UNPROCESSED")
    error_text = Column(Text)

    def __init__(
        self,
        accession: str,
        project: Project,
        instrument_platform: str,
        read_count: int,
        fastq_md5: str,
        fastq_ftp: str,
        collection_date: Date,
        host: str,
        country: str,
        json_metadata: str,
        error_text: str,
        status: SampleStatus = SampleStatus.UNPROCESSED,
    ):
        self.accession = accession
        self.project = project
        self.instrument_platform = instrument_platform
        self.read_count = read_count
        self.fastq_md5 = fastq_md5
        self.fastq_ftp = fastq_ftp
        self.collection_date = collection_date
        self.host = host
        self.country = country
        self.json_metadata = json_metadata
        self.status = status
        self.error_text = error_text


sample_view = Table("sample_view", MetaData())
sample_view_sql = text(
    """
    select accession
    from samples
    where status = 'UNPROCESSED'
    order by collection_date desc
    fetch first 10 rows only
    """
)
CreateView(sample_view, sample_view_sql)
