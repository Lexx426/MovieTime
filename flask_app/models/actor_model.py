
from flask_app.config.mysqlconnection import connectToMySQL 
from flask_app.models import movie_model



class Actor: 
    db_name = "group_project" 
    
    def __init__(self,data): 
        self.UUID = data['UUID'] 
        self.name = data['name'] 
        self.movies = []
        # added for many to many


    # CREATE and SAVE actor into database 
    @classmethod 
    def create_actor(cls,data): 
        query = "INSERT INTO actors (UUID, name) VALUES (%(UUID)s,%(name)s);" 
        return connectToMySQL(cls.db_name).query_db(query, data) 


    #RETRIVE ALL actors from database 
    @classmethod
    def get_all_actors(cls):
        query = "SELECT * FROM actors;"
        results = connectToMySQL(cls.db_name).query_db(query) 
        print(results) 
        all_actors = [] 
        for row in results: 
            print(row['name']) 
            all_actors.append(cls(row)) 
        return all_actors 

    #RETRIEVE ONE actor from database by movie's id 
    @classmethod
    def get_one_actor(cls,data): 
        query = "SELECT * FROM actors WHERE UUID = %(UUID)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0]) 

# UPDATE actor by actor's ID
# dont need an update

# DELETE actor
# maybeonly if you have an actor page?
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM actors WHERE UUID = %(UUID)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod 
    def get_actor_with_movies(cls,data): 
        query = " SELECT * FROM actors LEFT JOIN movies_has_actors ON movies_has_actors.actor_UUID = actors.UUID LEFT JOIN movies on movies_has_actors.movie_UUID = movies.UUID WHERE actors.UUID = %(UUID)s;" 
        results = connectToMySQL(cls.db_name).query_db(query,data)
        print(results)
        actor = cls(results[0])
        for row_from_db in results:
            movie_data = {
                "UUID" : row_from_db["movies.UUID"],
                "title" : row_from_db["title"],
            }
            actor.movies.append(movie_model.Movie(movie_data))
        return actor

    # this actually makes the many to many connection
    @classmethod
    def create_many(cls,data):
        query = "INSERT INTO movies_has_actors (actor_UUID, movie_UUID) VALUES (%(actor_UUID)s, %(movie_UUID)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)



