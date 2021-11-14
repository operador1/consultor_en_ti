import sys
from PyQt5 import uic, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
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
        self.btnRegistrar.clicked.connect(self.ingresarCliente)

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
        insertar_base_cliente(dato)
        self.nombap.setText("")
        self.numdoc.setText("")
        self.numcuit.setText("")
        self.numcel.setText("")
        self.direc.setText("")
        self.loc.setText("")
        self.sexo.setCurrentIndex(0)
        guiClienteGuardado.show()


class WindowCargar(QMainWindow):  # registrar trabajo
    def __init__(self):
        super().__init__()
        uic.loadUi('registrar_trabajo.ui', self)
        self.setWindowTitle('Registrar un nuevo trabajo')
        self.btnRegistrar.clicked.connect(self.ingresarTrabajo)
        self.tipotrab.setText("")
        self.comboBox.setCurrentIndex(0)
        self.montotrab.setText("")
        self.fechaentreg.setText("")
        self.cuitsolici.setText("")

    def ingresarTrabajo(self):
        tipo = self.tipotrab.text()
        factura = self.comboBox.currentText()
        monto = self.montotrab.text()
        fecha = self.fechaentreg.text()
        cuit = self.cuitsolici.text()
        dato = [tipo, factura, monto, fecha, cuit]
        insertar_base_trabajo(dato)
        guiTrabajoGuardado.show()
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
        self.btnBuscar.clicked.connect(self.buscarCliente)

        self.pushButton.clicked.connect(self.mostrartodo)
        # self.pushButton_2.clicked.connect(self.cargarIdCliente)
        # self.btnPagar.clicked.connect(self.pagarUnTrabajo)
        # self.tableWidgwt.horizontalHeaderItem(8)
        # self.tableWidget.setItem(rowPosition= 0, uic.QTableWidgetItem("text1"))
        self.tableWidget.setColumnCount(8)
        self.pushButton_3.clicked.connect(self.guardarModificacion)

        self.lineEdit.cursorPositionChanged.connect(self.actualizar_tableWidget_Automaticamente)
        self.lineEdit_3.cursorPositionChanged.connect(self.actualizar_tableWidget_Automaticamente)

        self.tableWidget.setHorizontalHeaderLabels(
            ['id', 'nom_ape', 'num_doc', 'num_cuit', 'num_cel', 'direc', 'localidad', 'sexo'])
        for i in [0, 1, 2, 3, 4, 5, 6, 7]:
            self.tableWidget.resizeColumnToContents(i)
        self.pushButton_2.clicked.connect(self.cargarCliente)

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

    def cargarCliente(self): #hola

        idCliente = self.lineEdit_2.text().strip()
        if idCliente == "":
            pass
        else:
            conn = conexion()
            resultado = buscarClienteSegunId(conn, idCliente)
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
        print('mostrartodo')
        resultado = extraer_todo_base_cliente()
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(resultado):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        for i in [0, 1, 2, 3, 4, 5, 6, 7]:
            self.tableWidget.resizeColumnToContents(i)

    def cargarIdcliente(self):
        idCli = self.lineEdit_2.text()
        print('id de Cliente: ' + idCli)

    def actualizar_tableWidget_Automaticamente(self):
        print('mama mia!')
        self.tableWidget.clear()

        nombreApellido = self.lineEdit.text().strip()
        numCuit = self.lineEdit_3.text().strip()

        print(numCuit)

        dato = ['%' + nombreApellido + '%', '%' + numCuit + '%']

        if dato[0] == '%%' and dato[1] == '%%':
            self.tableWidget.setHorizontalHeaderLabels(['ID Cliente', 'Nombre y apellido', 'N° Documento', 'N° CUIT', 'N° CEL', 'Direccion', 'Localidad', 'Sexo'])
            # self.tableWidget.setCellWidget(0,0,self.tableWidget)
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setRowCount(0)
        elif dato[0] != '%%' and dato[1] != '%%':
            self.tableWidget.setColumnCount(8)
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


class WindowGanan(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ganancias.ui', self)
        self.setWindowTitle('Ganancias')


class WindowInsu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('insumos.ui', self)
        self.setWindowTitle('Insumos')


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
    guiClienteGuardado = WindowClienteGuardado()
    guiTrabajoGuardado = WindowTrabajoGuardado()
    gui.show()
    sys.exit(app.exec_())
