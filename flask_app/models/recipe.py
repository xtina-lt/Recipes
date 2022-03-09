from flask_app.config.mysqlconnection import connectToMySQL

class Recipe:
    db="recipes_schema"
    def __init__(self, data):
        self.id=data["id"]
        self.name=data["name"]
        self.description=data["description"]
        self.instructions=data["instructions"]
        self.under_30=data["under_30"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.creator_id=data["creator_id"]
    
    '''READ ALL'''
    @classmethod
    def select_all(cls):
        query="SELECT * FROM recipes"
        results=connectToMySQL(cls.db).query_db(query)
        return [cls(i) for i in results]

    '''READ ONE'''
    @classmethod
    def select_one(cls, data):
        query="SELECT * FROM recipes WHERE id=%(id)s"
        result=connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])

    '''CREATE'''
    @classmethod
    def insert(cls, data):
        query="INSERT INTO recipes(name, description, instructions, under_30, creator_id) VALUES(%(name)s, %(description)s, %(instructions)s, %(under_thirty)s, %(creator_id)s)"
        return connectToMySQL(cls.db).query_db(query, data)
        # returns id number

    '''UPDATE'''
    @classmethod
    def update(cls,data):
        query="UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, under_30=%(under_thirty)s, creator_id=%(creator_id)s WHERE id = %(id)s"
        return connectToMySQL(cls.db).query_db(query, data)


    '''DELETE'''
    @classmethod
    def delete(cls,data):
        query="DELETE FROM recipes WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query, data)