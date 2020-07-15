import sqlite3
# Database abstraction

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("data.db")
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS services
                       (id integer PRIMARY KEY AUTOINCREMENT,
                       name text NOT NULL UNIQUE,
                       port integer NOT NULL) """)
        self.c.execute("""CREATE TABLE IF NOT EXISTS flags
                       (id integer PRIMARY KEY AUTOINCREMENT,
                        flag text NOT NULL UNIQUE,
                        service_id integer NOT NULL,
                        FOREIGN KEY (service_id) REFERENCES services (id))""")
        self.c.execute("""CREATE TABLE IF NOT EXISTS targets
                          (ip text NOT NULl UNIQUE)""")
        self.c.execute("""CREATE TABLE IF NOT EXISTS exploits
                       (id integer PRIMARY KEY AUTOINCREMENT,
                       filename text NOT NULL,
                       service_id integer NOT NULL,
                       FOREIGN KEY (service_id) REFERENCES services (id),
                       UNIQUE(filename, service_id))""")

    # Services
    def insert_service(self, name, port):
        try:
            self.c.execute("""INSERT INTO services (name, port) VALUES
                            (?, ?)""", (name, port))
        except sqlite3.IntegrityError:
            raise
        self.conn.commit()
    def get_services(self):
        self.c.execute("SELECT id, name, port FROM services")
        self.conn.commit()
        return self.c.fetchall()
    
    # Flags
    def insert_flag(self, flag, service_id):
        try:
            self.c.execute("INSERT INTO flags (flag, service_id) VALUES (?, ?)", (flag, service_id))
        except sqlite3.IntegrityError:
            raise
        self.conn.commit()
    def get_flags(self, _filter = None):
        if _filter:
            self.c.execute("SELECT * FROM flags f LEFT JOIN services s ON f.service_id = s.id WHERE flag = ?", (_filter,))
        else:
            self.c.execute("SELECT * FROM flags f LEFT JOIN services s ON f.service_id = s.id")
        self.conn.commit()
        return self.c.fetchall()
    
    # Targets
    def get_targets(self):
        self.c.execute("SELECT * FROM targets")
        self.conn.commit()
        return self.c.fetchall()
    
    # Exploits
    def insert_exploit(self, filename, service_id):
        self.c.execute("INSERT INTO exploits (filename, service_id) VALUES (?, ?)", (filename, service_id))
        self.conn.commit()
    def get_exploits(self, _filter = None):
        if _filter:
            self.c.execute("SELECT * FROM exploits e LEFT JOIN services s ON e.service_id = s.id WHERE filename = ?", (_filter,))
        else:
            self.c.execute("SELECT * FROM exploits e LEFT JOIN services s ON e.service_id = s.id")
        self.conn.commit()
        return self.c.fetchall()

database = Database()