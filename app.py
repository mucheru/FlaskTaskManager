from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import pygal


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:@127.0.0.1:5432/task_manager' #URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #anything happen to db report
app.config['SECRET_KEY']='steve'
db=SQLAlchemy(app=app) #creating instance of the db

from models import TaskModels

#create the table as per the given information

@app.before_first_request
def create_table():
    db.create_all()

#
# class UsersModel(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer,primary_key=True)
#     username = db.Column(db.String(120))
#
#     def save_record(self):
#         db.session.add(self)
#         db.session.commit()


@app.route('/')
def home():
    tasks=TaskModels.real_all()
    # read on  list comprehension

    statuslist = [x.status for x in tasks]
    print (statuslist)
    pie_chart = pygal.Pie()
    pie_chart.title = 'Task status)'
    pie_chart.add("completed projects",statuslist.count('complete'))
    pie_chart.add("pending projects", statuslist.count('pending'))
    pie_chart.add("cancelled projects", statuslist.count('cancel'))
    graph=pie_chart.render_data_uri()
    # print(graph)

    return  render_template('index.html',tasks=tasks,graph=graph)

# new route

@app.route('/new',methods=['POST'])
def newTask():
    if request.method=='POST':
        title=request.form['title']
        description=request.form['description']
        startdate=request.form['startdate']
        enddate=request.form['enddate']
        status=request.form['status']

        task=TaskModels(title=title,description=description,startdate=startdate,enddate=enddate,status=status)
# save
        task.insert_record()
        return redirect(url_for('home'))


@app.route('/edit/<int:id>',methods=['POST'])
def editTask(id):
    if request.method=='POST':
        title=request.form['title']
        description=request.form['description']
        startdate=request.form['startdate']
        enddate=request.form['enddate']
        status=request.form['status']
        # task=TaskModels(title=title,description=description,startdate=startdate,enddate=enddate,status=status)
        TaskModels.update_by_id(id=id,title=title,description=description,startdate=startdate,enddate=enddate,status=status)
        # task.insert_record()
        return redirect(url_for('home'))


@app.route('/delete/<int:id>')
def deleteTask(id):
    if request.method=="GET":
        TaskModels.delete_by_id(id)
        return redirect(url_for('home'))




if __name__ == '__main__':
    app.run()
