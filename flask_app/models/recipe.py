from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash
from flask_app import app
from flask_app.models import user 



class Recipe:
    db_name = 'recipes_schema'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        #--change self.user_id = data['user_id'] so recipe can access the users who made the recipe
        self.user = user.User.get_by_id({'id': data['user_id']})
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #-------CREATE-----------
    @classmethod
    def create_recipe(cls, data):
        # query = "INSERT INTO recipes (name, under30, description, instructions,user_id) VALUES(%(name)s,%(under30)s,%(description)s,%(instructions)s, %(date_made)s, %(user_id)s, NOW(),NOW());"
        # return connectToMySQL(cls.db_name).query_db(query,data)

        query = "INSERT INTO recipes (name,description, instructions, date_made, user_id) VALUES (%(name)s,%(description)s,%(instructions)s,%(date_made)s,%(user_id)s, NOW(),NOW());"
        return connectToMySQL(cls.db_name).query_db(query,data)
        

    #-------2 READ Function-----------
    @classmethod
    def retrieve_one(cls, data):
        query = 'SELECT * FROM recipes WHERE id = %(id)s;'
        results =  connectToMySQL(cls.db_name).query_db(query, data)
        
        if len(results) <1:
            return False

        return cls(results[0])
        

    @classmethod
    def retrieve_all(cls):

        query = "SELECT * FROM recipes;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        recipes = []
        for row in results:
            recipes.append( cls(row) )
        return recipes

    #-------UPDATE-----------
    @classmethod
    def update(cls, data):
        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, updated_at = NOW() WHERE id = %(id)s;'
        return connectToMySQL(cls.db_name).query_db(query,data)

    #-------DELETE--------
    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM recipes WHERE id = %(id)s;'
        connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_recipe(data):
        is_valid = True

        if len(data['name']) < 3:
            flash('Name must be at least 3 characters.',"create_recipe")
            is_valid = False

        if len(data['description']) < 3:
            flash('Description must be at least 3 characters.',"create_recipe")
            is_valid = False

        if len(data['instructions']) < 3:
            flash('Instructions must be at least 3 characters.',"create_recipe")
            is_valid = False

        if len(data['date_made']) < 3:
            flash('Must enter date',"create_recipe")
            is_valid = False


        return is_valid