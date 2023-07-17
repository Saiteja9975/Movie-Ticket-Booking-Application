from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Venue(db.Model):
    v_id =db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(50),nullable = False)
    place = db.Column(db.String(50),nullable = False)
    capacity = db.Column(db.Integer,nullable = False)
    shows = db.relationship("Show", backref = "venue")
    bookings = db.relationship('Booking',backref = 'venue')
    
    
    def __repr__(self):
        return f'<venue {self.name}>'

class Show(db.Model):
    s_id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(50),nullable = False)
    rating = db.Column(db.Integer,nullable = False)
    timing = db.Column(db.String(50),nullable  = False)
    tags = db.Column(db.String(50),nullable = False)
    price = db.Column(db.Integer,nullable = False)
    venue_id = db.Column(db.Integer,db.ForeignKey("venue.v_id"))
    # venue = db.relationship("Venue",back_populates = 'shows')
    bookings = db.relationship('Booking',backref='show')

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(30),nullable = False , unique = True) 
    password = db.Column(db.String(60), nullable = False)
    bookings = db.relationship('Booking',backref='user')


class Admin(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(30),nullable = False , unique = True) 
    password = db.Column(db.String(60), nullable = False)

class Booking(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False)
    show_id = db.Column(db.Integer,db.ForeignKey('show.s_id'))
    venue_id = db.Column(db.Integer,db.ForeignKey('venue.v_id'))
    num_seats =db.Column(db.Integer,nullable = False)
    total_price = db.Column(db.Integer,nullable=False)


