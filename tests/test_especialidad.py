import unittest
from modelo.especialidad import Especialidad

class TestEspecialidad(unittest.TestCase):

    def test_creacion_especialidad(self):
        esp = Especialidad("Cardiología", ["Lunes", "Miércoles"])
        self.assertEqual(esp.obtener_especialidad(), "Cardiología")

    def test_verificar_dia_true(self):
        esp = Especialidad("Pediatría", ["martes", "jueves"])
        self.assertTrue(esp.verificar_dia("Jueves"))
        self.assertTrue(esp.verificar_dia("martes"))

    def test_verificar_dia_false(self):
        esp = Especialidad("Dermatología", ["viernes"])
        self.assertFalse(esp.verificar_dia("lunes"))

    def test_str_especialidad(self):
        esp = Especialidad("Neurología", ["lunes", "miércoles"])
        texto = str(esp)
        self.assertIn("Neurología", texto)
        self.assertIn("lunes", texto)
        self.assertIn("miercoles", texto)

if __name__ == "__main__":
    unittest.main()
