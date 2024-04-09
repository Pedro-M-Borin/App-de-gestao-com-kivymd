from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from registrar import RegisterTab  # Importar a classe RegisterTab do arquivo registrar.py

class LoginApp(MDApp):
    def build(self):        
        self.screen_manager = ScreenManager()

        self.login_screen = Screen(name='login')
        self.register_screen = RegisterTab(name='register')  # Usar a classe RegisterTab

        self.title_label = MDLabel(
            text="Gestão Festa Junina 2024",
            halign="center",
            pos_hint={'center_x': 0.5, 'top': 0.8},
            size_hint_y=None,
            height=50,
            font_style='H5'
        )

        self.username = MDTextField(
            hint_text="Usuário",
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            size_hint=(0.7, None),
            width=200,
            required=True,
            line_color_focus=[0,0,0,1], # Adicionado para manter a cor da linha quando o campo está em foco
            line_anim=False, # Adicionado para desativar a animação da linha
        )
        self.password = MDTextField(
            hint_text="Senha",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.7, None),
            width=200,
            required=True,
            password=True,
            line_color_focus=[0,0,0,1], # Adicionado para manter a cor da linha quando o campo está em foco
            line_anim=False, # Adicionado para desativar a animação da linha
        )

        self.login_button = MDRaisedButton(
            text="Login",
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            size_hint=(0.7, None),
            width=200,
            on_press=self.login
        )

        self.register_button = MDFlatButton(
            text="Registrar-se",
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            size_hint=(0.7, None),
            width=200,
            on_press=self.switch_to_register_screen
        )

        self.return_to_login_button = MDFlatButton(
            text="Retornar ao Login",
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            size_hint=(0.7, None),
            width=200,
            on_press=self.switch_to_login_screen
        )

        self.login_screen.add_widget(self.title_label)
        self.login_screen.add_widget(self.username)
        self.login_screen.add_widget(self.password)
        self.login_screen.add_widget(self.login_button)
        self.login_screen.add_widget(self.register_button)

        self.screen_manager.add_widget(self.login_screen)
        self.screen_manager.add_widget(self.register_screen)  # Adicionar a tela de registro ao ScreenManager

        return self.screen_manager

    def login(self, instance):
        print("Login com usuário:", self.username.text, "e senha:", self.password.text)

    def switch_to_register_screen(self, instance):
        self.screen_manager.current = 'register'

    def switch_to_login_screen(self, instance):
        self.screen_manager.current = 'login'

if _name_ == '_main_':
    LoginApp().run()