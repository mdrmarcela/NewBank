from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

Base = declarative_base()


class Historico(Base):
    __tablename__ = 'historico'

    id = Column(Integer, primary_key=True)
    titular_id = Column(Integer, ForeignKey('titular.id'), nullable=False)

    titular = relationship("Titular", back_populates="historico")
    operacoes = relationship(
        "Operacao", back_populates="historico", cascade="all, delete-orphan")

    def __init__(self, titular):
        self.titular = titular

    def buscar(self, descricao=None, valor=None):
        resultados = self.operacoes
        if descricao:
            resultados = [
                op for op in resultados if descricao.lower() in op.descricao.lower()]
        if valor is not None:
            resultados = [op for op in resultados if op.valor == valor]
        return resultados


def gerar_pdf(self, nome_arquivo="extrato.pdf", idioma="pt"):
    traduzir = get_tradutor(idioma)
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    largura, altura = A4
    y = altura - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, traduzir("Extrato Bancário"))
    y -= 30

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"{traduzir('Titular')}: {self.titular.nome}")
    y -= 20

    if not self.operacoes:
        c.drawString(50, y, traduzir("Nenhuma operação registrada."))
    else:
        for op in self.operacoes:
            linha = f"{op.data.strftime('%d/%m/%Y %H:%M')} - {traduzir(op.descricao)} - R${op.valor:.2f}"
            c.drawString(50, y, linha)
            y -= 20
            if y < 50:
                c.showPage()
                y = altura - 50

    c.save()
    print(f"{traduzir('PDF gerado em')}: {os.path.abspath(nome_arquivo)}")


def get_tradutor(idioma):
    traducoes = {
        'pt': lambda texto: texto,
        'en': lambda texto: {
            "Extrato Bancário": "Bank Statement",
            "Titular": "Account Holder",
            "PDF gerado em": "PDF generated at",
            "Nenhuma operação registrada.": "No operations recorded."
        }.get(texto, texto),
        'es': lambda texto: {
            "Extrato Bancário": "Extracto Bancario",
            "Titular": "Titular",
            "PDF gerado em": "PDF generado en",
            "Nenhuma operação registrada.": "Ninguna operación registrada."
        }.get(texto, texto),
    }
    return traducoes.get(idioma, traducoes['pt'])
