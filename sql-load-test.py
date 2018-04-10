#!/usr/bin/env python
import csv
import os
import tempfile
from multiprocessing import Pool, cpu_count
from itertools import islice
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import func, Integer, Column
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from FunkyBusFare.multiread import MultiRead

@as_declarative()
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)

class TestQL(Base):
    foo = Column(Integer)
    bar = Column(Integer)

def prep_csv(record_count):
    with open(PATH, "w") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
        writer.writeheader()
        for i in range(record_count):
            writer.writerow({"foo":i, "bar": i*3})

class WackRead(MultiRead):
    
    def run(self):
        pool = Pool(cpu_count())
        pool.map(job, self.chunks)

class WackWrite(object):

    def worker(self, step, path, start, end, header):
        print("%s working"%step)
        with open(path, "r") as fh:
            reader = csv.reader(islice(fh, start, end))
            objects = []
            while True:
                try:
                    foo, bar = next(reader)
                    objects.append(TestQL(foo=foo, bar=bar))
                except StopIteration:
                    break
        session.bulk_save_objects(objects)
        session.commit()
        print("%s finished"%step)

def job(vals):
    ww = WackWrite()
    ww.worker(**vals)

if __name__ == "__main__":

    if os.path.exists("crapholder"):
        os.remove("crapholder")
    FIELDNAMES = ["foo", "bar"]
    PATH = os.path.join(tempfile.gettempdir(), "test.csv")
    prep_csv(1000000)
    engine = create_engine('sqlite:///crapholder')
    Base.metadata.create_all(engine)
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()
    ww = WackRead(PATH, limit=10000)
    ww.run()
    print(session.query(TestQL).count())
