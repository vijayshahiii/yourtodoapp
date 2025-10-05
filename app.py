from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class ToDoApp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        task_title = request.form.get("title")
        if task_title:
            new_task = ToDoApp(title=task_title)
            db.session.add(new_task)
            db.session.commit()
        return redirect(url_for('home'))

    tasks = ToDoApp.query.all()
    return render_template("index.html", tasks=tasks)

# Delete task route
@app.route("/delete/<int:id>")
def delete_task(id):
    task = ToDoApp.query.get_or_404(id)  # get the task or return 404
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

