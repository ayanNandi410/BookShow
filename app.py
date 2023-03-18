from __init__ import create_app
from constants import BASE_URL

app,api = create_app()

if __name__ == '__main__':
    app.run("127.0.0.1", debug=True)