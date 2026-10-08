from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do local do banco de dados (será criado dentro da pasta instance/)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///petshop.db"

# Objeto que representa o banco de dados
db = SQLAlchemy(app)

# ==========================================
# MODELOS (Mapeamento Objeto-Relacional)
# ==========================================

class Dono(db.Model):
    __tablename__ = "donos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

    # Relacionamento no Python para acessar os pets deste dono
    pets = db.relationship("Pet", backref="dono", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "telefone": self.telefone
        }


class Pet(db.Model):
    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    
    # Chave estrangeira física no banco de dados
    dono_id = db.Column(db.Integer, db.ForeignKey("donos.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "especie": self.especie,
            "idade": self.idade,
            "dono_id": self.dono_id,
            "dono_nome": self.dono.nome  # Busca automática do nome do dono via relacionamento
        }

# ==========================================
# ROTAS DE DONOS
# ==========================================

@app.route("/donos", methods=["GET"])
def listar_donos():
    donos_banco = Dono.query.all()
    return jsonify([dono.to_dict() for dono in donos_banco])

@app.route("/donos/<int:id>", methods=["GET"])
def obter_dono(id):
    dono = Dono.query.get_or_404(id)
    return jsonify(dono.to_dict())

@app.route("/donos", methods=["POST"])
def criar_dono():
    dados = request.get_json()
    novo_dono = Dono(nome=dados["nome"], telefone=dados["telefone"])
    db.session.add(novo_dono)
    db.session.commit()
    return jsonify(novo_dono.to_dict()), 201

@app.route("/donos/<int:id>", methods=["PUT"])
def atualizar_dono(id):
    dono = Dono.query.get_or_404(id)
    dados = request.get_json()
    
    dono.nome = dados.get("nome", dono.nome)
    dono.telefone = dados.get("telefone", dono.telefone)
    
    db.session.commit()
    return jsonify(dono.to_dict())

@app.route("/donos/<int:id>", methods=["DELETE"])
def deletar_dono(id):
    dono = Dono.query.get_or_404(id)
    db.session.delete(dono)
    db.session.commit()
    return jsonify({"mensagem": "Dono removido com sucesso"}), 200

# ==========================================
# ROTAS DE PETS
# ==========================================

@app.route("/pets", methods=["GET"])
def listar_pets():
    pets_banco = Pet.query.all()
    return jsonify([pet.to_dict() for pet in pets_banco])

@app.route("/pets/<int:id>", methods=["GET"])
def obter_pet(id):
    pet = Pet.query.get_or_404(id)
    return jsonify(pet.to_dict())

@app.route("/pets", methods=["POST"])
def criar_pet():
    dados = request.get_json()
    
    # Verifica se o dono existe antes de cadastrar o pet
    Dono.query.get_or_404(dados["dono_id"])
    
    novo_pet = Pet(
        nome=dados["nome"],
        especie=dados["especie"],
        idade=dados["idade"],
        dono_id=dados["dono_id"]
    )
    db.session.add(novo_pet)
    db.session.commit()
    return jsonify(novo_pet.to_dict()), 201

@app.route("/pets/<int:id>", methods=["PUT"])
def atualizar_pet(id):
    pet = Pet.query.get_or_404(id)
    dados = request.get_json()
    
    if "dono_id" in dados:
        Dono.query.get_or_404(dados["dono_id"])
        pet.dono_id = dados["dono_id"]
        
    pet.nome = dados.get("nome", pet.nome)
    pet.especie = dados.get("especie", pet.especie)
    pet.idade = dados.get("idade", pet.idade)
    
    db.session.commit()
    return jsonify(pet.to_dict())

@app.route("/pets/<int:id>", methods=["DELETE"])
def deletar_pet(id):
    pet = Pet.query.get_or_404(id)
    db.session.delete(pet)
    db.session.commit()
    return jsonify({"mensagem": "Pet removido com sucesso"}), 200

if __name__ == "__main__":
    app.run(debug=True)
