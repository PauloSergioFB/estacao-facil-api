def public_user_serializer(values):
    return dict(zip(["id", "first_name", "last_name", "email"], values))


def user_serializer(values):
    return dict(zip(["id", "first_name", "last_name", "email", "password"], values))
