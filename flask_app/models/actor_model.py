
from flask_app.config.mysqlconnection import connectToMySQL 
from flask_app.models import movie_model



class Actor: 
    db_name = "group_project" 
    
    def __init__(self,data): 
        self.id = data['id'] 
        self.first_name = data['first_name'] 
        self.last_name = data['last_name'] 
        self.img_path = data['img_path'] 
        self.movies = []
        # added for many to many
        self.created_at = data['created_at'] 
        self.updated_at = data['updated_at'] 

    # CREATE and SAVE actor into database 
    @classmethod 
    def create_actor(cls,data): 
        query = "INSERT INTO actors (first_name, last_name, img_path) VALUES (%(first_name)s,%(last_name)s,%(img_path)s);" 
        return connectToMySQL(cls.db_name).query_db(query, data) 


    #RETRIVE ALL actors from database 
    @classmethod
    def get_all_actors(cls):
        query = "SELECT * FROM actors;"
        results = connectToMySQL(cls.db_name).query_db(query) 
        print(results) 
        all_actors = [] 
        for row in results: 
            print(row['first_name']) 
            all_actors.append(cls(row)) 
        return all_actors 

    #RETRIEVE ONE actor from database by movie's id 
    @classmethod
    def get_one_actor(cls,data): 
        query = "SELECT * FROM actors WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0]) 

# UPDATE actor by actor's ID
    @classmethod
    def update_actor(cls, data):
        query = "UPDATE actors SET first_name = %(first_name)s, last_name = %(last_name)s, img_path = %(img_path)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

# DELETE actor
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM actors WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod 
    def get_actor_with_movies(cls,data): 
        query = " SELECT * FROM actors LEFT JOIN actors_has_movies ON actors_has_movies.actor_id = actors.id LEFT JOIN movies on actors_has_movies.movie_id = movies.id WHERE actors.id = %(id)s;" 
        results = connectToMySQL(cls.db_name).query_db(query,data)
        print(results)
        actor = cls(results[0])
        for row_from_db in results:
            movie_data = {
                "id" : row_from_db["movies.id"],
                "rating" : row_from_db["rating"],
                "title" : row_from_db["title"],
                "img_path" : row_from_db["img_path"],
                "description" : row_from_db["description"],
                "user_id" : row_from_db["user_id"],
                "created_at" : row_from_db["movies.created_at"],
                "updated_at" : row_from_db["movies.updated_at"]
                
            }
            actor.movies.append(movie_model.Movie(movie_data))
        return actor

    # this actually makes the many to many connection
    @classmethod
    def create_many(cls,data):
        query = "INSERT INTO actors_has_movies (actor_id, movie_id) VALUES (%(actor_id)s, %(movie_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)


#  VALIDATION OF ACTOR
    @staticmethod
    def validate_actor(actor):
        is_valid = True

        if len(actor["first_name"]) < 1:
            print("*************************")
            print(actor["first_name"])
            print("*************************")
            is_valid = False
            flash("Please name your actor", "actor")
        if actor['last_name'] == "":
            is_valid = False
            flash("Please name your actor", "actor")
        return is_valid
