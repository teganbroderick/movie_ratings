
import model
import seed





user = User.query.get(35)
ratings = Rating.query.filter_by(user_id=user.user_id).all()
movies = []

for r in ratings:
    movie = Movie.query.get(r.movie_id)
    movies.append(movie)


for m in movies:
    print(m.title)