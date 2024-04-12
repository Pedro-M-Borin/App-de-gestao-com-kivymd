import mysql.connector
from kivy.uix.screenmanager import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog

class RegisterTab(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Conectar ao banco de dados MySQL
        self.mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="ellieborin@123",
            database="gpjunina"
        )
        self.mycursor = self.mydb.cursor()

        self.title_label = MDLabel(
            text="Registrar-se",
            halign="center",
            pos_hint={'center_x': 0.5, 'top': 0.8},
            size_hint_y=None,
            height=50,
            font_style='H5'
        )

        self.admin_code = MDTextField(
            hint_text="Código de Administrador",
            pos_hint={'center_x': 0.5, 'center_y': 0.8},
            size_hint=(0.7, None),
            width=200,
            required=True,
        )

        self.name_field = MDTextField(
            hint_text="Nome",
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            size_hint=(0.7, None),
            width=200,
            required=True,
        )

        self.email = MDTextField(
            hint_text="E-mail",
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            size_hint=(0.7, None),
            width=200,
            required=True,
        )

        self.password_register = MDTextField(
            hint_text="Senha",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.7, None),
            width=200,
            required=True,
            password=True,
        )

        # Botão para mostrar/esconder a senha
        self.show_password_button = MDIconButton(
            icon="eye-off",
            pos_hint={'center_x': 0.85, 'center_y': 0.5},
            on_release=self.toggle_password_visibility
        )

        # Ícone de olho para confirmar senha
        self.show_confirm_password_button = MDIconButton(
            icon="eye-off",
            pos_hint={'center_x': 0.85, 'center_y': 0.4},
            on_release=self.toggle_confirm_password_visibility
        )

        self.confirm_password = MDTextField(
            hint_text="Confirmar Senha",
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            size_hint=(0.7, None),
            width=200,
            required=True,
            password=True,
        )

        self.register_button = MDRaisedButton(
            text="Cadastrar",
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            size_hint=(0.7, None),
            width=200,
            on_press=self.register
        )

        self.return_to_login_button = MDFlatButton(
            text="Retornar ao Login",
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            size_hint=(0.7, None),
            width=200,
            on_press=self.switch_to_login_screen
        )

        self.add_widget(self.admin_code)
        self.add_widget(self.name_field)
        self.add_widget(self.email)
        self.add_widget(self.password_register)
        self.add_widget(self.show_password_button)  # Adicionando botão para mostrar senha
        self.add_widget(self.show_confirm_password_button)  # Adicionando botão para mostrar senha de confirmação
        self.add_widget(self.confirm_password)
        self.add_widget(self.register_button)
        self.add_widget(self.return_to_login_button)

    def toggle_password_visibility(self, instance):
        # Alterna a visibilidade da senha
        if self.password_register.password:
            self.password_register.password = False
            self.show_password_button.icon = "eye"
        else:
            self.password_register.password = True
            self.show_password_button.icon = "eye-off"

    def toggle_confirm_password_visibility(self, instance):
        # Alterna a visibilidade da senha de confirmação
        if self.confirm_password.password:
            self.confirm_password.password = False
            self.show_confirm_password_button.icon = "eye"
        else:
            self.confirm_password.password = True
            self.show_confirm_password_button.icon = "eye-off"

    def register(self, instance):
        # Obter o código de administrador
        codigo_adm = self.admin_code.text

        # Verificar se todos os campos foram preenchidos
        if not codigo_adm or not self.name_field.text or not self.email.text or not self.password_register.text or not self.confirm_password.text:
            # Exibir mensagem de erro
            dialog = MDDialog(
                text="Por favor, preencha todos os campos!",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda x: dialog.dismiss()
                    )
                ]
            )
            dialog.open()
            return

        # Verificar se o código de administrador é válido
        if codigo_adm != "$#admingpjunina#$":
            # Exibir mensagem de erro
            dialog = MDDialog(
                text="Código de administrador inválido",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda x: dialog.dismiss()
                    )
                ]
            )
            dialog.open()
            return

        # Se o código de administrador for válido e todos os campos estiverem preenchidos, continuar com o registro
        nome = self.name_field.text
        email = self.email.text
        senha = self.password_register.text
        confirmar_senha = self.confirm_password.text

        # Verificar se as senhas coincidem
        if senha != confirmar_senha:
            # Exibir mensagem de erro
            dialog = MDDialog(
                text="As senhas não coincidem. Por favor, tente novamente.",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda x: dialog.dismiss()
                    )
                ]
            )
            dialog.open()
            return

        try:
            # Inserir os dados na tabela administradores
            sql = "INSERT INTO administradores (codigo_adm, nome, email, senha) VALUES (%s, %s, %s, %s)"
            val = (codigo_adm, nome, email, senha)
            self.mycursor.execute(sql, val)
            self.mydb.commit()

            # Exibir mensagem de sucesso
            dialog = MDDialog(
                text="Usuário cadastrado com sucesso!",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda x: dialog.dismiss()
                    )
                ]
            )
            dialog.open()

            # Limpar os campos após o registro
            self.admin_code.text = ""
            self.name_field.text = ""
            self.email.text = ""
            self.password_register.text = ""
            self.confirm_password.text = ""

        except mysql.connector.Error as e:
            print("Erro ao registrar usuário:", e)

    def switch_to_login_screen(self, instance):
        self.manager.current = 'login'
