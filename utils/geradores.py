import random
import time
from typing import List

from models.paciente import Paciente
from models.medico import Medico
from models.especialidade import Especialidade


def gerar_pacientes_aleatorios(quantidade: int) -> List[Paciente]:
    nomes = ["João", "Maria", "Pedro", "Ana", "Carlos", "Lucia", "Fernanda",
             "Ricardo", "Mariana", "José", "Patricia", "Rodrigo"]
    sobrenomes = ["Silva", "Santos", "Oliveira", "Souza", "Pereira", "Costa"]

    pacientes = []
    for i in range(1, quantidade + 1):
        nome = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
        gravidade = random.randint(1, 5)
        hora_chegada = time.time() - random.randint(0, 3600)  # Chegou até 1 hora atrás
        especialidade = random.choice(list(Especialidade)) if random.random() > 0.3 else None

        pacientes.append(
            Paciente(
                id=i,
                nome=nome,
                gravidade=gravidade,
                hora_chegada=hora_chegada,
                especialidade=especialidade
            )
        )

    return pacientes


def gerar_medicos_aleatorios(quantidade: int) -> List[Medico]:
    nomes = ["Dr. Carlos", "Dra. Ana", "Dr. Pedro", "Dra. Juliana",
             "Dr. Marcelo", "Dra. Beatriz", "Dr. Rafael", "Dra. Camila"]
    especialidades = list(Especialidade)

    medicos = []
    for i in range(1, quantidade + 1):
        medicos.append(
            Medico(
                id=i,
                nome=random.choice(nomes),
                especialidade=random.choice(especialidades),
                tempo_medio_atendimento=random.randint(15, 45)  # 15-45 minutos
            )
        )

    return medicos