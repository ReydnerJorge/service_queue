import time
from typing import List
from models.medico import Medico
from models.fila import Fila


class SimuladorAtendimento:
    def __init__(self, fila: Fila, medicos: List[Medico],
                 tempo_total: int, intervalo: float = 1):
        self.fila = fila
        self.medicos = medicos
        self.tempo_total = tempo_total  # em minutos
        self.intervalo = intervalo  # em segundos
        self.tempo_decorrido = 0  # em minutos
        self.pacientes_atendidos = []

    def executar(self) -> None:
        tempo_inicio = time.time()

        while self.tempo_decorrido < self.tempo_total:
            # Atualizar tempo decorrido
            self.tempo_decorrido = (time.time() - tempo_inicio) / 60

            # Atender pacientes com médicos disponíveis
            self._atender_pacientes()

            # Finalizar atendimentos concluídos
            self._finalizar_atendimentos()

            # Mostrar status periodicamente
            if int(self.tempo_decorrido) % 30 == 0:  # A cada 30 minutos
                self._mostrar_status()

            time.sleep(self.intervalo)

        # Finalizar simulação
        self._finalizar_simulacao()

    def _atender_pacientes(self) -> None:
        for medico in self.medicos:
            if not medico.ocupado and len(self.fila) > 0:
                paciente = self.fila.proximo()
                if paciente:
                    medico.iniciar_atendimento(paciente)

    def _finalizar_atendimentos(self) -> None:
        for medico in self.medicos:
            if medico.ocupado and medico.tempo_restante_atendimento() <= 0:
                paciente = medico.finalizar_atendimento()
                self.pacientes_atendidos.append(paciente)

    def _mostrar_status(self) -> None:
        print(f"\n[STATUS] Tempo: {self.tempo_decorrido:.1f} min")
        print(f"Pacientes na fila: {len(self.fila)}")
        print(f"Pacientes atendidos: {len(self.pacientes_atendidos)}")

        for medico in self.medicos:
            status = f"Atendendo: {medico.paciente_atual.nome}" if medico.ocupado else "Disponível"
            print(f"{medico.nome} ({medico.especialidade}): {status}")

    def _finalizar_simulacao(self) -> None:
        # Forçar finalização de todos os atendimentos
        for medico in self.medicos:
            if medico.ocupado:
                paciente = medico.finalizar_atendimento()
                self.pacientes_atendidos.append(paciente)

        print("\n=== FINALIZANDO SIMULAÇÃO ===")
        print(f"Total pacientes atendidos: {len(self.pacientes_atendidos)}")
        print(f"Pacientes restantes na fila: {len(self.fila)}")