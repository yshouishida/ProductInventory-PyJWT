from flask import Flask
from routes.auth import auth
from routes.products import products
from routes.users import users

app =  Flask(__name__)

app.register_blueprint(auth)
app.register_blueprint(products)
app.register_blueprint(users)

if __name__ == "__main__":
    app.run(debug=True)

    