from flask import redirect,render_template,request,session,Flask
from models import *

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
db.init_app(app)

app.config['SECRET_KEY'] = 'thisistejaticketbooking'

app.app_context().push()


@app.route("/all_venue")
def all_venues():
    venues = Venue.query.all()
    return render_template("all_venues.html", venues = venues)

@app.route("/add_venue" , methods =['GET','POST'])
def add_venue():
    if request.method == 'GET':
        return render_template('add_venue_form.html')
    if request.method == 'POST':
        name = request.form.get("name")
        place = request.form.get("place")
        capacity = request.form.get("capacity")
        ven = Venue(
            name = name,
            place = place,
            capacity = capacity
        )
        db.session.add(ven)
        db.session.commit()
        return redirect("/all_venue")

@app.route('/see_show/<int:id>' , methods = ['GET','POST'])
def venue_show(id):
    v1 = Venue.query.get(id)
    shows = v1.shows
    return render_template('venue_show.html',v1 = v1, shows = shows)

@app.route('/add_show/<int:id>', methods=['GET','POST'])
def add_show(id):
    if request.method == 'GET':
        v1 = Venue.query.get(id)
        return render_template('add_show_form.html', v1 = v1)
    if request.method == 'POST':
          name = request.form.get('name')
          rating = request.form.get('rating')
          timing = request.form.get('timing')
          tags = request.form.get('tags')
          price = request.form.get('price')
          v_id = request.form.get('v_id')
    show = Show(
         name = name,
         rating = rating,
         timing = timing,
         tags = tags,
         price = price 
         )
    v1 = Venue.query.get(id)
    if v1 is not None:
        db.session.add(show)
        v1.shows.append(show)
        db.session.commit()
    else:
        print("Venue with id {v_id} not found")
    dynamic_endpoint = '/see_show/' + str(id)
    return redirect(dynamic_endpoint)

@app.route('/delete_venue/<int:id>' , methods =['GET','POST'])
def delete_venue(id):
    if(request.method == 'GET'):
        v1 = Venue.query.get(id)
        return render_template('confirmation_admin_form.html',v1 = v1)
    if (request.method == 'POST'):
        if 'user_id' in session:
            user_id = session['user_id']
            username = request.form.get("username")
            password = request.form.get("password")
            user= Admin.query.filter_by(id=user_id).first()
            if(username==user.username and password==user.password):
                b1=Booking.query.filter_by(venue_id=id).all()
                for i in b1:
                    db.session.delete(i)
                s1=Show.query.filter_by(venue_id=id).all()
                for i in s1:
                    db.session.delete(i)
                db.session.commit() 
                v1 = Venue.query.get(id)
                db.session.delete(v1)
                db.session.commit()
                return redirect('/all_venue')
            else:
                return 'Invalid username or password.Please type correct username and password'
    
@app.route('/edit_venue/<int:id>',methods = ['GET','POST'])
def edit_venue(id):
    if request.method == 'GET':
        v1 = Venue.query.get(id)
        return render_template('edit_venue_form.html',v1 = v1)
    if request.method == 'POST':
        v1 = Venue.query.get(id)
        v1.name = request.form.get("u_name")
        v1.place = request.form.get("u_place")
        v1.capacity = request.form.get("u_capacity")
        db.session.commit()
        return redirect("/all_venue")

@app.route('/edit_show/<int:id>', methods = ['GET','POST'])
def edit_show(id):
    if request.method == 'GET':
        s1 = Show.query.get(id)
        venues = Venue.query.all()
        return render_template('edit_show_form.html',s1 = s1 , venues = venues)
    if request.method == 'POST':
        s1 = Show.query.get(id)
        s1.name    = request.form.get("u_name")
        s1.rating  = request.form.get("u_rating")
        s1.timing  = request.form.get("u_timing")
        s1.tags    = request.form.get("u_tags")
        s1.price   = request.form.get("u_price")
        s1.v_id    = request.form.get('u_v_id')
        db.session.commit()
        return redirect('/all_venue')
    
@app.route('/delete_show/<int:id>', methods = ['GET','POST'])
def delete_show(id):
    if(request.method == 'GET'):
        s1 = Show.query.get(id)
        return render_template('confirmation_admin_forms.html',s1=s1)
    if(request.method == 'POST'):
        user_id = session ['user_id']
        username = request.form.get("username")
        password = request.form.get("password")
        admin= Admin.query.filter_by(id=user_id).first()
        if(username == admin.username and password == admin.password):
            b1=Booking.query.filter_by(show_id=id).all()
            for i in b1:
                db.session.delete(i)
            db.session.commit()
            s1 = Show.query.get(id)
            db.session.delete(s1)
            db.session.commit()
            return redirect('/all_venue')
        else:
            return 'Invalid Username or password.Please type correct username and password'
    
