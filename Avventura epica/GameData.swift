//
//  GameData.swift
//  Avventura epica
//
//  Created by Ambrogio Riili on 27/07/25.
//

import Foundation

extension GameManager {
    
    // MARK: - Monster Database
    func getMonsterDatabase() -> [String: [Monster]] {
        return [
            "Villaggio": [
                Monster(nome: "Ratto Selvatico", emoji: "🐀", hp: 20, attacco: 3, area: "Villaggio"),
                Monster(nome: "Corvo Aggressivo", emoji: "🐦‍⬛", hp: 15, attacco: 4, area: "Villaggio")
            ],
            
            "🏠 Cantina": [
                Monster(nome: "Ragno Gigante", emoji: "🕷️", hp: 35, attacco: 5, area: "🏠 Cantina", 
                        chiave: "🗝️ Chiave della Cantina", abilitaSpeciale: "morso_feroce"),
                Monster(nome: "Pipistrello Vampiro", emoji: "🦇", hp: 25, attacco: 6, area: "🏠 Cantina")
            ],
            
            "🚰 Fogne": [
                Monster(nome: "Alligatore Mutante", emoji: "🐊", hp: 50, attacco: 8, area: "🚰 Fogne"),
                Monster(nome: "Ragno Velenoso", emoji: "🕸️", hp: 30, attacco: 7, area: "🚰 Fogne",
                        abilitaSpeciale: "ragnatela_velenosa")
            ],
            
            "🌀 Labirinto Antico": [
                Monster(nome: "Guardiano di Pietra", emoji: "🗿", hp: 80, attacco: 12, area: "🌀 Labirinto Antico"),
                Monster(nome: "Spirito del Labirinto", emoji: "👻", hp: 45, attacco: 10, area: "🌀 Labirinto Antico")
            ],
            
            "❄️ Area Innevata": [
                Monster(nome: "Orso Polare", emoji: "🐻‍❄️", hp: 90, attacco: 15, area: "❄️ Area Innevata"),
                Monster(nome: "Lupo Artico", emoji: "🐺", hp: 60, attacco: 12, area: "❄️ Area Innevata",
                        chiave: "🧊 Chiave del Ghiaccio", abilitaSpeciale: "teletrasporto")
            ],
            
            "🌿 Giungla Selvaggia": [
                Monster(nome: "Anaconda Gigante", emoji: "🐍", hp: 70, attacco: 14, area: "🌿 Giungla Selvaggia"),
                Monster(nome: "Giaguaro Mistico", emoji: "🐆", hp: 85, attacco: 16, area: "🌿 Giungla Selvaggia",
                        chiave: "🌿 Chiave della Giungla", abilitaSpeciale: "bufera")
            ],
            
            "🌲 Bosco Profondo": [
                Monster(nome: "Ent Antico", emoji: "🌳", hp: 120, attacco: 18, area: "🌲 Bosco Profondo"),
                Monster(nome: "Lupo Mannaro", emoji: "🐺", hp: 95, attacco: 20, area: "🌲 Bosco Profondo",
                        chiave: "🌲 Chiave della Natura", abilitaSpeciale: "ruggito_primitivo")
            ],
            
            "⚰️ Cimitero": [
                Monster(nome: "Scheletro Guerriero", emoji: "💀", hp: 80, attacco: 16, area: "⚰️ Cimitero"),
                Monster(nome: "Zombie Antico", emoji: "🧟", hp: 100, attacco: 14, area: "⚰️ Cimitero")
            ],
            
            "🏚️ Casa degli Orrori": [
                Monster(nome: "Fantasma Maledetto", emoji: "👻", hp: 110, attacco: 22, area: "🏚️ Casa degli Orrori"),
                Monster(nome: "Demone dell'Orrore", emoji: "👹", hp: 130, attacco: 25, area: "🏚️ Casa degli Orrori",
                        chiave: "🏚️ Chiave dell'Orrore", abilitaSpeciale: "maledizione")
            ],
            
            "🏭 Fabbrica Abbandonata": [
                Monster(nome: "Robot Impazzito", emoji: "🤖", hp: 140, attacco: 24, area: "🏭 Fabbrica Abbandonata"),
                Monster(nome: "Cyborg Corrotto", emoji: "🦾", hp: 120, attacco: 28, area: "🏭 Fabbrica Abbandonata",
                        chiave: "🏭 Chiave della Fabbrica", abilitaSpeciale: "terrore_paralizzante")
            ],
            
            "⛏️ Miniera Profonda": [
                Monster(nome: "Golem di Ferro", emoji: "⚒️", hp: 160, attacco: 26, area: "⛏️ Miniera Profonda"),
                Monster(nome: "Drago delle Miniere", emoji: "🐲", hp: 180, attacco: 30, area: "⛏️ Miniera Profonda",
                        chiave: "⛏️ Chiave della Miniera", abilitaSpeciale: "autocorrezione")
            ],
            
            "🌙 Cripta Maledetta": [
                Monster(nome: "Lich Supremo", emoji: "🧙‍♂️", hp: 200, attacco: 32, area: "🌙 Cripta Maledetta"),
                Monster(nome: "Drago di Cristallo", emoji: "💎", hp: 220, attacco: 35, area: "🌙 Cripta Maledetta",
                        chiave: "🌙 Chiave della Cripta", abilitaSpeciale: "soffio_cristallino")
            ],
            
            "🌊 Mare": [
                Monster(nome: "Kraken Leggendario", emoji: "🐙", hp: 250, attacco: 38, area: "🌊 Mare"),
                Monster(nome: "Leviatano Antico", emoji: "🐋", hp: 280, attacco: 40, area: "🌊 Mare",
                        chiave: "🌊 Chiave del Mare", abilitaSpeciale: "non_morto")
            ],
            
            "🏔️ Montagna Sacra": [
                Monster(nome: "Drago di Montagna", emoji: "🐉", hp: 300, attacco: 42, area: "🏔️ Montagna Sacra"),
                Monster(nome: "Angelo Caduto", emoji: "😇", hp: 320, attacco: 45, area: "🏔️ Montagna Sacra",
                        chiave: "🏔️ Chiave della Montagna", abilitaSpeciale: "tsunami")
            ],
            
            "🌋 Vulcano Attivo": [
                Monster(nome: "Fenice Immortale", emoji: "🔥", hp: 350, attacco: 48, area: "🌋 Vulcano Attivo"),
                Monster(nome: "Drago di Lava", emoji: "🌋", hp: 380, attacco: 50, area: "🌋 Vulcano Attivo",
                        chiave: "🌋 Chiave del Vulcano", abilitaSpeciale: "luce_divina")
            ],
            
            "👑 Palazzo Finale": [
                Monster(nome: "Re dei Demoni", emoji: "👑", hp: 450, attacco: 55, area: "👑 Palazzo Finale"),
                Monster(nome: "Boss Finale", emoji: "💀", hp: 500, attacco: 60, area: "👑 Palazzo Finale",
                        chiave: "👑 Chiave Finale", abilitaSpeciale: "eruzione"),
                Monster(nome: "Ombra Suprema", emoji: "🌚", hp: 400, attacco: 52, area: "👑 Palazzo Finale",
                        abilitaSpeciale: "dominazione"),
                Monster(nome: "Entità Cosmica", emoji: "🌌", hp: 600, attacco: 70, area: "👑 Palazzo Finale",
                        abilitaSpeciale: "metamorfosi", richiedeNox: true)
            ]
        ]
    }
    
