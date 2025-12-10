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

class MyLogger:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): print(msg)

class DownloaderApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.url_input = TextInput(hint_text='Pega enlace aquí', multiline=False, size_hint=(1, 0.2))
        self.layout.add_widget(self.url_input)
        
        self.download_btn = Button(text='Descargar Audio (M4A)', size_hint=(1, 0.2), background_color=(0, 0.5, 1, 1))
        self.download_btn.bind(on_press=self.start_download_thread)
        self.layout.add_widget(self.download_btn)
        
        self.status_label = Label(text='Guarda en carpeta Music', size_hint=(1, 0.6))
        self.layout.add_widget(self.status_label)
        
        self.request_android_permissions()
        return self.layout

    def request_android_permissions(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.INTERNET, Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

    def start_download_thread(self, instance):
        url = self.url_input.text
        if not url:
            self.status_label.text = "¡Falta enlace!"
            return
        
        self.status_label.text = "Descargando..."
        self.download_btn.disabled = True
        threading.Thread(target=self.download_audio, args=(url,)).start()

    def download_audio(self, url):
        # Guardamos en Music
        download_path = '/sdcard/Music/%(title)s.%(ext)s'
        
        ydl_opts = {
            'outtmpl': download_path,
            # TRUCO: Pedimos m4a directamente. No requiere conversión. ¡No falla!
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'noplaylist': False,
            'quiet': True,
            'no_warnings': True,
            'logger': MyLogger(),
            'ignoreerrors': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.update_status("¡GUARDADO!\nBusca el archivo .m4a en Music")
        except Exception as e:
            self.update_status(f"Error: {str(e)}")

    @mainthread
    def update_status(self, message):
        self.status_label.text = message
        self.download_btn.disabled = False

if __name__ == '__main__':
    DownloaderApp().run()
    
