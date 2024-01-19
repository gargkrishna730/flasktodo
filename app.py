from flask import Flask,render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500) , nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow )

    def __repr__(self)-> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods = ['GET','POST'])
def hello_world():
    if request.method == 'POST':
        title =request.form['title']
        desc = request.form['desc']

        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        
        db.session.commit()
    search_query = request.args.get('search_query', '')
    if search_query:
        # Use an OR condition to search for matching titles or descriptions
        allTodo = Todo.query.filter(or_(Todo.title.ilike(f'%{search_query}%'), Todo.desc.ilike(f'%{search_query}%'))).all()
    else:

        allTodo = Todo.query.all()
    return render_template('index.html',allTodo=allTodo)
@app.route('/search', methods=['GET'])
def search():
    # Redirect to the main route with the search query as a parameter
    search_query = request.args.get('search_query', '')
    return redirect(url_for('hello_world', search_query=search_query))

@app.route('/about')
def about_us():
    return render_template('about_us.html')

@app.route('/update/<int:sno>', methods = ['GET','POST'])
def update(sno):
    if request.method == 'POST':
        title =request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    
    app.run(debug=True)