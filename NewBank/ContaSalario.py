from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class Conta(Base):
    __tablename__ = 'contasalario'
    numero = Column(Integer, ForeignKey('conta.numero'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'contasalario',
    }

    def __init__(self, saldo_inicial: float = 0.0):
        self._saldo = saldo_inicial

    def sacar(self, valor: float) -> bool:
        if valor > 0 and valor <= self._saldo:
            self._saldo -= valor
            return True
        return False

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            return True
        return False

    def pagar_online(self, valor: float) -> bool:
        if valor > 0 and valor <= self._saldo:
            self._saldo -= valor
            return True
        return False

    def obter_saldo(self) -> float:
        return self._saldo


class ContaSalario(Conta):
    def pagar_online(self, valor: float) -> bool:
        return False
