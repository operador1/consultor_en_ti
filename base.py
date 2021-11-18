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
		[sexo] VARCHAR(10)  NULL,
		[borrar] VARCHAR(10)  NULL
		); 
		""")
    conn.commit()
    conn.close()


def buscarClienteSegunId(idCliente):
    try:
        conn = conexion()
        cursor = conn.cursor()
        dato = cursor.execute(
            "SELECT nom_ape,num_doc,num_cuit,num_cel,direc,localidad,sexo FROM Clientes WHERE id_cliente=(?);",
            (idCliente,))
        return dato
    except Error:
        print("error detectado")
        return "NO"


def guardarClienteModificado(conn, dato):
    # conn = conexion()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Clientes SET nom_ape=(?),num_doc=(?),num_cuit=(?),num_cel=(?),direc=(?),localidad=(?),sexo=(?) WHERE id_cliente==(?)",
        dato)
    conn.commit()


def insertar_base_cliente(dato):  # [nombre, documento, cuit, celular, direccion,localidad,sexo]
    try:
        conn = conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Clientes(nom_ape, num_doc, num_cuit, num_cel, direc, localidad, sexo,borrar) VALUES (?,?,?,?,?,?,?,?)",
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
		[factura] VARCHAR(55)  NOT NULL,
		[monto_trab] VARCHAR(55)  NULL,
		[fecha_entreg] VARCHAR(55)  NULL,
		[num_cuit] VARCHAR(55) NOT NULL,
		[monto_pagado] VARCHAR(55) NULL,
		[saldo] VARCHAR(55) NULL
		);
		""")
    conn.commit()
    conn.close()


def existeCuitParaTrabajo(dato):  # [tipo, factura, monto, fecha, cuit]
    try:
        conn = conexion()
        cursor = conn.cursor()
        print('---------22222-----------')
        print(dato)  # [tipo, factura, monto, fecha, cuit]
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


#        dato = [tipo,factura,monto,fecha,cuit]
def guardoTrabajoSegunCuit2(dato):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    datoNuevo = [dato[0], dato[1], dato[2], dato[3], dato[4], dato[2]]
    cursor.execute(
        'insert into Trabajos(tipo_trab,factura,monto_trab,fecha_entreg,num_cuit,saldo) values (?,?,?,?,?,?)',
        datoNuevo)
    conn.commit()
    conn.close()


def guardarSaldoDeTrabajo(monto):
    pass


def extraer_base_cliente_nomape_numcuit(conn, dato):  # dato=['%' + nombreApellido + '%','%' + numCuit + '%']
    try:
        cursor = conn.cursor()
        # print('----select * from clientes where nom_ape like 'a%';-----------')
        resultado = cursor.execute(
            "SELECT num_cuit,num_doc,nom_ape,num_cel,direc,localidad,sexo FROM Clientes WHERE nom_ape like ? AND num_cuit like ?",
            dato, )
        # cuit ~~ documento ~~ nombre y apellido ~~  celular ~~ direccion ~~~ localidad ~~ sexo    7 columnado
        # conn.close()
        return resultado
    except Error:
        print('error en extraer_base_cliente_nomape_numcuit')
        return 'error'


def extraer_base_cliente_nomape3(conn, dato):
    try:
        cursor = conn.cursor()
        print(dato)
        resultado = cursor.execute(
            "SELECT num_cuit,num_doc,nom_ape,num_cel,direc,localidad,sexo FROM Clientes WHERE nom_ape like ? or num_cuit like ?;",
            dato, )

        return resultado
    except Error:
        print('error fatal')


def extraer_base_cliente_nomape(conn, dato):  # dato=['%' + nombreApellido + '%']
    try:
        cursor = conn.cursor()
        print(dato)
        datoNuevo = [dato[0], '%2%']
        print(datoNuevo)

        resultado = cursor.executescript(
            "SELECT num_cuit,num_doc,nom_ape,num_cel,direc,localidad,sexo FROM Clientes WHERE nom_ape like ? and num_cuit like ?;",
            datoNuevo, )
        return resultado
    except Error:
        print('error en extraer_base_cliente_nomape_numcuit')
        return 'error'
    # try:
    #     conn = conexion()
    #     cursor = conn.cursor()
    #     resultado = cursor.execute("SELECT OR IGNORE * FROM Clientes WHERE nom_ape like ?", dato, )
    # resultado = cursor.execute("SELECT OR IGNORE num_cuit,num_doc,nom_ape,num_cel,direc,localidad,sexo FROM Clientes WHERE nom_ape like ?", dato, )
    # print("--------klklklklk----------")
    #
    # conn.close()
    # return resultado
    # except Error:
    #     print('error en extraer_base_cliente_nomape_numcuit')


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


