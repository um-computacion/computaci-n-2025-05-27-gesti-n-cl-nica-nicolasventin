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

if __name__ == "__main__":
    unittest.main()
