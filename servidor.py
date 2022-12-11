from config import *
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json


app = Flask(__name__)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{USER}:{PASS}@{DB_URL}/{DB}?charset=utf8mb4'


db = SQLAlchemy(app)


class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    def converte_json(self):
        return {'id': self.id, 'nome': self.nome, 'email': self.email}


def resposta (status, nome_status, conteudo, mensagem=False):
    body = {}
    body[nome_status] = conteudo
    if mensagem:
        body['mensagem'] = mensagem
    return Response(json.dumps(body), status=status, \
                    mimetype='application/json')


@app.route('/cadastro', methods=['POST'])
def cadastro():
    body = request.get_json()
    try:
        pessoa = Usuarios(nome=body['nome'], email=body['email'])
        db.session.add(pessoa)
        db.session.commit()
        return resposta(201, 'pessoa', pessoa.converte_json(), \
                        'Pessoa cadastrada com sucesso!')
    except Exception as e:
        print('Erro', e)
        return resposta(400, 'pessoa', {}, 'Pessoa nao cadastrada...')


@app.route('/consulta/<id>', methods=['GET'])
def consulta_um(id):
    pessoa = Usuarios.query.filter_by(id=id).first()
    try:
        pessoa_json = pessoa.converte_json()
        return resposta(200, 'pessoa', pessoa_json, 'Pessoa localizada')
    except Exception as e:
        print('Erro', e)
        return resposta(400, 'pessoa', {}, 'Pessoa nao localizada...')


@app.route('/consulta', methods=['GET'])
def consulta_todos():
    pessoas = Usuarios.query.all()
    todos = [pessoa.converte_json() for pessoa in pessoas]
    return resposta(200, 'pessoas', todos, 'Todas as pessoas cadastradas.')


@app.route('/atualiza-nome/<id>', methods=['PUT'])
def atualiza_nome(id):
    objeto_pessoa = Usuarios.query.filter_by(id=id).first()
    body = request.get_json()
    try:
        if 'nome' in body:
            objeto_pessoa.nome = body['nome']
            db.session.add(objeto_pessoa)
            db.session.commit()
            return resposta(200, 'pessoa', objeto_pessoa.converte_json(), \
                            'Nome atualizado com sucesso!')
    except Exception as e:
        print('Erro', e)
        return resposta(400, 'pessoa', {}, 'Nome nao atualizado...')


@app.route('/atualiza-email/<id>', methods=['PUT'])
def altera_email(id):
    objeto_pessoa = Usuarios.query.filter_by(id=id).first()
    body = request.get_json()
    try:
        if 'email' in body:
            objeto_pessoa.email = body['email']
            db.session.add(objeto_pessoa)
            db.session.commit()
            return resposta(200, 'pessoa', objeto_pessoa.converte_json(), \
                            'Email atualizado com sucesso!')
    except Exception as e:
        print('Error', e)
        return resposta(400, 'pessoa', {}, 'E-mail nao atualizado...')


@app.route('/exclui/<id>', methods=['DELETE'])
def exclui(id):
    objeto_pessoa = Usuarios.query.filter_by(id=id).first()
    try:
        db.session.delete(objeto_pessoa)
        db.session.commit()
        return resposta(200, 'pessoa', objeto_pessoa.converte_json(), \
                        'Pessoa deleteda com sucesso!')
    except Exception as e:
        print('Error', e)
        return resposta(400, 'pessoa', {}, 'Erro na tentativa de deletar...')


if __name__ == '__main__':
    app.run(host = 'localhost', port = 5000, debug = True)