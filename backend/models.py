from exts import db


"""
Reference for SQL db

class Booking:
    id:int primary key
    title:str
    description:str (text)
"""

class Booking(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    title=db.Column(db.String(),nullable=False)
    description=db.Column(db.Text(),nullable=False)
    
    def __repr__(self):
        return f"<Booking {self.title} {self.description}>"
    
    # SQL commands CRUD
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self,title,description):
        self.title=title
        self.description=description


'''
class User:
    id:int primary key
    username:str
    email:str
    password:str
'''

class User(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(25),nullable=False)
    email=db.Column(db.String(80),nullable=False)
    password=db.Column(db.Text(),nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
    
    