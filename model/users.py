""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
class Post(db.Model):
    __tablename__ = 'posts'

    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, unique=False, nullable=False)
    image = db.Column(db.String, unique=False)
    # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Constructor of a Notes object, initializes of instance variables within object
    def __init__(self, id, note, image):
        self.userID = id
        self.note = note
        self.image = image

    # Returns a string representation of the Notes object, similar to java toString()
    # returns string
    def __repr__(self):
        return "Notes(" + str(self.id) + "," + self.note + "," + str(self.userID) + ")"

    # CRUD create, adds a new record to the Notes table
    # returns the object added or None in case of an error
    def create(self):
        try:
            # creates a Notes object from Notes(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Notes table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read, returns dictionary representation of Notes object
    # returns dictionary
    def read(self):
        # encode image
        path = app.config['UPLOAD_FOLDER']
        file = os.path.join(path, self.image)
        file_text = open(file, 'rb')
        file_read = file_text.read()
        file_encode = base64.encodebytes(file_read)
        
        return {
            "id": self.id,
            "userID": self.userID,
            "note": self.note,
            "image": self.image,
            "base64": str(file_encode)
        }

# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class QuizScores(db.Model):
    __tablename__ = 'quizScores'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _email = db.Column(db.String(255), unique=True, nullable=False)
    _quiz1Score = db.Column(db.Integer, unique=False, nullable=False)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, email, quiz1Score):
        self._email = email
        self._quiz1Score = quiz1Score

    # a getter method, extracts email from object
    @property
    def email(self):
        return self._email
    
    # a setter function, allows name to be updated after initial object creation
    @email.setter
    def email(self, email):
        self._email = email
        
    # a getter method, extracts email from object
    @property
    def quiz1Score(self):
        return self._quiz1Score
    
    # a setter function, allows name to be updated after initial object creation
    @quiz1Score.setter
    def quiz1Score(self, quiz1Score):
        self._quiz1Score = quiz1Score
        
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "email": self.email,
            "quiz1Score": self.quiz1Score,
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, email="", quiz1Score=""):
        """only updates values with length"""
        if len(email) > 0:
            self.email = email
        self.quiz1Score = quiz1Score
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

class QuizQuestions(db.Model):
    __tablename__ = 'quizQuestions'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    #column name must match defined variable name
    _quizQuestion = db.Column(db.String(), unique=True, nullable=False)
    _quizAnswer = db.Column(db.String(), nullable=False)
    _difficulty = db.Column(db.String(), nullable=False)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, quizQuestion, quizAnswer, difficulty):
        self._quizQuestion = quizQuestion
        self._quizAnswer = quizAnswer
        self._difficulty = difficulty

    # a getter method, extracts email from object
    @property
    def quizQuestion(self):
        return self._quizQuestion
    
    # a setter function, allows name to be updated after initial object creation
    @quizQuestion.setter
    def quizQuestion(self, quizQuestion):
        self._quizQuestion = quizQuestion
    
    
    # a getter method, extracts email from object
    @property
    def quizAnswer(self):
        return self._quizAnswer
    
    # a setter function, allows name to be updated after initial object creation
    @quizAnswer.setter
    def quizAnswer(self, quizAnswer):
        self._quizAnswer = quizAnswer
      
    # a getter method, extracts email from object
    @property
    def difficulty(self):
        return self._difficulty
    
    # a setter function, allows name to be updated after initial object creation
    @difficulty.setter
    def difficulty(self, difficulty):
        self._difficulty = difficulty  
        
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "quizQuestion": self.quizQuestion,
            "quizAnswer": self.quizAnswer,
            "difficulty": self.difficulty
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, quizQuestion="", quizAnswer="", difficulty=""):
        """only updates values with length"""
        self.quizQuestion = quizQuestion
        self.quizAnswer = quizAnswer
        self.difficulty = difficulty
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class User(db.Model):
    __tablename__ = 'users'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _email = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)
    _dob = db.Column(db.Date)

    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    posts = db.relationship("Post", cascade='all, delete', backref='users', lazy=True)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, email, password="123qwerty", dob=date.today()):
        self._name = name    # variables with self prefix become part of the object, 
        self._email = email
        self.set_password(password)
        self._dob = dob

    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    # a getter method, extracts email from object
    @property
    def email(self):
        return self._email
    
    # a setter function, allows name to be updated after initial object creation
    @email.setter
    def email(self, email):
        self._email = email
        
    # check if uid parameter matches user id in object, return boolean
    def is_email(self, email):
        return self._email == email
    
    @property
    def password(self):
        return self._password[0:10] + "..." # because of security only show 1st characters

    # update password, this is conventional setter
    def set_password(self, password):
        """Create a hashed password."""
        self._password = generate_password_hash(password, method='sha256')

    # check password parameter versus stored/encrypted password
    def is_password(self, password):
        """Check against hashed password."""
        result = check_password_hash(self._password, password)
        return result
    
    # dob property is returned as string, to avoid unfriendly outcomes
    @property
    def dob(self):
        dob_string = self._dob.strftime('%m-%d-%Y')
        return dob_string
    
    # dob should be have verification for type date
    @dob.setter
    def dob(self, dob):
        self._dob = dob
    
    @property
    def age(self):
        today = date.today()
        return today.year - self._dob.year - ((today.month, today.day) < (self._dob.month, self._dob.day))
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "dob": self.dob,
            "age": self.age,
            "posts": [post.read() for post in self.posts]
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", email="", password=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(email) > 0:
            self.email = email
        if len(password) > 0:
            self.set_password(password)
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initUsers():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        u1 = User(name='Antony Yu', email='antony@gmail.com')
        u2 = User(name='Colin Weis', email='colin@gmail.com')
        u3 = User(name='Leonard Wright', email='leonard@gmail.com')
        u4 = User(name='Lily Wu', email='lily@gmail.com')
        u5 = User(name='Orlando Carcamo', email='orlando@gmail.com')
        u6 = User(name='Sachit Prasad', email='sachit@gmail.com')

        users = [u1, u2, u3, u4, u5, u6]

        """Builds sample user/note(s) data"""
        for user in users:
            try:
                '''add a few 1 to 4 notes per user'''
                for num in range(randrange(1, 4)):
                    note = "#### " + user.name + " note " + str(num) + ". \n Generated by test data."
                    user.posts.append(Post(id=user.id, note=note, image='ncs_logo.png'))
                '''add user/post data to table'''
                user.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {user.email}")

        
        q1 = QuizQuestions(quizQuestion="What do SASS variables start with?", quizAnswer="$", difficulty="easy")
        #need to remove unique=True from difficulty variable defined in QuizQuestions class, else won't show in table
        q2 = QuizQuestions(quizQuestion="Are SASS variables imperative or declarative?", quizAnswer="imperative", difficulty="easy")
        q3 = QuizQuestions(quizQuestion="Which of two variables are treated the same by SASS? || A. $coolVar and $coolvar || B. $coolVar1 and $coolVar || C. $cool_var and $cool-var || D. $cool_var and $coolVar", quizAnswer="C", difficulty="easy")

        questions = [q1, q2, q3]
        

        """Builds sample user/note(s) data"""
        for question in questions:
            try:
                question.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print("Records exist, duplicate email, or error")
            