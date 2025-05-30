from enum import auto, Enum


class Especialidade(Enum):
    CLINICO_GERAL = auto()
    CARDIOLOGIA = auto()
    ORTOPEDIA = auto()
    PEDIATRIA = auto()
    URGENCIA = auto()
    NEUROLOGIA = auto()
    PNEUMOLOGIA = auto()
    GINECOLOGIA = auto()
    OFTAMOLOGIA = auto()
    DERMATOLOGIA = auto()

    def __str__(self):
        return self.name.replace('_', '').title()