@app.route('/user_dashboard')
def user_dashboard():
    venues = Venue.query.all()
    return render_template('user_dashboard.html',venues = venues)

@app.route('/ven_shows/<int:id>')
def ven_shows(id):
    v1 = Venue.query.get(id)
    shows = v1.shows
    return render_template('ven_shows.html',v1 = v1, shows=shows)

@app.route("/book_tickets/<int:id>",methods = ['POST', 'GET'])
def book_tickets(id):
    s1 = Show.query.get(id)
    v_iid = s1.venue_id
    v2 = Venue.query.get(v_iid)
    price = s1.price
    all_bookings_data=Booking.query.all()
    num_booked_seats = 0
    num_available_seats = 0
    for single_booking in all_bookings_data:
        if v2.v_id == single_booking.venue_id:
            num_booked_seats += single_booking.num_seats
    num_available_seats = v2.capacity-num_booked_seats
    num_seats = 0
    total_price = num_seats * price
    if request.method == "POST" :
        num_seats = int(request.form.get('num_seats'))
        if num_seats <= num_available_seats:
            total_price = num_seats * price
            user_id = session['user_id']
            book = Booking(user_id = user_id,show_id = id,venue_id=v2.v_id,num_seats=num_seats,total_price=total_price)
            db.session.add(book)
            db.session.commit()
        return render_template('booking_confirmed.html',s1=s1,v2 =v2,num_seats=num_seats,total_price=total_price,all_bookings_data=all_bookings_data)
    return render_template('book_tickets.html',s1=s1,v2 =v2,num_available_seats=num_available_seats,num_seats=num_seats)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/userlogin', methods =['GET','POST'])
def login():
    if request.method == "GET":
        return render_template("userlogin.html")
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username = username).all()
        for i in user:
            if i.username == username and i.password == password:
                session['username'] =  username
                session['user_id'] = i.id
                return redirect('/user_dashboard')
            else:
                return "Invalid username or password"
        
@app.route('/adminlogin', methods =['GET','POST'])
def adminlogin():
    if request.method == "GET":
        return render_template("adminlogin.html")
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin.query.filter_by(username = username).first()
        if admin.username == username and admin.password == password:
            session['username'] = username
            session['user_id'] = admin.id
            return redirect('/all_venue')
        else:
            return "Invalid username or password"
        
@app.route('/userregister' , methods = ['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('userregister.html')
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = User(username = username,password = password)
        use = User.query.filter_by(username = username).all()
        for i in use:
            if i.username == username:
                return 'Username already exists.Please try using other username'
        db.session.add(user)
        db.session.commit()
        return redirect('/userlogin')
    
@app.route('/adminregister' , methods = ['GET','POST'])
def adminregister():
    if request.method == 'GET':
        return render_template('adminregister.html')
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin(username = username,password = password)
        db.session.add(admin)
        db.session.commit()
        return redirect('/adminlogin')
    
@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username',None)
        return render_template('logout.html')
        
@app.route('/search',methods = ['POST'])
def search():
    if request.method == "POST":
        name = request.form.get("name")
        venues=Venue.query.filter_by(name=name).all()
        return render_template('user_dashboard.html',venues = venues)
    
@app.route('/search1/<int:v_id>',methods = ['POST'])
def search1(v_id):
    if request.method == "POST":
        name = request.form.get("name")
        venue=Venue.query.get(v_id)
        shows = Show.query.filter_by(name=name).all()
        return render_template('ven_shows.html',shows=shows,v1=venue)

@app.route('/bookings',methods=["GET","POST"])
def bookings():
    if 'username' in session:
        user_id = session['user_id']
        booking = Booking.query.filter_by(user_id=user_id).all()
        v2,s1=[],[]
        for i in booking:
            currvenue=Venue.query.get(i.venue_id)
            currshow=Show.query.get(i.show_id)
            s1.append(currshow)
            v2.append(currvenue)
        final_res=list(zip(s1,v2,booking))
        print(final_res)
        return render_template('bookings.html', booking=booking,final_res=final_res)

if __name__ == '__main__':  
    app.run(debug = True)