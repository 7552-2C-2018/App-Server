from server.setup import app
from server.apis import registerApi

registerApi(app)
database = app.database

if __name__ == '__main__':
    app.run(host='0.0.0.0')
