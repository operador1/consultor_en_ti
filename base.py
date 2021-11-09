import sqlite3
from sqlite3 import Error


def conexion():
    try:
        conn = sqlite3.connect('base.db')
        return conn
    except Error:
        print("o rayos! :(")


def db_cliente(conn):
    cursor = conn.cursor()
    cursor.executescript(""" 
		CREATE TABLE IF NOT EXISTS [Clientes] (
		[id_cliente] INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
		[nom_ape] VARCHAR(55)  NULL,
		[num_doc] INTEGER  UNIQUE NOT NULL,
		[num_cuit] VARCHAR(13)  UNIQUE NOT NULL,
		[num_cel] INTEGER  NOT NULL,
		[direc] VARCHAR(55)  NULL,
		[localidad] VARCHAR(30)  NULL,
		[sexo] VARCHAR(10)  NULL
		); 
		""")

def buscarClienteSegunId(conn, idCliente):
    try:
        cursor = conn.cursor()
        dato = cursor.execute(
            "SELECT nom_ape,num_doc,num_cuit,num_cel,direc,localidad,sexo FROM Clientes WHERE id_cliente==(?);",
            idCliente, )
        return dato
    except Error:
        print("error detectado")
        return "NO"


def guardarClienteModificado(conn, dato):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Clientes SET nom_ape=(?),num_doc=(?),num_cuit=(?),num_cel=(?),direc=(?),localidad=(?),sexo=(?) WHERE id_cliente==(?)",
        dato)
    conn.commit()
    conn.close()




def insertar_base_cliente(conn, dato):  # [nombre, documento, cuit, celular, direccion,localidad,sexo]
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Clientes(nom_ape, num_doc, num_cuit, num_cel, direc, localidad, sexo) VALUES (?,?,?,?,?,?,?)",
            dato)
        conn.commit()
        return 'bien'
    except ValueError:
        print("error del tipo ValueError")
    except sqlite3.IntegrityError:
        print("error IntegrityError")
        return 'error'


def db_trabajo(conn):
    cursor = conn.cursor()
    cursor.executescript("""
		CREATE TABLE IF NOT EXISTS [Trabajos] (
		[id_trabajo] INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
		[tipo_trab] VARCHAR(55)  NOT NULL,
		[factura] VARCHAR(5)  NOT NULL,
		[monto_trab] VARCHAR(10)  NULL,
		[fecha_entreg] VARCHAR(8)  NULL,
		[num_cuit] VARCHAR(13)  UNIQUE NOT NULL
		);
		""")


def insertar_base_trabajo(conn, dato):  # [tipo, factura, monto, fecha, cuit]
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Trabajos(tipo_trab, factura, monto_trab, fecha_entreg, num_cuit) VALUES (?,?,?,?,?)", dato)
        conn.commit()
        print("bienn")
    except ValueError:
        print("error2valueerror")
    except sqlite3.IntegrityError:
        print("error2integrityerror")
        return 'error'


def extraer_base_cliente_nomape_numcuit(dato):  # dato=['%' + nombreApellido + '%','%' + numCuit + '%']
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Clientes WHERE nom_ape like ? AND num_cuit like ?", dato)
    return cursor


def extraer_base_cliente_nomape(dato):  # dato=['%' + nombreApellido + '%']
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Clientes WHERE nom_ape like ?", dato)
    return cursor


def extraer_base_cliente_numcuit(dato):  # dato=['%' + numCuit + '%']
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Clientes WHERE num_cuit like ?", dato)
    return cursor


def extraer_todo_base_cliente():
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Clientes ")
    return cursor
