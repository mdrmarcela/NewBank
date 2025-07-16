from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from Conta import Conta  

Base = declarative_base()


class Operacao(Base):
    __tablename__ = 'operacao'

    id = Column(Integer, primary_key=True)
    descricao = Column(String, nullable=False)
    valor = Column(Float, nullable=False)
    data = Column(DateTime, default=datetime.utcnow)

    conta_id = Column(Integer, ForeignKey('conta.id'), nullable=False)
    historico_id = Column(Integer, ForeignKey('historico.id'), nullable=True)

    conta = relationship("Conta", back_populates="operacoes")
    historico = relationship("Historico", back_populates="operacoes")

    def __init__(self, descricao: str, valor: float, conta: Conta, historico: None):
        self.descricao = descricao
        self.valor = valor
        self.data = datetime.now()
        self.conta = conta
        self.historico = historico

    def __str__(self):
        return f"{self.data.strftime('%d/%m/%Y %H:%M:%S')} | {self.descricao} | R${self.valor:.2f} | Saldo: R${self.conta.saldo:.2f}"
