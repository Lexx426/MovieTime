from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_model, actor_model, comment_model 


class Movie:
    db_name = "letterbox"
    
    def __init__(self,data): 
        self.id = data['id']
        self.rating = data['rating']
        self.title = data['title']
        self.img_path = data['img_path']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.actor = []
        # changed from none to list ( makes it class instances below)
        
    # CREATE and SAVE movie into database
    @classmethod
    def create_movie(cls,data):
        query = "INSERT INTO movies (rating, title, img_path, description, user_id) VALUES (%(rating)s,%(title)s,%(img_path)s, %(description)s,%(user_id)s);"
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
        query = "SELECT * FROM movies WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        movie = cls(results[0])
        movie.comments = comment_model.Comment.movie_with_comment({"id": results[0]["id"]})
        return movie
    
    #EDIT(Update) movie by movie's id
    @classmethod
    def update_movie(cls,data):
        query = "UPDATE movies SET rating = %(rating)s, title = %(title)s, img_path = %(img_path)s, description = %(description)s WHERE id = %(id)s"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    
    @classmethod
    def get_movie_with_comment(cls, data):
        query = "SELECT * FROM movies LEFT JOIN comments ON comments.movie_id = movies.id LEFT JOIN users ON comments.user_id = users.id WHERE movies.id = %(id)s;"
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
            movie_model.comments.append(comment_model.Comment(user_data))
        return movie 
    
    # will list all the movies a actor/ actress is in. 
    @classmethod 
    def get_movies_with_actor(cls,data): 
        query = "SELECT * FROM movies LEFT JOIN actors_has_movies ON actors_has_movies.movie_id = movies.id LEFT JOIN actors ON actors_has_movies.actor_id = actors.id WHERE movies.id = %(id)s;" 
        results = connectToMySQL(cls.db_name).query_db(query,data) 

        movie = cls(results[0]) 
        for row in results: 
            actor_info = { 
                'id' : row['actors.id'], 
                'first_name' : row['first_name'], 
                'last_name' : row['last_name'], 
                'img_path' : row['img_path'], 
                'created_at' : row['created_at'], 
                'updated_at' : row['updated_at'] 
            } 
            print("++++++++++++")
            movie.actor.append(actor_model.Actor(actor_info))
            # edited 
        return movie 

    #DELETE movie by movie's id 
    @classmethod
    def destroy(cls,data): 
        query = "DELETE FROM movies WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    #VALIDATE movie
    @staticmethod
    def validate_movie(movie):
        is_valid = True
        if (movie['rating']) == "":
            is_valid = False
            flash("Please rate this movie","movie")
        if len(movie['title']) < 2:
            is_valid = False
            flash("Title must be at least 2 characters","movie")
        if len(movie['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters","movie")
        return is_valid
        