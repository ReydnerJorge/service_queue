import time
from enum import nonmember


class Paciente:
    def __init__(self, id, nome, gravidade, hora_chegada, especialidade=None):
        self.id = id
        self.nome = nome
        self.gravidade = gravidade # 1 a 5 (1 = mais grave)
        self.hora_chegada = hora_chegada
        self.especialidade = None
        self.hora_saida = None

    ##def __str__(self):
    ##   return f'Paciente {self.id}: {self.nome} (Gravidade: {self.gravidade}'

    def tempo_espera(self):
        if self.hora.atendimento:
            return self.hora.atendimento - self.hora_chegada
        return None