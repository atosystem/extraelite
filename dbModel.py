from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import psycopg2



app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

def getComplains():
    conn = psycopg2.connect(database="d268qlch00j1lt", user="vtdymwiimcircz", password="ab0ffa3f42eda4ecb25df6a83514ca51b4fa08c69bd31e011680361b525cc54b", host="ec2-54-83-52-191.compute-1.amazonaws.com", port="5432")
    print ("Opened database successfully")

    cur = conn.cursor()

    cur.execute("SELECT complain_id,user_line_id,complain_content,agree_number  from complains;")
    rows = cur.fetchall()
    
    j_data=[]
    for row in rows:
        j_row={'complain_id':row[0],'user_line_id':row[1],'complain_content':row[2],'agree_number':row[3]}
        j_data.append(j_row)
    
    

    print ("Operation done successfully")
    conn.close()
    return j_data

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
