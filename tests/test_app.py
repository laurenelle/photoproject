import Dev
app = Dev.app.test_client()

def test_index():
	''' test that index page returns status code of 200'''
	result = app.get('/')
	assert result.status_code == 200

def test_upload():
	''' test that upload page returns status code of 200'''
	result = app.get('/upload')
	assert result.status_code == 200

# all routes
# -test functions
# -database mocks -- test  
# 200


# testing inputs -- right and wrong