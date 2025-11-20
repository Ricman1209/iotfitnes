from spyne import Application, rpc, ServiceBase, Integer, Unicode, Float, Date
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
from datetime import date

# =============================
#      BASE DE DATOS SIMPLE
#   (Estructuras en memoria)
# =============================

usuarios = {}                   # id → nombre
dispositivos = {}               # id → {tipo, marca, serie, user}
actividad_diaria = {}           # (user_id, fecha) → {pasos, calorias}
frecuencia = []                 # registros de bpm
sesiones = []                   # sesiones de entrenamiento


# =============================
#            SERVICIO
# =============================
class IoTFitnessService(ServiceBase):

    # ------------------------
    # 1. Registrar Usuario
    # ------------------------
    @rpc(Integer, Unicode, _returns=Unicode)
    def registrarUsuario(ctx, user_id, nombre):
        usuarios[user_id] = nombre
        return f"Usuario {nombre} registrado con id {user_id}"

    # ------------------------
    # 2. Registrar Dispositivo IoT
    # ------------------------
    @rpc(Integer, Unicode, Unicode, Unicode, _returns=Unicode)
    def registrarDispositivo(ctx, disp_id, tipo, marca, serie):
        dispositivos[disp_id] = {
            "tipo": tipo,
            "marca": marca,
            "serie": serie
        }
        return f"Dispositivo {disp_id} registrado ({tipo} - {marca})"

    # ------------------------
    # 3. Registrar Actividad Diaria
    # ------------------------
    @rpc(Integer, Integer, Float, Date, _returns=Unicode)
    def registrarActividad(ctx, user_id, pasos, calorias, fecha):
        actividad_diaria[(user_id, fecha)] = {
            "pasos": pasos,
            "calorias": calorias
        }
        return "Actividad registrada correctamente"

    # ------------------------
    # 4. Registrar Sesión de entrenamiento
    # ------------------------
    @rpc(Integer, Unicode, Integer, _returns=Unicode)
    def registrarSesion(ctx, user_id, tipo, duracion_min):
        sesiones.append({
            "user_id": user_id,
            "tipo": tipo,
            "duración": duracion_min
        })
        return "Sesión registrada"

    # ------------------------
    # 5. Registrar Frecuencia Cardiaca
    # ------------------------
    @rpc(Integer, Integer, Date, _returns=Unicode)
    def registrarFrecuencia(ctx, user_id, bpm, fecha):
        frecuencia.append({
            "user_id": user_id,
            "bpm": bpm,
            "fecha": fecha
        })
        return "Frecuencia registrada"

    # ------------------------
    # Resumen Diario (SOAP)
    # ------------------------
    @rpc(Integer, Date, _returns=Unicode)
    def resumenDiario(ctx, user_id, fecha):
        key = (user_id, fecha)
        if key not in actividad_diaria:
            return "No hay actividad registrada"

        act = actividad_diaria[key]
        return f"Pasos: {act['pasos']}, Calorías: {act['calorias']}"


# =============================
#        APLICACIÓN SOAP
# =============================
soap_app = Application(
    [IoTFitnessService],
    tns="iot.fitness.soap",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(),
)

wsgi_app = WsgiApplication(soap_app)


# =============================
#        SERVIDOR WSGI
# =============================
if __name__ == "__main__":
    print("Servidor SOAP corriendo en http://localhost:8000")
    print("WSDL disponible en: http://localhost:8000/?wsdl")

    server = make_server("0.0.0.0", 8000, wsgi_app)
    server.serve_forever()
