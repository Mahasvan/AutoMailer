import sqlalchemy as db
from sqlalchemy import Table, create_engine, Column
from sqlalchemy.orm import Session
import datetime


class Database:
    _instance = None
    
    # This will be a singleton class
    def __new__(cls, *args, **kwargs):
        if Database._instance is None:
            Database._instance = object.__new__(cls)
            Database._instance.__init__(*args, **kwargs)

        return Database._instance

    def __init__(self, dbfile: str):
        self.engine = create_engine(f"sqlite:///{dbfile}")
        self.engine.connect()
        self.meta = db.MetaData()

        self._sent = Table(
            "sent", self.meta,
            Column("recipient_hash", db.String, primary_key=True),
            Column("sent_time", db.DateTime))
        
        self.meta.create_all(self.engine)

    def insert_recipient(self, recipient_hash: str) -> int:
        with Session(self.engine) as session:
            command = self._sent.insert().values(recipient_hash=recipient_hash, sent_time=datetime.datetime.now())
            result = session.execute(command)
            session.commit()
            return result.lastrowid

    def check_recipient_sent(self, recipient_hash: str) -> bool:
        with Session(self.engine) as session:
            query = self._sent.select().where(self._sent.c.recipient_hash == recipient_hash)
            result = session.execute(query).fetchone()
            return result is not None
    
    def get_sent_recipients(self) -> list:
        with Session(self.engine) as session:
            query = self._sent.select()
            result = session.execute(query).fetchall()
            return [dict(row) for row in result]
        
    def delete_recipient(self, recipient_hash: str) -> None:
        if not self.check_recipient_sent(recipient_hash):
            raise ValueError(f"Recipient with hash {recipient_hash} not found in the database.")
    
        with Session(self.engine) as session:
            command = self._sent.delete().where(self._sent.c.recipient_hash == recipient_hash)
            session.execute(command)
            session.commit()
    