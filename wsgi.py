from tapes import app

if __name__ == "__main__":
    app.run(debug=True)

from tapes import db
db.create_all()
