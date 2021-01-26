from flask import Flask, render_template, request, redirect
import db_notes
import os


app = Flask(__name__, static_url_path='', 
              static_folder='static', 
              template_folder='templates')

user = {}

def file_update(my_notes):
    my_notes = my_notes[::-1]
    f = open("templates/notes.html", 'w')
    html = """<!DOCTYPE html>
            <head>
                <title>Sticky Notes</title>
                <link rel="stylesheet" type="text/css" href="notes.css" />
                <script
                src="https://code.jquery.com/jquery-3.5.1.min.js"
                integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0="
                crossorigin="anonymous"></script>
            </head>
            <body>
                <header>
                        <h2>My Notes<h2>
                </header>
                    <div id = "renderList">{0}</div>
                    <div id = "my_list">
                    </div>
                    <form class="form-style-7" act action="/addnotes" method="GET">
                        <input class="my_cool_button" type="submit" value="Add New Note">
                    </form>
                    <script type="text/javascript">function reply_click(clicked_id){{                        
                        $.ajax({{url: 'http://127.0.0.1:5000/notes' + '?' + $.param({{"Id": clicked_id}}),type: 'DELETE',success: function(result) {{
                            alert("deleted successfuly")
                        }}
                        }});}};</script>
            </body>
            </html>"""
    ul = "<ul>{0}</ul>"
    li = "<li><h4>{0}</h4><p>{1}</p><br><button class=\"bot\" Id={2} onClick=\"reply_click(this.id)\">Delete Note</button></li>" 
    subitems = ul.format(''.join(li.format(a['category'],a['content'],a['note_id']) for a in my_notes))
    print(subitems)
    html = html.format("".join(subitems))
    #print(html)
    f.write(html)
    f.close()

@app.route('/')
def welcome_page():
    return render_template('home.html')


@app.route('/notes', methods = ["POST", "GET"])
def notes_page():
    global user
    if request.method == 'POST':
        email = request.form["email"]
        userpassword = request.form["password"]
        print(email, userpassword)

        if db_notes.is_user_valid(email, userpassword):
            name = db_notes.get_name(email)
            user['name'] = name
            user['email'] = email
            user['allnotes'] = db_notes.get_all_notes(email)
            file_update(user['allnotes'])
            return render_template("notes.html", a=user['allnotes'])
        else:
            return render_template("home.html")
            
        #if os.path.exists("templates/notes.html"):
            #os.remove("templates/notes.html")
    else:
        user['allnotes'] = db_notes.get_all_notes(user['email'])
        file_update(user['allnotes'])
        return render_template("notes.html")


        #give error message


@app.route('/signup')
def signup_page():
    return render_template("signup.html")


@app.route('/addnotes')
def addnotes_page():
    return render_template("addnotes.html") 


@app.route('/newnote', methods=['POST'])
def new_note():
    global user
    email = user.get("email")
    newnote = request.form["note"]
    category = request.form["category"]
    db_notes.insert_new_note(email, newnote, category)
    name=db_notes.get_name(email)
    user['name'] = name
    user['email'] = email
    user['allnotes'] = db_notes.get_all_notes(email)
    file_update(user['allnotes'])
    return render_template("notes.html")



@app.route('/notes', methods = ["DELETE"])
def delete_note():
    global user
    id = request.args.get('Id')
    db_notes.delete_note(id)
    user['allnotes'] = db_notes.get_all_notes(user['email'])
    file_update(user['allnotes'])
    return render_template('notes.html')


@app.route('/view_notes')
def view_notes():
    global user
    user['allnotes'] = db_notes.get_all_notes(user['email'])
    file_update(user['allnotes'])
    return redirect('/notes')


@app.route('/signupinfo', methods = ["POST"])
def info_page():
    name = request.form["name"]
    email = request.form["email"]
    userpassword = request.form["password"]
    #function that checks if email is valid ()
    db_notes.insert_new_user(name, email, userpassword)    
    userinfo = {}
    userinfo["name"] = name
    userinfo["email"] = email   
    return render_template("home.html", username=userinfo)    


if __name__ == '__main__':
    app.run(port=3000)