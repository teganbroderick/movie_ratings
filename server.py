"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/register", methods=["GET"])
def register_user():
    """render template registration.html"""
    return render_template("registration.html")


@app.route("/register_process", methods=["POST"])
def register_process():
    """Check to see if user exists, if not, add them to user table"""

    email = request.form['email']
    password = request.form['password']

    #check to see if email and password are in the user database
    replicate_email = User.query.filter_by(email=email).first()
 
    if replicate_email == None:
        #add user to database
        user_info = User(email=email, password=password)
        db.session.add(user_info)
        db.session.commit()
        return redirect('/')
    else: 
        flash("Email already exists.")
        return redirect("/register")


@app.route("/login", methods=["GET"])
def login():
    """redirect to loginin.html"""

    return render_template("loginin.html")


@app.route("/login_process", methods=["POST"])
def login_process():
    """Check to see if email matches password in user table
    if yes - redirect to homepage and show flash message
    if no - redirect to login to try again and show flash message"""

    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email, password=password).first()

    if user == None:
        flash("Wrong password or Email!")
        return redirect('/login')
    else:
        session['user_id'] = user.user_id
        flash("Logged in!")
        return redirect('/')


@app.route("/logout")
def logout():
    #delete info from session
    session.pop('user_id')
    #From solution: del session["user_id"]

    return redirect('/')

@app.route("/movies")
def movie_list():

    # gets list of tuples => movies = db.session.query(Movie.title, Movie.movie_id).all()
    movies = Movie.query.order_by('title').all()

    return render_template("movie_list.html", movies=movies)

@app.route("/movie_details/<int:movie_id>")
def movie_details(movie_id):
    """Show all ratings for a movie, give option for adding a rating"""

    #route info < >: got movie_id string from html, converted string to integer

    movie = Movie.query.get(movie_id) #create movie object using movie_id
    movie_rating = movie.ratings #Backref relationship exists, so we can get ratings using the movie object
    
    for rating in movie_rating: #loop over list of ratings
        print(rating.score) #print score using the relationship with ratings

    #suggested next step: also get user email
    
    return render_template("movie_details.html", movie_rating=movie_rating)





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
