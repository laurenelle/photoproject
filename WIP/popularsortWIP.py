
1.

select photo_id,  sum( 1 / ( (extract(epoch from now()) - extract(epoch from timestamp))/60/60/24 ) * value ) from votes group by photo_id;

2. Derivatives...

select photo_id,  sum( 1 / ( (extract(epoch from now()) - extract(epoch from timestamp))/60/60/24 ) * value ) from votes;

select sum( 1 / ( (extract(epoch from now()) - extract(epoch from timestamp))/60/60/24 ) * value ) from votes;

select 1 / ( (extract(epoch from now()) - extract(epoch from timestamp))/60/60/24 ) * value from votes;

select 1 / ( (extract(epoch from now()) - extract(epoch from timestamp))/60/60/24 ) from votes;









@app.route("/movie/<int:id>", methods=["GET"])
def view_movie(id):
    movie = db_session.query(Movie).get(id)
    ratings = movie.ratings
    rating_nums = []
    user_rating = None
    for r in ratings:
        if r.user_id == session['user_id']:
            user_rating = r
        rating_nums.append(r.rating)
    avg_rating = float(sum(rating_nums))/len(rating_nums)

    prediction = None
    if not user_rating:
        user = db_session.query(User).get(g.user_id) 
        prediction = user.predict_rating(movie)
        print prediction
    
    return render_template("movie.html", movie=movie, 
            average=avg_rating, user_rating=user_rating,
            prediction = prediction)








    epoch = datetime(1970, 1, 1)

def epoch_seconds(timestamp):
    """Returns the number of seconds from the epoch to date."""
    td = date - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

def score(upvote, downvote):
    return upvote - downvote

def hot(upvote, downvote, timestamp):
    """The hot formula. Should match the equivalent function in postgres."""
    s = score(ups, downs)
    order = log(max(abs(s), 1), 10)
    sign = 1 if s > 0 else -1 if s < 0 else 0
    seconds = epoch_seconds(date) - 1134028003
    return round(order + sign * seconds / 45000, 7)