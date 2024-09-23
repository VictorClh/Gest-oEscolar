from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def current_user(user_id):
    return Professores.query.get(user_id)

 
class Professores(db.Model, UserMixin):
    __tablename__ = "professores"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(255), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    data = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    #materias = db.relationship('Materias', backref='professor', lazy=True)
    #turmas = db.relationship('Turmas', secondary=Turmas_Professores.__table__, backref=db.backref('professores', lazy=True))
    def json(self):
        return { 
                'id': self.id, 
                'nome': self.nome,
                'email': self.email,
                'cpf': self.cpf,
                'senha': self.senha
                
        }
class Alunos(db.Model):
    __tablename__ = "alunos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    data_nasc = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(255), nullable=False)
    id_responsavel = db.Column(db.Integer, db.ForeignKey('responsavel_aluno.id'), nullable=True)
    data_cadastro = db.Column(db.DateTime, default=db.func.current_timestamp())
    responsavel = db.relationship('Responsavel_Aluno', backref='aluno')
    def json(self):
        return { 
                'id': self.id, 
                'nome': self.nome,
                'data_nasc': self.data_nasc,
                'cpf': self.cpf,
                'id_responsavel': self.id_responsavel
                
        }

class Responsavel_Aluno(db.Model):
    __tablename__ = "responsavel_aluno"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(255), nullable=False)
    fone = db.Column(db.String(20), nullable=False)
    def json(self):
        return { 
                'id': self.id, 
                'nome': self.nome,
                'cpf': self.cpf,
                'fone': self.fone
                
        }

class Materias(db.Model):
    __tablename__ = 'materias'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    carga_horaria = db.Column(db.Float, nullable=False)  
    id_professor = db.Column(db.Integer, db.ForeignKey('professores.id'), nullable=True)
    professor = db.relationship('Professores', backref='materia')


class Turmas(db.Model):
    __tablename__ = "turmas"
    id = db.Column(db.Integer, primary_key=True)
    turma = db.Column(db.String(255), nullable=False)
    id_aluno = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=True)
    aluno = db.relationship('Alunos', backref='turma', lazy=True)
    
class Avaliacoes(db.Model):
    __tablename__ = "avaliacoes"
    id = db.Column(db.Integer, primary_key=True)
    nota = db.Column(db.Float, nullable=False)
    data_avaliacao = db.Column(db.DateTime, default=db.func.current_timestamp())
    id_aluno = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=True)
    aluno = db.relationship('Alunos', backref='avaliacao', lazy=True)
    id_materia = db.Column(db.Integer, db.ForeignKey('materias.id'), nullable=True)
    materia = db.relationship('Materias', backref='materia', lazy=True)

class Financeiro(db.Model):
    __tablename__ = "financeiro"
    id = db.Column(db.Integer, primary_key=True)
    mensalidade = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    id_aluno = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=True)
    aluno = db.relationship('Alunos', backref='financeiro', lazy=True)

class Planejamentos(db.Model):
    __tablename__ = 'planejamentos'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(500), nullable=False)
    data_planejamento = db.Column(db.Date) 
    id_professor = db.Column(db.Integer, db.ForeignKey('professores.id'), nullable=True)
    professor = db.relationship('Professores', backref='planejamento')
    id_materia = db.Column(db.Integer, db.ForeignKey('materias.id'), nullable=True)
    materia = db.relationship('Materias', backref='planejamento')