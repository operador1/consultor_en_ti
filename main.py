import sys
from PyQt5 import uic, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QDateEdit
from base import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_ui.ui', self)
        self.btnRegistrarcli.clicked.connect(self.ventanaRegistro)
        self.btnRegistrartrab.clicked.connect(self.ventanaCargar)
        self.btnBuscarcli.clicked.connect(self.ventanaBuscar)
        self.btnGanancia.clicked.connect(self.ventanaGanan)
        self.btnInsumos.clicked.connect(self.ventanaInsu)

    def ventanaRegistro(self):
        guiRegistro.show()

    def ventanaCargar(self):
        guiCargar.show()

    def ventanaBuscar(self):
        guiBuscar.show()

    def ventanaGanan(self):
        guiGanan.show()

    def ventanaInsu(self):
        guiInsu.show()


class WindowRegistro(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('registrar_cliente.ui', self)
        self.setWindowTitle('Registrar un nuevo cliente')
        self.btnRegistrar22.clicked.connect(self.ingresarCliente)

    def ingresarCliente(self):
        nombre = self.nombap.text()
        documento = self.numdoc.text()
        cuit = self.numcuit.text()
        celular = self.numcel.text()
        direccion = self.direc.text()
        localidad = self.loc.text()
        sexo = self.sexo.currentText()
        ######################
        # conn = conexion()
        # cursor = conn.cursor()
        # consulta2 = cursor.execute("SELECT COUNT(id_cliente) FROM Clientes;").fetchall() # da [(0,)]
        # conn.close()
        # idCliente = list(consulta2[0])[0] + 1 #int:
        ######################
        dato = [nombre, documento, cuit, celular, direccion, localidad, sexo]
        respuesta = insertar_base_cliente(dato)
        if respuesta == 'error, valores repetidos':
            guiAlerta.show()
        else:
            self.nombap.setText("")
            self.numdoc.setText("")
            self.numcuit.setText("")
            self.numcel.setText("")
            self.direc.setText("")
            self.loc.setText("")
            self.sexo.setCurrentIndex(0)
            guiClienteGuardado.show()


# registrar trabajo
class WindowCargar(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('registrar_trabajo.ui', self)
        self.setWindowTitle('Registrar un nuevo trabajo')
        self.btnRegistrar.clicked.connect(self.ingresarTrabajo)
        self.tipotrab.setText("")
        self.comboBox.setCurrentIndex(0)
        self.montotrab.setText("")

        self.fechaentreg.setText("")  # te vas
        # self.dateEdit.

        self.cuitsolici.setText("")

    def ingresarTrabajo(self):
        tipo = self.tipotrab.text().strip()
        factura = self.comboBox.currentText().strip()
        monto = self.montotrab.text().strip()

        fecha = self.fechaentreg.text().strip()

        dia = self.dateEdit.date().day()
        mes = self.dateEdit.date().month()
        anio = self.dateEdit.date().year()
        print(dia , mes, anio)
        fechaNueva = str(dia) + '/' + str(mes) + '/' + str(anio)

        cuit = self.cuitsolici.text().strip()
        # dato = [tipo, factura, monto, fecha, cuit]
        dato = [tipo, factura, monto, fechaNueva, cuit]
        # saldo=monto
        ############PROBLEMA usar cuit como id del cliente

        respuesta = existeCuitParaTrabajo(dato)  # 'existe' o 'no existe'
        print('----------respuesta-------------')
        print(respuesta)

        if respuesta == 'existe':

            guardoTrabajoSegunCuit2(dato)
            guiTrabajoGuardado.show()
            # guardarSaldoDeTrabajo(saldo)
            self.tipotrab.setText("")
            self.comboBox.setCurrentIndex(0)
            self.montotrab.setText("")
            self.fechaentreg.setText("")
            self.cuitsolici.setText("")
        elif respuesta == 'no existe':
            gui_noHayClienteRegistrado.show()
            self.tipotrab.setText("")
            self.comboBox.setCurrentIndex(0)
            self.montotrab.setText("")
            self.fechaentreg.setText("")
            self.cuitsolici.setText("")


class WindowBuscar(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('buscar_cliente.ui', self)
        self.setWindowTitle('Buscar un cliente')
        self.pushButton.clicked.connect(self.mostrartodo)
        self.pushButton_4.clicked.connect(self.pagarUnTrabajo)

        self.pushButton_2.clicked.connect(self.cargarIdCliente)
        self.tableWidget.setColumnCount(10)
        self.pushButton_3.clicked.connect(self.guardarModificacion)

        self.lineEdit.cursorPositionChanged.connect(self.actualizar_tableWidget_Automaticamente)
        self.lineEdit_3.cursorPositionChanged.connect(self.actualizar_tableWidget_Automaticamente)

        self.tableWidget.setHorizontalHeaderLabels(
            ['id', 'nom_ape', 'num_doc', 'num_cuit', 'num_cel', 'direc', 'localidad', 'sexo'])
        for i in [0, 1, 2, 3, 4, 5, 6, 7]:
            self.tableWidget.resizeColumnToContents(i)
        self.pushButton_2.clicked.connect(self.cargarCliente)
        # cargarIdCliente

    def guardarModificacion(self):

        self.lineEdit_4.setText("")
        self.lineEdit_5.setText("")
        self.lineEdit_6.setText("")
        self.lineEdit_7.setText("")
        self.lineEdit_8.setText("")
        self.lineEdit_9.setText("")
        nombreApellidoNuevo = self.lineEdit_4.text()
        documentoNuevo = self.lineEdit_5.text()
        CuitNuevo = self.lineEdit_6.text()
        CelularNuevo = self.lineEdit_7.text()
        DireccionNueva = self.lineEdit_8.text()
        LocalidadNueva = self.lineEdit_9.text()
        sexoIndice = self.sexo.currentText()
        idCliente = self.lineEdit_2.text()
        print(sexoIndice)
        if sexoIndice == 'FEMENINO':
            sexoNuevo = 'F'
        else:
            sexoNuevo = 'M'

        if (
                nombreApellidoNuevo.strip() == "" or documentoNuevo.strip() == "" or CuitNuevo.strip() == "" or CelularNuevo.strip() == "" or idCliente.strip() == ""):
            pass
        else:
            clienteModificado = [nombreApellidoNuevo, int(documentoNuevo), CuitNuevo, int(CelularNuevo), DireccionNueva,
                                 LocalidadNueva, sexoNuevo, int(idCliente)]
            conn = conexion()
            guardarClienteModificado(conn, clienteModificado)
            self.lineEdit_4.setText("")
            self.lineEdit_5.setText("")
            self.lineEdit_6.setText("")
            self.lineEdit_7.setText("")
            self.lineEdit_8.setText("")
            self.lineEdit_9.setText("")
            self.mostrartodo()

    def cargarCliente(self):  # hola

        idCliente = self.lineEdit_2.text().strip()
        if idCliente == "":
            pass
        else:
            resultado = buscarClienteSegunId(idCliente)
            if resultado == "NO":
                pass
            else:
                listaCliente = resultado.fetchall()
                self.lineEdit_4.setText(listaCliente[0][0])
                self.lineEdit_5.setText(str(listaCliente[0][1]))
                self.lineEdit_6.setText(listaCliente[0][2])
                self.lineEdit_7.setText(str(listaCliente[0][3]))
                self.lineEdit_8.setText(listaCliente[0][4])
                self.lineEdit_9.setText(listaCliente[0][5])
                if listaCliente[0][6] == 'F':
                    self.sexo.setCurrentIndex(1)
                else:
                    self.sexo.setCurrentIndex(0)

    def buscarCliente(self):
        nombreApellido = self.lineEdit.text()
        numCuit = self.lineEdit_3.text()
        print('nombre y apellido: ' + nombreApellido + '\nnumero de cuit: ' + numCuit)
        # dato = [nombreApellido, numCuit]
        dato = ['%' + nombreApellido + '%', '%' + numCuit + '%']
        # dato = ['%' + nombreApellido + '%']
        # if nombreApellido.strip()=='%' and numCuit.strip()==":
        if nombreApellido.strip() == '%' or numCuit.strip() == '%':
            print('falla')
        else:
            self.actualizar_tableWidget(dato)

    def mostrartodo(self):
        conn = conexion()
        print('mostrartodo')

        resultado = extraer_todo_base_cliente(conn)
        self.tableWidget.setColumnCount(8)
        print('222222222222222222222222')
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(resultado):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        for i in [0, 1, 2, 3, 4, 5, 6, 7]:
            self.tableWidget.resizeColumnToContents(i)
        conn.close()

    def cargarIdCliente(self):
        idCli = self.lineEdit_2.text()  # id de cliente
        conn = conexion()
        cursor = conn.cursor()
        numeroDeCuit = cursor.execute("select 'num_cuit' from Clientes where id_cliente==(?);", (idCli,)).fetchall()[0][
            0]  # str
        print(numeroDeCuit)
        print('----------s-s- CUIT  s-s-------------')
        conn = conexion()
        cursor = conn.cursor()
        trabajosDeCuit = cursor.execute('select * from Trabajos where num_cuit==(?);', (numeroDeCuit,)).fetchall()
        print('-=-=-=-=')
        print(trabajosDeCuit)
        print('-=-=-=-=')

        #############MOSTRAR TODOS LOS TRABAJOS DEL CLIENTE
        conn = conexion()
        print('mostrar trabajos del cliente cargado')

        # resultado = extraer_todo_base_cliente(conn)
        consulta = extraer_cuit_del_cliente(conn, idCli)
        print('-----------###------------')
        print('-----------###------------')
        print('-----------###------------')
        # print(resultado.fetchall()[0][0])
        cuitCliente = consulta.fetchall()[0][0]

        trabajosRealizados = trabajosRealizadosSegunCuit(conn, cuitCliente)
        print('-----------###------------')
        print('-----------###------------')
        print('-----------###------------')
        self.tableWidget_3.setColumnCount(8)

        self.tableWidget_3.setHorizontalHeaderLabels(
            ['id_trabajo', 'tipo_trab', 'factura', 'monto_trab', 'fecha_entreg', 'num_cuit', 'monto_pagado', 'saldo'])

        print('222222222222222222222222')
        self.tableWidget_3.setRowCount(0)
        for row_number, row_data in enumerate(trabajosRealizados):
            self.tableWidget_3.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_3.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        for i in [0, 1, 2, 3, 4, 5, 6, 7]:
            self.tableWidget_3.resizeColumnToContents(i)
        conn.close()

    def actualizar_tableWidget_Automaticamente(self):
        print('mama mia!')
        self.tableWidget.clear()

        nombreApellido = self.lineEdit.text().strip()
        numCuit = self.lineEdit_3.text().strip()

        print(numCuit)

        dato = ['%' + nombreApellido + '%', '%' + numCuit + '%']

        if dato[0] == '%%' and dato[1] == '%%':
            self.tableWidget.setHorizontalHeaderLabels(
                ['ID Cliente', 'Nombre y apellido', 'N° Documento', 'N° CUIT', 'N° CEL', 'Direccion', 'Localidad',
                 'Sexo'])
            # self.tableWidget.setCellWidget(0,0,self.tableWidget)
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setRowCount(0)

        elif dato[0] != '%%' and dato[1] != '%%':
            self.tableWidget.setColumnCount(8)

            conn = conexion()
            cursor = conn.cursor()
            cantidadDeFilas = cursor.execute('SELECT COUNT(ALL) from Clientes;').fetchall()[0]
            print(cantidadDeFilas)
            print(type(cantidadDeFilas))
            if type(cantidadDeFilas) == tuple:
                cantidadDeFilas = cantidadDeFilas[0]
                self.tableWidget.setRowCount(cantidadDeFilas)
            else:
                self.tableWidget.setRowCount(cantidadDeFilas)

            # conn = conexion()
            # cursor = conn.cursor()
            # cantidadDeFilas2 = cursor.execute('SELECT COUNT(ALL) from Clientes;').fetchall()[0]
            # self.tableWidget.setRowCount(cantidadDeFilas)

            self.tableWidget.setHorizontalHeaderLabels(
                ['ID Cliente', 'Nombre y apellido', 'N° Documento', 'N° CUIT', 'N° CEL', 'Direccion', 'Localidad',
                 'Sexo'])
            print(dato)
            resultado = extraer_base_cliente_nomape_numcuit(dato)
            for row_number, row_data in enumerate(resultado):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
            for i in [0, 1, 2, 3, 4, 5, 6, 7]:
                self.tableWidget.resizeColumnToContents(i)

        elif dato[0] != '%%':
            self.tableWidget.setColumnCount(8)

            conn = conexion()
            cursor = conn.cursor()
            cantidadDeFilas = list(cursor.execute('SELECT COUNT(ALL) from Clientes;').fetchall()[0])[0]
            print(cantidadDeFilas)
            print(type(cantidadDeFilas))
            self.tableWidget.setRowCount(cantidadDeFilas)

            self.tableWidget.setHorizontalHeaderLabels(
                ['ID Cliente', 'Nombre y apellido', 'N° Documento', 'N° CUIT', 'N° CEL', 'Direccion', 'Localidad',
                 'Sexo'])
            print(dato[0])
            resultado = extraer_base_cliente_nomape(dato[0])
            for row_number, row_data in enumerate(resultado):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
            for i in [0, 1, 2, 3, 4, 5, 6, 7]:
                self.tableWidget.resizeColumnToContents(i)
        elif dato[1] != '%%':
            self.tableWidget.setHorizontalHeaderLabels(
                ['ID Cliente', 'Nombre y apellido', 'N° Documento', 'N° CUIT', 'N° CEL', 'Direccion', 'Localidad',
                 'Sexo'])
            self.tableWidget.setColumnCount(8)

            conn = conexion()
            cursor = conn.cursor()
            cantidadDeFilas = list(cursor.execute('SELECT COUNT(ALL) from Clientes;').fetchall()[0])[0]
            self.tableWidget.setRowCount(cantidadDeFilas)

            print(dato[1])
            resultado = extraer_base_cliente_numcuit(dato[1])
            for row_number, row_data in enumerate(resultado):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
            for i in [0, 1, 2, 3, 4, 5, 6, 7]:
                self.tableWidget.resizeColumnToContents(i)

    def actualizar_tableWidget(dato):  # dato = ['%' + nombreApellido + '%','%' + numCuit + '%']
        if dato[0] != '' and dato[1] != '':
            resultado = extraer_base_cliente_nomape_numcuit(dato)
        elif dato[0] != '' and dato[1] == '':
            resultado = extraer_base_cliente_nomape(dato)
        elif dato[0] == '' and dato[1] != '':
            resultado = extraer_base_cliente_numcuit(dato)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(resultado):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        for i in [0, 1, 2, 3, 4, 5, 6, 7]:
            self.tableWidget.resizeColumnToContents(i)
        print(resultado.fetchall())

    def trabajoRealizados(self):
        print('trabajoRealizados')

    def cuenta(self):
        print('cuenta')

    def pagarUnTrabajo(self):
        print('pagarUnTrabajo')
        idTrabajo = self.lineEdit_10.text()
        monto = self.lineEdit_11.text()
        pagarUnMonto(idTrabajo, monto)

        conn = conexion()
        # print('mostrar trabajos del cliente cargado')

        # resultado = extraer_todo_base_cliente(conn)
        # consulta = extraer_cuit_del_cliente(conn, idCli)
        # print('-----------###------------')
        # print('-----------###------------')
        # print('-----------###------------')
        # print(resultado.fetchall()[0][0])
        # cuitCliente = consulta.fetchall()[0][0]

        cuitCliente = cauitSegunIdTrabajo(conn, idTrabajo)

        trabajosRealizados = trabajosRealizadosSegunCuit(conn, cuitCliente)
        print('-----------###------------')
        print('-----------###------------')
        print('-----------###------------')
        self.tableWidget_3.setColumnCount(8)

        self.tableWidget_3.setHorizontalHeaderLabels(
            ['id_trabajo', 'tipo_trab', 'factura', 'monto_trab', 'fecha_entreg', 'num_cuit', 'monto_pagado', 'saldo'])
        self.tableWidget_3.setRowCount(0)

        for row_number, row_data in enumerate(trabajosRealizados):
            self.tableWidget_3.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_3.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        for i in [0, 1, 2, 3, 4, 5, 6, 7]:
            self.tableWidget_3.resizeColumnToContents(i)
        conn.close()


###############################################################

class WindowGanan(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ganancias.ui', self)
        self.setWindowTitle('Ganancias')
        # self.dateEdit.setDisplayFormat("dd.MM.yyyy")
        # self.dateEdit.dateChanged.connect(self.printttt)
        self.pushButton.clicked.connect(self.reporte)

    def reporte(self):
        print('generar reporte')

        dia = self.dateEdit.date().day()
        mes = self.dateEdit.date().month()
        anio = self.dateEdit.date().year()
        print(dia, mes, anio)
        fechaNueva1 = str(dia) + '/' + str(mes) + '/' + str(anio)

        dia = self.dateEdit_2.date().day()
        mes = self.dateEdit_2.date().month()
        anio = self.dateEdit_2.date().year()
        print(dia, mes, anio)
        fechaNueva2 = str(dia) + '/' + str(mes) + '/' + str(anio)

        print(fechaNueva1<fechaNueva2)

        conn=conexion()

        #sumar todos los montosPagados
        ingresoBruto=calcularIngresoBruto(conn,fechaNueva1,fechaNueva2)

    def printttt(self):
        # print('qweqweqwe')
        # fecha=self.dateEdit.date()
        # fecha = self.dateEdit.displayFormat()
        dia = self.dateEdit.date().day()
        mes = self.dateEdit.date().month()
        anio = self.dateEdit.date().year()
        print(dia, mes, anio)
        print(type(dia))

        # print(fecha)


class WindowInsu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('insumos.ui', self)
        self.setWindowTitle('Insumos')
        self.btnRegistrar.clicked.connect(self.registrarInsumo)

        def registrarInsumo(self):
            descripcion = self.nombap.text()
            marca = self.nombap_2.text()
            cantidad = self.nombap_3.text()
            precioUnitario = self.nombap_4.text()
            fechaCompra = self.nombap_5.text()

            dato = [descripcion, marca, cantidad, precioUnitario, fechaCompra]
            respuesta = insertar_base_insumo(dato)
            self.nombap.setText("")
            self.nombap_2.setText("")
            self.nomba


class WindowAlerta(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('alerta.ui', self)
        self.setWindowTitle('ERROR')


class WindowClienteGuardado(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui_clienteGuardado.ui', self)
        self.setWindowTitle('cliente guardado')


class WindowTrabajoGuardado(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui_trabajoGuardado.ui', self)
        self.setWindowTitle('trabajo guardado')


class WindowAlertaClienteNoRegistrado(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui_noHayClienteRegistrado.ui', self)
        self.setWindowTitle('trabajo guardado')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # basededatos
    db_cliente()
    db_trabajo()
    gui = MainWindow()
    gui.setWindowTitle('Software para consultor en TI')
    guiRegistro = WindowRegistro()
    guiCargar = WindowCargar()
    guiBuscar = WindowBuscar()
    guiGanan = WindowGanan()
    guiInsu = WindowInsu()
    guiAlerta = WindowAlerta()
    gui_noHayClienteRegistrado = WindowAlertaClienteNoRegistrado()
    guiClienteGuardado = WindowClienteGuardado()
    guiTrabajoGuardado = WindowTrabajoGuardado()
    gui.show()
    sys.exit(app.exec_())
