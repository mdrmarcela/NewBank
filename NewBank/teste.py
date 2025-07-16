from sqlalchemy.orm import sessionmaker
from models import *
from sqlalchemy import create_engine

engine = create_engine('sqlite:///banco.db')
Session = sessionmaker(bind=engine)
session = Session()

titular = Titular(nome="Fulana", endereco="Rua Bala de iogurte")
session.add(titular)
session.commit()

conta = ContaCorrente(numero=1, saldo=1000.0, limite=500.0, titular=titular)
session.add(conta)
session.commit()

print("Dados inseridos com sucesso!")
