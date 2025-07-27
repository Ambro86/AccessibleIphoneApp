//
//  GameModels.swift
//  Avventura epica
//
//  Created by Ambrogio Riili on 27/07/25.
//

import Foundation

// MARK: - Enums
enum GameScreen {
    case mainMenu
    case game
    case cats
    case areas
    case settings
    case inventory
    case shop
    case info
}

enum CatAbility: String, CaseIterable {
    case raccolta = "raccolta"
    case combattimento = "combattimento"
    case guarigione = "guarigione"
    case partner = "partner"
    case riavvolgi = "riavvolgi"
    
    var description: String {
        switch self {
        case .raccolta: return "Raccolta"
        case .combattimento: return "Combattimento"
        case .guarigione: return "Guarigione"
        case .partner: return "Partner"
        case .riavvolgi: return "Riavvolgi"
        }
    }
}

enum RelicType: String {
    case passivo = "passivo"
    case attivabile = "attivabile"
}

enum RelicRarity: String {
    case comune = "comune"
    case raro = "raro"
    case epico = "epico"
    case leggendario = "leggendario"
}

// MARK: - Cat Model
struct Cat: Identifiable, Codable {
    let id: String
    var nome: String
    var emoji: String
    var livello: Int
    var attacco: Int
    var abilita: CatAbility
    var fame: Int
    var felicita: Int
    var sbloccato: Bool
    var affinita: Int
    var nomePersonalizzato: Bool
    var areeNonUsato: Int
    var formaEvoluta: Bool
    var dialoghiSbloccati: [String]
    var sceneViste: [String]
    
    init(id: String, nome: String, emoji: String, livello: Int = 1, attacco: Int = 5, 
         abilita: CatAbility, fame: Int = 100, felicita: Int = 100, sbloccato: Bool = false) {
        self.id = id
        self.nome = nome
        self.emoji = emoji
        self.livello = livello
        self.attacco = attacco
        self.abilita = abilita
        self.fame = fame
        self.felicita = felicita
        self.sbloccato = sbloccato
        self.affinita = sbloccato ? 30 : 0
        self.nomePersonalizzato = false
        self.areeNonUsato = 0
        self.formaEvoluta = false
        self.dialoghiSbloccati = []
        self.sceneViste = []
    }
}

// MARK: - Cat Evolution Model
struct CatEvolution: Codable {
    let nomeEvoluto: String
    let abilitaEvoluta: String
    let bonusPassivo: String
    let storia: String
    let dialoghi: [String]
}

// MARK: - Resources Model
struct Resources: Codable {
    var cibo: Int = 50
    var acqua: Int = 50
    var legno: Int = 0
    var pietra: Int = 0
    var ferro: Int = 0
    var energia: Int = 100
    var pozioni: Int = 100
}

// MARK: - Monster Model
struct Monster: Codable {
    let nome: String
    let emoji: String
    var hp: Int
    var attacco: Int
    let area: String
    let chiave: String?
    let abilitaSpeciale: String?
    let richiedeNox: Bool
    let audioFile: String?
    
    init(nome: String, emoji: String, hp: Int, attacco: Int, area: String, 
         chiave: String? = nil, abilitaSpeciale: String? = nil, richiedeNox: Bool = false, audioFile: String? = nil) {
        self.nome = nome
        self.emoji = emoji
        self.hp = hp
        self.attacco = attacco
        self.area = area
        self.chiave = chiave
        self.abilitaSpeciale = abilitaSpeciale
        self.richiedeNox = richiedeNox
        self.audioFile = audioFile
    }
}

// MARK: - Relic Model
struct Relic: Identifiable, Codable {
    let id = UUID()
    let nome: String
    let tipo: RelicType
    let effetto: String
    let valore: Int
    let descrizione: String
    let rarita: RelicRarity
    let origine: String
    
    init(nome: String, tipo: RelicType, effetto: String, valore: Int, 
         descrizione: String, rarita: RelicRarity, origine: String) {
        self.nome = nome
        self.tipo = tipo
        self.effetto = effetto
        self.valore = valore
        self.descrizione = descrizione
        self.rarita = rarita
        self.origine = origine
    }
}

// MARK: - Game State Model
struct GameState: Codable {
    var versione: String = "1.0.0"
    var autore: String = "Ambrogio Riili"
    
