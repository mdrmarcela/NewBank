from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship, declarative_base
from Operacao import Operacao

Base = declarative_base()

class Titular(Base):
    __tablename__ = 'titular'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    endereco = Column(String, nullable=False)

    contas = relationship("Conta", back_populates="titular")
    historico = relationship("Historico", back_populates="titular", uselist=False)

    def __init__(self, nome: str, endereco: str):
        self.nome = nome
        self.endereco = endereco

class Conta(Base):
    __tablename__ = 'contacorrente'
    numero = Column(Integer, ForeignKey('conta.numero'), primary_key=True)
    limite = Column(Float)

    __mapper_args__ = {
        'polymorphic_identity': 'contacorrente',
    }

    def __init__(self, titular: Titular, saldo_inicial: float = 0.0):
        self.titular = titular
        self._saldo = saldo_inicial

    def sacar(self, valor: float, session, historico) -> bool:
        if valor > 0 and self._saldo >= valor:
            self._saldo -= valor
            nova_op = Operacao(
                descricao='Saque',
                valor=valor,
                conta=self,
                historico=historico
            )
            session.add(nova_op)
            return True
        return False

    def depositar(self, valor: float, session, historico) -> bool:
        if valor > 0:
            self._saldo += valor
            nova_op = Operacao (
                descricao='Deposito',
                valor=valor,
                conta=self,
                historico=historico,
            )
            session.add(nova_op)
            return True
        return False

    def pagar_online(self, valor: float, session, historico) -> bool:
        if valor > 0 and self._saldo >= valor:
            self._saldo -= valor
            nova_op = Operacao(
                descricao="Pagamento online",
                valor=valor,
                conta=self,
                historico=historico,
            )
            session.add(nova_op)
            return True
        return False

    def obter_saldo(self) -> float:
        return self._saldo


class ContaCorrente(Conta):
    def __init__(self, titular: Titular, saldo_inicial: float = 0.0, limite_negativo: float = 0.0):
        super().__init__(titular, saldo_inicial)
        self.limite_negativo = limite_negativo

    def sacar(self, valor: float, session, historico) -> bool:
        if valor > 0 and (self._saldo - valor) >= -self.limite_negativo:
            self._saldo -= valor
            nova_op = Operacao(
                descricao="Saque",
                valor=valor,
                conta=self,
                historico=historico
            )
            session.add(nova_op)
            return True
        return False

    def pagar_online(self, valor: float, session, historico) -> bool:
        if valor > 0 and (self._saldo - valor) >= -self.limite_negativo:
            self._saldo -= valor
            nova_op = Operacao(
                descricao="Pagamento online",
                valor=valor,
                conta=self,
                historico=historico
            )
            session.add(nova_op)
            return True
        return False

