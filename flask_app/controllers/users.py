from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe 
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():

    if 'user_id' in session:
        return ('/dashboard')
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/')
    # data ={ 
    #     "first_name": request.form['first_name'],
    #     "last_name": request.form['last_name'],
    #     "email": request.form['email'],
    #     "password": bcrypt.generate_password_hash(request.form['password'])
    # }
    # id = User.create(data)
    # session['user_id'] = id

    hash_password = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': hash_password
    }
    user_id = User.create(data)
    session['user_id'] = user_id 

    return redirect('/dashboard')

@app.route('/login',methods=['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    
    user = User.get_by_email({'email': request.form['email']})

    # if not user:
    #     flash("Invalid Email","login")
    #     return redirect('/')
    # if not bcrypt.check_password_hash(user.password, request.form['password']):
    #     flash("Invalid Password","login")
    #     return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

    

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')