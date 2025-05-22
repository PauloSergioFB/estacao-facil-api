import database.core as db
from services.security import password_hash
from serializers.users import public_user_serializer, user_serializer


class UserAlreadyExists(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def get_user_by_id(con, id):
    stmt = """
    SELECT 
        user_id,
        user_first_name,
        user_last_name,
        user_email
    FROM
        ef_user
    WHERE
        user_id = :user_id
    """
    return db.select_one(
        con, stmt, values={"user_id": id}, serializer=public_user_serializer
    )


def get_user_by_email(con, email):
    stmt = """
    SELECT 
        user_id,
        user_first_name,
        user_last_name,
        user_email,
        user_password
    FROM
        ef_user
    WHERE
        user_email = :user_email
    """
    return db.select_one(
        con, stmt, values={"user_email": email}, serializer=user_serializer
    )


def check_user_conflict(con, first_name, last_name, email):
    stmt = """
    SELECT
        user_id,
        user_first_name,
        user_last_name,
        user_email
    FROM
        ef_user
    WHERE
        ( user_first_name = :user_first_name
        AND user_last_name = :user_last_name )
        OR user_email = :user_email
    """
    user = db.select_one(
        con,
        stmt,
        values={
            "user_first_name": first_name,
            "user_last_name": last_name,
            "user_email": email,
        },
        serializer=public_user_serializer,
    )

    if not user:
        return

    if user["first_name"] == first_name and user["last_name"] == last_name:
        raise UserAlreadyExists("First name and last name combination already exists")

    if user["email"] == email:
        raise UserAlreadyExists("Email already exists")


def check_update_user_conflict(con, id, first_name, last_name, email):
    stmt = """
    SELECT
        user_id,
        user_first_name,
        user_last_name,
        user_email
    FROM
        ef_user
    WHERE
        ( ( user_first_name = :user_first_name
        AND user_last_name = :user_last_name )
        OR user_email = :user_email )
        AND user_id != :user_id
    """
    user = db.select_one(
        con,
        stmt,
        values={
            "user_id": id,
            "user_first_name": first_name,
            "user_last_name": last_name,
            "user_email": email,
        },
        serializer=public_user_serializer,
    )

    if not user:
        return

    if user["first_name"] == first_name and user["last_name"] == last_name:
        raise UserAlreadyExists("First name and last name combination already exists")

    if user["email"] == email:
        raise UserAlreadyExists("Email already exists")


def insert_user(con, user):
    check_user_conflict(con, user["first_name"], user["last_name"], user["email"])

    user["password"] = password_hash(user["password"])
    user_id = db.insert(
        con,
        "ef_user",
        {
            "user_first_name": user["first_name"],
            "user_last_name": user["last_name"],
            "user_email": user["email"],
            "user_password": user["password"],
        },
        id_key="user_id",
    )
    return get_user_by_id(con, user_id)


def update_user(con, id, user):
    check_update_user_conflict(
        con, id, user["first_name"], user["last_name"], user["email"]
    )

    db.update(
        con,
        id,
        "ef_user",
        {
            "user_first_name": user["first_name"],
            "user_last_name": user["last_name"],
            "user_email": user["email"],
        },
        id_key="user_id",
    )
    return get_user_by_id(con, id)


def update_user_password(con, id, user):
    user["new_password"] = password_hash(user["new_password"])
    db.update(
        con,
        id,
        "ef_user",
        {"user_password": user["new_password"]},
        id_key="user_id",
    )
