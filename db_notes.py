from config import connection as con
def get_name(email):
    with con.cursor() as cursor:
        cursor.execute('SELECT * FROM user WHERE email=%s', [email])
        result_user = cursor.fetchone()
    if result_user == None:
        return {"result":"the user not found, Please singup first, thanks"}
    else:
        return result_user['name']


def delete_note(note_id):
        with con.cursor() as cursor:
            cursor.execute('SELECT * FROM Note WHERE note_id=%s', [note_id])
            result_note = cursor.fetchone()
        if result_note == None:
            return {"result": "the note not found"}
        else:
            with con.cursor() as cursor:
                cursor.execute('DELETE FROM user_note WHERE note_id=%s ',[note_id])
                con.commit()
            with con.cursor() as cursor:
                cursor.execute('DELETE FROM Note WHERE note_id=%s',[note_id])
                con.commit()


def is_user_valid(email,password):
    with con.cursor() as cursor:
        cursor.execute('SELECT * FROM user WHERE email=%s and password=%s', [email,password])
        result_user = cursor.fetchone()
    if result_user == None:
        return False
    return True


def get_all_notes(email):
    with con.cursor() as cursor:
        cursor.execute('SELECT * FROM user WHERE email=%s', [email])
        result_user = cursor.fetchone()
    if result_user == None:
        return {"result":"the user not found, Please singup first, thanks"}
    else:
        with con.cursor() as cursor:
            cursor.execute('SELECT * FROM user_note WHERE user_id=%s', [result_user['user_id']])
            results_note = cursor.fetchall()
        nots_id=[note['note_id'] for note in results_note]
        results=[]
        for note in nots_id:
            with con.cursor() as cursor:
                cursor.execute('SELECT * FROM Note WHERE note_id=%s', [note])
                result_note = cursor.fetchone()
                results.append(result_note)
                #results.append(result_note['content'])
        return results


def insert_new_note(email,content_note,category=None):
    if category == None:
        category="other"
    with con.cursor() as cursor:
        cursor.execute('SELECT * FROM user WHERE email=%s', [email])
        result_user = cursor.fetchone()
    if result_user == None:
        return {"result":"the user not found, Please singup first, thanks"}
    else:
        with con.cursor() as cursor:
            cursor.execute('INSERT into Note (content,category) values (%s,%s)', [content_note,category])
            con.commit()
        with con.cursor() as cursor:
            cursor.execute('SELECT * FROM Note WHERE content=%s and category=%s', [content_note,category])
            result_note = cursor.fetchone()
        with con.cursor() as cursor:
            cursor.execute('INSERT into user_note values (%s,%s)', [result_user['user_id'], result_note['note_id']])
            con.commit()

    return {"result": "welcome "+result_user['name']}
def insert_new_user(*args):
    args = list(args)
    with con.cursor() as cursor:
        cursor.execute('INSERT into user (name,email,password) values (%s,%s,%s)', args)
        con.commit()

     

