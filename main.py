from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float


app = Flask(__name__)

class Base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-bookshelf.db"

db = SQLAlchemy(model_class=Base)

db.init_app(app)


class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[str] = mapped_column(Float, nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars().all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        new_book = Book(
            title=request.form.get("title"),
            author=request.form.get("author"),
            rating=request.form.get("rating")
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("add.html")

@app.route("/delete")
def delete():
    book_id = request.args.get("id")
    book_to_delete = db.get_or_404(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/show", methods=["GET", "POST"])
def show():
    if request.method == "POST":
        book_id = request.form.get("id")
        book_to_show = db.get_or_404(Book, book_id)
        book_to_show.rating = request.form.get("rating")
        db.session.commit()
        return redirect(url_for("home"))
    book_id = request.args.get("id")
    book_to_show = db.get_or_404(Book, book_id)
    return render_template("show.html", book=book_to_show)

if __name__ == "__main__":
    app.run(debug=True)

