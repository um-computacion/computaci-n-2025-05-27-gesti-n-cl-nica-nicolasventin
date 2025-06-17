import unittest
from datetime import datetime
from modelo.clinica import Clinica
from modelo.paciente import Paciente
from modelo.medico import Medico
from modelo.especialidad import Especialidad
from modelo.excepciones import (
    PacienteNoEncontradoException,
    MedicoNoDisponibleException,
    TurnoOcupadoException,
    RecetaInvalidaException,
    MedicoNoEncontradoException
)

class TestClinica(unittest.TestCase):

    def setUp(self):
        self.clinica = Clinica()
        self.paciente = Paciente("Nicolás Ventin", "99999999", "12/12/1995")
        self.medico = Medico("Luciano Miranda", "MP1234")
        self.especialidad = Especialidad("Clínica médica", ["martes"])
        self.medico.agregar_especialidad(self.especialidad)
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)

    def test_agendar_turno_exitoso(self):
        fecha = datetime(2025, 6, 17, 10, 0) 
        self.clinica.agendar_turno("99999999", "MP1234", "Clínica médica", fecha)
        turnos = self.clinica.obtener_turnos()
        self.assertEqual(len(turnos), 1)

    def test_agendar_turno_paciente_inexistente(self):
        fecha = datetime(2025, 6, 17, 10, 0)
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.agendar_turno("00000000", "MP1234", "Clínica médica", fecha)

    def test_agendar_turno_medico_no_disponible(self):
        fecha = datetime(2025, 6, 19, 10, 0) 
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.agendar_turno("99999999", "MP1234", "Clínica médica", fecha)

    def test_emitir_receta_exitosa(self):
        self.clinica.emitir_receta("99999999", "MP1234", ["Paracetamol"])
        historia = self.clinica.obtener_historia_clinica("99999999")
        self.assertEqual(len(historia.obtener_recetas()), 1)

    def test_emitir_receta_vacia(self):
        with self.assertRaises(RecetaInvalidaException):
            self.clinica.emitir_receta("99999999", "MP1234", [])
    
    def test_turno_ocupado(self):
        fecha = datetime(2025, 6, 17, 10, 0)  # martes
        self.clinica.agendar_turno("99999999", "MP1234", "Clínica médica", fecha)
        with self.assertRaises(TurnoOcupadoException):
            self.clinica.agendar_turno("99999999", "MP1234", "Clínica médica", fecha)
    
    def test_no_se_permite_paciente_duplicado(self):
        paciente1 = Paciente("Nicolás", "45718427", "04/05/2004")
        paciente2 = Paciente("Roberto", "45718427", "02/02/2001")
        self.clinica.agregar_paciente(paciente1)
        with self.assertRaises(ValueError):
            self.clinica.agregar_paciente(paciente2)

    def test_no_se_permite_medico_duplicado(self):
        medico1 = Medico("Claudia Elaskar", "MP9999")
        medico2 = Medico("Luciano Miranda", "MP9999")
        self.clinica.agregar_medico(medico1)
        with self.assertRaises(ValueError):
            self.clinica.agregar_medico(medico2)

    def test_no_se_puede_agendar_turno_con_medico_inexistente(self):
        paciente = Paciente("Test Paciente", "100", "01/01/2000")
        self.clinica.agregar_paciente(paciente)

        with self.assertRaises(MedicoNoEncontradoException):
            self.clinica.agendar_turno("100", "MATRI_INEXISTENTE", "Cardiología", datetime(2025, 6, 18, 10, 0))
    
    def test_no_se_puede_agendar_turno_duplicado(self):
        paciente = Paciente("Test Paciente", "101", "01/01/2000")
        medico = Medico("Test Médico", "MP777")
        esp = Especialidad("Cardiología", ["miércoles"])
        medico.agregar_especialidad(esp)

        self.clinica.agregar_paciente(paciente)
        self.clinica.agregar_medico(medico)

        fecha = datetime(2025, 6, 18, 10, 0)  # miércoles
        self.clinica.agendar_turno("101", "MP777", "Cardiología", fecha)

        with self.assertRaises(TurnoOcupadoException):
            self.clinica.agendar_turno("101", "MP777", "Cardiología", fecha)

    def test_turno_especialidad_o_dia_incorrecto(self):
        paciente = Paciente("Paciente A", "102", "01/01/2000")
        medico = Medico("Médico B", "MP778")
        esp = Especialidad("Dermatología", ["lunes"])  # solo lunes

        self.clinica.agregar_paciente(paciente)
        self.clinica.agregar_medico(medico)
        medico.agregar_especialidad(esp)

        fecha = datetime(2025, 6, 18, 10, 0)  # miércoles
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.agendar_turno("102", "MP778", "Dermatología", fecha)

        fecha_lunes = datetime(2025, 6, 16, 10, 0)  # lunes
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.agendar_turno("102", "MP778", "Cardiología", fecha_lunes)

    def test_no_se_puede_emitir_receta_sin_medicamentos(self):
        paciente = Paciente("Paciente A", "300", "01/01/2000")
        medico = Medico("Médico B", "MP300")
        self.clinica.agregar_paciente(paciente)
        self.clinica.agregar_medico(medico)

        with self.assertRaises(RecetaInvalidaException):
            self.clinica.emitir_receta("300", "MP300", [])

    def test_no_se_puede_emitir_receta_a_paciente_inexistente(self):
        medico = Medico("Médico C", "MP301")
        self.clinica.agregar_medico(medico)

        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.emitir_receta("999", "MP301", ["Ibuprofeno"])

    def test_no_se_puede_emitir_receta_con_medico_inexistente(self):
        paciente = Paciente("Paciente B", "301", "01/01/2000")
        self.clinica.agregar_paciente(paciente)

        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.emitir_receta("301", "MP404", ["Amoxicilina"])



if __name__ == "__main__":
    unittest.main()
