import unicodedata

class Especialidad:
    DIAS_VALIDOS = {"lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"}

    def __init__(self, tipo, dias):
        self.__tipo__ = tipo
        self.__dias__ = []

        for d in dias:
            dia_normalizado = self.__normalizar_dia(d)
            if dia_normalizado not in self.DIAS_VALIDOS:
                raise ValueError(f"Día inválido: '{d}'")
            self.__dias__.append(dia_normalizado)

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
