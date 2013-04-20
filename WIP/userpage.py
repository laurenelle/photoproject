ORIGINAL



@app.route("/userpage")
def user_page():
    g.user_id = session.get('user_id')
    user = db_session.query(User).filter_by(id=g.user_id).one()

    return render_template("userpage.html", u=user)




_____________________________________________________________________





@app.route("/userpage")
def user_page():
	g.user_id = session.get('user_id')
	if not g.user_id:
		flash("Please log in", "warning")
		return redirect(url_for("index"))
	user = db_session.query(User).filter_by(id=g.user_id).one()
	photos = db_session.query(Photo).filter_by(user_id=g.user_id).all()

    return render_template("userpage.html", u=user, photos=photos)
____________________________________________________

@app.route("/my_ratings")
def my_ratings():
    if not g.user_id:
        flash("Please log in", "warning")
        return redirect(url_for("index"))

    ratings = db_session.query(Rating).filter_by(user_id=g.user_id).all()
    return render_template("my_ratings.html", ratings=ratings)