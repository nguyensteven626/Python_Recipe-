from flask import render_template, redirect, session, request, flash
from flask_app import app 
from flask_app.models.user import User
from flask_app.models.recipe import Recipe 


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('dashboard.html', user = User.get_by_id({'id': session['user_id']}), all_recipes = Recipe.retrieve_all())

@app.route('/recipe/new')
def new_recipe():
    return render_template('create.html')

@app.route('/recipe/create', methods=['POST'])
def create_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipe/new')
    data = {
        **request.form,
        'user_id': session['user_id']
    }
    Recipe.create_recipe(data)
    return redirect('/dashboard')

@app.route('/recipe/<int:id>')
def view_one(id):
    return render_template('view.html', user = User.get_by_id({'id': session['user_id']}), recipe=Recipe.retrieve_one({'id': id}))

@app.route('/recipe/<int:id>/edit')
def edit(id):
    return render_template('edit.html',recipe=Recipe.retrieve_one({'id': id}) )

@app.route('/recipe/<int:id>/update', methods = ['POST'])
def update(id):
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipe/{id}/edit')
    
    data = {
        **request.form,
        'id': id
    }

    Recipe.update(data)
    return redirect ('/dashboard')

@app.route('/recipe/<int:id>/delete')
def delete(id):
    
    Recipe.delete({'id':id})
    return redirect('/dashboard')
