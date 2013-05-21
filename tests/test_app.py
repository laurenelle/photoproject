import Dev
app = Dev.app.test_client()

#test all routes

def test_index():
	''' test that index page returns status code of 200'''
	result = app.get('/')
	assert result.status_code == 200

def test_upload():
	''' test that upload page returns status code of 200'''
	result = app.get('/upload')
	assert result.status_code == 200

def test_login():
	''' test that login page returns status code of 200'''
	result = app.get('/login')
	assert result.status_code == 200

def test_signup():
	''' test that signup page returns status code of 200'''
	result = app.get('/signup')
	assert result.status_code == 200

def test_popular():
	''' test that popular page returns status code of 200'''
	result = app.get('/popular')
	assert result.status_code == 200

def test_vote():
	''' test that vote page returns status code of 200'''
	result = app.get('/vote')
	assert result.status_code == 200

def test_map():
	''' test that popular page returns status code of 200'''
	result = app.get('/map')
	assert result.status_code == 200

def test_userpage():
	''' test that popular page returns status code of 200'''
	result = app.get('/userpage')
	assert result.status_code == 200

def test_logout():
	''' test that logout page returns status code of 200'''
	result = app.get('/logout')
	assert result.status_code == 200

def test_addlocation():
	''' test that addlocation page returns status code of 200'''
	result = app.get('/addlocation')
	assert result.status_code == 200

def test_photosearch():
	''' test that photosearch page returns status code of 200'''
	result = app.get('/photosearch')
	assert result.status_code == 200

# -test functions
# -database mocks -- test  
# 200


# testing inputs -- right and wrong
# all exif function

#