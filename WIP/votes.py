@app.route('/vote', methods=['POST'])
def vote():
    vote = request.form['vote']
 
    if vote == "upvote":
		v = Vote(up=1, give_vote_user_id=g.user_id, photo_id=1, receive_vote_user_id=1)
		# change hard coded values when photo can be viewed
	elif vote == "downvote":
		v = Vote(down=1, give_vote_user_id=g.user_id, photo_id=1, receive_vote_user_id=1)

    db_session.add(v)
    db_session.commit()
    db_session.refresh(v)
    return render_template("vote.html")