def extraer_todo_base_cliente(conn):
    cursor = conn.cursor()
    # resultado = cursor.execute("SELECT * FROM Clientes;")
    resultado2 = cursor.execute("SELECT num_cuit,num_doc,nom_ape,num_cel,direc,localidad,sexo FROM Clientes where borrar='no';")

    return resultado2


def extraer_cuit_del_cliente(conn, idCli):
    cursor = conn.cursor()
    cuitCliente = cursor.execute('select num_cuit from Clientes where id_cliente=(?)', (idCli,))
    print(cuitCliente)
    return cuitCliente


def trabajosRealizadosSegunCuit(conn, cuit):
    cursor = conn.cursor()
    resultados = cursor.execute('select * from Trabajos where num_cuit=(?);', (cuit,))
    print('hakuna matata')
    return resultados


def pagarUnMonto(idTrabajo, monto):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    montoPagado = cursor.execute('select monto_pagado from Trabajos where id_trabajo=(?)', (idTrabajo,)).fetchall()[0][
        0]
    if montoPagado == None:
        montoPagado = 0

    else:
        float(montoPagado.replace('$', ''))
        pass
    montoPagado = float(montoPagado) + float(monto.replace('$', ''))

    parametro1 = [montoPagado, idTrabajo]
    cursor.execute('UPDATE Trabajos SET monto_pagado=(?) WHERE id_trabajo=(?)', parametro1)
    #######################

    #################
    saldo = cursor.execute('select saldo from Trabajos where id_trabajo=(?)', (idTrabajo,)).fetchall()[0][0].replace(
        '$', '')
    saldo = float(saldo)
    # saldo = saldo - montoPagado
    saldo = saldo - float(monto)

    print('----------SALDO-----------')
    print(saldo)

    parametro = [saldo, idTrabajo]
    cursor.execute('UPDATE Trabajos SET saldo=? WHERE id_trabajo=(?)', parametro)

    conn.commit()
    conn.close()


def cauitSegunIdTrabajo(conn, idTrabajo):
    cursor = conn.cursor()
    cuit = cursor.execute('select num_cuit from Trabajos where id_trabajo=(?)', (idTrabajo,)).fetchall()[0][0]
    return cuit


def calcularIngresoBruto(conn):
    cursor = conn.cursor()
    # fechas = [f1, f2]
    # listaMontoPagado = cursor.execute('select monto_pagado from Trabajos where monto_pagado between (?) and (?)',
    #                                   fechas).fetchall()
    # listaMontoPagado2=cursor.execute('select monto_pagado from Trabajos').fetchall()
    # select monto_pagado from Trabajos where monto_pagado between (?f1) and (?f2)

    respuesta = list(cursor.execute('SELECT monto_pagado FROM Trabajos').fetchall())

    print(respuesta)
    return respuesta

    # print('listaMontoPagado2')
    # print(listaMontoPagado2)


def insertar_base_insumo(dato):  # [descripcion, marca, cantidad, precioUnitario, fechaCompra]
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Insumos(descrip, marca, cant, precio_uni, fecha_compra,total) VALUES (?,?,?,?,?,?)",
        dato)
    conn.commit()
    conn.close()


def db_insumos():
    conn = conexion()
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS [Insumos] (
        [id_insumo] INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
        [descrip] VARCHAR(55)  NULL,
        [marca] VARCHAR(55)  NULL,
        [cant] VARCHAR(20)  NULL,
        [precio_uni] VARCHAR(20)  NULL,
        [fecha_compra] VARCHAR(20)  NULL,
        [total] VARCHAR(20)  NULL
        );
        """)
    conn.commit()
    conn.close()


def extraerListaInsumos(conn):
    cursor = conn.cursor()
    lista = cursor.execute("select total from Insumos;").fetchall()
    return lista
