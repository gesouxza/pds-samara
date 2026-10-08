# backend/criar_banco.py
from app import app, db, Dono, Pet

with app.app_context():
    # Cria a pasta instance/ e o arquivo petshop.db se não existirem
    db.create_all()

    # Só insere os dados de exemplo se o banco estiver vazio
    if Dono.query.first() is None:
        # Criando os donos de teste
        ana = Dono(nome="Ana Paula Ribeiro", telefone="45999110001")
        bruno = Dono(nome="Bruno Martins", telefone="45999110002")

        db.session.add(ana)
        db.session.add(bruno)
        db.session.commit()  # Salva para gerar os IDs da Ana e do Bruno no banco

        # Criando os pets associados aos IDs que acabaram de ser gerados
        rex = Pet(nome="Rex", especie="cachorro", idade=4, dono_id=ana.id)
        mimi = Pet(nome="Mimi", especie="gato", idade=2, dono_id=ana.id)
        thor = Pet(nome="Thor", especie="cachorro", idade=7, dono_id=bruno.id)

        db.session.add(rex)
        db.session.add(mimi)
        db.session.add(thor)
        db.session.commit()

        print("Banco de dados criado e populado com sucesso!")
    else:
        print("O banco já existe e possui dados. Nenhuma alteração foi feita.")
