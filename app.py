from . import create_app
from .constants import BASE_URL

app,api = create_app()

if __name__ == '__main__':
    app.run(BASE_URL, debug=True)