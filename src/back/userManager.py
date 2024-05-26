def createUser(data):
    user = User(
        username=data['username'],
        email=data['email'],
        password=hash_password(data['password'])
    )
    db.session.add(user)
    db.session.commit()
    return user