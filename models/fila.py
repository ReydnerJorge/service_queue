class Fila:
    def __init__(self):
        self.fila = []

    def adicionar_paciente(self, paciente):
        """Adiciona paciente na fila com base na gravidade"""
        self.fila.append(paciente)
        self.fila.sort(key=lambda x: x.gravidade)

    def atender_proximo(self):
        """Remove e retornar o próximo paciente da fila"""
        if self.fila:
            return self.fila.pop(0)
        return None

    def mostrar_fila(self):
        """Exibe a fila atual"""
        print('\n--- FILA DE ATENDIMENTO ---')
        for paciente in self.fila:
            print(paciente)
        print(f'Total na fila: {len(self.fila)} pacientes')
        print('---------------------------')