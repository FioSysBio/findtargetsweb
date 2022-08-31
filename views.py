import cobra as cobra
from flask import render_template, request,  redirect, session, flash, url_for
from models import Modelos_Execucao, Users
from dao import ModeloDao, UsuarioDao
from findtarget import db, app
import random
import string
from datetime import timedelta

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pathlib import Path
from cobra.io import save_json_model, load_matlab_model, save_matlab_model, read_sbml_model, write_sbml_model, validate_sbml_model
import logging

model_dao = ModeloDao(db)
usuario_dao = UsuarioDao(db)

@app.route('/')
def index():
    return render_template('index.html', titulo='Select your mode', category='info')


@app.route('/simulation/')
def simulation():
    email_user = session['usuario_logado']

    lista_organismos = model_dao.listar_por_email(email_user)
    user = usuario_dao.buscar_por_email(email_user)

    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('simulation')))
    return render_template('run_models.html', titulo='Run Simulation Models', organismos=lista_organismos, id_user=user.id, category='danger')

@app.route('/adm')
def adm():
    lista_contas = usuario_dao.listar_contas()
    email_user = session['usuario_logado']
    user = usuario_dao.buscar_por_email(email_user)

    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('adm')))
    elif user.nivel == 1:
        return render_template('list_request_account.html', titulo="List of requested accounts", contas=lista_contas, id_user=user.id, category='success')
    else:
        flash('Não há permissão necessária!!!')
        return redirect(url_for('login', proxima=url_for('simulation')))


@app.route('/request_account')
def request_account():
    return render_template('request_account.html', titulo="Request your account")


@app.route('/create_account', methods = ['POST',])
def create_account():
    nome = request.form['name']
    email = request.form['email']
    senha = request.form['password']
    status = 0
    nivel = 0
    instituicao = request.form['instituicao']

    token = ''.join(random.choice(string.ascii_letters) for i in range(8))
    validado = 0

    #CONFIGURAÇÕES PARA ENVIO DE TOKEN - VALIDAR EMAIL
    # Configuração
    host = 'smtp.office365.com'
    port = 587
    user = 'suportefindtargets@outlook.com'
    password = '@find123'

    # Criando objeto
    server = smtplib.SMTP(host, port)

    # Login com servidor
    server.ehlo()
    server.starttls()
    server.login(user, password)

    # Criando mensagem
    message = 'Segue token para validação de email registrado no FindTargetsWeb: ' + token

    email_msg = MIMEMultipart()
    email_msg['From'] = user
    email_msg['To'] = email
    email_msg['Subject'] = 'Validação de email'

    email_msg.attach(MIMEText(message, 'plain'))

    # Enviando mensagem
    server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())
    server.quit()

    account = Users(nome, email, senha, status, nivel, instituicao, token, validado)

    usuario_dao.salvar_user(account)
    #lista_organismos.append(account)


    #vai pra pag validar o token
    return redirect(url_for('valida_token'))

@app.route('/valida_token')
def valida_token():
    return render_template('valida_token.html', titulo="Valide seu token", category='warning')


@app.route('/validarToken', methods=['POST',])
def validarToken():

    usuario = usuario_dao.buscar_Token(request.form['token'])

    if usuario:
        usuario_dao.atualiza_Token(request.form['token'])
        flash('Token encontrado, email validado, aguarde agora a validação da conta pelo Adm')
        return redirect(url_for('login'))

    else:
        flash('Token incorreto, tente novamente!!!')
        return redirect(url_for('valida_token'))


