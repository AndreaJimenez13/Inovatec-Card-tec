"""
db.py — Capa de datos
=====================
Conecta tu base de datos MySQL/MariaDB.

PENDIENTE: reemplaza cada funcion con tu logica real de conexion.
Por ahora cada funcion tiene datos de ejemplo para que la UI funcione
sin BD mientras desarrollas.
"""

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURA TU CONEXION AQUI
# ─────────────────────────────────────────────────────────────────────────────
# import mysql.connector
#
# DB_CONFIG = {
#     "host":     "localhost",
#     "port":     3306,
#     "user":     "root",
#     "password": "TU_PASSWORD",
#     "database": "rfid_acceso",
# }
#
# def get_connection():
#     return mysql.connector.connect(**DB_CONFIG)
# ─────────────────────────────────────────────────────────────────────────────


def registrar_acceso(uid: str, nombre: str, tipo: str,
                     fecha: str, hora: str,
                     matricula: str = None, programa: str = None,
                     modalidad: str = None) -> int:
    """
    Inserta un nuevo registro de acceso.
    Retorna el id del registro creado.

    Campos:
        uid       — identificador unico de la tarjeta RFID
        nombre    — nombre completo del usuario
        tipo      — 'Estudiante' o 'Visitante'
        fecha     — fecha en formato YYYY-MM-DD
        hora      — hora en formato HH:MM:SS
        matricula — numero de matricula (solo estudiantes)
        programa  — programa academico (solo estudiantes)
        modalidad — modalidad (solo estudiantes)

    TODO: conectar a tabla `accesos`
    """
    # --- REEMPLAZA CON TU QUERY ---
    # conn = get_connection()
    # cursor = conn.cursor()
    # cursor.execute(
    #     """INSERT INTO accesos
    #        (uid, nombre, tipo, fecha, hora, matricula, programa, modalidad)
    #        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
    #     (uid, nombre, tipo, fecha, hora, matricula, programa, modalidad)
    # )
    # conn.commit()
    # return cursor.lastrowid
    print(f"[DB MOCK] Registrar: uid={uid} nombre={nombre} tipo={tipo} "
          f"fecha={fecha} hora={hora}")
    return 1  # id de prueba
