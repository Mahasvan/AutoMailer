import sqlite3
from tabulate import tabulate
import datetime

class SessionManager:
    def __init__(self, db_path='automailer.db'):
        self.conn = sqlite3.connect(db_path)
        self.db_path = db_path
        self._create_db()

    def _create_db(self):
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

    def _hash_recipient(self, session_id, recipient):
        recipient['session_id'] = session_id
        return str(recipient)
    
    def start_session(self,
                        sender_email: str, password: str,
                        recipients: list[dict[str, str]], 
                        subject_template: str, 
                        text_template: str = None,
                        html_template: str = None, 
                        attachment_paths: list[str] = None, 
                        cc: list[str] = None, 
                        bcc: list[str] = None,
                        provider: str = "gmail"):
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
    
    def continue_session(self, session_id):
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
    
    def retry_failed(self,session_id):
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
    
    def show_sessions(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Sessions")
        sessions = cursor.fetchall()

        table = tabulate(sessions)
        return table




