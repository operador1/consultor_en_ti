import sys
from PyQt5 import uic, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QDateEdit, QFrame, QComboBox
from base import *
import logo


# import time

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
        guiRegistro.showMaximized()

    def ventanaCargar(self):
        guiCargar.show()

    def ventanaBuscar(self):
        guiBuscar.showMaximized()

    def ventanaGanan(self):
        guiGanan.showMaximized()

    def ventanaInsu(self):
        guiInsu.showMaximized()


class WindowRegistro(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('registrar_cliente.ui', self)
        self.setWindowTitle('Registrar un nuevo cliente')
        self.btnRegistrar22.clicked.connect(self.ingresarCliente)

    def ingresarCliente(self):
        nombre = self.nombap.text()
        # documento = self.numdoc.text()
        cuit = self.numcuit.text()
        documento = cuit[3:-2]
        celular = self.numcel.text()
        direccion = self.direc.text()
        localidad = self.loc.text()
        sexo = self.sexo.currentText()
        if (
                nombre == '' or len(cuit) != 13 or celular == '' or direccion == '' or localidad == '' or sexo == ''):
            pass
        else:
            borrar = 'no'
            dato = [nombre, documento, cuit, celular, direccion, localidad, sexo, borrar]
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


class WindowCargar(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('registrar_trabajo.ui', self)
        self.setWindowTitle('Registrar un nuevo trabajo')
        self.btnRegistrar.clicked.connect(self.ingresarTrabajo)
        self.tipotrab.setText("")
        self.comboBox.setCurrentIndex(0)
        self.montotrab.setText("")
        self.pushButton.clicked.connect(self.llenarComboBox)
        # conn = conexion()
        # cursor = conn.cursor()
        # listaDeCuitNombre = cursor.execute('select num_cuit,nom_ape from Clientes').fetchall()
        # lista1 = []
        # for i in listaDeCuitNombre:
        #     lista1.append(i[0] + ' - ' + i[1])
        #     self.comboBox_2.addItem(i[0] + ' - ' + i[1])
        # conn.close()

        # self.comboBox_2.currentIndexChanged.connect(self.borrar)
        # self.comboBox_2.highlighted.connect(self.borrar)
        # self.comboBox_2.activated.connect(self.borrar)
        # self.comboBox_2.activated.connect(self.borrar)
        # self.comboBox_2.currentIndexChanged.connect(self.borrar)
        # self.comboBox_2.currentIndexChanged.connect(self.borrar)
        # self.comboBox_2.currentTextChanged.connect(self.borrar)
        # self.comboBox_2.editTextChanged.connect(self.borrar)
        # self.comboBox_2.highlighted.connect(self.borrar)
        # self.comboBox_2.highlighted.connect(self.borrar)
        # self.comboBox_2.textActivated.connect(self.borrar)
        # self.comboBox_2.textHighlighted.connect(self.borrar)

    def borrar(self):
        print('HOLA MUNDO!')

    def llenarComboBox(self):
        # self.comboBox_2.addItem('')
        self.comboBox_2.clear()

        # self.comboBox_2.removeItem(20)
        conn = conexion()
        cursor = conn.cursor()
        listaDeCuitNombre = cursor.execute("select num_cuit,nom_ape from Clientes where borrar='no'").fetchall()
        lista1 = []
        for i in listaDeCuitNombre:
            lista1.append(i[0] + ' - ' + i[1])
            self.comboBox_2.addItem(i[0] + ' - ' + i[1])
        conn.close()

    def ingresarTrabajo(self):
        tipo = self.tipotrab.text().strip()
        factura = self.comboBox.currentText().strip()
        monto = self.montotrab.text().strip()
        dia = self.dateEdit.date().day()
        mes = self.dateEdit.date().month()
        anio = self.dateEdit.date().year()
        fechaNueva = str(dia) + '/' + str(mes) + '/' + str(anio)
        cuitsolici = self.comboBox_2.currentText()[0:13]
        if (tipo == '' or monto.replace('$', '') == ''):
            pass
        else:
            dato = [tipo, factura, monto, fechaNueva, cuitsolici]
            respuesta = existeCuitParaTrabajo(dato)
            if respuesta == 'existe':
                guardoTrabajoSegunCuit2(dato)
                guiTrabajoGuardado.show()
                self.tipotrab.setText("")
                self.comboBox.setCurrentIndex(0)
                self.montotrab.setText("")
            elif respuesta == 'no existe':
                gui_noHayClienteRegistrado.show()
                self.tipotrab.setText("")
                self.comboBox.setCurrentIndex(0)
                self.montotrab.setText("")


class WindowBuscar(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('buscar_cliente.ui', self)
        self.setWindowTitle('Buscar un cliente')
        self.pushButton.clicked.connect(self.mostrartodo)
        self.pushButton_2.clicked.connect(self.cargarIdCliente)
        self.pushButton_6.clicked.connect(self.cargarIdCliente)

        ####Borrar cliente - conectar boton
        self.pushButton_2.clicked.connect(self.cargarClienteParaBorrar)
        self.pushButton_6.clicked.connect(self.borrarCliente)

        self.tableWidget.setColumnCount(7)
        self.pushButton_3.clicked.connect(self.guardarModificacion)
        self.comboBox.currentTextChanged.connect(self.seleccionarCuit)
        self.pushButton_5.clicked.connect(self.actualizarTabla)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Cuit", "Documento", "Nombre y apellido", "Celular", "Direccion", "Localidad", "Sexo"])
        for i in [0, 1, 2, 3, 4, 5, 6, 7]:
            self.tableWidget.resizeColumnToContents(i)
        self.pushButton_2.clicked.connect(self.cargarCliente)

    def cargarClienteParaBorrar(self):
        nombreCliente = self.comboBox.currentText()[15:]
        print('nombreCliente')
        print(nombreCliente)
        cuit = self.comboBox.currentText()[13:]
        print('cuit')
        print(cuit)
        self.label_2.setText('Desea borrar al cliente %s' % nombreCliente)
        self.label_2.adjustSize()  # ajustar tamaño a texto

    def borrarCliente(self):
        try:

            nombreCliente = self.comboBox.currentText()[15:]
            # print('nombreCliente')
            # print(nombreCliente)
            cuit = self.comboBox.currentText()[0:13]
            # print('cuit')
            # print(cuit)
            conn = conexion()
            cursor = conn.cursor()
            # borrar = 'si'
            cursor.execute("update Clientes set borrar='si' where num_cuit=?;", (cuit,))
            conn.commit()
            print('logrado')
            conn.close()
        except Error:
            print('ups!')
        # self.label_2.setText('Desea borrar al cliente %s' % nombreCliente)
        # self.label_2.adjustSize()  # ajustar tamaño a texto

    def seleccionarCuit(self):
        pass

    def actualizarTabla(self):
        self.tableWidget.setRowCount(0)
        nomApe = self.lineEdit.text().strip()
        cuit = self.lineEdit_3.text().strip()
        conn = conexion()
        datoNombre = '%' + nomApe + '%'
        datoCuit = '%' + cuit + '%'
        dato = [datoNombre, datoCuit]
        cursor = conn.cursor()

        if nomApe != '' and cuit != '':  # primer EVENTO
            resultado = cursor.execute(
                "SELECT num_cuit,num_doc,nom_ape,num_cel,direc,localidad,sexo FROM Clientes WHERE nom_ape like ? AND num_cuit like ? and borrar='no';",
                dato)
            for row_number, row_data in enumerate(resultado):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
            for i in [0, 1, 2, 3, 4, 5, 6]:
                self.tableWidget.resizeColumnToContents(i)
            # cantidadFilas = cursor.execute(
            #     "SELECT num_cuit,num_doc,nom_ape,num_cel,direc,localidad,sexo FROM Clientes WHERE nom_ape like ? AND num_cuit like ?;",
            #     dato).fetchall()
            cantidadFilas = cursor.execute(
                "SELECT num_cuit,nom_ape FROM Clientes WHERE nom_ape like ? AND num_cuit like ? and borrar='no';",
                dato).fetchall()
            # self.tableWidget.setRowCount(len(cantidadFilas))
            self.llenarComboBox(cantidadFilas=cantidadFilas)

        elif nomApe != '' and cuit == '':
            resultado = cursor.execute(
                "SELECT num_cuit,num_doc,nom_ape,num_cel,direc,localidad,sexo FROM Clientes WHERE nom_ape like ? and borrar='no';",
                (datoNombre,))
            for row_number, row_data in enumerate(resultado):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
            for i in [0, 1, 2, 3, 4, 5, 6]:
                self.tableWidget.resizeColumnToContents(i)
            cantidadFilas = cursor.execute(
                "SELECT num_cuit,nom_ape FROM Clientes WHERE nom_ape like ? and borrar='no';",
                (datoNombre,)).fetchall()
            # self.tableWidget.setRowCount(len(cantidadFilas))
            self.llenarComboBox(cantidadFilas=cantidadFilas)
        elif nomApe == '' and cuit != '':
            resultado = cursor.execute(
                "SELECT num_cuit,num_doc,nom_ape,num_cel,direc,localidad,sexo FROM Clientes WHERE num_cuit like ? and borrar='no';",
                (datoCuit,))
            for row_number, row_data in enumerate(resultado):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
            for i in [0, 1, 2, 3, 4, 5, 6]:
                self.tableWidget.resizeColumnToContents(i)
            cantidadFilas = cursor.execute(
                "SELECT num_cuit,nom_ape FROM Clientes WHERE num_cuit like ? and borrar='no';",
                (datoCuit,)).fetchall()
            # self.tableWidget.setRowCount(len(cantidadFilas))
            self.llenarComboBox(cantidadFilas=cantidadFilas)
        if nomApe == '' and cuit == '':
            conn.close()

    def llenarComboBox(self, cantidadFilas):
        self.comboBox.clear()
        self.tableWidget.setRowCount(len(cantidadFilas))
        for i in cantidadFilas:
            print(cantidadFilas)
            # self.comboBox.clear()
            self.comboBox.addItem(i[0] + ' - ' + i[1])

    def guardarModificacion(self):
        nombreApellidoNuevo = self.lineEdit_4.text()  ##
        documentoNuevo = self.lineEdit_5.text()  ##
        CuitNuevo = self.lineEdit_6.text()  ##
        CelularNuevo = self.lineEdit_7.text()  ##
        DireccionNueva = self.lineEdit_8.text()  ##
        LocalidadNueva = self.lineEdit_9.text()  ##
        sexoIndice = self.sexo.currentText()  ##
        cuit = self.comboBox.currentText()
        conn = conexion()
        cursor = conn.cursor()
        idCliente = \
            cursor.execute('select id_cliente from Clientes where num_cuit=(?) and borrar="no";',
                           (cuit[0:13],)).fetchall()[0][0]
        if (
                nombreApellidoNuevo.strip() == "" or documentoNuevo.strip() == "" or CuitNuevo.strip() == ""):
            pass
        else:
            clienteModificado = [nombreApellidoNuevo, int(documentoNuevo), CuitNuevo, int(CelularNuevo),
                                 DireccionNueva,
                                 LocalidadNueva, sexoIndice, int(idCliente)]
            conn = conexion()
            guardarClienteModificado(conn, clienteModificado)
            conn.close()
            self.lineEdit_4.setText("")
            self.lineEdit_5.setText("")
            self.lineEdit_6.setText("")
            self.lineEdit_7.setText("")
            self.lineEdit_8.setText("")
            self.lineEdit_9.setText("")
            self.mostrartodo()

    def cargarCliente(self):  # hola
        cuit = self.comboBox.currentText()
        if cuit == '':
            pass
        else:
            conn = conexion()
            cursor = conn.cursor()
            idCliente = \
                cursor.execute('select id_cliente from Clientes where num_cuit=(?) and borrar="no";', (cuit[0:13],)).fetchall()[0][
                    0]
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
        dato = ['%' + nombreApellido + '%', '%' + numCuit + '%']
        if nombreApellido.strip() == '%' or numCuit.strip() == '%':
            pass
        else:
            self.actualizar_tableWidget(dato)

    def mostrartodo(self):
        conn = conexion()
        resultado = extraer_todo_base_cliente(conn)
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Cuit", "Documento", "Nombre y apellido", "Celular", "Direccion", "Localidad", "Sexo"])
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(resultado):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        for i in [0, 1, 2, 3, 4, 5, 6, 7]:
            self.tableWidget.resizeColumnToContents(i)
        conn = conexion()
        cursor = conn.cursor()
        cantidadFilas = cursor.execute('select num_cuit,nom_ape from Clientes where borrar="no"').fetchall()
        self.llenarComboBox(cantidadFilas=cantidadFilas)
        conn.close()

    def cargarIdCliente(self):
        cuitNombre = self.comboBox.currentText()
        conn = conexion()  # -------------- < - > --------------
        numeroDeCuit = cuitNombre[0:13]
        cursor = conn.cursor()
        trabajosSegunCuit = cursor.execute(
            'select id_trabajo, tipo_trab,factura,monto_trab,fecha_entreg,num_cuit,monto_pagado,saldo from Trabajos where num_cuit=(?);',
            (numeroDeCuit,))
        self.tableWidget_3.setColumnCount(8)
        self.tableWidget_3.setHorizontalHeaderLabels(
            ['id_trabajo', 'tipo_trab', 'factura', 'monto_trab', 'fecha_entreg', 'num_cuit', 'monto_pagado',
             'saldo'])
        self.tableWidget_3.setRowCount(0)
        for row_number, row_data in enumerate(trabajosSegunCuit):
            self.tableWidget_3.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_3.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        for i in [0, 1, 2, 3, 4, 5, 6, 7]:
            self.tableWidget_3.resizeColumnToContents(i)
        conn.close()


class WindowGanan(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ganancias.ui', self)
        self.label_7.setText('')
        self.setWindowTitle('Ganancias')
        self.pushButton.clicked.connect(self.reporte)

    def reporte(self):
        conn = conexion()
        ingresoBruto = calcularIngresoBruto(conn)
        listaNueva = []
        for i in ingresoBruto:
            if i[0] == None:
                pass
            else:
                listaNueva.append(i[0])
        total = 0
        for i in listaNueva:
            total = total + float(i[0])
        self.label_7.setText(str(total))
        listaInsumos = extraerListaInsumos(conn)
        totalInsumos = 0
        for i in listaInsumos:
            totalInsumos = totalInsumos + float(i[0])
        self.label_8.setText(str(totalInsumos))
        ingresoNeto = total - totalInsumos
        self.label_9.setText(str(ingresoNeto))

    def printttt(self):
        dia = self.dateEdit.date().day()
        mes = self.dateEdit.date().month()
        anio = self.dateEdit.date().year()


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
        if (descripcion == '' or marca == '' or cantidad == '' or precioUnitario == '' or fechaCompra == ''):
            pass
        else:
            total = int(cantidad) * float(precioUnitario.replace('$', ''))
            dato = [descripcion, marca, cantidad, precioUnitario, fechaCompra, str(total)]
            insertar_base_insumo(dato)
            self.nombap.setText("")
            self.nombap_2.setText("")
            self.nombap_3.setText("")
            self.nombap_4.setText("")
            self.nombap_5.setText("")


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

    # class WindowBorrarCliente(QMainWindow):
    #     def __init__(self):
    #         super().__init__()
    #         uic.loadUi('borrarCliente.ui', self)
    #         self.pushButton.clicked.connect(self.borrarCliente)
    #
    #     def borrarCliente(self):
    #         print('borrar cliente!!!')

    def actualizar_tableWidget(dato):
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

    def pagarUnTrabajo(self):
        idTrabajo = self.lineEdit_10.text()
        monto = self.lineEdit_11.text()
        pagarUnMonto(idTrabajo, monto)
        conn = conexion()
        cuitCliente = cauitSegunIdTrabajo(conn, idTrabajo)
        trabajosRealizados = trabajosRealizadosSegunCuit(conn, cuitCliente)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # basededatos
    db_cliente()
    db_trabajo()
    db_insumos()
    gui = MainWindow()
    gui.setWindowTitle('Software para consultor en TI')
    guiRegistro = WindowRegistro()
    guiCargar = WindowCargar()
    guiBuscar = WindowBuscar()
    guiGanan = WindowGanan()
    guiInsu = WindowInsu()
    guiAlerta = WindowAlerta()
    # borrarCliente = WindowBorrarCliente()
    gui_noHayClienteRegistrado = WindowAlertaClienteNoRegistrado()
    guiClienteGuardado = WindowClienteGuardado()
    guiTrabajoGuardado = WindowTrabajoGuardado()
    gui.show()
    sys.exit(app.exec_())
