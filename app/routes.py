from app import app

@app.route('/')
def homePage():
    return {
        'test':'hi'
    }
