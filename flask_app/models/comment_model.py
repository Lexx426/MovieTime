from flask_app.config.mysqlconnection import connectToMySQL 
from flask import flash
from flask_app.models import user_model
from flask_app.models import movie_model

class Comment:
    db_name = "group_project"
    
    def __init__(self,data): 
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data ['updated_at']
        self.movie_id = data ['movie_id']
        self.user_id = data ['user_id']
        
        
    @classmethod
    def save(cls,data):
        query = "INSERT INTO comments (content, movie_id, user_id) VALUES (%(content)s,%(movie_id)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    #DESCENDING ORDER BY POST
    @classmethod
    def get_all_comments(cls):
        query = "SELECT * FROM comments;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_comments = []
        for row in results: 
            print(row['content'])
            all_comments.append(cls(row))
        return all_comments
    
    @classmethod
    def get_one_comment(cls, data): 
        query = "SELECT * FROM comments where id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])
    
    
    @classmethod
    def movie_with_comment(cls,data):
        query = "SELECT comments.* FROM movies JOIN comments on comments.movie_id = movies.id WHERE movies.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        comments = []
        for row in results:
            one_comment = cls(row)
            one_comment.user = user_model.User.get_by_id({'id': row["user_id"]})
            comments.append(one_comment)
        return comments

    @classmethod
    def get_comments_for_one_movie(cls,data): 
        query = "SELECT * FROM comments JOIN users ON comments.user_id = users.id WHERE movie_id = %(movie_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        comments = []
        for row in results: 
            one_comment = (cls(row))
            one_comment.user = user_model.User.get_by_id({"id": row["users.id"]})
            comments.append(one_comment)
        return comments 
    
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM comments WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
        
    