    // MARK: - Cat Evolution Database
    func getCatEvolutionDatabase() -> [String: CatEvolution] {
        return [
            "gatto_1": CatEvolution(
                nomeEvoluto: "⭐ Micio Stellare",
                abilitaEvoluta: "raccolta_suprema",
                bonusPassivo: "schivata_5",
                storia: "Micio rivela di essere un antico guardiano delle stelle, caduto sulla Terra per proteggere i tesori perduti.",
                dialoghi: [
                    "💭 Sento l'energia delle stelle antiche...",
                    "💭 Insieme possiamo trovare tesori nascosti!",
                    "💭 Le costellazioni mi guidano verso i segreti."
                ]
            ),
            
            "gatto_2": CatEvolution(
                nomeEvoluto: "⚡ Shadow Tempesta",
                abilitaEvoluta: "combattimento_fulmineo",
                bonusPassivo: "critico_15",
                storia: "Shadow era un guerriero leggendario in una vita passata, ora risveglia la sua vera natura combattiva.",
                dialoghi: [
                    "💭 La battaglia scorre nelle mie vene!",
                    "💭 Nessun nemico può resistere alla tempesta!",
                    "💭 I miei artigli portano il tuono!"
                ]
            ),
            
            "gatto_3": CatEvolution(
                nomeEvoluto: "🌙 Luna Celestiale",
                abilitaEvoluta: "guarigione_celestiale",
                bonusPassivo: "luce_nelle_tenebre",
                storia: "Luna ha curato innumerevoli creature perdute. Il suo sogno è creare un santuario di pace per tutti gli esseri feriti.",
                dialoghi: [
                    "💭 La luna mi dona la forza di guarire...",
                    "💭 Ogni creatura merita compassione e cure.",
                    "💭 Insieme porteremo pace in questo mondo."
                ]
            ),
            
            "gatto_4": CatEvolution(
                nomeEvoluto: "💫 Stella Cosmica",
                abilitaEvoluta: "partnership_galattica",
                bonusPassivo: "sincronia_perfetta",
                storia: "Stella è un essere cosmico che viaggia tra le dimensioni, legandosi ai compagni più coraggiosi.",
                dialoghi: [
                    "💭 Il nostro legame trascende lo spazio-tempo!",
                    "💭 Insieme possiamo superare ogni ostacolo.",
                    "💭 La partnership perfetta è la nostra forza!"
                ]
            ),
            
            "gatto_5": CatEvolution(
                nomeEvoluto: "🌌 Nox Eterno",
                abilitaEvoluta: "controllo_temporale",
                bonusPassivo: "manipolazione_destino",
                storia: "Nox è il custode del tempo stesso, capace di vedere tutti i possibili futuri e scegliere il migliore.",
                dialoghi: [
                    "💭 Ho visto infinite linee temporali...",
                    "💭 Il passato e il futuro si intrecciano.",
                    "💭 Insieme riscriveremo il destino!"
                ]
            )
        ]
    }
    
