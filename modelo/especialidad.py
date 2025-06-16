import unicodedata

class Especialidad:
    def __init__(self, tipo, dias):
        self.__tipo__ = tipo
        self.__dias__ = [self.__normalizar_dia(d) for d in dias]

    def obtener_especialidad(self):
        return self.__tipo__

    def verificar_dia(self, dia):
        return self.__normalizar_dia(dia) in self.__dias__

    def __normalizar_dia(self, dia):
        dia = dia.strip().lower()
        dia = unicodedata.normalize("NFKD", dia).encode("ascii", "ignore").decode("utf-8")
        return dia

    def __str__(self):
        dias_str = ", ".join(self.__dias__)
        return f"{self.__tipo__} (Días: {dias_str})"
