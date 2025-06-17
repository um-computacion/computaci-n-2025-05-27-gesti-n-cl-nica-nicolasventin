import unicodedata
from modelo.historia_clinica import HistoriaClinica
from modelo.turno import Turno
from modelo.receta import Receta
from modelo.excepciones import (
    PacienteNoEncontradoException,
    MedicoNoDisponibleException,
    TurnoOcupadoException,
    RecetaInvalidaException,
    MedicoNoEncontradoException
)

class Clinica:
    def __init__(self):
        self.__pacientes__ = {}
        self.__medicos__ = {}
        self.__turnos__ = []
        self.__historias_clinicas__ = {}

    def agregar_paciente(self, paciente):
        dni = paciente.obtener_dni()
        if dni in self.__pacientes__:
            raise ValueError(f"Ya existe un paciente con el DNI {dni}")
        self.__pacientes__[dni] = paciente
        self.__historias_clinicas__[dni] = HistoriaClinica(paciente)

    def agregar_medico(self, medico):
        matricula = medico.obtener_matricula()
        if matricula in self.__medicos__:
            raise ValueError(f"Ya existe un médico con la matrícula {matricula}")
        self.__medicos__[matricula] = medico

    def obtener_turnos(self):
        return self.__turnos__.copy()

    def obtener_historia_clinica(self, dni):
        return self.__historias_clinicas__[dni]

    def agendar_turno(self, dni, matricula, especialidad, fecha_hora):
        if dni not in self.__pacientes__:
            raise PacienteNoEncontradoException()
        if matricula not in self.__medicos__:
            raise MedicoNoEncontradoException()

        medico = self.__medicos__[matricula]
        dia_semana = self.obtener_dia_semana(fecha_hora)

        disponible = medico.obtener_especialidad_para_dia(dia_semana)

        if not disponible or self.__normalizar_texto(disponible) != self.__normalizar_texto(especialidad):
            raise MedicoNoDisponibleException()

        for turno in self.__turnos__:
            if turno.obtener_medico() == medico and turno.obtener_fecha_hora() == fecha_hora:
                raise TurnoOcupadoException()

        paciente = self.__pacientes__[dni]
        turno = Turno(paciente, medico, fecha_hora, especialidad)
        self.__turnos__.append(turno)
        self.__historias_clinicas__[dni].agregar_turno(turno)

    def emitir_receta(self, dni, matricula, medicamentos):
        if dni not in self.__pacientes__:
            raise PacienteNoEncontradoException()
        if matricula not in self.__medicos__:
            raise MedicoNoDisponibleException()
        if not medicamentos:
            raise RecetaInvalidaException()

        paciente = self.__pacientes__[dni]
        medico = self.__medicos__[matricula]
        receta = Receta(paciente, medico, medicamentos)
        self.__historias_clinicas__[dni].agregar_receta(receta)

    def obtener_dia_semana(self, fecha_hora):
        dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        return dias[fecha_hora.weekday()]

    def __normalizar_texto(self, texto):
        texto = texto.strip().lower()
        texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("utf-8")
        return texto

    def obtener_pacientes(self):
        return list(self.__pacientes__.values())

    def obtener_medicos(self):
        return list(self.__medicos__.values())

    def obtener_medico_por_matricula(self, matricula):
        return self.__medicos__.get(matricula)
