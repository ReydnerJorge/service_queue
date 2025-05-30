from models.paciente import Paciente
from models.fila import Fila
from models.medico import Medico
from models.especialidade import Especialidade
from utils.geradores import gerar_pacientes_aleatorios, gerar_medicos_aleatorios
from services.atendimento import SimuladorAtendimento
from services.relatorios import gerar_relatorio
import time


def main():
    # Configuração
    num_pacientes = 20  # Reduzido para demonstração
    num_medicos = 5
    tempo_simulacao = 480  # minutos (8 horas)
    tempo_intervalo = 1  # segundos entre passos da simulação

    print("=== INICIANDO SIMULAÇÃO HOSPITALAR ===")

    # Gerar dados iniciais
    print("\nGerando recursos hospitalares...")
    medicos = gerar_medicos_aleatorios(num_medicos)
    pacientes = gerar_pacientes_aleatorios(num_pacientes)

    # Inicializar fila prioritária
    fila = Fila()
    for paciente in pacientes:
        fila.adicionar_paciente(paciente)

    # Inicializar simulador
    simulador = SimuladorAtendimento(
        fila=fila,
        medicos=medicos,
        tempo_total=tempo_simulacao,
        intervalo=tempo_intervalo
    )

    # Executar simulação
    print("\nIniciando simulação...")
    simulador.executar()

    # Gerar relatórios
    print("\nGerando relatórios finais...")
    gerar_relatorio(simulador)

    print("\n=== SIMULAÇÃO CONCLUÍDA ===")


if __name__ == "__main__":
    main()