import unittest
from modelo.medico import Medico
from modelo.especialidad import Especialidad

class TestMedico(unittest.TestCase):

    def test_creacion_medico(self):
        medico = Medico("Guillermo Ventin", "MP1234")
        self.assertEqual(medico.obtener_matricula(), "MP1234")

    def test_agregar_especialidad(self):
        medico = Medico("Diego Ventin", "MP5678")
        esp = Especialidad("Cardiología", ["lunes", "miércoles"])
        medico.agregar_especialidad(esp)
        self.assertEqual(len(medico.obtener_especialidades()), 1)

    def test_obtener_especialidad_para_dia(self):
        medico = Medico("Raúl Ponte", "MP9999")
        esp = Especialidad("Pediatría", ["martes", "jueves"])
        medico.agregar_especialidad(esp)
        self.assertEqual(medico.obtener_especialidad_para_dia("jueves"), "Pediatría")
        self.assertIsNone(medico.obtener_especialidad_para_dia("lunes"))

if __name__ == "__main__":
    unittest.main()
