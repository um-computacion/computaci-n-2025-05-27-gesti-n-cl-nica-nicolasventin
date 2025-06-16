import unicodedata

class Medico:
    def __init__(self, nombre, matricula):
        self.__nombre__ = nombre
        self.__matricula__ = matricula
        self.__especialidades__ = []

    def agregar_especialidad(self, especialidad):
        self.__especialidades__.append(especialidad)

    def obtener_matricula(self):
        return self.__matricula__

    def obtener_especialidades(self):
        return self.__especialidades__.copy()

    def obtener_especialidad_para_dia(self, dia):
        dia_normalizado = self.__normalizar_dia(dia)
        for esp in self.__especialidades__:
            if esp.verificar_dia(dia_normalizado):
                return esp.obtener_especialidad()
        return None

    def __normalizar_dia(self, dia):
        dia = dia.strip().lower()
        dia = unicodedata.normalize("NFKD", dia).encode("ascii", "ignore").decode("utf-8")
        return dia

    def __str__(self):
        especialidades_str = "\n  ".join(str(e) for e in self.__especialidades__)
        return f"{self.__nombre__} (Matrícula: {self.__matricula__})\n  {especialidades_str}"
