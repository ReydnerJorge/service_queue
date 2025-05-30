from heapq import heappush, heappop
from typing import List
import time
from models.paciente import Paciente

class Fila:
    def __init__(self):
        # Usando heap para eficiência na priorização
        self._fila = []
        self._contador = 0  # Para desempate em casos de mesma prioridade

    def adicionar_paciente(self, paciente: Paciente) -> None:
        """Adiciona paciente na fila com base na gravidade e tempo de espera
        Args:
            paciente: Instância de Paciente a ser adicionada
        """
        prioridade = (paciente.gravidade, paciente.hora_chegada, self._contador)
        heappush(self._fila, (prioridade, paciente))
        self._contador += 1

    def atender_proximo(self) -> Paciente:
        """Remove e retorna o próximo paciente da fila
        Returns:
            Paciente: O próximo paciente mais prioritário ou None se fila vazia
        """
        if self._fila:
            return heappop(self._fila)[1]
        return None

    def mostrar_fila(self) -> None:
        """Exibe a fila atual ordenada por prioridade"""
        print('\n=== FILA DE ATENDIMENTO ===')
        print(f'{"ID":<5} | {"Nome":<20} | {"Gravidade":<10} | {"Especialidade":<15} | {"Tempo Espera (min)":<15}')
        print('-' * 70)

        # Cria lista ordenada sem modificar a heap original
        fila_ordenada = sorted(self._fila, key=lambda x: x[0])
        for prioridade, paciente in fila_ordenada:
            tempo_espera = (time.time() - paciente.hora_chegada)/60 if paciente.hora_chegada else 0
            print(f'{paciente.id:<5} | {paciente.nome:<20} | {paciente.gravidade:<10} | '
                  f'{str(paciente.especialidade):<15} | {tempo_espera:.1f}')

        print(f'\nTotal na fila: {len(self._fila)} pacientes')
        print('=' * 70)

    def __len__(self) -> int:
        """Retorna o número de pacientes na fila"""
        return len(self._fila)

    def pacientes_em_espera(self) -> List[Paciente]:
        """Retorna lista de pacientes em espera, ordenados por prioridade
        Returns:
            List[Paciente]: Lista ordenada de pacientes
        """
        return [paciente for _, paciente in sorted(self._fila, key=lambda x: x[0])]