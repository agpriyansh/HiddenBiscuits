from flask import Flask, render_template, request, session, redirect
import json

app = Flask(__name__)
app.secret_key = 'test'

def check_passwd(username,password):
    f = open('/var/www/HiddenBiscuits/HiddenBiscuits/database/login_info.json','r')
    login_info = json.load(f)
    found = False
    for user in login_info:
        if user == username:
            if login_info[user]['password'] == password:
                found = True
                break
            else:
                pass
        else:
            pass
    f.close()
    return found

def check_username(username):
    f = open('/var/www/HiddenBiscuits/HiddenBiscuits/database/login_info.json','r')
    login_info = json.load(f)
    found = False
    for user in login_info:
        if user == username:
            found = True
        else:
            pass
    return found

def add_post(title, content, username):
    post = {title:content}
    file_name = f'/var/www/HiddenBiscuits/HiddenBiscuits/database/posts/{username}.json'
    try:
        f = open(file_name,'r')
        all_posts = json.load(f)
        f.close()
    except:
        all_posts = {}
    f = open(file_name,'w')
    all_posts.update(post)
    data = json.dumps(all_posts, indent=4)
    f.write(data)
    f.close()

def add_user(username, name, password):
    f = open('/var/www/HiddenBiscuits/HiddenBiscuits/database/login_info.json','r')
    all_data = json.load(f)
    f.close()
    entry = {
        username:{
            "name":name,
            "password":password
        }
    }
    all_data.update(entry)
    json_data = json.dumps(all_data, indent=4)
    f = open('/var/www/HiddenBiscuits/HiddenBiscuits/database/login_info.json','w')
    f.write(json_data)
    f.close()

@app.route('/', methods=['GET'])
def index():
    if 'logged_in_as' in session and session['logged_in_as']:
        return render_template('index.html', logged_in=True, user=session['logged_in_as'])
    else:
        return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        check = check_passwd(username,password)
        if check:
            session['logged_in_as'] = username
            return redirect('/')
        else:
            return render_template('login.html', message='Incorrect username or password.')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        conf_password = request.form.get('conf_password')
        if check_username(username):
            return render_template('register.html', message="Pick a different username, this one already exists.")
        if password != conf_password:
            return render_template('register.html', message='Passwords dont match')
        else:
            add_user(username,name,password)
            return render_template('register.html', message="Account successfully created.")

@app.route('/logout', methods=['GET'])
def logout():
    if 'logged_in_as' in session and session['logged_in_as']:
        session.pop('logged_in_as')
        return redirect('/')
    else:
        return redirect('/')

@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'GET':
        if 'logged_in_as' in session and session['logged_in_as']:
            return render_template('create.html', logged_in=True, user=session['logged_in_as'])
        else:
            return render_template('login.html')
    elif request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        add_post(title, content, session['logged_in_as'])
        return redirect('/all')

@app.route('/all', methods=['GET'])
def all():
    username = session['logged_in_as']
    try:
        filename = f'/var/www/HiddenBiscuits/HiddenBiscuits/database/posts/{username}.json'
        f = open(filename,'r')
        all_posts = json.load(f)
        f.close()
        return render_template('all.html', all_posts=all_posts, logged_in=True, user=session['logged_in_as'])
    except:
        return render_template('all.html', message="No posts for this user.", logged_in=True, user=session['logged_in_as'])
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