    // MARK: - Relic Database
    func getRelicDatabase() -> [String: Relic] {
        return [
            "Braciere di Fuoco Antico": Relic(
                nome: "🔥 Braciere di Fuoco Antico",
                tipo: .passivo,
                effetto: "undead_damage",
                valore: 10,
                descrizione: "+10 attacco contro boss non morti",
                rarita: .epico,
                origine: "boss_speciale"
            ),
            
            "Specchio Lunare": Relic(
                nome: "🌕 Specchio Lunare",
                tipo: .attivabile,
                effetto: "rifletti_attacco",
                valore: 1,
                descrizione: "Una volta per battaglia: riflette un attacco al mittente",
                rarita: .leggendario,
                origine: "mini_dungeon"
            ),
            
            "Gemma della Foresta": Relic(
                nome: "🌿 Gemma della Foresta",
                tipo: .passivo,
                effetto: "regen_gatti",
                valore: 2,
                descrizione: "I gatti guariscono 2 HP ogni turno",
                rarita: .raro,
                origine: "npc_raro"
            ),
            
            "Artiglio Dorato": Relic(
                nome: "⭐ Artiglio Dorato",
                tipo: .passivo,
                effetto: "critico_gatti",
                valore: 15,
                descrizione: "+15% critico per i gatti da combattimento",
                rarita: .epico,
                origine: "boss_speciale"
            ),
            
            "Candela delle Anime": Relic(
                nome: "🕯️ Candela delle Anime",
                tipo: .passivo,
                effetto: "resistenza_orrore",
                valore: 25,
                descrizione: "+25% resistenza agli effetti di orrore",
                rarita: .raro,
                origine: "casa_orrori"
            ),
            
            "Cristallo del Tempo": Relic(
                nome: "⏰ Cristallo del Tempo",
                tipo: .attivabile,
                effetto: "riavvolgi_turno",
                valore: 3,
                descrizione: "3 usi: riavvolge l'ultimo turno di combattimento",
                rarita: .leggendario,
                origine: "palazzo_finale"
            ),
            
            "Amuleto del Mare": Relic(
                nome: "🌊 Amuleto del Mare",
                tipo: .passivo,
                effetto: "rigenerazione_acqua",
                valore: 5,
                descrizione: "Regenera 5 HP per turno quando vicino all'acqua",
                rarita: .raro,
                origine: "mare"
            ),
            
            "Corona del Re": Relic(
                nome: "👑 Corona del Re",
                tipo: .passivo,
                effetto: "leadership",
                valore: 20,
                descrizione: "+20% statistiche per tutti i gatti",
                rarita: .leggendario,
                origine: "palazzo_finale"
            )
        ]
    }
    
