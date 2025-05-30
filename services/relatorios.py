from typing import Dict, List
from models.paciente import Paciente
from models.medico import Medico
from services.atendimento import SimuladorAtendimento


def gerar_relatorio(simulador: SimuladorAtendimento) -> Dict:
    relatorio = {
        'estatisticas_gerais': {
            'tempo_total': simulador.tempo_total,
            'pacientes_atendidos': len(simulador.pacientes_atendidos),
            'pacientes_na_fila': len(simulador.fila),
            'taxa_atendimento': len(
                simulador.pacientes_atendidos) / simulador.tempo_total if simulador.tempo_total > 0 else 0
        },
        'tempos_espera': {
            'medio': 0,
            'maximo': 0,
            'minimo': 0
        },
        'por_gravidade': {},
        'por_especialidade': {},
        'desempenho_medicos': []
    }

    # Calcula tempos de espera
    tempos_espera = [p.tempo_espera() for p in simulador.pacientes_atendidos if p.tempo_espera() is not None]
    if tempos_espera:
        relatorio['tempos_espera']['medio'] = sum(tempos_espera) / len(tempos_espera)
        relatorio['tempos_espera']['maximo'] = max(tempos_espera)
        relatorio['tempos_espera']['minimo'] = min(tempos_espera)

    # Agrupa por gravidade
    for gravidade in range(1, 6):
        pacientes_grav = [p for p in simulador.pacientes_atendidos if p.gravidade == gravidade]
        relatorio['por_gravidade'][gravidade] = {
            'quantidade': len(pacientes_grav),
            'tempo_medio_espera': sum(p.tempo_espera() for p in pacientes_grav if p.tempo_espera()) / len(
                pacientes_grav) if pacientes_grav else 0
        }

    # Agrupa por especialidade
    especialidades = set(p.especialidade for p in simulador.pacientes_atendidos if p.especialidade)
    for esp in especialidades:
        pacientes_esp = [p for p in simulador.pacientes_atendidos if p.especialidade == esp]
        relatorio['por_especialidade'][str(esp)] = {
            'quantidade': len(pacientes_esp),
            'tempo_medio_espera': sum(p.tempo_espera() for p in pacientes_esp if p.tempo_espera()) / len(
                pacientes_esp) if pacientes_esp else 0
        }

    # Desempenho dos médicos
    for medico in simulador.medicos:
        relatorio['desempenho_medicos'].append({
            'id': medico.id,
            'nome': medico.nome,
            'especialidade': str(medico.especialidade),
            'pacientes_atendidos': medico.total_pacientes_atendidos,
            'tempo_medio_atendimento': medico.tempo_total_atendimento / medico.total_pacientes_atendidos / 60 if medico.total_pacientes_atendidos > 0 else 0
        })

    # Exibe o relatório formatado
    print("\n=== RELATÓRIO FINAL ===")
    print(f"Total pacientes atendidos: {relatorio['estatisticas_gerais']['pacientes_atendidos']}")
    print(f"Tempo médio de espera: {relatorio['tempos_espera']['medio']:.1f} minutos")

    print("\nPor gravidade:")
    for grav, dados in relatorio['por_gravidade'].items():
        print(f"  Gravidade {grav}: {dados['quantidade']} pacientes (média {dados['tempo_medio_espera']:.1f} min)")

    print("\nDesempenho dos médicos:")
    for med in relatorio['desempenho_medicos']:
        print(
            f"  {med['nome']}: {med['pacientes_atendidos']} atendidos (média {med['tempo_medio_atendimento']:.1f} min/paciente)")

    return relatorio