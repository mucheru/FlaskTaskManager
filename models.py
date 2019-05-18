from app import  db

# creating tables

class TaskModels(db.Model):
    __tablename__='tasks'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(500))
    description = db.Column(db.String(500))
    startdate= db.Column(db.String(100))
    enddate = db.Column(db.String(100))
    status = db.Column(db.String(100))

    # creating crude insert

    def insert_record(self):
        db.session.add(self)
        db.session.commit()

        # read all records
    @classmethod

    def real_all(cls):
        return cls.query.all()

#     update a record
    @classmethod
    def update_by_id(cls,id,title=None, description = None, startdate= None, enddate=None, status=None):
        record=cls.query.filter_by(id=id).first()
        if title:
            record.title=title
        if description:
            record.decription=description
        if startdate:
            record.startdate=startdate
        if enddate:
            record.enddate=enddate
        if status:
            record.status=status
        db.session.commit()
        return True


    @classmethod
    def delete_by_id(cls,id):
        record =cls.query.filter_by(id=id)
        if record.first():
            record.delete()
            db.session.commit()
            return True
        else:
            return False
