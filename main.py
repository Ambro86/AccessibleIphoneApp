import flet as ft
import flet_audio as fa
import json
import os
import random

class AvventuraEpica:
    def __init__(self, page: ft.Page):
        self.page = page
        self.versione = "1.0.0" 
        self.autore   = "Ambrogio Riili"
        self.inizializza_gioco()
        self.crea_audio_system()
        self.crea_ui()
        
    def inizializza_gioco(self):
        # 🗺️ Mappa del gioco 4x4 - 16 aree diverse!
        self.mappa = [
            ["🏘️ Villaggio", "🌲 Bosco", "🏔️ Montagna", "🏰 Castello"],
            ["🛤️ Strada", "🌊 Lago", "⛰️ Caverna", "🗡️ Arena"],
            ["🏪 Mercato", "🌳 Foresta", "🔥 Vulcano", "❄️ Ghiacciai"],
            ["🏝️ Isola", "🏜️ Deserto", "🌙 Cripta", "👑 Palazzo"]
        ]
        
        # 📖 Descrizioni ricche e immersive
        self.descrizioni = {
            "🏘️ Villaggio": "Un tranquillo villaggio con case di pietra. Gli abitanti ti salutano calorosamente. Qui puoi riposare e fare acquisti.",
            "🌲 Bosco": "Un bosco rigoglioso con alberi secolari. Senti fruscii tra le foglie e vedi ombre misteriose muoversi.",
            "🏔️ Montagna": "Vette innevate che toccano le nuvole. L'aria è rarefatta e il vento soffia forte. Scorgi grotte nascoste.",
            "🏰 Castello": "Un maestoso castello gotico con torri imponenti. Le guardie vigilano ai cancelli. Qui risiede il re.",
            "🛤️ Strada": "Una strada sterrata che collega i villaggi. Mercanti viaggiano con le loro carovane cariche di merci.",
            "🌊 Lago": "Un lago cristallino circondato da canneti. Pesci guizzano nell'acqua e uccelli volano in cerchio.",
            "⛰️ Caverna": "Una caverna buia e umida. Gocce d'acqua echeggiano nell'oscurità. Senti ringhii provenire dal profondo.",
            "🗡️ Arena": "Un'arena di gladiatori con spalti di pietra. La sabbia è macchiata di sangue. Qui si combatte per la gloria.",
            "🏪 Mercato": "Un vivace mercato con bancarelle colorate. Mercanti gridano i loro prezzi. Profumo di spezie nell'aria.",
            "🌳 Foresta": "Una foresta antica e misteriosa. Raggi di sole filtrano tra le fronde. Creature magiche si nascondono qui.",
            "🔥 Vulcano": "Un vulcano attivo con lava che scorre. Il calore è insopportabile. Creature del fuoco popolano quest'area.",
            "❄️ Ghiacciai": "Distese di ghiaccio eterno sotto un cielo plumbeo. Il freddo penetra nelle ossa. Lupi artici ululano.",
            "🏝️ Isola": "Un'isola tropicale con palme e spiagge bianche. Onde si infrangono dolcemente. Pirati potrebbero nascondersi qui.",
            "🏜️ Deserto": "Un deserto rovente con dune infinite. Miraggio danzano all'orizzonte. Scorpioni strisciano sulla sabbia.",
            "🌙 Cripta": "Una cripta sotterranea con sarcofagi antichi. L'aria è stagnante e fredda. Non-morti riposano qui.",
            "👑 Palazzo": "Il palazzo reale con sale dorate. Guardie d'élite presidiano ogni angolo. Tesori inestimabili sono custoditi qui."
        }
        
        # 🎒 Oggetti speciali distribuiti per il mondo
        self.oggetti = {
            "🏘️ Villaggio": "🗝️ chiave di bronzo",
            "🌲 Bosco": "🏹 arco elfico",
            "🏔️ Montagna": "⛏️ piccone di mithril",
            "🏰 Castello": "👑 corona reale",
            "🛤️ Strada": "🥾 stivali da viaggio",
            "🌊 Lago": "🎣 canna da pesca magica",
            "⛰️ Caverna": "💎 gemma brillante",
            "🗡️ Arena": "🛡️ scudo del campione",
            "🏪 Mercato": "",  # Niente oggetti, solo negozi
            "🌳 Foresta": "🌿 erba medicinale",
            "🔥 Vulcano": "🔥 essenza di fuoco",
            "❄️ Ghiacciai": "❄️ cristallo di ghiaccio",
            "🏝️ Isola": "🏴‍☠️ mappa del tesoro",
            "🏜️ Deserto": "🏺 anfora antica",
            "🌙 Cripta": "💀 teschio maledetto",
            "👑 Palazzo": "💰 tesoro reale"
        }
        
        # 👹 Mostri con livelli e statistiche
        self.mostri = {
            "🏘️ Villaggio": None,  # Sicuro
            "🌲 Bosco": {"nome": "🐺 Lupo", "hp": 15, "attacco": 8, "livello": 1, "exp": 20},
            "🏔️ Montagna": {"nome": "🦅 Aquila Gigante", "hp": 25, "attacco": 12, "livello": 2, "exp": 35},
            "🏰 Castello": {"nome": "🛡️ Guardia Reale", "hp": 40, "attacco": 15, "livello": 3, "exp": 50},
            "🛤️ Strada": {"nome": "🏴‍☠️ Bandito", "hp": 20, "attacco": 10, "livello": 2, "exp": 30},
            "🌊 Lago": {"nome": "🐙 Kraken", "hp": 35, "attacco": 18, "livello": 3, "exp": 60},
            "⛰️ Caverna": {"nome": "🐻 Orso delle Caverne", "hp": 30, "attacco": 14, "livello": 2, "exp": 40},
            "🗡️ Arena": {"nome": "⚔️ Gladiatore", "hp": 45, "attacco": 20, "livello": 4, "exp": 80},
            "🏪 Mercato": None,  # Sicuro
            "🌳 Foresta": {"nome": "🧚‍♀️ Spirito Oscuro", "hp": 28, "attacco": 16, "livello": 3, "exp": 45},
            "🔥 Vulcano": {"nome": "🔥 Elementale di Fuoco", "hp": 50, "attacco": 25, "livello": 5, "exp": 100},
            "❄️ Ghiacciai": {"nome": "❄️ Yeti", "hp": 55, "attacco": 22, "livello": 5, "exp": 110},
            "🏝️ Isola": {"nome": "🏴‍☠️ Pirata", "hp": 25, "attacco": 13, "livello": 2, "exp": 35},
            "🏜️ Deserto": {"nome": "🦂 Scorpione Gigante", "hp": 32, "attacco": 17, "livello": 3, "exp": 55},
            "🌙 Cripta": {"nome": "💀 Scheletro Guerriero", "hp": 38, "attacco": 19, "livello": 4, "exp": 70},
            "👑 Palazzo": {"nome": "👑 Boss Finale", "hp": 100, "attacco": 30, "livello": 10, "exp": 500}
        }
        
        # 🏪 Negozi e mercanti
        self.negozi = {
            "🏘️ Villaggio": {
                "🍞 Pane": {"prezzo": 5, "tipo": "cibo", "descrizione": "Ripristina 15 HP"},
                "⚔️ Spada": {"prezzo": 50, "tipo": "arma", "descrizione": "+5 danno"},
                "🛡️ Armatura": {"prezzo": 80, "tipo": "armatura", "descrizione": "-3 danni ricevuti"}
            },
            "🏪 Mercato": {
                "🧪 Pozione Vita": {"prezzo": 30, "tipo": "pozione", "descrizione": "Ripristina 50 HP"},
                "⚡ Pozione Forza": {"prezzo": 45, "tipo": "pozione", "descrizione": "+10 danno per 3 turni"},
                "🏹 Arco Lungo": {"prezzo": 120, "tipo": "arma", "descrizione": "+8 danno"},
                "💎 Anello Magico": {"prezzo": 200, "tipo": "accessorio", "descrizione": "+2 HP per turno"}
            },
            "🛤️ Strada": {
                "🍎 Mela": {"prezzo": 3, "tipo": "cibo", "descrizione": "Ripristina 10 HP"},
                "🗡️ Pugnale": {"prezzo": 25, "tipo": "arma", "descrizione": "+3 danno"},
                "📜 Mappa": {"prezzo": 15, "tipo": "oggetto", "descrizione": "Mostra tutte le aree"}
            }
        }
        
        # 🎵 Musiche per ogni area
        self.musiche_aree = {
            "🏘️ Villaggio": "assets/music/1.wav",
            "🌲 Bosco": "assets/music/2.wav",
            "🏔️ Montagna": "assets/music/3.wav", 
            "🏰 Castello": "assets/music/4.wav",
            "🛤️ Strada": "assets/music/5.wav",
            "🌊 Lago": "assets/music/6.wav",
            "⛰️ Caverna": "assets/music/7.wav",
            "🗡️ Arena": "assets/music/8.wav",
            "🏪 Mercato": "assets/music/9.wav",
            "🌳 Foresta": "assets/music/10.wav",
            "🔥 Vulcano": "assets/music/11.wav",
            "❄️ Ghiacciai": "assets/music/12.wav",
            "🏝️ Isola": "assets/music/13.wav",
            "🏜️ Deserto": "assets/music/14.wav",
            "🌙 Cripta": "assets/music/15.wav",
            "👑 Palazzo": "assets/music/16.wav"
        }
        
        # 📊 Stato del giocatore avanzato
        self.posizione_giocatore = [0, 0]
        self.hp_giocatore = 100
        self.hp_max = 100
        self.livello = 1
        self.esperienza = 0
        self.esperienza_prossimo_livello = 100
        self.attacco_base = 15
        self.difesa = 0
        self.monete = 100
        self.inventario = []
        self.equipaggiamento = {"arma": None, "armatura": None, "accessorio": None}
        self.effetti_temporanei = {}
        self.gioco_iniziato = False
        self.audio_abilitato = True
        self.haptic_abilitato = True
        self.volume_musica = 0.3
        self.volume_effetti = 0.7
        self.turno = 0
        
        # Stato dell'interfaccia
        self.modalita_menu = "principale"  # principale, gioco, inventario, negozio, statistiche
        
    def reset_gioco(self):
        """Reset completo con nuove statistiche"""
        self.oggetti = {
            "🏘️ Villaggio": "🗝️ chiave di bronzo",
            "🌲 Bosco": "🏹 arco elfico",
            "🏔️ Montagna": "⛏️ piccone di mithril",
            "🏰 Castello": "👑 corona reale",
            "🛤️ Strada": "🥾 stivali da viaggio",
            "🌊 Lago": "🎣 canna da pesca magica",
            "⛰️ Caverna": "💎 gemma brillante",
            "🗡️ Arena": "🛡️ scudo del campione",
            "🏪 Mercato": "",
            "🌳 Foresta": "🌿 erba medicinale",
            "🔥 Vulcano": "🔥 essenza di fuoco",
            "❄️ Ghiacciai": "❄️ cristallo di ghiaccio",
            "🏝️ Isola": "🏴‍☠️ mappa del tesoro",
            "🏜️ Deserto": "🏺 anfora antica",
            "🌙 Cripta": "💀 teschio maledetto",
            "👑 Palazzo": "💰 tesoro reale"
        }
        
        self.mostri = {
            "🏘️ Villaggio": None,
            "🌲 Bosco": {"nome": "🐺 Lupo", "hp": 15, "attacco": 8, "livello": 1, "exp": 20},
            "🏔️ Montagna": {"nome": "🦅 Aquila Gigante", "hp": 25, "attacco": 12, "livello": 2, "exp": 35},
            "🏰 Castello": {"nome": "🛡️ Guardia Reale", "hp": 40, "attacco": 15, "livello": 3, "exp": 50},
            "🛤️ Strada": {"nome": "🏴‍☠️ Bandito", "hp": 20, "attacco": 10, "livello": 2, "exp": 30},
            "🌊 Lago": {"nome": "🐙 Kraken", "hp": 35, "attacco": 18, "livello": 3, "exp": 60},
            "⛰️ Caverna": {"nome": "🐻 Orso delle Caverne", "hp": 30, "attacco": 14, "livello": 2, "exp": 40},
            "🗡️ Arena": {"nome": "⚔️ Gladiatore", "hp": 45, "attacco": 20, "livello": 4, "exp": 80},
            "🏪 Mercato": None,
            "🌳 Foresta": {"nome": "🧚‍♀️ Spirito Oscuro", "hp": 28, "attacco": 16, "livello": 3, "exp": 45},
            "🔥 Vulcano": {"nome": "🔥 Elementale di Fuoco", "hp": 50, "attacco": 25, "livello": 5, "exp": 100},
            "❄️ Ghiacciai": {"nome": "❄️ Yeti", "hp": 55, "attacco": 22, "livello": 5, "exp": 110},
            "🏝️ Isola": {"nome": "🏴‍☠️ Pirata", "hp": 25, "attacco": 13, "livello": 2, "exp": 35},
            "🏜️ Deserto": {"nome": "🦂 Scorpione Gigante", "hp": 32, "attacco": 17, "livello": 3, "exp": 55},
            "🌙 Cripta": {"nome": "💀 Scheletro Guerriero", "hp": 38, "attacco": 19, "livello": 4, "exp": 70},
            "👑 Palazzo": {"nome": "👑 Boss Finale", "hp": 100, "attacco": 30, "livello": 10, "exp": 500}
        }
        
        self.posizione_giocatore = [0, 0]
        self.hp_giocatore = 100
        self.hp_max = 100
        self.livello = 1
        self.esperienza = 0
        self.esperienza_prossimo_livello = 100
        self.attacco_base = 15
        self.difesa = 0
        self.monete = 100
        self.inventario = []
        self.equipaggiamento = {"arma": None, "armatura": None, "accessorio": None}
        self.effetti_temporanei = {}
        self.turno = 0
        
    def crea_audio_system(self):
        """Sistema audio semplificato"""
        self.musica_sottofondo = fa.Audio(
            src="assets/music/1.wav",
            autoplay=False,
            volume=self.volume_musica,
            balance=0,
            on_state_changed=lambda e: print(f"🎵 Stato: {e.data}"),
            on_loaded=lambda _: print("🎵 Caricato")
        )
        
        self.effetti_sonori = fa.Audio(
            src="assets/sounds/5.wav",
            autoplay=False,
            volume=self.volume_effetti,
            balance=0
        )
        
        self.musica_attuale = ""
        self.page.overlay.extend([self.musica_sottofondo, self.effetti_sonori])
        
    def haptic_feedback(self, tipo="light"):
        """Feedback aptico"""
        if not self.haptic_abilitato:
            return
            
        try:
            if hasattr(self.page, 'haptic_feedback'):
                self.page.haptic_feedback(tipo)
            else:
                js_code = f"""
                if (navigator.vibrate) {{
                    const patterns = {{
                        'light': [50],
                        'medium': [100], 
                        'heavy': [200],
                        'success': [100, 50, 100],
                        'warning': [150, 100, 150],
                        'error': [200, 100, 200, 100, 200]
                    }};
                    navigator.vibrate(patterns['{tipo}'] || [50]);
                }}
                """
                self.page.evaluate_js(js_code)
        except Exception:
            pass
            
    def on_musica_state_changed(self, e):
        """Loop musica"""
        if e.data == "completed" and self.audio_abilitato:
            self.musica_sottofondo.play()
            
    def cambia_musica_area(self, area):
        """Cambia musica con sistema robusto"""
        if not self.audio_abilitato or area not in self.musiche_aree:
            return
            
        file_musica = self.musiche_aree[area]
        
        if self.musica_attuale == file_musica:
            return
            
        if not os.path.exists(file_musica):
            return
            
        if self.musica_sottofondo in self.page.overlay:
            self.page.overlay.remove(self.musica_sottofondo)
        
        self.musica_sottofondo = fa.Audio(
            src=file_musica,
            autoplay=True,
            volume=self.volume_musica,
            balance=0,
            on_state_changed=self.on_musica_state_changed,
            on_loaded=lambda _: print(f"🎵 Nuovo file: {file_musica}")
        )
        
        self.page.overlay.append(self.musica_sottofondo)
        self.page.update()
        self.musica_attuale = file_musica
        
    def riproduci_effetto(self, effetto):
        """Effetti sonori"""
        if not self.audio_abilitato:
            return
            
        effetti_files = {
            "attacco": "assets/sounds/5.wav",
            "raccogli": "assets/sounds/6.wav", 
            "mostro": "assets/sounds/7.wav",
            "vittoria": "assets/sounds/8.wav",
            "sconfitta": "assets/sounds/9.wav",
            "monete": "assets/sounds/5.wav",
            "livello": "assets/sounds/8.wav"
        }
        
        if effetto in effetti_files:
            self.effetti_sonori.src = effetti_files[effetto]
            self.effetti_sonori.volume = self.volume_effetti
            self.effetti_sonori.play()
            
    def calcola_attacco_totale(self):
        """Calcola attacco con equipaggiamento"""
        attacco = self.attacco_base
        if self.equipaggiamento["arma"]:
            if "Spada" in self.equipaggiamento["arma"]:
                attacco += 5
            elif "Arco" in self.equipaggiamento["arma"]:
                attacco += 8
            elif "Pugnale" in self.equipaggiamento["arma"]:
                attacco += 3
        
        # Effetti temporanei
        if "forza" in self.effetti_temporanei:
            attacco += 10
            
        return attacco
        
    def calcola_difesa_totale(self):
        """Calcola difesa con equipaggiamento"""
        difesa = self.difesa
        if self.equipaggiamento["armatura"]:
            if "Armatura" in self.equipaggiamento["armatura"]:
                difesa += 3
        return difesa
        
    def gestisci_livello(self):
        """Sistema di livellamento"""
        if self.esperienza >= self.esperienza_prossimo_livello:
            self.livello += 1
            self.esperienza -= self.esperienza_prossimo_livello
            self.esperienza_prossimo_livello = self.livello * 100
            
            # Bonus per livello
            self.hp_max += 20
            self.hp_giocatore = self.hp_max  # Ripristina HP
            self.attacco_base += 3
            
            self.haptic_feedback("success")
            self.riproduci_effetto("livello")
            
            return f"🎉 LIVELLO AUMENTATO! Ora sei livello {self.livello}!\n💪 HP Max: {self.hp_max}, Attacco: {self.attacco_base}\n"
        return ""
        
    def gestisci_effetti_temporanei(self):
        """Gestisce effetti con durata"""
        effetti_scaduti = []
        for effetto, turni_rimasti in self.effetti_temporanei.items():
            if turni_rimasti <= 1:
                effetti_scaduti.append(effetto)
            else:
                self.effetti_temporanei[effetto] -= 1
                
        for effetto in effetti_scaduti:
            del self.effetti_temporanei[effetto]
            
        if effetti_scaduti:
            return f"⏰ Effetti scaduti: {', '.join(effetti_scaduti)}\n"
        return ""
        
    def rigenerazione_passiva(self):
        """Rigenerazione HP con anello magico"""
        if self.equipaggiamento["accessorio"] and "Anello" in self.equipaggiamento["accessorio"]:
            if self.hp_giocatore < self.hp_max:
                self.hp_giocatore = min(self.hp_max, self.hp_giocatore + 2)
                return "💍 L'anello magico ti rigenera 2 HP!\n"
        return ""
        
    # LOGICA PULSANTI DINAMICI
    
    def movimenti_possibili(self):
        """Restituisce lista dei movimenti possibili dalla posizione attuale"""
        riga, colonna = self.posizione_giocatore
        movimenti = []
        
        if riga > 0:  # Può andare a nord
            movimenti.append(("⬆️ Nord", "nord"))
        if riga < 3:  # Può andare a sud
            movimenti.append(("⬇️ Sud", "sud"))
        if colonna > 0:  # Può andare a ovest
            movimenti.append(("⬅️ Ovest", "ovest"))
        if colonna < 3:  # Può andare a est
            movimenti.append(("➡️ Est", "est"))
            
        return movimenti
    
    def azioni_possibili(self):
        """Restituisce lista delle azioni possibili nell'area attuale"""
        riga, colonna = self.posizione_giocatore
        stanza_attuale = self.mappa[riga][colonna]
        azioni = []
        
        # Raccogli solo se c'è un oggetto
        if self.oggetti[stanza_attuale]:
            azioni.append(("🎒 Raccogli", self.raccogli_oggetto, "Raccogli oggetti nell'area"))
            
        # Attacca solo se c'è un mostro
        if self.mostri[stanza_attuale]:
            azioni.append(("⚔️ Attacca", self.attacca_mostro, "Attacca il mostro presente"))
            
        # Negozio solo se c'è un negozio
        if stanza_attuale in self.negozi:
            azioni.append(("🏪 Negozio", self.vai_a_negozio, "Visita il negozio dell'area"))
            
        return azioni
    
    def oggetti_usabili(self):
        """Restituisce True se ci sono oggetti usabili nell'inventario"""
        for oggetto in self.inventario:
            if any(keyword in oggetto for keyword in ["Pozione", "Pane", "Mela", "erba"]):
                return True
        return False
    
    def oggetti_equipaggiabili(self):
        """Restituisce True se ci sono oggetti equipaggiabili nell'inventario"""
        for oggetto in self.inventario:
            if any(keyword in oggetto for keyword in ["Spada", "Arco", "Pugnale", "Armatura", "Scudo", "Anello"]):
                return True
        return False
    
    def oggetti_acquistabili(self):
        """Restituisce True se ci sono oggetti acquistabili nel negozio attuale"""
        riga, colonna = self.posizione_giocatore
        stanza_attuale = self.mappa[riga][colonna]
        
        if stanza_attuale not in self.negozi:
            return False
            
        negozio = self.negozi[stanza_attuale]
        for nome, info in negozio.items():
            if self.monete >= info["prezzo"]:
                return True
        return False
    def crea_ui(self):
        """Crea l'interfaccia utente principale con tab in fondo accessibili"""
        self.page.title = "🏰 Avventura Epica - Accessibile"
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.theme_mode = ft.ThemeMode.DARK  # Tema scuro per un look più immersivo
        
        # Inizializza i componenti principali con colori
        self.area_stats = ft.TextField(
            value="📊 Statistiche Giocatore:\n👤 Livello 1 • ❤️ 100/100 HP • 💰 100 monete\n⚔️ Attacco: 15 • 🛡️ Difesa: 0\n⭐ EXP: 0/100",
            multiline=True,
            read_only=True,
            min_lines=4,
            max_lines=6,
            text_size=14,
            label="📊 Le tue statistiche",
            bgcolor=ft.Colors.BLUE_GREY_900,
            color=ft.Colors.CYAN_100,
            border_color=ft.Colors.CYAN_400,
            focused_border_color=ft.Colors.CYAN_300
        )
        
        self.area_storia = ft.TextField(
            value="🎮 Benvenuto nell'Avventura Epica!\n🗺️ Esplora 16 aree diverse\n🛍️ Visita negozi e mercanti\n⚔️ Combatti mostri e sali di livello\n🎵 Audio immersivo e feedback aptico\n\nPremi 'Inizia Avventura' per cominciare!",
            multiline=True,
            read_only=True,
            expand=True,
            min_lines=10,
            max_lines=15,
            text_size=14,
            label="📜 La tua storia epica",
            bgcolor=ft.Colors.DEEP_PURPLE_900,
            color=ft.Colors.AMBER_100,
            border_color=ft.Colors.AMBER_400,
            focused_border_color=ft.Colors.AMBER_300
        )
        
        self.container_pulsanti = ft.Column()
        
        # Contenitore principale per il contenuto della tab Home
        self.container_principale = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=20,
            expand=True
        )
        
        # Imposta il menu principale come vista iniziale per la tab Home
        self.crea_menu_principale_per_tab()
        
        # 🔹 CONTENUTO TAB HOME
        home_content = ft.Container(
            content=self.container_principale,
            bgcolor=ft.Colors.GREY_900,
            padding=20,
            border_radius=10
        )
        
        # 🔹 CONTENUTO TAB IMPOSTAZIONI
        impostazioni_content = ft.Container(
            content=self.crea_contenuto_impostazioni(),
            bgcolor=ft.Colors.BLUE_GREY_800,
            padding=20,
            border_radius=10
        )
        
        # 🔹 CONTENUTO TAB INFO
        info_content = ft.Container(
            content=self.crea_contenuto_info(),
            bgcolor=ft.Colors.GREEN_900,
            padding=20,
            border_radius=10
        )
        
        # Costruzione delle Tab (manteniamo il sistema esistente)
        self.tabs = ft.Tabs(
            selected_index=0,
            expand=1,
            indicator_color=ft.Colors.AMBER_400,
            label_color=ft.Colors.WHITE,
            unselected_label_color=ft.Colors.GREY_400,
            tabs=[
                ft.Tab(
                    text="🏠 Home", 
                    content=home_content,
                    icon=ft.Icons.HOME
                ),
                ft.Tab(
                    text="⚙️ Impostazioni", 
                    content=impostazioni_content,
                    icon=ft.Icons.SETTINGS
                ),
                ft.Tab(
                    text="ℹ️ Info", 
                    content=info_content,
                    icon=ft.Icons.INFO
                ),
            ],
            on_change=self.on_tab_change
        )
        
        # Barra di navigazione in fondo - accessibile a VoiceOver
        self.nav_bar = ft.Container(
            content=ft.Row(
                controls=[
                    ft.TextButton(
                        content=ft.Column([
                            ft.Icon(ft.Icons.HOME, size=24),
                            ft.Text("Home", size=12)
                        ], 
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=2),
                        on_click=lambda _: self.seleziona_tab(0),
                        style=ft.ButtonStyle(
                            color=ft.Colors.AMBER_400,
                            padding=ft.padding.all(8)
                        ),
                        tooltip="Vai alla schermata principale"
                    ),
                    ft.TextButton(
                        content=ft.Column([
                            ft.Icon(ft.Icons.SETTINGS, size=24),
                            ft.Text("Impostazioni", size=12)
                        ], 
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=2),
                        on_click=lambda _: self.seleziona_tab(1),
                        style=ft.ButtonStyle(
                            color=ft.Colors.GREY_400,
                            padding=ft.padding.all(8)
                        ),
                        tooltip="Vai alle impostazioni audio e vibrazione"
                    ),
                    ft.TextButton(
                        content=ft.Column([
                            ft.Icon(ft.Icons.INFO, size=24),
                            ft.Text("Info", size=12)
                        ], 
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=2),
                        on_click=lambda _: self.seleziona_tab(2),
                        style=ft.ButtonStyle(
                            color=ft.Colors.GREY_400,
                            padding=ft.padding.all(8)
                        ),
                        tooltip="Informazioni sul gioco e l'autore"
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY
            ),
            bgcolor=ft.Colors.GREY_900,
            padding=ft.padding.all(10),
            height=70,
            border=ft.border.only(top=ft.BorderSide(1, ft.Colors.GREY_600))
        )
        
        # Layout finale: Column semplice con contenuto sopra e nav bar sotto
        layout_finale = ft.Column(
            controls=[
                # Contenuto principale che si espande
                ft.Container(
                    content=self.tabs,
                    expand=True
                ),
                # Barra di navigazione fissa in fondo
                self.nav_bar
            ],
            spacing=0,
            expand=True
        )
        
        # Inizializza variabile tab corrente
        self.tab_corrente = 0
        
        # Aggiungi alla pagina
        self.page.controls.clear()
        self.page.add(layout_finale)
        self.page.update()
    def seleziona_tab(self, index):
        """Seleziona tab e aggiorna la navigazione"""
        self.tab_corrente = index
        self.tabs.selected_index = index
        self.aggiorna_nav_bar()
        self.page.update()
        # Chiama la funzione di cambio tab esistente se necessario
        if hasattr(self, 'on_tab_change'):
            class MockEvent:
                def __init__(self, selected_index):
                    self.control = self
                    self.selected_index = selected_index
            self.on_tab_change(MockEvent(index))

    def aggiorna_nav_bar(self):
        """Aggiorna i colori della barra di navigazione"""
        # Questa funzione verrà chiamata automaticamente dal seleziona_tab
        pass
    def on_tab_change(self, e):
        """Gestisce il cambio di tab"""
        # Quando si cambia tab, aggiorna le etichette dei volumi se necessario
        if e.control.selected_index == 1:  # Tab Impostazioni
            self.aggiorna_labels_volume()
            
    def aggiorna_labels_volume(self):
        """Aggiorna le etichette del volume"""
        if hasattr(self, 'volume_musica_label_tab'):
            self.volume_musica_label_tab.value = f"🎵 Volume Musica: {int(self.volume_musica * 100)}%"
        if hasattr(self, 'volume_effetti_label_tab'):
            self.volume_effetti_label_tab.value = f"🔊 Volume Effetti: {int(self.volume_effetti * 100)}%"
        self.page.update()
    
    def crea_contenuto_impostazioni(self):
        """Crea il contenuto della tab impostazioni"""
        # Toggle audio e haptic
        toggle_audio = ft.Switch(
            label="🔊 Audio Attivato",
            value=self.audio_abilitato,
            on_change=self.toggle_audio_callback,
            tooltip="Attiva o disattiva tutti gli effetti audio"
        )
        
        toggle_haptic = ft.Switch(
            label="📳 Vibrazione Attivata",
            value=self.haptic_abilitato,
            on_change=self.toggle_haptic_callback,
            tooltip="Attiva o disattiva il feedback aptico"
        )
        
        # Slider volume musica per tab
        self.volume_musica_label_tab = ft.Text(f"🎵 Volume Musica: {int(self.volume_musica * 100)}%")
        slider_volume_musica = ft.Slider(
            min=0,
            max=1,
            value=self.volume_musica,
            divisions=10,
            on_change=self.cambia_volume_musica_tab,
            tooltip="Regola il volume della musica di sottofondo"
        )
        
        # Slider volume effetti per tab
        self.volume_effetti_label_tab = ft.Text(f"🔊 Volume Effetti: {int(self.volume_effetti * 100)}%")
        slider_volume_effetti = ft.Slider(
            min=0,
            max=1,
            value=self.volume_effetti,
            divisions=10,
            on_change=self.cambia_volume_effetti_tab,
            tooltip="Regola il volume degli effetti sonori"
        )
        
        # Pulsante test audio
        test_audio_btn = ft.ElevatedButton(
            "🎵 Testa Audio",
            on_click=self.testa_audio,
            width=200,
            tooltip="Riproduci un suono di test"
        )
        
        return ft.Column(
            [
                ft.Text("⚙️ IMPOSTAZIONI", size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Divider(),
                
                ft.Text("🔊 Audio", size=16, weight=ft.FontWeight.BOLD),
                toggle_audio,
                ft.Container(height=10),
                
                self.volume_musica_label_tab,
                slider_volume_musica,
                ft.Container(height=10),
                
                self.volume_effetti_label_tab,
                slider_volume_effetti,
                ft.Container(height=10),
                
                test_audio_btn,
                ft.Divider(),
                
                ft.Text("📳 Feedback", size=16, weight=ft.FontWeight.BOLD),
                toggle_haptic,
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    
    def crea_contenuto_info(self):
        """Crea il contenuto della tab info"""
        return ft.Column(
            [
                ft.Text("ℹ️ INFORMAZIONI", size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Divider(),
                
                ft.Container(height=20),
                ft.Text("🏰⚔️ AVVENTURA EPICA ⚔️🏰", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Container(height=10),
                
                ft.Text(f"📋 Versione: {self.versione}", size=16),
                ft.Text(f"👨‍💻 Autore: {self.autore}", size=16),
                ft.Text("📅 Data rilascio: 18 giugno 2025", size=16),
                ft.Container(height=20),
                
                ft.Text("📖 Descrizione:", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Un emozionante RPG accessibile con audio immersivo e feedback aptico. "
                    "Esplora 16 aree diverse, combatti mostri, raccogli tesori, visita negozi "
                    "e diventa il nuovo re!",
                    size=14,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=20),
                
                ft.Text("🎮 Caratteristiche:", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("🗺️ 16 aree uniche da esplorare", size=14),
                ft.Text("⚔️ Sistema di combattimento con livellamento", size=14),
                ft.Text("🛍️ Negozi e mercanti", size=14),
                ft.Text("🎒 Sistema di inventario ed equipaggiamento", size=14),
                ft.Text("🎵 Audio immersivo per ogni area", size=14),
                ft.Text("📳 Feedback aptico per un'esperienza tattile", size=14),
                ft.Text("💾 Salvataggio e caricamento partite", size=14),
                ft.Text("♿ Completamente accessibile con screen reader", size=14),
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=8,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def crea_menu_principale_per_tab(self):
        """Crea il menu principale per la tab Home con colori"""
        self.container_pulsanti.controls.clear()
        
        # Titoli con colori
        titolo_principale = ft.Text(
            "🏰⚔️ AVVENTURA EPICA ⚔️🏰", 
            size=28, 
            weight=ft.FontWeight.BOLD, 
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.AMBER_400
        )
        sottotitolo = ft.Text(
            "🎵 Audio Immersivo • 📳 Feedback Aptico • 🗺️ 16 Aree • 🛍️ Negozi • ⚔️ RPG", 
            size=14, 
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.CYAN_200
        )
        
        pulsanti = ft.Column([
            ft.ElevatedButton(
                text="🎮 Inizia Nuova Avventura",
                on_click=self.inizia_gioco,
                width=300,
                height=50,
                tooltip="Inizia una nuova partita",
                bgcolor=ft.Colors.GREEN_700,
                color=ft.Colors.WHITE,
                style=ft.ButtonStyle(
                    overlay_color=ft.Colors.GREEN_600,
                    elevation=8
                )
            ),
            ft.ElevatedButton(
                text="📂 Carica Gioco Salvato",
                on_click=self.carica_gioco,
                width=300,
                height=50,
                tooltip="Carica una partita precedentemente salvata",
                bgcolor=ft.Colors.BLUE_700,
                color=ft.Colors.WHITE,
                style=ft.ButtonStyle(
                    overlay_color=ft.Colors.BLUE_600,
                    elevation=8
                )
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
        
        self.container_pulsanti.controls.append(pulsanti)
        
        # Layout per menu principale nella tab
        self.container_principale.controls.clear()
        self.container_principale.controls.extend([
            titolo_principale,
            sottotitolo,
            self.area_storia,
            self.area_stats,
            self.container_pulsanti
        ])
        
        self.modalita_menu = "principale"
        self.page.update()
        
    def crea_menu_gioco(self):
        """Crea il menu di gioco con pulsanti dinamici e colori"""
        self.container_pulsanti.controls.clear()
        
        # MOVIMENTO DINAMICO - Solo direzioni possibili
        movimenti_disponibili = self.movimenti_possibili()
        if movimenti_disponibili:
            pulsanti_movimento = []
            for testo, direzione in movimenti_disponibili:
                pulsanti_movimento.append(
                    ft.ElevatedButton(
                        testo, 
                        on_click=lambda _, d=direzione: self.muovi(d), 
                        width=100, 
                        tooltip=f"Muoviti verso {direzione}",
                        bgcolor=ft.Colors.INDIGO_600,
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            overlay_color=ft.Colors.INDIGO_500,
                            elevation=4
                        )
                    )
                )
            
            movimento_row = ft.Row(
                pulsanti_movimento, 
                alignment=ft.MainAxisAlignment.CENTER, 
                spacing=10
            )
            self.container_pulsanti.controls.append(movimento_row)
        
        # AZIONI DINAMICHE - Solo azioni possibili
        azioni_disponibili = self.azioni_possibili()
        if azioni_disponibili:
            pulsanti_azioni = []
            for testo, funzione, tooltip in azioni_disponibili:
                # Colori diversi per azioni diverse
                if "Raccogli" in testo:
                    color = ft.Colors.ORANGE_600
                    overlay = ft.Colors.ORANGE_500
                elif "Attacca" in testo:
                    color = ft.Colors.RED_700
                    overlay = ft.Colors.RED_600
                elif "Negozio" in testo:
                    color = ft.Colors.PURPLE_600
                    overlay = ft.Colors.PURPLE_500
                else:
                    color = ft.Colors.BLUE_600
                    overlay = ft.Colors.BLUE_500
                    
                pulsanti_azioni.append(
                    ft.ElevatedButton(
                        testo,
                        on_click=funzione,
                        width=120,
                        tooltip=tooltip,
                        bgcolor=color,
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            overlay_color=overlay,
                            elevation=6
                        )
                    )
                )
            
            azioni_row = ft.Row(
                pulsanti_azioni,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )
            self.container_pulsanti.controls.append(azioni_row)
        
        # MENU SEMPRE DISPONIBILI
        menu_base = []
        
        # Inventario solo se non vuoto O se ci sono oggetti equipaggiati
        if self.inventario or any(self.equipaggiamento.values()):
            menu_base.append(
                ft.ElevatedButton(
                    "📋 Inventario", 
                    on_click=self.vai_a_inventario, 
                    width=140, 
                    tooltip="Visualizza inventario ed equipaggiamento",
                    bgcolor=ft.Colors.BROWN_600,
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(
                        overlay_color=ft.Colors.BROWN_500,
                        elevation=4
                    )
                )
            )
        
        # Statistiche sempre disponibili
        menu_base.append(
            ft.ElevatedButton(
                "📊 Statistiche", 
                on_click=self.vai_a_statistiche, 
                width=140, 
                tooltip="Visualizza statistiche dettagliate",
                bgcolor=ft.Colors.CYAN_600,
                color=ft.Colors.WHITE,
                style=ft.ButtonStyle(
                    overlay_color=ft.Colors.CYAN_500,
                    elevation=4
                )
            )
        )
        
        # Salva sempre disponibile
        menu_base.append(
            ft.ElevatedButton(
                "💾 Salva", 
                on_click=self.salva_gioco, 
                width=140, 
                tooltip="Salva la partita corrente",
                bgcolor=ft.Colors.GREEN_600,
                color=ft.Colors.WHITE,
                style=ft.ButtonStyle(
                    overlay_color=ft.Colors.GREEN_500,
                    elevation=4
                )
            )
        )
        
        if menu_base:
            menu_row = ft.Row(
                menu_base,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )
            self.container_pulsanti.controls.append(menu_row)
        
        # Torna al menu sempre disponibile
        torna_menu = ft.Row([
            ft.ElevatedButton(
                "🚪 Torna al Menu Principale", 
                on_click=self.torna_menu_principale, 
                width=200, 
                tooltip="Torna al menu principale",
                bgcolor=ft.Colors.GREY_700,
                color=ft.Colors.WHITE,
                style=ft.ButtonStyle(
                    overlay_color=ft.Colors.GREY_600,
                    elevation=4
                )
            )
        ], alignment=ft.MainAxisAlignment.CENTER)
        
        self.container_pulsanti.controls.append(torna_menu)
        
        # Layout per gioco (SENZA titoli, PRIMA area storia, POI statistiche)
        self.container_principale.controls.clear()
        self.container_principale.controls.extend([
            self.area_storia,
            self.area_stats,
            self.container_pulsanti
        ])
        
        self.modalita_menu = "gioco"
        self.page.update()
        
    def crea_menu_inventario(self):
        """Menu inventario con pulsanti dinamici"""
        self.container_pulsanti.controls.clear()
        
        pulsanti_inventario = []
        
        # Usa oggetto solo se ci sono oggetti usabili
        if self.oggetti_usabili():
            pulsanti_inventario.append(
                ft.ElevatedButton(
                    "🧪 Usa Oggetto", 
                    on_click=self.usa_oggetto, 
                    width=200, 
                    height=50, 
                    tooltip="Usa pozioni o oggetti consumabili",
                    data="btn_usa_oggetto"
                )
            )
        
        # Equipaggia solo se ci sono oggetti equipaggiabili
        if self.oggetti_equipaggiabili():
            pulsanti_inventario.append(
                ft.ElevatedButton(
                    "⚔️ Equipaggia", 
                    on_click=self.equipaggia_oggetto, 
                    width=200, 
                    height=50, 
                    tooltip="Equipaggia armi, armature o accessori",
                    data="btn_equipaggia"
                )
            )
        
        # Torna sempre disponibile
        pulsanti_inventario.append(
            ft.ElevatedButton(
                "🔙 Torna al Gioco", 
                on_click=self.torna_al_gioco, 
                width=200, 
                height=50, 
                tooltip="Torna alla schermata di gioco",
                data="btn_torna_gioco"
            )
        )
        
        pulsanti = ft.Column(
            pulsanti_inventario,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
            spacing=15
        )
        
        self.container_pulsanti.controls.append(pulsanti)
        
        # Layout per inventario
        self.container_principale.controls.clear()
        self.container_principale.controls.extend([
            self.area_storia,
            self.area_stats,
            self.container_pulsanti
        ])
        
        self.modalita_menu = "inventario"
        self.page.update()
        
    def crea_menu_negozio(self):
        """Menu negozio con pulsanti dinamici"""
        self.container_pulsanti.controls.clear()
        
        pulsanti_negozio = []
        
        # Compra solo se ci sono oggetti acquistabili
        if self.oggetti_acquistabili():
            pulsanti_negozio.append(
                ft.ElevatedButton(
                    "💰 Compra Oggetto", 
                    on_click=self.compra_oggetto, 
                    width=200, 
                    height=50, 
                    tooltip="Compra oggetti dal negozio",
                    data="btn_compra"
                )
            )
        
        # Torna sempre disponibile
        pulsanti_negozio.append(
            ft.ElevatedButton(
                "🔙 Torna al Gioco", 
                on_click=self.torna_al_gioco, 
                width=200, 
                height=50, 
                tooltip="Torna alla schermata di gioco",
                data="btn_torna_gioco"
            )
        )
        
        pulsanti = ft.Column(
            pulsanti_negozio,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
            spacing=15
        )
        
        self.container_pulsanti.controls.append(pulsanti)
        
        # Layout per negozio
        self.container_principale.controls.clear()
        self.container_principale.controls.extend([
            self.area_storia,
            self.area_stats,
            self.container_pulsanti
        ])
        
        self.modalita_menu = "negozio"
        self.page.update()
        
    def crea_menu_statistiche(self):
        """Menu statistiche semplificato"""
        self.container_pulsanti.controls.clear()
        
        pulsanti = ft.Column([
            ft.ElevatedButton(
                "🔙 Torna al Gioco", 
                on_click=self.torna_al_gioco, 
                width=200, 
                height=50, 
                tooltip="Torna alla schermata di gioco",
                data="btn_torna_gioco"
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)
        
        self.container_pulsanti.controls.append(pulsanti)
        
        # Layout per statistiche
        self.container_principale.controls.clear()
        self.container_principale.controls.extend([
            self.area_storia,
            self.area_stats,
            self.container_pulsanti
        ])
        
        self.modalita_menu = "statistiche"
        self.page.update()
        
    def crea_menu_impostazioni(self):
        """Menu impostazioni completo"""
        self.container_pulsanti.controls.clear()
        
        # Toggle audio e haptic
        toggle_audio = ft.Switch(
            label="🔊 Audio Attivato",
            value=self.audio_abilitato,
            on_change=self.toggle_audio_callback,
            tooltip="Attiva o disattiva tutti gli effetti audio"
        )
        
        toggle_haptic = ft.Switch(
            label="📳 Vibrazione Attivata",
            value=self.haptic_abilitato,
            on_change=self.toggle_haptic_callback,
            tooltip="Attiva o disattiva il feedback aptico"
        )
        
        # Slider volume musica
        self.volume_musica_label = ft.Text(f"🎵 Volume Musica: {int(self.volume_musica * 100)}%")
        slider_volume_musica = ft.Slider(
            min=0,
            max=1,
            value=self.volume_musica,
            divisions=10,
            on_change=self.cambia_volume_musica,
            tooltip="Regola il volume della musica di sottofondo"
        )
        
        # Slider volume effetti
        self.volume_effetti_label = ft.Text(f"🔊 Volume Effetti: {int(self.volume_effetti * 100)}%")
        slider_volume_effetti = ft.Slider(
            min=0,
            max=1,
            value=self.volume_effetti,
            divisions=10,
            on_change=self.cambia_volume_effetti,
            tooltip="Regola il volume degli effetti sonori"
        )
        
        # Pulsante test audio
        test_audio_btn = ft.ElevatedButton(
            "🎵 Testa Audio",
            on_click=self.testa_audio,
            width=200,
            tooltip="Riproduci un suono di test",
            data="btn_test_audio"
        )
        
        # Layout impostazioni
        impostazioni_content = ft.Column([
            ft.Text("⚙️ === IMPOSTAZIONI ===", size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Divider(),
            
            ft.Text("🔊 Audio", size=16, weight=ft.FontWeight.BOLD),
            toggle_audio,
            ft.Container(height=10),
            
            self.volume_musica_label,
            slider_volume_musica,
            ft.Container(height=10),
            
            self.volume_effetti_label,
            slider_volume_effetti,
            ft.Container(height=10),
            
            test_audio_btn,
            ft.Divider(),
            
            ft.Text("📳 Feedback", size=16, weight=ft.FontWeight.BOLD),
            toggle_haptic,
            ft.Container(height=20),
            
            ft.ElevatedButton(
                "🔙 Torna al Menu Principale", 
                on_click=self.torna_menu_principale, 
                width=250, 
                height=50, 
                tooltip="Torna al menu principale",
                data="btn_torna_menu"
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
        
        self.container_pulsanti.controls.append(impostazioni_content)
        
        # Rimuovo le funzioni non più necessarie per il menu impostazioni separato
        
    def crea_menu_impostazioni(self):
        """Menu impostazioni rimosso - ora è una tab separata"""
        pass
        
    def vai_a_impostazioni(self, e):
        """Vai al menu impostazioni"""
        self.crea_menu_impostazioni()
        
    def toggle_audio_callback(self, e):
        """Toggle audio"""
        self.audio_abilitato = e.control.value
        if not self.audio_abilitato:
            self.musica_sottofondo.pause()
        else:
            if self.gioco_iniziato:
                self.riavvia_musica_corrente()
                
    def toggle_haptic_callback(self, e):
        """Toggle feedback aptico"""
        self.haptic_abilitato = e.control.value
        if self.haptic_abilitato:
            self.haptic_feedback("light")
            
    def cambia_volume_musica(self, e):
        """Cambia volume musica"""
        self.volume_musica = e.control.value
        self.musica_sottofondo.volume = self.volume_musica
        self.musica_sottofondo.update()
        
        # Aggiorna label se esiste (per compatibilità con vecchi menu)
        if hasattr(self, 'volume_musica_label'):
            self.volume_musica_label.value = f"🎵 Volume Musica: {int(self.volume_musica * 100)}%"
        
        # Aggiorna label nella tab se esiste
        if hasattr(self, 'volume_musica_label_tab'):
            self.volume_musica_label_tab.value = f"🎵 Volume Musica: {int(self.volume_musica * 100)}%"
        
        self.page.update()
            
    def cambia_volume_effetti(self, e):
        """Cambia volume effetti"""
        self.volume_effetti = e.control.value
        self.effetti_sonori.volume = self.volume_effetti
        
        # Aggiorna label se esiste (per compatibilità con vecchi menu)
        if hasattr(self, 'volume_effetti_label'):
            self.volume_effetti_label.value = f"🔊 Volume Effetti: {int(self.volume_effetti * 100)}%"
        
        # Aggiorna label nella tab se esiste  
        if hasattr(self, 'volume_effetti_label_tab'):
            self.volume_effetti_label_tab.value = f"🔊 Volume Effetti: {int(self.volume_effetti * 100)}%"
        
        self.page.update()
        
    def cambia_volume_musica_tab(self, e):
        """Cambia volume musica dalla tab impostazioni (alias per compatibilità)"""
        self.cambia_volume_musica(e)
            
    def cambia_volume_effetti_tab(self, e):
        """Cambia volume effetti dalla tab impostazioni (alias per compatibilità)"""
        self.cambia_volume_effetti(e)
            
    def testa_audio(self, e):
        """Testa audio"""
        if self.audio_abilitato:
            self.riproduci_effetto("vittoria")
            self.haptic_feedback("success")
        
    def torna_menu_principale(self, e):
        """Torna al menu principale"""
        self.gioco_iniziato = False
        if self.audio_abilitato:
            self.musica_sottofondo.pause()
        self.crea_menu_principale_per_tab()
        
    def torna_al_gioco(self, e):
        """Torna al gioco dalla modalità menu"""
        if not self.gioco_iniziato:
            self.torna_menu_principale(e)
            return
            
        self.crea_menu_gioco()
        self.descrivi_situazione_attuale()
        
    def vai_a_inventario(self, e):
        """Vai al menu inventario"""
        self.crea_menu_inventario()
        self.mostra_inventario_dettagliato()
        
    def vai_a_negozio(self, e):
        """Vai al menu negozio"""
        riga, colonna = self.posizione_giocatore
        stanza_attuale = self.mappa[riga][colonna]
        
        if stanza_attuale not in self.negozi:
            self.aggiorna_storia("❌ Nessun negozio qui!")
            self.haptic_feedback("error")
            return
            
        self.crea_menu_negozio()
        self.mostra_negozio_dettagliato()
        
    def vai_a_statistiche(self, e):
        """Vai al menu statistiche"""
        self.crea_menu_statistiche()
        self.mostra_statistiche_dettagliate()
        
    def riavvia_musica_corrente(self):
        """Riavvia musica area corrente"""
        riga, colonna = self.posizione_giocatore
        stanza_attuale = self.mappa[riga][colonna]
        self.cambia_musica_area(stanza_attuale)
        
    def aggiorna_storia(self, testo):
        """Aggiorna testo storia"""
        self.area_storia.value = testo
        self.page.update()
        
    def aggiorna_stats(self, testo):
        """Aggiorna statistiche giocatore"""
        self.area_stats.value = testo
        self.page.update()
        
    def inizia_gioco(self, e):
        """Inizia nuova avventura"""
        self.reset_gioco()
        self.gioco_iniziato = True
        self.crea_menu_gioco()
        
        if self.audio_abilitato:
            self.cambia_musica_area("🏘️ Villaggio")
            
        self.haptic_feedback("success")
        self.descrivi_situazione_attuale()
        
    def descrivi_situazione_attuale(self):
        """Descrizione completa con statistiche separate"""
        riga, colonna = self.posizione_giocatore
        stanza_attuale = self.mappa[riga][colonna]
        
        # Aggiorna statistiche giocatore
        stats = f"📊 Statistiche Giocatore:\n"
        stats += f"👤 Livello {self.livello} • ❤️ {self.hp_giocatore}/{self.hp_max} HP • 💰 {self.monete} monete\n"
        stats += f"⚔️ Attacco: {self.calcola_attacco_totale()} • 🛡️ Difesa: {self.calcola_difesa_totale()}\n"
        stats += f"⭐ EXP: {self.esperienza}/{self.esperienza_prossimo_livello}"
        
        # Effetti attivi nelle stats
        if self.effetti_temporanei:
            stats += f"\n✨ Effetti attivi: {', '.join(self.effetti_temporanei.keys())}"
            
        self.aggiorna_stats(stats)
        
        # Descrizione dell'area
        testo = f"📍 {stanza_attuale}\n\n"
        testo += f"📖 {self.descrizioni[stanza_attuale]}\n\n"
        
        # Oggetti
        if self.oggetti[stanza_attuale]:
            testo += f"✨ Vedi: {self.oggetti[stanza_attuale]}\n"
        
        # Negozi
        if stanza_attuale in self.negozi:
            testo += f"🏪 NEGOZIO DISPONIBILE! Usa il pulsante Negozio per comprare oggetti.\n"
            
        # Mostri
        if self.mostri[stanza_attuale]:
            mostro = self.mostri[stanza_attuale]
            testo += f"⚠️ {mostro['nome']} (Lv.{mostro['livello']}) - HP: {mostro['hp']}\n"
            if self.audio_abilitato:
                self.riproduci_effetto("mostro")
        else:
            testo += "😌 Area sicura.\n"
            
        # Vittoria
        if "👑 corona reale" in self.inventario and "💰 tesoro reale" in self.inventario:
            testo += "\n🎉🏆 HAI COMPLETATO L'AVVENTURA! SEI IL NUOVO RE! 🏆🎉"
            if self.audio_abilitato:
                self.riproduci_effetto("vittoria")
            self.haptic_feedback("success")
            
        self.aggiorna_storia(testo)
        
        # Aggiorna i pulsanti con le opzioni disponibili
        self.crea_menu_gioco()
        
    def muovi(self, direzione):
        """Movimento con controlli migliorati"""
        if not self.gioco_iniziato:
            return
            
        riga, colonna = self.posizione_giocatore
        
        if direzione == "nord" and riga > 0:
            self.posizione_giocatore[0] -= 1
        elif direzione == "sud" and riga < 3:
            self.posizione_giocatore[0] += 1
        elif direzione == "est" and colonna < 3:
            self.posizione_giocatore[1] += 1
        elif direzione == "ovest" and colonna > 0:
            self.posizione_giocatore[1] -= 1
        else:
            self.aggiorna_storia(f"❌ Non puoi andare a {direzione} da qui!")
            self.haptic_feedback("error")
            return
            
        self.haptic_feedback("light")
        self.turno += 1
        
        # Gestisci effetti per turno
        testo_effetti = self.gestisci_effetti_temporanei()
        testo_regen = self.rigenerazione_passiva()
        
        # Cambia musica
        riga, colonna = self.posizione_giocatore
        nuova_stanza = self.mappa[riga][colonna]
        if self.audio_abilitato:
            self.cambia_musica_area(nuova_stanza)
            
        self.descrivi_situazione_attuale()
        
        if testo_effetti or testo_regen:
            self.aggiorna_storia(self.area_storia.value + "\n" + testo_effetti + testo_regen)
        
    def raccogli_oggetto(self, e):
        """Raccolta oggetti migliorata"""
        if not self.gioco_iniziato:
            return
            
        riga, colonna = self.posizione_giocatore
        stanza_attuale = self.mappa[riga][colonna]
        
        if self.oggetti[stanza_attuale]:
            oggetto = self.oggetti[stanza_attuale]
            self.inventario.append(oggetto)
            self.oggetti[stanza_attuale] = ""
            
            # Monete bonus per oggetti speciali
            if "💎" in oggetto or "👑" in oggetto:
                bonus = random.randint(20, 50)
                self.monete += bonus
                testo = f"✅ Hai raccolto: {oggetto}!\n💰 Bonus: +{bonus} monete!"
            else:
                testo = f"✅ Hai raccolto: {oggetto}!"
                
            self.haptic_feedback("success")
            if self.audio_abilitato:
                self.riproduci_effetto("raccogli")
                
            self.aggiorna_storia(testo)
            # Aggiorna i pulsanti dopo aver raccolto
            self.crea_menu_gioco()
        else:
            testo = "❌ Niente da raccogliere qui."
            self.haptic_feedback("warning")
            self.aggiorna_storia(testo)
        
    def mostra_inventario_dettagliato(self):
        """Inventario dettagliato per il menu"""
        testo = "🎒 === INVENTARIO ===\n\n"
        
        if self.inventario:
            testo += "📦 Oggetti:\n"
            for i, oggetto in enumerate(self.inventario, 1):
                testo += f"{i}. {oggetto}\n"
        else:
            testo += "📦 Inventario vuoto.\n"
            
        testo += f"\n⚔️ === EQUIPAGGIAMENTO ===\n"
        testo += f"🗡️ Arma: {self.equipaggiamento['arma'] or 'Nessuna'}\n"
        testo += f"🛡️ Armatura: {self.equipaggiamento['armatura'] or 'Nessuna'}\n" 
        testo += f"💍 Accessorio: {self.equipaggiamento['accessorio'] or 'Nessuno'}\n"
        
        self.aggiorna_storia(testo)
        
    def equipaggia_oggetto(self, e):
        """Sistema di equipaggiamento"""
        if not self.gioco_iniziato:
            return
            
        if not self.inventario:
            self.aggiorna_storia("❌ Inventario vuoto!")
            return
            
        testo = "⚔️ EQUIPAGGIA OGGETTO:\n\n"
        
        oggetti_equipaggiabili = []
        for i, oggetto in enumerate(self.inventario):
            if any(keyword in oggetto for keyword in ["Spada", "Arco", "Pugnale"]):
                tipo = "arma"
            elif any(keyword in oggetto for keyword in ["Armatura", "Scudo"]):
                tipo = "armatura" 
            elif any(keyword in oggetto for keyword in ["Anello"]):
                tipo = "accessorio"
            else:
                continue
                
            oggetti_equipaggiabili.append((i, oggetto, tipo))
            
        if not oggetti_equipaggiabili:
            testo += "❌ Nessun oggetto equipaggiabile nell'inventario."
        else:
            # Equipaggia automaticamente il primo oggetto equipaggiabile
            indice, oggetto, tipo = oggetti_equipaggiabili[0]
            
            # Rimetti nell'inventario l'oggetto precedente
            if self.equipaggiamento[tipo]:
                self.inventario.append(self.equipaggiamento[tipo])
                
            # Equipaggia il nuovo oggetto
            self.equipaggiamento[tipo] = oggetto
            self.inventario.pop(indice)
            
            testo += f"✅ Equipaggiato: {oggetto} ({tipo})\n"
            testo += f"⚔️ Nuovo attacco: {self.calcola_attacco_totale()}\n"
            testo += f"🛡️ Nuova difesa: {self.calcola_difesa_totale()}"
            
            self.haptic_feedback("success")
            # Aggiorna i pulsanti dopo equipaggiamento
            self.crea_menu_inventario()
            
        self.aggiorna_storia(testo)
        
    def usa_oggetto(self, e):
        """Sistema uso oggetti (pozioni, cibo)"""
        if not self.gioco_iniziato:
            return
            
        if not self.inventario:
            self.aggiorna_storia("❌ Inventario vuoto!")
            return
            
        # Trova primo oggetto usabile
        oggetto_usato = None
        for i, oggetto in enumerate(self.inventario):
            if any(keyword in oggetto for keyword in ["Pozione", "Pane", "Mela", "erba"]):
                oggetto_usato = (i, oggetto)
                break
                
        if not oggetto_usato:
            self.aggiorna_storia("❌ Nessun oggetto usabile nell'inventario!")
            return
            
        indice, oggetto = oggetto_usato
        self.inventario.pop(indice)
        
        testo = f"🧪 Usi: {oggetto}\n"
        
        # Effetti oggetti
        if "Pozione Vita" in oggetto:
            guarigione = 50
            self.hp_giocatore = min(self.hp_max, self.hp_giocatore + guarigione)
            testo += f"❤️ Ripristini {guarigione} HP!"
        elif "Pozione Forza" in oggetto:
            self.effetti_temporanei["forza"] = 3
            testo += f"💪 +10 attacco per 3 turni!"
        elif "Pane" in oggetto:
            guarigione = 15
            self.hp_giocatore = min(self.hp_max, self.hp_giocatore + guarigione)
            testo += f"🍞 Ripristini {guarigione} HP!"
        elif "Mela" in oggetto:
            guarigione = 10
            self.hp_giocatore = min(self.hp_max, self.hp_giocatore + guarigione)
            testo += f"🍎 Ripristini {guarigione} HP!"
        elif "erba medicinale" in oggetto:
            guarigione = 25
            self.hp_giocatore = min(self.hp_max, self.hp_giocatore + guarigione)
            testo += f"🌿 Ripristini {guarigione} HP!"
            
        self.haptic_feedback("success")
        self.aggiorna_storia(testo)
        # Aggiorna i pulsanti dopo uso oggetto
        self.crea_menu_inventario()
        
    def mostra_negozio_dettagliato(self):
        """Mostra dettagli negozio"""
        riga, colonna = self.posizione_giocatore
        stanza_attuale = self.mappa[riga][colonna]
        
        if stanza_attuale not in self.negozi:
            self.aggiorna_storia("❌ Nessun negozio qui!")
            return
            
        negozio = self.negozi[stanza_attuale]
        
        testo = f"🏪 === NEGOZIO {stanza_attuale} ===\n"
        testo += f"💰 Le tue monete: {self.monete}\n\n"
        
        testo += "📋 OGGETTI DISPONIBILI:\n"
        for nome, info in negozio.items():
            disponibile = "✅" if self.monete >= info["prezzo"] else "❌"
            testo += f"{disponibile} {nome} - {info['prezzo']} monete\n"
            testo += f"   📝 {info['descrizione']}\n\n"
            
        self.aggiorna_storia(testo)
        
    def compra_oggetto(self, e):
        """Sistema acquisti negozio"""
        if not self.gioco_iniziato:
            return
            
        riga, colonna = self.posizione_giocatore
        stanza_attuale = self.mappa[riga][colonna]
        
        if stanza_attuale not in self.negozi:
            self.aggiorna_storia("❌ Nessun negozio qui!")
            return
            
        negozio = self.negozi[stanza_attuale]
        
        # Compra automaticamente l'oggetto più economico che puoi permetterti
        oggetti_acquistabili = []
        for nome, info in negozio.items():
            if self.monete >= info["prezzo"]:
                oggetti_acquistabili.append((nome, info))
                
        if not oggetti_acquistabili:
            testo = "❌ Non hai abbastanza monete per comprare nulla!"
        else:
            # Compra l'oggetto più economico
            nome_oggetto, info = min(oggetti_acquistabili, key=lambda x: x[1]["prezzo"])
            
            self.monete -= info["prezzo"]
            self.inventario.append(nome_oggetto)
            
            testo = f"✅ Acquistato: {nome_oggetto}\n"
            testo += f"💰 Costo: {info['prezzo']} monete\n"
            testo += f"📝 {info['descrizione']}\n"
            testo += f"💰 Monete rimaste: {self.monete}"
            
            self.haptic_feedback("success")
            if self.audio_abilitato:
                self.riproduci_effetto("monete")
            
            # Aggiorna i pulsanti dopo acquisto
            self.crea_menu_negozio()
                
        self.aggiorna_storia(testo)
        
    def mostra_statistiche_dettagliate(self):
        """Statistiche complete del giocatore"""
        testo = f"📊 === STATISTICHE GIOCATORE ===\n\n"
        testo += f"👤 Livello: {self.livello}\n"
        testo += f"❤️ HP: {self.hp_giocatore}/{self.hp_max}\n"
        testo += f"⭐ Esperienza: {self.esperienza}/{self.esperienza_prossimo_livello}\n"
        testo += f"⚔️ Attacco: {self.calcola_attacco_totale()} (base: {self.attacco_base})\n"
        testo += f"🛡️ Difesa: {self.calcola_difesa_totale()}\n"
        testo += f"💰 Monete: {self.monete}\n"
        testo += f"🎒 Oggetti inventario: {len(self.inventario)}\n"
        testo += f"🕐 Turni giocati: {self.turno}\n\n"
        
        if self.effetti_temporanei:
            testo += f"✨ Effetti attivi:\n"
            for effetto, turni in self.effetti_temporanei.items():
                testo += f"• {effetto}: {turni} turni\n"
        else:
            testo += "✨ Nessun effetto attivo\n"
            
        self.aggiorna_storia(testo)
        
    def attacca_mostro(self, e):
        """Sistema di combattimento avanzato"""
        if not self.gioco_iniziato:
            return
            
        riga, colonna = self.posizione_giocatore
        stanza_attuale = self.mappa[riga][colonna]
        
        if not self.mostri[stanza_attuale]:
            self.aggiorna_storia("❌ Nessun mostro da attaccare!")
            self.haptic_feedback("error")
            return
            
        mostro = self.mostri[stanza_attuale]
        testo = f"⚔️ COMBATTIMENTO vs {mostro['nome']}\n\n"
        
        self.haptic_feedback("heavy")
        if self.audio_abilitato:
            self.riproduci_effetto("attacco")
        
        # Attacco del giocatore
        danno_inflitto = max(1, self.calcola_attacco_totale() - (mostro.get("difesa", 0)))
        mostro['hp'] -= danno_inflitto
        testo += f"💥 Infliggi {danno_inflitto} danni!\n"
        
        if mostro['hp'] <= 0:
            # Vittoria!
            testo += f"🎉 Hai sconfitto {mostro['nome']}!\n"
            
            # Ricompense
            exp_guadagnata = mostro['exp']
            monete_guadagnate = random.randint(10, 30)
            
            self.esperienza += exp_guadagnata
            self.monete += monete_guadagnate
            
            testo += f"⭐ +{exp_guadagnata} EXP\n"
            testo += f"💰 +{monete_guadagnate} monete\n"
            
            # Controlla livello
            testo_livello = self.gestisci_livello()
            if testo_livello:
                testo += "\n" + testo_livello
                
            self.mostri[stanza_attuale] = None
            self.haptic_feedback("success")
            if self.audio_abilitato:
                self.riproduci_effetto("vittoria")
                
            # Aggiorna i pulsanti dopo aver sconfitto il mostro
            self.aggiorna_storia(testo)
            self.crea_menu_gioco()
        else:
            # Mostro contrattacca
            testo += f"👹 {mostro['nome']} ha {mostro['hp']} HP rimasti\n"
            
            danno_subito = max(1, mostro['attacco'] - self.calcola_difesa_totale())
            self.hp_giocatore -= danno_subito
            testo += f"💢 {mostro['nome']} ti infligge {danno_subito} danni!\n"
            testo += f"❤️ HP: {self.hp_giocatore}/{self.hp_max}"
            
            self.haptic_feedback("medium")
            
            if self.hp_giocatore <= 0:
                testo += "\n\n💀 SEI STATO SCONFITTO! GAME OVER 💀"
                self.haptic_feedback("error")
                if self.audio_abilitato:
                    self.riproduci_effetto("sconfitta")
                    self.musica_sottofondo.pause()
                self.gioco_iniziato = False
                self.aggiorna_storia(testo)
                self.crea_menu_principale()
                return
                
            self.aggiorna_storia(testo)
        
    def salva_gioco(self, e):
        """Salvataggio completo"""
        if not self.gioco_iniziato:
            return
            
        stato_gioco = {
            "posizione_giocatore": self.posizione_giocatore,
            "hp_giocatore": self.hp_giocatore,
            "hp_max": self.hp_max,
            "livello": self.livello,
            "esperienza": self.esperienza,
            "esperienza_prossimo_livello": self.esperienza_prossimo_livello,
            "attacco_base": self.attacco_base,
            "difesa": self.difesa,
            "monete": self.monete,
            "inventario": self.inventario,
            "equipaggiamento": self.equipaggiamento,
            "effetti_temporanei": self.effetti_temporanei,
            "oggetti": self.oggetti,
            "mostri": self.mostri,
            "turno": self.turno,
            "audio_abilitato": self.audio_abilitato,
            "haptic_abilitato": self.haptic_abilitato,
            "volume_musica": self.volume_musica,
            "volume_effetti": self.volume_effetti
        }
        
        try:
            with open("avventura_epica_save.json", "w") as file:
                json.dump(stato_gioco, file, indent=2)
            self.aggiorna_storia("💾 Avventura salvata con successo!")
            self.haptic_feedback("success")
        except Exception as ex:
            self.aggiorna_storia(f"❌ Errore salvataggio: {str(ex)}")
            
    def carica_gioco(self, e):
        """Caricamento completo"""
        if not os.path.exists("avventura_epica_save.json"):
            self.aggiorna_storia("❌ Nessun salvataggio trovato!")
            return
            
        try:
            with open("avventura_epica_save.json", "r") as file:
                stato_gioco = json.load(file)
                
            # Ripristina tutti i dati
            self.posizione_giocatore = stato_gioco["posizione_giocatore"]
            self.hp_giocatore = stato_gioco["hp_giocatore"]
            self.hp_max = stato_gioco.get("hp_max", 100)
            self.livello = stato_gioco.get("livello", 1)
            self.esperienza = stato_gioco.get("esperienza", 0)
            self.esperienza_prossimo_livello = stato_gioco.get("esperienza_prossimo_livello", 100)
            self.attacco_base = stato_gioco.get("attacco_base", 15)
            self.difesa = stato_gioco.get("difesa", 0)
            self.monete = stato_gioco.get("monete", 100)
            self.inventario = stato_gioco["inventario"]
            self.equipaggiamento = stato_gioco.get("equipaggiamento", {"arma": None, "armatura": None, "accessorio": None})
            self.effetti_temporanei = stato_gioco.get("effetti_temporanei", {})
            self.oggetti = stato_gioco["oggetti"]
            self.mostri = stato_gioco["mostri"]
            self.turno = stato_gioco.get("turno", 0)
            
            # Ripristina impostazioni audio
            if "audio_abilitato" in stato_gioco:
                self.audio_abilitato = stato_gioco["audio_abilitato"]
                
            if "haptic_abilitato" in stato_gioco:
                self.haptic_abilitato = stato_gioco["haptic_abilitato"]
                
            if "volume_musica" in stato_gioco:
                self.volume_musica = stato_gioco["volume_musica"]
                self.musica_sottofondo.volume = self.volume_musica
                
            if "volume_effetti" in stato_gioco:
                self.volume_effetti = stato_gioco["volume_effetti"]
                self.effetti_sonori.volume = self.volume_effetti
            
            self.gioco_iniziato = True
            self.crea_menu_gioco()
            
            if self.audio_abilitato:
                self.riavvia_musica_corrente()
            
            self.haptic_feedback("success")
            self.aggiorna_storia("📂 Avventura caricata con successo!")
            self.descrivi_situazione_attuale()
            
        except Exception as ex:
            self.aggiorna_storia(f"❌ Errore caricamento: {str(ex)}")

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.window_width = 1000
    page.window_height = 800
    page.window_resizable = True
    
    # Inizializza l'avventura epica
    gioco = AvventuraEpica(page)

if __name__ == "__main__":
    ft.app(target=main)
 