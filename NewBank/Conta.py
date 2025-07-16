from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Conta(Base):
    __tablename__ = 'conta'

    numero = Column(Integer, primary_key=True, autoincrement=True)
    saldo = Column(Float, default=0.0)
    tipo = Column(String)
    titular_id = Column(Integer, ForeignKey('titular.id'))

    titular = relationship("Titular", back_populates="contas")
    operacoes = relationship("Operacao", back_populates="conta", cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'conta',
        'polymorphic_on': tipo
    }

    def __init__(self, titular, saldo=0.0):
        self.titular = titular
        self.saldo = saldo

    def sacar(self, valor: float) -> bool:
        if valor <= 0 or valor > self.saldo:
            return False
        self.saldo -= valor
        return True

    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            return False
        self.saldo += valor
        return True

    def pagar_online(self, valor: float) -> bool:
        return self.sacar(valor)
