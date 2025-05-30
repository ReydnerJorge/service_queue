from typing import Optional
from models.especialidade import Especialidade
from models.paciente import Paciente
import time


class Medico:
    def __init__(self, id: int, nome: str, especialidade: Especialidade, tempo_medio_atendimento: int):
        """
        Inicializa um médico com seus atributos básicos

        Args:
            id: Identificador único do médico
            nome: Nome completo do médico
            especialidade: Especialidade médica (enum Especialidade)
            tempo_medio_atendimento: Tempo médio de atendimento em minutos
        """
        self.id = id
        self.nome = nome
        self.especialidade = especialidade
        self.tempo_medio_atendimento = tempo_medio_atendimento
        self.paciente_atual: Optional[Paciente] = None
        self.hora_inicio_atendimento: Optional[float] = None
        self.total_pacientes_atendidos = 0
        self.tempo_total_atendimento = 0

    def iniciar_atendimento(self, paciente: Paciente) -> None:
        """
        Inicia o atendimento de um paciente
        """
        if self.ocupado:
            raise ValueError("Médico já está atendendo outro paciente")

        self.paciente_atual = paciente
        self.hora_inicio_atendimento = time.time()
        paciente.hora_atendimento = self.hora_inicio_atendimento

    def finalizar_atendimento(self) -> Paciente:
        """
        Finaliza o atendimento e retorna o paciente atendido
        """
        if not self.ocupado:
            raise ValueError("Médico não está atendendo nenhum paciente")

        paciente = self.paciente_atual
        hora_fim = time.time()

        # Registra os tempos
        paciente.hora_saida = hora_fim
        duracao = hora_fim - self.hora_inicio_atendimento

        # Atualiza estatísticas do médico
        self.tempo_total_atendimento += duracao
        self.total_pacientes_atendidos += 1

        # Limpa o estado de atendimento
        self.paciente_atual = None
        self.hora_inicio_atendimento = None

        return paciente

    @property
    def ocupado(self) -> bool:
        """Retorna True se o médico está atendendo um paciente"""
        return self.paciente_atual is not None

    def tempo_restante_atendimento(self) -> float:
        """
        Estima o tempo restante para o atendimento atual em minutos
        """
        if not self.ocupado:
            return 0

        tempo_decorrido = (time.time() - self.hora_inicio_atendimento) / 60
        return max(0, self.tempo_medio_atendimento - tempo_decorrido)

    def __str__(self) -> str:
        status = "Ocupado" if self.ocupado else "Disponível"
        if self.ocupado and self.paciente_atual:
            status += f" (Atendendo: {self.paciente_atual.nome})"

        return (f"Médico {self.id}: {self.nome} | "
                f"Especialidade: {self.especialidade} | "
                f"Status: {status} | "
                f"Atendidos: {self.total_pacientes_atendidos}")