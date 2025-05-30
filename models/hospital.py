from typing import Dict, List, Optional
from models.medico import Medico
from models.paciente import Paciente
from models.especialidade import Especialidade
from models.fila import Fila
import time
import random


class Hospital:
    def __init__(self, nome: str):
        self.nome = nome
        self.medicos: List[Medico] = []
        self.filas_espera: Dict[Especialidade, Fila] = {}
        self.pacientes_atendidos: List[Paciente] = []
        self.historico_medicos: Dict[int, List[Dict]] = {}  # ID médico: lista de atendimentos
        self._inicializar_filas()

    def _inicializar_filas(self) -> None:
        """Inicializa filas de espera para todas as especialidades"""
        for especialidade in Especialidade:
            self.filas_espera[especialidade] = Fila()

    def adicionar_medico(self, medico: Medico) -> None:
        """Cadastra um novo médico no hospital"""
        self.medicos.append(medico)
        self.historico_medicos[medico.id] = []

    def admitir_paciente(self, paciente: Paciente) -> None:
        """Adiciona paciente na fila de espera apropriada"""
        if not paciente.especialidade:
            paciente.especialidade = self._determinar_especialidade(paciente.gravidade)

        fila = self.filas_espera[paciente.especialidade]
        fila.adicionar_paciente(paciente)

    def _determinar_especialidade(self, gravidade: int) -> Especialidade:
        """Determina a especialidade adequada baseada na gravidade"""
        if gravidade == 1:  # Casos mais graves
            return Especialidade.URGENCIA
        elif gravidade == 2:
            return random.choice([Especialidade.CARDIOLOGIA, Especialidade.NEUROLOGIA])
        else:
            return Especialidade.CLINICO_GERAL

    def atender_pacientes(self) -> None:
        """Processa o atendimento de pacientes por todos os médicos disponíveis"""
        for medico in self.medicos:
            if not medico.ocupado:
                fila = self.filas_espera[medico.especialidade]

                if len(fila) > 0:
                    paciente = fila.atender_proximo()
                    medico.iniciar_atendimento(paciente)
                    print(f"{medico.nome} iniciou atendimento de {paciente.nome}")

    def finalizar_atendimentos(self) -> None:
        """Finaliza atendimentos que já completaram o tempo médio"""
        for medico in self.medicos:
            if medico.ocupado and medico.tempo_restante_atendimento() <= 0:
                paciente = medico.finalizar_atendimento()
                self.pacientes_atendidos.append(paciente)
                self._registrar_atendimento(medico, paciente)
                print(f"{medico.nome} finalizou atendimento de {paciente.nome}")

    def _registrar_atendimento(self, medico: Medico, paciente: Paciente) -> None:
        """Registra estatísticas do atendimento"""
        registro = {
            'paciente_id': paciente.id,
            'paciente_nome': paciente.nome,
            'hora_inicio': paciente.hora_atendimento,
            'hora_fim': paciente.hora_saida,
            'tempo_espera': paciente.tempo_espera(),
            'gravidade': paciente.gravidade
        }
        self.historico_medicos[medico.id].append(registro)

    def mostrar_estado(self) -> None:
        """Exibe o estado atual do hospital"""
        print(f"\n=== {self.nome.upper()} ===")
        print("\nMédicos:")
        for medico in self.medicos:
            print(f"  - {medico}")

        print("\nFilas de espera:")
        for especialidade, fila in self.filas_espera.items():
            print(f"\nEspecialidade: {especialidade.name}")
            fila.mostrar_fila()

        print(f"\nTotal pacientes atendidos: {len(self.pacientes_atendidos)}")
        print("=" * 50)

    def gerar_relatorio(self) -> Dict:
        """Gera um relatório com estatísticas do hospital"""
        relatorio = {
            'nome_hospital': self.nome,
            'total_medicos': len(self.medicos),
            'total_pacientes_atendidos': len(self.pacientes_atendidos),
            'especialidades': {},
            'tempo_medio_espera': 0,
            'medicos': []
        }

        # Calcula estatísticas por especialidade
        tempo_total_espera = 0
        for especialidade, fila in self.filas_espera.items():
            relatorio['especialidades'][especialidade.name] = {
                'em_espera': len(fila),
                'atendidos': sum(1 for p in self.pacientes_atendidos
                                 if p.especialidade == especialidade)
            }

        # Calcula tempo médio de espera
        if self.pacientes_atendidos:
            tempo_total_espera = sum(p.tempo_espera() or 0
                                     for p in self.pacientes_atendidos)
            relatorio['tempo_medio_espera'] = (
                    tempo_total_espera / len(self.pacientes_atendidos))

        # Estatísticas por médico
        for medico in self.medicos:
            relatorio['medicos'].append({
                'id': medico.id,
                'nome': medico.nome,
                'especialidade': medico.especialidade.name,
                'pacientes_atendidos': medico.total_pacientes_atendidos,
                'tempo_medio_atendimento': (
                    medico.tempo_total_atendimento / 60 / medico.total_pacientes_atendidos
                    if medico.total_pacientes_atendidos > 0 else 0)
            })

        return relatorio