    // MARK: - Special Items Database
    func getSpecialItemsDatabase() -> [String: [String]] {
        return [
            "Villaggio": [
                "🍖 Carne Fresca",
                "🥛 Latte Caldo",
                "🧶 Gomitolo di Lana"
            ],
            
            "🏠 Cantina": [
                "🕯️ Candela Antica",
                "🍷 Vino Pregiato",
                "📜 Mappa Segreta"
            ],
            
            "🚰 Fogne": [
                "💎 Gemma Nascosta",
                "🔧 Chiave Inglese",
                "🧪 Pozione Misteriosa"
            ],
            
            "❄️ Area Innevata": [
                "❄️ Cristallo di Ghiaccio",
                "🧣 Sciarpa Calda",
                "⛷️ Sci Magici"
            ],
            
            "🌿 Giungla Selvaggia": [
                "🌺 Fiore Raro",
                "🍯 Miele Dorato",
                "🦋 Farfalla Magica"
            ],
            
            "🌲 Bosco Profondo": [
                "🍄 Fungo Luminoso",
                "🌰 Ghianda Magica",
                "🦌 Corno di Cervo"
            ],
            
            "🏚️ Casa degli Orrori": [
                "👻 Essenza Spettrale",
                "🔮 Sfera del Terrore",
                "📖 Libro Maledetto"
            ],
            
            "🌊 Mare": [
                "🐚 Conchiglia Magica",
                "🦈 Dente di Squalo",
                "⚓ Ancora Antica"
            ],
            
            "👑 Palazzo Finale": [
                "💠 Gemma del Potere",
                "⚔️ Spada Leggendaria",
                "🛡️ Scudo Divino"
            ]
        ]
    }
    
    // MARK: - Area Music Database
    func getAreaMusicDatabase() -> [String: String] {
        return [
            "Villaggio": "villaggio_peaceful",
            "🏠 Cantina": "underground_mysterious",
            "🚰 Fogne": "sewer_ambient",
            "🌀 Labirinto Antico": "labyrinth_puzzle",
            "❄️ Area Innevata": "snow_wind",
            "🌿 Giungla Selvaggia": "jungle_wild",
            "🌲 Bosco Profondo": "forest_deep",
            "⚰️ Cimitero": "cemetery_spooky",
            "🏚️ Casa degli Orrori": "horror_tension",
            "🏭 Fabbrica Abbandonata": "factory_industrial",
            "⛏️ Miniera Profonda": "mine_echo",
            "🌙 Cripta Maledetta": "crypt_dark",
            "🌊 Mare": "ocean_waves",
            "🏔️ Montagna Sacra": "mountain_epic",
            "🌋 Vulcano Attivo": "volcano_intense",
            "👑 Palazzo Finale": "final_boss_epic"
        ]
    }
    
    // MARK: - Random Event Database
    func getRandomEventsDatabase() -> [String: [String]] {
        return [
            "positive": [
                "🍀 Hai trovato un quadrifoglio! +10 Fortuna per il prossimo combattimento",
                "💰 Un mercante generoso ti ha dato risorse gratuite!",
                "🌟 Le stelle si allineano favorevolmente! +20 Esperienza",
                "🎁 Hai trovato un tesoro nascosto!",
                "🦋 Una farfalla magica ti benedice! I tuoi gatti recuperano energia",
                "🌈 Un arcobaleno appare! Tutti i gatti guadagnano affinità"
            ],
            
            "neutral": [
                "🌤️ Una brezza leggera rinfresca l'aria",
                "🦅 Un'aquila vola sopra di te osservando il territorio",
                "🍃 Le foglie danzano nel vento",
                "💫 Una stella cadente attraversa il cielo",
                "🦆 Un gruppo di anatre attraversa il sentiero",
                "🌸 I fiori profumano l'aria intorno a te"
            ],
            
            "negative": [
                "⛈️ Un temporale improvviso! Perdi energia",
                "🕳️ Cadi in una buca! Il tuo gatto si ferisce leggermente",
                "🦇 I pipistrelli ti disturbano! Perdi concentrazione",
                "🌫️ Una nebbia fitta rallenta i tuoi progressi",
                "🐀 I ratti hanno rubato del cibo!",
                "🌪️ Un vento forte ti fa perdere alcune risorse"
            ],
            
            "combat": [
                "⚔️ Nemici in agguato! Preparati al combattimento",
                "👹 Un boss appare improvvisamente!",
                "🐺 Un branco di lupi ti circonda!",
                "🕷️ Ragni giganti emergono dalle tenebre",
                "👻 Fantasmi si materializzano dal nulla",
                "🦖 Una creatura antica si risveglia!"
            ]
        ]
    }
}