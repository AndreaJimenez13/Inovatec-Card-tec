import pyodbc
from datetime import datetime

# Configuración de la conexión
DB_CONFIG = {
    "driver": "{SQL Server}",
    "server": "TU_SERVIDOR", # Ejemplo: 'localhost' o el nombre de tu PC
    "database": "CardTec",
    "trusted_connection": "yes" # Usa tu cuenta de Windows
}

def get_connection():
    # Crea el "túnel" de comunicación
    conn_str = f"DRIVER={DB_CONFIG['driver']};SERVER={DB_CONFIG['server']};DATABASE={DB_CONFIG['database']};Trusted_Connection={DB_CONFIG['trusted_connection']};"
    return pyodbc.connect(conn_str)

def registrar_acceso(uid: str, punto_id: int, concedido: bool) -> int:
    """
    Inserta un nuevo registro de acceso en la tabla Historial_acceso.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Obtenemos fecha y hora actual
        ahora = datetime.now()
        fecha = ahora.strftime('%Y-%m-%d')
        hora = ahora.strftime('%H:%M:%S')

        # La "orden" para la base de datos
        query = """INSERT INTO Historial_acceso (RFID_UID, id_puntos_acceso, fecha, hora, acceso_concedido)
                   VALUES (?, ?, ?, ?, ?)"""
        
        cursor.execute(query, (uid, punto_id, fecha, hora, 1 if concedido else 0))
        conn.commit() # ¡Importante! Guarda los cambios permanentemente
        
        print("Acceso guardado exitosamente.")
        return True
    except Exception as e:
        print(f"Error al conectar: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close() # Cerramos el túnel para no desperdiciar recursos