from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
db_string = "postgres://vtdymwiimcircz:ab0ffa3f42eda4ecb25df6a83514ca51b4fa08c69bd31e011680361b525cc54b@ec2-54-83-52-191.compute-1.amazonaws.com:5432/d268qlch00j1lt"
db1 = create_engine(db_string)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

def getComplains():
    result_set = db1.execute("SELECT * FROM complains")
    return result_set

class UserData(db.Model):
    __tablename__ = 'UserData'

    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(64))
    Description = db.Column(db.String(256))
    CreateDate = db.Column(db.DateTime)

    def __init__(self
                 , Name
                 , Description
                 , CreateDate
                 ):
        self.Name = Name
        self.Description = Description
        self.CreateDate = CreateDate


if __name__ == '__main__':
    manager.run()
