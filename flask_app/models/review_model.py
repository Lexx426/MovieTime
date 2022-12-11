from flask_app.config.mysqlconnection import connectToMySQL 
from flask import flash
from flask_app.models import user_model
from flask_app.models import movie_model

class Review:
    db_name = "letterbox"
    
    def __init__(self,data): 
        self.id = data['id']
        self.title_post = data['title_post']
        self.content = data['content']
        self.rating = data['rating']
        self.created_at = data['created_at']
        self.updated_at = data ['updated_at']
        self.user_id = data ['user_id']
        self.movie_UUID = data ['movie_UUID']

        
        
    @classmethod
    def save(cls,data):
        query = "INSERT INTO reviews (title_post,content, rating, movie_UUID, user_id) VALUES (%(title_post)s,%(content)s,%(rating)s,%(movie_UUID)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    #DESCENDING ORDER BY POST
    @classmethod
    def get_all_comments(cls):
        query = "SELECT * FROM reviews;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_reviews = []
        for row in results: 
            print(row['title_post'], row['content'], row['rating'])
            all_reviews.append(cls(row))
        return all_reviews
    
    @classmethod
    def get_one_review(cls, data): 
        query = "SELECT * FROM reviews where id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])
    
    
    @classmethod
    def movie_with_review(cls,data):
        query = "SELECT reviews.* FROM movies JOIN comments on reviews.movie_UUID = movies.UUID WHERE movies.UUID = %(UUID)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        reviews= []
        for row in results:
            one_review = cls(row)
            one_review.user = user_model.User.get_by_id({'id': row["user_id"]})
            reviews.append(one_review)
        return reviews

    @classmethod
    def get_reviews_for_one_movie(cls,data): 
        query = "SELECT * FROM reviews JOIN users ON reviews.user_id = users.id WHERE movie_UUID = %(movie_UUID)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        reviews = []
        for row in results: 
            one_review = (cls(row))
            one_review.user = user_model.User.get_by_id({"id": row["users.id"]})
            reviews.append(one_review)
        return reviews 
    
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM reviews WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
        
    