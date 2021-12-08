
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#init app
app =Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

#database
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Init db
db =SQLAlchemy(app)

#Init marshmallow
ma = Marshmallow(app) 

#Account Class/Model
class Account(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String(100),unique=True)
    address = db.Column(db.String(200))
    telephone =db.Column(db.Integer(10))
    accno =db.Column(db.Integer)
    acctype =db.Column(db.String(50))
    nic =db.Column(db.String(10))
    def __init__(self, name, address, telephone,accno,acctype,nic):
        self.name = name
        self.address = address
        self.telephone = telephone
        self.accno = accno
        self.acctype = acctype
        self.nic = nic

#account Schema
class AccountSchema(ma.Schema):
    class Meta:
        fields = ('id','name','address','telephone','accno','acctype','nic')


#add account
@app.route('/account',methods =['POST'])
def add_account():
    name = request.json['name']
    address = request.json['address']
    telephone = request.json['telephone']
    accno = request.json['accno']
    acctype = request.json['acctype']
    nic = request.json['nic']

    new_account = Account(name,address,telephone,accno,acctype,nic)

    db.session.add(new_account)
    db.session.commit()

    return account_schema.jsonify(new_account)


#Get all account
@app.route('/account',methods=['GET'])
def get_accounts():
    all_accounts = Account.query.all()
    result =accounts_schema.dump(all_accounts)
    return jsonify(result.data)


#Get single account
@app.route('/account/<id>',methods=['GET'])
def get_account(id):
    account = Account.query.get(id)
    return account_schema.jsonify(Account)


#Update account
@app.route('/account/<id>',methods =['PUT'])
def update_account(id):
    account = Account.query.get(id)
    name = request.json['name']
    address = request.json['address']
    telephone = request.json['telephone']
    accno = request.json['accno']
    acctype = request.json['acctype']
    nic = request.json['nic']

    account.name = name
    account.address = address
    account.telephone = telephone
    account.accno = accno
    account.acctype = acctype
    account.nic = nic

    db.session.commit()

    return account_schema.jsonify(account)

#Delete account
@app.route('/account/<id>',methods=['DELETE'])
def delete_account(id):
    account = Account.query.get(id)
    db.session.delete(account)
    db.session.commit()

    return account_schema.jsonify(Account)





#Init schema
account_schema = AccountSchema(strict=True)
accounts_schema = AccountSchema(many =True, strict=True)
        

#Run Server
if __name__ == '__main__':
    app.run(debug=True)
