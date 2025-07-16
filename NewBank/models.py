from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class Titular(Base):
    __tablename__ = 'titular'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    endereco = Column(String)

    contas = relationship("Conta", back_populates="titular")
    historico = relationship("Historico", uselist=False,
                             back_populates="titular")


class Conta(Base):
    __tablename__ = 'conta'

    numero = Column(Integer, primary_key=True)
    saldo = Column(Float)
    titular_id = Column(Integer, ForeignKey('titular.id'))
    tipo = Column(String)  # Usado para herança (ContaCorrente, Poupanca etc.)

    titular = relationship("Titular", back_populates="contas")

    __mapper_args__ = {
        'polymorphic_on': tipo,
        'polymorphic_identity': 'conta'
    }


class ContaCorrente(Conta):
    __tablename__ = 'contacorrente'
    numero = Column(Integer, ForeignKey('conta.numero'), primary_key=True)
    limite = Column(Float)

    __mapper_args__ = {
        'polymorphic_identity': 'contacorrente'
    }


class ContaSalario(Conta):
    __tablename__ = 'contasalario'
    numero = Column(Integer, ForeignKey('conta.numero'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'contasalario'
    }


class Poupanca(Conta):
    __tablename__ = 'poupanca'
    numero = Column(Integer, ForeignKey('conta.numero'), primary_key=True)
    taxa = Column(Float)

    __mapper_args__ = {
        'polymorphic_identity': 'poupanca'
    }


class Operacao(Base):
    __tablename__ = 'operacao'

    id = Column(Integer, primary_key=True)
    descricao = Column(String)
    valor = Column(Float)
    data = Column(DateTime, default=datetime.utcnow)
    conta_id = Column(Integer, ForeignKey('conta.numero'))

    conta = relationship("Conta")


class Historico(Base):
    __tablename__ = 'historico'

    id = Column(Integer, primary_key=True)
    titular_id = Column(Integer, ForeignKey('titular.id'))

    titular = relationship("Titular", back_populates="historico")
    operacoes = relationship("Operacao")
