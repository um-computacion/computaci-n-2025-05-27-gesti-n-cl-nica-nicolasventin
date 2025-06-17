import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modelo.clinica import Clinica
from modelo.paciente import Paciente
from modelo.medico import Medico
from modelo.especialidad import Especialidad
from modelo.excepciones import *
from datetime import datetime

class CLI:
    def __init__(self):
        self.clinica = Clinica()

    def mostrar_menu(self):
        while True:
            print("\n--- Menú Clínica ---")
            print("1) Agregar paciente")
            print("2) Agregar médico")
            print("3) Agregar especialidad a médico")
            print("4) Agendar turno")
            print("5) Emitir receta")
            print("6) Ver historia clínica")
            print("7) Ver todos los turnos")
            print("8) Ver todos los pacientes")
            print("9) Ver todos los médicos")
            print("0) Salir")

            opcion = input("Seleccioná una opción: ")

            if opcion == "1":
                self.agregar_paciente()
            elif opcion == "2":
                self.agregar_medico()
            elif opcion == "3":
                self.agregar_especialidad()
            elif opcion == "4":
                self.agendar_turno()
            elif opcion == "5":
                self.emitir_receta()
            elif opcion == "6":
                self.ver_historia_clinica()
            elif opcion == "7":
                self.ver_turnos()
            elif opcion == "8":
                self.ver_pacientes()
            elif opcion == "9":
                self.ver_medicos()
            elif opcion == "0":
                print("Saliendo...")
                break
            else:
                print("Opción inválida.")

    def agregar_paciente(self):
        pasos = ["nombre", "dni", "fecha"]
        datos = {}
        indice = 0

        while indice < len(pasos):
            paso = pasos[indice]
            entrada = input(f"{'Nombre y apellido del paciente' if paso == 'nombre' else 'DNI' if paso == 'dni' else 'Fecha de nacimiento (dd/mm/aaaa)'} ('salir' para menú, 'volver' para atrás): ")
            if entrada.lower() == "salir":
                return
            if entrada.lower() == "volver":
                if indice > 0:
                    indice -= 1
                continue
            datos[paso] = entrada
            indice += 1

        try:
            paciente = Paciente(datos["nombre"], datos["dni"], datos["fecha"])
            self.clinica.agregar_paciente(paciente)
            print("Paciente agregado.")
        except Exception as e:
            print("Error:", e)
            self.agregar_paciente()

    def agregar_medico(self):
        pasos = ["nombre", "matricula"]
        datos = {}
        indice = 0

        while indice < len(pasos):
            paso = pasos[indice]
            entrada = input(f"{'Nombre del médico' if paso == 'nombre' else 'Matrícula'} ('salir' para menú, 'volver' para atrás): ")
            if entrada.lower() == "salir":
                return
            if entrada.lower() == "volver":
                if indice > 0:
                    indice -= 1
                continue
            datos[paso] = entrada.upper() if paso == "matricula" else entrada
            indice += 1

        try:
            medico = Medico(datos["nombre"], datos["matricula"])
            self.clinica.agregar_medico(medico)
            print("Médico agregado.")
        except Exception as e:
            print("Error:", e)
            self.agregar_medico()

    def agregar_especialidad(self):
        pasos = ["matricula", "tipo", "dias"]
        datos = {}
        indice = 0

        while indice < len(pasos):
            paso = pasos[indice]
            entrada = input(f"{'Matrícula del médico' if paso == 'matricula' else 'Especialidad' if paso == 'tipo' else 'Días de atención (separados por coma)'} ('salir' para menú, 'volver' para atrás): ")
            if entrada.lower() == "salir":
                return
            if entrada.lower() == "volver":
                if indice > 0:
                    indice -= 1
                continue
            datos[paso] = entrada.upper() if paso == "matricula" else entrada
            indice += 1

        try:
            dias = [d.strip() for d in datos["dias"].split(",")]
            especialidad = Especialidad(datos["tipo"], dias)
            medico = self.clinica.obtener_medico_por_matricula(datos["matricula"])
            if medico is None:
                print("Error: No se encontró un médico con esa matrícula.")
                return
            medico.agregar_especialidad(especialidad)
            print("Especialidad agregada.")
        except ValueError as ve:
            print("Error:", ve)
            self.agregar_especialidad()
        except Exception as e:
            print("Error:", e)
            self.agregar_especialidad()

    def agendar_turno(self):
        pasos = ["dni", "matricula", "especialidad", "fecha"]
        datos = {}
        indice = 0

        while indice < len(pasos):
            paso = pasos[indice]
            if paso == "fecha":
                entrada = input("Fecha y hora (dd/mm/aaaa HH:MM) ('salir' para menú, 'volver' para atrás): ")
            else:
                entrada = input(f"{paso.capitalize()} del turno ('salir' para menú, 'volver' para atrás): ")

            if entrada.lower() == "salir":
                return
            if entrada.lower() == "volver":
                if indice > 0:
                    indice -= 1
                continue

            if paso == "fecha":
                try:
                    datos[paso] = datetime.strptime(entrada, "%d/%m/%Y %H:%M")
                    indice += 1
                except ValueError:
                    print("Formato inválido. Usá: dd/mm/aaaa HH:MM")
            else:
                datos[paso] = entrada.upper() if paso == "matricula" else entrada
                indice += 1

        try:
            self.clinica.agendar_turno(
                datos["dni"],
                datos["matricula"],
                datos["especialidad"],
                datos["fecha"]
            )
            print("Turno agendado correctamente.")

        except MedicoNoDisponibleException:
            print("Error: El médico no atiende esa especialidad ese día.")
            medico = self.clinica.obtener_medico_por_matricula(datos["matricula"])
            if medico:
                print("Especialidades disponibles:")
                for esp in medico.obtener_especialidades():
                    print(" -", str(esp))
            self.agendar_turno()
        
        except MedicoNoEncontradoException:
            print("Error: No se encontró ningún médico con esa matrícula.")
            self.agendar_turno()

        except PacienteNoEncontradoException:
            print("Error: Paciente no encontrado.")
            self.agendar_turno()

        except TurnoOcupadoException:
            print("Error: Ese horario ya está ocupado por el médico.")
            self.agendar_turno()

        except Exception as e:
            print("Error inesperado:", e)
            self.agendar_turno()

    def emitir_receta(self):
        pasos = ["dni", "matricula", "medicamentos"]
        datos = {}
        indice = 0

        while indice < len(pasos):
            paso = pasos[indice]
            entrada = input(f"{'DNI del paciente' if paso == 'dni' else 'Matrícula del médico' if paso == 'matricula' else 'Medicamentos (separados por coma)'} ('salir' para menú, 'volver' para atrás): ")
            if entrada.lower() == "salir":
                return
            if entrada.lower() == "volver":
                if indice > 0:
                    indice -= 1
                continue
            datos[paso] = entrada.upper() if paso == "matricula" else entrada
            indice += 1

        try:
            medicamentos = [m.strip() for m in datos["medicamentos"].split(",")]
            self.clinica.emitir_receta(datos["dni"], datos["matricula"], medicamentos)
            print("Receta emitida.")
        except (PacienteNoEncontradoException, MedicoNoDisponibleException, RecetaInvalidaException) as e:
            print(f"Error: {e.__class__.__name__}")
            self.emitir_receta()
        except Exception as e:
            print("Error:", e)
            self.emitir_receta()

    def ver_historia_clinica(self):
        dni = input("DNI del paciente ('salir' para menú): ")
        if dni.lower() == "salir":
            return
        try:
            historia = self.clinica.obtener_historia_clinica(dni)
            print(historia)
        except Exception as e:
            print("Error:", e)

    def ver_turnos(self):
        for turno in self.clinica.obtener_turnos():
            print(turno)

    def ver_pacientes(self):
        for p in self.clinica.obtener_pacientes():
            print(p)

    def ver_medicos(self):
        for m in self.clinica.obtener_medicos():
            print(m)

if __name__ == "__main__":
    CLI().mostrar_menu()
