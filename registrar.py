import mysql.connector
from kivy.uix.screenmanager import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel

class RegisterTab(Screen):
    def _init_(self, **kwargs):
        super()._init_(**kwargs)

        # Conectar ao banco de dados MySQL
        self.mydb = mysql.connector.connect(
            host="127.0.0.1:3306",
            user="root",
            password="ellieborin@123",
            database="gpjunina"
        )
        self.mycursor = self.mydb.cursor()

        # Resto do código permanece igual

    def register(self, instance):
        # Obter os valores dos campos de entrada
        codigo_adm = self.admin_code.text
        nome = self.name_field.text
        email = self.email.text
        senha = self.password_register.text
        confirmar_senha = self.confirm_password.text

        # Verificar se as senhas coincidem
        if senha != confirmar_senha:
            print("As senhas não coincidem")
            return

        # Inserir os dados no banco de dados
        sql = "INSERT INTO usuarios (codigo_adm, nome, email, senha) VALUES (%s, %s, %s, %s)"
        val = (codigo_adm, nome, email, senha)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

        print("Usuário registrado com sucesso")

        # Limpar os campos após o registro
        self.admin_code.text = ""
        self.name_field.text = ""
        self.email.text = ""
        self.password_register.text = ""
        self.confirm_password.text = ""

    # Resto do código permanece igual