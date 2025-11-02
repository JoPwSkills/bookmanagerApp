from flask import Flask
from flask import render_template
from flask import request
import os
from flask_sqlalchemy import SQLAlchemy
from flask import redirect

# Database creation
project_dir = os.path.dirname(os.path.abspath(__file__))

database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__);

app.config['SQLALCHEMY_DATABASE_URI'] = database_file

db = SQLAlchemy(app)

# Define schema for our DB
class Book(db.Model):
    title = db.Column(db.String(80), unique = True, nullable=False, primary_key = True)

    def __repr__(self):
        return "<Title: {}>".format(self.title)


# api route --- api endpoint 
# CREATE and READ
@app.route("/", methods = ['GET', 'POST'])
def home():
    if request.form:
        try:
            book = Book(title=request.form.get('title'));
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            print('Failed to add book')
            print(e)
    books = Book.query.all()
    print(books);
    return render_template('home.html', books = books);

# UPDATE Endpoint
@app.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get('newtitle');
        oldtitle = request.form.get('oldtitle');
        book = Book.query.filter_by(title=oldtitle).first()
        book.title = newtitle
        db.session.commit()
    except Exception as e:
        print('Failed to update book')
        print(e)
    return redirect("/")

# DELETE Endpoint
@app.route("/delete", methods=["POST"])
def delete():
    try:
        title = request.form.get('title')
        book = Book.query.filter_by(title=title).first()

        db.session.delete(book)

        db.session.commit()
    except Exception as e:
        print('Deletion failed')
        print(e)

    return redirect("/")



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug =True) # localhost



