class Titular:
    def __init__(self, nome: str, endereco: str):
        self.nome = nome
        self.endereco = endereco


class Conta:
    def __init__(self, titular: Titular, saldo: float = 0.0):
        self.titular = titular
        self._saldo = saldo

    @property
    def saldo(self):
        return self._saldo

    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            return False
        if valor > self._saldo:
            return False
        self._saldo -= valor
        return True

    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            return False
        self._saldo += valor
        return True

    def pagar_online(self, valor: float) -> bool:
        return self.sacar(valor)


operacoes = relationship(
    "Operacao", back_populates="conta", cascade="all, delete-orphan")
