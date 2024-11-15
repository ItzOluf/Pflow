import kivy
kivy.require('2.3.0')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 3 # Layout mit 3 Spalten
        # Label und Eingabefeld für Benutzername
        self.username_label = Label(text='User Name')  # Label speichern, um es später zu ändern
        self.add_widget(self.username_label)
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)

        # Platzhalter, damit das Layout 3 Spalten bleibt
        self.add_widget(Label())

        # Label und Eingabefeld für Passwort
        self.add_widget(Label(text='Password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)
        self.add_widget(Label())

        # Button hinzufügen
        self.change_button = Button(text="Login")
        self.change_button.on_press = self.change_username  # Mit Funktion verbinden
        self.add_widget(self.change_button)

    # Funktion, die den Text des Labels ändert
    def change_username(self):
        self.username_label.text = self.username.text  # Label-Text ändern


class MyApp(App):
    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    MyApp().run()
