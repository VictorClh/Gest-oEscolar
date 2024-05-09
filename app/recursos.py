# CRIAR NOVO ARQUIVO recursos.py
from flask_restful import Resource, reqparse
from app.models import Professores
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from blacklist import BLACKLIST
from app import db


class User_modelo(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('email')
    argumentos.add_argument('cpf')
    argumentos.add_argument('senha')


    #@jwt_required()
    def get(self):
        return {'Professores':[prof.json() for prof in Professores.query.all()]}

    def post(self):
        dados = User_modelo.argumentos.parse_args()
        users = Professores(**dados)
        db.session.add(users)
        db.session.commit()
        return users.json(), 201
    

class Users_modelo(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('email')
    argumentos.add_argument('cpf')
    argumentos.add_argument('senha')


    #@jwt_required()
    def get(self, id):
        users = Professores.query_by(id=id).first()
        if users:
            return users.json()
        return {'message': 'Professor inexistente'}, 404

    #@jwt_required()
    def put(self, id):
        dados = Users_modelo.argumentos.parse_args()
        users = Professores(**dados)
        user_encontrado = Professores.query.filter_by(id=id).first()
        if user_encontrado:
            user_encontrado.query.filter_by(id=id).update({**dados})
            db.session.commit()
            return user_encontrado.json(), 200
        db.session.add(users)
        db.session.commit()
        return users.json(), 201
    
    def delete(self, id):
        users = Professores.query.filter_by(id=id).first()
        if users:
            db.session.delete(users)
            db.session.commit()
            return {'message':'Deletado com sucesso'}
        return {'message': 'Usuário inexistente'}, 404