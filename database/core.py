from contextlib import contextmanager

import oracledb

from settings import Settings


settings = Settings()


def open_connection():
    return oracledb.connect(
        user=settings.DB_USER, password=settings.DB_PASSWORD, dsn=settings.DB_URL
    )


def get_connection():
    con = open_connection()
    try:
        yield con
    finally:
        con.close()


# Função para testes
@contextmanager
def _get_connection():
    con = open_connection()
    try:
        yield con
    finally:
        con.close()


def get_insert_stmt(table_name, keys, id_key):
    columns = ", ".join(keys)
    values = ", ".join(list(map(lambda k: f":{k}", keys)))

    stmt = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
    stmt += f" RETURNING {id_key} INTO :{id_key}"

    return stmt


def get_update_stmt(table_name, keys, id_key):
    setters = ", ".join(list(map(lambda k: f"{k} = :{k}", keys)))

    stmt = f"UPDATE {table_name} SET {setters} WHERE {id_key} = :id"

    return stmt


def get_delete_stmt(table_name, id_key):
    stmt = f"DELETE FROM {table_name} WHERE {id_key} = :id"

    return stmt


def select_one(con, stmt, values={}, serializer=lambda x: x):
    with con.cursor() as cur:
        cur.execute(stmt, values)
        result = cur.fetchone()

    return serializer(result) if result else None


def select_all(con, stmt, values={}, serializer=lambda x: x):
    with con.cursor() as cur:
        cur.execute(stmt, values)
        result = cur.fetchall()

    return list(map(serializer, result)) if result else []


def insert(con, table_name, data, id_key):
    data = data.copy()
    stmt = get_insert_stmt(table_name, data.keys(), id_key)

    with con.cursor() as cur:
        id = cur.var(oracledb.NUMBER)
        data[id_key] = id

        cur.execute(stmt, data)
        id = id.getvalue()[0]

    con.commit()
    return id


def update(con, id, table_name, data, id_key):
    data = data.copy()
    stmt = get_update_stmt(table_name, data.keys(), id_key)

    with con.cursor() as cur:
        data["id"] = id
        cur.execute(stmt, data)

    con.commit()


def delete(con, id, table_name, id_key):
    stmt = get_delete_stmt(table_name, id_key)

    with con.cursor() as cur:
        cur.execute(stmt, {"id": id})

    con.commit()
