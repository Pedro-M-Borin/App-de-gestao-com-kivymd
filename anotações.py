 import sys
from PyQt5.QtWidgets import QInputDialog ,QApplication, QMainWindow, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QTableWidget, QDialog, QMessageBox
from PyQt5.QtCore import Qt
import mysql.connector
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Farfala DeskNote 1.3")
        self.setGeometry(500, 300, 830, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        self.init_ui()

    def init_ui(self):
      

        # Botão de adicionar
        self.add_button = QPushButton('Adicionar Pedido', self)
        self.add_button.clicked.connect(self.add_pedido)
        self.layout.addWidget(self.add_button)

        # Botão de editar
        self.edit_button = QPushButton('Editar Pedido', self)
        self.edit_button.clicked.connect(self.edit_pedido)
        self.layout.addWidget(self.edit_button)

        # Botão de excluir
        self.delete_button = QPushButton('Excluir Pedido', self)
        self.delete_button.clicked.connect(self.delete_pedido)
        self.layout.addWidget(self.delete_button)

        # Conectar ao banco de dados
        self.db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="ellieborin@123",
            database="farfala"
        )

        self.update_table()

    def update_table(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM pedidos")
        rows = cursor.fetchall()

        self.table_widget.setRowCount(len(rows))
        self.table_widget.setColumnCount(8)
        self.table_widget.setHorizontalHeaderLabels(['ID', 'Data Acesso', 'Hora Acesso', 'Atendente', 'Cliente', 'Mesa', 'Descrição Pedido', 'Status Pedido'])

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.table_widget.setItem(i, j, item)

    def add_pedido(self):
        dialog = AddPedidoDialog(self)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            data_acesso = datetime.now().date()
            hora_acesso = datetime.now().time()
            atendente = dialog.atendente_line.text()
            cliente = dialog.cliente_line.text()
            mesa = dialog.mesa_line.text()
            descricao_pedido = dialog.descricao_line.text()
            status_pedido = dialog.status_line.text()

            cursor = self.db.cursor()
            cursor.execute("INSERT INTO pedidos (data_acesso, hora_acesso, atendente, cliente, mesa, descricao_pedido, status_pedido) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (data_acesso, hora_acesso, atendente, cliente, mesa, descricao_pedido, status_pedido))
            self.db.commit()

            self.update_table()

    def edit_pedido(self):
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            # Recuperar dados da linha selecionada
            id_pedido = self.table_widget.item(selected_row, 0).text()
            atendente = self.table_widget.item(selected_row, 3).text()
            cliente = self.table_widget.item(selected_row, 4).text()
            mesa = self.table_widget.item(selected_row, 5).text()
            descricao_pedido = self.table_widget.item(selected_row, 6).text()
            status_pedido = self.table_widget.item(selected_row, 7).text()

            # Abrir o diálogo de edição
            dialog = EditPedidoDialog(self, id_pedido, atendente, cliente, mesa, descricao_pedido, status_pedido)
            result = dialog.exec_()

            if result == QDialog.Accepted:
                # Atualizar o registro no banco de dados
                new_data = {
                    'atendente': dialog.atendente_line.text(),
                    'cliente': dialog.cliente_line.text(),
                    'mesa': dialog.mesa_line.text(),
                    'descricao_pedido': dialog.descricao_line.text(),
                    'status_pedido': dialog.status_line.text(),
                }
                self.update_registro(id_pedido, new_data)
                self.update_table()

    def delete_pedido(self):
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            # Recuperar o ID do pedido da linha selecionada
            id_pedido = self.table_widget.item(selected_row, 0).text()

            senha, ok = QInputDialog.getText(self, 'Senha de Exclusão', 'Digite a senha para excluir o pedido:', QLineEdit.Password)
            
            if ok and senha == '12':  # Substitua 'sua_senha_correta' pela senha correta
                # Confirmar exclusão
                confirmar = QMessageBox.question(self, 'Confirmar Exclusão', f'Deseja excluir o pedido ID {id_pedido}?',
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                if confirmar == QMessageBox.Yes:
                    # Excluir o registro do banco de dados
                    self.delete_registro(id_pedido)
                    self.update_table()
            else:
                QMessageBox.warning(self, 'Senha Incorreta', 'Senha incorreta. A exclusão foi cancelada.', QMessageBox.Ok)

            

    def update_registro(self, id_pedido, new_data):
        # Implemente a lógica para atualizar o registro no banco de dados
        cursor = self.db.cursor()
        cursor.execute("UPDATE pedidos SET atendente=%s, cliente=%s, mesa=%s, descricao_pedido=%s, status_pedido=%s WHERE id=%s",
                       (new_data['atendente'], new_data['cliente'], new_data['mesa'], new_data['descricao_pedido'], new_data['status_pedido'], id_pedido))
        self.db.commit()

    def delete_registro(self, id_pedido):
        # Implemente a lógica para excluir o registro do banco de dados
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM pedidos WHERE id=%s", (id_pedido,))
        self.db.commit()


class AddPedidoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Adicionar Pedido")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QVBoxLayout(self)

        self.atendente_label = QLabel("Atendente:")
        self.atendente_line = QLineEdit(self)
        self.layout.addWidget(self.atendente_label)
        self.layout.addWidget(self.atendente_line)

        self.cliente_label = QLabel("Cliente:")
        self.cliente_line = QLineEdit(self)
        self.layout.addWidget(self.cliente_label)
        self.layout.addWidget(self.cliente_line)

        self.mesa_label = QLabel("Mesa:")
        self.mesa_line = QLineEdit(self)
        self.layout.addWidget(self.mesa_label)
        self.layout.addWidget(self.mesa_line)

        self.descricao_label = QLabel("Descrição Pedido:")
        self.descricao_line = QLineEdit(self)
        self.layout.addWidget(self.descricao_label)
        self.layout.addWidget(self.descricao_line)

        self.status_label = QLabel("Status Pedido:")
        self.status_line = QLineEdit(self)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.status_line)

        self.add_button = QPushButton('Adicionar', self)
        self.add_button.clicked.connect(self.accept)
        self.layout.addWidget(self.add_button)


class EditPedidoDialog(QDialog):
    def __init__(self, parent=None, id_pedido='', atendente='', cliente='', mesa='', descricao_pedido='', status_pedido=''):
        super().__init__(parent)

        self.setWindowTitle("Editar Pedido")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QVBoxLayout(self)

        self.atendente_label = QLabel("Atendente:")
        self.atendente_line = QLineEdit(atendente, self)
        self.layout.addWidget(self.atendente_label)
        self.layout.addWidget(self.atendente_line)

        self.cliente_label = QLabel("Cliente:")
        self.cliente_line = QLineEdit(cliente, self)
        self.layout.addWidget(self.cliente_label)
        self.layout.addWidget(self.cliente_line)

        self.mesa_label = QLabel("Mesa:")
        self.mesa_line = QLineEdit(mesa, self)
        self.layout.addWidget(self.mesa_label)
        self.layout.addWidget(self.mesa_line)

        self.descricao_label = QLabel("Descrição Pedido:")
        self.descricao_line = QLineEdit(descricao_pedido, self)
        self.layout.addWidget(self.descricao_label)
        self.layout.addWidget(self.descricao_line)

        self.status_label = QLabel("Status Pedido:")
        self.status_line = QLineEdit(status_pedido, self)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.status_line)

        self.edit_button = QPushButton('Salvar Edições', self)
        self.edit_button.clicked.connect(self.accept)
        self.layout.addWidget(self.edit_button)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
