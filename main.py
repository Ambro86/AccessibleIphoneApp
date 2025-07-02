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
        self.app_inizializzata = False  # Flag per evitare suoni durante init
        self.inizializza_gioco()
        self.crea_audio_system()
        self.crea_ui()
        self.app_inizializzata = True  # Ora l'app è pronta
        

    def analizza_accessibilita(self, view):
        return  # DEBUG TEMPORANEAMENTE DISABILITATO
        print(f"\n🔍 ========== ANALISI ACCESSIBILITÀ ==========\n🎯 VIEW: {view.route}\n📱 PIATTAFORMA: {self.page.platform}")
        
        # Statistiche generali
        problemi_totali = []
        elementi_totali = 0
        
        for idx, control in enumerate(view.controls):
            problemi = self._analizza_control(control, path=f"root[{idx}]", problemi=[])
            problemi_totali.extend(problemi)
            elementi_totali += self._conta_elementi(control)
        
        # Riepilogo finale
        print(f"\n📊 RIEPILOGO ACCESSIBILITÀ:")
        print(f"🔢 Elementi totali: {elementi_totali}")
        print(f"⚠️  Problemi trovati: {len(problemi_totali)}")
        
        if problemi_totali:
            print(f"\n❌ PROBLEMI CRITICI DA RISOLVERE:")
            for i, problema in enumerate(problemi_totali, 1):
                if isinstance(problema, dict):
                    print(f"\n   {i}. 📍 POSIZIONE: {problema['path']}")
                    print(f"      🏷️  TIPO: {problema['tipo']} - {problema['descrizione']}")
                    print(f"      🔧 SOLUZIONE: {problema['raccomandazione']}")
                    print(f"      ♿ PERCHÉ: {problema['impatto_accessibilita']}")
                else:
                    print(f"   {i}. {problema}")
            print(f"\n🎯 PRIORITÀ: Risolvi questi problemi per migliorare l'accessibilità della view '{view.route}'")
        else:
            print(f"✅ OTTIMO: Nessun problema di accessibilità rilevato!")
        
        print(f"\n🔍 ========================================\n")
        
        # Stampa ordine di lettura
        print("\n📐 ORDINE VISIVO E DI LETTURA:")
        for c in view.controls:
            self._stampa_ordine_lettura(c)

    def _analizza_control(self, control, path, problemi=None):
        if problemi is None:
            problemi = []
            
        # Controlli vuoti rilevanti
        vuoto = False
        raccomandazione = ""
        
        if isinstance(control, ft.Text):
            if not control.value or not control.value.strip():
                vuoto = True
                raccomandazione = "TEXT VUOTO - Aggiungi valore al text o rimuovi l'elemento"
        elif isinstance(control, ft.Container):
            if not control.content:
                vuoto = True
                raccomandazione = self._genera_raccomandazione_container(control, path)
        elif isinstance(control, (ft.Column, ft.Row)):
            if not getattr(control, 'controls', []):
                vuoto = True
                raccomandazione = f"Rimuovi {type(control).__name__} vuoto o aggiungi elementi"
        elif isinstance(control, ft.TextField):
            if not control.value and not control.label and not control.hint_text:
                vuoto = True
                raccomandazione = "Aggiungi label, hint_text o valore iniziale"
        elif isinstance(control, ft.ElevatedButton):
            if not control.text and not control.content:
                vuoto = True
                raccomandazione = "Aggiungi text o content al button"
        elif isinstance(control, ft.Card):
            if not control.content:
                vuoto = True
                raccomandazione = "Aggiungi content alla Card o rimuovila"
        
        if vuoto:
            problema = {
                'path': path,
                'tipo': type(control).__name__,
                'descrizione': f"{type(control).__name__} vuoto",
                'raccomandazione': raccomandazione,
                'impatto_accessibilita': self._spiega_impatto_accessibilita(control)
            }
            problemi.append(problema)
            print(f"⚠️  {path} → {type(control).__name__}: {problema['descrizione']}")
            print(f"🔧 SOLUZIONE: {raccomandazione}")
            print(f"♿ IMPATTO: {problema['impatto_accessibilita']}")
        
        # Verifica problemi di accessibilità aggiuntivi
        self._verifica_accessibilita_specifica(control, path, problemi)
        
        # Analizza figli
        if hasattr(control, 'content') and control.content:
            self._analizza_control(control.content, path + ".content", problemi)
        if hasattr(control, 'controls') and control.controls:
            for i, c in enumerate(control.controls):
                self._analizza_control(c, f"{path}.controls[{i}]", problemi)
                
        return problemi
    
    def _genera_raccomandazione_container(self, control, path):
        """Genera raccomandazione specifica per Container vuoti"""
        # Controlla se è un spaziatore (ha solo height)
        if hasattr(control, 'height') and control.height and not control.width:
            spacing_value = int(control.height * 1.5) if isinstance(control.height, (int, float)) else 30
            return f"SPAZIATORE VUOTO - Rimuovi 'ft.Container(height={control.height})' e aumenta spacing del parent Column/Row a {spacing_value}"
        elif hasattr(control, 'width') and control.width and not control.height:
            return f"SPAZIATORE VUOTO - Rimuovi 'ft.Container(width={control.width})' e usa padding o margin"
        else:
            return "CONTAINER VUOTO - Aggiungi content o rimuovi completamente"
    
    def _spiega_impatto_accessibilita(self, control):
        """Spiega perché l'elemento vuoto è problematico per l'accessibilità"""
        if isinstance(control, ft.Container):
            return "Screen reader si confonde con elementi vuoti, crea navigazione inconsistente"
        elif isinstance(control, ft.Text):
            return "Text vuoto causa pause confuse nella lettura dello screen reader"
        elif isinstance(control, (ft.Column, ft.Row)):
            return "Layout vuoto può causare problemi di focus e navigazione"
        else:
            return "Elemento vuoto può confondere gli utenti con disabilità visive"
    
    def _verifica_accessibilita_specifica(self, control, path, problemi):
        """Verifica problemi specifici di accessibilità"""
        
        # Verifica bottoni senza tooltip
        if isinstance(control, (ft.ElevatedButton, ft.TextButton, ft.IconButton)):
            if not getattr(control, 'tooltip', None):
                problema = {
                    'path': path,
                    'tipo': type(control).__name__,
                    'descrizione': 'Manca tooltip',
                    'raccomandazione': f"Aggiungi tooltip=\"Descrizione azione\" al button",
                    'impatto_accessibilita': 'Utenti screen reader non capiscono la funzione del button'
                }
                problemi.append(problema)
                print(f"💡 {path} → {type(control).__name__}: Manca tooltip")
                print(f"🔧 SOLUZIONE: {problema['raccomandazione']}")
        
        # Verifica immagini senza semantics
        if isinstance(control, ft.Image):
            if not getattr(control, 'semantics_label', None):
                problema = {
                    'path': path,
                    'tipo': 'Image',
                    'descrizione': 'Manca semantics_label',
                    'raccomandazione': 'Aggiungi semantics_label="Descrizione immagine"',
                    'impatto_accessibilita': 'Screen reader non può descrivere l\'immagine agli utenti non vedenti'
                }
                problemi.append(problema)
                print(f"🖼️  {path} → Image: Manca semantics_label")
                print(f"🔧 SOLUZIONE: {problema['raccomandazione']}")
        
        # Verifica testi troppo piccoli
        if isinstance(control, ft.Text):
            size = getattr(control, 'size', 14)
            if size is not None and size < 12:
                problema = {
                    'path': path,
                    'tipo': 'Text',
                    'descrizione': f'Testo troppo piccolo ({size}px)',
                    'raccomandazione': f'Aumenta size a minimo 12px (raccomandato 14px+)',
                    'impatto_accessibilita': 'Testo piccolo difficile da leggere per utenti ipovedenti'
                }
                problemi.append(problema)
                print(f"📏 {path} → Text: Dimensione troppo piccola ({size}px)")
                print(f"🔧 SOLUZIONE: {problema['raccomandazione']}")
    
    def _conta_elementi(self, control):
        """Conta il numero totale di elementi UI"""
        count = 1
        
        if hasattr(control, 'content') and control.content:
            count += self._conta_elementi(control.content)
        if hasattr(control, 'controls') and control.controls:
            for c in control.controls:
                count += self._conta_elementi(c)
                
        return count

    def _stampa_ordine_lettura(self, control, depth=0):
        indent = "  " * depth
        if isinstance(control, ft.Text):
            descr = f'Text: "{control.value}"'
        elif isinstance(control, ft.Container):
            descr = f'Container: height={control.height}, width={control.width}'
        elif isinstance(control, ft.Column):
            descr = "Column"
        elif isinstance(control, ft.Row):
            descr = "Row"
        else:
            descr = control.__class__.__name__
        
        print(f"{indent}- {descr}")
        
        # Analizza figli
        if hasattr(control, 'content') and control.content:
            self._stampa_ordine_lettura(control.content, depth + 1)
        if hasattr(control, 'controls') and control.controls:
            for c in control.controls:
                self._stampa_ordine_lettura(c, depth + 1)

    def inizializza_gioco(self):
        # Nuove aree con progressione lineare + area segreta
        self.aree_ordinate = [
            "Villaggio",
            "🏠 Cantina", 
            "🚰 Fogne",
            "🌀 Labirinto Antico",
            "❄️ Area Innevata",
            "🌿 Giungla Selvaggia",
            "🌲 Bosco Profondo",
            "⚰️ Cimitero",
            "🏚️ Casa degli Orrori",
            "🏭 Fabbrica Abbandonata",
            "⛏️ Miniera Profonda",
            "🌙 Cripta Maledetta",
            "🌊 Mare",
            "🏔️ Montagna Sacra",
            "🌋 Vulcano Attivo",
            "👑 Palazzo Finale"
        ]
        
        # Modalità rinomina
        self.modalita_rinomina = False
        self.gatto_da_rinominare = None
        
        #  Sistema incrementale con gatti e risorse
        self.aree_sbloccate = ["Villaggio"]
        self.area_attuale = "Villaggio"
        self.progressione_area = {area: 0 for area in self.aree_ordinate}
        
        # Sistema di navigazione a schermate
        self.schermata_corrente = "menu_principale"
        self.stack_schermate = []
        
        # Traccia boss notifications già mostrate
        self.boss_notifications_mostrate = set()
        
        # Stato combattimento
        self.in_combattimento = False
        self.mostro_attuale = None
        self.hp_mostro_attuale = 0
        self.round_combattimento = 0
        
        #  Sistema gatti con nomi personalizzabili e affinità
        self.gatti = {
            "gatto_1": {
                "nome": "Micio", "emoji": "", "livello": 1, "attacco": 5, 
                "abilita": "raccolta", "fame": 100, "felicita": 100, "sbloccato": True,
                "affinita": 30, "nome_personalizzato": False, "aree_non_usato": 0,
                "forma_evoluta": False, "dialoghi_sbloccati": [], "scene_viste": []
            },
            "gatto_2": {
                "nome": "Shadow", "emoji": "🐾", "livello": 0, "attacco": 8, 
                "abilita": "combattimento", "fame": 0, "felicita": 0, "sbloccato": False,
                "affinita": 0, "nome_personalizzato": False, "aree_non_usato": 0,
                "forma_evoluta": False, "dialoghi_sbloccati": [], "scene_viste": []
            },
            "gatto_3": {
                "nome": "Luna", "emoji": "😻", "livello": 0, "attacco": 3, 
                "abilita": "guarigione", "fame": 0, "felicita": 0, "sbloccato": False,
                "affinita": 0, "nome_personalizzato": False, "aree_non_usato": 0,
                "forma_evoluta": False, "dialoghi_sbloccati": [], "scene_viste": []
            },
            "gatto_4": {
                "nome": "Stella", "emoji": "", "livello": 0, "attacco": 6, 
                "abilita": "partner", "fame": 0, "felicita": 0, "sbloccato": False,
                "affinita": 0, "nome_personalizzato": False, "aree_non_usato": 0,
                "forma_evoluta": False, "dialoghi_sbloccati": [], "scene_viste": []
            },
            "gatto_5": {
                "nome": "Nox", "emoji": "🌌", "livello": 0, "attacco": 10, 
                "abilita": "riavvolgi", "fame": 100, "felicita": 100, "sbloccato": False,
                "affinita": 0, "nome_personalizzato": False, "aree_non_usato": 0,
                "forma_evoluta": False, "dialoghi_sbloccati": [], "scene_viste": []
            }
        }
        self.gatto_attivo = "gatto_1"
        
        #  Sistema risorse
        self.risorse = {
            "cibo": 50,
            "acqua": 50,
            "legno": 0,
            "pietra": 0,
            "ferro": 0,
            "energia": 100,
            "pozioni": 100  # Aggiungiamo pozioni per test
        }
        
        # Sistema di progressione con chiavi e boss
        self.chiavi_raccolte = []
        self.boss_sconfitti = []
        
        # Area segreta endgame
        self.area_segreta = "🌌 Regno dei Sogni"
        self.portale_sogni_sbloccato = False
        self.pesci_magici_rari = 0
        self.finale_alternativo_raggiunto = False
        
        # Aree speciali con pesce per gatti
        self.pesce_raccolto = 0
        self.casa_nel_bosco_costruita = False
        
        # Sistema scelte oniriche
        self.scelte_oniriche = []
        self.forma_regno_sogni = "neutrale"
        self.riavvolgimenti_disponibili = 0
        
        # 🔮 Sistema Reliquie Antiche
        self.reliquie_possedute = []
        self.reliquie_equipaggiate = {"slot_1": None, "slot_2": None, "slot_3": None}
        self.reliquie_scoperte = []  # Per album collezione
        self.mini_dungeon_completati = []
        self.npc_rari_incontrati = []
        
        #  Sistema Affinità e Legame Emotivo
        self.affinita_milestone = {50: "💛", 100: "💚", 150: "💙", 200: ""}
        self.ultimo_gatto_usato = None
        self.turni_in_area = 0
        
        # 🏚️ Sistema Sanità Mentale (per Casa degli Orrori)
        self.sanita_mentale = 100
        self.eventi_orrore_visti = []
        
        # Database evoluzione gatti
        self.gatti_evoluzione = {
            "gatto_1": {
                "nome_evoluto": " Micio Stellare", 
                "abilita_evoluta": "raccolta_suprema",
                "bonus_passivo": "schivata_5",
                "storia": "Micio rivela di essere un antico guardiano delle stelle, caduto sulla Terra per proteggere i tesori perduti.",
                "dialoghi": ["💭 Sento l'energia delle stelle antiche...", "💭 Insieme possiamo trovare tesori nascosti!", "💭 Le costellazioni mi guidano verso i segreti."]
            },
            "gatto_2": {
                "nome_evoluto": " Shadow Tempesta", 
                "abilita_evoluta": "combattimento_fulmineo",
                "bonus_passivo": "critico_15",
                "storia": "Shadow era un guerriero leggendario in una vita passata, ora risveglia la sua vera natura combattiva.",
                "dialoghi": ["💭 La battaglia scorre nelle mie vene!", "💭 Nessun nemico può resistere alla tempesta!", "💭 I miei artigli portano il tuono!"]
            },
            "gatto_3": {
                "nome_evoluto": "🌙 Luna Celestiale", 
                "abilita_evoluta": "guarigione_celestiale",
                "bonus_passivo": "luce_nelle_tenebre",
                "storia": "Luna ha curato innumerevoli creature perdute. Il suo sogno è creare un santuario di pace per tutti gli esseri feriti.",
                "dialoghi": ["💭 La luna mi dona la forza di guarire...", "💭 Ogni creatura merita compassione e cure.", "💭 Insieme porteremo pace in questo mondo."]
            },
            "gatto_4": {
                "nome_evoluto": "💫 Stella Cosmica", 
                "abilita_evoluta": "partnership_galattica",
                "bonus_passivo": "sincronia_perfetta",
                "storia": "Stella è un essere cosmico che viaggia tra le dimensioni, legandosi ai compagni più coraggiosi.",
                "dialoghi": ["💭 Il nostro legame trascende lo spazio-tempo!", "💭 Insieme possiamo superare ogni ostacolo.", "💭 La partnership perfetta è la nostra forza!"]
            },
            "gatto_5": {
                "nome_evoluto": "🌌 Nox Eterno", 
                "abilita_evoluta": "controllo_temporale",
                "bonus_passivo": "manipolazione_destino",
                "storia": "Nox è il custode del tempo stesso, capace di vedere tutti i possibili futuri e scegliere il migliore.",
                "dialoghi": ["💭 Ho visto infinite linee temporali...", "💭 Il passato e il futuro si intrecciano.", "💭 Insieme riscriveremo il destino!"]
            }
        }
        
        # Database reliquie con effetti unici
        self.reliquie_database = {
            "Braciere di Fuoco Antico": {
                "tipo": "passivo",
                "effetto": "undead_damage",
                "valore": 10,
                "descrizione": "+10 attacco contro boss non morti",
                "rarita": "epico",
                "origine": "boss_speciale"
            },
            "🌕 Specchio Lunare": {
                "tipo": "attivabile",
                "effetto": "rifletti_attacco",
                "valore": 1,
                "descrizione": "Una volta per battaglia: riflette un attacco al mittente",
                "rarita": "leggendario",
                "origine": "mini_dungeon"
            },
            "🌿 Gemma della Foresta": {
                "tipo": "passivo",
                "effetto": "regen_gatti",
                "valore": 2,
                "descrizione": "I gatti guariscono 2 HP ogni turno",
                "rarita": "raro",
                "origine": "npc_raro"
            },
            " Artiglio Dorato": {
                "tipo": "passivo",
                "effetto": "critico_gatti",
                "valore": 15,
                "descrizione": "+15% critico per i gatti da combattimento",
                "rarita": "epico",
                "origine": "boss_speciale"
            },
            "🕯️ Candela delle Anime": {
                "tipo": "passivo",
                "effetto": "boost_partner",
                "valore": 25,
                "descrizione": "Aumenta l'efficacia delle abilità partner e guarigione",
                "rarita": "raro",
                "origine": "puzzle"
            },
            "🐾 Amuleto dei Gatti Perduti": {
                "tipo": "passivo",
                "effetto": "exp_felicita_gatti",
                "valore": 50,
                "descrizione": "Aumenta felicità e esperienza dei gatti del 50%",
                "rarita": "leggendario",
                "origine": "quest_secondaria"
            },
            "💎 Cristallo dell'Eternità": {
                "tipo": "attivabile",
                "effetto": "resurrezione",
                "valore": 1,
                "descrizione": "Una volta per avventura: resuscita con metà HP",
                "rarita": "leggendario",
                "origine": "finale_segreto"
            },
            "🌊 Perla delle Profondità": {
                "tipo": "passivo",
                "effetto": "doppio_pesce",
                "valore": 100,
                "descrizione": "Doppia quantità di pesce quando peschi",
                "rarita": "epico",
                "origine": "mare_profondo"
            },
            "🗡️ Lama Spettrale": {
                "tipo": "passivo",
                "effetto": "danno_fantasmi",
                "valore": 20,
                "descrizione": "+20 danno contro demoni e spiriti",
                "rarita": "epico",
                "origine": "cimitero_segreto"
            },
            " Stella Cadente": {
                "tipo": "attivabile",
                "effetto": "attacco_devastante",
                "valore": 3,
                "descrizione": "3 usi: attacco devastante che ignora difese",
                "rarita": "leggendario",
                "origine": "cielo_notturno"
            },
            "🌀 Bussola del Labirinto": {
                "tipo": "passivo",
                "effetto": "anti_teletrasporto",
                "valore": 100,
                "descrizione": "Immunità al teletrasporto nemico e +20% successo esplorazione",
                "rarita": "epico",
                "origine": "labirinto_antico"
            },
            "🌿 Zanna Primordiale": {
                "tipo": "passivo",
                "effetto": "danno_bestie",
                "valore": 25,
                "descrizione": "+25 danno contro creature preistoriche e bestie",
                "rarita": "epico",
                "origine": "giungla_selvaggia"
            },
            "🏭 Nucleo Energetico": {
                "tipo": "attivabile",
                "effetto": "ricarica_totale",
                "valore": 2,
                "descrizione": "2 usi: ripristina completamente energia e risorse",
                "rarita": "leggendario",
                "origine": "fabbrica_abbandonata"
            },
            "⛏️ Piccone di Diamante": {
                "tipo": "passivo",
                "effetto": "raccolta_cristalli",
                "valore": 200,
                "descrizione": "Doppi cristalli raccolti e +30% chance di gemme rare",
                "rarita": "epico",
                "origine": "miniera_profonda"
            },
            "🏔️ Benedizione Angelica": {
                "tipo": "passivo",
                "effetto": "protezione_divina",
                "valore": 20,
                "descrizione": "20% chance di annullare completamente un attacco",
                "rarita": "leggendario",
                "origine": "montagna_sacra"
            },
            "🌋 Cuore di Magma": {
                "tipo": "passivo",
                "effetto": "danno_fuoco",
                "valore": 30,
                "descrizione": "+30 danno da fuoco e immunità ai danni da calore",
                "rarita": "leggendario",
                "origine": "vulcano_attivo"
            },
            "🏚️ Amuleto Anti-Paura": {
                "tipo": "passivo",
                "effetto": "resistenza_terrore",
                "valore": 75,
                "descrizione": "75% resistenza agli effetti di paura e terrore",
                "rarita": "epico",
                "origine": "casa_orrori"
            },
            "👻 Cattura Fantasmi": {
                "tipo": "attivabile",
                "effetto": "intrappola_spiriti",
                "valore": 3,
                "descrizione": "3 usi: intrappola temporaneamente nemici spettrali",
                "rarita": "leggendario",
                "origine": "casa_orrori"
            }
        }
        
        # Boss per ogni area con meccaniche uniche
        self.boss_aree = {
            "Villaggio": {
                "nome": "🐕 Cane Randagio", "hp": 180, "attacco": 40, "exp": 75,
                "chiave": "🗝️ Chiave della Cantina", "abilita_speciale": "morso_feroce"
            },
            "🏠 Cantina": {
                "nome": "🐁 Re Ratto", "hp": 240, "attacco": 50, "exp": 100,
                "chiave": "🗝️ Chiave della Cantina", "abilita_speciale": "richiama_ratti"
            },
            "🚰 Fogne": {
                "nome": "🐀 Boss Topo delle Fogne", "hp": 360, "attacco": 65, "exp": 150,
                "chiave": "🌀 Chiave del Labirinto", "richiede_partner": True
            },
            "🌀 Labirinto Antico": {
                "nome": "🏛️ Guardiano del Labirinto", "hp": 420, "attacco": 75, "exp": 175,
                "chiave": "🧊 Chiave del Ghiaccio", "abilita_speciale": "teletrasporto"
            },
            "❄️ Area Innevata": {
                "nome": "🐺 Lupo Bianco Alfa", "hp": 480, "attacco": 85, "exp": 200,
                "chiave": "🌿 Chiave della Giungla", "abilita_speciale": "bufera"
            },
            "🌿 Giungla Selvaggia": {
                "nome": "🦖 Rex Primordiale", "hp": 540, "attacco": 95, "exp": 225,
                "chiave": "🌲 Chiave della Natura", "abilita_speciale": "ruggito_primitivo"
            },
            "🌲 Bosco Profondo": {
                "nome": "🐻 Grande Orso delle Radici", "hp": 600, "attacco": 105, "exp": 275,
                "chiave": "⚰️ Chiave del Cimitero", "richiede_casa": True
            },
            "⚰️ Cimitero": {
                "nome": "👹 Demone Custode", "hp": 660, "attacco": 115, "exp": 300,
                "chiave": "🏚️ Chiave dell'Orrore", "abilita_speciale": "maledizione"
            },
            "🏚️ Casa degli Orrori": {
                "nome": "👻 Custode degli Incubi", "hp": 720, "attacco": 125, "exp": 325,
                "chiave": "🏭 Chiave della Fabbrica", "abilita_speciale": "terrore_paralizzante"
            },
            "🏭 Fabbrica Abbandonata": {
                "nome": "🤖 Automa Corrotto", "hp": 750, "attacco": 130, "exp": 350,
                "chiave": "⛏️ Chiave della Miniera", "abilita_speciale": "autocorrezione"
            },
            "⛏️ Miniera Profonda": {
                "nome": "🐲 Drago di Cristallo", "hp": 840, "attacco": 140, "exp": 400,
                "chiave": "🌙 Chiave della Cripta", "abilita_speciale": "soffio_cristallino"
            },
            "🌙 Cripta Maledetta": {
                "nome": "💀 Lich Antico", "hp": 960, "attacco": 150, "exp": 450,
                "chiave": "🌊 Chiave del Mare", "abilita_speciale": "non_morto"
            },
            "🌊 Mare": {
                "nome": "🦈 Re Squalo", "hp": 1050, "attacco": 160, "exp": 500,
                "chiave": "🏔️ Chiave della Montagna", "abilita_speciale": "tsunami"
            },
            "🏔️ Montagna Sacra": {
                "nome": "👼 Angelo Custode", "hp": 1200, "attacco": 170, "exp": 600,
                "chiave": "🌋 Chiave del Vulcano", "abilita_speciale": "luce_divina"
            },
            "🌋 Vulcano Attivo": {
                "nome": "Signore del Magma", "hp": 1350, "attacco": 180, "exp": 750,
                "chiave": "👑 Chiave Finale", "abilita_speciale": "eruzione"
            },
            "👑 Palazzo Finale": {
                "nome": "👑 Imperatore Oscuro", "hp": 1500, "attacco": 200, "exp": 1000,
                "chiave": None, "abilita_speciale": "dominazione"
            },
            "🌌 Regno dei Sogni": {
                "nome": "🌌 Dream Eternal", "hp": 2500, "attacco": 250, "exp": 2000,
                "chiave": None, "abilita_speciale": "metamorfosi", "richiede_nox": True
            }
        }
        
        # Descrizioni ricche e immersive
        self.descrizioni = {
            "Villaggio": "Un tranquillo villaggio con case di pietra. Gli abitanti ti salutano calorosamente. Qui puoi riposare e fare acquisti. Ma si sentono strani rumori dalla cantina...",
            "🏠 Cantina": "Una cantina buia e umida sotto il villaggio. Odore di muffa e formaggio invecchiato. Occhi rossi ti fissano dall'oscurità. I ratti giganti hanno invaso questo posto e il loro Re Ratto custodisce una chiave antica.",
            "🚰 Fogne": "Tunnel sotterranei fetidi con acqua stagnante. Topi di fogna enormi si aggirano nei canali. Il fetore è insopportabile e da solo non riusciresti mai. Serve l'aiuto di un gatto partner per affrontare il Boss Topo delle Fogne.",
            "🌀 Labirinto Antico": "Un intricato labirinto di pietra con pareti che si spostano magicamente. Antiche rune brillano debolmente illuminando corridoi senza fine. Il Guardiano del Labirinto conosce tutti i passaggi segreti e può teletrasportarsi istantaneamente.",
            "❄️ Area Innevata": "Una distesa di ghiaccio e neve eterna. Vento gelido e bufera rendono difficile la visione. Qui puoi costruire rifugi di ghiaccio, pescare nei laghi ghiacciati e raccogliere cristalli di ghiaccio magici. Il Lupo Bianco Alfa custodisce la chiave del gelo.",
            "🌿 Giungla Selvaggia": "Una giungla primordiale con vegetazione fitta e predatori antichi. Liane giganti penzolano dagli alberi millenari mentre creature preistoriche si nascondono nell'ombra. Il Rex Primordiale domina questa terra selvaggia con il suo ruggito terrificante.",
            "🌲 Bosco Profondo": "Una foresta antica e selvaggia. Devi costruire una casa nel bosco ma orsi, lupi e cinghiali difendono il territorio. Gli alberi sussurrano segreti antichi. Il Grande Orso delle Radici protegge la chiave della natura.",
            "⚰️ Cimitero": "Un cimitero nebbioso con lapidi storte. Demoni e spiriti maligni si aggirano tra le tombe. Ostacoli magici bloccano il cammino. Il Demone Custode ha la chiave per aprire la Casa degli Orrori.",
            "🏚️ Casa degli Orrori": "Una villa decadente avvolta nell'oscurità perpetua. Porte che si aprono da sole, sussurri che echeggiano nei corridoi, ombre che si muovono contro natura. La sanità mentale viene messa a dura prova mentre il Custode degli Incubi manipola la realtà stessa per terrorizzare gli intrusi.",
            "🏭 Fabbrica Abbandonata": "Una fabbrica industriale in rovina con macchinari arrugginiti e vapore tossico. Automi corrotti vagano tra i rottami, seguendo ancora antichi programmi. L'Automa Corrotto principale cerca di 'riparare' tutto ciò che incontra.",
            "⛏️ Miniera Profonda": "Tunnel minerari che si addentrano nelle viscere della terra. Cristalli magici illuminano le gallerie buie mentre echi misteriosi risuonano dalle profondità. Il Drago di Cristallo dorme su un tesoro di gemme preziose.",
            "🌙 Cripta Maledetta": "Una cripta sotterranea piena di magia oscura. Qui riposano antichi stregoni. L'aria vibra di energia maledetta. Il Lich Antico, signore dei non-morti, custodisce la chiave del mare.",
            "🌊 Mare": "Un vasto oceano azzurro con onde possenti. Squali di ogni tipo nuotano nelle profondità. Puoi pescare per nutrire i tuoi gatti con pesce magico che aumenta le loro abilità. Il Re Squalo domina questi mari.",
            "🏔️ Montagna Sacra": "Una montagna maestosa che tocca le nuvole, con templi antichi incastonati nella roccia. L'aria è pura e carica di energia divina. Un Angelo Custode protegge questo luogo sacro con la sua luce accecante.",
            "🌋 Vulcano Attivo": "Un vulcano in eruzione con lava incandescente e gas velenosi. Il calore è insopportabile e la terra trema costantemente. Il Signore del Magma governa questo inferno di fuoco e roccia fusa.",
            "👑 Palazzo Finale": "Il palazzo reale con sale dorate e tesori infiniti. Il boss finale, l'Imperatore Oscuro, ti aspetta sul trono.",
            "🌌 Regno dei Sogni": "Un regno onirico dove la realtà cambia forma secondo le tue scelte. Qui le decisioni influenzano non solo il presente, ma anche il passato e il futuro. Il tempo stesso è fluido e Nox può aiutarti a riavvolgere i momenti critici. Il Dream Eternal, boss finale segreto, assume forme diverse in base alle tue scelte oniriche precedenti."
        }
        
        # 🎒 Oggetti speciali distribuiti per il mondo
        self.oggetti = {
            "Villaggio": "🗝️ chiave di bronzo",
            "🌲 Bosco": "🏹 arco elfico",
            "🏔️ Montagna": "⛏️ piccone di mithril",
            "🏰 Castello": "👑 corona reale",
            "🛤️ Strada": "🥾 stivali da viaggio",
            "🌊 Lago": "🎣 canna da pesca magica",
            "⛰️ Caverna": "💎 gemma brillante",
            "🗡️ Arena": " scudo del campione",
            "🏪 Mercato": "",  # Niente oggetti, solo negozi
            "🌳 Foresta": "🌿 erba medicinale",
            "Vulcano": "essenza di fuoco",
            "❄️ Ghiacciai": "❄️ cristallo di ghiaccio",
            "🏝️ Isola": "🏴‍☠️ mappa del tesoro",
            "🏜️ Deserto": "🏺 anfora antica",
            "🌙 Cripta": "💀 teschio maledetto",
            "👑 Palazzo": " tesoro reale"
        }
        
        # 👹 Mostri con livelli e statistiche
        self.mostri = {
            "Villaggio": None,  # Sicuro
            "🌲 Bosco": {"nome": "🐺 Lupo", "hp": 15, "attacco": 8, "livello": 1, "exp": 20},
            "🏔️ Montagna": {"nome": "🦅 Aquila Gigante", "hp": 25, "attacco": 12, "livello": 2, "exp": 35},
            "🏰 Castello": {"nome": " Guardia Reale", "hp": 40, "attacco": 15, "livello": 3, "exp": 50},
            "🛤️ Strada": {"nome": "🏴‍☠️ Bandito", "hp": 20, "attacco": 10, "livello": 2, "exp": 30},
            "🌊 Lago": {"nome": "🐙 Kraken", "hp": 35, "attacco": 18, "livello": 3, "exp": 60},
            "⛰️ Caverna": {"nome": "🐻 Orso delle Caverne", "hp": 30, "attacco": 14, "livello": 2, "exp": 40},
            "🗡️ Arena": {"nome": " Gladiatore", "hp": 45, "attacco": 20, "livello": 4, "exp": 80},
            "🏪 Mercato": None,  # Sicuro
            "🌳 Foresta": {"nome": "🧚‍♀️ Spirito Oscuro", "hp": 28, "attacco": 16, "livello": 3, "exp": 45},
            "Vulcano": {"nome": "Elementale di Fuoco", "hp": 50, "attacco": 25, "livello": 5, "exp": 100},
            "❄️ Ghiacciai": {"nome": "❄️ Yeti", "hp": 55, "attacco": 22, "livello": 5, "exp": 110},
            "🏝️ Isola": {"nome": "🏴‍☠️ Pirata", "hp": 25, "attacco": 13, "livello": 2, "exp": 35},
            "🏜️ Deserto": {"nome": "🦂 Scorpione Gigante", "hp": 32, "attacco": 17, "livello": 3, "exp": 55},
            "🌙 Cripta": {"nome": "💀 Scheletro Guerriero", "hp": 38, "attacco": 19, "livello": 4, "exp": 70},
            "👑 Palazzo": {"nome": "👑 Boss Finale", "hp": 100, "attacco": 30, "livello": 10, "exp": 500}
        }
        
        # 🏪 Negozi e mercanti
        self.negozi = {
            "Villaggio": {
                "Pane": {"prezzo": 60, "tipo": "cibo", "descrizione": "Ripristina 15 HP"},
                "Spada": {"prezzo": 300, "tipo": "arma", "descrizione": "+5 danno"},
                "Armatura": {"prezzo": 400, "tipo": "armatura", "descrizione": "-3 danni ricevuti"}
            },
            "🏪 Mercato": {
                "Pozione Vita": {"prezzo": 300, "tipo": "pozione", "descrizione": "Ripristina 50 HP"},
                "Pozione Forza": {"prezzo": 450, "tipo": "pozione", "descrizione": "+10 danno per 3 turni"},
                "Arco Lungo": {"prezzo": 720, "tipo": "arma", "descrizione": "+8 danno"},
                "Anello Magico": {"prezzo": 1200, "tipo": "accessorio", "descrizione": "+2 HP per turno"}
            },
            "🛤️ Strada": {
                "Mela": {"prezzo": 330, "tipo": "cibo", "descrizione": "Ripristina 10 HP"},
                "Pugnale": {"prezzo": 390, "tipo": "arma", "descrizione": "+3 danno"},
                "Mappa": {"prezzo": 360, "tipo": "oggetto", "descrizione": "Mostra tutte le aree"}
            }
        }
        
        # 🎵 Musiche in formato MP3 per compatibilità universale 
        self.musiche_aree = {
            "Villaggio": "assets/music/villaggio.mp3",
            "🏠 Cantina": "assets/music/cantina.mp3",
            "🚰 Fogne": "assets/music/fogne.mp3",
            "🌀 Labirinto Antico": "assets/music/labirinto.mp3",
            "❄️ Area Innevata": "assets/music/area_innevata.mp3",
            "🌿 Giungla Selvaggia": "assets/music/giungla.mp3",
            "🌲 Bosco Profondo": "assets/music/bosco.mp3",
            "⚰️ Cimitero": "assets/music/cimitero.mp3",
            "🏭 Fabbrica Abbandonata": "assets/music/fabbrica.mp3",
            "⛏️ Miniera Profonda": "assets/music/miniera.mp3",
            "🌙 Cripta Maledetta": "assets/music/cripta.mp3",
            "🌊 Mare": "assets/music/mare.mp3",
            "🏔️ Montagna Sacra": "assets/music/montagna_sacra.mp3",
            "🏚️ Casa degli Orrori": "assets/music/casa_orrori.mp3",
            "🌋 Vulcano Attivo": "assets/music/vulcano.mp3",
            "👑 Palazzo Finale": "assets/music/palazzo_finale.mp3",
            "🌌 Regno dei Sogni": "assets/music/regno_sogni.mp3"
        }
        
        # 🌿 Suoni ambientali per ogni area
        self.suoni_ambiente_aree = {
            "Villaggio": "assets/music/ambient_villaggio_uccelli.mp3",
            "🏠 Cantina": "assets/music/ambient_cantina_gocce.mp3",
            "🚰 Fogne": "assets/music/ambient_fogne_topi.mp3",
            "🌀 Labirinto Antico": "assets/music/ambient_labirinto_vento.mp3",
            "❄️ Area Innevata": "assets/music/ambient_neve_vento.mp3",
            "🌿 Giungla Selvaggia": "assets/music/ambient_giungla_animali.mp3",
            "🌲 Bosco Profondo": "assets/music/ambient_bosco_foglie.mp3",
            "⚰️ Cimitero": "assets/music/ambient_cimitero_spettri.mp3",
            "🏚️ Casa degli Orrori": "assets/music/ambient_orrori_porta.mp3",
            "🏭 Fabbrica Abbandonata": "assets/music/ambient_fabbrica_macchinari.mp3",
            "⛏️ Miniera Profonda": "assets/music/ambient_miniera_picconate.mp3",
            "🌙 Cripta Maledetta": "assets/music/ambient_cripta_magia.mp3",
            "🌊 Mare": "assets/music/ambient_mare_onde.mp3",
            "🏔️ Montagna Sacra": "assets/music/ambient_montagna_vento.mp3",
            "🌋 Vulcano Attivo": "assets/music/ambient_vulcano_lava.mp3",
            "👑 Palazzo Finale": "assets/music/ambient_palazzo_eco.mp3",
            "🌌 Regno dei Sogni": "assets/music/ambient_sogni_magia.mp3"
        }
        
        #  Stato del giocatore incrementale
        self.hp_giocatore = 100
        self.hp_max = 100
        self.vita = 100  # Alias per compatibilità
        self.vita_massima = 100  # Alias per compatibilità
        self.livello = 1
        self.esperienza = 0
        self.esperienza_prossimo_livello = 100
        self.esperienza_necessaria = 100  # Alias per compatibilità
        self.attacco_base = 15
        self.difesa = 0
        self.monete = 100
        self.oro = 100  # Alias per compatibilità
        self.inventario = {}
        self.equipaggiamento = {"arma": None, "armatura": None, "accessorio": None}
        self.effetti_temporanei = {}
        self.gioco_iniziato = False
        self.audio_abilitato = True
        self.haptic_abilitato = True
        self.volume_musica = 0.3
        self.volume_effetti = 0.7
        self.turno = 0
        
        # 🗺️ Sistema legacy compatibilità (per funzioni vecchie)
        self.posizione_giocatore = [0, 0]
        self.mappa = [[self.area_attuale]]  # Mappa dinamica basata su area attuale
        
        # 🎵 Sistema musiche di battaglia
        self.musica_battaglia = "assets/music/battaglia.mp3"
        self.musica_battaglia_boss = "assets/music/battaglia_boss.mp3" 
        self.musica_battaglia_boss_finale = "assets/music/battaglia_boss_finale.mp3"
        self.in_battaglia = False
        self.musica_area_precedente = None
        
        #  Sistema energie e automazione
        self.automazione = {
            "raccolta_automatica": False,
            "combattimento_automatico": False,
            "cura_gatti_automatica": False
        }
        
        # 🏗️ Sistema costruzioni
        self.costruzioni = {
            "casette_gatti": 0,
            "distributori_cibo": 0,
            "pozzi_acqua": 0,
            "fucine": 0
        }
        
        # Stato dell'interfaccia
        self.modalita_menu = "principale"  # principale, gioco, inventario, negozio, statistiche
        
    def reset_gioco(self):
        """Reset completo per gioco incrementale"""
        # Reset stato incrementale
        self.aree_sbloccate = ["Villaggio"]
        self.area_attuale = "Villaggio"
        self.progressione_area = {area: 0 for area in self.aree_ordinate}
        
        # Reset gatti (mantieni affinità e personalizzazioni)
        for gatto_id in self.gatti:
            gatto = self.gatti[gatto_id]
            if gatto_id == "gatto_1":
                gatto.update({"livello": 1, "attacco": 5, "fame": 100, "felicita": 100, "sbloccato": True})
            else:
                gatto.update({"livello": 0, "fame": 0, "felicita": 0, "sbloccato": False})
            # Reset solo contatori temporanei, mantieni affinità e nomi personalizzati
            gatto["aree_non_usato"] = 0
        self.gatto_attivo = "gatto_1"
        
        # Reset chiavi e boss
        self.chiavi_raccolte = []
        self.boss_sconfitti = []
        self.boss_notifications_mostrate = set()
        self.pesce_raccolto = 0
        self.casa_nel_bosco_costruita = False
        
        # Reset sistema legacy
        self.posizione_giocatore = [0, 0]
        self.mappa = [[self.area_attuale]]
        
        # Reset reliquie (mantieni scoperte per collezione)
        self.reliquie_possedute = []
        self.reliquie_equipaggiate = {"slot_1": None, "slot_2": None, "slot_3": None}
        self.mini_dungeon_completati = []
        self.npc_rari_incontrati = []
        
        # Reset sanità mentale
        self.sanita_mentale = 100
        self.eventi_orrore_visti = []
        
        # Reset risorse
        self.risorse = {
            "cibo": 50,
            "acqua": 50,
            "legno": 0,
            "pietra": 0,
            "ferro": 0,
            "energia": 100
        }
        
        # Reset costruzioni
        self.costruzioni = {
            "casette_gatti": 0,
            "distributori_cibo": 0,
            "pozzi_acqua": 0,
            "fucine": 0
        }
        
        # Reset automazione
        self.automazione = {
            "raccolta_automatica": False,
            "combattimento_automatico": False,
            "cura_gatti_automatica": False
        }
        
        # Reset statistiche giocatore
        self.hp_giocatore = 100
        self.hp_max = 100
        self.livello = 1
        self.esperienza = 0
        self.esperienza_prossimo_livello = 100
        self.attacco_base = 15
        self.difesa = 0
        self.monete = 100
        self.inventario = {}
        self.equipaggiamento = {"arma": None, "armatura": None, "accessorio": None}
        self.effetti_temporanei = {}
        self.turno = 0
        
    def crea_audio_system(self):
        """Sistema audio con supporto OGG"""
        # Musica di default (villaggio)
        self.musica_sottofondo = fa.Audio(
            src="assets/music/villaggio.ogg",
            autoplay=False,
            volume=self.volume_musica,
            balance=0,
            on_state_changed=lambda e: print(f"🎵 Stato: {e.data}"),
            on_loaded=lambda _: print("🎵 Musica caricata")
        )
        
        # Canali dedicati fissi - SISTEMA SEMPLICE CHE FUNZIONA
        self.effetto_gatto = fa.Audio(
            src="assets/music/effetto_gatto_attacco.mp3",
            autoplay=False,
            volume=self.volume_effetti,
            balance=0
        )
        
        self.effetto_vittoria = fa.Audio(
            src="assets/music/effetto_vittoria.mp3",
            autoplay=False,
            volume=self.volume_effetti,
            balance=0
        )
        
        self.effetto_sconfitta = fa.Audio(
            src="assets/music/effetto_sconfitta.mp3",
            autoplay=False,
            volume=self.volume_effetti,
            balance=0
        )
        
        self.effetto_livello = fa.Audio(
            src="assets/music/effetto_livello_up.mp3",
            autoplay=False,
            volume=self.volume_effetti,
            balance=0
        )
        
        self.effetto_raccolta = fa.Audio(
            src="assets/music/effetto_raccolta.mp3",
            autoplay=False,
            volume=self.volume_effetti,
            balance=0
        )
        
        self.effetto_gatto_raccolta = fa.Audio(
            src="assets/music/effetto_gatto_raccolta.mp3",
            autoplay=False,
            volume=self.volume_effetti,
            balance=0
        )
        
        self.effetto_monete = fa.Audio(
            src="assets/music/effetto_monete.mp3",
            autoplay=False,
            volume=self.volume_effetti,
            balance=0
        )
        
        # Canale dedicato per suono del mangiare
        self.effetto_mangiare = fa.Audio(
            src="assets/music/effetto_mangiare.mp3",
            autoplay=False,
            volume=self.volume_effetti,
            balance=0
        )
        
        # Canale dedicato per suono del bere pozioni
        self.effetto_bere_pozione = fa.Audio(
            src="assets/music/effetto_bere_pozione.mp3",
            autoplay=False,
            volume=self.volume_effetti,
            balance=0
        )
        
        # Canale dedicato per suono del bere acqua
        self.effetto_bere_acqua = fa.Audio(
            src="assets/music/effetto_bere_acqua.mp3",
            autoplay=False,
            volume=self.volume_effetti,
            balance=0
        )
        
        # Canale dedicato per suono delle fusa del gatto
        self.effetto_fusa = fa.Audio(
            src="assets/music/effetto_fusa.mp3",
            autoplay=False,
            volume=self.volume_effetti,
            balance=0
        )
        
        # Canale dedicato per suono heartbeat (vita bassa) - in loop
        self.effetto_heartbeat = fa.Audio(
            src="assets/music/effetto_heartbeat.mp3",
            autoplay=False,
            volume=self.volume_effetti,
            balance=0,
            on_state_changed=self.heartbeat_loop_handler
        )
        
        # Flag per tracciare se heartbeat è attivo
        self.heartbeat_attivo = False
        
        # Canale dedicato per suoni ambientali delle aree
        self.audio_ambiente = fa.Audio(
            src="assets/music/ambient_villaggio_uccelli.mp3",
            autoplay=False,
            volume=self.volume_effetti * 0.3,  # Volume più basso per ambiente
            balance=0,
            on_state_changed=lambda e: print(f"🌿 Ambiente: {e.data}"),
            on_loaded=lambda _: print("🌿 Suono ambiente caricato")
        )
        
        self.musica_attuale = ""
        self.suono_ambiente_attuale = ""
        self.page.overlay.extend([
            self.musica_sottofondo,
            self.effetto_gatto,
            self.effetto_vittoria,
            self.effetto_sconfitta,
            self.effetto_livello,
            self.effetto_raccolta,
            self.effetto_gatto_raccolta,
            self.effetto_monete,
            self.effetto_mangiare,
            self.effetto_bere_pozione,
            self.effetto_bere_acqua,
            self.effetto_fusa,
            self.effetto_heartbeat,
            self.audio_ambiente
        ])
        
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
        print(f"🎵 Stato musica cambiato: {e.data}")
        if e.data == "completed" and self.audio_abilitato:
            self.musica_sottofondo.play()
        elif e.data == "playing":
            print("🎵 Musica in riproduzione!")
        elif e.data == "paused":
            print("🎵 Musica in pausa")
    
            
    def cambia_musica_area(self, area):
        """Cambia musica con sistema robusto"""
        if not self.audio_abilitato or area not in self.musiche_aree:
            return
            
        # Non cambiare musica se si è in battaglia
        if self.in_battaglia:
            return
            
        file_musica = self.musiche_aree[area]
        
        if self.musica_attuale == file_musica:
            return
            
        # Debug per capire il problema
        print(f"🎵 Tentativo di caricare: {file_musica}")
        print(f"🎵 Directory corrente: {os.getcwd()}")
        print(f"🎵 File esiste: {os.path.exists(file_musica)}")
        
        # Percorso assoluto come fallback
        percorso_assoluto = os.path.abspath(file_musica)
        print(f"🎵 Percorso assoluto: {percorso_assoluto}")
        
        if not os.path.exists(percorso_assoluto):
            print(f"❌ File non trovato: {percorso_assoluto}")
            return
            
        if self.musica_sottofondo in self.page.overlay:
            self.page.overlay.remove(self.musica_sottofondo)
        
        # Caricamento audio semplificato (autoplay gestisce l'avvio)
        try:
            print(f"🎵 Creazione Audio object con: {file_musica}")
            self.musica_sottofondo = fa.Audio(
                src=file_musica,
                autoplay=True,
                volume=self.volume_musica,
                balance=0,
                playback_rate=1.0,
                on_state_changed=self.on_musica_state_changed
            )
            
            self.page.overlay.append(self.musica_sottofondo)
            self.page.update()
            
            self.musica_attuale = file_musica
            print(f"✅ Audio caricato con successo: {file_musica}")
            
        except Exception as e:
            print(f"❌ Errore caricamento audio: {e}")
            print(f"🔄 Tentativo con percorso assoluto...")
            
            try:
                # Fallback con percorso assoluto
                percorso_completo = os.path.abspath(file_musica)
                self.musica_sottofondo = fa.Audio(
                    src=f"file://{percorso_completo}",
                    autoplay=True,
                    volume=self.volume_musica,
                    balance=0,
                    on_state_changed=self.on_musica_state_changed,
                    on_loaded=lambda _: print(f"🎵 Caricato con file://: {percorso_completo}")
                )
                
                self.page.overlay.append(self.musica_sottofondo)
                self.page.update()
                self.musica_attuale = file_musica
                print(f"✅ Audio caricato con file://: {percorso_completo}")
                
            except Exception as e2:
                print(f"❌ Errore anche con file://: {e2}")
                print("🎵 Disabilitazione audio per questa sessione")
                self.audio_abilitato = False
        
    def cambia_suono_ambiente_area(self, area):
        """Cambia suono ambientale dell'area con sistema robusto"""
        if not self.audio_abilitato or area not in self.suoni_ambiente_aree:
            return
            
        file_ambiente = self.suoni_ambiente_aree[area]
        
        if self.suono_ambiente_attuale == file_ambiente:
            return
            
        # Debug per capire il problema
        print(f"🌿 Tentativo di caricare ambiente: {file_ambiente}")
        print(f"🌿 File esiste: {os.path.exists(file_ambiente)}")
        
        # Percorso assoluto come fallback
        percorso_assoluto = os.path.abspath(file_ambiente)
        print(f"🌿 Percorso assoluto ambiente: {percorso_assoluto}")
        
        if not os.path.exists(percorso_assoluto):
            print(f"❌ File ambiente non trovato: {percorso_assoluto}")
            return
            
        if self.audio_ambiente in self.page.overlay:
            self.page.overlay.remove(self.audio_ambiente)
        
        # Caricamento audio ambientale
        try:
            print(f"🌿 Creazione Audio ambiente con: {file_ambiente}")
            self.audio_ambiente = fa.Audio(
                src=file_ambiente,
                autoplay=True,
                volume=self.volume_effetti * 0.3,  # Volume più basso per ambiente
                balance=0,
                playback_rate=1.0,
                on_state_changed=lambda e: self.on_ambiente_state_changed(e),
                on_loaded=lambda _: print("🌿 Suono ambiente caricato")
            )
            
            self.page.overlay.append(self.audio_ambiente)
            
            # Gestisci update della pagina in modo sicuro
            try:
                self.page.update()
            except Exception as e_update:
                print(f"⚠️ Warning: page.update() fallito (normale se chiamato da thread): {e_update}")
            
            self.suono_ambiente_attuale = file_ambiente
            print(f"✅ Audio ambiente caricato con successo: {file_ambiente}")
            
        except Exception as e:
            print(f"❌ Errore caricamento audio ambiente: {e}")
            try:
                # Fallback con percorso assoluto
                percorso_completo = os.path.abspath(file_ambiente)
                self.audio_ambiente = fa.Audio(
                    src=f"file://{percorso_completo}",
                    autoplay=True,
                    volume=self.volume_effetti * 0.3,
                    balance=0,
                    on_state_changed=lambda e: self.on_ambiente_state_changed(e),
                    on_loaded=lambda _: print(f"🌿 Ambiente caricato con file://: {percorso_completo}")
                )
                
                self.page.overlay.append(self.audio_ambiente)
                
                # Gestisci update della pagina in modo sicuro
                try:
                    self.page.update()
                except Exception as e_update:
                    print(f"⚠️ Warning: page.update() fallback fallito: {e_update}")
                    
                self.suono_ambiente_attuale = file_ambiente
                print(f"✅ Audio ambiente caricato con file://: {percorso_completo}")
                
            except Exception as e2:
                print(f"❌ Errore anche con file:// per ambiente: {e2}")
    
    def on_ambiente_state_changed(self, e):
        """Loop suono ambiente"""
        print(f"🌿 Stato ambiente cambiato: {e.data}")
        if e.data == "completed" and self.audio_abilitato:
            # Loop infinito per suoni ambientali
            self.audio_ambiente.play()
        elif e.data == "playing":
            print("🌿 Ambiente in riproduzione!")
        elif e.data == "paused":
            print("🌿 Ambiente in pausa")
    
    def usa_pozione_vita(self, e=None):
        """Usa pozione vita se disponibile nell'inventario"""
        if not self.gioco_iniziato:
            return
            
        # Cerca pozione vita nell'inventario
        if "🧪 Pozione Vita" in self.inventario:
            self.inventario.remove("🧪 Pozione Vita")
            hp_recuperati = min(50, self.hp_max - self.hp_giocatore)
            self.hp_giocatore = min(self.hp_max, self.hp_giocatore + hp_recuperati)
            
            testo = f"🧪 Usi Pozione Vita:\n"
            testo += f" HP recuperati: +{hp_recuperati}\n"
            testo += f" HP attuali: {self.hp_giocatore}/{self.hp_max}"
            
            self.haptic_feedback("success")
            self.riproduci_effetto("bere_pozione")
            self.aggiorna_storia(testo)
            self.aggiorna_stats_incrementali()
        else:
            self.aggiorna_storia("❌ Non hai Pozioni Vita nell'inventario!")
            self.haptic_feedback("warning")
    
    def usa_pozione_forza(self, e=None):
        """Usa pozione forza se disponibile nell'inventario"""
        if not self.gioco_iniziato:
            return
            
        # Cerca pozione forza nell'inventario
        if " Pozione Forza" in self.inventario:
            self.inventario.remove(" Pozione Forza")
            self.effetti_temporanei["Forza Aumentata"] = 3  # 3 turni di bonus
            
            testo = f" Usi Pozione Forza:\n"
            testo += f"💪 +10 danno per 3 turni!\n"
            testo += f"✨ Effetto attivo: Forza Aumentata"
            
            self.haptic_feedback("success")
            self.riproduci_effetto("bere_pozione")
            self.aggiorna_storia(testo)
            self.aggiorna_stats_incrementali()
        else:
            self.aggiorna_storia("❌ Non hai Pozioni Forza nell'inventario!")
            self.haptic_feedback("warning")

    def ferma_suono_ambiente(self):
        """Ferma il suono ambientale (per battaglie)"""
        if not self.audio_abilitato or not hasattr(self, 'audio_ambiente'):
            return
            
        try:
            self.audio_ambiente.pause()
            print("🌿 Suono ambiente fermato per battaglia")
        except Exception as e:
            print(f"❌ Errore fermando suono ambiente: {e}")
    
    def riprendi_suono_ambiente(self):
        """Riprende il suono ambientale dell'area corrente"""
        if not self.audio_abilitato or not hasattr(self, 'audio_ambiente'):
            return
            
        try:
            # Prima controlla se il suono attuale è già quello giusto per l'area
            file_ambiente_richiesto = self.suoni_ambiente_aree.get(self.area_attuale)
            if file_ambiente_richiesto and self.suono_ambiente_attuale == file_ambiente_richiesto:
                # Stesso file, riprendi semplicemente la riproduzione
                print(f"🌿 Ripresa suono ambiente esistente per: {self.area_attuale}")
                self.audio_ambiente.play()
            else:
                # File diverso, cambia completamente
                print(f"🌿 Cambio suono ambiente per: {self.area_attuale}")
                self.cambia_suono_ambiente_area(self.area_attuale)
        except Exception as e:
            print(f"❌ Errore riprendendo suono ambiente: {e}")
            # Fallback: prova a cambiare completamente
            if self.area_attuale in self.suoni_ambiente_aree:
                self.cambia_suono_ambiente_area(self.area_attuale)
        
    def riproduci_effetto(self, effetto):
        """Sistema canali dedicati fissi - SEMPLICE E FUNZIONANTE"""
        # Evita suoni durante l'inizializzazione dell'app
        if not getattr(self, 'app_inizializzata', False):
            return
        
        if not self.audio_abilitato:
            return
        
        # Usa canali dedicati fissi per ogni effetto
        if effetto == "gatto_attacco" or effetto == "attacco":
            self.effetto_gatto.play()
        elif effetto == "vittoria":
            self.effetto_vittoria.play()
        elif effetto == "sconfitta":
            self.effetto_sconfitta.play()
        elif effetto == "livello":
            self.effetto_livello.play()
        elif effetto == "raccogli":
            self.effetto_raccolta.play()
        elif effetto == "gatto_raccolta":
            self.effetto_gatto_raccolta.play()
        elif effetto == "monete":
            self.effetto_monete.play()
        elif effetto == "mangiare" or effetto == "mangia" or effetto == "cibo":
            self.effetto_mangiare.play()
        elif effetto == "bere_pozione" or effetto == "pozione":
            self.effetto_bere_pozione.play()
        elif effetto == "bere_acqua" or effetto == "acqua" or effetto == "bere":
            self.effetto_bere_acqua.play()
        elif effetto == "fusa" or effetto == "gatto_felice" or effetto == "purr":
            self.effetto_fusa.play()
        elif effetto == "heartbeat" or effetto == "vita_bassa" or effetto == "battito":
            self.effetto_heartbeat.play()
    
    def heartbeat_loop_handler(self, e):
        """Gestisce il loop del heartbeat quando finisce"""
        if e.data == "completed" and self.heartbeat_attivo:
            # Se heartbeat deve continuare, riavvialo
            percentuale_vita = (self.vita / self.vita_massima) * 100
            if percentuale_vita <= 20 and self.vita > 0:
                self.effetto_heartbeat.play()
    
    def controlla_vita_bassa(self):
        """Controlla se la vita è sotto il 20% e gestisce il loop heartbeat"""
        if not self.audio_abilitato:
            return
            
        percentuale_vita = (self.vita / self.vita_massima) * 100
        
        # Se la vita è sotto o uguale al 20%, avvia heartbeat loop
        if percentuale_vita <= 20 and self.vita > 0:
            if not self.heartbeat_attivo:
                self.heartbeat_attivo = True
                self.effetto_heartbeat.play()
        else:
            # Se la vita è sopra il 20%, ferma heartbeat
            if self.heartbeat_attivo:
                self.heartbeat_attivo = False
                self.effetto_heartbeat.pause()
    
    def ferma_heartbeat(self):
        """Ferma il loop del heartbeat"""
        if self.heartbeat_attivo:
            self.heartbeat_attivo = False
            self.effetto_heartbeat.pause()
    
    def avvia_musica_battaglia(self, tipo_battaglia="normale"):
        """Avvia musica di battaglia specifica"""
        if not self.audio_abilitato or self.in_battaglia:
            return
            
        # Salva musica area corrente
        self.musica_area_precedente = self.musica_attuale
        self.in_battaglia = True
        
        # Ferma suoni ambientali durante la battaglia
        self.ferma_suono_ambiente()
        
        # Scegli musica battaglia
        if tipo_battaglia == "boss_finale":
            musica_battaglia = self.musica_battaglia_boss_finale
        elif tipo_battaglia == "boss":
            musica_battaglia = self.musica_battaglia_boss
        else:
            musica_battaglia = self.musica_battaglia
            
        print(f"🎵 Avvio musica battaglia: {tipo_battaglia}")
        self.cambia_musica_diretta(musica_battaglia)
    
    def termina_musica_battaglia(self):
        """Termina musica di battaglia e riprende quella dell'area"""
        if not self.audio_abilitato or not self.in_battaglia:
            return
            
        self.in_battaglia = False
        print("🎵 Fine battaglia - ripristino musica area")
        
        # NON fermare gli effetti sonori qui - devono suonare!
        
        # PAUSA NON-BLOCCANTE prima di riavviare la musica per dare tempo agli effetti finali
        import threading
        
        def ripristina_audio_dopo_battaglia():
            import time
            time.sleep(4)  # 4 secondi per sentire gli effetti finali
            
            if not self.audio_abilitato:
                return
                
            # Riprendi musica area precedente o attuale
            if self.musica_area_precedente and self.musica_area_precedente in self.musiche_aree.values():
                self.cambia_musica_diretta(self.musica_area_precedente)
            else:
                # Fallback: musica area attuale
                self.cambia_musica_diretta(self.musiche_aree[self.area_attuale])
            
            # Riprendi suoni ambientali dopo la battaglia
            print("🎵 Tentativo ripresa suono ambiente...")
            self.riprendi_suono_ambiente()
            print("🎵 Ripresa suono ambiente completata")
                    
            self.musica_area_precedente = None
            print("🎵 Audio ripristinato dopo battaglia")
        
        # Avvia ripristino audio in background
        threading.Thread(target=ripristina_audio_dopo_battaglia, daemon=True).start()
    
    def ferma_musica_completamente(self):
        """Ferma completamente la musica (per chiusura app)"""
        if self.audio_abilitato and hasattr(self, 'musica_sottofondo'):
            try:
                self.musica_sottofondo.pause()
                print("🎵 Musica fermata completamente")
            except:
                pass
    
    def aggiorna_mappa_legacy(self):
        """Aggiorna mappa legacy per compatibilità"""
        self.mappa = [[self.area_attuale]]
    
    def cambia_musica_diretta(self, file_musica):
        """Cambia musica direttamente senza controlli area"""
        if not self.audio_abilitato:
            return
            
        if self.musica_attuale == file_musica:
            return
            
        print(f"🎵 Cambio musica diretto: {file_musica}")
        
        # Rimuovi audio precedente
        if hasattr(self, 'musica_sottofondo') and self.musica_sottofondo in self.page.overlay:
            self.page.overlay.remove(self.musica_sottofondo)
        
        try:
            self.musica_sottofondo = fa.Audio(
                src=file_musica,
                autoplay=True,
                volume=self.volume_musica,
                balance=0,
                playback_rate=1.0,
                on_state_changed=self.on_musica_state_changed
            )
            
            self.page.overlay.append(self.musica_sottofondo)
            self.page.update()
            
            self.musica_attuale = file_musica
            print(f"✅ Musica battaglia caricata: {file_musica}")
            
        except Exception as e:
            print(f"❌ Errore caricamento musica battaglia: {e}")
            
    def calcola_attacco_totale(self):
        """Calcola attacco con equipaggiamento e gatto"""
        attacco = self.attacco_base
        if self.equipaggiamento["arma"]:
            if "Spada" in self.equipaggiamento["arma"]:
                attacco += 5
            elif "Arco" in self.equipaggiamento["arma"]:
                attacco += 8
            elif "Pugnale" in self.equipaggiamento["arma"]:
                attacco += 3
        
        # Bonus gatto
        if self.gatto_attivo and self.gatti[self.gatto_attivo]["abilita"] == "combattimento":
            attacco += self.gatti[self.gatto_attivo]["attacco"]
            
        # Effetti temporanei
        if "forza" in self.effetti_temporanei:
            attacco += 10
        if "idratazione" in self.effetti_temporanei:
            attacco += 3
            
        # Bonus reliquie (possono essere condizionali)
        # Questi saranno calcolati nel contesto specifico del combattimento
            
        return attacco
        
    def calcola_difesa_totale(self):
        """Calcola difesa con equipaggiamento e effetti"""
        difesa = self.difesa
        if self.equipaggiamento["armatura"]:
            if "Armatura" in self.equipaggiamento["armatura"]:
                difesa += 3
                
        # Effetti temporanei
        if "idratazione" in self.effetti_temporanei:
            difesa += 2
            
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
            
            # Riproduci effetto livello su canale dedicato
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
    
    # === NUOVE FUNZIONI INCREMENTALI ===
    
    def raccogli_risorse(self, e):
        """Raccolta risorse nell'area attuale"""
        if not self.gioco_iniziato:
            return
            
        if self.risorse["energia"] < 10:
            self.aggiorna_storia(" Non hai abbastanza energia! Riposa o mangia per recuperare.")
            self.haptic_feedback("warning")
            return
            
        self.risorse["energia"] -= 10
        area = self.area_attuale
        
        # Bonus gatto per raccolta
        bonus_gatto = 1
        if self.gatto_attivo and self.gatti[self.gatto_attivo]["abilita"] in ["raccolta", "raccolta_suprema"]:
            bonus_gatto = 1 + (self.gatti[self.gatto_attivo]["livello"] * 0.2)
            
        # Risorse per area
        risorse_raccolte = {}
        if area == "Villaggio":
            risorse_raccolte = {"cibo": int(random.randint(5, 15) * bonus_gatto), "acqua": int(random.randint(3, 8) * bonus_gatto)}
        elif area == "🌲 Bosco":
            risorse_raccolte = {"legno": int(random.randint(10, 20) * bonus_gatto), "cibo": int(random.randint(2, 5) * bonus_gatto)}
        elif area == "🏔️ Montagna":
            risorse_raccolte = {"pietra": int(random.randint(8, 15) * bonus_gatto), "ferro": int(random.randint(1, 3) * bonus_gatto)}
        else:
            # Altre aree
            risorse_raccolte = {"cibo": int(random.randint(2, 8) * bonus_gatto)}
            
        # Aggiorna risorse
        testo = f" Raccogli risorse in {area}:\n"
        for risorsa, quantita in risorse_raccolte.items():
            self.risorse[risorsa] += quantita
            testo += f"• +{quantita} {risorsa}\n"
            
        # Bonus esperienza
        exp_guadagnata = 1
        self.esperienza += exp_guadagnata
        testo += f"\n +{exp_guadagnata} EXP"
        
        # Controlla livello
        testo_livello = self.gestisci_livello()
        if testo_livello:
            testo += "\n" + testo_livello
        
        # Controlla sblocco gatti
        self.controlla_sblocco_gatti()
            
        # Progressione area (solo se area valida)
        if area in self.progressione_area:
            self.progressione_area[area] += 1
            print(f" Progressione {area}: {self.progressione_area[area]}")
            
            # Controlla se il boss dell'area è stato sbloccato per la prima volta
            if (self.progressione_area[area] >= 100 and 
                area not in self.boss_notifications_mostrate):
                boss_sconfitto = self.controlla_boss_sconfitto(area)
                if boss_sconfitto and self.sblocca_prossima_area():
                    testo += f"\n🎆 Hai sbloccato una nuova area!"
                elif not boss_sconfitto:
                    # Mostra notifica sblocco boss solo una volta
                    self.boss_notifications_mostrate.add(area)
                    self.mostra_notifica_boss_sbloccato(area)
                    testo += f"\n Devi prima sconfiggere il boss di quest'area per procedere!"
        else:
            print(f"⚠️ Area non trovata in progressione_area: {area}")
            
        self.haptic_feedback("success")
        # Effetto diverso se ha gatto da raccolta attivo
        if self.gatto_attivo and self.gatti[self.gatto_attivo]["abilita"] in ["raccolta", "raccolta_suprema"]:
            self.riproduci_effetto("gatto_raccolta")
        else:
            self.riproduci_effetto("raccogli")
        self.aggiorna_storia(testo)
        self.aggiorna_stats_incrementali()
        
    def nutri_gatto(self, e):
        """Nutri il gatto attivo"""
        if not self.gioco_iniziato or not self.gatto_attivo:
            return
            
        if self.risorse["cibo"] < 5:
            self.aggiorna_storia("🍽️ Non hai abbastanza cibo! Vai a raccogliere risorse.")
            self.haptic_feedback("warning")
            return
            
        self.risorse["cibo"] -= 5
        gatto = self.gatti[self.gatto_attivo]
        gatto["fame"] = min(100, gatto["fame"] + 30)
        gatto["felicita"] = min(100, gatto["felicita"] + 15)
        
        # Bonus per gatto felice
        if gatto["felicita"] > 80:
            exp_bonus = 3
            self.esperienza += exp_bonus
            testo = f" {self.gatto_attivo} è molto felice!\n"
            testo += f"🍽️ Fame: {gatto['fame']}/100\n"
            testo += f"😊 Felicità: {gatto['felicita']}/100\n"
            testo += f" Bonus: +{exp_bonus} EXP"
            # Riproduci suono delle fusa quando il gatto è felice
            self.riproduci_effetto("fusa")
        else:
            testo = f" {self.gatto_attivo} ha mangiato.\n"
            testo += f"🍽️ Fame: {gatto['fame']}/100\n"
            testo += f"😊 Felicità: {gatto['felicita']}/100"
            
        self.haptic_feedback("success")
        self.aggiorna_storia(testo)
        self.aggiorna_stats_incrementali()
        
    def consuma_cibo(self, e):
        """Consuma cibo per recuperare energia e HP"""
        if not self.gioco_iniziato:
            return
            
        if self.risorse["cibo"] < 10:
            self.aggiorna_storia("🍽️ Non hai abbastanza cibo! Vai a raccogliere risorse.")
            self.haptic_feedback("warning")
            return
            
        self.risorse["cibo"] -= 10
        self.risorse["energia"] = min(100, self.risorse["energia"] + 40)
        hp_recuperati = min(20, self.hp_max - self.hp_giocatore)
        self.hp_giocatore = min(self.hp_max, self.hp_giocatore + hp_recuperati)
        
        # Sincronizza anche vita se esiste per evitare sovrascritture
        if hasattr(self, 'vita'):
            self.vita = self.hp_giocatore
        
        testo = f"🍽️ Consumi cibo:\n"
        testo += f" Energia: {self.risorse['energia']}/100\n"
        if hp_recuperati > 0:
            testo += f" HP recuperati: +{hp_recuperati}"
        else:
            testo += f" HP già al massimo"
            
        self.haptic_feedback("success")
        self.riproduci_effetto("mangiare")
        self.aggiorna_storia(testo)
        self.aggiorna_stats_incrementali()
        
    def bevi_acqua(self, e):
        """Bevi acqua per bonus temporanei"""
        if not self.gioco_iniziato:
            return
            
        if self.risorse["acqua"] < 5:
            self.aggiorna_storia("💧 Non hai abbastanza acqua! Vai a raccogliere risorse.")
            self.haptic_feedback("warning")
            return
            
        self.risorse["acqua"] -= 5
        self.effetti_temporanei["idratazione"] = 5
        
        testo = f"💧 Bevi acqua fresca:\n"
        testo += f"✨ Effetto idratazione per 5 turni\n"
        testo += f"💪 +3 attacco, +2 difesa"
        
        self.haptic_feedback("success")
        self.riproduci_effetto("bere_acqua")
        self.aggiorna_storia(testo)
        self.aggiorna_stats_incrementali()
        
    def sblocca_nuova_area(self):
        """Sblocca nuova area basata sulla progressione"""
        aree_disponibili = [
            "🌲 Bosco", "🏔️ Montagna", "🏰 Castello", "🛤️ Strada",
            "🌊 Lago", "⛰️ Caverna", "🗡️ Arena", "🏪 Mercato",
            "🌳 Foresta", "Vulcano", "❄️ Ghiacciai", "🏝️ Isola",
            "🏜️ Deserto", "🌙 Cripta", "👑 Palazzo"
        ]
        
        for area in aree_disponibili:
            if area not in self.aree_sbloccate:
                self.aree_sbloccate.append(area)
                
                # Controlla sblocco gatti dopo nuova area
                self.controlla_sblocco_gatti()
                
                self.haptic_feedback("success")
                # NON riprodurre vittoria qui - crea conflitto con raccolta risorse
                return f"\n\n🎆 NUOVA AREA SBLOCCATA: {area}!"
        return ""
        
    def cambia_area(self, nuova_area):
        """Cambia area attuale"""
        if nuova_area not in self.aree_sbloccate:
            self.aggiorna_storia(f"❌ Area {nuova_area} non ancora sbloccata!")
            self.haptic_feedback("error")
            return
            
        self.area_attuale = nuova_area
        self.aggiorna_mappa_legacy()  # Aggiorna mappa per compatibilità
        if self.audio_abilitato:
            self.cambia_musica_area(nuova_area)
            self.cambia_suono_ambiente_area(nuova_area)
            
        self.haptic_feedback("light")
        self.aggiorna_storia(f" Ti sposti in {nuova_area}")
        self.aggiorna_stats_incrementali()
        
    def cambia_gatto_attivo(self, nome_gatto):
        """Cambia gatto attivo"""
        if nome_gatto not in self.gatti:
            return
            
        gatto = self.gatti[nome_gatto]
        if not gatto.get("sbloccato", True):
            self.aggiorna_storia(f"❌ {nome_gatto} non è ancora sbloccato!")
            self.haptic_feedback("error")
            return
            
        self.gatto_attivo = nome_gatto
        gatto_info = self.gatti[nome_gatto]
        nome_display = f"{gatto_info['emoji']} {gatto_info['nome']}"
        self.haptic_feedback("light")
        self.aggiorna_storia(f" {nome_display} è ora il tuo compagno attivo!")
        self.aggiorna_stats_incrementali()
        
    def aggiorna_stats_incrementali(self):
        """Aggiorna statistiche per gioco incrementale"""
        # Sincronizza sempre HP con vita per assicurare coerenza
        if hasattr(self, 'vita'):
            self.hp_giocatore = self.vita
        
        # Applica bonus reliquie passive e aggiorna affinità
        self.applica_bonus_reliquie_gatti()
        self.aggiorna_contatori_affinita()
        
        # Gestisci effetti temporanei (decrementali solo durante certe azioni)
        # Non li decrementiamo automaticamente per non farli scadere troppo velocemente
        
        stats = f"Statistiche Incrementali:\n"
        stats += f"Livello {self.livello}.\n"
        stats += f"HP: {self.hp_giocatore}/{self.hp_max}.\n"
        stats += f"Monete: {self.monete}.\n"
        stats += f"Attacco: {self.calcola_attacco_totale()}.\n"
        stats += f"Difesa: {self.calcola_difesa_totale()}.\n"
        stats += f"EXP: {self.esperienza}/{self.esperienza_prossimo_livello}.\n"
        stats += f"Area: {self.area_attuale}.\n"
        # Mostra progressione area corrente
        progressione_corrente = self.progressione_area.get(self.area_attuale, 0)
        stats += f"Progressione: {progressione_corrente}/100 (Boss a 100).\n\n"
        
        stats += f"Risorse:\n"
        for risorsa, quantita in self.risorse.items():
            stats += f"• {risorsa.title()}: {quantita}.\n"
            
        if self.gatto_attivo:
            gatto = self.gatti[self.gatto_attivo]
            nome_gatto = f"{gatto['emoji']} {gatto['nome']}"
            
            # Mostra livello affinità con emoji
            affinita = gatto["affinita"]
            if affinita >= 200:
                affinita_emoji = ""
            elif affinita >= 150:
                affinita_emoji = "💙"
            elif affinita >= 100:
                affinita_emoji = "💚"
            elif affinita >= 50:
                affinita_emoji = "💛"
            else:
                affinita_emoji = ""
                
            stats += f"\nGatto attivo: {nome_gatto}.\n"
            stats += f"Affinità: {affinita_emoji} {affinita}/200.\n"
            stats += f"• Livello: {gatto['livello']} • Abilità: {gatto['abilita']}.\n"
            stats += f"• Fame: {gatto['fame']}/100 • Felicità: {gatto['felicita']}/100."
            
        # Mostra sanità mentale se in Casa degli Orrori o se danneggiata
        if self.area_attuale == "🏚️ Casa degli Orrori" or self.sanita_mentale < 100:
            if self.sanita_mentale >= 80:
                sanita_emoji = "🧠"
                sanita_status = "STABILE"
            elif self.sanita_mentale >= 60:
                sanita_emoji = "😰"
                sanita_status = "PREOCCUPATO"
            elif self.sanita_mentale >= 40:
                sanita_emoji = "😱"
                sanita_status = "SPAVENTATO"
            elif self.sanita_mentale >= 20:
                sanita_emoji = "🤯"
                sanita_status = "TERRORIZZATO"
            else:
                sanita_emoji = "💀"
                sanita_status = "FOLLE"
            stats += f"\nSanità Mentale: {sanita_emoji} {self.sanita_mentale}/100 ({sanita_status})."
            
        # Mostra chiavi raccolte
        if self.chiavi_raccolte:
            stats += f"\n\nChiavi: {len(self.chiavi_raccolte)}."
            
        # Mostra pesce se nell'area mare
        if self.area_attuale == "🌊 Mare" and self.pesce_raccolto > 0:
            stats += f"\nPesce: {self.pesce_raccolto}."
            
        if self.effetti_temporanei:
            stats += f"\n\nEffetti attivi: {', '.join(self.effetti_temporanei.keys())}."
            
        self.aggiorna_stats(stats)
        
    # LOGICA PULSANTI DINAMICI
    
    def azioni_incrementali_possibili(self):
        """Restituisce lista delle azioni incrementali possibili"""
        print(f"🎮 DEBUG: azioni_incrementali_possibili() chiamata")
        azioni = []
        
        # Raccolta risorse sempre disponibile
        if self.risorse["energia"] >= 10:
            azioni.append(("Raccogli Risorse", self.raccogli_risorse, "Raccogli risorse nell'area attuale"))
        
        # Azioni cibo e acqua
        if self.risorse["cibo"] >= 10:
            azioni.append(("Consuma Cibo", self.consuma_cibo, "Mangia per recuperare energia e HP"))
        if self.risorse["acqua"] >= 5:
            azioni.append(("Bevi Acqua", self.bevi_acqua, "Bevi per bonus temporanei"))
            
        # Azioni gatto
        if self.gatto_attivo and self.risorse["cibo"] >= 5:
            azioni.append(("Nutri Gatto", self.nutri_gatto, "Nutri il tuo gatto compagno"))
        
        # Rinomina gatto se ne hai uno attivo (sempre disponibile)
        print(f" DEBUG: gatto_attivo in azioni_incrementali = {self.gatto_attivo}")
        if self.gatto_attivo:
            nome_gatto = self.gatti[self.gatto_attivo]["nome"]
            print(f" DEBUG: Aggiungendo Rinomina Gatto per {nome_gatto}")
            azioni.append(("Rinomina Gatto", self.rinomina_gatto, f"Rinomina {nome_gatto}"))
            
        # Costruzioni se si hanno risorse
        if self.risorse["legno"] >= 20 or self.risorse["pietra"] >= 15:
            azioni.append(("Costruisci", self.costruisci, "Costruisci strutture utili"))
            
        # Cambia area se ne hai sbloccate altre
        if len(self.aree_sbloccate) > 1:
            azioni.append(("Cambia Area", self.menu_cambia_area, "Viaggia verso altre aree"))
            
        # Pulsante Boss se progressione >= 100 e boss non sconfitto
        if (self.progressione_area.get(self.area_attuale, 0) >= 100 and 
            self.area_attuale in self.boss_aree and
            not self.controlla_boss_sconfitto(self.area_attuale)):
            boss_nome = self.boss_aree[self.area_attuale]["nome"]
            azioni.append(("Combatti Boss dell'Area!", self.combatti_boss, f"Affronta {boss_nome}"))
        
        # Inventario sempre disponibile (in fondo alla lista)
        azioni.append(("Inventario", self.vai_a_inventario, "Visualizza inventario ed equipaggiamento"))
            
        return azioni
    
    def azioni_speciali_possibili(self):
        """Restituisce lista delle azioni speciali nell'area attuale"""
        area = self.area_attuale
        azioni = []
        
        # Boss fight se disponibile e non ancora sconfitto
        if area in self.boss_aree:
            boss_nome = self.boss_aree[area]["nome"]
            if boss_nome not in self.boss_sconfitti:
                azioni.append(("👹 Sfida Boss", self.combatti_boss, f"Combatti contro {boss_nome}"))
        
        # Azioni specifiche per area
        if area == "🌊 Mare":
            azioni.append(("🎣 Pesca", self.pesca_nel_mare, "Pesca per ottenere pesce magico"))
            if self.pesce_raccolto >= 3:
                azioni.append(("🐟 Nutri con Pesce", self.nutri_gatto_con_pesce, "Nutri gatto con pesce magico"))
                
        elif area == "🌌 Regno dei Sogni":
            # Azioni oniriche speciali
            if len(self.scelte_oniriche) < 3:  # Massimo 3 scelte oniriche
                azioni.append(("Scelta Armonia", lambda e: self.azione_scelta_onirica("armonia"), "Porta armonia nel regno"))
                azioni.append(("Scelta Caos", lambda e: self.azione_scelta_onirica("caos"), "Scatena il caos nel regno"))
                azioni.append(("Scelta Equilibrio", lambda e: self.azione_scelta_onirica("equilibrio"), "Mantieni l'equilibrio"))
            
            if self.gatti["gatto_5"]["sbloccato"] and self.riavvolgimenti_disponibili > 0:
                azioni.append(("Riavvolgi Tempo", self.usa_riavvolgimento_nox, f"Usa Nox per riavvolgere ({self.riavvolgimenti_disponibili} rimasti)"))
                
        elif area == "🌲 Bosco Profondo":
            if not self.casa_nel_bosco_costruita:
                if (self.risorse["legno"] >= 50 and self.risorse["pietra"] >= 30 and 
                    self.progressione_area[area] >= 15):
                    azioni.append(("Costruisci Casa", self.costruisci_casa_nel_bosco, "Costruisci casa nel bosco"))
            else:
                # Casa già costruita - azioni aggiuntive
                azioni.append(("Riposa con Gatto", lambda e: self.riposa_con_gatto_in_casa(), "Riposa con il tuo gatto per rafforzare il legame"))
                
        elif area == "🌀 Labirinto Antico":
            azioni.append(("Naviga Labirinto", self.naviga_labirinto, "Attraversa i corridoi che cambiano"))
            if random.randint(1, 100) <= 30:  # 30% chance
                azioni.append(("Camera Segreta", self.scopri_camera_segreta, "Hai trovato una stanza nascosta!"))
                
        elif area == "❄️ Area Innevata":
            azioni.append(("Raccogli Ghiaccio", self.raccogli_ghiaccio, "Raccogli cristalli di ghiaccio"))
            
        elif area == "🏚️ Casa degli Orrori":
            azioni.append(("Esplora Stanze", self.esplora_stanze_orrore, "Attraversa le stanze infestate"))
            azioni.append(("Caccia Fantasmi", self.caccia_fantasmi, "Cerca e affronta spiriti maligni"))
            if self.sanita_mentale < 50:
                azioni.append(("Medita per Calmarsi", self.medita_sanita, "Recupera sanità mentale"))
            
        elif area == "🌿 Giungla Selvaggia":
            azioni.append(("Raccogli Erbe", self.raccogli_erbe_medicinali, "Trova erbe medicinali rare"))
            azioni.append(("Traccia Dinosauri", self.traccia_dinosauri, "Segui le tracce di creature antiche"))
            
        elif area == "🏭 Fabbrica Abbandonata":
            azioni.append(("Ripara Macchinari", self.ripara_macchinari, "Ripara automi per ottenere componenti"))
            azioni.append(("Riattiva Energia", self.riattiva_energia_fabbrica, "Riavvia i sistemi energetici"))
            
        elif area == "⛏️ Miniera Profonda":
            azioni.append(("Estrai Cristalli", self.estrai_cristalli, "Raccogli cristalli magici preziosi"))
            azioni.append(("Cerca Tesoro Drago", self.cerca_tesoro_drago, "Esplora la tana del drago"))
            
        elif area == "🏔️ Montagna Sacra":
            azioni.append(("Prega al Tempio", self.prega_al_tempio, "Ricevi benedizioni divine"))
            azioni.append(("Comunica con Angelo", self.comunica_angelo, "Parla con l'Angelo Custode"))
            
        elif area == "🌋 Vulcano Attivo":
            azioni.append(("Raccogli Magma", self.raccogli_magma, "Raccogli magma cristallizzato"))
            azioni.append(("Tempra Armi", self.tempra_armi_vulcano, "Usa il calore per potenziare le armi"))
        
        # Esplora per trovare tesori (sostituisce raccolta oggetti)
        if self.progressione_area[area] < 20:
            azioni.append(("Esplora", self.esplora_area, "Esplora l'area per trovare tesori"))
            
        # Combatti mostri normali (più incrementale)
        azioni.append(("Combatti", self.combatti_mostri, "Combatti mostri per esperienza"))
        
            
        # Legame con gatti
        if self.gatto_attivo and self.gatti[self.gatto_attivo]["sbloccato"]:
            azioni.append((" Legame Gatti", self.mostra_legame_gatti, "Gestisci il tuo rapporto con i gatti"))
            
        # Negozio se disponibile
        if area in ["Villaggio"]:
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
        """Crea l'interfaccia utente principale usando page.views per VoiceOver"""
        self.page.title = "🏰 Avventura Epica - Accessibile"
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.theme_mode = ft.ThemeMode.DARK
        
        # Setup route handler
        self.page.on_route_change = self.route_change
        
        # Inizializza i componenti principali con colori
        self.area_stats = ft.TextField(
            value=" Statistiche Giocatore:\n Livello 1 •  100/100 HP •  100 monete\n Attacco: 15 •  Difesa: 0\n EXP: 0/100",
            multiline=True,
            read_only=True,
            min_lines=4,
            max_lines=6,
            text_size=14,
            bgcolor=ft.Colors.BLUE_GREY_900,
            color=ft.Colors.CYAN_100,
            border_color=ft.Colors.CYAN_400,
            focused_border_color=ft.Colors.CYAN_300
        )
        
        self.area_storia = ft.TextField(
            value="🎮 Benvenuto nell'Avventura Incrementale!\n Compagni gatti con abilità speciali\n Raccogli risorse e costruisci\n Combatti mostri e sali di livello\n🍽️ Gestisci cibo e acqua per energia\n🎵 Audio immersivo e feedback aptico\n\nPremi 'Inizia Avventura' per cominciare!",
            multiline=True,
            read_only=True,
            expand=True,
            min_lines=10,
            max_lines=15,
            text_size=14,
            bgcolor=ft.Colors.DEEP_PURPLE_900,
            color=ft.Colors.AMBER_100,
            border_color=ft.Colors.AMBER_400,
            focused_border_color=ft.Colors.AMBER_300
        )
        
        # Mantieni container_pulsanti per compatibilità con vecchie funzioni
        self.container_pulsanti = ft.Column()
        
        # Inizializza con la vista del menu principale
        self.page.views.clear()
        vista_menu = self.crea_vista_menu_principale()
        self.page.views.append(vista_menu)
        self.analizza_accessibilita(vista_menu)  # 👈 Diagnostica la view
        self.page.go("/")
    
    def inizia_o_continua_gioco(self, e):
        """Inizia nuovo gioco o continua se già iniziato"""
        if not self.gioco_iniziato:
            # Nuovo gioco
            self.inizia_gioco(e)
        else:
            # Continua - vai alla schermata gioco
            self.page.go("/gioco")
    
    def sincronizza_variabili_alias(self):
        """Sincronizza le variabili alias per compatibilità"""
        # NON sincronizzare vita se siamo appena usciti da un combattimento
        # Usa sempre il valore della vita attuale che può essere stato modificato dal combattimento
        if hasattr(self, 'vita'):
            self.hp_giocatore = self.vita
        if hasattr(self, 'hp_max'):
            self.vita_massima = self.hp_max
        # Sincronizza oro
        if hasattr(self, 'monete'):
            self.oro = self.monete
        # Sincronizza esperienza
        if hasattr(self, 'esperienza_prossimo_livello'):
            self.esperienza_necessaria = self.esperienza_prossimo_livello

    def route_change(self, route):
        """Handler per cambiamenti di route"""
        print(f"🧭 NAVIGAZIONE: Route cambiata a '{route.route}'")

        # Sempre pulire prima di cambiare vista
        if route.route != "/gioco" or (len(self.page.views) == 0 or self.page.views[-1].route != "/gioco"):
            self.page.views.clear()

        match route.route:
            case "/":
                vista = self.crea_vista_menu_principale()
                self.page.views.append(vista)
                self.analizza_accessibilita(vista)
            case "/gioco":
                if len(self.page.views) > 0 and self.page.views[-1].route == "/gioco":
                    print(f"🎮 DEBUG: Vista /gioco già presente, non duplico")
                else:
                    vista = self.crea_vista_gioco()
                    self.page.views.append(vista)
                    self.analizza_accessibilita(vista)
            case "/impostazioni":
                vista = self.crea_vista_impostazioni()
                self.page.views.append(vista)
                self.analizza_accessibilita(vista)
            case "/info":
                vista = self.crea_vista_info()
                self.page.views.append(vista)
                self.analizza_accessibilita(vista)
            case "/negozio":
                vista = self.crea_vista_negozio()
                self.page.views.append(vista)
                self.analizza_accessibilita(vista)
            case "/aree":
                vista = self.crea_vista_aree()
                self.page.views.append(vista)
                self.analizza_accessibilita(vista)
            case "/combattimento":
                vista = self.crea_vista_combattimento()
                self.page.views.append(vista)
                self.analizza_accessibilita(vista)
            case "/gatti":
                vista = self.crea_vista_gatti()
                self.page.views.append(vista)
                self.analizza_accessibilita(vista)
            case "/inventario":
                vista = self.crea_vista_inventario()
                self.page.views.append(vista)
                self.analizza_accessibilita(vista)
            case "/statistiche":
                vista = self.crea_vista_statistiche()
                self.page.views.append(vista)
                self.analizza_accessibilita(vista)
            case "/rinomina_gatto":
                vista = self.crea_vista_rinomina_gatto()
                self.page.views.append(vista)
                self.analizza_accessibilita(vista)
            case "/gestione_reliquie":
                vista = self.crea_vista_gestione_reliquie()
                self.page.views.append(vista)
                self.analizza_accessibilita(vista)
            case "/salvataggio_conferma":
                vista = self.crea_vista_salvataggio_conferma()
                self.page.views.append(vista)
                self.analizza_accessibilita(vista)
            case _:
                vista = self.crea_vista_menu_principale()
                self.page.views.append(vista)
                self.analizza_accessibilita(vista)

        self.page.update()
        self.haptic_feedback("light")

    def torna_indietro(self, e=None):
        print(f"🔙 Torna indietro - Views: {len(self.page.views)}")

        if len(self.page.views) > 1:
            self.page.views.pop()
            previous_route = self.page.views[-1].route if len(self.page.views) > 0 else "/"
            self.page.views.clear()
            self.page.go(previous_route)
        else:
            self.page.views.clear()
            self.page.go("/gioco" if self.gioco_iniziato else "/")

        self.haptic_feedback("light")

    def naviga_a_schermata(self, nuova_schermata):
        """Naviga a una nuova schermata usando page.go(), evitando navigazioni ridondanti"""
        
        route_map = {
            "menu_principale": "/",
            "gioco": "/gioco",
            "impostazioni": "/impostazioni",
            "info": "/info",
            "negozio": "/negozio",
            "aree": "/aree",
            "combattimento": "/combattimento",
            "gatti": "/gatti",
            "gestione_gatti": "/gatti",
            "inventario": "/inventario",
            "rinomina_gatto": "/rinomina_gatto",
            "gestione_reliquie": "/gestione_reliquie",
            "salvataggio_conferma": "/salvataggio_conferma"
        }

        route = route_map.get(nuova_schermata, "/")
        
        if self.page.route != route:
            print(f"🧭 NAVIGAZIONE: Andando a {nuova_schermata} -> {route}")
            self.page.go(route)
        else:
            print(f"ℹ️ Già sulla schermata '{nuova_schermata}', nessuna navigazione necessaria.")

    def crea_pulsante_indietro(self):
        """Crea pulsante per tornare indietro"""
        return ft.ElevatedButton(
            text="Indietro",
            on_click=self.torna_indietro,
            width=150,
            height=50,
            bgcolor=ft.Colors.RED_700,
            color=ft.Colors.WHITE,
            tooltip="Torna alla schermata precedente"
        )
    
    def crea_vista_menu_principale(self):
        """Crea la vista del menu principale"""
        titolo = ft.Text(
            "Avventura Epica", 
            size=28, 
            weight=ft.FontWeight.BOLD, 
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.AMBER_400
        )
        
        pulsanti = [
            ft.ElevatedButton(
                text="Inizia Gioco",
                on_click=self.inizia_o_continua_gioco,
                width=300,
                height=60,
                bgcolor=ft.Colors.GREEN_700,
                color=ft.Colors.WHITE,
                tooltip="Inizia una nuova avventura o continua"
            ),
            ft.ElevatedButton(
                text="Carica Gioco",
                on_click=self.carica_gioco,
                width=300,
                height=60,
                bgcolor=ft.Colors.BLUE_700,
                color=ft.Colors.WHITE,
                tooltip="Carica partita salvata"
            ),
            ft.ElevatedButton(
                text="Impostazioni",
                on_click=lambda e: self.page.go("/impostazioni"),
                width=300,
                height=60,
                bgcolor=ft.Colors.PURPLE_700,
                color=ft.Colors.WHITE,
                tooltip="Impostazioni audio e vibrazione"
            ),
            ft.ElevatedButton(
                text="Info",
                on_click=lambda e: self.page.go("/info"),
                width=300,
                height=60,
                bgcolor=ft.Colors.ORANGE_700,
                color=ft.Colors.WHITE,
                tooltip="Informazioni sul gioco"
            )
        ]
        
        content = ft.Column([
            titolo,
            ft.Column(pulsanti, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
        ], scroll=ft.ScrollMode.AUTO, spacing=50, expand=True)
        
        return ft.View(
            "/",
            controls=[
                ft.Container(
                    content=content,
                    bgcolor=ft.Colors.GREY_900,
                    padding=20,
                    expand=True
                )
            ],
            bgcolor=ft.Colors.GREY_900
        )
    def crea_vista_gioco(self):
        """Vista di gioco ottimizzata per performance e accessibilità"""
        titolo = ft.Text("AVVENTURA IN CORSO", size=24, weight=ft.FontWeight.BOLD)

        # 🔁 Riutilizza o crea area_storia
        valore_storia = getattr(self.area_storia, "value", "🎮 Benvenuto nell'Avventura Incrementale!")
        if hasattr(self, 'area_storia') and self.area_storia:
            self.area_storia.value = valore_storia
        else:
            self.area_storia = ft.TextField(
                value=valore_storia,
                multiline=True,
                read_only=True,
                expand=True,
                min_lines=10,
                max_lines=15,
                text_size=14,
                bgcolor=ft.Colors.DEEP_PURPLE_900,
                color=ft.Colors.AMBER_100,
                border_color=ft.Colors.AMBER_400,
                focused_border_color=ft.Colors.AMBER_300,
                label="Storia dell'avventura"
            )

        # 🔁 Riutilizza o crea area_stats
        valore_stats = f" Statistiche Giocatore:\n Livello {self.livello} •  {self.vita}/{self.vita_massima} HP •  {self.monete} monete\n Attacco: {self.calcola_attacco_totale()} •  Difesa: {self.calcola_difesa_totale()}\n EXP: {self.esperienza}/{self.esperienza_necessaria}"
        if hasattr(self, 'area_stats') and self.area_stats:
            self.area_stats.value = valore_stats
        else:
            self.area_stats = ft.TextField(
                value=valore_stats,
                multiline=True,
                read_only=True,
                min_lines=4,
                max_lines=6,
                text_size=14,
                bgcolor=ft.Colors.BLUE_GREY_900,
                color=ft.Colors.CYAN_100,
                border_color=ft.Colors.CYAN_400,
                focused_border_color=ft.Colors.CYAN_300,
                label="Statistiche giocatore"
            )

        # 🔁 Ricrea solo i pulsanti dinamici
        pulsanti_gioco = []

        for testo, funzione, tooltip in self.azioni_incrementali_possibili():
            pulsanti_gioco.append(
                ft.ElevatedButton(
                    text=testo,
                    on_click=funzione,
                    width=280,
                    height=50,
                    bgcolor=ft.Colors.GREEN_600,
                    color=ft.Colors.WHITE,
                    tooltip=tooltip
                )
            )

        # ✅ Pulsanti statici (riutilizzati o creati una volta)
        if not hasattr(self, 'pulsante_combattimento'):
            self.pulsante_combattimento = ft.ElevatedButton(
                text="Combattimento",
                on_click=lambda e: self.page.go("/combattimento"),
                width=280,
                height=50,
                bgcolor=ft.Colors.RED_600,
                color=ft.Colors.WHITE,
                tooltip="Combatti contro i mostri"
            )

            self.pulsante_negozio = ft.ElevatedButton(
                text="Negozio",
                on_click=lambda e: self.page.go("/negozio"),
                width=280,
                height=50,
                bgcolor=ft.Colors.ORANGE_600,
                color=ft.Colors.WHITE,
                tooltip="Visita il negozio"
            )

            self.pulsante_gatti = ft.ElevatedButton(
                text="Gatti",
                on_click=lambda e: self.page.go("/gatti"),
                width=280,
                height=50,
                bgcolor=ft.Colors.PINK_600,
                color=ft.Colors.WHITE,
                tooltip="Gestisci i tuoi gatti"
            )

            self.pulsante_salva = ft.ElevatedButton(
                text="Salva Partita",
                on_click=self.salva_gioco,
                width=280,
                height=50,
                bgcolor=ft.Colors.PURPLE_600,
                color=ft.Colors.WHITE,
                tooltip="Salva il tuo progresso"
            )

        pulsanti_gioco.extend([
            self.pulsante_combattimento,
            self.pulsante_negozio,
            self.pulsante_gatti
        ])

        # 🔁 Condizionale: pulsante aree
        if len(self.aree_sbloccate) > 1:
            pulsanti_gioco.append(
                ft.ElevatedButton(
                    text="Cambia Area",
                    on_click=lambda e: self.page.go("/aree"),
                    width=280,
                    height=50,
                    bgcolor=ft.Colors.BLUE_600,
                    color=ft.Colors.WHITE,
                    tooltip="Scegli area da esplorare"
                )
            )

        # 🔁 Condizionale: boss
        if (self.area_attuale in self.boss_aree and
            self.boss_aree[self.area_attuale]["nome"] not in self.boss_sconfitti and
            self.progressione_area.get(self.area_attuale, 0) >= 100):
            pulsanti_gioco.append(
                ft.ElevatedButton(
                    text="Combatti Boss dell'Area!",
                    on_click=self.combatti_boss,
                    width=280,
                    height=50,
                    bgcolor=ft.Colors.DEEP_PURPLE_600,
                    color=ft.Colors.WHITE,
                    tooltip=f"Affronta il boss: {self.boss_aree[self.area_attuale]['nome']}"
                )
            )

        # ✅ Pulsante salva (già creato sopra)
        pulsanti_gioco.append(self.pulsante_salva)

        # 🔁 Colonna pulsanti in ListView per performance
        colonna_pulsanti = ft.Column(
            pulsanti_gioco,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )

        # ✅ Usa ListView scrollabile per evitare lag
        area_gioco_scrollabile = ft.ListView(
            controls=[
                self.area_storia,
                self.area_stats,
                colonna_pulsanti
            ],
            expand=True,
            spacing=10,
            padding=10
        )

        # Pulsante menu
        pulsante_menu = ft.ElevatedButton(
            text="Torna al Menu",
            on_click=lambda e: self.page.go("/"),
            width=200,
            height=50,
            bgcolor=ft.Colors.GREY_600,
            color=ft.Colors.WHITE,
            tooltip="Torna al menu principale"
        )

        # ✅ Layout finale
        content = ft.Column([
            titolo,
            ft.Container(
                content=area_gioco_scrollabile,
                bgcolor=ft.Colors.GREY_800,
                border_radius=10,
                expand=True
            ),
            pulsante_menu
        ], spacing=30, expand=True)

        return ft.View(
            "/gioco",
            controls=[
                ft.Container(
                    content=content,
                    bgcolor=ft.Colors.GREY_900,
                    padding=20,
                    expand=True
                )
            ],
            bgcolor=ft.Colors.GREY_900
        )

    def crea_vista_gioco_NonOttimizzata(self):
        """Vista con paginazione per migliore performance"""
        titolo = ft.Text("AVVENTURA EPICA", size=24, weight=ft.FontWeight.BOLD)
        
        # Valori dinamici
        valore_storia = "🎮 Benvenuto nell'Avventura Incrementale!"
        if hasattr(self, 'area_storia') and self.area_storia and hasattr(self.area_storia, 'value'):
            valore_storia = self.area_storia.value
        
        valore_stats = f" Statistiche Giocatore:\n Livello {self.livello} •  {self.vita}/{self.vita_massima} HP •  {self.monete} monete\n Attacco: {self.calcola_attacco_totale()} •  Difesa: {self.calcola_difesa_totale()}\n EXP: {self.esperienza}/{self.esperienza_necessaria}"
        if hasattr(self, 'area_stats') and self.area_stats and hasattr(self.area_stats, 'value'):
            valore_stats = self.area_stats.value
        
        # TextField
        area_storia_locale = ft.TextField(
            value=valore_storia,
            multiline=True,
            read_only=True,
            expand=True,
            min_lines=10,
            max_lines=15,
            text_size=14,
            bgcolor=ft.Colors.DEEP_PURPLE_900,
            color=ft.Colors.AMBER_100,
            border_color=ft.Colors.AMBER_400,
            focused_border_color=ft.Colors.AMBER_300,
            label="Storia dell'avventura"
        )
        
        area_stats_locale = ft.TextField(
            value=valore_stats,
            multiline=True,
            read_only=True,
            min_lines=4,
            max_lines=6,
            text_size=14,
            bgcolor=ft.Colors.BLUE_GREY_900,
            color=ft.Colors.CYAN_100,
            border_color=ft.Colors.CYAN_400,
            focused_border_color=ft.Colors.CYAN_300,
            label="Statistiche giocatore"
        )
        
        self.area_storia = area_storia_locale
        self.area_stats = area_stats_locale
        
        # SOLUZIONE: Crea solo i pulsanti ESSENZIALI (max 4-5)
        pulsanti_essenziali = []
        
        # Azioni incrementali - prendi solo le prime 2-3
        azioni_incrementali = self.azioni_incrementali_possibili()
        for i, (testo, funzione, tooltip) in enumerate(azioni_incrementali[:3]):
            pulsante = ft.ElevatedButton(
                text=testo,
                on_click=funzione,
                width=280,
                height=50,
                bgcolor=ft.Colors.GREEN_600,
                color=ft.Colors.WHITE,
                tooltip=tooltip
            )
            pulsanti_essenziali.append(pulsante)
        
        # Se ci sono più azioni, aggiungi pulsante "Altre Azioni"
        if len(azioni_incrementali) > 3:
            pulsante_altre_azioni = ft.ElevatedButton(
                text=f"Altre {len(azioni_incrementali) - 3} Azioni...",
                on_click=lambda e: self.mostra_menu_azioni_extra(e),
                width=280,
                height=50,
                bgcolor=ft.Colors.GREY_600,
                color=ft.Colors.WHITE,
                tooltip="Mostra altre azioni disponibili"
            )
            pulsanti_essenziali.append(pulsante_altre_azioni)
        
        # Pulsanti navigazione in un Row orizzontale (più compatto)
        pulsanti_nav = ft.Row([
            ft.ElevatedButton(
                text="Combattimento",
                icon=ft.Icons.SPORTS_KABADDI,
                icon_color=ft.Colors.RED_400,
                on_click=lambda e: self.page.go("/combattimento"),
                bgcolor=ft.Colors.RED_600,
                color=ft.Colors.WHITE,
                tooltip="Vai al combattimento"
            ),
            ft.ElevatedButton(
                text="Negozio",
                icon=ft.Icons.STORE,
                icon_color=ft.Colors.ORANGE_400,
                on_click=lambda e: self.page.go("/negozio"),
                bgcolor=ft.Colors.ORANGE_600,
                color=ft.Colors.WHITE,
                tooltip="Vai al negozio"
            ),
            ft.ElevatedButton(
                text="Gatti",
                icon=ft.Icons.PETS,
                icon_color=ft.Colors.PINK_400,
                on_click=lambda e: self.page.go("/gatti"),
                bgcolor=ft.Colors.PINK_600,
                color=ft.Colors.WHITE,
                tooltip="Gestisci i tuoi gatti"
            ),
            ft.ElevatedButton(
                text="Salva",
                icon=ft.Icons.SAVE,
                icon_color=ft.Colors.PURPLE_400,
                on_click=self.salva_gioco,
                bgcolor=ft.Colors.PURPLE_600,
                color=ft.Colors.WHITE,
                tooltip="Salva la partita"
            )
        ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
        
        # Container per navigazione
        container_nav = ft.Container(
            content=pulsanti_nav,
            bgcolor=ft.Colors.GREY_800,
            border_radius=10,
            padding=10,
            margin=ft.margin.only(top=10)
        )
        
        # Controlli principali
        gioco_controls = [
            area_storia_locale,
            area_stats_locale,
            ft.Column(pulsanti_essenziali, spacing=10),  # Solo pulsanti essenziali
            container_nav  # Navigazione compatta
        ]
        
        # Pulsante menu
        pulsante_menu = ft.ElevatedButton(
            text="Torna al Menu Principale",
            icon=ft.Icons.HOME,
            icon_color=ft.Colors.GREY_400,
            on_click=lambda e: self.page.go("/"),
            bgcolor=ft.Colors.GREY_600,
            color=ft.Colors.WHITE,
            tooltip="Torna al menu principale"
        )
        
        # Layout finale senza scroll
        content = ft.Column([
            ft.Row([
                titolo,
                pulsante_menu
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(
                content=ft.Column(gioco_controls, spacing=10),
                bgcolor=ft.Colors.GREY_800,
                border_radius=10,
                padding=10,
                expand=True
            )
        ], spacing=20, expand=True)
        
        return ft.View(
            "/gioco",
            controls=[
                ft.Container(
                    content=content,
                    bgcolor=ft.Colors.GREY_900,
                    padding=20,
                    expand=True
                )
            ],
            bgcolor=ft.Colors.GREY_900
        )

    def mostra_menu_azioni_extra(self, e):
        """Mostra un dialog con le azioni extra"""
        azioni_incrementali = self.azioni_incrementali_possibili()
        azioni_extra = azioni_incrementali[3:]  # Salta le prime 3
        
        pulsanti_dialog = []
        for testo, funzione, tooltip in azioni_extra:
            def crea_handler(f):
                def handler(e):
                    self.page.close(dlg)
                    f(e)
                return handler
            
            pulsante = ft.TextButton(
                text=testo,
                on_click=crea_handler(funzione)
            )
            pulsanti_dialog.append(pulsante)
        
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Altre Azioni", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Column(
                pulsanti_dialog,
                tight=True,
                scroll=ft.ScrollMode.AUTO,
                height=300,
                spacing=10
            ),
            actions=[
                ft.TextButton("Chiudi", on_click=lambda e: self.page.close(dlg))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.open(dlg)
        print(f"🎮 DEBUG: Dialog azioni extra aperto")
    def crea_vista_gioco_vecchia(self):
        """Crea la vista principale di gioco"""
        # Crea tutte le variabili locali per evitare il problema dell'elemento vuoto in VoiceOver
        titolo = ft.Text(
            "AVVENTURA IN CORSO", 
            size=24, 
            weight=ft.FontWeight.BOLD, 
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.AMBER_400,
            semantics_label="Avventura in corso",
            style=ft.TextThemeStyle.HEADLINE_MEDIUM
        )
        
        # Ottieni i valori attuali dalle variabili globali se esistono
        valore_storia = "🎮 Benvenuto nell'Avventura Incrementale!\n Compagni gatti con abilità speciali\n Raccogli risorse e costruisci\n Combatti mostri e sali di livello\n🍽️ Gestisci cibo e acqua per energia\n🎵 Audio immersivo e feedback aptico\n\nPremi 'Inizia Avventura' per cominciare!"
        if hasattr(self, 'area_storia') and self.area_storia and hasattr(self.area_storia, 'value'):
            valore_storia = self.area_storia.value
        
        valore_stats = f" Statistiche Giocatore:\n Livello {self.livello} •  {self.vita}/{self.vita_massima} HP •  {self.monete} monete\n Attacco: {self.calcola_attacco_totale()} •  Difesa: {self.calcola_difesa_totale()}\n EXP: {self.esperienza}/{self.esperienza_necessaria}"
        if hasattr(self, 'area_stats') and self.area_stats and hasattr(self.area_stats, 'value'):
            valore_stats = self.area_stats.value
        
        # Crea controlli locali per VoiceOver accessibility
        area_storia_locale = ft.Container(
            content=ft.Text(
                valore_storia,
                size=14,
                color=ft.Colors.AMBER_100
            ),
            bgcolor=ft.Colors.DEEP_PURPLE_900,
            border_radius=5,
            padding=10,
            expand=True
        )

        area_stats_locale = ft.Container(
            content=ft.Text(
                valore_stats,
                size=14,
                color=ft.Colors.CYAN_100
            ),
            bgcolor=ft.Colors.BLUE_GREY_900,
            border_radius=5,
            padding=10
        )
        # Aggiorna i riferimenti globali per mantenere la sincronizzazione
        self.area_storia = area_storia_locale
        self.area_stats = area_stats_locale
        
        # Crea pulsanti locali per evitare problemi VoiceOver
        pulsanti_gioco = []
        
        # Azioni incrementali - variabili locali
        azioni_incrementali = self.azioni_incrementali_possibili()
        for testo, funzione, tooltip in azioni_incrementali:
            pulsante_incrementale = ft.ElevatedButton(
                text=testo,
                on_click=funzione,
                width=280,
                height=50,
                bgcolor=ft.Colors.GREEN_600,
                color=ft.Colors.WHITE,
                tooltip=tooltip
            )
            pulsanti_gioco.append(pulsante_incrementale)
        
        # Pulsante cambio area - variabile locale
        if len(self.aree_sbloccate) > 1:
            pulsante_aree = ft.ElevatedButton(
                text="Cambia Area",
                on_click=lambda e: self.page.go("/aree"),
                width=280,
                height=50,
                bgcolor=ft.Colors.BLUE_600,
                color=ft.Colors.WHITE,
                tooltip="Scegli area da esplorare"
            )
            pulsanti_gioco.append(pulsante_aree)
        
        # Pulsanti di navigazione - variabili locali
        pulsante_combattimento = ft.ElevatedButton(
            text="Combattimento",
            on_click=lambda e: self.page.go("/combattimento"),
            width=280,
            height=50,
            bgcolor=ft.Colors.RED_600,
            color=ft.Colors.WHITE,
            tooltip="Combatti contro i mostri"
        )
        
        pulsante_negozio = ft.ElevatedButton(
            text="Negozio",
            on_click=lambda e: self.page.go("/negozio"),
            width=280,
            height=50,
            bgcolor=ft.Colors.ORANGE_600,
            color=ft.Colors.WHITE,
            tooltip="Visita il negozio"
        )
        
        pulsante_gatti = ft.ElevatedButton(
            text="Gatti",
            on_click=lambda e: self.page.go("/gatti"),
            width=280,
            height=50,
            bgcolor=ft.Colors.PINK_600,
            color=ft.Colors.WHITE,
            tooltip="Gestisci i tuoi gatti"
        )
        
        pulsanti_gioco.extend([pulsante_combattimento, pulsante_negozio, pulsante_gatti])
        
        # Pulsante boss - variabile locale
        if (self.area_attuale in self.boss_aree and 
            self.boss_aree[self.area_attuale]["nome"] not in self.boss_sconfitti and
            self.progressione_area.get(self.area_attuale, 0) >= 100):
            pulsante_boss = ft.ElevatedButton(
                text="Combatti Boss dell'Area!",
                on_click=self.combatti_boss,
                width=280,
                height=50,
                bgcolor=ft.Colors.DEEP_PURPLE_600,
                color=ft.Colors.WHITE,
                tooltip=f"Affronta il boss: {self.boss_aree[self.area_attuale]['nome']}"
            )
            pulsanti_gioco.append(pulsante_boss)
        
        # Pulsante salva - variabile locale
        pulsante_salva = ft.ElevatedButton(
            text="Salva Partita",
            on_click=self.salva_gioco,
            width=280,
            height=50,
            bgcolor=ft.Colors.PURPLE_600,
            color=ft.Colors.WHITE,
            tooltip="Salva il tuo progresso"
        )
        pulsanti_gioco.append(pulsante_salva)
        
        # Colonna pulsanti - variabile locale
        colonna_pulsanti = ft.Column(pulsanti_gioco, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)
        
        # Controlli di gioco - variabile locale
        gioco_controls = [
            area_storia_locale,
            area_stats_locale,
            colonna_pulsanti
        ]
        
        # Pulsante menu - variabile locale
        pulsante_menu = ft.ElevatedButton(
            text="Torna al Menu",
            on_click=lambda e: self.page.go("/"),
            width=200,
            height=50,
            bgcolor=ft.Colors.GREY_600,
            color=ft.Colors.WHITE,
            tooltip="Torna al menu principale"
        )
        
        # Content principale - variabile locale  
        content = ft.Column([
            titolo,
            ft.Container(
                content=ft.Column(gioco_controls, spacing=10),
                bgcolor=ft.Colors.GREY_800,
                border_radius=10,
                padding=10,
                height=800
            ),
            pulsante_menu
        ], scroll=ft.ScrollMode.AUTO, spacing=30, expand=True)
        
        return ft.View(
            "/gioco",
            controls=[
                ft.Container(
                    content=content,
                    bgcolor=ft.Colors.GREY_900,
                    padding=20,
                    expand=True
                )
            ],
            bgcolor=ft.Colors.GREY_900
        )
    
    def crea_vista_impostazioni(self):
        """Crea la vista delle impostazioni"""
        titolo = ft.Text(
            "Impostazioni", 
            size=24, 
            weight=ft.FontWeight.BOLD, 
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.PURPLE_400
        )
        
        # Crea contenuto impostazioni direttamente qui (come fa inventario)
        # Toggle audio e haptic
        toggle_audio = ft.Switch(
            label="Audio Attivato",
            value=self.audio_abilitato,
            on_change=self.toggle_audio_callback,
            tooltip="Attiva o disattiva tutti gli effetti audio"
        )
        
        toggle_haptic = ft.Switch(
            label="Vibrazione Attivata",
            value=self.haptic_abilitato,
            on_change=self.toggle_haptic_callback,
            tooltip="Attiva o disattiva il feedback aptico"
        )
        
        # Slider volume musica per tab
        self.volume_musica_label_tab = ft.Text(f"Volume Musica: {int(self.volume_musica * 100)}%")
        slider_volume_musica = ft.Slider(
            min=0,
            max=1,
            value=self.volume_musica,
            divisions=10,
            on_change=self.cambia_volume_musica_tab,
            tooltip="Regola il volume della musica di sottofondo"
        )
        
        # Slider volume effetti per tab
        self.volume_effetti_label_tab = ft.Text(f"Volume Effetti: {int(self.volume_effetti * 100)}%")
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
            "Testa Audio",
            on_click=self.testa_audio,
            width=200,
            tooltip="Riproduci un suono di test"
        )
        
        impostazioni_controls = [
            ft.Text("Audio", size=16, weight=ft.FontWeight.BOLD),
            toggle_audio,
            self.volume_musica_label_tab,
            slider_volume_musica,
            self.volume_effetti_label_tab,
            slider_volume_effetti,
            test_audio_btn,
            ft.Divider(),
            ft.Text("Feedback", size=16, weight=ft.FontWeight.BOLD),
            toggle_haptic,
        ]
        
        content = ft.Column([
            titolo,
            ft.Container(
                content=ft.Column(impostazioni_controls, spacing=15),
                height=400,
                bgcolor=ft.Colors.GREY_800,
                border_radius=10,
                padding=10
            ),
            self.crea_pulsante_indietro()
        ], scroll=ft.ScrollMode.AUTO, spacing=30, expand=True)
        
        return ft.View(
            "/impostazioni",
            controls=[
                ft.Container(
                    content=content,
                    bgcolor=ft.Colors.GREY_900,
                    padding=20,
                    expand=True
                )
            ],
            bgcolor=ft.Colors.GREY_900
        )
    
    def crea_vista_info(self):
        """Crea la vista delle informazioni"""
        titolo = ft.Text(
            "Info Gioco", 
            size=24, 
            weight=ft.FontWeight.BOLD, 
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.ORANGE_400
        )
        
        # Crea contenuto info direttamente qui (come fa inventario)
        info_controls = [
            ft.Text("AVVENTURA EPICA", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Text(f" Versione: {self.versione}", size=16),
            ft.Text(f"Autore: {self.autore}", size=16),
            ft.Text("Data rilascio: 18 giugno 2025", size=16),
            ft.Text("Descrizione:", size=16, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Un emozionante RPG accessibile con audio immersivo e feedback aptico. "
                "Esplora 16 aree diverse, combatti mostri, raccogli tesori, visita negozi "
                "e diventa il nuovo re!",
                size=14,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Text("Caratteristiche:", size=16, weight=ft.FontWeight.BOLD),
            ft.Text("16 aree uniche da esplorare", size=14),
            ft.Text("Sistema di combattimento con livellamento", size=14),
            ft.Text("Negozi e mercanti", size=14),
            ft.Text("Sistema di inventario ed equipaggiamento", size=14),
            ft.Text("Audio immersivo per ogni area", size=14),
            ft.Text("Feedback aptico per un'esperienza tattile", size=14),
            ft.Text("Salvataggio e caricamento partite", size=14),
            ft.Text("Completamente accessibile con screen reader", size=14),
        ]
        
        content = ft.Column([
            titolo,
            ft.Container(
                content=ft.Column(info_controls, spacing=20),
                height=400,
                bgcolor=ft.Colors.GREY_800,
                border_radius=10,
                padding=10
            ),
            self.crea_pulsante_indietro()
        ], scroll=ft.ScrollMode.AUTO, spacing=30, expand=True)
        
        return ft.View(
            "/info",
            controls=[
                ft.Container(
                    content=content,
                    bgcolor=ft.Colors.GREY_900,
                    padding=20,
                    expand=True
                )
            ],
            bgcolor=ft.Colors.GREY_900
        )
    
    def crea_vista_aree(self):
        """Crea la vista di selezione aree"""
        titolo = ft.Text(
            "Scegli Area", 
            size=24, 
            weight=ft.FontWeight.BOLD, 
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.BLUE_400
        )
        
        pulsanti_aree = []
        
        for area in self.aree_sbloccate:
            if area == self.area_attuale:
                testo = f"{area} (ATTUALE)"
                colore = ft.Colors.GREEN_600
            else:
                testo = f"{area}"
                colore = ft.Colors.BLUE_600
            
            pulsanti_aree.append(
                ft.ElevatedButton(
                    text=testo,
                    on_click=lambda e, area_target=area: self.seleziona_area_e_torna(e, area_target),
                    width=280,
                    height=50,
                    bgcolor=colore,
                    color=ft.Colors.WHITE,
                    tooltip=f"Vai a {area}"
                )
            )
        
        pulsanti_aree.append(self.crea_pulsante_indietro())
        
        content = ft.Column([
            titolo,
            ft.Container(height=20),
            ft.Column(pulsanti_aree, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)
        ], scroll=ft.ScrollMode.AUTO, spacing=20, expand=True)
        
        return ft.View(
            "/aree",
            controls=[
                ft.Container(
                    content=content,
                    bgcolor=ft.Colors.GREY_900,
                    padding=20,
                    expand=True
                )
            ],
            bgcolor=ft.Colors.GREY_900
        )
    
    def crea_vista_combattimento(self):
        """Crea la vista del combattimento"""
        # Crea tutte le variabili locali per evitare il problema dell'elemento vuoto in VoiceOver
        titolo = ft.Text(
            "Combattimento", 
            size=24, 
            weight=ft.FontWeight.BOLD, 
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.RED_400
        )
        
        # Info mostro - salva riferimento per aggiornamenti
        if self.mostro_attuale:
            self.info_mostro_combattimento = ft.Text(
                f"{self.mostro_attuale['nome']}\n HP: {self.hp_mostro_attuale}/{self.mostro_attuale['hp']}\n Attacco: {self.mostro_attuale['attacco']}", 
                size=18, 
                text_align=ft.TextAlign.CENTER,
                color=ft.Colors.ORANGE_300,
                semantics_label=f"Nemico: {self.mostro_attuale['nome']}, Punti vita {self.hp_mostro_attuale} su {self.mostro_attuale['hp']}, Attacco {self.mostro_attuale['attacco']}"
            )
        else:
            self.info_mostro_combattimento = ft.Text(
                "Nessun mostro in vista\nClicca 'Cerca Mostri' per iniziare una battaglia!", 
                size=16, 
                text_align=ft.TextAlign.CENTER,
                color=ft.Colors.GREY_400,
                semantics_label="Nessun nemico presente. Cerca mostri per iniziare una battaglia"
            )
        info_mostro = self.info_mostro_combattimento
        
        # Info giocatore - salva riferimento per aggiornamenti
        gatto_info = self.gatti[self.gatto_attivo]
        self.info_giocatore_combattimento = ft.Text(
            f"{gatto_info['nome']}\n Vita: {self.vita}/{self.vita_massima}\n Attacco: {self.calcola_attacco_totale()}\n Energia: {self.risorse['energia']}", 
            size=18, 
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.GREEN_300,
            semantics_label=f"Giocatore: {gatto_info['nome']}, Vita {self.vita} su {self.vita_massima}, Attacco {self.calcola_attacco_totale()}, Energia {self.risorse['energia']}"
        )
        info_giocatore = self.info_giocatore_combattimento
        
        # Log combattimento - salva riferimento per aggiornamenti
        valore_log = "Preparati al combattimento!"
        self.log_combattimento_campo = ft.TextField(
            value=valore_log,
            multiline=True,
            read_only=True,
            expand=True,
            min_lines=8,
            max_lines=12,
            text_size=14,
            bgcolor=ft.Colors.DEEP_ORANGE_900,
            color=ft.Colors.AMBER_100,
            border_color=ft.Colors.RED_400,
            focused_border_color=ft.Colors.RED_300,
            label="Log del combattimento",
            hint_text="Cronologia delle azioni di combattimento"
        )
        log_combattimento_locale = self.log_combattimento_campo
        
        # Pulsanti combattimento - array locale
        pulsanti_combattimento = []
        oggetti_curativi_disponibili = self.conta_oggetti_curativi()
        
        print(f"🎮 DEBUG: Creando pulsanti combattimento - in_combattimento = {self.in_combattimento}")
        
        if self.in_combattimento:
            print(f"🎮 DEBUG: Aggiungendo pulsanti Attacca e Difendi")
            pulsanti_combattimento.extend([
                ft.ElevatedButton(
                    text="Attacca",
                    on_click=self.attacca_mostro,
                    width=200,
                    height=50,
                    bgcolor=ft.Colors.RED_600,
                    color=ft.Colors.WHITE,
                    tooltip=f"Attacca il {self.mostro_attuale['nome'] if self.mostro_attuale else 'mostro'}",
                    data="attacca"
                ),
                ft.ElevatedButton(
                    text="Difendi",
                    on_click=self.difendi_combattimento,
                    width=200,
                    height=50,
                    bgcolor=ft.Colors.BLUE_600,
                    color=ft.Colors.WHITE,
                    tooltip="Riduci il danno subito del 50%",
                    data="difendi"
                ),
                ft.ElevatedButton(
                    text=f"Usa Oggetto Curativo ({oggetti_curativi_disponibili})",
                    on_click=self.usa_pozione_combattimento,
                    width=200,
                    height=50,
                    bgcolor=ft.Colors.GREEN_600 if oggetti_curativi_disponibili > 0 else ft.Colors.GREY_600,
                    color=ft.Colors.WHITE,
                    tooltip=f"Usa oggetti curativi. Disponibili: {oggetti_curativi_disponibili}",
                    disabled=oggetti_curativi_disponibili <= 0,
                    data="pozione"
                ),
                ft.ElevatedButton(
                    text="Fuggi",
                    on_click=self.fuggi_combattimento,
                    width=200,
                    height=50,
                    bgcolor=ft.Colors.PURPLE_600,
                    color=ft.Colors.WHITE,
                    tooltip="Tenta di fuggire dal combattimento. 70% di successo",
                    data="fuggi"
                )
            ])
        else:
            print(f"🎮 DEBUG: Non in combattimento - in_battaglia={getattr(self, 'in_battaglia', False)}, mostro_attuale={self.mostro_attuale}")
            if not self.in_battaglia and not self.in_combattimento and self.mostro_attuale is None:
                print(f"🎮 DEBUG: Aggiungendo pulsante Cerca Mostri")
                pulsanti_combattimento.append(
                    ft.ElevatedButton(
                        text="Cerca Mostri",
                        on_click=self.inizia_combattimento,
                        width=200,
                        height=50,
                        bgcolor=ft.Colors.ORANGE_600,
                        color=ft.Colors.WHITE,
                        tooltip="Cerca mostri da combattere"
                    )
                )
        
        # Pulsante indietro - variabile locale
        pulsante_indietro = ft.ElevatedButton(
            text="Torna al Gioco",
            on_click=lambda e: self.page.go("/gioco"),
            width=200,
            height=50,
            bgcolor=ft.Colors.GREY_600,
            color=ft.Colors.WHITE,
            tooltip="Torna alla schermata principale"
        )
        
        # Content principale - variabile locale
        content = ft.Column([
            titolo,
            ft.Container(
                content=ft.Column([
                    info_mostro,
                    info_giocatore,
                    log_combattimento_locale,
                    ft.Column(pulsanti_combattimento, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
                ], spacing=25, scroll=ft.ScrollMode.AUTO),
                bgcolor=ft.Colors.GREY_800,
                border_radius=10,
                padding=10,
                expand=True
            ),
            pulsante_indietro
        ], spacing=30, expand=True)
        
        return ft.View(
            "/combattimento",
            controls=[
                ft.Container(
                    content=content,
                    bgcolor=ft.Colors.GREY_900,
                    padding=20,
                    expand=True
                )
            ],
            bgcolor=ft.Colors.GREY_900
        )
    
    def crea_vista_negozio(self):
        """Crea la vista del negozio"""
        titolo = ft.Text(
            "Negozio", 
            size=24, 
            weight=ft.FontWeight.BOLD, 
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.ORANGE_400
        )
        
        # Crea contenuto negozio direttamente qui (come fa inventario)
        self.testo_monete_negozio = ft.Text(f"Monete disponibili: {self.monete}", size=16, color=ft.Colors.AMBER_400)
        
        # Create shop items localmente
        oggetti_negozio = [
            {"nome": "Pozione Vita", "prezzo": 50, "descrizione": "Ripristina 30 HP"},
            {"nome": "Spada di Ferro", "prezzo": 200, "descrizione": "Attacco +10"},
            {"nome": "Armatura di Cuoio", "prezzo": 150, "descrizione": "Difesa +5"},
            {"nome": "Anello della Fortuna", "prezzo": 300, "descrizione": "Esperienza +20%"}
        ]
        
        oggetti_controls = []
        for oggetto in oggetti_negozio:
            pulsante_acquista = ft.ElevatedButton(
                text="Acquista",
                on_click=lambda e, obj=oggetto: self.acquista_oggetto_negozio(obj),
                bgcolor=ft.Colors.GREEN_600,
                color=ft.Colors.WHITE,
                tooltip=f"Acquista {oggetto['nome']}: {oggetto['descrizione']}"
            )
            
            oggetto_card = ft.Container(
                content=ft.Column([
                    ft.Text(oggetto['nome'], size=18, weight=ft.FontWeight.BOLD),
                    ft.Text(oggetto['descrizione'], size=14),
                    ft.Text(f"Prezzo: {oggetto['prezzo']} monete", size=12, color=ft.Colors.AMBER_400),
                    pulsante_acquista
                ], spacing=5),
                bgcolor=ft.Colors.GREY_800,
                border_radius=10,
                padding=15,
                margin=5
            )
            oggetti_controls.append(oggetto_card)
        
        negozio_controls = [
            self.testo_monete_negozio,
            ft.Column(oggetti_controls, spacing=10)
        ]
        
        content = ft.Column([
            titolo,
            ft.Container(
                content=ft.Column(negozio_controls, spacing=20),
                height=400,
                bgcolor=ft.Colors.GREY_800,
                border_radius=10,
                padding=10
            ),
            self.crea_pulsante_indietro()
        ], scroll=ft.ScrollMode.AUTO, spacing=30, expand=True)
        
        return ft.View(
            "/negozio",
            controls=[
                ft.Container(
                    content=content,
                    bgcolor=ft.Colors.GREY_900,
                    padding=20,
                    expand=True
                )
            ],
            bgcolor=ft.Colors.GREY_900
        )
    
    def acquista_oggetto_negozio(self, oggetto):
        """Gestisce l'acquisto di un oggetto dal negozio"""
        prezzo = oggetto['prezzo']
        nome = oggetto['nome']
        
        if self.monete >= prezzo:
            self.monete -= prezzo
            
            # Aggiungi oggetto all'inventario (semplificato)
            if nome not in self.inventario:
                self.inventario[nome] = 0
            self.inventario[nome] += 1
            
            self.aggiorna_storia(f"💰 Hai acquistato {nome} per {prezzo} monete!")
            self.haptic_feedback("success")
            if self.audio_abilitato:
                self.riproduci_effetto("monete")
            # Aggiorna il display delle monete
            if hasattr(self, 'testo_monete_negozio'):
                self.testo_monete_negozio.value = f"Monete disponibili: {self.monete}"
                self.page.update()
        else:
            self.aggiorna_storia(f"❌ Non hai abbastanza monete per {nome} (servono {prezzo}, ne hai {self.monete})")
            self.haptic_feedback("error")
    
    def crea_vista_gatti(self):
        """Crea la vista di gestione gatti"""
        titolo = ft.Text(
            "Gestione Gatti", 
            size=24, 
            weight=ft.FontWeight.BOLD, 
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.PINK_400
        )
        
        sottotitolo = ft.Text(
            "Scegli il tuo gatto attivo tra quelli disponibili",
            size=16,
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.GREY_400
        )
        
        # Lista gatti
        gatti_controls = []
        
        for gatto_id, gatto_info in self.gatti.items():
            if not gatto_info.get("sbloccato", False):
                continue
                
            nome = gatto_info["nome"]
            emoji = gatto_info["emoji"]
            livello = gatto_info["livello"]
            abilita = gatto_info["abilita"]
            affinita = gatto_info["affinita"]
            felicita = gatto_info["felicita"]
            
            # Indica se è il gatto attivo
            is_attivo = gatto_id == self.gatto_attivo
            
            def crea_handler_gatto(gatto_target):
                """Crea handler per selezionare il gatto specifico"""
                return lambda e: self.seleziona_gatto_attivo(gatto_target)
            
            # Colore basato sullo stato
            if is_attivo:
                colore_sfondo = ft.Colors.GREEN_600
                testo_stato = "ATTIVO"
            else:
                colore_sfondo = ft.Colors.BLUE_600
                testo_stato = "Seleziona"
            
            # Descrizione accessibile del gatto
            descrizione_accessibile = f"Gatto {nome}, livello {livello}, abilità {abilita}, affinità {affinita}, felicità {felicita}"
            if is_attivo:
                descrizione_accessibile += ", attualmente attivo"
            
            gatto_card = ft.Container(
                content=ft.Column([
                    ft.Text(f"{emoji} {nome}", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    ft.Text(f"Livello: {livello} | Abilità: {abilita}", size=14, text_align=ft.TextAlign.CENTER),
                    ft.Text(f"Affinità: {affinita}/100 | Felicità: {felicita}/100", size=12, text_align=ft.TextAlign.CENTER),
                    ft.ElevatedButton(
                        text=testo_stato,
                        on_click=crea_handler_gatto(gatto_id),
                        bgcolor=colore_sfondo,
                        color=ft.Colors.WHITE,
                        disabled=is_attivo,
                        tooltip=f"Seleziona {nome} come gatto attivo"
                    )
                ], spacing=5),
                bgcolor=ft.Colors.GREY_800,
                border_radius=10,
                padding=15,
                margin=5
            )
            
            gatti_controls.append(gatto_card)
        
        if not gatti_controls:
            gatti_controls.append(
                ft.Text(
                    "Nessun gatto sbloccato",
                    size=16,
                    text_align=ft.TextAlign.CENTER,
                    color=ft.Colors.GREY_400,
                    semantics_label="Nessun gatto disponibile al momento. Continua a giocare per sbloccare nuovi gatti compagni."
                )
            )
        
        # Contenitore scrollabile per i gatti
        gatti_container = ft.Column([
            ft.Text(
                "Lista gatti disponibili",
                semantics_label="Lista gatti disponibili, scorri per vedere tutti i gatti",
                visible=False
            ),
            ft.Container(
                content=ft.Column(gatti_controls, spacing=10),
                height=400,
                bgcolor=ft.Colors.GREY_800,
                border_radius=10,
                padding=10
            )
        ])
        
        # Pulsanti aggiuntivi
        pulsanti_azioni = []
        
        if self.gatto_attivo and self.gatti[self.gatto_attivo].get("sbloccato", False):
            pulsanti_azioni.extend([
                ft.ElevatedButton(
                    text="Rinomina Gatto Attivo",
                    on_click=lambda e: self.page.go("/rinomina_gatto"),
                    width=250,
                    height=50,
                    bgcolor=ft.Colors.PURPLE_600,
                    color=ft.Colors.WHITE,
                    tooltip="Rinomina il gatto attualmente selezionato"
                ),
                ft.ElevatedButton(
                    text="Gestisci Reliquie",
                    on_click=lambda e: self.page.go("/gestione_reliquie"),
                    width=250,
                    height=50,
                    bgcolor=ft.Colors.AMBER_600,
                    color=ft.Colors.WHITE,
                    tooltip="Gestisci le reliquie equipaggiate"
                )
            ])
        
        content = ft.Column([
            titolo,
            ft.Container(
                content=ft.Column([
                    sottotitolo,
                    gatti_container,
                    ft.Column(pulsanti_azioni, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
                ], spacing=30),
                height=400,
                bgcolor=ft.Colors.GREY_800,
                border_radius=10,
                padding=10
            ),
            self.crea_pulsante_indietro()
        ], scroll=ft.ScrollMode.AUTO, spacing=30, expand=True)
        
        return ft.View(
            "/gatti",
            controls=[
                ft.Container(
                    content=content,
                    bgcolor=ft.Colors.GREY_900,
                    padding=20,
                    expand=True
                )
            ],
            bgcolor=ft.Colors.GREY_900
        )
    
    def crea_vista_inventario(self):
        """Crea la vista dell'inventario"""
        titolo = ft.Text(
            "Inventario", 
            size=24, 
            weight=ft.FontWeight.BOLD, 
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.CYAN_400
        )
        
        # Lista oggetti inventario
        oggetti_controls = []
        
        if not self.inventario:
            oggetti_controls.append(
                ft.Text(
                    "Inventario vuoto",
                    size=16,
                    text_align=ft.TextAlign.CENTER,
                    color=ft.Colors.GREY_400
                )
            )
        else:
            for oggetto, quantita in self.inventario.items():
                oggetti_controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Text(f"{oggetto} (x{quantita})", size=16, expand=True),
                            ft.ElevatedButton(
                                text="Usa",
                                on_click=lambda e, obj=oggetto: self.usa_oggetto_inventario(obj),
                                width=80,
                                height=40,
                                bgcolor=ft.Colors.GREEN_600,
                                color=ft.Colors.WHITE,
                                tooltip=f"Usa {oggetto}"
                            ),
                            ft.ElevatedButton(
                                text="Equipaggia",
                                on_click=lambda e, obj=oggetto: self.equipaggia_oggetto_inventario(obj),
                                width=100,
                                height=40,
                                bgcolor=ft.Colors.BLUE_600,
                                color=ft.Colors.WHITE,
                                tooltip=f"Equipaggia {oggetto}"
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        bgcolor=ft.Colors.GREY_800,
                        border_radius=10,
                        padding=15,
                        margin=5
                    )
                )
        
        content = ft.Column([
            titolo,
            ft.Container(
                content=ft.Column(oggetti_controls, spacing=10),
                height=400,
                bgcolor=ft.Colors.GREY_800,
                border_radius=10,
                padding=10
            ),
            self.crea_pulsante_indietro()
        ], scroll=ft.ScrollMode.AUTO, spacing=30, expand=True)
        
        return ft.View(
            "/inventario",
            controls=[
                ft.Container(
                    content=content,
                    bgcolor=ft.Colors.GREY_900,
                    padding=20,
                    expand=True
                )
            ],
            bgcolor=ft.Colors.GREY_900
        )
    
    def crea_vista_statistiche(self):
        """Crea la vista delle statistiche"""
        titolo = ft.Text(
            "Statistiche", 
            size=24, 
            weight=ft.FontWeight.BOLD, 
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.PURPLE_400
        )
        
        # Contenuto statistiche
        stats_text = self.ottieni_statistiche_dettagliate()
        contenuto_stats = ft.Text(
            stats_text,
            size=14,
            color=ft.Colors.WHITE,
            selectable=True
        )
        
        content = ft.Column([
            titolo,
            ft.Container(height=20),
            ft.Container(
                content=contenuto_stats,
                bgcolor=ft.Colors.GREY_800,
                border_radius=10,
                padding=20,
                expand=True
            ),
            ft.Container(height=20),
            self.crea_pulsante_indietro()
        ], scroll=ft.ScrollMode.AUTO, spacing=20, expand=True)
        
        return ft.View(
            "/statistiche",
            controls=[
                ft.Container(
                    content=content,
                    bgcolor=ft.Colors.GREY_900,
                    padding=20,
                    expand=True
                )
            ],
            bgcolor=ft.Colors.GREY_900
        )
    
    def crea_vista_rinomina_gatto(self):
        """Crea la vista per rinominare il gatto"""
        titolo = ft.Text(
            "Rinomina Gatto", 
            size=24, 
            weight=ft.FontWeight.BOLD, 
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.PURPLE_400
        )
        
        # Crea contenuto rinomina gatto direttamente qui (come fa inventario)
        if not self.gatto_attivo or not self.gatti[self.gatto_attivo].get("sbloccato", False):
            # Caso: nessun gatto disponibile
            rinomina_controls = [
                ft.Text("Nessun gatto attivo disponibile", size=16, text_align=ft.TextAlign.CENTER)
            ]
        else:
            gatto_info = self.gatti[self.gatto_attivo]
            
            # TextField locale per nuovo nome (invece di self.campo_nuovo_nome)
            campo_nuovo_nome_locale = ft.TextField(
                value=gatto_info["nome"],
                width=300,
                autofocus=True,
                on_blur=self.riavvia_musica_dopo_dettatura
            )
            
            def conferma_rinomina(e):
                nuovo_nome = campo_nuovo_nome_locale.value.strip()
                if nuovo_nome and nuovo_nome != gatto_info["nome"]:
                    self.gatti[self.gatto_attivo]["nome"] = nuovo_nome
                    self.gatti[self.gatto_attivo]["nome_personalizzato"] = True
                    self.aggiorna_storia(f"Il tuo gatto si chiama ora {nuovo_nome}! Sembra molto felice del nuovo nome!")
                    self.haptic_feedback("light")
                self.torna_indietro()
            
            rinomina_controls = [
                ft.Text(f"Rinomina: {gatto_info['emoji']} {gatto_info['nome']}", size=18, text_align=ft.TextAlign.CENTER),
                campo_nuovo_nome_locale,
                ft.Row([
                    ft.ElevatedButton(
                        text="Conferma Rinomina",
                        on_click=conferma_rinomina,
                        width=300,
                        height=60,
                        bgcolor=ft.Colors.GREEN_600,
                        color=ft.Colors.WHITE,
                        tooltip="Conferma il nuovo nome per il gatto"
                    )
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    ft.ElevatedButton(
                        text="Annulla",
                        on_click=lambda e: self.torna_indietro(),
                        width=200,
                        height=50,
                        bgcolor=ft.Colors.RED_600,
                        color=ft.Colors.WHITE,
                        tooltip="Annulla la rinomina"
                    )
                ], alignment=ft.MainAxisAlignment.CENTER)
            ]
        
        content = ft.Column([
            titolo,
            ft.Container(
                content=ft.Column(rinomina_controls, spacing=25, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                height=400,
                bgcolor=ft.Colors.GREY_800,
                border_radius=10,
                padding=10
            ),
            self.crea_pulsante_indietro()
        ], scroll=ft.ScrollMode.AUTO, spacing=30, expand=True)
        
        return ft.View(
            "/rinomina_gatto",
            controls=[
                ft.Container(
                    content=content,
                    bgcolor=ft.Colors.GREY_900,
                    padding=20,
                    expand=True
                )
            ],
            bgcolor=ft.Colors.GREY_900
        )
    
    def riavvia_musica_dopo_dettatura(self, e):
        """Riavvia la musica dopo che l'utente ha finito di usare la dettatura vocale"""
        print("🎵 DEBUG: Campo testo ha perso focus - riavvio musica se necessario")
        
        if not self.audio_abilitato:
            return
            
        try:
            # Riavvia sia musica che suoni ambientali
            print("🎵 DEBUG: Riavvio musica area dopo dettatura")
            self.cambia_musica_area(self.area_attuale)
            
            print("🌿 DEBUG: Riavvio suoni ambientali dopo dettatura") 
            self.cambia_suono_ambiente_area(self.area_attuale)
                
        except Exception as ex:
            print(f"🎵 WARNING: Errore riavvio audio dopo dettatura: {ex}")
    
    def crea_vista_gestione_reliquie(self):
        """Crea la vista per gestire le reliquie"""
        titolo = ft.Text(
            "🔮 Gestione Reliquie", 
            size=24, 
            weight=ft.FontWeight.BOLD, 
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.AMBER_400
        )
        
        # Equipaggiamento attuale
        equipaggiamento_controls = []
        
        for slot, oggetto in self.equipaggiamento.items():
            slot_nome = {
                "arma": "🗡️ Arma",
                "armatura": "🛡️ Armatura", 
                "accessorio": "💍 Accessorio"
            }.get(slot, slot)
            
            if oggetto:
                equipaggiamento_controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Text(f"{slot_nome}: {oggetto}", size=16, expand=True),
                            ft.ElevatedButton(
                                text="Rimuovi",
                                on_click=lambda e, s=slot: self.rimuovi_equipaggiamento(s),
                                width=100,
                                height=40,
                                bgcolor=ft.Colors.RED_600,
                                color=ft.Colors.WHITE,
                                tooltip=f"Rimuovi {oggetto}"
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        bgcolor=ft.Colors.GREY_800,
                        border_radius=10,
                        padding=15,
                        margin=5
                    )
                )
            else:
                equipaggiamento_controls.append(
                    ft.Container(
                        content=ft.Text(f"{slot_nome}: Vuoto", size=16, color=ft.Colors.GREY_400),
                        bgcolor=ft.Colors.GREY_800,
                        border_radius=10,
                        padding=15,
                        margin=5
                    )
                )
        
        content = ft.Column([
            titolo,
            ft.Container(height=20),
            ft.Text("Equipaggiamento Attuale", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Container(height=10),
            ft.Container(
                content=ft.Column(equipaggiamento_controls, spacing=10),
                bgcolor=ft.Colors.GREY_800,
                border_radius=10,
                padding=10
            ),
            ft.Container(height=20),
            self.crea_pulsante_indietro()
        ], scroll=ft.ScrollMode.AUTO, spacing=20, expand=True)
        
        return ft.View(
            "/gestione_reliquie",
            controls=[
                ft.Container(
                    content=content,
                    bgcolor=ft.Colors.GREY_900,
                    padding=20,
                    expand=True
                )
            ],
            bgcolor=ft.Colors.GREY_900
        )
    
    def seleziona_area_e_torna(self, e, area_scelta):
        """Seleziona area e torna alla schermata di gioco"""
        if area_scelta != self.area_attuale:
            self.cambia_area(area_scelta)
        self.torna_indietro()
    
    def inizia_combattimento(self, e):
        """Inizia un nuovo combattimento"""
        if self.risorse["energia"] < 20:
            self.haptic_feedback("warning")
            self.aggiorna_storia("❌ Non hai abbastanza energia per combattere! (servono 20)")
            return
            
        if self.vita <= 10:
            self.haptic_feedback("warning")
            self.aggiorna_storia("❌ La tua vita è troppo bassa per combattere! Riposa o usa pozioni.")
            return
        
        # Dati mostri per area
        mostri_area = {
            "Villaggio": {"nome": "Topo Gigante", "hp": 80, "attacco": 10, "verso": "Squeak!"},
            "🏠 Cantina": {"nome": "Ragno Peloso", "hp": 100, "attacco": 14, "verso": "Hiss!"},
            "🚰 Fogne": {"nome": "Ratto delle Fogne", "hp": 120, "attacco": 18, "verso": "Screech!"},
            "🌀 Labirinto Antico": {"nome": "Guardiano di Pietra", "hp": 140, "attacco": 22, "verso": "Rumble!"},
            "❄️ Area Innevata": {"nome": "Lupo Gelido", "hp": 160, "attacco": 26, "verso": "Howl!"},
            "🌿 Giungla Selvaggia": {"nome": "Serpente Velenoso", "hp": 180, "attacco": 30, "verso": "Ssss!"},
            "🌲 Bosco Profondo": {"nome": "Orso Bruno", "hp": 200, "attacco": 34, "verso": "Roar!"},
            "⚰️ Cimitero": {"nome": "Scheletro Errante", "hp": 220, "attacco": 38, "verso": "Clatter!"},
            "🏚️ Casa degli Orrori": {"nome": "Fantasma Tormentato", "hp": 240, "attacco": 42, "verso": "Woooo!"},
            "🏭 Fabbrica Abbandonata": {"nome": "Robot Malfunzionante", "hp": 260, "attacco": 46, "verso": "Beep-Error!"},
            "⛏️ Miniera Profonda": {"nome": "Golem di Ferro", "hp": 280, "attacco": 50, "verso": "Clang!"},
            "🌙 Cripta Maledetta": {"nome": "Lich Minore", "hp": 300, "attacco": 54, "verso": "Necro!"},
            "🌊 Mare": {"nome": "Kraken Giovane", "hp": 320, "attacco": 58, "verso": "Splash!"},
            "🏔️ Montagna Sacra": {"nome": "Drago di Montagna", "hp": 340, "attacco": 62, "verso": "Roooar!"},
            "🌋 Vulcano Attivo": {"nome": "Elementale del Fuoco", "hp": 360, "attacco": 66, "verso": "Flame!"},
            "👑 Palazzo Finale": {"nome": "Guardia Reale", "hp": 380, "attacco": 70, "verso": "En garde!"}
        }
        
        self.mostro_attuale = mostri_area.get(self.area_attuale, {"nome": "Mostro Sconosciuto", "hp": 20, "attacco": 5, "verso": "Grrr!"})
        self.hp_mostro_attuale = self.mostro_attuale["hp"]
        self.in_combattimento = True
        self.round_combattimento = 1
        self.risorse["energia"] -= 20
        
        # Avvia musica battaglia
        if self.audio_abilitato:
            self.avvia_musica_battaglia("normale")
        
        messaggio_log = f"Incontri un {self.mostro_attuale['nome']}!\n{self.mostro_attuale['verso']}\n\nIl combattimento inizia!"
        self.haptic_feedback("medium")
        
        # Controlla se la vita è già bassa all'inizio del combattimento
        self.controlla_vita_bassa()
        
        # Aggiorna il log di combattimento e poi ricrea la vista
        self.aggiorna_storia(messaggio_log)
        self.aggiorna_info_combattimento()
    
    
    def attacca_mostro_wrapper(self, e):
        """Wrapper per debug del pulsante attacca"""
        try:
            self.attacca_mostro(e)
        except Exception as ex:
            print(f"❌ ERRORE in attacca_mostro: {ex}")
            import traceback
            traceback.print_exc()
    
    def attacca_mostro(self, e):
        """Attacca il mostro"""
        if not self.in_combattimento:
            return
        
        # Calcola danno del giocatore
        try:
            danno_giocatore = self.calcola_attacco_totale()
        except:
            danno_giocatore = 15  # Fallback
        
        self.hp_mostro_attuale -= danno_giocatore
        
        # Effetti sonori e aptico
        self.haptic_feedback("medium")
        if self.audio_abilitato:
            self.riproduci_effetto("gatto_attacco")
        
        messaggio = f"Round {self.round_combattimento}:\n Attacchi il {self.mostro_attuale['nome']} per {danno_giocatore} danni!\n"
        
        # Controlla se il mostro è morto
        if self.hp_mostro_attuale <= 0:
            # Mostro sconfitto
            self.in_combattimento = False
            self.ferma_heartbeat()  # Ferma heartbeat quando vinci
            messaggio += f"🎉 Hai sconfitto il {self.mostro_attuale['nome']}!\n"
            
            # Ricompense
            oro_guadagnato = self.mostro_attuale["attacco"] * 5
            exp_guadagnata = self.mostro_attuale["hp"] // 5
            self.oro += oro_guadagnato
            self.monete = self.oro
            self.esperienza += exp_guadagnata
            
            # Controlla livello dopo esperienza guadagnata
            testo_livello = self.gestisci_livello()
            if testo_livello:
                messaggio += f"\n{testo_livello}"
            
            # Controlla sblocco gatti
            self.controlla_sblocco_gatti()
            
            # Progressione area per combattimento vinto
            if self.area_attuale in self.progressione_area:
                self.progressione_area[self.area_attuale] += 1
                print(f" Progressione {self.area_attuale}: {self.progressione_area[self.area_attuale]}")
                
                # Controlla se il boss dell'area è stato sbloccato per la prima volta
                if (self.progressione_area[self.area_attuale] >= 100 and 
                    self.area_attuale not in self.boss_notifications_mostrate):
                    boss_sconfitto = self.controlla_boss_sconfitto(self.area_attuale)
                    if not boss_sconfitto:
                        # Mostra notifica sblocco boss solo una volta
                        self.boss_notifications_mostrate.add(self.area_attuale)
                        self.mostra_notifica_boss_sbloccato(self.area_attuale)
                        messaggio += f"\n Devi prima sconfiggere il boss di quest'area per procedere!"
            
            messaggio += f" +{oro_guadagnato} oro\n +{exp_guadagnata} esperienza"
            
            if self.audio_abilitato:
                self.riproduci_effetto("vittoria")
                self.termina_musica_battaglia()
            
            self.haptic_feedback("success")
            
            # Reset mostro dopo vittoria
            self.mostro_attuale = None
            
            # Sincronizza HP dopo vittoria
            self.hp_giocatore = self.vita
            
            # Aggiorna le statistiche per mostrare la nuova progressione
            self.aggiorna_stats_incrementali()
        else:
            # Mostro contrattacca
            try:
                danno_mostro = max(1, self.mostro_attuale["attacco"] - self.calcola_difesa_totale())
            except:
                danno_mostro = 2  # Fallback
            
            self.vita -= danno_mostro
            self.hp_giocatore = self.vita
            
            messaggio += f"💥 Il {self.mostro_attuale['nome']} ti attacca per {danno_mostro} danni!\n"
            messaggio += f" La tua vita: {self.vita}/{self.vita_massima}"
            
            if self.vita <= 0:
                # Player defeated - end combat immediately
                self.in_combattimento = False
                self.ferma_heartbeat()  # Ferma heartbeat quando perdi
                messaggio += "\n💀 Sei stato sconfitto! Torni in città."
                
                if self.audio_abilitato:
                    self.riproduci_effetto("sconfitta")
                    self.termina_musica_battaglia()
                
                # Reset mostro dopo sconfitta
                self.mostro_attuale = None
                self.vita = 1  # Ripristina vita a 1 per continuare il gioco
                self.hp_giocatore = 1
                
                self.haptic_feedback("heavy")
                
                # Exit combat and return to main game
                self.aggiorna_storia(messaggio)
                self.aggiorna_stats_incrementali()
                self.page.go("/gioco")
                return
            else:
                self.controlla_vita_bassa()
                self.aggiorna_stats_incrementali()  # Aggiorna statistiche dopo danno
                self.haptic_feedback("light")
        
        self.round_combattimento += 1
        self.aggiorna_info_combattimento()
    
    def difendi_combattimento(self, e):
        """Difendi per ridurre i danni"""
        if not self.in_combattimento:
            return
        
        # Mostro attacca con danni ridotti
        danno_mostro = max(1, (self.mostro_attuale["attacco"] - self.calcola_difesa_totale()) // 2)
        self.vita -= danno_mostro
        self.hp_giocatore = self.vita
        
        messaggio = f"Round {self.round_combattimento}:\n Ti difendi!\n💥 Il {self.mostro_attuale['nome']} ti attacca per {danno_mostro} danni ridotti!\n"
        
        if self.vita <= 0:
            # Player defeated - end combat immediately
            self.in_combattimento = False
            self.ferma_heartbeat()  # Ferma heartbeat quando perdi
            messaggio += "💀 Sei stato sconfitto! Torni in città."
            
            if self.audio_abilitato:
                self.riproduci_effetto("sconfitta")
                self.termina_musica_battaglia()
            
            # Reset mostro dopo sconfitta
            self.mostro_attuale = None
            self.vita = 1  # Ripristina vita a 1 per continuare il gioco
            self.hp_giocatore = 1
            
            self.haptic_feedback("heavy")
            
            # Exit combat and return to main game
            self.aggiorna_storia(messaggio)
            self.aggiorna_stats_incrementali()
            self.page.go("/gioco")
            return
        else:
            self.controlla_vita_bassa()
            self.aggiorna_stats_incrementali()  # Aggiorna statistiche dopo difesa
            self.haptic_feedback("light")
        
        self.round_combattimento += 1
        # Non ricreare l'intera schermata, solo aggiornare le info
        self.aggiorna_info_combattimento()
    
    def usa_pozione_combattimento(self, e):
        """Usa un oggetto curativo durante il combattimento"""
        if not self.in_combattimento:
            return
            
        # Trova il primo oggetto curativo disponibile
        oggetto_da_usare = None
        cura = 0
        
        # Priorità: Pozione Vita > Pane > Mela
        if "Pozione Vita" in self.inventario and self.inventario["Pozione Vita"] > 0:
            oggetto_da_usare = "Pozione Vita"
            cura = 50
        elif "Pane" in self.inventario and self.inventario["Pane"] > 0:
            oggetto_da_usare = "Pane"
            cura = 15
        elif "Mela" in self.inventario and self.inventario["Mela"] > 0:
            oggetto_da_usare = "Mela"
            cura = 10
            
        if not oggetto_da_usare:
            return
            
        # Usa l'oggetto
        self.inventario[oggetto_da_usare] -= 1
        if self.inventario[oggetto_da_usare] <= 0:
            del self.inventario[oggetto_da_usare]
            
        self.vita = min(self.vita_massima, self.vita + cura)
        self.hp_giocatore = self.vita
        self.controlla_vita_bassa()  # Controlla se fermare heartbeat dopo guarigione
        self.aggiorna_stats_incrementali()  # Aggiorna statistiche dopo guarigione
        
        # Riproduci effetto sonoro
        if self.audio_abilitato:
            self.riproduci_effetto("bere_pozione")
        
        # Mostro attacca comunque
        danno_mostro = max(1, self.mostro_attuale["attacco"] - self.calcola_difesa_totale())
        self.vita -= danno_mostro
        self.hp_giocatore = self.vita
        
        messaggio = f"Round {self.round_combattimento}:\nUsi {oggetto_da_usare} e recuperi {cura} vita!\n💥 Il {self.mostro_attuale['nome']} ti attacca per {danno_mostro} danni!\n"
        
        if self.vita <= 0:
            # Player defeated - end combat immediately
            self.in_combattimento = False
            self.ferma_heartbeat()  # Ferma heartbeat quando perdi
            messaggio += "💀 Sei stato sconfitto! Torni in città."
            
            if self.audio_abilitato:
                self.riproduci_effetto("sconfitta")
                self.termina_musica_battaglia()
            
            # Reset mostro dopo sconfitta
            self.mostro_attuale = None
            self.vita = 1  # Ripristina vita a 1 per continuare il gioco
            self.hp_giocatore = 1
            
            self.haptic_feedback("heavy")
            
            # Exit combat and return to main game
            self.aggiorna_storia(messaggio)
            self.aggiorna_stats_incrementali()
            self.page.go("/gioco")
            return
        else:
            self.controlla_vita_bassa()
            self.aggiorna_stats_incrementali()  # Aggiorna statistiche dopo attacco post-pozione
            self.haptic_feedback("light")
        
        self.round_combattimento += 1
        # Non ricreare l'intera schermata, solo aggiornare le info
        self.aggiorna_info_combattimento()
    
    def fuggi_combattimento(self, e):
        """Tenta di fuggire dal combattimento"""
        if not self.in_combattimento:
            return
        
        import random
        if random.randint(1, 10) <= 7:  # 70% di successo
            self.in_combattimento = False
            self.ferma_heartbeat()  # Ferma heartbeat quando fuggi
            messaggio = f"🏃 Sei riuscito a fuggire dal {self.mostro_attuale['nome']}!"
            
            if self.audio_abilitato:
                self.termina_musica_battaglia()
            
            # Reset mostro dopo fuga
            self.mostro_attuale = None
            
            self.haptic_feedback("light")
        else:
            # Fuga fallita, mostro attacca
            danno_mostro = self.mostro_attuale["attacco"]
            self.vita -= danno_mostro
            self.hp_giocatore = self.vita
            messaggio = f"❌ Non riesci a fuggire!\n💥 Il {self.mostro_attuale['nome']} ti attacca per {danno_mostro} danni!\n"
            
            if self.vita <= 0:
                # Player defeated - end combat immediately
                self.in_combattimento = False
                self.ferma_heartbeat()  # Ferma heartbeat quando perdi
                messaggio += "💀 Sei stato sconfitto! Torni in città."
                
                if self.audio_abilitato:
                    self.riproduci_effetto("sconfitta")
                    self.termina_musica_battaglia()
                
                # Reset mostro dopo sconfitta
                self.mostro_attuale = None
                self.vita = 1  # Ripristina vita a 1 per continuare il gioco
                self.hp_giocatore = 1
                
                self.haptic_feedback("heavy")
                
                # Exit combat and return to main game
                self.aggiorna_storia(messaggio)
                self.aggiorna_stats_incrementali()
                self.page.go("/gioco")
                return
            else:
                self.controlla_vita_bassa()
                self.aggiorna_stats_incrementali()  # Aggiorna statistiche dopo fuga fallita
                self.haptic_feedback("medium")
        
        self.round_combattimento += 1
        # Non ricreare l'intera schermata, solo aggiornare le info
        self.aggiorna_info_combattimento()
    
    def aggiorna_info_combattimento(self):
        """Aggiorna le informazioni di combattimento ricreando la vista"""
        # SOLO se siamo nella vista combattimento, aggiornala
        if len(self.page.views) > 0 and self.page.views[-1].route == "/combattimento":
            print(f"🎮 DEBUG: Ricreando vista combattimento - in_combattimento = {self.in_combattimento}")
            # Ricrea la vista combattimento
            self.page.views.pop()  # Rimuovi vista corrente
            vista = self.crea_vista_combattimento()
            self.page.views.append(vista)
            self.analizza_accessibilita(vista)
            self.page.update()
            print("🎮 INFO: Vista combattimento ricreata")
        else:
            print("🎮 DEBUG: Non nella vista combattimento, IGNORO aggiornamento")

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
            self.volume_musica_label_tab.value = f"Volume Musica: {int(self.volume_musica * 100)}%"
        if hasattr(self, 'volume_effetti_label_tab'):
            self.volume_effetti_label_tab.value = f"Volume Effetti: {int(self.volume_effetti * 100)}%"
        self.page.update()
    
# Funzioni crea_contenuto_* rimosse - contenuto ora creato localmente nelle viste

    def crea_menu_principale_per_tab(self):
        """Crea il menu principale per la tab Home con colori"""
        self.container_pulsanti.controls.clear()
        
        # Titoli con colori
        titolo_principale = ft.Text(
            "🏰 AVVENTURA EPICA 🏰", 
            size=28, 
            weight=ft.FontWeight.BOLD, 
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.AMBER_400
        )
        sottotitolo = ft.Text(
            "🎵 Audio Immersivo • 📳 Feedback Aptico • 🗺️ 16 Aree • 🛍️ Negozi •  RPG", 
            size=14, 
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.CYAN_200
        )
        
        pulsanti = ft.Column([
            ft.ElevatedButton(
                text="Inizia Nuova Avventura",
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
                text="Carica Gioco Salvato",
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
        """Crea il menu di gioco incrementale con controlli locali accessibili"""

        self.container_pulsanti.controls.clear()

        # Titolo senza semantics_label
        titolo_gioco = ft.Text(
            "Avventura in corso",
            size=24,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.RED_400
        )

        # Controlli locali: area storia e stats
        area_storia_locale = ft.TextField(
            value=self.area_storia.value if hasattr(self, 'area_storia') else "",
            multiline=True,
            read_only=True,
            expand=True,
            min_lines=10,
            max_lines=15,
            text_size=14,
            bgcolor=ft.Colors.DEEP_PURPLE_900,
            color=ft.Colors.AMBER_100,
            border_color=ft.Colors.AMBER_400,
            focused_border_color=ft.Colors.AMBER_300,
            label="Storia dell'avventura"
        )

        area_stats_locale = ft.TextField(
            value=self.area_stats.value if hasattr(self, 'area_stats') else "",
            multiline=True,
            read_only=True,
            min_lines=4,
            max_lines=6,
            text_size=14,
            bgcolor=ft.Colors.BLUE_GREY_900,
            color=ft.Colors.CYAN_100,
            border_color=ft.Colors.CYAN_400,
            focused_border_color=ft.Colors.CYAN_300,
            label="Statistiche giocatore"
        )

        # Salva riferimenti se servono altrove
        self.area_storia = area_storia_locale
        self.area_stats = area_stats_locale

        # Azioni incrementali
        azioni_incrementali = self.azioni_incrementali_possibili()
        if azioni_incrementali:
            righe = [azioni_incrementali[i:i+3] for i in range(0, len(azioni_incrementali), 3)]
            for riga in righe:
                pulsanti = []
                for testo, funzione, tooltip in riga:
                    colore, overlay = self.get_colori_azione(testo)
                    pulsanti.append(
                        ft.ElevatedButton(
                            text=testo,
                            on_click=funzione,
                            width=120,
                            height=50,
                            tooltip=tooltip,
                            bgcolor=colore,
                            color=ft.Colors.WHITE,
                            style=ft.ButtonStyle(
                                overlay_color=overlay,
                                elevation=6
                            )
                        )
                    )
                self.container_pulsanti.controls.append(
                    ft.Row(pulsanti, alignment=ft.MainAxisAlignment.CENTER, spacing=10)
                )

        # Azioni speciali
        azioni_speciali = self.azioni_speciali_possibili()
        if azioni_speciali:
            pulsanti_speciali = []
            for testo, funzione, tooltip in azioni_speciali:
                colore, overlay = self.get_colori_azione_speciale(testo)
                pulsanti_speciali.append(
                    ft.ElevatedButton(
                        text=testo,
                        on_click=funzione,
                        width=120,
                        height=50,
                        tooltip=tooltip,
                        bgcolor=colore,
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            overlay_color=overlay,
                            elevation=6
                        )
                    )
                )
            self.container_pulsanti.controls.append(
                ft.Row(pulsanti_speciali, alignment=ft.MainAxisAlignment.CENTER, spacing=10)
            )

        # Menu gatti e utility
        menu_gatti = []

        menu_gatti.append(
            ft.ElevatedButton(
                "Gestione Gatti",
                on_click=lambda e: self.page.go("/gatti"),
                width=140,
                height=50,
                tooltip="Gestisci i tuoi gatti compagni",
                bgcolor=ft.Colors.PINK_600,
                color=ft.Colors.WHITE,
                style=ft.ButtonStyle(
                    overlay_color=ft.Colors.PINK_500,
                    elevation=4
                )
            )
        )

        if self.gatto_attivo and self.gatto_attivo in self.gatti:
            menu_gatti.append(
                ft.ElevatedButton(
                    "Rinomina Gatto",
                    on_click=self.rinomina_gatto,
                    width=140,
                    height=50,
                    tooltip="Dai un nuovo nome al tuo gatto",
                    bgcolor=ft.Colors.PURPLE_600,
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(
                        overlay_color=ft.Colors.PURPLE_500,
                        elevation=4
                    )
                )
            )

        menu_gatti.append(
            ft.ElevatedButton(
                "Statistiche",
                on_click=lambda e: self.page.go("/statistiche"),
                width=140,
                height=50,
                tooltip="Visualizza statistiche dettagliate",
                bgcolor=ft.Colors.CYAN_600,
                color=ft.Colors.WHITE,
                style=ft.ButtonStyle(
                    overlay_color=ft.Colors.CYAN_500,
                    elevation=4
                )
            )
        )

        self.container_pulsanti.controls.append(
            ft.Row(menu_gatti, alignment=ft.MainAxisAlignment.CENTER, spacing=10)
        )

        # Menu finale
        self.container_pulsanti.controls.append(
            ft.Row([
                ft.ElevatedButton(
                    "Salva Avventura",
                    on_click=self.salva_gioco,
                    width=150,
                    height=50,
                    tooltip="Salva la tua avventura",
                    bgcolor=ft.Colors.GREEN_600,
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(
                        overlay_color=ft.Colors.GREEN_500,
                        elevation=4
                    )
                )
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

        self.container_pulsanti.controls.append(
            ft.Row([
                ft.ElevatedButton(
                    "Torna al Menu",
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
        )

        # Layout finale
        self.container_principale.controls.clear()
        self.container_principale.controls.extend([
            titolo_gioco,
            area_storia_locale,
            area_stats_locale,
            self.container_pulsanti
        ])

        self.modalita_menu = "gioco"
        self.page.update()

    def crea_menu_inventario(self):
        """Menu inventario con pulsanti dinamici"""
        self.container_pulsanti.controls.clear()
        
        # Titolo inventario
        titolo_inventario = ft.Text(
            "INVENTARIO", 
            size=24, 
            weight=ft.FontWeight.BOLD, 
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.CYAN_400
        )
        
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
                    "Equipaggia", 
                    on_click=self.equipaggia_oggetto, 
                    width=200, 
                    height=50, 
                    tooltip="Equipaggia armi, armature o accessori",
                    data="btn_equipaggia"
                )
            )
        
        # Gestione reliquie sempre disponibile
        pulsanti_inventario.append(
            ft.ElevatedButton(
                "Reliquie", 
                on_click=self.gestisci_reliquie, 
                width=200, 
                height=50, 
                tooltip="Gestisci le tue reliquie antiche",
                data="btn_reliquie"
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
            titolo_inventario,
            self.area_storia,
            self.area_stats,
            self.container_pulsanti
        ])
        
        self.modalita_menu = "inventario"
        self.page.update()
        
    def crea_menu_negozio(self):
        """Menu negozio con pulsanti individuali per ogni oggetto"""
        self.container_pulsanti.controls.clear()
        
        # Titolo negozio
        titolo_negozio = ft.Text(
            "NEGOZIO", 
            size=24, 
            weight=ft.FontWeight.BOLD, 
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.AMBER_400
        )
        
        pulsanti_negozio = []
        
        # Ottieni negozio dell'area corrente
        negozio = self.negozi.get(self.area_attuale, {})
        
        # Crea un pulsante per ogni oggetto nel negozio
        for nome_oggetto, info in negozio.items():
            disponibile = self.monete >= info["prezzo"]
            colore = ft.Colors.GREEN_600 if disponibile else ft.Colors.RED_600
            testo_prezzo = f"💰 {info['prezzo']}"
            tooltip_text = f"{info['descrizione']} - Costo: {info['prezzo']} monete"
            
            if not disponibile:
                tooltip_text += " (Non hai abbastanza monete)"
            
            print(f"🛒 DEBUG: Creando pulsante per {nome_oggetto}, prezzo={info['prezzo']}, disponibile={disponibile}, monete={self.monete}")
            
            pulsanti_negozio.append(
                ft.ElevatedButton(
                    f"Compra {nome_oggetto}",
                    on_click=lambda e, oggetto=nome_oggetto, prezzo=info["prezzo"]: self.compra_oggetto_specifico(e, oggetto, prezzo),
                    width=350,
                    height=60,
                    bgcolor=colore,
                    color=ft.Colors.WHITE,
                    tooltip=tooltip_text,
                    disabled=not disponibile,
                    data=f"compra_{nome_oggetto}"
                )
            )
        
        # Torna sempre disponibile
        pulsanti_negozio.append(
            ft.ElevatedButton(
                "🔙 Torna al Gioco", 
                on_click=self.vai_direttamente_al_gioco, 
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
            titolo_negozio,
            self.area_storia,
            self.area_stats,
            self.container_pulsanti
        ])
        
        self.modalita_menu = "negozio"
        self.page.update()
        
    def crea_menu_statistiche(self):
        """Menu statistiche semplificato"""
        self.container_pulsanti.controls.clear()
        
        # Titolo statistiche
        titolo_statistiche = ft.Text(
            "STATISTICHE", 
            size=24, 
            weight=ft.FontWeight.BOLD, 
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.PURPLE_400
        )
        
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
            titolo_statistiche,
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
            label="Audio Attivato",
            value=self.audio_abilitato,
            on_change=self.toggle_audio_callback,
            tooltip="Attiva o disattiva tutti gli effetti audio"
        )
        
        toggle_haptic = ft.Switch(
            label="Vibrazione Attivata",
            value=self.haptic_abilitato,
            on_change=self.toggle_haptic_callback,
            tooltip="Attiva o disattiva il feedback aptico"
        )
        
        # Slider volume musica
        self.volume_musica_label = ft.Text(f"Volume Musica: {int(self.volume_musica * 100)}%")
        slider_volume_musica = ft.Slider(
            min=0,
            max=1,
            value=self.volume_musica,
            divisions=10,
            on_change=self.cambia_volume_musica,
            tooltip="Regola il volume della musica di sottofondo"
        )
        
        # Slider volume effetti
        self.volume_effetti_label = ft.Text(f"Volume Effetti: {int(self.volume_effetti * 100)}%")
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
            "Testa Audio",
            on_click=self.testa_audio,
            width=200,
            tooltip="Riproduci un suono di test",
            data="btn_test_audio"
        )
        
        # Pulsante debug audio
        debug_audio_btn = ft.ElevatedButton(
            "Debug Audio",
            on_click=self.test_audio_debug,
            width=200,
            tooltip="Diagnosi completa sistema audio",
            data="btn_debug_audio"
        )
        
        # Layout impostazioni
        impostazioni_content = ft.Column([
            ft.Text("=== IMPOSTAZIONI ===", size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
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
            debug_audio_btn,
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
        
    def vai_a_impostazioni(self, e):
        """Vai al menu impostazioni"""
        self.page.go("/impostazioni")
        
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
            self.volume_musica_label.value = f"Volume Musica: {int(self.volume_musica * 100)}%"
        
        # Aggiorna label nella tab se esiste
        if hasattr(self, 'volume_musica_label_tab'):
            self.volume_musica_label_tab.value = f"Volume Musica: {int(self.volume_musica * 100)}%"
        
        self.page.update()
            
    def cambia_volume_effetti(self, e):
        """Cambia volume effetti"""
        self.volume_effetti = e.control.value
        # Aggiorna volume di tutti i canali effetti
        if hasattr(self, 'effetto_gatto'):
            self.effetto_gatto.volume = self.volume_effetti
            self.effetto_vittoria.volume = self.volume_effetti
            self.effetto_sconfitta.volume = self.volume_effetti
            self.effetto_livello.volume = self.volume_effetti
            self.effetto_raccolta.volume = self.volume_effetti
            self.effetto_gatto_raccolta.volume = self.volume_effetti
            self.effetto_monete.volume = self.volume_effetti
        
        # Aggiorna label se esiste (per compatibilità con vecchi menu)
        if hasattr(self, 'volume_effetti_label'):
            self.volume_effetti_label.value = f"Volume Effetti: {int(self.volume_effetti * 100)}%"
        
        # Aggiorna label nella tab se esiste  
        if hasattr(self, 'volume_effetti_label_tab'):
            self.volume_effetti_label_tab.value = f"Volume Effetti: {int(self.volume_effetti * 100)}%"
        
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
        self.stack_schermate.clear()  # Pulisce lo stack di navigazione
        self.schermata_corrente = "menu_principale"
        # Non mettere in pausa la musica qui - lasciala continuare
        # if self.audio_abilitato:
        #     self.musica_sottofondo.pause()
        self.crea_menu_principale_per_tab()
        
    def torna_al_gioco(self, e):
        """Torna al gioco dalla modalità menu"""
        if not self.gioco_iniziato:
            self.torna_menu_principale(e)
            return
            
        # Naviga correttamente alla schermata di gioco
        self.page.go("/gioco")
        self.descrivi_situazione_attuale()
        
        # 🎵 Ripristina musica area se non in battaglia
        if self.audio_abilitato and not self.in_battaglia:
            print(f"🎵 Ripristino musica area: {self.area_attuale}")
            self.cambia_musica_area(self.area_attuale)
            self.cambia_suono_ambiente_area(self.area_attuale)
        
    def vai_a_inventario(self, e):
        """Naviga alla schermata inventario con vista pulita"""
        print(f"🎮 DEBUG: Navigando a inventario - views attuali: {[v.route for v in self.page.views]}")
        
        # Assicurati che le views siano pulite prima della navigazione
        if len(self.page.views) > 1:
            # Mantieni solo la vista base
            self.page.views = [self.page.views[0]]
        
        self.page.go("/inventario")
        print(f"🎮 DEBUG: Navigazione inventario completata")
        
    def vai_a_negozio(self, e):
        """Vai al menu negozio"""
        area_attuale = self.area_attuale
        
        if area_attuale not in self.negozi:
            self.aggiorna_storia("❌ Nessun negozio qui!")
            self.haptic_feedback("error")
            return
            
        self.page.go("/negozio")
        
    def vai_a_statistiche(self, e):
        """Vai al menu statistiche"""
        self.page.go("/statistiche")
        
    def riavvia_musica_corrente(self):
        """Riavvia musica area corrente"""
        self.cambia_musica_area(self.area_attuale)
        
    def aggiorna_storia(self, testo):
        """Aggiorna testo storia - usa log combattimento se in battaglia"""
        if (hasattr(self, 'log_combattimento_campo') and self.log_combattimento_campo and 
            len(self.page.views) > 0 and self.page.views[-1].route == "/combattimento"):
            # Se siamo in combattimento, aggiorna il log di combattimento
            self.log_combattimento_campo.value = testo
            self.log_combattimento_campo.update()
        elif hasattr(self, 'area_storia') and self.area_storia:
            # Altrimenti aggiorna l'area storia normale
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
        
        if self.audio_abilitato:
            self.cambia_musica_area("Villaggio")
            self.cambia_suono_ambiente_area("Villaggio")
            
        self.haptic_feedback("success")
        self.descrivi_situazione_attuale()
        
        # Naviga al gioco mantenendo la possibilità di tornare al menu
        self.page.go("/gioco")
        
    def descrivi_situazione_attuale(self):
        """Descrizione incrementale dell'area attuale"""
        area = self.area_attuale
        
        # Aggiorna statistiche incrementali
        self.aggiorna_stats_incrementali()
        
        # Descrizione dell'area
        testo = f" {area}\n\n"
        testo += f"{self.descrizioni[area]}\n\n"
        
        # Progressione area
        progressione = self.progressione_area[area]
        testo += f" Progressione area: {progressione}/20\n"
        
        if progressione < 10:
            testo += f"Continua ad esplorare per sbloccare nuove aree!\n"
        elif progressione < 20:
            testo += f"🎆 Stai per sbloccare qualcosa di speciale!\n"
        else:
            testo += f"✨ Area completamente esplorata!\n"
        
        # Info gatto attivo
        if self.gatto_attivo:
            gatto = self.gatti[self.gatto_attivo]
            testo += f"\n Compagno: {self.gatto_attivo}\n"
            testo += f"• Abilità: {gatto['abilita']} (Lv.{gatto['livello']})\n"
            
            if gatto['fame'] < 30:
                testo += f"• 🍽️ Il tuo gatto ha fame!\n"
            elif gatto['felicita'] > 80:
                testo += f"• 😊 Il tuo gatto è molto felice!\n"
                
        # Stato energia
        if self.risorse["energia"] < 30:
            testo += f"\n Energia bassa! Mangia per recuperare.\n"
            
        # Negozio disponibile
        if area in [
            "Villaggio", "🏪 Mercato", "🛤️ Strada"
        ]:
            testo += f"\n🏪 Negozio disponibile in quest'area!\n"
            
        # Condizione vittoria incrementale
        tesori_importanti = [item for item in self.inventario if any(parola in item for parola in ["corona", "tesoro", "reliquia"])]
        if len(tesori_importanti) >= 3 and self.livello >= 10:
            testo += "\n🎉 HAI RACCOLTO ABBASTANZA TESORI! SEI UN VERO AVVENTURIERO! 🎉"
            if self.audio_abilitato:
                self.riproduci_effetto("vittoria")
            self.haptic_feedback("success")
            
        self.aggiorna_storia(testo)
        
    def esplora_area(self, e):
        """Esplora l'area per trovare tesori e risorse"""
        if not self.gioco_iniziato:
            return
            
        if self.risorse["energia"] < 15:
            self.aggiorna_storia(" Non hai abbastanza energia per esplorare!")
            self.haptic_feedback("warning")
            return
            
        self.risorse["energia"] -= 15
        area = self.area_attuale
        
        # Possibilità di trovare tesori e reliquie
        possibilita = random.randint(1, 100)
        
        # Controlla eventi speciali di reliquie
        if self.genera_mini_dungeon(area):
            testo = f"Esplorando {area} scopri un MINI DUNGEON SEGRETO!\n"
            testo += f"🏛️ Antiche rovine nascoste ti aspettano..."
        elif self.incontra_npc_raro(area):
            testo = f"Esplorando {area}...\n"
        elif possibilita <= 25:  # 25% tesoro normale
            tesori = [" monete d'oro", "💎 gemma preziosa", "🗝️ antica reliquia", "🏺 vaso antico"]
            tesoro = random.choice(tesori)
            self.inventario.append(tesoro)
            monete_bonus = random.randint(15, 40)
            self.monete += monete_bonus
            
            testo = f"Esplorando {area} trovi:\n"
            testo += f"✨ {tesoro}!\n"
            testo += f" +{monete_bonus} monete"
            
            self.haptic_feedback("success")
            # Effetto diverso se ha gatto da raccolta attivo
            if self.gatto_attivo and self.gatti[self.gatto_attivo]["abilita"] in ["raccolta", "raccolta_suprema"]:
                self.riproduci_effetto("gatto_raccolta")
            else:
                self.riproduci_effetto("raccogli")
            # Effetto monete per tesori
            self.riproduci_effetto("monete")
            
        elif possibilita <= 60:  # 30% risorse extra
            if area == "🌲 Bosco":
                legno_extra = random.randint(15, 25)
                self.risorse["legno"] += legno_extra
                testo = f"Esplorando trovi un deposito di legno:\n+{legno_extra} legno"
            elif area == "🏔️ Montagna":
                pietra_extra = random.randint(10, 20)
                ferro_extra = random.randint(2, 5)
                self.risorse["pietra"] += pietra_extra
                self.risorse["ferro"] += ferro_extra
                testo = f"Esplorando trovi una vena mineraria:\n+{pietra_extra} pietra, +{ferro_extra} ferro"
            else:
                cibo_extra = random.randint(10, 20)
                acqua_extra = random.randint(5, 15)
                self.risorse["cibo"] += cibo_extra
                self.risorse["acqua"] += acqua_extra
                testo = f"Esplorando trovi provviste:\n+{cibo_extra} cibo, +{acqua_extra} acqua"
                
            self.haptic_feedback("success")
            
        else:  # 40% solo esperienza
            exp_guadagnata = random.randint(8, 15)
            self.esperienza += exp_guadagnata
            testo = f"Esplori {area} accuratamente\n"
            testo += f" +{exp_guadagnata} EXP per l'esplorazione"
            
        # Progressione area (solo se area valida)
        if area in self.progressione_area:
            self.progressione_area[area] += 1
        else:
            print(f"⚠️ Area non trovata in progressione_area: {area}")
        
        # Controlla livello
        testo_livello = self.gestisci_livello()
        if testo_livello:
            testo += "\n" + testo_livello
        
        # Controlla sblocco gatti
        self.controlla_sblocco_gatti()
            
        if self.progressione_area[area] >= 100:
            # Controlla se il boss dell'area è stato sconfitto
            boss_sconfitto = self.controlla_boss_sconfitto(area)
            if boss_sconfitto and self.sblocca_prossima_area():
                testo += f"\n🎆 Hai sbloccato una nuova area!"
            elif not boss_sconfitto:
                testo += f"\n Devi prima sconfiggere il boss di quest'area per procedere!"
            
        self.aggiorna_storia(testo)
        self.aggiorna_stats_incrementali()
        
    def controlla_boss_sconfitto(self, area):
        """Controlla se il boss dell'area attuale è stato sconfitto"""
        # Mappa aree ai boss (basata sui boss_aree esistenti)
        boss_aree_mappa = {
            "Villaggio": "🐕 Cane Randagio",
            "🏠 Cantina": "🕷️ Ragno Gigante", 
            "🚰 Fogne": "🐀 Re dei Ratti",
            "🌀 Labirinto Antico": "🏺 Guardiano Antico",
            "❄️ Area Innevata": "🐺 Lupo Gelido",
            "🌿 Giungla Selvaggia": "🐍 Serpente Gigante",
            "🌲 Bosco Profondo": "🐻 Orso Gigante",
            "⚰️ Cimitero": "💀 Scheletro Re",
            "🏚️ Casa degli Orrori": "👻 Custode Nightmare",
            "🏭 Fabbrica Abbandonata": "🤖 Robot Boss",
            "⛏️ Miniera Profonda": "⛏️ Golem di Ferro",
            "🌙 Cripta Maledetta": "🧙‍♂️ Lich Antico",
            "🌊 Mare": "🐙 Kraken Gigante",
            "🏔️ Montagna Sacra": "🦅 Fenice Antica",
            "🌋 Vulcano Attivo": "Signore del Fuoco",
            "👑 Palazzo Finale": "👑 Imperatore Oscuro"
        }
        
        # Se l'area ha un boss, controlla se è sconfitto
        if area in boss_aree_mappa:
            boss_nome = boss_aree_mappa[area]
            return boss_nome in self.boss_sconfitti
        
        # Se l'area non ha boss, è sempre "sconfitto"
        return True

    def combatti_mostri(self, e):
        """Reindirizza alla nuova schermata di combattimento"""
        self.page.go("/combattimento")
        
        
    def esegui_battaglia_dettagliata(self, area):
        """Esegue una battaglia dettagliata con narrazione estesa"""
        import threading
        import time
        
        def battaglia_con_narrazione():
            try:
                # Dati mostri per area
                mostri_area = {
                    "Villaggio": {"nome": "Topo Gigante", "hp": 80, "attacco": 3, "verso": "Squeak!"},
                    "🏠 Cantina": {"nome": "Ragno Peloso", "hp": 100, "attacco": 4, "verso": "Hiss!"},
                    "🚰 Fogne": {"nome": "Ratto delle Fogne", "hp": 120, "attacco": 5, "verso": "Screech!"},
                    "🌀 Labirinto Antico": {"nome": "Guardiano di Pietra", "hp": 140, "attacco": 6, "verso": "Rumble!"},
                    "❄️ Area Innevata": {"nome": "Lupo Gelido", "hp": 160, "attacco": 7, "verso": "Howl!"},
                    "🌿 Giungla Selvaggia": {"nome": "Serpente Velenoso", "hp": 180, "attacco": 8, "verso": "Ssss!"},
                    "🌲 Bosco Profondo": {"nome": "Orso Bruno", "hp": 200, "attacco": 9, "verso": "Roar!"},
                    "⚰️ Cimitero": {"nome": "Scheletro Errante", "hp": 220, "attacco": 10, "verso": "Clatter!"},
                    "🏚️ Casa degli Orrori": {"nome": "Fantasma Tormentato", "hp": 240, "attacco": 11, "verso": "Woooo!"},
                    "🏭 Fabbrica Abbandonata": {"nome": "Robot Malfunzionante", "hp": 260, "attacco": 12, "verso": "Beep-Error!"},
                    "⛏️ Miniera Profonda": {"nome": "Golem di Ferro", "hp": 280, "attacco": 13, "verso": "Clang!"},
                    "🌙 Cripta Maledetta": {"nome": "Lich Minore", "hp": 300, "attacco": 14, "verso": "Necro!"},
                    "🌊 Mare": {"nome": "Kraken Giovane", "hp": 320, "attacco": 15, "verso": "Splash!"},
                    "🏔️ Montagna Sacra": {"nome": "Drago di Montagna", "hp": 340, "attacco": 16, "verso": "Roooar!"},
                    "🌋 Vulcano Attivo": {"nome": "Elementale del Fuoco", "hp": 360, "attacco": 17, "verso": "Flame!"},
                    "👑 Palazzo Finale": {"nome": "Guardia Reale", "hp": 380, "attacco": 18, "verso": "En garde!"}
                }
                
                mostro = mostri_area.get(area, {"nome": "Mostro Sconosciuto", "hp": 100, "attacco": 5, "verso": "Grrr!"})
                hp_mostro = mostro["hp"]
                attacco_mostro = mostro["attacco"]
                nome_mostro = mostro["nome"]
                verso_mostro = mostro["verso"]
                
                # Ottieni gatto attivo e sue statistiche
                gatto = self.gatti[self.gatto_attivo]
                attacco_giocatore = self.calcola_attacco_totale()
                
                # Inizio battaglia
                self.aggiorna_storia(f" BATTAGLIA IN {area}")
                time.sleep(1.5)
                
                self.aggiorna_storia(f"🐾 {gatto['nome']} {gatto['emoji']} si prepara al combattimento!")
                time.sleep(2)
                
                self.aggiorna_storia(f"👹 Appare un {nome_mostro}!")
                self.aggiorna_storia(f"💀 '{verso_mostro}' - grida il mostro!")
                time.sleep(2)
                
                turno = 1
                
                while hp_mostro > 0 and self.hp_giocatore > 0:
                    self.aggiorna_storia(f"\n=== TURNO {turno} ===")
                    time.sleep(1)
                    
                    # Attacco del gatto
                    if gatto["abilita"] == "combattimento":
                        self.aggiorna_storia(f"🐾 {gatto['nome']} usa la sua abilità di combattimento!")
                        danno = attacco_giocatore + random.randint(2, 5)
                        self.riproduci_effetto("gatto_attacco")  # Suono durante il combattimento
                    else:
                        danno = attacco_giocatore + random.randint(1, 3)
                        self.riproduci_effetto("gatto_attacco")  # Suono durante il combattimento
                        
                    hp_mostro -= danno
                    
                    self.aggiorna_storia(f"🗡️ {gatto['nome']} attacca per {danno} danni!")
                    if random.choice([True, False]):
                        self.aggiorna_storia(f" '{random.choice(['Miao!', 'Hiss!', 'Purr!'])}' - verso di battaglia!")
                    
                    time.sleep(2)
                    
                    if hp_mostro <= 0:
                        break
                        
                    # Attacco del mostro
                    danno_ricevuto = max(1, attacco_mostro - random.randint(0, 2))
                    self.hp_giocatore -= danno_ricevuto
                    
                    self.aggiorna_storia(f"💥 {nome_mostro} contrattacca per {danno_ricevuto} danni!")
                    self.aggiorna_storia(f"👹 '{verso_mostro}' - ringhia minaccioso!")
                    
                    time.sleep(2)
                    
                    # Status check
                    self.aggiorna_storia(f" Tua vita: {self.hp_giocatore}/{self.hp_max}")
                    self.aggiorna_storia(f"👹 Vita mostro: {max(0, hp_mostro)}")
                    
                    time.sleep(1.5)
                    turno += 1
                
                # Risultato battaglia
                time.sleep(1)
                
                if hp_mostro <= 0:
                    # Ferma musica di battaglia SUBITO
                    self.termina_musica_battaglia()
                    
                    # Vittoria
                    self.aggiorna_storia(f"\n🎉 VITTORIA!")
                    self.aggiorna_storia(f" Hai sconfitto il {nome_mostro}!")
                    
                    # Effetto vittoria
                    print("🎉 Riproducendo effetto vittoria...")
                    self.riproduci_effetto("vittoria")
                    self.haptic_feedback("success")
                    
                    # Ricompense
                    exp_guadagnata = random.randint(15, 25)
                    oro_guadagnato = random.randint(20, 40)
                    
                    self.esperienza += exp_guadagnata
                    self.risorse["cibo"] += oro_guadagnato // 2
                    
                    self.aggiorna_storia(f" +{exp_guadagnata} esperienza")
                    self.aggiorna_storia(f"🥕 +{oro_guadagnato//2} cibo")
                    
                    # Gatto felice
                    gatto["felicita"] = min(100, gatto["felicita"] + 10)
                    gatto["affinita"] = min(100, gatto["affinita"] + 5)
                    
                    self.aggiorna_storia(f"😻 {gatto['nome']} è felice della vittoria!")
                    
                    # Aggiorna progressione area dopo vittoria
                    if self.area_attuale in self.progressione_area:
                        self.progressione_area[self.area_attuale] += 1
                        self.aggiorna_storia(f"Progressione {self.area_attuale}: {self.progressione_area[self.area_attuale]}/100")
                    
                else:
                    # Ferma musica di battaglia SUBITO
                    self.termina_musica_battaglia()
                    
                    # Sconfitta
                    self.aggiorna_storia(f"\n💀 SCONFITTA!")
                    self.aggiorna_storia(f"😿 {gatto['nome']} e tu siete stati sopraffatti...")
                    
                    # Effetto sconfitta SUBITO
                    self.riproduci_effetto("sconfitta")
                    self.haptic_feedback("error")
                    
                    # Penalità
                    self.hp_giocatore = max(1, self.hp_giocatore)
                    gatto["felicita"] = max(0, gatto["felicita"] - 5)
                
                # Fine battaglia
                time.sleep(1)
                self.aggiorna_storia(" La battaglia è finita.")
                
                # La musica è già stata terminata sopra
                
                # Aggiorna interfaccia
                self.aggiorna_stats_incrementali()
                
            except Exception as e:
                self.aggiorna_storia(f"❌ Errore durante la battaglia: {str(e)}")
                self.termina_musica_battaglia()
        
        # Avvia battaglia in thread separato per non bloccare l'interfaccia
        threading.Thread(target=battaglia_con_narrazione, daemon=True).start()
        
        
    def costruisci(self, e):
        """Sistema di costruzione"""
        if not self.gioco_iniziato:
            return
            
        # Controlla risorse disponibili
        costruzioni_possibili = []
        
        if self.risorse["legno"] >= 20 and self.risorse["pietra"] >= 10:
            costruzioni_possibili.append(("Casetta Gatti", 20, 10, 0))
            
        if self.risorse["legno"] >= 15:
            costruzioni_possibili.append(("Distributore Cibo", 15, 0, 0))
            
        if self.risorse["pietra"] >= 25:
            costruzioni_possibili.append(("Pozzo Acqua", 0, 25, 0))
            
        if self.risorse["ferro"] >= 10 and self.risorse["pietra"] >= 15:
            costruzioni_possibili.append(("Fucina", 0, 15, 10))
            
        if not costruzioni_possibili:
            self.aggiorna_storia("🏗️ Non hai abbastanza risorse per costruire!")
            self.haptic_feedback("warning")
            return
            
        # Costruisci la prima struttura possibile
        nome, legno_req, pietra_req, ferro_req = costruzioni_possibili[0]
        
        self.risorse["legno"] -= legno_req
        self.risorse["pietra"] -= pietra_req
        self.risorse["ferro"] -= ferro_req
        
        if nome == "Casetta Gatti":
            self.costruzioni["casette_gatti"] += 1
            testo = f"🏗️ Costruisci una {nome}!\n"
            testo += f" I gatti sono più felici e recuperano energia"
            
        elif nome == "Distributore Cibo":
            self.costruzioni["distributori_cibo"] += 1
            testo = f"🏗️ Costruisci un {nome}!\n"
            testo += f"🍽️ Produzione automatica di cibo"
            
        elif nome == "Pozzo Acqua":
            self.costruzioni["pozzi_acqua"] += 1
            testo = f"🏗️ Costruisci un {nome}!\n"
            testo += f"💧 Produzione automatica di acqua"
            
        elif nome == "Fucina":
            self.costruzioni["fucine"] += 1
            testo = f"🏗️ Costruisci una {nome}!\n"
            testo += f" Ora puoi creare armi migliori"
            
        self.haptic_feedback("success")
        self.riproduci_effetto("raccogli")
        self.aggiorna_storia(testo)
        self.aggiorna_stats_incrementali()
        
    def menu_cambia_area(self, e):
        """Menu per scegliere area con selezione"""
        if not self.gioco_iniziato:
            return
            
        if len(self.aree_sbloccate) <= 1:
            self.aggiorna_storia("🗺️ Devi sbloccare più aree esplorando!")
            self.haptic_feedback("warning")
            return
        
        # Crea menu di selezione area
        self.mostra_menu_selezione_area()
    
    def mostra_menu_selezione_area(self):
        """Mostra menu di selezione delle aree disponibili"""
        # Crea lista di bottoni per ogni area sbloccata
        bottoni_aree = []
        
        def crea_handler_area(area_target):
            """Crea handler per l'area specifica"""
            return lambda e: self.seleziona_area(e, area_target)
        
        for area in self.aree_sbloccate:
            # Evidenzia l'area corrente
            if area == self.area_attuale:
                testo_bottone = f" {area} (ATTUALE)"
                colore = ft.Colors.GREEN
            else:
                testo_bottone = f"🗺️ {area}"
                colore = ft.Colors.BLUE
            
            bottone = ft.ElevatedButton(
                text=testo_bottone,
                on_click=crea_handler_area(area),
                color=colore,
                width=300
            )
            bottoni_aree.append(bottone)
        
        # Bottone per annullare
        bottone_annulla = ft.ElevatedButton(
            text="Annulla",
            on_click=self.chiudi_menu_area,
            color=ft.Colors.RED,
            width=300
        )
        bottoni_aree.append(bottone_annulla)
        
        # Crea dialog con i bottoni
        self.dialog_area = ft.AlertDialog(
            title=ft.Text("🗺️ Scegli Area", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Column(
                controls=bottoni_aree,
                height=min(400, len(bottoni_aree) * 50),
                scroll=ft.ScrollMode.AUTO
            ),
            modal=True
        )
        
        # Mostra il dialog
        self.page.dialog = self.dialog_area
        self.dialog_area.open = True
        self.page.update()
    
    def seleziona_area(self, e, area_scelta):
        """Seleziona l'area scelta e chiude il menu"""
        # Chiudi il dialog
        self.dialog_area.open = False
        self.page.update()
        
        # Cambia area se diversa da quella attuale
        if area_scelta != self.area_attuale:
            self.cambia_area(area_scelta)
        else:
            self.aggiorna_storia(f" Sei già in {area_scelta}")
            self.haptic_feedback("light")
    
    def chiudi_menu_area(self, e):
        """Chiude il menu area senza cambiare"""
        self.dialog_area.open = False
        self.page.update()
        self.haptic_feedback("light")
        
    def vai_a_gesti_gatti(self, e):
        """Naviga alla schermata di gestione gatti"""
        if not self.gioco_iniziato:
            print("🐱 DEBUG: Gioco non iniziato, non posso navigare ai gatti")
            return
        
        print("🐱 DEBUG: Navigando a gestione gatti...")
        # Naviga alla schermata di gestione gatti
        self.page.go("/gatti")
        
    def rinomina_gatto(self, e):
        """Naviga alla schermata di rinomina gatto"""
        if not self.gioco_iniziato or not self.gatto_attivo:
            return
        
        # Salva il gatto da rinominare
        self.gatto_da_rinominare = self.gatto_attivo
        
        # Naviga alla schermata di rinomina
        self.page.go("/rinomina_gatto")
    
    def combatti_boss(self, e):
        """Sistema di combattimento contro boss delle aree"""
        if not self.gioco_iniziato:
            return
            
        area = self.area_attuale
        if area not in self.boss_aree:
            self.aggiorna_storia("❌ Nessun boss in quest'area!")
            self.haptic_feedback("warning")
            return
            
        boss_info = self.boss_aree[area]
        nome_boss = boss_info["nome"]
        
        # Controlla se il boss è già stato sconfitto
        if nome_boss in self.boss_sconfitti:
            self.aggiorna_storia(f"✅ Hai già sconfitto {nome_boss}!")
            return
            
        # Controlla requisiti speciali
        if boss_info.get("richiede_partner") and not self.ha_gatto_partner():
            self.aggiorna_storia(" Serve un gatto partner per affrontare questo boss!")
            self.haptic_feedback("warning")
            return
            
        if boss_info.get("richiede_casa") and not self.casa_nel_bosco_costruita:
            self.aggiorna_storia("🏠 Devi prima costruire una casa nel bosco!")
            self.haptic_feedback("warning")
            return
            
        if boss_info.get("richiede_nox") and not self.gatti["gatto_5"]["sbloccato"]:
            self.aggiorna_storia("🌌 Serve Nox per affrontare il Dream Eternal!")
            self.haptic_feedback("warning")
            return
            
        # Il boss sarà molto più forte se il giocatore è sotto-livello
        # Ma permettiamo comunque di combattere (e perdere!)
            
        if self.risorse["energia"] < 30:
            self.aggiorna_storia(" Serve più energia per affrontare un boss!")
            self.haptic_feedback("warning")
            return
            
        self.risorse["energia"] -= 30
        
        # 🎵 Avvia musica battaglia boss
        if area == "👑 Palazzo Finale" or nome_boss == "Dream Eternal":
            self.avvia_musica_battaglia("boss_finale")
        else:
            self.avvia_musica_battaglia("boss")
            
        # Inizia combattimento vero contro il boss - naviga alla schermata combattimento
        self.page.go("/combattimento")
        self.inizia_combattimento_boss(boss_info)
        return  # Esci dalla funzione senza eseguire il vecchio codice
        import threading
        import time
        
        def battaglia_boss_con_delay():
            time.sleep(3)  # Battaglia boss dura 3 secondi
            self.page.update()
        
        # Avvia battaglia boss in background
        threading.Thread(target=battaglia_boss_con_delay, daemon=True).start()
        
        # Calcola forza combattimento
        attacco_totale = self.calcola_attacco_totale()
        if self.gatto_attivo:
            gatto = self.gatti[self.gatto_attivo]
            if gatto["abilita"] == "combattimento":
                attacco_totale += gatto["attacco"]
                # Bonus critico da reliquie per gatti da combattimento
                bonus_critico = self.calcola_bonus_reliquie("critico_gatti")
                if bonus_critico > 0 and random.randint(1, 100) <= bonus_critico:
                    attacco_totale = int(attacco_totale * 1.5)  # Danno critico
                    
            if boss_info.get("richiede_partner") and self.ha_gatto_partner():
                attacco_totale += 15  # Bonus coppia
                # Bonus partner da reliquie
                bonus_partner = self.calcola_bonus_reliquie("boost_partner")
                attacco_totale += int(bonus_partner * 0.6)  # 60% del bonus come attacco extra
                
        # Bonus specifici contro tipi di nemici e protezioni da reliquie
        if nome_boss in ["💀 Lich Antico", "👹 Demone Custode"]:
            # Boss non morti
            bonus_undead = self.calcola_bonus_reliquie("undead_damage")
            attacco_totale += bonus_undead
            
        if nome_boss in ["👹 Demone Custode", "👻 Custode degli Incubi"]:
            # Boss fantasmi/demoni/spiriti
            bonus_fantasmi = self.calcola_bonus_reliquie("danno_fantasmi")
            attacco_totale += bonus_fantasmi
            
        if nome_boss in ["🦖 Rex Primordiale", "🐻 Grande Orso delle Radici"]:
            # Boss bestie
            bonus_bestie = self.calcola_bonus_reliquie("danno_bestie")
            attacco_totale += bonus_bestie
            
        if nome_boss in ["Signore del Magma"]:
            # Boss di fuoco - immunità da Cuore di Magma
            bonus_fuoco = self.calcola_bonus_reliquie("danno_fuoco")
            attacco_totale += bonus_fuoco
            
        # Protezione speciale da teletrasporto
        if nome_boss == "🏛️ Guardiano del Labirinto":
            # Bussola del Labirinto previene il teletrasporto
            if self.calcola_bonus_reliquie("anti_teletrasporto") > 0:
                attacco_totale += 20  # Bonus per aver neutralizzato l'abilità
                
        # Protezione divina contro attacchi potenti
        if self.calcola_bonus_reliquie("protezione_divina") > 0:
            if random.randint(1, 100) <= 20:  # 20% chance
                attacco_totale = int(attacco_totale * 1.5)  # Bonus protezione attivata
                
        # Resistenza al terrore per boss horror
        if nome_boss == "👻 Custode degli Incubi":
            resistenza_terrore = self.calcola_bonus_reliquie("resistenza_terrore")
            if resistenza_terrore > 0:
                # L'Amuleto Anti-Paura riduce l'effetto terrore del boss
                boss_attacco = int(boss_attacco * (1 - resistenza_terrore/100))
                attacco_totale += 15  # Bonus per resistere al terrore
                
        # Simula combattimento boss
        boss_hp = boss_info["hp"]
        boss_attacco = boss_info["attacco"]
        
        # Dream Eternal metamorfosi - cambia statistiche in base alla forma del regno
        if nome_boss == "🌌 Dream Eternal":
            if self.forma_regno_sogni == "luminoso":
                boss_hp = int(boss_hp * 0.8)  # Più debole in forma luminosa
                boss_attacco = int(boss_attacco * 0.9)
            elif self.forma_regno_sogni == "oscuro":
                boss_hp = int(boss_hp * 1.2)  # Più forte in forma oscura
                boss_attacco = int(boss_attacco * 1.1)
            # Forma neutrale mantiene stats originali
        
        # Controlla livello minimo richiesto per sconfiggere il boss
        livello_minimo_richiesto = self.calcola_livello_minimo_boss(area)
        livello_sufficiente = self.livello >= livello_minimo_richiesto
        
        if attacco_totale >= boss_attacco and self.hp_giocatore > 30 and livello_sufficiente:
            # VITTORIA!
            exp_guadagnata = boss_info["exp"]
            monete_guadagnate = random.randint(100, 200)
            
            self.esperienza += exp_guadagnata
            self.monete += monete_guadagnate
            self.boss_sconfitti.append(nome_boss)
            
            # Controlla sblocco gatti dopo boss sconfitto
            self.controlla_sblocco_gatti()
            
            # Effetto monete per boss
            self.riproduci_effetto("monete")
            
            # Controlla se è l'Imperatore Oscuro - sblocca portale sogni
            if nome_boss == "👑 Imperatore Oscuro":
                self.controlla_sblocco_portale_sogni()
            
            # Reliquie da boss speciali
            reliquie_specifiche = {
                "🏛️ Guardiano del Labirinto": "🌀 Bussola del Labirinto",
                "🦖 Rex Primordiale": "🌿 Zanna Primordiale", 
                "👻 Custode degli Incubi": "🏚️ Amuleto Anti-Paura",
                "🤖 Automa Corrotto": "🏭 Nucleo Energetico",
                "🐲 Drago di Cristallo": "⛏️ Piccone di Diamante",
                "👼 Angelo Custode": "🏔️ Benedizione Angelica",
                "Signore del Magma": "🌋 Cuore di Magma"
            }
            
            if nome_boss in reliquie_specifiche:
                if random.randint(1, 100) <= 70:  # 70% chance per boss specifici
                    self.ottieni_reliquia(reliquie_specifiche[nome_boss])
            elif nome_boss in ["💀 Lich Antico", "👹 Demone Custode"]:
                # Boss non morti danno reliquie speciali generiche
                reliquie_boss = [nome for nome, info in self.reliquie_database.items() 
                               if info["origine"] == "boss_speciale"]
                if reliquie_boss and random.randint(1, 100) <= 60:  # 60% chance
                    reliquia_boss = random.choice(reliquie_boss)
                    self.ottieni_reliquia(reliquia_boss)
            
            # Dream Eternal finale alternativo
            if nome_boss == "🌌 Dream Eternal":
                self.finale_alternativo_raggiunto = True
                # Dream Eternal garantisce reliquia leggendaria
                self.ottieni_reliquia("💎 Cristallo dell'Eternità")
                chiave_msg = "🌌 HAI RAGGIUNTO IL FINALE SEGRETO!"
                if self.forma_regno_sogni == "luminoso":
                    chiave_msg += "\n✨ Finale Luminoso: Il mondo è stato salvato dall'armonia!"
                elif self.forma_regno_sogni == "oscuro":
                    chiave_msg += "\n🌑 Finale Oscuro: Hai conquistato il regno con il caos!"
                else:
                    chiave_msg += "\n⚖️ Finale Equilibrato: L'equilibrio è stato ristabilito!"
            # Ottieni chiave
            elif boss_info["chiave"]:
                self.chiavi_raccolte.append(boss_info["chiave"])
                chiave_msg = f"🗝️ Ottieni: {boss_info['chiave']}"
            else:
                chiave_msg = "👑 Hai vinto l'avventura!"
                
            testo = f" COMBATTIMENTO EPICO vs {nome_boss}\n\n"
            testo += f"🎆 VITTORIA LEGGENDARIA!\n"
            testo += f" +{exp_guadagnata} EXP\n"
            testo += f" +{monete_guadagnate} monete\n"
            testo += f"{chiave_msg}\n"
            
            if self.gatto_attivo:
                gatto_nome = self.gatti[self.gatto_attivo]['nome']
                testo += f" {gatto_nome} è stato eroico!"
                # Bonus affinità per vittoria boss
                self.modifica_affinita(self.gatto_attivo, 5, "la vittoria epica")
                # Dialogo telepatico casuale
                self.dialogo_telepatico_casuale(self.gatto_attivo)
                # Effetto attacco gatto per boss
                if self.gatti[self.gatto_attivo]["abilita"] == "combattimento":
                    self.riproduci_effetto("gatto_attacco")
                
            self.haptic_feedback("success")
            self.riproduci_effetto("vittoria")
            
            # Sblocca area successiva
            self.sblocca_prossima_area()
            
        else:
            # Sconfitta parziale
            danno_subito = random.randint(20, 40)
            self.hp_giocatore = max(1, self.hp_giocatore - danno_subito)
            
            testo = f" COMBATTIMENTO vs {nome_boss}\n\n"
            if not livello_sufficiente:
                testo += f"😰 Il boss è troppo forte per il tuo livello!\n"
                testo += f" Livello richiesto: {livello_minimo_richiesto} (Attuale: {self.livello})\n"
                testo += f"💔 -{danno_subito} HP\n"
                testo += f" Ottieni più esperienza e riprova!"
            else:
                testo += f"😰 Il boss è troppo forte!\n"
                testo += f"💔 -{danno_subito} HP\n"
                testo += f"💪 Diventa più forte e riprova!"
            
            self.haptic_feedback("error")
            
        # Controlla livello
        testo_livello = self.gestisci_livello()
        if testo_livello:
            testo += "\n" + testo_livello
        
        # Controlla sblocco gatti
        self.controlla_sblocco_gatti()
            
        self.aggiorna_storia(testo)
        self.aggiorna_stats_incrementali()
        
        # 🎵 Termina musica battaglia boss
        self.termina_musica_battaglia()
        
    def mostra_notifica_boss_sbloccato(self, area):
        """Mostra notifica quando il boss dell'area viene sbloccato"""
        if area not in self.boss_aree:
            return
            
        boss_info = self.boss_aree[area]
        nome_boss = boss_info["nome"]
        
        # Crea dialog di notifica
        def affronta_boss_ora(e):
            dialog.open = False
            self.page.update()
            self.combatti_boss(e)
            
        def non_ora(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Boss Sbloccato!", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Text(f"Hai sbloccato il boss {nome_boss}!\n\nVuoi affrontarlo ora?", size=16),
            actions=[
                ft.TextButton(
                    text="Affronta Ora!",
                    on_click=affronta_boss_ora,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.RED_600,
                        color=ft.Colors.WHITE
                    )
                ),
                ft.TextButton(
                    text="❌ Non Ora",
                    on_click=non_ora,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.GREY_600,
                        color=ft.Colors.WHITE
                    )
                )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
        
    def calcola_livello_minimo_boss(self, area):
        """Calcola il livello minimo richiesto per sconfiggere il boss dell'area"""
        # Mappa le aree ai livelli minimi richiesti
        # Area 1 = livello 4, Area 2 = livello 8, etc.
        try:
            indice_area = self.aree_ordinate.index(area)
            # Il villaggio (indice 0) non ha boss
            # La cantina (indice 1) è la prima area con boss = livello 4
            # Le fogne (indice 2) è la seconda area con boss = livello 8
            if indice_area <= 0:
                return 1  # Nessun boss nel villaggio
            else:
                livello_minimo = indice_area * 4
                return livello_minimo
        except ValueError:
            # Area non trovata, probabilmente area speciale
            return 20  # Livello alto per aree speciali
        
    def ha_gatto_partner(self):
        """Controlla se hai un gatto con abilità partner sbloccato"""
        for gatto_id, gatto_info in self.gatti.items():
            if (gatto_info.get("sbloccato", False) and 
                gatto_info.get("abilita") == "partner"):
                return True
        return False
        
    def sblocca_prossima_area(self):
        """Sblocca la prossima area nella sequenza"""
        indice_attuale = self.aree_ordinate.index(self.area_attuale)
        if indice_attuale + 1 < len(self.aree_ordinate):
            prossima_area = self.aree_ordinate[indice_attuale + 1]
            if prossima_area not in self.aree_sbloccate:
                self.aree_sbloccate.append(prossima_area)
                
                # Controlla sblocco gatti dopo nuova area
                self.controlla_sblocco_gatti()
                
                self.aggiorna_storia(f"\n🎆 NUOVA AREA SBLOCCATA: {prossima_area}!")
                self.page.update()  # Refresh UI to show new area button immediately
                return True
        return False
        
    def pesca_nel_mare(self, e):
        """Pesca nel mare per ottenere pesce magico per i gatti"""
        if not self.gioco_iniziato:
            return
            
        if self.area_attuale != "🌊 Mare":
            self.aggiorna_storia("🎣 Puoi pescare solo nel Mare!")
            self.haptic_feedback("warning")
            return
            
        if self.risorse["energia"] < 15:
            self.aggiorna_storia(" Non hai abbastanza energia per pescare!")
            self.haptic_feedback("warning")
            return
            
        self.risorse["energia"] -= 15
        
        # Probabilità di catturare pesce
        possibilita = random.randint(1, 100)
        
        if possibilita <= 40:  # 40% pesce normale
            pesce_catturato = random.randint(2, 5)
            # Bonus doppio pesce da reliquie
            if self.calcola_bonus_reliquie("doppio_pesce") > 0:
                pesce_catturato *= 2
                testo = f"🎣 Peschi con successo!\n"
                testo += f"🌊 RELIQUIA ATTIVA: Doppio pesce!\n"
                testo += f"🐟 +{pesce_catturato} pesci catturati"
            else:
                testo = f"🎣 Peschi con successo!\n"
                testo += f"🐟 +{pesce_catturato} pesci catturati"
            self.pesce_raccolto += pesce_catturato
            
        elif possibilita <= 70:  # 30% pesce magico
            pesce_magico = random.randint(1, 3)
            self.pesce_raccolto += pesce_magico
            testo = f"🎣 Catturi del pesce magico!\n"
            testo += f"✨ +{pesce_magico} pesci magici"
            
        elif possibilita <= 85:  # 15% attacco squalo
            danno = random.randint(5, 15)
            self.hp_giocatore = max(1, self.hp_giocatore - danno)
            testo = f"🎣 Uno squalo attacca!\n"
            testo += f"🦈 -{danno} HP"
            self.haptic_feedback("medium")
            
        elif possibilita <= 95:  # 10% tesoro del mare
            tesoro_marino = random.choice(["🐚 conchiglia dorata", "⚓ ancora magica", "💎 perla gigante"])
            self.inventario.append(tesoro_marino)
            monete_bonus = random.randint(30, 60)
            self.monete += monete_bonus
            testo = f"🎣 Trovi un tesoro marino!\n"
            testo += f"✨ {tesoro_marino}\n"
            testo += f" +{monete_bonus} monete"
            
        else:  # 5% pesce magico raro (per portale sogni) o reliquia mare
            if random.randint(1, 100) <= 50:  # 50% pesce raro, 50% reliquia mare
                self.pesci_magici_rari += 1
                self.pesce_raccolto += 1
                testo = f"🎣 PESCE MAGICO RARO! ✨\n"
                testo += f" Questo pesce contiene essence oniriche!\n"
                testo += f"🐟 Pesci rari: {self.pesci_magici_rari}/3"
                
                # Controlla se possiamo sbloccare il portale
                if (self.pesci_magici_rari >= 3 and 
                    "👑 Imperatore Oscuro" in self.boss_sconfitti and 
                    self.tutti_gatti_max_livello()):
                    testo += f"\n🌌 Hai tutti i requisiti per il Portale dei Sogni!"
            else:
                # Scoperta reliquia marina rara
                reliquie_marine = [nome for nome, info in self.reliquie_database.items() 
                                 if info["origine"] == "mare_profondo"]
                if reliquie_marine:
                    reliquia_marina = random.choice(reliquie_marine)
                    self.ottieni_reliquia(reliquia_marina)
                    testo = f"🎣 SCOPERTA DELLE PROFONDITÀ! 🌊\n"
                    testo += f"🏛️ Antiche rovine sottomarine rivelate!"
            
        self.haptic_feedback("success")
        # Effetto diverso se ha gatto da raccolta attivo
        if self.gatto_attivo and self.gatti[self.gatto_attivo]["abilita"] in ["raccolta", "raccolta_suprema"]:
            self.riproduci_effetto("gatto_raccolta")
        else:
            self.riproduci_effetto("raccogli")
        self.aggiorna_storia(testo)
        self.aggiorna_stats_incrementali()
        
    def nutri_gatto_con_pesce(self, e):
        """Nutri il gatto con pesce magico per bonus speciali"""
        if not self.gioco_iniziato or not self.gatto_attivo:
            return
            
        if self.pesce_raccolto < 3:
            self.aggiorna_storia("🐟 Non hai abbastanza pesce! Serve almeno 3 pesci.")
            self.haptic_feedback("warning")
            return
            
        self.pesce_raccolto -= 3
        gatto = self.gatti[self.gatto_attivo]
        
        # Benefici del pesce magico
        gatto["felicita"] = 100
        gatto["fame"] = 100
        
        # Bonus affinità importante per nutrimento con pesce magico
        self.modifica_affinita(self.gatto_attivo, 30, "il delizioso pesce magico")
        gatto["livello"] = min(10, gatto["livello"] + 1)
        gatto["attacco"] += 2
        
        # Bonus esperienza
        exp_bonus = 20
        self.esperienza += exp_bonus
        
        testo = f"🐟 Nutri {gatto['nome']} con pesce magico!\n"
        testo += f" Livello gatto: {gatto['livello']}\n"
        testo += f" Attacco gatto: +2 (ora {gatto['attacco']})\n"
        testo += f"😊 Felicità e fame al massimo!\n"
        testo += f"✨ +{exp_bonus} EXP bonus"
        
        self.haptic_feedback("success")
        self.aggiorna_storia(testo)
        self.aggiorna_stats_incrementali()
        
    def costruisci_casa_nel_bosco(self, e):
        """Costruisce una casa nel bosco dopo aver sconfitto gli animali"""
        if not self.gioco_iniziato:
            return
            
        if self.area_attuale != "🌲 Bosco Profondo":
            self.aggiorna_storia("🏠 Puoi costruire la casa solo nel Bosco Profondo!")
            self.haptic_feedback("warning")
            return
            
        if self.casa_nel_bosco_costruita:
            self.aggiorna_storia("🏠 Hai già costruito la casa nel bosco!")
            return
            
        # Requisiti per costruire
        if (self.risorse["legno"] < 50 or self.risorse["pietra"] < 30 or 
            self.progressione_area["🌲 Bosco Profondo"] < 15):
            
            self.aggiorna_storia("🏠 Requisiti: 50 legno, 30 pietra, e aver esplorato l'area!")
            self.haptic_feedback("warning")
            return
            
        self.risorse["legno"] -= 50
        self.risorse["pietra"] -= 30
        self.casa_nel_bosco_costruita = True
        
        testo = f"🏠 Costruisci una bellissima casa nel bosco!\n"
        testo += f"🌲 Ora puoi sfidare il Grande Orso delle Radici!\n"
        testo += f" La casa ti dà protezione extra (+5 difesa)"
        
        self.difesa += 5
        
        self.haptic_feedback("success")
        self.riproduci_effetto("raccogli")
        self.aggiorna_storia(testo)
        self.aggiorna_stats_incrementali()
        
    def raccogli_ghiaccio(self, e):
        """Raccoglie cristalli di ghiaccio nell'area innevata"""
        if not self.gioco_iniziato:
            return
            
        if self.area_attuale != "❄️ Area Innevata":
            self.aggiorna_storia("🧊 Puoi raccogliere ghiaccio solo nell'Area Innevata!")
            self.haptic_feedback("warning")
            return
            
        if self.risorse["energia"] < 12:
            self.aggiorna_storia(" Non hai abbastanza energia!")
            self.haptic_feedback("warning")
            return
            
        self.risorse["energia"] -= 12
        
        # Raccolta ghiaccio con possibili eventi
        possibilita = random.randint(1, 100)
        
        if possibilita <= 50:  # 50% raccolta normale
            ghiaccio_raccolto = random.randint(3, 8)
            self.risorse["acqua"] += ghiaccio_raccolto
            testo = f"🧊 Raccogli cristalli di ghiaccio!\n"
            testo += f"💧 +{ghiaccio_raccolto} acqua (ghiaccio sciolto)"
            
        elif possibilita <= 75:  # 25% cristallo magico
            self.inventario.append("❄️ cristallo di ghiaccio magico")
            testo = f"🧊 Trovi un cristallo magico!\n"
            testo += f"✨ Cristallo di ghiaccio magico ottenuto!"
            
        else:  # 25% bufera improvvisa
            danno_freddo = random.randint(8, 15)
            self.hp_giocatore = max(1, self.hp_giocatore - danno_freddo)
            testo = f"🌨️ Una bufera improvvisa!\n"
            testo += f"❄️ -{danno_freddo} HP per il freddo"
            self.haptic_feedback("medium")
            
        self.haptic_feedback("success")
        # Effetto diverso se ha gatto da raccolta attivo
        if self.gatto_attivo and self.gatti[self.gatto_attivo]["abilita"] in ["raccolta", "raccolta_suprema"]:
            self.riproduci_effetto("gatto_raccolta")
        else:
            self.riproduci_effetto("raccogli")
        self.aggiorna_storia(testo)
        self.aggiorna_stats_incrementali()
        
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
        if "👑 corona reale" in self.inventario and " tesoro reale" in self.inventario:
            testo += "\n🎉 HAI COMPLETATO L'AVVENTURA! SEI IL NUOVO RE! 🎉"
            if self.audio_abilitato:
                self.riproduci_effetto("vittoria")
            self.haptic_feedback("success")
            
        self.aggiorna_storia(testo)
        
        # Assicurati di essere sulla schermata gioco e aggiorna i pulsanti
        if self.schermata_corrente != "gioco":
            self.page.go("/gioco")
        else:
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
                testo = f"✅ Hai raccolto: {oggetto}!\n Bonus: +{bonus} monete!"
            else:
                testo = f"✅ Hai raccolto: {oggetto}!"
                
            self.haptic_feedback("success")
            if self.audio_abilitato:
                # Effetto diverso se ha gatto da raccolta attivo
                if self.gatto_attivo and self.gatti[self.gatto_attivo]["abilita"] in ["raccolta", "raccolta_suprema"]:
                    self.riproduci_effetto("gatto_raccolta")
                else:
                    self.riproduci_effetto("raccogli")
                
            self.aggiorna_storia(testo)
            # Assicurati di essere sulla schermata gioco e aggiorna i pulsanti
            if self.schermata_corrente != "gioco":
                self.page.go("/gioco")
            else:
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
            
        testo += f"\n === EQUIPAGGIAMENTO ===\n"
        testo += f"🗡️ Arma: {self.equipaggiamento['arma'] or 'Nessuna'}\n"
        testo += f" Armatura: {self.equipaggiamento['armatura'] or 'Nessuna'}\n" 
        testo += f"💍 Accessorio: {self.equipaggiamento['accessorio'] or 'Nessuno'}\n"
        
        self.aggiorna_storia(testo)
        
    def equipaggia_oggetto(self, e):
        """Sistema di equipaggiamento"""
        if not self.gioco_iniziato:
            return
            
        if not self.inventario:
            self.aggiorna_storia("❌ Inventario vuoto!")
            return
            
        testo = " EQUIPAGGIA OGGETTO:\n\n"
        
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
            testo += f" Nuovo attacco: {self.calcola_attacco_totale()}\n"
            testo += f" Nuova difesa: {self.calcola_difesa_totale()}"
            
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
            testo += f" Ripristini {guarigione} HP!"
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
        
        testo = f"=== NEGOZIO {stanza_attuale} ===\n"
        testo += f" Le tue monete: {self.monete}\n\n"
        
        testo += " OGGETTI DISPONIBILI:\n"
        for nome, info in negozio.items():
            disponibile = "✅" if self.monete >= info["prezzo"] else "❌"
            testo += f"{disponibile} {nome} - {info['prezzo']} monete\n"
            testo += f"   📝 {info['descrizione']}\n\n"
            
        self.aggiorna_storia(testo)
        
    def mostra_azioni_oggetto(self, nome_oggetto):
        """Mostra finestra popup con azioni per l'oggetto"""
        def chiudi_popup(e):
            popup.open = False
            self.page.update()
            
        def equipaggia_oggetto(e):
            self.equipaggia_oggetto_specifico(nome_oggetto)
            chiudi_popup(e)
            
        def disequipaggia_oggetto(e):
            self.disequipaggia_oggetto_specifico(nome_oggetto)
            chiudi_popup(e)
            
        def usa_oggetto(e):
            self.usa_oggetto_specifico(nome_oggetto)
            chiudi_popup(e)
            
        def elimina_oggetto(e):
            self.elimina_oggetto_specifico(nome_oggetto)
            chiudi_popup(e)
        
        # Determina tipo di oggetto e azioni disponibili
        equipaggiato = (nome_oggetto in self.equipaggiamento.values())
        
        # Trova il tipo dell'oggetto
        tipo_oggetto = None
        for negozio in self.negozi.values():
            if nome_oggetto in negozio:
                tipo_oggetto = negozio[nome_oggetto]["tipo"]
                break
        
        azioni = []
        
        if tipo_oggetto in ["arma", "armatura", "accessorio"]:
            if equipaggiato:
                azioni.append(ft.ElevatedButton(
                    "Disequipaggia",
                    on_click=disequipaggia_oggetto,
                    width=200,
                    bgcolor=ft.Colors.ORANGE_600,
                    color=ft.Colors.WHITE
                ))
            else:
                azioni.append(ft.ElevatedButton(
                    "Equipaggia", 
                    on_click=equipaggia_oggetto,
                    width=200,
                    bgcolor=ft.Colors.GREEN_600,
                    color=ft.Colors.WHITE
                ))
        elif tipo_oggetto in ["cibo", "pozione"]:
            azioni.append(ft.ElevatedButton(
                "Usa",
                on_click=usa_oggetto,
                width=200,
                bgcolor=ft.Colors.BLUE_600,
                color=ft.Colors.WHITE
            ))
        
        # Azione elimina sempre disponibile
        azioni.append(ft.ElevatedButton(
            "Elimina",
            on_click=elimina_oggetto,
            width=200,
            bgcolor=ft.Colors.RED_600,
            color=ft.Colors.WHITE
        ))
        
        # Azione chiudi
        azioni.append(ft.ElevatedButton(
            "Chiudi",
            on_click=chiudi_popup,
            width=200,
            bgcolor=ft.Colors.GREY_600,
            color=ft.Colors.WHITE
        ))
        
        popup = ft.AlertDialog(
            title=ft.Text(f"Gestisci: {nome_oggetto}"),
            content=ft.Column([
                ft.Text(f"Cosa vuoi fare con {nome_oggetto}?", size=16),
                ft.Container(height=10),
                ft.Column(azioni, spacing=10)
            ], tight=True),
            actions_alignment=ft.MainAxisAlignment.CENTER
        )
        
        self.page.dialog = popup
        popup.open = True
        self.page.update()
        
    def vai_direttamente_al_gioco(self, e=None):
        """Va direttamente alla schermata di gioco, bypassando lo stack"""
        if self.gioco_iniziato:
            self.page.go("/gioco")
            self.haptic_feedback("light")
        else:
            self.page.go("/")
        
    def conta_oggetti_curativi(self):
        """Conta il numero totale di oggetti curativi nell'inventario"""
        totale = 0
        oggetti_curativi = ["Pozione Vita", "Pane", "Mela"]
        
        for oggetto in oggetti_curativi:
            if oggetto in self.inventario:
                totale += self.inventario[oggetto]
                
        return totale
        
    def equipaggia_oggetto_specifico(self, nome_oggetto):
        """Equipaggia un oggetto specifico"""
        if nome_oggetto not in self.inventario or self.inventario[nome_oggetto] <= 0:
            self.aggiorna_storia(f"❌ Non hai {nome_oggetto} nell'inventario!")
            return
            
        # Trova il tipo dell'oggetto
        tipo_oggetto = None
        for negozio in self.negozi.values():
            if nome_oggetto in negozio:
                tipo_oggetto = negozio[nome_oggetto]["tipo"]
                break
        
        if tipo_oggetto == "arma":
            slot = "arma"
        elif tipo_oggetto == "armatura":
            slot = "armatura" 
        elif tipo_oggetto == "accessorio":
            slot = "accessorio"
        else:
            self.aggiorna_storia(f"❌ {nome_oggetto} non può essere equipaggiato!")
            return
            
        # Se hai già qualcosa equipaggiato in quello slot, mettilo nell'inventario
        if self.equipaggiamento[slot]:
            vecchio_oggetto = self.equipaggiamento[slot]
            if vecchio_oggetto in self.inventario:
                self.inventario[vecchio_oggetto] += 1
            else:
                self.inventario[vecchio_oggetto] = 1
                
        # Equipaggia il nuovo oggetto
        self.equipaggiamento[slot] = nome_oggetto
        self.inventario[nome_oggetto] -= 1
        
        if self.inventario[nome_oggetto] <= 0:
            del self.inventario[nome_oggetto]
            
        testo = f"✅ {nome_oggetto} equipaggiato!\n"
        testo += f"🗡️ Attacco: {self.calcola_attacco_totale()}\n"
        testo += f"🛡️ Difesa: {self.calcola_difesa_totale()}"
        
        self.aggiorna_storia(testo)
        self.aggiorna_stats_incrementali()
        self.page.go("/inventario")  # Ricarica l'inventario
        
    def disequipaggia_oggetto_specifico(self, nome_oggetto):
        """Disequipaggia un oggetto specifico"""
        slot_trovato = None
        for slot, oggetto in self.equipaggiamento.items():
            if oggetto == nome_oggetto:
                slot_trovato = slot
                break
                
        if not slot_trovato:
            self.aggiorna_storia(f"❌ {nome_oggetto} non è equipaggiato!")
            return
            
        # Metti l'oggetto nell'inventario
        if nome_oggetto in self.inventario:
            self.inventario[nome_oggetto] += 1
        else:
            self.inventario[nome_oggetto] = 1
            
        # Rimuovi dall'equipaggiamento
        self.equipaggiamento[slot_trovato] = None
        
        testo = f"❌ {nome_oggetto} disequipaggiato!\n"
        testo += f"🗡️ Attacco: {self.calcola_attacco_totale()}\n"
        testo += f"🛡️ Difesa: {self.calcola_difesa_totale()}"
        
        self.aggiorna_storia(testo)
        self.aggiorna_stats_incrementali()
        self.page.go("/inventario")  # Ricarica l'inventario
        
    def usa_oggetto_specifico(self, nome_oggetto):
        """Usa un oggetto specifico (cibo/pozione)"""
        if nome_oggetto not in self.inventario or self.inventario[nome_oggetto] <= 0:
            self.aggiorna_storia(f"❌ Non hai {nome_oggetto} nell'inventario!")
            return
            
        self.inventario[nome_oggetto] -= 1
        if self.inventario[nome_oggetto] <= 0:
            del self.inventario[nome_oggetto]
            
        # Effetti dell'oggetto
        if "Pane" in nome_oggetto:
            cura = 15
            self.hp_giocatore = min(self.hp_max, self.hp_giocatore + cura)
            testo = f"🍞 Hai mangiato {nome_oggetto} e recuperato {cura} HP!"
        elif "Mela" in nome_oggetto:
            cura = 10
            self.hp_giocatore = min(self.hp_max, self.hp_giocatore + cura)
            testo = f"🍎 Hai mangiato {nome_oggetto} e recuperato {cura} HP!"
        elif "Pozione Vita" in nome_oggetto:
            cura = 50
            self.hp_giocatore = min(self.hp_max, self.hp_giocatore + cura)
            testo = f"🧪 Hai bevuto {nome_oggetto} e recuperato {cura} HP!"
        elif "Pozione Forza" in nome_oggetto:
            self.effetti_temporanei["forza"] = 3
            testo = f"💪 Hai bevuto {nome_oggetto}! +10 attacco per 3 turni!"
        else:
            testo = f"✅ Hai usato {nome_oggetto}!"
            
        self.aggiorna_storia(testo)
        self.aggiorna_stats_incrementali()
        self.page.go("/inventario")  # Ricarica l'inventario
        
    def elimina_oggetto_specifico(self, nome_oggetto):
        """Elimina un oggetto specifico dall'inventario"""
        if nome_oggetto not in self.inventario or self.inventario[nome_oggetto] <= 0:
            self.aggiorna_storia(f"❌ Non hai {nome_oggetto} nell'inventario!")
            return
            
        self.inventario[nome_oggetto] -= 1
        if self.inventario[nome_oggetto] <= 0:
            del self.inventario[nome_oggetto]
            
        self.aggiorna_storia(f"🗑️ {nome_oggetto} eliminato dall'inventario!")
        self.page.go("/inventario")  # Ricarica l'inventario
        
    def compra_oggetto_specifico(self, e, nome_oggetto, prezzo):
        """Compra un oggetto specifico dal negozio"""
        print(f"🛒 DEBUG: Tentativo acquisto {nome_oggetto} per {prezzo} monete")
        print(f"🎮 DEBUG: gioco_iniziato = {self.gioco_iniziato}")
        print(f"💰 DEBUG: monete attuali = {self.monete}")
        
        if not self.gioco_iniziato:
            print("❌ DEBUG: Gioco non iniziato!")
            self.aggiorna_storia("❌ Devi iniziare una partita prima di poter comprare oggetti!")
            return
            
        if self.monete < prezzo:
            testo = f"❌ Non hai abbastanza monete per comprare {nome_oggetto}!"
            testo += f"\nTi servono {prezzo} monete, ne hai {self.monete}"
        else:
            self.monete -= prezzo
            
            # Trova l'info dell'oggetto per la descrizione
            negozio = self.negozi.get(self.area_attuale, {})
            info = negozio.get(nome_oggetto, {"descrizione": "Oggetto misterioso"})
            
            # Auto-equipaggia armi e armature, altrimenti metti in inventario
            if info["tipo"] == "arma":
                # Se hai già un'arma, metti quella vecchia nell'inventario
                if self.equipaggiamento["arma"]:
                    vecchia_arma = self.equipaggiamento["arma"]
                    if vecchia_arma in self.inventario:
                        self.inventario[vecchia_arma] += 1
                    else:
                        self.inventario[vecchia_arma] = 1
                self.equipaggiamento["arma"] = nome_oggetto
            elif info["tipo"] == "armatura":
                # Se hai già un'armatura, metti quella vecchia nell'inventario
                if self.equipaggiamento["armatura"]:
                    vecchia_armatura = self.equipaggiamento["armatura"]
                    if vecchia_armatura in self.inventario:
                        self.inventario[vecchia_armatura] += 1
                    else:
                        self.inventario[vecchia_armatura] = 1
                self.equipaggiamento["armatura"] = nome_oggetto
            elif info["tipo"] == "accessorio":
                # Se hai già un accessorio, metti quello vecchio nell'inventario
                if self.equipaggiamento["accessorio"]:
                    vecchio_accessorio = self.equipaggiamento["accessorio"]
                    if vecchio_accessorio in self.inventario:
                        self.inventario[vecchio_accessorio] += 1
                    else:
                        self.inventario[vecchio_accessorio] = 1
                self.equipaggiamento["accessorio"] = nome_oggetto
            else:
                # Per oggetti consumabili (cibo, pozioni), metti in inventario
                if nome_oggetto in self.inventario:
                    self.inventario[nome_oggetto] += 1
                else:
                    self.inventario[nome_oggetto] = 1
            
            testo = f"✅ Acquistato: {nome_oggetto}\n"
            testo += f"💰 Costo: {prezzo} monete\n"
            testo += f"📝 {info['descrizione']}\n"
            
            # Mostra se equipaggiato automaticamente
            if info["tipo"] in ["arma", "armatura", "accessorio"]:
                testo += f"⚡ Equipaggiato automaticamente!\n"
                testo += f"🗡️ Attacco: {self.calcola_attacco_totale()}\n"
                testo += f"🛡️ Difesa: {self.calcola_difesa_totale()}\n"
            
            testo += f"💰 Monete rimaste: {self.monete}"
            
            self.haptic_feedback("success")
            if self.audio_abilitato:
                self.riproduci_effetto("monete")
                
            # Aggiorna i pulsanti del negozio per riflettere il nuovo stato
            self.crea_menu_negozio()
            
            # Aggiorna anche le statistiche
            self.aggiorna_stats_incrementali()
                
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
            if nome_oggetto in self.inventario:
                self.inventario[nome_oggetto] += 1
            else:
                self.inventario[nome_oggetto] = 1
            
            testo = f"✅ Acquistato: {nome_oggetto}\n"
            testo += f" Costo: {info['prezzo']} monete\n"
            testo += f"📝 {info['descrizione']}\n"
            testo += f" Monete rimaste: {self.monete}"
            
            self.haptic_feedback("success")
            if self.audio_abilitato:
                self.riproduci_effetto("monete")
            
            # Aggiorna i pulsanti dopo acquisto
            self.crea_menu_negozio()
            
            # Aggiorna le statistiche per mostrare le monete corrette
            self.aggiorna_stats_incrementali()
                
        self.aggiorna_storia(testo)
        
    def mostra_statistiche_dettagliate(self):
        """Statistiche complete del giocatore"""
        testo = f" === STATISTICHE GIOCATORE ===\n\n"
        testo += f" Livello: {self.livello}\n"
        testo += f" HP: {self.hp_giocatore}/{self.hp_max}\n"
        testo += f" Esperienza: {self.esperienza}/{self.esperienza_prossimo_livello}\n"
        testo += f" Attacco: {self.calcola_attacco_totale()} (base: {self.attacco_base})\n"
        testo += f" Difesa: {self.calcola_difesa_totale()}\n"
        testo += f" Monete: {self.monete}\n"
        testo += f"🎒 Oggetti inventario: {len(self.inventario)}\n"
        testo += f"🕐 Turni giocati: {self.turno}\n\n"
        
        if self.effetti_temporanei:
            testo += f"✨ Effetti attivi:\n"
            for effetto, turni in self.effetti_temporanei.items():
                testo += f"• {effetto}: {turni} turni\n"
        else:
            testo += "✨ Nessun effetto attivo\n"
            
        self.aggiorna_storia(testo)
        
    def salva_stato_immediato(self):
        """Salvataggio immediato senza interfaccia"""
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
            "volume_effetti": self.volume_effetti,
            "gatti": self.gatti,
            "gatto_attivo": self.gatto_attivo,
            "risorse": self.risorse,
            "aree_sbloccate": self.aree_sbloccate,
            "area_attuale": self.area_attuale,
            "progressione_area": self.progressione_area,
            "pesce_raccolto": self.pesce_raccolto
        }
        
        try:
            with open("avventura_epica_save.json", "w") as file:
                json.dump(stato_gioco, file, indent=2)
            print(f"💾 DEBUG: Salvataggio automatico completato - HP: {self.hp_giocatore}")
        except Exception as ex:
            print(f"❌ DEBUG: Errore salvataggio automatico: {str(ex)}")

    def salva_gioco(self, e):
        """Salvataggio completo"""
        print(f"🎮 DEBUG: Tentativo salvataggio - gioco_iniziato = {self.gioco_iniziato}")
        if not self.gioco_iniziato:
            print("❌ ERRORE: Impossibile salvare - gioco non iniziato!")
            self.aggiorna_storia("❌ Errore: Devi prima iniziare una partita!")
            self.haptic_feedback("error")
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
            "volume_effetti": self.volume_effetti,
            # Dati gatti (era mancante!)
            "gatti": self.gatti,
            "gatto_attivo": self.gatto_attivo,
            # Risorse (era mancante!)
            "risorse": self.risorse,
            # Altri dati importanti
            "aree_sbloccate": self.aree_sbloccate,
            "area_attuale": self.area_attuale,
            "progressione_area": self.progressione_area,
            "pesce_raccolto": self.pesce_raccolto
        }
        
        try:
            with open("avventura_epica_save.json", "w") as file:
                json.dump(stato_gioco, file, indent=2)
            print("✅ DEBUG: Salvataggio completato con successo!")
            
            # Salva stato per la vista di conferma
            self.salvataggio_successo = True
            self.salvataggio_errore = None
            self.page.go("/salvataggio_conferma")
            self.haptic_feedback("success")
            
        except Exception as ex:
            print(f"❌ DEBUG: Errore durante salvataggio: {str(ex)}")
            self.salvataggio_successo = False
            self.salvataggio_errore = str(ex)
            self.page.go("/salvataggio_conferma")
            self.haptic_feedback("error")
            
    def crea_vista_salvataggio_conferma(self):
        """Crea vista pulita di conferma salvataggio"""
        if getattr(self, 'salvataggio_successo', True):
            titolo = "✅ Partita Salvata"
            messaggio = "La tua avventura è stata salvata con successo!"
            colore = ft.Colors.GREEN_400
        else:
            titolo = "❌ Errore Salvataggio"
            messaggio = f"Errore durante il salvataggio:\n{getattr(self, 'salvataggio_errore', 'Errore sconosciuto')}"
            colore = ft.Colors.RED_400
        
        content = ft.Column([
            ft.Text(
                titolo,
                size=28,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                color=colore,
                style=ft.TextThemeStyle.HEADLINE_MEDIUM
            ),
            ft.Text(
                messaggio,
                size=18,
                text_align=ft.TextAlign.CENTER,
                color=ft.Colors.WHITE
            ),
            ft.ElevatedButton(
                text="Torna al Gioco",
                on_click=lambda e: self.page.go("/gioco"),
                width=200,
                height=50,
                bgcolor=ft.Colors.BLUE_600,
                color=ft.Colors.WHITE,
                tooltip="Torna alla schermata di gioco"
            )
        ], 
        spacing=40,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True)
        
        return ft.View(
            route="/salvataggio_conferma",
            controls=[
                ft.Container(
                    content=content,
                    bgcolor=ft.Colors.GREY_900,
                    padding=40,
                    expand=True
                )
            ],
            bgcolor=ft.Colors.GREY_900
        )

    def mostra_dialog_salvataggio(self, successo, errore=None):
        """Mostra dialog di conferma salvataggio"""
        if successo:
            titolo = "✅ Partita Salvata"
            messaggio = "La tua avventura è stata salvata con successo!"
        else:
            titolo = "❌ Errore"
            messaggio = f"Errore durante il salvataggio:\n{errore}"
        
        def chiudi_dialog(e):
            self.dialog_salvataggio.open = False
            self.page.update()
        
        self.dialog_salvataggio = ft.AlertDialog(
            modal=True,
            title=ft.Text(titolo, size=20, weight=ft.FontWeight.BOLD),
            content=ft.Text(messaggio, size=16),
            actions=[
                ft.TextButton("OK", on_click=chiudi_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.dialog = self.dialog_salvataggio
        self.dialog_salvataggio.open = True
        self.page.update()
        print(f"🎮 DEBUG: Dialog salvataggio mostrato - successo: {successo}")

    def mostra_conferma_salvataggio_pulita(self, successo, errore=None):
        """Mostra finestra pulita di conferma salvataggio"""
        print(f"🎮 DEBUG: Creando vista conferma - successo: {successo}")
        
        if successo:
            titolo = "Partita Salvata"
            messaggio = "Salvataggio completato!"
        else:
            titolo = "Errore Salvataggio"
            messaggio = f"Errore: {errore}"
        
        # Vista molto semplice per debug
        vista_conferma = ft.View(
            route="/salvataggio_conferma",
            controls=[
                ft.Text(titolo, size=24, color=ft.Colors.WHITE),
                ft.Text(messaggio, size=16, color=ft.Colors.WHITE),
                ft.ElevatedButton(
                    text="Indietro",
                    on_click=self.torna_alla_vista_precedente,
                    bgcolor=ft.Colors.BLUE_600,
                    color=ft.Colors.WHITE
                )
            ],
            bgcolor=ft.Colors.GREY_900
        )
        
        print(f"🎮 DEBUG: Creando vista conferma salvataggio")
        print(f"🎮 DEBUG: Views prima di aggiungere conferma: {[v.route for v in self.page.views]}")
        
        self.page.views.append(vista_conferma)
        self.analizza_accessibilita(vista_conferma)
        
        print(f"🎮 DEBUG: Views dopo aver aggiunto conferma: {[v.route for v in self.page.views]}")
        print(f"🎮 DEBUG: Navigando verso /salvataggio_conferma")
        
        self.page.go("/salvataggio_conferma")

    def torna_alla_vista_precedente(self, e):
        """Torna alla vista da cui si è venuti"""
        try:
            print(f"🎮 DEBUG: INIZIO - Tornando alla vista precedente")
            print(f"🎮 DEBUG: Views attuali: {[v.route for v in self.page.views]}")
            
            # Semplicemente rimuovi la vista corrente e torna indietro
            if len(self.page.views) > 1:
                self.page.views.pop()
                print(f"🎮 DEBUG: Vista rimossa, views rimaste: {[v.route for v in self.page.views]}")
                self.page.update()
                print(f"🎮 DEBUG: SUCCESSO - Navigazione completata")
            else:
                print(f"🎮 DEBUG: ERRORE - Non abbastanza views per tornare indietro")
                
        except Exception as ex:
            print(f"🎮 DEBUG: ERRORE in torna_alla_vista_precedente: {str(ex)}")
            import traceback
            traceback.print_exc()

    def mostra_conferma_salvataggio(self, successo, errore=None):
        """Mostra una schermata di conferma salvataggio accessibile"""
        if successo:
            titolo = "Salvataggio Completato"
            messaggio = "La tua avventura è stata salvata con successo!"
            colore_titolo = ft.Colors.GREEN_400
            icona = "✅"
        else:
            titolo = "Errore Salvataggio"
            messaggio = f"Si è verificato un errore durante il salvataggio:\n{errore}"
            colore_titolo = ft.Colors.RED_400
            icona = "❌"
        
        # Titolo principale per VoiceOver
        titolo_principale = ft.Text(
            titolo,
            size=24,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
            color=colore_titolo
        )
        
        # Crea vista con accessibilità migliorata
        content = ft.Column([
            titolo_principale,
            ft.Container(
                content=ft.Column([
                    # Icona separata per decorazione
                    ft.Text(
                        icona,
                        size=48,
                        text_align=ft.TextAlign.CENTER
                    ),
                    # Messaggio principale
                    ft.Text(
                        messaggio,
                        size=16,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.WHITE
                    ),
                    # Pulsante per tornare al gioco
                    ft.ElevatedButton(
                        text="Continua",
                        on_click=self.torna_al_gioco_da_conferma,
                        width=200,
                        height=50,
                        bgcolor=ft.Colors.PURPLE_600,
                        color=ft.Colors.WHITE,
                        tooltip="Torna al gioco"
                    )
                ], spacing=30),
                height=400,
                bgcolor=ft.Colors.GREY_800,
                border_radius=10,
                padding=10
            )
        ], scroll=ft.ScrollMode.AUTO, spacing=30, expand=True)
        
        vista_conferma = ft.View(
            route="/conferma_salvataggio",
            controls=[
                ft.Container(
                    content=content,
                    bgcolor=ft.Colors.GREY_900,
                    padding=20,
                    expand=True
                )
            ],
            bgcolor=ft.Colors.GREY_900
        )
        
        self.page.views.append(vista_conferma)
        self.analizza_accessibilita(vista_conferma)
        self.page.go("/conferma_salvataggio")
        
    def torna_al_gioco_da_conferma(self, e):
        """Torna al gioco dalla schermata di conferma salvataggio"""
        print(f"🎮 DEBUG: Tornando al gioco da conferma salvataggio")
        print(f"🎮 DEBUG: Views attuali: {[v.route for v in self.page.views]}")
        
        # Rimuovi tutte le views e ricrea quella del gioco
        self.page.views.clear()
        self.page.views.append(ft.View("/", []))  # Vista base
        vista_gioco = self.crea_vista_gioco()
        self.page.views.append(vista_gioco)
        self.analizza_accessibilita(vista_gioco)
        self.page.update()
        
        print(f"🎮 DEBUG: Dopo ricreazione: {[v.route for v in self.page.views]}")

    def controlla_sblocco_portale_sogni(self):
        """Controlla se il portale dei sogni può essere sbloccato"""
        # Condizioni: Imperatore sconfitto + tutti i gatti al max livello + pesci magici rari
        if (self.boss_sconfitti.count("👑 Imperatore Oscuro") >= 1 and 
            self.tutti_gatti_max_livello() and 
            self.pesci_magici_rari >= 3):
            
            if not self.portale_sogni_sbloccato:
                self.portale_sogni_sbloccato = True
                if self.area_segreta not in self.aree_sbloccate:
                    self.aree_sbloccate.append(self.area_segreta)
                    
                    # Controlla sblocco gatti dopo area segreta
                    self.controlla_sblocco_gatti()
                    
                self.gatti["gatto_5"]["sbloccato"] = True  # Sblocca Nox
                self.riavvolgimenti_disponibili = 3
                
                self.aggiorna_storia(f"\n🌌✨ PORTALE DEI SOGNI SBLOCCATO! ✨🌌\n"
                                   f"Il 5° gatto Nox si è risvegliato!\n"
                                   f"Hai {self.riavvolgimenti_disponibili} riavvolgimenti disponibili!\n"
                                   f"🌌 Regno dei Sogni ora accessibile!")
    
    def controlla_sblocco_gatti(self):
        """Controlla se i gatti possono essere sbloccati in base alla progressione"""
        
        # Shadow (gatto_2): Sbloccato dopo aver sconfitto 3 boss
        if not self.gatti["gatto_2"]["sbloccato"] and len(self.boss_sconfitti) >= 3:
            self.gatti["gatto_2"]["sbloccato"] = True
            self.gatti["gatto_2"]["fame"] = 100
            self.gatti["gatto_2"]["felicita"] = 100
            self.gatti["gatto_2"]["livello"] = 1
            self.aggiorna_storia(f"\n🐾✨ NUOVO COMPAGNO SBLOCCATO! ✨🐾\n"
                               f"Shadow si è unito al tuo gruppo!\n"
                               f"Abilità: Combattimento - Bonus danni in battaglia!\n"
                               f"Puoi selezionarlo dal menu Gesti Gatti.")
            self.haptic_feedback("success")
        
        # Luna (gatto_3): Sbloccata dopo aver raggiunto livello 5
        if not self.gatti["gatto_3"]["sbloccato"] and self.livello >= 5:
            self.gatti["gatto_3"]["sbloccato"] = True
            self.gatti["gatto_3"]["fame"] = 100
            self.gatti["gatto_3"]["felicita"] = 100
            self.gatti["gatto_3"]["livello"] = 1
            self.aggiorna_storia(f"\n🌙✨ NUOVO COMPAGNO SBLOCCATO! ✨🌙\n"
                               f"Luna si è unita al tuo gruppo!\n"
                               f"Abilità: Guarigione - Rigenera HP nel tempo!\n"
                               f"Puoi selezionarla dal menu Gesti Gatti.")
            self.haptic_feedback("success")
        
        # Stella (gatto_4): Sbloccata dopo aver esplorato 5 aree diverse
        if not self.gatti["gatto_4"]["sbloccato"] and len(self.aree_sbloccate) >= 5:
            self.gatti["gatto_4"]["sbloccato"] = True
            self.gatti["gatto_4"]["fame"] = 100
            self.gatti["gatto_4"]["felicita"] = 100
            self.gatti["gatto_4"]["livello"] = 1
            self.aggiorna_storia(f"\n✨ NUOVO COMPAGNO SBLOCCATO! ✨\n"
                               f"Stella si è unita al tuo gruppo!\n"
                               f"Abilità: Partner - Supporto in esplorazione!\n"
                               f"Puoi selezionarla dal menu Gesti Gatti.")
            self.haptic_feedback("success")
                
    def tutti_gatti_max_livello(self):
        """Controlla se tutti i gatti sbloccati sono al livello massimo"""
        for gatto_id, info in self.gatti.items():
            if info["sbloccato"] and gatto_id != "gatto_5":  # Escludi Nox
                if info["livello"] < 10:  # Livello max 10
                    return False
        return True
        
    def azione_scelta_onirica(self, scelta):
        """Gestisce le scelte oniriche nel Regno dei Sogni"""
        self.scelte_oniriche.append(scelta)
        
        if scelta == "armonia":
            self.forma_regno_sogni = "luminoso"
            # Bonus a tutti i gatti
            for gatto_id in self.gatti:
                if self.gatti[gatto_id]["sbloccato"]:
                    self.gatti[gatto_id]["felicita"] = min(100, self.gatti[gatto_id]["felicita"] + 20)
                    
        elif scelta == "caos":
            self.forma_regno_sogni = "oscuro"
            # Bonus combattimento ma malus felicità
            for gatto_id in self.gatti:
                if self.gatti[gatto_id]["sbloccato"]:
                    self.gatti[gatto_id]["attacco"] += 5
                    self.gatti[gatto_id]["felicita"] = max(20, self.gatti[gatto_id]["felicita"] - 10)
                    
        elif scelta == "equilibrio":
            self.forma_regno_sogni = "neutrale"
            # Bonus bilanciato
            self.hp_max += 50
            self.attacco_base += 10
            
        # Aggiorna descrizione area in base alla scelta
        self.aggiorna_descrizione_regno_sogni()
        
    def aggiorna_descrizione_regno_sogni(self):
        """Aggiorna la descrizione del Regno dei Sogni in base alle scelte"""
        if self.forma_regno_sogni == "luminoso":
            descrizione = "Un regno onirico luminoso dove i sogni più belli prendono forma. I tuoi gatti sono euforici e l'energia positiva permea tutto. Il Dream Eternal appare come una creatura di pura luce."
        elif self.forma_regno_sogni == "oscuro":
            descrizione = "Un regno onirico tormentato dove gli incubi regnano. L'oscurità ha corrotto questo mondo, ma i tuoi gatti sono diventati guerrieri temibili. Il Dream Eternal si manifesta come un'ombra minacciosa."
        else:  # neutrale
            descrizione = "Un regno onirico equilibrato dove sogni e incubi coesistono. Qui la realtà cambia forma secondo le tue scelte. Il Dream Eternal assume una forma cangiante, riflettendo la dualità del mondo."
            
        self.descrizioni["🌌 Regno dei Sogni"] = descrizione
        
    def usa_riavvolgimento_nox(self, e):
        """Usa l'abilità speciale di Nox per riavvolgere il tempo"""
        if not self.gatti["gatto_5"]["sbloccato"]:
            self.aggiorna_storia("❌ Nox non è ancora sbloccato!")
            return
            
        if self.riavvolgimenti_disponibili <= 0:
            self.aggiorna_storia("❌ Nessun riavvolgimento disponibile!")
            return
            
        if self.gatto_attivo != "gatto_5":
            self.aggiorna_storia("❌ Devi avere Nox come gatto attivo!")
            return
            
        # Riavvolgi HP e alcune risorse
        self.hp_giocatore = min(self.hp_max, self.hp_giocatore + 50)
        for risorsa in ["cibo", "acqua"]:
            self.risorse[risorsa] = min(100, self.risorse[risorsa] + 25)
            
        # Cura tutti i gatti
        for gatto_id in self.gatti:
            if self.gatti[gatto_id]["sbloccato"]:
                self.gatti[gatto_id]["fame"] = min(100, self.gatti[gatto_id]["fame"] + 30)
                self.gatti[gatto_id]["felicita"] = min(100, self.gatti[gatto_id]["felicita"] + 30)
                
        self.riavvolgimenti_disponibili -= 1
        
        self.aggiorna_storia(f"🌌 NOX RIAVVOLGE IL TEMPO! 🌌\n"
                           f"✨ HP ripristinati (+50)\n"
                           f"🍞 Cibo e acqua ripristinati (+25)\n"
                           f"😸 Tutti i gatti si sentono meglio!\n"
                           f"⏰ Riavvolgimenti rimasti: {self.riavvolgimenti_disponibili}")
        
        self.aggiorna_stats_incrementali()
        
    def ottieni_reliquia(self, nome_reliquia):
        """Ottieni una nuova reliquia e aggiungila alla collezione"""
        if nome_reliquia not in self.reliquie_possedute:
            self.reliquie_possedute.append(nome_reliquia)
            
            # Aggiungi alla collezione se non già presente
            if nome_reliquia not in self.reliquie_scoperte:
                self.reliquie_scoperte.append(nome_reliquia)
                
            info_reliquia = self.reliquie_database[nome_reliquia]
            rarita_emoji = {"raro": "🟢", "epico": "🟣", "leggendario": "🟡"}
            rarita_colore = rarita_emoji.get(info_reliquia["rarita"], "⚪")
            
            self.aggiorna_storia(f"✨ RELIQUIA OTTENUTA! ✨\n\n"
                               f"{rarita_colore} {nome_reliquia}\n"
                               f" {info_reliquia['descrizione']}\n"
                               f"🎯 Rarità: {info_reliquia['rarita'].upper()}")
                               
            self.haptic_feedback("success")
            self.riproduci_effetto("vittoria")
            
    def equipaggia_reliquia(self, nome_reliquia, slot):
        """Equipaggia una reliquia in uno slot specifico"""
        if nome_reliquia not in self.reliquie_possedute:
            return False
            
        # Rimuovi reliquia da altri slot se già equipaggiata
        for slot_id in self.reliquie_equipaggiate:
            if self.reliquie_equipaggiate[slot_id] == nome_reliquia:
                self.reliquie_equipaggiate[slot_id] = None
                
        self.reliquie_equipaggiate[slot] = nome_reliquia
        return True
        
    def rimuovi_reliquia(self, slot):
        """Rimuovi reliquia da uno slot"""
        self.reliquie_equipaggiate[slot] = None
        
    def calcola_bonus_reliquie(self, tipo_bonus):
        """Calcola i bonus delle reliquie equipaggiate per un tipo specifico"""
        bonus = 0
        for slot, reliquia in self.reliquie_equipaggiate.items():
            if reliquia and reliquia in self.reliquie_database:
                info = self.reliquie_database[reliquia]
                if info["effetto"] == tipo_bonus and info["tipo"] == "passivo":
                    bonus += info["valore"]
        return bonus
        
    def ha_reliquia_attivabile(self, effetto):
        """Controlla se ha una reliquia attivabile con un certo effetto"""
        for slot, reliquia in self.reliquie_equipaggiate.items():
            if reliquia and reliquia in self.reliquie_database:
                info = self.reliquie_database[reliquia]
                if info["effetto"] == effetto and info["tipo"] == "attivabile":
                    return True
        return False
        
    def usa_reliquia_attivabile(self, effetto):
        """Usa una reliquia attivabile (consuma uso se necessario)"""
        for slot, reliquia in self.reliquie_equipaggiate.items():
            if reliquia and reliquia in self.reliquie_database:
                info = self.reliquie_database[reliquia]
                if info["effetto"] == effetto and info["tipo"] == "attivabile":
                    # Qui potresti implementare logic per consumare usi
                    return True
        return False
        
    def genera_mini_dungeon(self, area):
        """Genera un mini dungeon nascosto nell'area"""
        if area in self.mini_dungeon_completati:
            return False
            
        # Probabilità di trovare mini dungeon
        if random.randint(1, 100) <= 15:  # 15% chance
            self.mini_dungeon_completati.append(area)
            
            # Scegli reliquia casuale da mini dungeon
            reliquie_dungeon = [nome for nome, info in self.reliquie_database.items() 
                              if info["origine"] == "mini_dungeon"]
            if reliquie_dungeon:
                reliquia_trovata = random.choice(reliquie_dungeon)
                self.ottieni_reliquia(reliquia_trovata)
                return True
        return False
        
    def incontra_npc_raro(self, area):
        """Incontra un NPC raro che offre reliquie"""
        npc_key = f"npc_{area}"
        if npc_key in self.npc_rari_incontrati:
            return False
            
        if random.randint(1, 100) <= 8:  # 8% chance
            self.npc_rari_incontrati.append(npc_key)
            
            npc_nomi = {
                "Villaggio": "🧙‍♂️ Sage Merlino",
                "🌲 Bosco Profondo": "🦌 Spirito del Bosco",
                "🌊 Mare": "🧜‍♀️ Sirena Antica",
                "⚰️ Cimitero": "👻 Fantasma Benevolo",
                "🌌 Regno dei Sogni": "🌙 Mercante Onirico"
            }
            
            npc_nome = npc_nomi.get(area, "🔮 Mercante Misterioso")
            
            # Scegli reliquia da NPC
            reliquie_npc = [nome for nome, info in self.reliquie_database.items() 
                           if info["origine"] == "npc_raro"]
            if reliquie_npc:
                reliquia_offerta = random.choice(reliquie_npc)
                
                self.aggiorna_storia(f"✨ INCONTRO RARO! ✨\n\n"
                                   f"{npc_nome} appare davanti a te!\n"
                                   f"💬 'Prendi questo, ti servirà...'\n")
                                   
                self.ottieni_reliquia(reliquia_offerta)
                return True
        return False
        
    def gestisci_reliquie(self, e):
        """Naviga alla schermata di gestione reliquie"""
        # Naviga alla schermata di gestione reliquie
        self.page.go("/gestione_reliquie")
        
    def applica_bonus_reliquie_gatti(self):
        """Applica bonus reliquie ai gatti passivamente"""
        # Regenerazione HP gatti
        regen_bonus = self.calcola_bonus_reliquie("regen_gatti")
        if regen_bonus > 0:
            for gatto_id, gatto in self.gatti.items():
                if gatto["sbloccato"] and gatto["fame"] < 100:
                    self.gatti[gatto_id]["fame"] = min(100, gatto["fame"] + regen_bonus)
                    
        # Bonus esperienza e felicità
        exp_bonus = self.calcola_bonus_reliquie("exp_felicita_gatti")
        if exp_bonus > 0:
            # Questo bonus viene applicato quando i gatti guadagnano EXP
            pass  # Implementato nelle funzioni che danno EXP
            
    def modifica_affinita(self, gatto_id, incremento, motivo=""):
        """Modifica l'affinità di un gatto e controlla milestone"""
        if gatto_id not in self.gatti or not self.gatti[gatto_id]["sbloccato"]:
            return
            
        gatto = self.gatti[gatto_id]
        vecchia_affinita = gatto["affinita"]
        gatto["affinita"] = max(0, min(250, gatto["affinita"] + incremento))  # Cap a 250
        
        # Controlla se ha raggiunto una nuova milestone
        for milestone, emoji in self.affinita_milestone.items():
            if vecchia_affinita < milestone <= gatto["affinita"]:
                self.raggiunta_milestone_affinita(gatto_id, milestone)
                
        # Messaggio di feedback positivo
        if incremento > 0 and motivo:
            self.aggiorna_storia(f" {gatto['nome']} apprezza {motivo}! (+{incremento} affinità)")
            
    def raggiunta_milestone_affinita(self, gatto_id, milestone):
        """Gestisce il raggiungimento di milestone di affinità"""
        gatto = self.gatti[gatto_id]
        emoji = self.affinita_milestone[milestone]
        
        if milestone == 50:  # 💛 Abilità passiva bonus
            self.sblocca_bonus_passivo(gatto_id)
        elif milestone == 100:  # 💚 Scena speciale
            self.mostra_scena_speciale(gatto_id)
        elif milestone == 150:  # 💙 Abilità evoluta
            self.evolvi_abilita_gatto(gatto_id)
        elif milestone == 200:  #  Forma evoluta
            self.evolvi_forma_gatto(gatto_id)
            
        self.aggiorna_storia(f"\n{emoji} MILESTONE AFFINITÀ RAGGIUNTA! {emoji}\n"
                           f" {gatto['nome']} ha raggiunto {milestone} punti affinità!\n")
                           
    def sblocca_bonus_passivo(self, gatto_id):
        """Sblocca bonus passivo per il gatto"""
        gatto = self.gatti[gatto_id]
        evoluzione = self.gatti_evoluzione[gatto_id]
        
        if evoluzione["bonus_passivo"] == "schivata_5":
            bonus_desc = "+5% probabilità di schivare attacchi"
        elif evoluzione["bonus_passivo"] == "critico_15":
            bonus_desc = "+15% probabilità di critico"
        elif evoluzione["bonus_passivo"] == "luce_nelle_tenebre":
            bonus_desc = "Illumina aree oscure e +10% guarigione"
        elif evoluzione["bonus_passivo"] == "sincronia_perfetta":
            bonus_desc = "+20% efficacia quando lavora in coppia"
        else:
            bonus_desc = "Bonus speciale sbloccato"
            
        self.aggiorna_storia(f"✨ BONUS PASSIVO SBLOCCATO!\n"
                           f" {gatto['nome']}: {bonus_desc}")
                           
    def mostra_scena_speciale(self, gatto_id):
        """Mostra la scena speciale del gatto"""
        gatto = self.gatti[gatto_id]
        evoluzione = self.gatti_evoluzione[gatto_id]
        
        if "scena_100" not in gatto["scene_viste"]:
            gatto["scene_viste"].append("scena_100")
            
            self.aggiorna_storia(f"💚 === SCENA SPECIALE: {gatto['nome']} === 💚\n\n"
                               f"{evoluzione['storia']}\n\n"
                               f"💭 {gatto['nome']}: '{evoluzione['dialoghi'][0]}'\n"
                               f"Il vostro legame si è rafforzato profondamente...")
                               
    def evolvi_abilita_gatto(self, gatto_id):
        """Evolve l'abilità principale del gatto"""
        gatto = self.gatti[gatto_id]
        evoluzione = self.gatti_evoluzione[gatto_id]
        
        abilita_vecchia = gatto["abilita"]
        gatto["abilita"] = evoluzione["abilita_evoluta"]
        
        descrizioni_evolute = {
            "raccolta_suprema": "Trova tesori rari e può raccogliere in aree multiple",
            "combattimento_fulmineo": "Attacchi multipli e danno elettrico",
            "guarigione_celestiale": "Cura anche il giocatore ogni 3 turni",
            "partnership_galattica": "Potenzia enormemente i compagni di squadra",
            "controllo_temporale": "Può rallentare il tempo e prevedere attacchi"
        }
        
        desc = descrizioni_evolute.get(gatto["abilita"], "Abilità potenziata")
        
        self.aggiorna_storia(f"💙 ABILITÀ EVOLUTA! 💙\n"
                           f" {gatto['nome']}: {abilita_vecchia} → {gatto['abilita']}\n"
                           f" {desc}")
                           
    def evolvi_forma_gatto(self, gatto_id):
        """Evolve la forma del gatto alla versione suprema"""
        gatto = self.gatti[gatto_id]
        evoluzione = self.gatti_evoluzione[gatto_id]
        
        gatto["forma_evoluta"] = True
        nome_vecchio = gatto["nome"]
        gatto["nome"] = evoluzione["nome_evoluto"]
        
        # Bonus statistiche per forma evoluta
        gatto["attacco"] += 10
        gatto["livello"] = max(gatto["livello"], 5)
        
        self.aggiorna_storia(f" FORMA EVOLUTA SUPREMA! \n"
                           f"✨ {nome_vecchio} si trasforma in {gatto['nome']}!\n"
                           f" +10 attacco, bonus supremi sbloccati!\n"
                           f"💭 '{evoluzione['dialoghi'][1]}'")
                           
    def dialogo_telepatico_casuale(self, gatto_id):
        """Mostra dialogo telepatico casuale basato sull'affinità"""
        if random.randint(1, 100) > 15:  # 15% chance
            return
            
        gatto = self.gatti[gatto_id]
        if gatto["affinita"] < 50:
            return
            
        evoluzione = self.gatti_evoluzione[gatto_id]
        dialogo = random.choice(evoluzione["dialoghi"])
        
        self.aggiorna_storia(f"💭 {gatto['nome']}: {dialogo}")
        
    def aggiorna_contatori_affinita(self):
        """Aggiorna contatori per penalità affinità"""
        # Penalizza gatti non usati
        for gatto_id, gatto in self.gatti.items():
            if gatto["sbloccato"] and gatto_id != self.gatto_attivo:
                gatto["aree_non_usato"] += 1
                if gatto["aree_non_usato"] >= 5:  # 5 aree senza uso
                    self.modifica_affinita(gatto_id, -5, "si sente trascurato")
                    gatto["aree_non_usato"] = 0
                    
        # Bonus per gatto attivo
        if self.gatto_attivo:
            self.modifica_affinita(self.gatto_attivo, 1, "è al tuo fianco")
            
    def mostra_legame_gatti(self, e):
        """Mostra interfaccia legame emotivo con i gatti"""
        testo = " === LEGAME EMOTIVO CON I GATTI === \n\n"
        
        for gatto_id, gatto in self.gatti.items():
            if not gatto["sbloccato"]:
                continue
                
            nome = gatto["nome"]
            affinita = gatto["affinita"]
            
            # Emoji affinità
            if affinita >= 200:
                affinita_emoji = ""
                status = "LEGAME SUPREMO"
            elif affinita >= 150:
                affinita_emoji = "💙"
                status = "ABILITÀ EVOLUTA"
            elif affinita >= 100:
                affinita_emoji = "💚"
                status = "STORIA SBLOCCATA"
            elif affinita >= 50:
                affinita_emoji = "💛"
                status = "BONUS PASSIVO"
            else:
                affinita_emoji = ""
                status = "IN CRESCITA"
                
            testo += f"{gatto['emoji']} {nome}:\n"
            testo += f"    Affinità: {affinita_emoji} {affinita}/200 ({status})\n"
            
            if gatto["forma_evoluta"]:
                evoluzione = self.gatti_evoluzione[gatto_id]
                testo += f"   ✨ EVOLUTO: {evoluzione['nome_evoluto']}\n"
                
            if not gatto["nome_personalizzato"] and affinita < 50:
                testo += f"   📝 Puoi dare un nome personalizzato! (+20 affinità)\n"
                
            testo += f"   🎯 Abilità: {gatto['abilita']}\n\n"
            
        # Suggerimenti per aumentare affinità
        testo += " COME AUMENTARE L'AFFINITÀ:\n"
        testo += "• Usalo in battaglia e esplorazione (+1 per azione)\n"
        testo += "• Nutrilo con pesce magico (+30)\n"
        testo += "• Dagli un nome personalizzato (+20)\n"
        testo += "• Riposare insieme nella casa del bosco (+10)\n"
        testo += "• Evita di farlo sconfiggere (+5 per sopravvivenza)\n\n"
        
        testo += "⚠️ L'affinità diminuisce se ignori un gatto per troppe aree!"
        
        self.aggiorna_storia(testo)
        
    def rinomina_gatto_personalizzato(self, gatto_id, nuovo_nome):
        """Rinomina un gatto con nome personalizzato"""
        if gatto_id not in self.gatti or not self.gatti[gatto_id]["sbloccato"]:
            return False
            
        gatto = self.gatti[gatto_id]
        if gatto["nome_personalizzato"]:
            return False  # Già rinominato
            
        gatto["nome"] = nuovo_nome
        gatto["nome_personalizzato"] = True
        
        # Bonus affinità importante per naming
        self.modifica_affinita(gatto_id, 20, "il nome speciale che gli hai dato")
        
        self.aggiorna_storia(f" {nuovo_nome} apprezza molto il nome che gli hai dato!\n"
                           f"Il vostro legame si è rafforzato!")
        return True
        
    def riposa_con_gatto_in_casa(self):
        """Riposa con il gatto nella casa del bosco per bonus affinità"""
        if not self.casa_nel_bosco_costruita:
            return False
            
        if not self.gatto_attivo or not self.gatti[self.gatto_attivo]["sbloccato"]:
            return False
            
        gatto = self.gatti[self.gatto_attivo]
        nome = gatto["nome"]
        
        # Bonus affinità per riposo insieme
        self.modifica_affinita(self.gatto_attivo, 10, "il riposo tranquillo insieme")
        
        # Bonus secondari
        gatto["felicita"] = min(100, gatto["felicita"] + 20)
        self.hp_giocatore = min(self.hp_max, self.hp_giocatore + 15)
        
        self.aggiorna_storia(f"🏠 Riposi pacificamente con {nome} nella casa del bosco.\n"
                           f" Il vostro legame si rafforza durante il riposo.\n"
                           f"✨ Ti senti riposato (+15 HP) e {nome} è felice!")
        
        # Dialogo telepatico speciale durante riposo
        if gatto["affinita"] >= 100:
            evoluzione = self.gatti_evoluzione[self.gatto_attivo]
            dialogo_riposo = f"💭 {nome}: {random.choice(evoluzione['dialoghi'])}"
            self.aggiorna_storia(dialogo_riposo)
            
        return True
        
    def naviga_labirinto(self, e):
        """Naviga attraverso il labirinto con pareti che si spostano"""
        if not self.gioco_iniziato or self.area_attuale != "🌀 Labirinto Antico":
            return
            
        if self.risorse["energia"] < 20:
            self.aggiorna_storia(" Serve più energia per navigare il labirinto!")
            self.haptic_feedback("warning")
            return
            
        self.risorse["energia"] -= 20
        
        # Bussola del Labirinto aiuta
        bonus_navigazione = self.calcola_bonus_reliquie("anti_teletrasporto")
        successo_base = 60 + (bonus_navigazione * 0.2)  # Max 80% con reliquia
        
        if random.randint(1, 100) <= successo_base:
            tesoro = random.choice(["🗝️ chiave antica", " monete dimenticate", " mappa magica"])
            self.inventario.append(tesoro)
            monete_bonus = random.randint(30, 60)
            self.monete += monete_bonus
            
            testo = f"🌀 Navighi con successo il labirinto!\n"
            testo += f"✨ Trovi: {tesoro}\n"
            testo += f" +{monete_bonus} monete"
            
            # Chance di trovare reliquia del labirinto
            if random.randint(1, 100) <= 15:
                self.ottieni_reliquia("🌀 Bussola del Labirinto")
        else:
            testo = f"🌀 Ti perdi nel labirinto...\n"
            testo += f"Le pareti si spostano confondendoti!"
            
        self.aggiorna_storia(testo)
        self.aggiorna_stats_incrementali()
        
    def raccogli_erbe_medicinali(self, e):
        """Raccogli erbe curative nella giungla"""
        if not self.gioco_iniziato or self.area_attuale != "🌿 Giungla Selvaggia":
            return
            
        if self.risorse["energia"] < 15:
            self.aggiorna_storia(" Serve energia per raccogliere erbe!")
            return
            
        self.risorse["energia"] -= 15
        
        erbe_raccolte = random.randint(2, 5)
        bonus_hp = erbe_raccolte * 10
        self.hp_giocatore = min(self.hp_max, self.hp_giocatore + bonus_hp)
        
        # Bonus per gatti
        if self.gatto_attivo:
            gatto = self.gatti[self.gatto_attivo]
            gatto["felicita"] = min(100, gatto["felicita"] + 15)
            self.modifica_affinita(self.gatto_attivo, 2, "le erbe medicinali")
            
        testo = f"🌿 Raccogli {erbe_raccolte} erbe medicinali!\n"
        testo += f" +{bonus_hp} HP ripristinati\n"
        testo += f"😸 Il tuo gatto apprezza le erbe!"
        
        # Chance di Zanna Primordiale
        if random.randint(1, 100) <= 12:
            self.ottieni_reliquia("🌿 Zanna Primordiale")
            
        self.aggiorna_storia(testo)
        self.aggiorna_stats_incrementali()
        
    def ripara_macchinari(self, e):
        """Ripara automi nella fabbrica per componenti"""
        if not self.gioco_iniziato or self.area_attuale != "🏭 Fabbrica Abbandonata":
            return
            
        if self.risorse["energia"] < 25:
            self.aggiorna_storia(" Serve molta energia per riparare i macchinari!")
            return
            
        self.risorse["energia"] -= 25
        
        componenti = random.randint(3, 8)
        self.risorse["ferro"] += componenti
        monete_tech = random.randint(40, 80)
        self.monete += monete_tech
        
        testo = f"🔧 Ripari con successo un automa!\n"
        testo += f"⚙️ +{componenti} componenti di ferro\n"
        testo += f" +{monete_tech} monete tecnologiche"
        
        # Chance di Nucleo Energetico
        if random.randint(1, 100) <= 8:
            self.ottieni_reliquia("🏭 Nucleo Energetico")
            
        self.aggiorna_storia(testo)
        self.aggiorna_stats_incrementali()
        
    def estrai_cristalli(self, e):
        """Estrai cristalli magici nella miniera"""
        if not self.gioco_iniziato or self.area_attuale != "⛏️ Miniera Profonda":
            return
            
        if self.risorse["energia"] < 30:
            self.aggiorna_storia(" L'estrazione richiede molta energia!")
            return
            
        self.risorse["energia"] -= 30
        
        cristalli_base = random.randint(2, 6)
        # Bonus da Piccone di Diamante
        if self.calcola_bonus_reliquie("raccolta_cristalli") > 0:
            cristalli_base *= 2
            
        self.risorse["pietra"] += cristalli_base
        
        # Chance di gemme rare
        chance_gemme = 20 + self.calcola_bonus_reliquie("raccolta_cristalli") * 0.15
        if random.randint(1, 100) <= chance_gemme:
            gemma_rara = random.choice(["💎 diamante puro", "🔮 cristallo magico", "💠 ametista sacra"])
            self.inventario.append(gemma_rara)
            gemma_msg = f"\n✨ GEMMA RARA: {gemma_rara}!"
        else:
            gemma_msg = ""
            
        testo = f"⛏️ Estrai {cristalli_base} cristalli magici!{gemma_msg}"
        
        # Chance di Piccone di Diamante
        if random.randint(1, 100) <= 10:
            self.ottieni_reliquia("⛏️ Piccone di Diamante")
            
        self.aggiorna_storia(testo)
        self.aggiorna_stats_incrementali()
        
    def prega_al_tempio(self, e):
        """Prega al tempio della montagna sacra"""
        if not self.gioco_iniziato or self.area_attuale != "🏔️ Montagna Sacra":
            return
            
        # La preghiera non costa energia ma ha cooldown
        if hasattr(self, 'ultima_preghiera'):
            if self.turno - self.ultima_preghiera < 3:
                self.aggiorna_storia("🙏 Devi aspettare prima di pregare di nuovo...")
                return
                
        self.ultima_preghiera = self.turno
        
        # Benedizioni divine
        benedizione = random.choice([
            "hp_max", "attacco", "felicita_gatti", "energia_max"
        ])
        
        if benedizione == "hp_max":
            self.hp_max += 10
            self.hp_giocatore = self.hp_max
            msg = " I tuoi HP massimi aumentano di 10!"
        elif benedizione == "attacco":
            self.attacco_base += 3
            msg = " Il tuo attacco base aumenta di 3!"
        elif benedizione == "felicita_gatti":
            for gatto_id, gatto in self.gatti.items():
                if gatto["sbloccato"]:
                    gatto["felicita"] = 100
                    self.modifica_affinita(gatto_id, 5, "la benedizione divina")
            msg = "😸 Tutti i tuoi gatti sono benedetti dalla felicità!"
        else:  # energia_max
            self.risorse["energia"] = 100
            msg = " La tua energia è completamente ripristinata!"
            
        testo = f"🙏 Preghi al tempio sacro...\n{msg}"
        
        # Chance di Benedizione Angelica
        if random.randint(1, 100) <= 5:
            self.ottieni_reliquia("🏔️ Benedizione Angelica")
            
        self.aggiorna_storia(testo)
        self.aggiorna_stats_incrementali()
        
    def esplora_stanze_orrore(self, e):
        """Esplora le stanze infestate della Casa degli Orrori"""
        if not self.gioco_iniziato or self.area_attuale != "🏚️ Casa degli Orrori":
            return
            
        if self.risorse["energia"] < 25:
            self.aggiorna_storia(" Le stanze dell'orrore richiedono molta energia mentale!")
            self.haptic_feedback("warning")
            return
            
        self.risorse["energia"] -= 25
        
        # Eventi horror casuali che influenzano la sanità
        eventi_horror = [
            {
                "nome": "specchio_infranto",
                "testo": "🪞 Ti rifletti in uno specchio... ma la tua immagine non si muove con te!",
                "sanita_loss": 15,
                "ricompensa": "👻 essenza spettrale"
            },
            {
                "nome": "sussurio_muri",
                "testo": "🧱 I muri sussurrano il tuo nome con voci di persone che ami...",
                "sanita_loss": 10,
                "ricompensa": "🕯️ candela maledetta"
            },
            {
                "nome": "ombre_viventi", 
                "testo": " Le tue ombre si staccano dal corpo e iniziano a camminare autonomamente!",
                "sanita_loss": 20,
                "ricompensa": "🔮 frammento d'ombra"
            },
            {
                "nome": "ritratti_maledetti",
                "testo": "🖼️ I ritratti sui muri ti seguono con gli occhi... e ora stanno sorridendo...",
                "sanita_loss": 12,
                "ricompensa": " tesoro nascosto"
            }
        ]
        
        evento = random.choice(eventi_horror)
        
        # Resistenza al terrore riduce la perdita di sanità
        sanita_ridotta = evento["sanita_loss"]
        resistenza = self.calcola_bonus_reliquie("resistenza_terrore")
        if resistenza > 0:
            sanita_ridotta = int(sanita_ridotta * (1 - resistenza/100))
            
        self.sanita_mentale = max(0, self.sanita_mentale - sanita_ridotta)
        
        # Aggiungi ricompensa
        self.inventario.append(evento["ricompensa"])
        monete_bonus = random.randint(20, 50)
        self.monete += monete_bonus
        
        testo = f"🏚️ {evento['testo']}\n"
        testo += f"😱 -{sanita_ridotta} Sanità Mentale\n"
        testo += f"✨ Trovi: {evento['ricompensa']}\n"
        testo += f" +{monete_bonus} monete"
        
        # Chance di trovare reliquia horror
        if random.randint(1, 100) <= 10:
            reliquia_horror = random.choice(["🏚️ Amuleto Anti-Paura", "👻 Cattura Fantasmi"])
            self.ottieni_reliquia(reliquia_horror)
            
        # Effetti della bassa sanità
        if self.sanita_mentale <= 20:
            testo += f"\n🤯 La tua mente vacilla... vedi cose che non ci sono!"
            # Penalità combattimento per bassa sanità
            self.attacco_base = max(5, self.attacco_base - 2)
            
        self.aggiorna_storia(testo)
        self.aggiorna_stats_incrementali()
        
    def caccia_fantasmi(self, e):
        """Caccia attiva ai fantasmi per guadagni maggiori ma più rischiosi"""
        if not self.gioco_iniziato or self.area_attuale != "🏚️ Casa degli Orrori":
            return
            
        if self.risorse["energia"] < 30:
            self.aggiorna_storia(" La caccia ai fantasmi richiede molta energia!")
            return
            
        if self.sanita_mentale <= 30:
            self.aggiorna_storia("🤯 La tua mente è troppo instabile per cacciare fantasmi!")
            return
            
        self.risorse["energia"] -= 30
        
        # Combattimento fantasmi
        fantasma_hp = random.randint(25, 45)
        attacco_giocatore = self.calcola_attacco_totale()
        
        # Cattura Fantasmi può intrappolare
        if self.ha_reliquia_attivabile("intrappola_spiriti"):
            if random.randint(1, 100) <= 60:  # 60% successo cattura
                self.usa_reliquia_attivabile("intrappola_spiriti")
                testo = f"👻 Catturi il fantasma nella reliquia!\n"
                testo += f"🎆 CATTURA PERFETTA!"
                ricompensa_boost = 2
            else:
                testo = f"👻 Il fantasma resiste alla cattura! Combattimento normale.\n"
                ricompensa_boost = 1
        else:
            testo = f"👻 Affronti il fantasma in combattimento diretto!\n"
            ricompensa_boost = 1
            
        if attacco_giocatore >= fantasma_hp:
            # Vittoria
            exp_guadagnata = random.randint(40, 70) * ricompensa_boost
            monete_guadagnate = random.randint(60, 100) * ricompensa_boost
            sanita_recuperata = random.randint(5, 15)  # Sconfiggere fantasmi aiuta la sanità
            
            self.esperienza += exp_guadagnata
            self.monete += monete_guadagnate
            self.sanita_mentale = min(100, self.sanita_mentale + sanita_recuperata)
            
            testo += f"✨ Fantasma sconfitto!\n"
            testo += f" +{exp_guadagnata} EXP\n"
            testo += f" +{monete_guadagnate} monete\n"
            testo += f"🧠 +{sanita_recuperata} Sanità Mentale (vittoria su paura)"
            
            # Bonus affinità se gatto attivo
            if self.gatto_attivo:
                self.modifica_affinita(self.gatto_attivo, 3, "la coraggiosa caccia ai fantasmi")
                
            # Controlla livello dopo esperienza guadagnata
            testo_livello = self.gestisci_livello()
            if testo_livello:
                testo += f"\n{testo_livello}"
            
            # Controlla sblocco gatti
            self.controlla_sblocco_gatti()
        else:
            # Sconfitta - perdita sanità e HP
            danno_subito = random.randint(15, 25)
            sanita_persa = random.randint(20, 30)
            
            self.hp_giocatore = max(1, self.hp_giocatore - danno_subito)
            self.sanita_mentale = max(0, self.sanita_mentale - sanita_persa)
            
            testo += f"👻 Il fantasma ti sopraffà!\n"
            testo += f"💔 -{danno_subito} HP\n"
            testo += f"😱 -{sanita_persa} Sanità Mentale"
            
        self.aggiorna_storia(testo)
        self.aggiorna_stats_incrementali()
        
    def medita_sanita(self, e):
        """Medita per recuperare sanità mentale"""
        if not self.gioco_iniziato:
            return
            
        if self.sanita_mentale >= 100:
            self.aggiorna_storia("🧠 La tua mente è già perfettamente stabile!")
            return
            
        # La meditazione costa tempo ma non energia
        sanita_recuperata = random.randint(15, 30)
        
        # Bonus se gatto attivo con alta affinità (supporto emotivo)
        if self.gatto_attivo and self.gatti[self.gatto_attivo]["affinita"] >= 100:
            sanita_recuperata += 10
            supporto_msg = f"\n😸 {self.gatti[self.gatto_attivo]['nome']} ti fa compagnia durante la meditazione!"
        else:
            supporto_msg = ""
            
        self.sanita_mentale = min(100, self.sanita_mentale + sanita_recuperata)
        
        testo = f"🧘 Mediti per calmare la mente...\n"
        testo += f"🧠 +{sanita_recuperata} Sanità Mentale{supporto_msg}"
        
        self.aggiorna_storia(testo)
        self.aggiorna_stats_incrementali()
        
    def test_audio_debug(self, e):
        """Funzione di debug per testare audio"""
        print("=== DIAGNOSI AUDIO ===")
        print(f"Directory corrente: {os.getcwd()}")
        print(f"Audio abilitato: {self.audio_abilitato}")
        print(f"Area attuale: {self.area_attuale}")
        print(f"Volume musica: {self.volume_musica}")
        print(f"Volume effetti: {self.volume_effetti}")
        
        # Test volume di sistema (Windows)
        try:
            import platform
            if platform.system() == "Windows":
                print("🔊 Sistema: Windows - controlla mixer audio")
        except:
            pass
        
        if self.area_attuale in self.musiche_aree:
            file_musica = self.musiche_aree[self.area_attuale]
            print(f"File musica per area: {file_musica}")
            
            # Test percorsi
            percorso_relativo = file_musica
            percorso_assoluto = os.path.abspath(file_musica)
            
            print(f"Percorso relativo: {percorso_relativo}")
            print(f"Esiste relativo: {os.path.exists(percorso_relativo)}")
            print(f"Percorso assoluto: {percorso_assoluto}")
            print(f"Esiste assoluto: {os.path.exists(percorso_assoluto)}")
            
            # Controlla dimensione file
            if os.path.exists(percorso_assoluto):
                size = os.path.getsize(percorso_assoluto)
                print(f"📏 Dimensione file: {size} bytes")
                if size == 0:
                    print("❌ File vuoto!")
            
            # Lista files nella directory
            try:
                music_dir = "assets/music"
                if os.path.exists(music_dir):
                    files = os.listdir(music_dir)
                    print(f"File nella cartella music: {files}")
                else:
                    print(f"❌ Cartella {music_dir} non esiste!")
            except Exception as e:
                print(f"Errore listing directory: {e}")
                
            # Test manuale caricamento con controllo stato
            try:
                print("🎵 Test caricamento manuale...")
                if hasattr(self, 'musica_sottofondo') and self.musica_sottofondo:
                    print(f"🎵 Oggetto audio esistente: {self.musica_sottofondo}")
                    try:
                        self.musica_sottofondo.play()
                        print("🎵 Forzata riproduzione audio esistente")
                    except Exception as play_error:
                        print(f"❌ Errore play esistente: {play_error}")
                        
                self.cambia_musica_area(self.area_attuale)
            except Exception as e:
                print(f"❌ Errore test: {e}")
        else:
            print(f"❌ Area {self.area_attuale} non ha musica associata")
            
        self.aggiorna_storia("Diagnosi audio completata - controlla console")

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
            self.inventario = stato_gioco.get("inventario", {})
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
                # Aggiorna volume di tutti i canali effetti
                if hasattr(self, 'effetto_gatto'):
                    self.effetto_gatto.volume = self.volume_effetti
                    self.effetto_vittoria.volume = self.volume_effetti
                    self.effetto_sconfitta.volume = self.volume_effetti
                    self.effetto_livello.volume = self.volume_effetti
                    self.effetto_raccolta.volume = self.volume_effetti
                    self.effetto_gatto_raccolta.volume = self.volume_effetti
                    self.effetto_monete.volume = self.volume_effetti
            
            # Carica dati gatti (era mancante!)
            if "gatti" in stato_gioco:
                self.gatti = stato_gioco["gatti"]
            if "gatto_attivo" in stato_gioco:
                self.gatto_attivo = stato_gioco["gatto_attivo"]
            
            # Carica risorse (era mancante!)
            if "risorse" in stato_gioco:
                self.risorse = stato_gioco["risorse"]
            
            # Carica altri dati importanti
            if "aree_sbloccate" in stato_gioco:
                self.aree_sbloccate = stato_gioco["aree_sbloccate"]
            if "area_attuale" in stato_gioco:
                self.area_attuale = stato_gioco["area_attuale"]
            if "progressione_area" in stato_gioco:
                self.progressione_area = stato_gioco["progressione_area"]
            if "pesce_raccolto" in stato_gioco:
                self.pesce_raccolto = stato_gioco["pesce_raccolto"]
            
            self.gioco_iniziato = True
            
            # Naviga al gioco mantenendo la possibilità di tornare al menu
            self.page.go("/gioco")
            
            if self.audio_abilitato:
                self.cambia_musica_area(self.area_attuale)
            
            self.haptic_feedback("success")
            self.aggiorna_storia("📂 Avventura caricata con successo!")
            self.descrivi_situazione_attuale()
            
            # Vai alla vista gioco dopo il caricamento
            self.page.go("/gioco")
            
        except Exception as ex:
            self.aggiorna_storia(f"❌ Errore caricamento: {str(ex)}")

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.window_width = 1000
    page.window_height = 800
    page.window_resizable = True
    
    # Inizializza l'avventura epica
    gioco = AvventuraEpica(page)

    def calcola_livello_minimo_boss(self, area):
        """Calcola il livello minimo richiesto per ogni boss (4, 8, 12, 16...)"""
        # Mappa ogni area al suo livello minimo
        indice_area = self.aree_ordinate.index(area) if area in self.aree_ordinate else 0
        return (indice_area + 1) * 4  # 4, 8, 12, 16, 20, etc.
    
    def inizia_combattimento_boss(self, boss_info):
        """Inizia un vero combattimento a turni contro il boss"""
        self.in_combattimento = True
        
        # Calcola livello minimo e se il boss deve essere potenziato
        livello_minimo = self.calcola_livello_minimo_boss(self.area_attuale)
        boss_potenziato = self.livello < livello_minimo
        
        # Se il giocatore è sotto-livello, il boss diventa molto più forte
        hp_boss = boss_info["hp"]
        attacco_boss = boss_info["attacco"]
        
        if boss_potenziato:
            # Boss diventa 3x più forte in HP e attacco
            hp_boss = int(hp_boss * 3)
            attacco_boss = int(attacco_boss * 3)
        
        self.mostro_attuale = {
            "nome": boss_info["nome"],
            "hp": hp_boss,
            "attacco": attacco_boss,
            "exp": boss_info["exp"],
            "tipo": "boss",
            "boss_potenziato": boss_potenziato
        }
        self.hp_mostro_attuale = hp_boss
        self.round_combattimento = 0
        
        # Messaggio iniziale
        nome_boss = boss_info["nome"]
        if boss_potenziato:
            self.aggiorna_storia(f" BOSS FIGHT!\n{nome_boss} appare davanti a te!\n⚠️ Il boss è molto più forte del previsto! (Livello richiesto: {livello_minimo})\nHP Boss: {self.hp_mostro_attuale}")
        else:
            self.aggiorna_storia(f" BOSS FIGHT!\n{nome_boss} appare davanti a te!\nHP Boss: {self.hp_mostro_attuale}")
        
        # Controlla se la vita è già bassa all'inizio del combattimento boss
        self.controlla_vita_bassa()
        
        # Aggiorna i pulsanti per mostrare le azioni di combattimento
        self.page.go("/combattimento")

    # Aggiungi il metodo alla classe
    AvventuraEpica.calcola_livello_minimo_boss = calcola_livello_minimo_boss
    AvventuraEpica.inizia_combattimento_boss = inizia_combattimento_boss

if __name__ == "__main__":
    ft.app(target=main)
 