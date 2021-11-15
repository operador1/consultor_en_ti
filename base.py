import sqlite3
from sqlite3 import Error


def conexion():
    try:
        conn = sqlite3.connect('base.db')
        return conn
    except Error:
        print("o rayos! :(")


def db_cliente():
    conn = conexion()
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
    conn.commit()
    conn.close()


def buscarClienteSegunId(idCliente):
    try:
        conn = conexion()
        cursor = conn.cursor()
        dato = cursor.execute(
            "SELECT nom_ape,num_doc,num_cuit,num_cel,direc,localidad,sexo FROM Clientes WHERE id_cliente==(?);",
            idCliente, )
        return dato
    except Error:
        print("error detectado")
        return "NO"


def guardarClienteModificado(dato):
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Clientes SET nom_ape=(?),num_doc=(?),num_cuit=(?),num_cel=(?),direc=(?),localidad=(?),sexo=(?) WHERE id_cliente==(?)",
        dato)
    conn.commit()
    conn.close()


def insertar_base_cliente(dato):  # [nombre, documento, cuit, celular, direccion,localidad,sexo]
    try:
        conn = conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Clientes(nom_ape, num_doc, num_cuit, num_cel, direc, localidad, sexo) VALUES (?,?,?,?,?,?,?)",
            dato)
        conn.commit()
        conn.close()
        return 'cliente guardado'
    except ValueError:
        print("error del tipo ValueError")
    except sqlite3.IntegrityError:
        print("error IntegrityError, valores repetidos")
        return 'error, valores repetidos'


def db_trabajo():
    conn = conexion()
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
    conn.commit()
    conn.close()


def existeCuitParaTrabajo(dato):  # [tipo, factura, monto, fecha, cuit]
    try:
        conn = conexion()
        cursor = conn.cursor()
        print('---------22222-----------')
        print(dato) #[tipo, factura, monto, fecha, cuit]
        existe = \
            cursor.execute("select count(*) num_cuit FROM Clientes WHERE num_cuit==(?);", (dato[4],)).fetchall()[0][
                0]
        print(existe)
        if existe == 1:
            return 'existe'
        elif existe == 0:
            return 'no existe'
        else:
            print('error inesperado en existencia de cliente para el trabajo, un problemon')
            return 'no existe'
    except Error:
        pass
        # if existe

        # cursor.execute("INSERT INTO Trabajos (tipo_trab,factura,monto_trab,fecha_entreg,num_cuit) VALUES (?,?,?,?,?)",
        #                dato)
        # conn.commit()
        # conn.close()
        # print("TRABAJO GUARDADO! ! !")
    # except ValueError:
    #     print("error2valueerror")
    # except sqlite3.IntegrityError:
    #     print("error2integrityerror")
    #     return 'error'


def guardoTrabajoSegunCuit(dato):  # dato = [tipo, factura, monto, fecha, cuit]
    try:
        conn = conexion()
        cursor = conn.cursor()
        print(dato)
        cursor.execute("INSERT INTO Trabajos (tipo_trab,factura,monto_trab,fecha_entreg,num_cuit) VALUES (?,?,?,?,?)",dato)
        conn.commit()
        conn.close()
    except Error:
        print('====ERROR====')

        # (tipo_trab,factura,monto_trab,fecha_entreg,num_cuit)


def extraer_base_cliente_nomape_numcuit(dato):  # dato=['%' + nombreApellido + '%','%' + numCuit + '%']
    try:
        conn = conexion()
        cursor = conn.cursor()
        print('---------------')
        print(dato)
        # print('----select * from clientes where nom_ape like 'a%';-----------')
        resultado = cursor.execute("SELECT OR IGNORE * FROM Clientes WHERE nom_ape like ? AND num_cuit like ?",
                                   dato, )
        conn.close()
        return resultado
    except Error:
        print('error en extraer_base_cliente_nomape_numcuit')
        return 'error'


def extraer_base_cliente_nomape(dato):  # dato=['%' + nombreApellido + '%']
    try:
        conn = conexion()
        cursor = conn.cursor()
        resultado = cursor.execute("SELECT OR IGNORE * FROM Clientes WHERE nom_ape like ?", dato, )
        conn.close()
        return resultado
    except Error:
        print('error en extraer_base_cliente_nomape_numcuit')


def extraer_base_cliente_numcuit(dato):  # dato=['%' + nombreApellido + '%','%' + numCuit + '%']
    try:
        conn = conexion()
        cursor = conn.cursor()
        print('---------------')
        print(dato)
        # print('----select * from clientes where nom_ape like 'a%';-----------')
        resultado = cursor.execute("SELECT OR IGNORE * FROM Clientes WHERE num_cuit like ?",
                                   dato, )
        conn.close()
        return resultado
    except Error:
        print('error en extraer_base_cliente_nomape_numcuit')


def extraer_base_cliente_nomape(dato):  # dato=['%' + nombreApellido + '%']
    conn = conexion()
    cursor = conn.cursor()
    resultado = cursor.execute("SELECT * FROM Clientes WHERE nom_ape like ?", (dato,)).fetchall()
    conn.close()
    return resultado


def extraer_base_cliente_numcuit(dato):  # dato=['%' + numCuit + '%']
    try:
        conn = conexion()
        cursor = conn.cursor()
        resultado = cursor.execute("SELECT * FROM Clientes WHERE num_cuit like ?", (dato,)).fetchall()
        print('------a-d-awd-awd')
        conn.close()
        return resultado
    except Error:
        print('hola mundo!')


def extraer_todo_base_cliente():
    conn = conexion()
    cursor = conn.cursor()
    resultado = cursor.execute("SELECT * FROM Clientes ")
    conn.close()
    return resultado
