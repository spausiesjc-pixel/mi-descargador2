import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import mainthread
from kivy.utils import platform
import yt_dlp
import os

class DownloaderApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.url_input = TextInput(hint_text='Pega el enlace de YouTube aquí', multiline=False, size_hint=(1, 0.2))
        self.layout.add_widget(self.url_input)
        
        self.download_btn = Button(text='Descargar Video', size_hint=(1, 0.2), background_color=(0, 0.7, 0, 1))
        self.download_btn.bind(on_press=self.start_download_thread)
        self.layout.add_widget(self.download_btn)
        
        self.status_label = Label(text='Esperando enlace...', size_hint=(1, 0.6))
        self.layout.add_widget(self.status_label)
        
        self.request_android_permissions()
        return self.layout

    def request_android_permissions(self):
        """Pide permiso de almacenamiento al iniciar en Android"""
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.INTERNET, Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

    def start_download_thread(self, instance):
        url = self.url_input.text
        if not url:
            self.status_label.text = "¡Por favor pega un enlace!"
            return
        
        self.status_label.text = "Iniciando descarga..."
        self.download_btn.disabled = True
        # Ejecutar en segundo plano para no congelar la app
        threading.Thread(target=self.download_video, args=(url,)).start()

    def download_video(self, url):
        # Configuración para guardar en la carpeta de Descargas del móvil
        download_path = '/sdcard/Download/%(title)s.%(ext)s'
        
        ydl_opts = {
            'outtmpl': download_path,
            'format': 'best',  # Descarga la mejor calidad disponible (video+audio)
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.update_status("¡Éxito! Guardado en Descargas.")
        except Exception as e:
            self.update_status(f"Error: {str(e)}")

    @mainthread
    def update_status(self, message):
        """Actualiza la interfaz desde el hilo secundario"""
        self.status_label.text = message
        self.download_btn.disabled = False

if __name__ == '__main__':
    DownloaderApp().run()