    // Areas and progression
    var areeOrdinate: [String] = [
        "Villaggio", "🏠 Cantina", "🚰 Fogne", "🌀 Labirinto Antico",
        "❄️ Area Innevata", "🌿 Giungla Selvaggia", "🌲 Bosco Profondo", "⚰️ Cimitero",
        "🏚️ Casa degli Orrori", "🏭 Fabbrica Abbandonata", "⛏️ Miniera Profonda",
        "🌙 Cripta Maledetta", "🌊 Mare", "🏔️ Montagna Sacra", "🌋 Vulcano Attivo", "👑 Palazzo Finale"
    ]
    var areeSbloccate: [String] = ["Villaggio"]
    var areaAttuale: String = "Villaggio"
    var progressioneArea: [String: Int] = [:]
    
    // Inventory and equipment system
    var inventario: PlayerInventory = PlayerInventory()
    var modalitaMenu: String = "principale" // principale, gioco, inventario, negozio, statistiche
    
    // Screen navigation
    var schermataCorrente: GameScreen = .mainMenu
    var stackSchermate: [GameScreen] = []
    
    // Combat system
    var inCombattimento: Bool = false
    var combattimentoAutomatico: Bool = false
    var mostroAttuale: Monster?
    var hpMostroAttuale: Int = 0
    var roundCombattimento: Int = 0
    
    // Cats
    var gatti: [String: Cat] = [:]
    var gattoAttivo: String = "gatto_1"
    
    // Resources and items
    var risorse: Resources = Resources()
    var chiaviRaccolte: [String] = []
    var bossSconfitti: [String] = []
    
    // Boss notification system
    var bossNotificationsMostrate: Set<String> = []
    var showingBossNotification: Bool = false
    var currentBossArea: String?
    
    // Special areas and features
    var areaSegreta: String = "🌌 Regno degli Incubi"
    var portaleSogniBlocatto: Bool = false
    var pesciMagiciRari: Int = 0
    var finaleAlternativoRaggiunto: Bool = false
    var pesceRaccolto: Int = 0
    var casaNelBoscoCostruita: Bool = false
    
    // Dream choices system
    var scelteOniriche: [String] = []
    var formaRegnoSogni: String = "neutrale"
    var riavvolgimentiDisponibili: Int = 0
    
    // Relics system
    var reliquiePossedute: [String] = []
    var reliqueEquipaggiate: [String: String?] = ["slot_1": nil, "slot_2": nil, "slot_3": nil]
    var reliqueScoperte: [String] = []
    var miniDungeonCompletati: [String] = []
    var npcRariIncontrati: [String] = []
    
    // Affinity system
    var affinitaMilestone: [Int: String] = [50: "💛", 100: "💚", 150: "💙", 200: "💜"]
    var ultimoGattoUsato: String?
    var turniInArea: Int = 0
    
    // Horror system
    var sanitaMentale: Int = 100
    var eventiOrroreVisti: [String] = []
    
    // Audio settings
    var audioAbilitato: Bool = true
    var hapticAbilitato: Bool = true
    var heartbeatAttivo: Bool = false
    
    // Player stats
    var livello: Int = 1
    var esperienza: Int = 0
    var esperienzaProssimoLivello: Int = 100
    
    // Map system
    var posizioneGiocatore: [Int] = [0, 0]
    var mappa: [[String]] = [[]]
    
    init() {
        setupInitialCats()
        setupProgressioneArea()
        setupMappa()
    }
    
    private mutating func setupInitialCats() {
        gatti = [
            "gatto_1": Cat(id: "gatto_1", nome: "Micio", emoji: "🐱", 
                          abilita: .raccolta, sbloccato: true),
            "gatto_2": Cat(id: "gatto_2", nome: "Shadow", emoji: "🐾", 
                          attacco: 8, abilita: .combattimento),
            "gatto_3": Cat(id: "gatto_3", nome: "Luna", emoji: "😻", 
                          attacco: 3, abilita: .guarigione),
            "gatto_4": Cat(id: "gatto_4", nome: "Stella", emoji: "⭐", 
                          attacco: 6, abilita: .partner),
            "gatto_5": Cat(id: "gatto_5", nome: "Nox", emoji: "🌌", 
                          attacco: 10, abilita: .riavvolgi)
        ]
    }
    
    private mutating func setupProgressioneArea() {
        progressioneArea = Dictionary(uniqueKeysWithValues: areeOrdinate.map { ($0, 0) })
    }
    
    private mutating func setupMappa() {
        mappa = [[areaAttuale]]
    }
}