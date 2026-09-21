import os
import sqlite3

URL = os.environ.get("SUPABASE_URL", "https://lamiupfzrllaqkcgbluv.supabase.co")
KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_qWk-x1Ano4lrNEpg99kKzA_xeYUxXUL")
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rh.db")


class LocalResponse:
    def __init__(self, data):
        self.data = data


class ExecutableQueryBuilder:
    def __init__(self, client, table_name):
        self.client = client
        self.table_name = table_name
        self._select_fields = "*"
        self._filters = []
        self._order_by = None
        self._limit = None

    def select(self, fields="*"):
        self._select_fields = fields
        return self

    def eq(self, column, value):
        self._filters.append((column, "=", value))
        return self

    def order(self, column, desc=False):
        self._order_by = f"{column} {'DESC' if desc else 'ASC'}"
        return self

    def limit(self, count):
        self._limit = count
        return self

    def insert(self, record_or_records):
        records = record_or_records if isinstance(record_or_records, list) else [record_or_records]
        self._pending_action = ("insert", records)
        return self

    def update(self, values):
        self._pending_action = ("update", values)
        return self

    def delete(self):
        self._pending_action = ("delete", None)
        return self

    def execute(self):
        if hasattr(self, "_pending_action"):
            action, payload = self._pending_action
            if action == "insert":
                records = payload
                with self.client.get_connection() as conn:
                    cursor = conn.cursor()
                    inserted = []
                    for rec in records:
                        cols = list(rec.keys())
                        placeholders = ", ".join(["?"] * len(cols))
                        sql = f"INSERT OR REPLACE INTO {self.table_name} ({', '.join(cols)}) VALUES ({placeholders})"
                        cursor.execute(sql, [rec[c] for c in cols])
                        last_id = cursor.lastrowid
                        rec_copy = dict(rec)
                        if "id" not in rec_copy and last_id:
                            pk_col = f"id_{self.table_name[:-1]}" if self.table_name.endswith("s") else "id"
                            rec_copy.setdefault(pk_col, last_id)
                        inserted.append(rec_copy)
                    conn.commit()
                    return LocalResponse(inserted)
            elif action == "update":
                values = payload
                with self.client.get_connection() as conn:
                    cursor = conn.cursor()
                    set_clause = ", ".join([f"{col} = ?" for col in values.keys()])
                    params = list(values.values())
                    where_clause = ""
                    if self._filters:
                        where_clause = " WHERE " + " AND ".join([f"{col} {op} ?" for col, op, _ in self._filters])
                        params += [val for _, _, val in self._filters]
                    sql = f"UPDATE {self.table_name} SET {set_clause}{where_clause}"
                    cursor.execute(sql, params)
                    conn.commit()
                    return LocalResponse([])
            elif action == "delete":
                with self.client.get_connection() as conn:
                    cursor = conn.cursor()
                    where_clause = ""
                    params = []
                    if self._filters:
                        where_clause = " WHERE " + " AND ".join([f"{col} {op} ?" for col, op, _ in self._filters])
                        params = [val for _, _, val in self._filters]
                    sql = f"DELETE FROM {self.table_name}{where_clause}"
                    cursor.execute(sql, params)
                    conn.commit()
                    return LocalResponse([])

        query = f"SELECT * FROM {self.table_name}"
        params = []
        if self._filters:
            where_clauses = [f"{col} {op} ?" for col, op, _ in self._filters]
            query += " WHERE " + " AND ".join(where_clauses)
            params = [val for _, _, val in self._filters]
        if self._order_by:
            query += f" ORDER BY {self._order_by}"
        if self._limit is not None:
            query += f" LIMIT {self._limit}"

        with self.client.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = [dict(row) for row in cursor.fetchall()]
            return LocalResponse(rows)


class LocalSupabaseClient:
    def __init__(self, db_path=DB_FILE):
        self.db_path = db_path
        self._init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_db(self):
        with self.get_connection() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS departamentos (
                    id_departamento INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL UNIQUE,
                    descricao TEXT
                );

                CREATE TABLE IF NOT EXISTS funcionarios (
                    id_funcionario INTEGER PRIMARY KEY,
                    id_departamento INTEGER,
                    nome TEXT NOT NULL,
                    cpf TEXT UNIQUE,
                    cargo TEXT NOT NULL,
                    salario REAL NOT NULL,
                    status TEXT NOT NULL DEFAULT 'Ativo',
                    FOREIGN KEY(id_departamento) REFERENCES departamentos(id_departamento)
                );

                CREATE TABLE IF NOT EXISTS dependentes (
                    id_dependente INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_funcionario INTEGER NOT NULL,
                    nome TEXT NOT NULL,
                    parentesco TEXT NOT NULL,
                    data_nascimento TEXT,
                    FOREIGN KEY(id_funcionario) REFERENCES funcionarios(id_funcionario)
                );

                CREATE TABLE IF NOT EXISTS pagamentos (
                    id_pagamento INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_funcionario INTEGER NOT NULL,
                    mes_referencia TEXT NOT NULL,
                    salario_base REAL NOT NULL,
                    descontos REAL DEFAULT 0,
                    beneficios REAL DEFAULT 0,
                    valor_liquido REAL NOT NULL,
                    data_pagamento TEXT NOT NULL,
                    FOREIGN KEY(id_funcionario) REFERENCES funcionarios(id_funcionario)
                );
            """)

    def table(self, table_name):
        return ExecutableQueryBuilder(self, table_name)


def init_client():
    # Tenta conectar no Supabase remoto se configurado e acessível
    try:
        from supabase import create_client
        client = create_client(URL, KEY)
        client.table("funcionarios").select("id_funcionario").limit(1).execute()
        return client
    except Exception:
        return LocalSupabaseClient()


supabase = init_client()
