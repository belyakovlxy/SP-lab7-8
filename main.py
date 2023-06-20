from flask import Flask, make_response
from flask_restful import Api, Resource, request

import queries
import jwt_tokens
import sqlite3

app = Flask(__name__)
api = Api(app)


heroes = []

class AllHeroes(Resource):
    def get(self):
        verifyResult = jwt_tokens.verify("")
        if "INFO" in verifyResult.keys():
            return verifyResult
        else:
            heroes = queries.getAllHeroes()
            return {"superheroes" : heroes}
    
class Hero(Resource):
    def get(self):
        verifyResult = jwt_tokens.verify("")
        if "INFO" in verifyResult.keys():
            return verifyResult
        else:
            args = queries.my_args.parse_args()
            return queries.getHeroByName(args["superhero_name"])
         
    def post(self):
        verifyResult = jwt_tokens.verify("admin")
        if "INFO" in verifyResult.keys():
            return verifyResult
        else:
            args = queries.my_args.parse_args()
            return queries.insertHero(args)
        
    def put(self):
        verifyResult = jwt_tokens.verify("admin")
        if "INFO" in verifyResult.keys():
            return verifyResult
        else:
            args = queries.my_args.parse_args()
            return queries.updateHero(args)
    
    def delete(self):
        verifyResult = jwt_tokens.verify("admin")
        if "INFO" in verifyResult.keys():
            return verifyResult
        else:
            args = queries.my_args.parse_args()
            return queries.deleteHero(args)

class Powers(Resource):
    def get(self):
        verifyResult = jwt_tokens.verify("")
        if "INFO" in verifyResult.keys():
            return verifyResult
        else:
            args = queries.my_args.parse_args()
            return queries.getHeroSuperpowers(args)
    
    def post(self):
        verifyResult = jwt_tokens.verify("admin")
        if "INFO" in verifyResult.keys():
            return verifyResult
        else:
            args = queries.my_args.parse_args()
            return queries.insertHeroPower(args)
    
    def delete(self):
        verifyResult = jwt_tokens.verify("admin")
        if "INFO" in verifyResult.keys():
            return verifyResult
        else:
            args = queries.my_args.parse_args()
            return queries.deleteHeroPower(args)
    
    def put(self):
        verifyResult = jwt_tokens.verify("admin")
        if "INFO" in verifyResult.keys():
            return verifyResult
        else:
            args = queries.my_args.parse_args()
            return queries.updateHeroPower(args)

class Authentication(Resource):
    def post(self):
        args = queries.my_args.parse_args()
        
        role = queries.loginQuery(args)
        response = ""
        if "INFO" in role.keys():
            response = make_response(role)
        else:
            token = jwt_tokens.createJWT(args["login"], args["password"])
            response = make_response({"INFO" : "You Logged In!"})
            response.set_cookie("my_token", token)
            response.set_cookie("my_role", role["role"])
        return response

    def get(self):
        verifyResult = jwt_tokens.verify("")
        return verifyResult

api.add_resource(AllHeroes, "/heroes")
api.add_resource(Hero, "/hero")
api.add_resource(Powers, "/powers")
api.add_resource(Authentication, "/login")

if __name__ == "__main__":
    app.run(debug=True)