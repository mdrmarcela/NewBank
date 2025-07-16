from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base
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

    def __init__(self, nome: str, endereco: str):
        self.nome = nome
        self.endereco = endereco

