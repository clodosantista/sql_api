#import para trabalhar com json
import json
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy

#flasck um das ferramenta que o pythom disponibiliza
#aplicacao do tipo flask.

app = Flask('carros')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:senai%40134@127.0.0.1/bd_carro'

mybd = SQLAlchemy(app)

#mybd armazena tudo.

class Carros(mybd.Model):
    __tablename__ ='tb_carros'
    id = mybd.Column(mybd.Integer, primary_key = True)
    marca = mybd.Column(mybd.String(100))
    modelo = mybd.Column(mybd.String(100))
    valor = mybd.Column(mybd.Float)
    cor = mybd.Column(mybd.String(100))
    numero_vendas = mybd.Column(mybd.Float)
    ano = mybd.Column(mybd.String(10))

    def to_json(self):
        return{"id": self.id, "marca": self.marca,"modelo": self.modelo, "valor": self.valor, "cor":self.cor, "numero_vendas": self.numero_vendas, "ano":self.ano} 
       # estrutura que trabalha com chaves.
       # GET pra atualizar
       # ALL ele busca tudo        
               
@app.route("/carros", methods=["GET"])
def selecionar_carros():
    carro_objetos = Carros.query.all()

    carro_json = [carro.to_json() for carro in carro_objetos]
    return gera_response(200, "carros", carro_json)

@app.route("/carros/<id>", methods=["GET"])
def seleciona_carro_id(id):
    carro_objetos = Carros.query.filter_by(id=id).first()
    carro_json = carro_objetos.to_json()
    return gera_response(200, "carros", carro_json)

@app.route("/carros", methods=["POST"])
def criar_carro():
    body = request.get_json()

    try:
        carro = Carros(id=body["id"], marca=body["marca"], modelo=body["modelo"],valor=body["valor"],cor=body["cor"],numero_vendas=body["numero_vendas"],ano=body["ano"])
        mybd.session.add(carro)
        mybd.session.commit()

        return gera_response(201, "carros", carro.to_json(), "criado com sucesso!!!")
    except Exception as e:
        print('Erro', e)

        return gera_response(400, "carros", {},"Erro ao cadastro!!")
    
@app.route("/carros/<id>", methods=["PUT"]) 
def atualizar_carro(id):
    carro_objetos = Carros.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if('marca' in body):
            carro_objetos.marca = body['marca']
        if('modelo' in body):
            carro_objetos.modelo = body['modelo']
        if('cor' in body):
            carro_objetos.cor = body['cor'] 
        if('valor' in body):
            carro_objetos.valor = body['valor']
        if('numero_vendas' in body):
            carro_objetos.numero_vendas = body['numero_vendas'] 
        if('ano' in body):
            carro_objetos.ano = body['ano'] 

        mybd.session.add(carro_objetos)
        mybd.session.commit()

        return gera_response(200, "carros", carro_objetos.to_json(), "atualizado com sucesso") 
    
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "carros", {}, "Erro ao atualizar")

def gera_response(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json" )
    
app.run(port=5000,host='localhost',debug=True)

#vdelatar

@app.route("/carros/<id>", methods=["DELETE"])
def delatar_carros(id):
    carro_objetos = carros.query.filter_by(id=id).first()
    try:
        mybd.session.delete(carro_objetos)
        mybd.session.commit()

        return gera_response(200, "carro", carro_objetos.to_json(), "deletado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "carro", {}, "Erro ao deletar")

def gera_response(status, nome_conteudo, conteudo,mensagem=False):
    body = {}
    body[nome_conteudo] = Conteudo 

    if(mensagem):
        body["mensagem"] = mensagem

        return Response(json.dumps(body), status=status, mimetype="application/json")
    
    ######

    ## pip install mysql-



    

