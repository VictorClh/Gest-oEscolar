from app import db
from sqlalchemy import func
from app.models import Alunos, Professores, Avaliacoes, Financeiro, Responsavel_Aluno, Materias, Turmas, Planejamentos
from app.forms import LoginForm
from datetime import timedelta
from flask import render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import os

def init_app(app):

    @app.route("/")
    def home():        
        return render_template("/home.html")
    
    
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form["email"]
            senha = request.form["senha"]
        
        # Consulte o banco de dados para verificar se o usuário existe e as credenciais estão corretas
            with app.app_context():
                professor = Professores.query.filter_by(email=email, senha=senha).first()

            if professor:
            # Se as credenciais estiverem corretas, redirecione para a página inicial
                return redirect(url_for("inicio"))
            else:
            # Se as credenciais estiverem incorretas, exiba uma mensagem de erro
                error_message = "Credenciais inválidas. Por favor, tente novamente."
                return render_template("login.html", error_message=error_message)
    
    # Se o método for GET, exiba o formulário de login
        return render_template("login.html")
        
    
    @app.route("/cadastro")
    def cadastro():        
        return render_template("/cadastrar.html")

        
    @app.route("/inicio")
    def inicio():        
        professores = Professores.query.order_by(Professores.id).all()
        return render_template("/inicio.html", professores=professores) 

    @app.route("/cad_professor")
    def cad_professor():        
        return render_template("cad_professor.html")
    
    @app.route("/atualiza_user")
    def atualiza_user():        
        return render_template("atualiza_user.html")
    
    @app.route("/alunos")
    def alunos():        
        return render_template("/alunos.html", aluno=db.session.execute(db.select(Alunos).order_by(Alunos.id)).scalars())

    @app.route("/turmas")
    def turmas():        
        return render_template("/turmas.html", turma=db.session.execute(db.select(Turmas).order_by(Turmas.id)).scalars())

    @app.route("/responsaveis")
    def responsaveis():        
        return render_template("/responsavel.html", responsavel=db.session.execute(db.select(Responsavel_Aluno).order_by(Responsavel_Aluno.id)).scalars())
    
    @app.route("/materias")
    def materias():        
        return render_template("/materias.html", materia=db.session.execute(db.select(Materias).order_by(Materias.id)).scalars())

    @app.route("/avaliacoes")
    def avaliacoes():        
        return render_template("/avaliacoes.html", avaliacao=db.session.execute(db.select(Avaliacoes).order_by(Avaliacoes.id)).scalars())
    
    @app.route("/financeiro")
    def financeiro():        
        return render_template("/financeiro.html", finan=db.session.execute(db.select(Financeiro).order_by(Financeiro.id)).scalars())
    
    @app.route("/planejamento")
    def planejamento():        
        return render_template("/planejamentos.html", planejamento=db.session.execute(db.select(Planejamentos).order_by(Planejamentos.id)).scalars())

    @app.route("/excluir_professor/<int:id>")
    def excluir_professor(id):
        delete=Professores.query.filter_by(id=id).first()
        db.session.delete(delete)
        db.session.commit()
        return redirect(url_for("inicio"))
    
    @app.route("/excluir_aluno/<int:id>")
    def excluir_aluno(id):
        delete=Alunos.query.filter_by(id=id).first()
        db.session.delete(delete)
        db.session.commit()
        return redirect(url_for("alunos"))
    
    @app.route("/excluir_turma/<int:id>")
    def excluir_turma(id):
        delete=Turmas.query.filter_by(id=id).first()
        db.session.delete(delete)
        db.session.commit()
        return redirect(url_for("turmas"))
    
    @app.route("/excluir_responsavel/<int:id>")
    def excluir_responsavel(id):
        delete=Responsavel_Aluno.query.filter_by(id=id).first()
        db.session.delete(delete)
        db.session.commit()
        return redirect(url_for("responsanveis"))
    
    @app.route("/excluir_materias/<int:id>")
    def excluir_materias(id):
        delete=Materias.query.filter_by(id=id).first()
        db.session.delete(delete)
        db.session.commit()
        return redirect(url_for("materias"))
    
    @app.route("/excluir_avaliacao/<int:id>")
    def excluir_avaliacao(id):
        delete=Avaliacoes.query.filter_by(id=id).first()
        db.session.delete(delete)
        db.session.commit()
        return redirect(url_for("avaliacoes"))

    @app.route("/excluir_financas/<int:id>")
    def excluir_financas(id):
        delete=Financeiro.query.filter_by(id=id).first()
        db.session.delete(delete)
        db.session.commit()
        return redirect(url_for("financeiro"))
    
    @app.route("/excluir_planejamento/<int:id>")
    def excluir_planejamento(id):
        delete=Planejamentos.query.filter_by(id=id).first()
        db.session.delete(delete)
        db.session.commit()
        return redirect(url_for("planejamento"))

    @app.route("/inserir_professores", methods=["GET", "POST"])
    def inserir_professores():
        if request.method == "POST":
            profe = Professores()
            profe.nome = request.form['nome']
            profe.email = request.form['email']
            profe.cpf = request.form['cpf']
            profe.senha = request.form['senha']    
            db.session.add(profe)
            db.session.commit()

            flash("Registro de professor criado com sucesso!")

            return redirect(url_for("inserir_professores"))
        return render_template("cadastrar.html")
    
    @app.route("/inserir_alunos", methods=["GET", "POST"])
    def inserir_alunos():
        if request.method == "POST":
            alun = Alunos()
            alun.nome = request.form['nome']
            alun.data_nasc = request.form['data_nasc']
            alun.cpf = request.form['cpf'] 
            alun.id_responsavel = request.form['id_resp']       
            db.session.add(alun)
            db.session.commit()

            flash("Registro de professor criado com sucesso!")

            return redirect(url_for("inserir_alunos"))
        return render_template("cad_aluno.html")
    
    @app.route("/inserir_turmas", methods=["GET", "POST"])
    def inserir_turmas():
        if request.method == "POST":
            tur = Turmas()
            tur.turma = request.form['turma']
            tur.id_aluno = request.form['id_aluno']       
            db.session.add(tur)
            db.session.commit()

            flash("Registro de turma criado com sucesso!")

            return redirect(url_for("inserir_turmas"))
        return render_template("cad_turma.html")

    @app.route("/inserir_responsavel", methods=["GET", "POST"])
    def inserir_responsavel():
        if request.method == "POST":
            resp = Responsavel_Aluno()
            resp.nome = request.form['nome']
            resp.cpf = request.form['cpf']
            resp.fone = request.form['fone']        
            db.session.add(resp)
            db.session.commit()

            flash("Registro de professor criado com sucesso!")

            return redirect(url_for("inserir_responsavel"))
        return render_template("cad_responsavel.html")
    

    @app.route("/inserir_materias", methods=["GET", "POST"])
    def inserir_materias():
        if request.method == "POST":
            mat = Materias()
            mat.nome = request.form['nome']
            mat.carga_horaria = request.form['carga_horaria']
            mat.id_professor = request.form['id_professor']        
            db.session.add(mat)
            db.session.commit()

            flash("Registro de matéria criado com sucesso!")

            return redirect(url_for("inserir_materias"))
        return render_template("cad_materia.html")
    

    @app.route("/inserir_avaliacao", methods=["GET", "POST"])
    def inserir_avaliacao():
        if request.method == "POST":
            aval = Avaliacoes()
            aval.nota = request.form['nota']
            aval.data_avaliacao = request.form['data_avaliacao']
            aval.id_aluno = request.form['id_aluno']   
            aval.id_materia = request.form['id_materia']     
            db.session.add(aval)
            db.session.commit()

            flash("Registro de avaliação criado com sucesso!")

            return redirect(url_for("inserir_avaliacao"))
        return render_template("cad_avaliacao.html")
    

    @app.route("/inserir_financas", methods=["GET", "POST"])
    def inserir_financas():
        if request.method == "POST":
            fin = Financeiro()
            fin.mensalidade = request.form['mensalidade']
            fin.valor = request.form['valor']
            fin.id_aluno = request.form['id_aluno']   
            db.session.add(fin)
            db.session.commit()

            flash("Registro de finanças criado com sucesso!")

            return redirect(url_for("inserir_financas"))
        return render_template("cad_financeiro.html")
    

    @app.route("/inserir_planejamento", methods=["GET", "POST"])
    def inserir_planejamento():
        if request.method == "POST":
            plan = Planejamentos()
            plan.descricao = request.form['descricao']
            plan.data_planejamento = request.form['data_planejamento']
            plan.id_professor = request.form['id_professor']
            plan.id_materia = request.form['id_materia']   
            db.session.add(plan)
            db.session.commit()

            flash("Registro de planejamento criado com sucesso!")

            return redirect(url_for("inserir_planejamento"))
        return render_template("cad_planejamento.html")

    
    @app.route("/atualizar_professor/<int:id>", methods=["GET", "POST"])
    def atualizar_professor(id):
        prof = Professores.query.filter_by(id=id).first()
        if request.method == 'POST':
            prof_nome = request.form['nome']
            prof_email = request.form['email']
            #prof_cpf = request.form['nome']
            prof_senha = request.form['senha']

            flash("Usuário atualizado com sucesso!")

            prof.query.filter_by(id=id).update({"nome":prof_nome, "senha":prof_senha, "email":prof_email})  #"data":prof_data
            db.session.commit()
            return redirect(url_for('inicio'))
        return render_template("atualiza_professor.html", prof=prof)
    
    
    @app.route("/atualizar_aluno/<int:id>", methods=["GET", "POST"])
    def atualizar_aluno(id):
        alun = Alunos.query.filter_by(id=id).first()
        if request.method == 'POST':
            alun_nome = request.form['nome']
            alun_data_nasc = request.form['data_nasc']
            alun_cpf = request.form['cpf']

            flash("Usuário atualizado com sucesso!")

            alun.query.filter_by(id=id).update({"nome":alun_nome, "data_nasc":alun_data_nasc, "cpf":alun_cpf})
            db.session.commit()
            return redirect(url_for('alunos'))
        return render_template("atualiza_aluno.html", alun=alun)
    

    @app.route("/atualizar_responsavel/<int:id>", methods=["GET", "POST"])
    def atualizar_responsavel(id):
        resp = Responsavel_Aluno.query.filter_by(id=id).first()
        if request.method == 'POST':
            resp_nome = request.form['nome']
            resp_cpf = request.form['cpf']
            resp_fone = request.form['fone']

            flash("Responsável atualizado com sucesso!")

            resp.query.filter_by(id=id).update({"nome":resp_nome, "cpf":resp_cpf, "fone":resp_fone})
            db.session.commit()
            return redirect(url_for('responsaveis'))
        return render_template("atualiza_responsavel.html", resp=resp)
    

    @app.route("/atualizar_avaliacao/<int:id>", methods=["GET", "POST"])
    def atualizar_avaliacao(id):
        aval = Avaliacoes.query.filter_by(id=id).first()
        if request.method == 'POST':
            aval_nota = request.form['nota']
            aval_data_avaliacao = request.form['data_avaliacao']
            aval_id_aluno = request.form['id_aluno']
            aval_id_materia = request.form['id_materia']

            flash("Avaliação atualizado com sucesso!")

            aval.query.filter_by(id=id).update({"nota":aval_nota, "data_avaliacao":aval_data_avaliacao, "id_aluno":aval_id_aluno, "id_materia":aval_id_materia})
            db.session.commit()
            return redirect(url_for('avaliacoes'))
        return render_template("atualiza_avaliacao.html", aval=aval)
    

    @app.route("/atualizar_turma/<int:id>", methods=["GET", "POST"])
    def atualizar_turma(id):
        turm = Turmas.query.filter_by(id=id).first()
        if request.method == 'POST':
            turm_turma = request.form['turma']
            turm_id_aluno = request.form['id_aluno']

            flash("Turma atualizada com sucesso!")

            turm.query.filter_by(id=id).update({"turma":turm_turma, "id_aluno":turm_id_aluno})
            db.session.commit()
            return redirect(url_for('turmas'))
        return render_template("atualizar_turma.html", turm=turm)
    

    @app.route("/atualizar_planejamento/<int:id>", methods=["GET", "POST"])
    def atualizar_planejamento(id):
        plane = Planejamentos.query.filter_by(id=id).first()
        if request.method == 'POST':
            plane_descricao = request.form['descricao']
            plan_data_planejamento = request.form['data_planejamento']
            plan_id_professor = request.form['id_professor']
            plan_id_materia = request.form['id_materia']

            flash("Planejamento atualizado com sucesso!")

            plane.query.filter_by(id=id).update({"descricao":plane_descricao, "data_planejamento":plan_data_planejamento, "id_professor":plan_id_professor, "id_materia":plan_id_materia})
            db.session.commit()
            return redirect(url_for('planejamento'))
        return render_template("atualizar_planejamento.html", plane=plane)
    
    @app.route("/atualizar_financeiro/<int:id>", methods=["GET", "POST"])
    def atualizar_financeiro(id):
        finan = Financeiro.query.filter_by(id=id).first()
        if request.method == 'POST':
            finan_mensalidade = request.form['mensalidade']
            finan_valor = request.form['valor']
            finan_id_aluno = request.form['id_aluno']

            flash("Financeiro atualizado com sucesso!")

            finan.query.filter_by(id=id).update({"mensalidade":finan_mensalidade, "valor":finan_valor, "id_aluno":finan_id_aluno})
            db.session.commit()
            return redirect(url_for('financeiro'))
        return render_template("atualiza_financeiro.html", finan=finan)