@app.route('/edit_account/<int:id>')
def edit_account(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return (url_for('login', proxima=url_for('edit_account')))
    user = usuario_dao.busca_por_id(id)
    return render_template('edit_account.html', titulo="Edit account", conta = user, category='warning')

@app.route('/edit_profile/<int:id>')
def edit_profile(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return (url_for('login', proxima=url_for('edit_account')))

    user = usuario_dao.busca_por_id(id)

    return render_template('edit_profile.html', titulo="Edit profile", conta=user, category='warning')

@app.route('/update_profile', methods = ['POST',])
def update_profile():
    id = request.form['id']
    nome = request.form['name']
    email = request.form['email']
    password = request.form['password']

    status = request.form['status']

    nivel = request.form['nivel']
    instituicao = request.form['instituicao']

    token = '0'
    validado = '1'

    account = Users(nome, email, password, status, nivel, instituicao, token, validado, id)

    usuario_dao.salvar_user(account)

    return redirect(url_for('simulation'))

@app.route('/atualiza_conta', methods = ['POST',])
def atualiza_conta():
    id = request.form['id']
    nome = request.form['name']
    email = request.form['email']
    password = request.form['password']
    status = request.form['status']
    nivel = request.form['nivel']
    instituicao = request.form['instituicao']

    validado = 1
    token = 0

    account = Users(nome, email, password, status, nivel, instituicao, token, validado, id)

    usuario_dao.salvar_user(account)

    return redirect(url_for('adm'))


@app.route('/delete_account/<int:id>')
def delete_account(id):
    user = usuario_dao.busca_por_id(id)
    usuario_dao.deletar(id)

    model_dao.deletar_modelo_user(user.email)

    flash("Conta deletada com sucesso")
    return redirect(url_for('adm'))


@app.route('/simulation/delete_simulation/<int:id>')
def delete_simulation_2(id):
    model_dao.deletar(id)

    flash("Simulação deletada com sucesso")

    return redirect(url_for('simulation'))

@app.route('/simulation/new_model/')
def new_model():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('new_model')))
    return render_template('new_model.html', titulo='New Simulation', category='info')


def readModel(self, sbmlfile):
    return cobra.io.read_sbml_model(sbmlfile)

@app.route('/create_simulation', methods = ['POST',])
def create_simulation():
    organism = request.form['organism']
    arquivo = request.files['fileSBML']
    form_analysis = request.form['form_analysis']
    description = request.form['description']

    print("-----init calc fba------")

    data_dir = Path(".") / "uploads"
    data_dir = data_dir.resolve()

    print("data_dir -> ", data_dir)

    mini_fbc2_path = data_dir / "arquivo_sbml3_ccbh4851_argollo.xml"

    model = read_sbml_model(str(mini_fbc2_path.resolve()))
    report = validate_sbml_model(str(mini_fbc2_path.resolve()))

    solution = model.optimize()
    print(round(solution, 6))
    print(report)

    print("-----end calc fba------")


    simulation = Modelos_Execucao(organism, '1.036524', arquivo.filename, form_analysis, description, '', session['usuario_logado'])
    simulation = model_dao.salvar(simulation)

    upload_path = app.config['UPLOAD_PATH']
    arquivo.save(f'{upload_path}/simulation_{simulation.id}.xml')

    return redirect(url_for('simulation'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo='Login', proxima=proxima, category='info')


@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = usuario_dao.buscar_por_email(request.form['email'])

    if usuario:
        if usuario.status == 1:
            if usuario.validado == 1:
                if request.form['senha'] == usuario.senha:
                    session['usuario_logado'] = usuario.email
                    flash('Você ' + usuario.nome + ' esta logado!!!')
                    proxima_pagina = request.form['proxima']
                    return redirect(proxima_pagina)
                else:
                    flash('Senha está incorreta, confirme novamente!!!')
                    return redirect(url_for('login'))
            else:
                flash('Email ainda não validado!!!')
                return redirect(url_for('valida_token'))
        else:
            flash('Credenciais ainda não aprovadas!!!')
            return redirect(url_for('login'))
    else:
        flash('Credenciais incorretas, tente novamente!!!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!!!')
    return redirect(url_for('index'))


@app.route('/simulation/logout')
def logout_simulation():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!!!')
    return redirect(url_for('index'))


