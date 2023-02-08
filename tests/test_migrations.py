from pytest_alembic.tests import test_single_head_revision  # noqa: F401
from pytest_alembic.tests import test_upgrade  # noqa: F401
from pytest_alembic.tests import test_model_definitions_match_ddl  # noqa: F401
from pytest_alembic.tests import test_up_down_consistency  # noqa: F401

from gpas_adb import Project, Sample, SampleStatus
import datetime


def test_insert_project(dbsession):
    projects = dbsession.query(Project)
    assert projects.count() == 0

    p1 = Project(accession='PRJNA631061', name='Quest Diagnostics')
    dbsession.add(p1)
    dbsession.commit()

    projects = dbsession.query(Project)
    assert projects.count() == 1
    project: Project = projects.one()
    assert project.accession == 'PRJNA631061'
    assert project.name == 'Quest Diagnostics'


def test_insert_sample(dbsession):
    p1 = Project(accession='PRJNA631061', name='Quest Diagnostics')
    dbsession.add(p1)
    dbsession.commit()

    s1 = Sample(
        accession="ERR12345",
        project=p1,
        instrument_platform="illumina",
        read_count=1000,
        fastq_md5="12fe4521",
        fastq_ftp="test.com/test.fastq",
        collection_date=datetime.date(2022, 5, 10),
        host="human",
        country="United Kingdom",
        json_metadata="{'test': 'test'}",
        status=SampleStatus.UNPROCESSED,
        error_text="Error"
    )

    dbsession.add(s1)
    dbsession.commit()

    samples = dbsession.query(Sample)
    assert samples.count() == 1
    sample: Sample = samples.one()
    assert sample.accession == "ERR12345"
    assert sample.project_acession == 'PRJNA631061'
    assert sample.instrument_platform == "illumina"
    assert sample.read_count == 1000
    assert sample.fastq_md5 == "12fe4521"
    assert sample.fastq_ftp == "test.com/test.fastq"
    assert sample.collection_date == datetime.date(2022, 5, 10)
    assert sample.host == "human"
    assert sample.country == "United Kingdom"
    assert sample.json_metadata == "{'test': 'test'}"
    assert sample.status == SampleStatus.UNPROCESSED
    assert sample.error_text == "Error"
