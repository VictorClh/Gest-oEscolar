# CRIAR NOVO ARQUIVO recursos.py
from flask_restful import Resource, reqparse
from app.models import Professores, Alunos, Responsavel_Aluno
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from blacklist import BLACKLIST
from app import db


class Professor_model(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('email')
    argumentos.add_argument('cpf')
    argumentos.add_argument('senha')


    #@jwt_required()
    def get(self):
        return {'Professores':[prof.json() for prof in Professores.query.all()]}

    def post(self):
        dados = Professor_model.argumentos.parse_args()
        professor = Professores(**dados)
        db.session.add(professor)
        db.session.commit()
        return professor.json(), 201
    

class Professores_model(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('email')
    argumentos.add_argument('cpf')
    argumentos.add_argument('senha')


    #@jwt_required()
    def get(self, id):
        professores = Professores.query.filter_by(id=id).first()
        if professores:
            return professores.json()
        return {'message': 'Professor inexistente'}, 404

    #@jwt_required()
    def put(self, id):
        dados = Professores_model.argumentos.parse_args()
        professores = Professores(**dados)
        professor_encontrado = Professores.query.filter_by(id=id).first()
        if professor_encontrado:
            professor_encontrado.query.filter_by(id=id).update({**dados})
            db.session.commit()
            return professor_encontrado.json(), 200
        db.session.add(professores)
        db.session.commit()
        return professores.json(), 201
    
    def delete(self, id):
        professores = Professores.query.filter_by(id=id).first()
        if professores:
            db.session.delete(professores)
            db.session.commit()
            return {'message':'Deletado com sucesso'}
        return {'message': 'Professores inexistente'}, 404
    
    
class Responsavel_model(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True)
    argumentos.add_argument('cpf', type=str, required=True)
    argumentos.add_argument('fone', type=str, required=True)

    def get(self):
        return{'responsaveis':[responsavel.json() for responsavel in Responsavel_Aluno.query.all()]}
    
    def post(self):
        dados = Responsavel_model.argumentos.parse_args()
        responsavel_aluno = Responsavel_Aluno(**dados)
        db.session.add(responsavel_aluno)
        db.session.commit()
        return responsavel_aluno.json(), 201
    
    
class Responsaveis_model(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True)
    argumentos.add_argument('cpf', type=str, required=True)
    argumentos.add_argument('fone', type=str, required=True)

    def get(self, id):
        responsavel_aluno = Responsavel_Aluno.query.filter_by(id=id).first()
        if responsavel_aluno:
            return responsavel_aluno.json()
        return {'message': 'Responsavel inexistente'}, 404
    
    def put(self, id):
        dados = Responsavel_model.argumentos.parse_args()
        responsavel = Responsavel_Aluno(**dados)
        responsavel_aluno = Responsavel_Aluno.query.filter_by(id=id).first()
        if responsavel_aluno:
            responsavel_aluno.query.filter_by(id=id).update({**dados})
            db.session.commit()
            return responsavel_aluno.json(), 200
        db.session.add(responsavel)
        db.session.commit()
        return responsavel.json(), 201
    
    def delete(self, id):
        responsavel_aluno = Responsavel_Aluno.query.filter_by(id=id).first()
        if responsavel_aluno:
            db.session.delete(responsavel_aluno)
            db.session.commit()
            return {'message':'Deletado com sucesso'}
        return{'message':'Informação não encontrada'}

    
class Aluno_model(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True)
    argumentos.add_argument('data_nasc', type=str, required=True)
    argumentos.add_argument('cpf', type=str, required=True)
    argumentos.add_argument('id_responsavel', type=str, required=True)

    def get(self):
        return{'Alunos':[aluno.json() for aluno in Alunos.query.all()]}
    
    def post(self):
        dados = Alunos_model.argumentos.parse_args()
        aluno = Alunos(**dados)
        db.session.add(aluno)
        db.session.commit()
        return aluno.json(), 201
    
class Alunos_model(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True)
    argumentos.add_argument('data_nasc', type=str, required=True)
    argumentos.add_argument('cpf', type=str, required=True)
    argumentos.add_argument('id_responsavel', type=str, required=True)

    def get(self, id):
        aluno = Alunos.query.filter_by(id=id).first()
        if aluno:
            return aluno.json()
        return {'message': 'Aluno inexistente'}, 404
    
    def put(self, id):
        dados = Alunos_model.argumentos.parse_args()
        aluno = Alunos(**dados)
        aluno_encontrado = Alunos.query.filter_by(id=id).first()
        if aluno_encontrado:
            aluno_encontrado.query.filter_by(id=id).update({**dados})
            db.session.commit()
            return aluno_encontrado.json()
        db.session.add(aluno)
        db.session.commit()
        return aluno.json(), 201
    
    def delete(self, id):
        aluno = Alunos.query.filter_by(id=id).first()
        if aluno:
            db.session.delete(aluno)
            db.session.commit()
            return {'message': 'Aluno deletado com sucesso'}, 200
        return{'message':'informação não encontrada'}
        

    
