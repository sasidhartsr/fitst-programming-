import json
from datetime import datetime
import psycopg2
from flask import Flask, request
from flask_restful import Api
from sqlalchemy import Column, String, Integer, Date, BOOLEAN, and_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

app = Flask(__name__)
api = Api(app)
Base = declarative_base()
database_url = "postgresql://postgres:1234@localhost:5432/postgres"
engine = create_engine(database_url, echo=True, poolclass=NullPool)
Session = sessionmaker(bind=engine)
session = Session()


class KxnCompany(Base):
    __tablename__ = "kxncompany"
    Name = Column("name", String)
    age = Column("age", Integer)
    address = Column("address", String)
    Mobile = Column("mobileno", Integer, primary_key=True)
    City = Column("city", String)
    Create_date = Column("create_date", String)
    sentEmployee = Column("sent_employee", BOOLEAN)


@app.route('/newLeads', methods=['GET'])
def new_leads():
    Name1 = request.args.get('name')
    results = session.query(KxnCompany).filter(KxnCompany.Name == Name1).all()
    resutlstsr = [item.__dict__ for item in results]
    print()
    print("resutlstsr ", resutlstsr)
    print()

    mob_no_list = []
    for item in resutlstsr:

        del item['_sa_instance_state']
        mob_no_list.append(item.get('Mobile'))
    print()
    print("mob_no_list ", mob_no_list)
    enable_sent_flag(mob_no_list)
    return json.dumps(resutlstsr)

def enable_sent_flag(mob_no_list):
    for item1 in mob_no_list:
        print("item is ", item1)
        session.query(KxnCompany).filter(KxnCompany.Mobile == item1).update({"sentEmployee": True})
        session.commit()

app.run(debug=True)

#                                   "full table view"

# # http://127.0.0.1:5000/KxnCompany/get/fullView/details
# @app.route('/KxnCompany/get/fullView/details', methods=['GET'])
# def home():
#     results = session.query(KxnCompany).all()
#     results_1 = [item.__dict__ for item in results]
#     for item in results_1:
#         del item['_sa_instance_state']
#     return json.dumps(results_1)
# app.run(debug=True)

#                                   "one column show(mobile)"
# http://127.0.0.1:5000/KxnCompany/get/mobileColumn/details?mobile=1234567890
# @app.route('/KxnCompany/get/mobileColumn/details', methods=['GET'])
# def home():
#     mobileNumber = request.args.get('mobile')
#     results = session.query(KxnCompany).filter(KxnCompany.Mobile == mobileNumber).all()
#     results_3=[item.__dict__ for item in results]
#     for item in results_3:
#         del item['_sa_instance_state']
#     return json.dumps(results_3)
# app.run(debug=True)
#                               "and show(mobile & name)"
# #http://127.0.0.1:5000/KxnCompany/get/and/mobile/name/data?mobile=7097535317&name=sasi
# @app.route('/KxnCompany/get/and/mobile/name/data', methods=['GET'])
# def home():
#     mobileNumber = request.args.get('mobile')
#     NameFull=request.args.get('name')
#     results = session.query(KxnCompany).filter(and_(KxnCompany.Mobile == mobileNumber,KxnCompany.Name ==NameFull)).all()
#     results4=[item.__dict__ for item in results]
#     for item in results4:
#         del item['_sa_instance_state']
#     return json.dumps(results4)
# app.run(debug=True)
#                                         "or show(mobile & name)"
# #http://127.0.0.1:5000/KxnCompany/get/or/mobile/name/data?mobile=9618115355&name=sagar
# @app.route('/KxnCompany/get/or/mobile/name/data', methods=['GET'])
# def home():
#     mobileNumber = request.args.get('mobile')
#     NameFull=request.args.get('name')
#     results = session.query(KxnCompany).filter(or_(KxnCompany.Mobile == mobileNumber,KxnCompany.Name ==NameFull)).all()
#     results4=[item.__dict__ for item in results]
#     for item in results4:
#         del item['_sa_instance_state']
#     return json.dumps(results4)
# app.run(debug=True)

#                                       'limite&offset'
# http://127.0.0.1:5000/KxnCompany/get/limite/offset/data
# @app.route('/KxnCompany/get/limite/offset/data', methods=['GET'])
# def get_limited_data():
#     # Limit: How many leads to distribute, offset: Stating point
#     result = session.query(KxnCompany).limit(1).offset(2).all()
#     results5 = [item.__dict__ for item in result]
#     for item in results5:
#         del item['_sa_instance_state']
#     return json.dumps(results5)
#
# app.run(debug=True)

# # http://127.0.0.1:5000/KxnCompany/date/update?startdate=2022-1-1&enddate=2022-1-6
# @app.route('/KxnCompany/date/update', methods=['GET'])
# def home():
#     start_date = request.args.get("startdate")
#     end_date = request.args.get("enddate")
#     result = session.query(KxnCompany). \
#         filter(KxnCompany.Create_date >= start_date,
#                KxnCompany.Create_date < end_date).all()
#     results_6 = [item.__dict__ for item in result]
#     for item in results_6:
#         del item['_sa_instance_state']
#     return json.dumps(results_6)
#
# app.run(debug=True)
#                                            " PATCH METHAODS"
# #http://127.0.0.1:5000/KxnCompany/date/update/address?mobile=70975378887&address=tiruapti
# @app.route('/KxnCompany/date/update/address', methods=['PATCH'])
# def KxnCompany_update_address():
#         mobile = request.args.get('mobile')
#         address = request.args.get('address')
#         session.query(KxnCompany).filter(KxnCompany.Mobile == mobile).update({"address": address})
#         session.commit()
#         return "address has been updated"
# app.run(debug=True)
