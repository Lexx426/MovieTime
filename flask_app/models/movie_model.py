from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_model, actor_model, comment_model 


class Movie:
    db_name = "letterbox"
    
    def __init__(self,data): 
        self.UUID = data['UUID']
        self.title = data['title']
        self.reviews = []
        # changed from none to list ( makes it class instances below)
        
    # CREATE and SAVE movie into database
    @classmethod
    def create_movie(cls,data):
        query = "INSERT INTO movies (UUID, title) VALUES (%(UUID)s,%(title)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
        
    #RETRIVE ALL movies from database
    @classmethod
    def get_all_movies(cls):
        query = "SELECT * FROM movies;"
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results)
        all_movies = []
        for row in results: 
            print(row['title'])
            all_movies.append(cls(row))
        return all_movies
            #bring comments into this class method
    
    #RETRIEVE ONE movie from database by movie's id 
    @classmethod
    def get_one_movie(cls,data): 
        query = "SELECT * FROM movies WHERE UUID = %(UUID)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        movie = cls(results[0])
        movie.reviews = review_model.Review.movie_with_review({"id": results[0]["id"]})
        # movie.reviews = review_model.Review.movie_with_review({"UUID": results[0]["UUID"]})
        return movie
    
    # You do not need an update movie since you cant
    
    
    @classmethod
    def get_movie_with_review(cls, data):
        query = "SELECT * FROM movies LEFT JOIN reviews ON reviewss.UUID = movies.UUID LEFT JOIN users ON reviews.user_id = users.id WHERE movies.UUID = %(UUID)s;"
        results = connectToMySQL('users').query_db(query, data)
        # results will be a list of posts with the attached comments
        movie = cls(results[0])
        for row_from_db in results: 
        #Now we parse the user data to make instances of comments and add them into our list. 
            user_data = {
                "id": row_from_db["users.id"], 
                "first_name": row_from_db["first_name"],
                "last_name" : row_from_db["last_name"],
                "username": row_from_db["username"],
                "email": row_from_db["email"],
                "password": row_from_db["password"],
                "created_at": row_from_db["comments.created_at"],
                "updated_at" : row_from_db ["comments.updated_at"]
            }
            movie_model.reviews.append(review_model.Review(user_data))
            # why is movie_model undefined?
        return movie 
    
    # will list all the movies a actor/ actress is in. 
    @classmethod 
    def get_movies_with_actor(cls,data): 
        query = "SELECT * FROM movies LEFT JOIN movies_has_actors ON movies_has_actors.movie_UUID = movies.UUID LEFT JOIN actors ON movies_has_actors.actor_UUID = actors.UUID WHERE movies.UUID = %(UUID)s;" 
        results = connectToMySQL(cls.db_name).query_db(query,data) 

        movie = cls(results[0]) 
        for row in results: 
            actor_info = { 
                'UUID' : row['actors.UUID'], 
                'name' : row['name'], 
            } 
            print("++++++++++++")
            movie.actor.append(actor_model.Actor(actor_info))
            # edited 
        return movie 

    #DELETE - you cant  delete these movies, only on reviews

    # this actually makes the many to many connection
    @classmethod
    def create_watchlist(cls,data):
        query = "INSERT INTO watchlist (user_id, movie_UUID) VALUES (%(user_id)s, %(movie_UUID)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)
        