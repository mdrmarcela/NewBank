from models import Titular, Conta, ContaCorrente, ContaSalario, Poupanca, Operacao, Historico
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base


def criar_sessao():
    engine = create_engine("sqlite:///banco.db")
    Session = sessionmaker(bind=engine)
    return Session()


def criar_titular(session: Session, nome, endereco):
    titular = Titular(nome=nome, endereco=endereco)
    historico = Historico(titular=titular)
    session.add(titular)
    session.commit()
    return titular


def criar_conta(session: Session, tipo, titular_id, saldo_inicial=0.0, **kwargs):
    if tipo == 'contacorrente':
        conta = ContaCorrente(
            titular_id=titular_id, saldo=saldo_inicial, limite=kwargs.get('limite', 500.0))
    elif tipo == 'poupanca':
        conta = Poupanca(titular_id=titular_id,
                         saldo=saldo_inicial, taxa=kwargs.get('taxa', 0.01))
    elif tipo == 'contasalario':
        conta = ContaSalario(titular_id=titular_id, saldo=saldo_inicial)
    else:
        raise ValueError("Tipo de conta inválido")

    session.add(conta)
    session.commit()
    return conta


def buscar_conta_por_id(session, id_conta):
    from models import Conta
    return session.query(Conta).filter_by(id=id_conta).first()
