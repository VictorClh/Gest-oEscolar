from flask import Flask, jsonify
from flask_restful import Api
from app import create_app
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from app.recursos import Professor_model, Aluno_model, Alunos_model, Responsaveis_model, Responsavel_model
from app.recursos import Professores_model
app = create_app()
api = Api(app)
# jwt = JWTManager(app)

# @jwt.token_in_blocklist_loader
# def verifica_blacklist(self, token):
#     return token['jti'] in BLACKLIST

# @jwt.revoked_token_loader
# def token_expirado(self, jwt_header, jwt_payload):
#     return jsonify({'message': 'Token expirado ou inválido!'}), 401

api.add_resource(Professor_model, '/professor_api')
api.add_resource(Professores_model, '/professor_api/<string:id>')
api.add_resource(Responsavel_model, '/responsavel_api')
api.add_resource(Responsaveis_model, '/responsavel_api/<string:id>')
api.add_resource(Aluno_model, '/aluno_api')
api.add_resource(Alunos_model, '/aluno_api/<string:id>')

if __name__ == "__main__":
    
    app.run(debug=True)