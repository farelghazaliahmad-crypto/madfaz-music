import os
import threading
import certifi
import yt_dlp
from ytmusicapi import YTMusic

# PENTING: Obat Anti SSL Error biar koneksi ke YouTube gak ditolak Android
os.environ['SSL_CERT_FILE'] = certifi.where()

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList, TwoLineAvatarListItem, IconLeftWidget
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.image import AsyncImage
from kivy.uix.floatlayout import FloatLayout
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

class MusicApp(MDApp):
    def build(self):
        # Tema Aplikasi (Ala Apple Music)
        self.theme_cls.theme_style = "Light" 
        self.theme_cls.primary_palette = "Red"
        
        # Panggil API YouTube Music dengan proteksi error
        try:
            self.yt = YTMusic()
        except Exception as e:
            print(f"Gagal konek YTMusic: {e}")
        
        self.id_lagu_sekarang = ""
        self.player_suara = None

        layar_utama = MDScreen()
        nav_bawah = MDBottomNavigation()
        nav_bawah.text_color_active = self.theme_cls.primary_color

        # ==========================================
        # TAB 1: BERANDA (HOME)
        # ==========================================
        tab_home = MDBottomNavigationItem(name='home', text='Beranda', icon='home')
        layout_home = MDBoxLayout(orientation='vertical', padding=20, spacing=10)
        
        layout_home.add_widget(MDLabel(text="New for Ahmad", font_style="H4", bold=True, size_hint_y=None, height=50))
        
        scroll_home = MDScrollView()
        list_rekomendasi = MDList()
        
        # Contoh Lagu Rekomendasi
        songs = [
            ("Lo-fi Guitar Beats", "Chill Vibes"),
            ("Alternative Rock Hits", "Top Tracks"),
            ("Electric Guitar Solo", "Masterclass"),
            ("For Revenge Style", "Emotional Rock")
        ]
        
        for title, subtitle in songs:
            item = TwoLineAvatarListItem(text=title, secondary_text=subtitle)
            item.add_widget(IconLeftWidget(icon="music-note"))
            list_rekomendasi.add_widget(item)
            
        scroll_home.add_widget(list_rekomendasi)
        layout_home.add_widget(scroll_home)
        tab_home.add_widget(layout_home)

        # ==========================================
        # TAB 2: SEARCH (LIQUID GLASS + PLAYER)
        # ==========================================
        tab_search = MDBottomNavigationItem(name='search', text='Search', icon='magnify')
        layout_tumpuk = FloatLayout()

        # Background Kaca
        self.bg_image = AsyncImage(source='', allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        layout_tumpuk.add_widget(self.bg_image)

        lapisan_kaca = MDBoxLayout(md_bg_color=(1, 1, 1, 0.85), size_hint=(1, 1))
        layout_tumpuk.add_widget(lapisan_kaca)

        # UI Pencarian
        ui_layout = MDBoxLayout(orientation='vertical', padding=40, spacing=15)
        ui_layout.add_widget(MDLabel(text="Search", font_style="H3", bold=True, size_hint_y=None, height=80))
        
        self.input_lagu = MDTextField(hint_text="Cari Artis atau Lagu...", mode="round", size_hint_x=1)
        ui_layout.add_widget(self.input_lagu)
        
        btn_cari = MDFillRoundFlatButton(text="Cari", pos_hint={"center_x": 0.5}, size_hint_x=0.5)
        btn_cari.bind(on_press=self.cari_lagu)
        ui_layout.add_widget(btn_cari)
        
        self.label_hasil = MDLabel(text="", halign='center', size_hint_y=None, height=60, bold=True)
        ui_layout.add_widget(self.label_hasil)
        
        self.cover_album = AsyncImage(source='', size_hint_y=None, height=200)
        ui_layout.add_widget(self.cover_album)

        # Tombol Play Lagu
        self.btn_play = MDFillRoundFlatButton(text="Play Lagu", pos_hint={"center_x": 0.5}, size_hint_x=0.5, disabled=True)
        self.btn_play.bind(on_press=self.putar_lagu)
        ui_layout.add_widget(self.btn_play)

        layout_tumpuk.add_widget(ui_layout)
        tab_search.add_widget(layout_tumpuk)

        # ==========================================
        # TAB 3: LIBRARY (HISTORY)
        # ==========================================
        tab_library = MDBottomNavigationItem(name='library', text='Library', icon='library-music')
        layout_lib = MDBoxLayout(orientation='vertical', padding=20)
        layout_lib.add_widget(MDLabel(text="Koleksi Lu", font_style="H4", bold=True, size_hint_y=None, height=50))
        
        self.list_history = MDList()
        scroll_lib = MDScrollView()
        scroll_lib.add_widget(self.list_history)
        layout_lib.add_widget(scroll_lib)
        tab_library.add_widget(layout_lib)

        # Gabungkan semua tab ke layar
        nav_bawah.
      
