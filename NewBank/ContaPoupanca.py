from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship, declarative_base


class Titular:
    def __init__(self, nome: str, endereco: str):
        self.nome = nome
        self.endereco = endereco


Base = declarative_base()


class Conta(Base):
    __tablename__ = 'poupanca'
    numero = Column(Integer, ForeignKey('conta.numero'), primary_key=True)
    taxa = Column(Float)

    __mapper_args__ = {
        'polymorphic_identity': 'poupanca',
    }

    def __init__(self, titular: Titular, saldo_inicial: float = 0.0):
        self.titular = titular
        self._saldo = saldo_inicial

    def sacar(self, valor: float) -> bool:
        if valor > 0 and self._saldo >= valor:
            self._saldo -= valor
            return True
        return False

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            return True
        return False

    def pagar_online(self, valor: float) -> bool:
        if valor > 0 and self._saldo >= valor:
            self._saldo -= valor
            return True
        return False

    def obter_saldo(self) -> float:
        return self._saldo


class ContaPoupanca(Conta):
    TAXA_SAQUE = 0.0005

    def sacar(self, valor: float) -> bool:
        valor_total = valor + (valor * ContaPoupanca.TAXA_SAQUE)
        if valor > 0 and self._saldo >= valor_total:
            self._saldo -= valor_total
            return True
        return False
