import logging
from flask_pymongo import pymongo
from flask import jsonify, request

con_string = "mongodb+srv://ramya:muruga@cluster0.x57r05g.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(con_string)
db = client.get_database('testdb')
user_collection = pymongo.collection.Collection(db, 'usercollection')
print("Mongo db connected successfully")


def project_api_routes(endpoints):
    @endpoints.route('/hello', methods=['GET'])
    def hello():
        res = 'Hello World'
        print('Hello World')
        return res

    @endpoints.route('/register-user', methods=['POST'])
    def register_user():
        resp = {}
        try:
            req_body = request.json
            user_collection.insert_one(req_body)
            print("user data successfully added")
            status1 = {
                "statusCode": "200",
                "statusMessage": "User data successfully stored"
            }
        except Exception as e:
            print(e)
            status1 = {
                "statusCode": "400",
                "statusMessage": str(e)
            }
        resp["status"] = status1
        return resp

    @endpoints.route('/read_users', methods=['GET'])
    def read_users():
        resp = {}
        try:
            users = user_collection.find({})
            print(users)
            users = list(users)
            print("user data retrieved successfully")
            status = {
                "statusCode": "200",
                "statusMessage": "User data successfully retrieved"
            }
            output = [{'Name': user['name'], 'Email': user['email']} for user in users]
            resp['data'] = output
        except Exception as e:
            print(e)
            status = {
                "statusCode": "400",
                "statusMessage": str(e)
            }
        resp["status"] = status
        return resp

    @endpoints.route('/update-users', methods=['PUT'])
    def update_users():
        resp = {}
        try:
            req_body = request.json
            user_collection.update_one({"id": req_body['id']}, {"$set": req_body['updated_user_body']})
            print("user updated successfully")
            status = {
                "statusCode": "200",
                "statusMessage": "User data successfully updated"
            }
        except Exception as e:
            status = {
                "statusCode": "400",
                "statusMessage": str(e)
            }
        resp["status"] = status
        return resp

    @endpoints.route('/delete', methods=['DELETE'])
    def delete():
        resp = {}
        try:
            delete_id = request.args.get('delete_id')
            user_collection.delete_one({"id": delete_id})
            status = {
                "statusCode": "200",
                "statusMessage": "User data successfully deleted"
            }

        except Exception as e:
            status = {
                "statusCode": "400",
                "statusMessage": str(e)
            }
        resp["status"] = status
        return resp

    return endpoints
