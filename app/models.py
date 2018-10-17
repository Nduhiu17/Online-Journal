from datetime import datetime


from passlib.handlers.pbkdf2 import pbkdf2_sha256

from app.database import connect_to_db

cursor = connect_to_db()


class Entry:
    def __init__(self, id, title, description, user_id, date_created, date_modified):
        '''method to initialize an entry class'''
        self.id = id
        self.title = title
        self.description = description
        self.user_id = user_id
        self.date_created = date_created
        self.date_modified = date_modified

    def json_dumps(self):
        '''method to return a json object from an entry details'''
        obj = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "user": User.find_by_id(self.user_id),
            "date_created": str(self.date_created),
            "date_modified": str(self.date_modified),
        }
        return obj

    @classmethod
    def find_by_id(cls, id):
        '''method to find a user by id'''
        try:
            cursor.execute("select * from users where id = %s", (id,))
            retrieved_user = list(cursor.fetchone())
            user = User(id=retrieved_user[0], username=retrieved_user[1], email=retrieved_user[2],
                        password=retrieved_user[3], date_created=retrieved_user[4], date_modified=retrieved_user[5])

            return user.json_dumps()
        except Exception:
            return False

    @classmethod
    def save(cls, user_id, date_created, date_modified, title, description):
        """Method to save an entry"""
        format_str = f"""
        INSERT INTO public.entries (user_id,title,description,date_created,date_modified)
        VALUES ('{user_id}','{title}','{description}','{str(datetime.now())}','{str(datetime.now())}') ;
        """
        cursor.execute(format_str)

        return {
            "title": title,
            "description": description,
            "user_id": user_id,
            "date_created": date_created,
            "date_modified":date_modified

        }

    @classmethod
    def get_all_entries(cls):
        """Method to get all entries"""
        cursor.execute(
            f"SELECT * FROM public.entries")
        rows = cursor.fetchall()
        print(rows)

        list_dict = []

        for item in rows:
            entry = Entry(id=item[0], user_id=item[1], date_created=item[2], date_modified=item[3], title=item[4],
                          description=item[5])
            list_dict.append(entry.json_dumps())
        return list_dict


    @classmethod
    def get_entry(cls, id):
        """Method to get an entry by id"""
        cursor.execute('SELECT * FROM "public"."entries" WHERE id=%s', (id,))
        row = cursor.fetchone()
        if row:
            entry = Entry(id=row[0],user_id=row[1],date_created=row[2],date_modified=row[3],title=row[4],description=row[5])
            retrieved_entry= entry.json_dumps()
            return retrieved_entry
        return None




    @classmethod
    def delete(cls, id):
        '''method to delete a question'''
        try:
            cursor.execute('DELETE FROM public.entries CASCADE WHERE id = %s', (id,))
        except Exception:
            return "failed"

    @classmethod
    def update(cls, title, description, id):
        """Method to save an entry"""

        format_str = f"""
        UPDATE public.entries SET title = '{title}', description = '{description}', date_modified = '{str(datetime.now())}' WHERE id = {id};
        """
        try:
            cursor.execute(format_str)
        except Exception:
            return "failed"

        return {
            "date_modified": str(datetime.now()),
            "title": title,
            "description": description
        }


class User:
    def __init__(self, id, username, email, password, date_created, date_modified):
        '''method to initialize User class'''
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.date_created = date_created
        self.date_modified = date_modified

    @classmethod
    # this method registers a user in the database
    def save(cls, username, email, password, date_created, date_modified):
        found_user = cls.find_by_email(email)
        if found_user != False:
            return {'status': "failed", "message": 'email already registered'}
        format_str = f"""
        INSERT INTO public.users (username,email,password,date_created,date_modified)
        VALUES ('{username}','{email}','{password}','{str(datetime.now())}','{str(datetime.now())}');
        """
        cursor.execute(format_str)

        return {
            "username": username,
            "email": email,
            "date_created": str(date_created),
            "date_modified": str(date_modified)
        }

    @classmethod
    # This method gets a user using email
    def find_by_email(cls, email):
        try:
            cursor.execute("select * from users where email = %s", (email,))
            user = cursor.fetchone()
            return list(user)
        except Exception as e:
            return False

    @classmethod
    def find_by_username(cls, username):
        '''method to find a user by username'''
        try:
            cursor.execute("select * from users where username = %s", (username,))
            user = cursor.fetchone()
            return list(user)
        except Exception:
            return False

    # method to generate hash from the password
    @staticmethod
    def generate_hash(password):
        return pbkdf2_sha256.hash(password)

    # method to verify the harshed password
    @staticmethod
    def verify_hash(password, hash):
        return pbkdf2_sha256.verify(password, hash)

    def json_dumps(self):
        '''method to return a json object from a user'''
        ans = {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }
        return ans


    @classmethod
    def find_by_id(cls, id):
        '''method to find a user by id'''
        try:
            cursor.execute("select * from users where id = %s", (id,))
            retrieved_user = list(cursor.fetchone())
            user = User(id=retrieved_user[0], username=retrieved_user[1], email=retrieved_user[2],
                        password=retrieved_user[3], date_created=retrieved_user[4], date_modified=retrieved_user[5])
            return user.json_dumps()
        except Exception:
            return False