import sqlite3
from tabulate import tabulate
import datetime
from typing import List, Dict, Optional, Any

class SessionManager:
    def __init__(self, db_path: str = 'automailer.db') -> None:
        #Initialize connection
        self.conn = sqlite3.connect(db_path)
        self.db_path = db_path
        self._create_db()

    #Create the tables if they don't exist
    def _create_db(self) -> None:
        cursor = self.conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Sessions (
                session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Recipients (
                r_hash TEXT PRIMARY KEY,
                session_id INTEGER,
                status TEXT,
                FOREIGN KEY(session_id) REFERENCES Sessions(session_id)
            )
        ''')

        self.conn.commit()

    #Creates the primary key of the Recipients table
    def _hash_recipient(self, session_id: int, recipient: Dict[str, Any]) -> str:
        recipient['session_id'] = session_id
        return str(recipient)
    
    #Start a new session
    def start_session(self,recipients: List[Dict[str, str]]) -> int:
        cursor = self.conn.cursor()
        start_time = datetime.datetime.now()
        cursor.execute("INSERT INTO Sessions (start_time) VALUES (?)",(start_time,))
        session_id = cursor.lastrowid

        for rec in recipients:
            r_hash = self._hash_recipient(session_id,rec)
            cursor.execute(
                "INSERT INTO Recipients (r_hash,session_id,status) VALUES (?,?,?)",
                (r_hash,session_id,'Pending')
            )

        self.conn.commit()
        return session_id
    
    #Filter the recipients whose email wasn't sent in the previous run
    def continue_session(self, session_id: int) -> List[Dict[str, str]]:
        cursor = self.conn.cursor()

        cursor.execute("SELECT r_hash FROM Recipients WHERE session_id = ? AND status = 'Pending",(session_id,))
        recipients = cursor.fetchall()

        recipients_list = []
        for rec in recipients:
            r = rec[0]
            r = eval(r)
            del r['session_id']
            recipients_list.append(r)

        return recipients_list
    
    #Filter recipients whose email failed in the previous run
    def retry_failed(self, session_id: int) -> List[Dict[str, str]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT r_hash FROM Recipients WHERE session_id = ? AND status = 'Failed",(session_id,))
        recipients = cursor.fetchall()

        recipients_list = []
        for rec in recipients:
            r = rec[0]
            r = eval(r)
            del r['session_id']
            recipients_list.append(r)

        return recipients_list        
    
    #Returns a table of all sessions
    def show_sessions(self) -> str:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Sessions")
        sessions = cursor.fetchall()

        table = tabulate(sessions)
        return table