//
//  ShopData.swift
//  Avventura epica
//
//  Created by Ambrogio Riili on 27/07/25.
//

import Foundation

extension GameManager {
    
    // MARK: - Area-Specific Shops
    func getAreaShop(_ area: String) -> [String: EquipmentItem] {
        let allEquipment = getEquipmentDatabase()
        var areaShop: [String: EquipmentItem] = [:]
        
        // Material Progression System - 17 tiers based on original game
        switch area {
        case "Villaggio":
            // Material 1 - Legno (Wood) - Basic equipment
            areaShop = [
                "Spada di Legno": allEquipment["Spada di Legno"]!,
                "Scudo di Legno": allEquipment["Scudo di Legno"]!,
                "Armatura di Cuoio": allEquipment["Armatura di Cuoio"]!,
                "Pozione Vita": EquipmentItem(nome: "Pozione Vita", tipo: .consumabile, prezzo: 60, descrizione: "Ripristina 15 HP")
            ]
            
        case "🏠 Cantina":
            // Material 2 - Pietra (Stone) - First upgrade
            areaShop = [
                "Spada di Pietra": allEquipment["Spada di Pietra"]!,
                "Scudo di Pietra": allEquipment["Scudo di Pietra"]!,
                "Anello Magico": allEquipment["Anello Magico"]!,
                "Sardina": EquipmentItem(nome: "Sardina", tipo: .consumabile, prezzo: 90, descrizione: "Ripristina 25 HP")
            ]
            
        case "🚰 Fogne":
            // Material 3 - Rame (Copper) - First metals
            areaShop = [
                "Spada di Rame": allEquipment["Spada di Rame"]!,
                "Scudo di Rame": allEquipment["Scudo di Rame"]!,
                "Armatura di Rame": allEquipment["Armatura di Rame"]!,
                "Pesce Dorato": EquipmentItem(nome: "Pesce Dorato", tipo: .consumabile, prezzo: 120, descrizione: "Ripristina 35 HP")
            ]
            
        case "🌀 Labirinto Antico":
            // Material 4 - Bronzo (Bronze) - Ancient weapons
            areaShop = [
                "Spada di Bronzo": allEquipment["Spada di Bronzo"]!,
                "Scudo di Bronzo": allEquipment["Scudo di Bronzo"]!,
                "Elmo di Bronzo": allEquipment["Elmo di Bronzo"]!,
                "Amuleto Antico": allEquipment["Amuleto Antico"]!
            ]
            
        case "❄️ Area Innevata":
            // Material 5 - Ferro (Iron) - Medieval equipment
            areaShop = [
                "Spada di Ferro": allEquipment["Spada di Ferro"]!,
                "Scudo di Ferro": allEquipment["Scudo di Ferro"]!,
                "Armatura di Ferro": allEquipment["Armatura di Ferro"]!,
                "Mantello Termico": EquipmentItem(nome: "Mantello Termico", tipo: .armatura, prezzo: 2200, descrizione: "Protezione dal freddo +5 DEF")
            ]
            
        case "🌿 Giungla Selvaggia":
            // Material 6 - Acciaio (Steel) - Knight weapons
            areaShop = [
                "Spada d'Acciaio": allEquipment["Spada d'Acciaio"]!,
                "Scudo d'Acciaio": allEquipment["Scudo d'Acciaio"]!,
                "Lancia della Giungla": EquipmentItem(nome: "Lancia della Giungla", tipo: .arma, prezzo: 2800, descrizione: "Arma della giungla +20 ATK"),
                "Antidoto Naturale": EquipmentItem(nome: "Antidoto Naturale", tipo: .consumabile, prezzo: 180, descrizione: "Cura veleni e +45 HP")
            ]
            
        case "🌲 Bosco Profondo":
            // Material 7 - Acciaio Temprato - Gladiator equipment
            areaShop = [
                "Spada Temprata": allEquipment["Spada Temprata"]!,
                "Scudo Temprato": allEquipment["Scudo Temprato"]!,
                "Armatura del Bosco": EquipmentItem(nome: "Armatura del Bosco", tipo: .armatura, prezzo: 3800, descrizione: "Protezione naturale +12 DEF"),
                "Elisir della Foresta": EquipmentItem(nome: "Elisir della Foresta", tipo: .consumabile, prezzo: 220, descrizione: "Ripristina 55 HP e +10 energia")
            ]
            
        case "⚰️ Cimitero":
            // Material 8 - Argento (Silver) - Effective against undead
            areaShop = [
                "Spada d'Argento": allEquipment["Spada d'Argento"]!,
                "Scudo Benedetto": allEquipment["Scudo Benedetto"]!,
                "Amuleto Sacro": allEquipment["Amuleto Sacro"]!,
                "Acqua Santa": EquipmentItem(nome: "Acqua Santa", tipo: .consumabile, prezzo: 300, descrizione: "Anti-non morti +65 HP")
            ]
            
        case "🏚️ Casa degli Orrori":
            // Material 9 - Oro (Gold) - Ceremonial equipment
            areaShop = [
                "Spada Dorata": allEquipment["Spada Dorata"]!,
                "Scudo Dorato": allEquipment["Scudo Dorato"]!,
                "Corona dell'Orrore": EquipmentItem(nome: "Corona dell'Orrore", tipo: .accessorio, prezzo: 5500, descrizione: "Resistenza mentale +15 DEF"),
                "Pozione del Coraggio": EquipmentItem(nome: "Pozione del Coraggio", tipo: .consumabile, prezzo: 350, descrizione: "Immunità paura +75 HP")
            ]
            
        case "🏭 Fabbrica Abbandonata":
            // Material 10 - Platino (Platinum) - Luxury technology
            areaShop = [
                "Lama al Platino": allEquipment["Lama al Platino"]!,
                "Scudo Tecno": allEquipment["Scudo Tecno"]!,
                "Tuta Industriale": EquipmentItem(nome: "Tuta Industriale", tipo: .armatura, prezzo: 7200, descrizione: "Protezione industriale +20 DEF"),
                "Stimolante Sintetico": EquipmentItem(nome: "Stimolante Sintetico", tipo: .consumabile, prezzo: 400, descrizione: "Boost energia +85 HP")
            ]
            
        case "⛏️ Miniera Profonda":
            // Material 11 - Titanio (Titanium) - Advanced technology
            areaShop = [
                "Piccone di Titanio": allEquipment["Piccone di Titanio"]!,
                "Scudo Rinforzato": allEquipment["Scudo Rinforzato"]!,
                "Casco da Minatore": EquipmentItem(nome: "Casco da Minatore", tipo: .accessorio, prezzo: 8800, descrizione: "Visione notturna +18 DEF"),
                "Minerale Energetico": EquipmentItem(nome: "Minerale Energetico", tipo: .consumabile, prezzo: 450, descrizione: "Energia pura +95 HP")
            ]
            
        case "🌙 Cripta Maledetta":
            // Material 12 - Ossidiana (Obsidian) - Volcanic equipment
            areaShop = [
                "Lama d'Ossidiana": allEquipment["Lama d'Ossidiana"]!,
                "Scudo Vulcanico": allEquipment["Scudo Vulcanico"]!,
                "Mantello dell'Ombra": EquipmentItem(nome: "Mantello dell'Ombra", tipo: .armatura, prezzo: 11000, descrizione: "Invisibilità parziale +25 DEF"),
                "Sangue di Drago": EquipmentItem(nome: "Sangue di Drago", tipo: .consumabile, prezzo: 550, descrizione: "Rigenerazione +120 HP")
            ]
            
        case "🌊 Mare":
            // Material 13 - Diamante (Diamond) - Supreme hardness
            areaShop = [
                "Tridente di Diamante": allEquipment["Tridente di Diamante"]!,
                "Scudo di Corallo": allEquipment["Scudo di Corallo"]!,
                "Armatura Marina": EquipmentItem(nome: "Armatura Marina", tipo: .armatura, prezzo: 13500, descrizione: "Resistenza acquatica +30 DEF"),
                "Perla Curativa": EquipmentItem(nome: "Perla Curativa", tipo: .consumabile, prezzo: 650, descrizione: "Cura magica +140 HP")
            ]
            
        case "🏔️ Montagna Sacra":
            // Material 14 - Mithril - Mythological metal
            areaShop = [
                "Spada di Mithril": allEquipment["Spada di Mithril"]!,
                "Scudo Sacro": allEquipment["Scudo Sacro"]!,
                "Vesti Celestiali": EquipmentItem(nome: "Vesti Celestiali", tipo: .armatura, prezzo: 16000, descrizione: "Benedizione divina +35 DEF"),
                "Nettare Divino": EquipmentItem(nome: "Nettare Divino", tipo: .consumabile, prezzo: 750, descrizione: "Cura divina +160 HP")
            ]
            
        case "🌋 Vulcano Attivo":
            // Material 15 - Cristallo Runico - Amplifies magic
            areaShop = [
                "Spada Runica": allEquipment["Spada Runica"]!,
                "Scudo di Magma": allEquipment["Scudo di Magma"]!,
                "Armatura Ignea": EquipmentItem(nome: "Armatura Ignea", tipo: .armatura, prezzo: 19000, descrizione: "Resistenza fuoco +40 DEF"),
                "Elisir Vulcanico": EquipmentItem(nome: "Elisir Vulcanico", tipo: .consumabile, prezzo: 850, descrizione: "Potere del fuoco +180 HP")
            ]
            
        case "👑 Palazzo Finale":
            // Material 16 - Essenza Divina - Celestial power
            areaShop = [
                "Spada Imperiale": allEquipment["Spada Imperiale"]!,
                "Scudo della Corona": allEquipment["Scudo della Corona"]!,
                "Corona Imperiale": EquipmentItem(nome: "Corona Imperiale", tipo: .accessorio, prezzo: 25000, descrizione: "Potere assoluto +50 DEF"),
                "Elisir Imperiale": EquipmentItem(nome: "Elisir Imperiale", tipo: .consumabile, prezzo: 1000, descrizione: "Cura suprema +200 HP")
            ]
            
        case "🌌 Regno degli Incubi":
            // Material 17 - Scaglie di Drago - FINAL TIER
            areaShop = [
                "Arma del Caos": EquipmentItem(nome: "Arma del Caos", tipo: .arma, prezzo: 50000, descrizione: "Potere del caos +100 ATK"),
                "Scudo dell'Incubo": EquipmentItem(nome: "Scudo dell'Incubo", tipo: .scudo, prezzo: 40000, descrizione: "Protezione onirica +60 DEF"),
                "Armatura del Vuoto": EquipmentItem(nome: "Armatura del Vuoto", tipo: .armatura, prezzo: 60000, descrizione: "Potere dell'oblio +70 DEF"),
                "Essenza Primordiale": EquipmentItem(nome: "Essenza Primordiale", tipo: .consumabile, prezzo: 2000, descrizione: "Cura assoluta +500 HP")
            ]
            
        default:
            // Fallback to basic village shop
            areaShop = [
                "Spada di Legno": allEquipment["Spada di Legno"]!,
                "Scudo di Legno": allEquipment["Scudo di Legno"]!,
                "Pozione Vita": EquipmentItem(nome: "Pozione Vita", tipo: .consumabile, prezzo: 50, descrizione: "Ripristina 30 HP")
            ]
        }
        
        return areaShop
    }
    
    func hasShop(_ area: String) -> Bool {
        // All areas except special/unknown ones have shops
        return gameState.areeOrdinate.contains(area)
    }
    
    // MARK: - Equipment Database
    func getEquipmentDatabase() -> [String: EquipmentItem] {
        return [
            // ARMI - Progression dal legno al drago
            "Spada di Legno": EquipmentItem(
                nome: "Spada di Legno",
                tipo: .arma,
                prezzo: 150,
                descrizione: "Arma basilare di legno",
                danno: 3
            ),
            "Spada di Pietra": EquipmentItem(
                nome: "Spada di Pietra", 
                tipo: .arma,
                prezzo: 400,
                descrizione: "Arma primitiva di pietra",
                danno: 5
            ),
            "Spada di Rame": EquipmentItem(
                nome: "Spada di Rame",
                tipo: .arma,
                prezzo: 800,
                descrizione: "Primo metallo per armi",
                danno: 8
            ),
            "Spada di Bronzo": EquipmentItem(
                nome: "Spada di Bronzo",
                tipo: .arma,
                prezzo: 1200,
                descrizione: "Arma degli antichi",
                danno: 12
            ),
            "Spada di Ferro": EquipmentItem(
                nome: "Spada di Ferro",
                tipo: .arma,
                prezzo: 1800,
                descrizione: "Arma medievale classica",
                danno: 15
            ),
            "Spada di Acciaio": EquipmentItem(
                nome: "Spada di Acciaio",
                tipo: .arma,
                prezzo: 2500,
                descrizione: "Arma dei cavalieri",
                danno: 20
            ),
            "Spada di Acciaio Temprato": EquipmentItem(
                nome: "Spada di Acciaio Temprato",
                tipo: .arma,
                prezzo: 3500,
                descrizione: "Arma da gladiatore",
                danno: 25
            ),
            "Spada d'Argento": EquipmentItem(
                nome: "Spada d'Argento",
                tipo: .arma,
                prezzo: 4000,
                descrizione: "Efficace contro non-morti",
                danno: 22,
                bonus: "Anti-non morti"
            ),
            "Spada d'Oro": EquipmentItem(
                nome: "Spada d'Oro",
                tipo: .arma,
                prezzo: 6000,
                descrizione: "Arma cerimoniale",
                danno: 28
            ),
            "Spada di Platino": EquipmentItem(
                nome: "Spada di Platino",
                tipo: .arma,
                prezzo: 8000,
                descrizione: "Arma di lusso",
                danno: 32
            ),
            "Spada di Titanio": EquipmentItem(
                nome: "Spada di Titanio",
                tipo: .arma,
                prezzo: 10000,
                descrizione: "Tecnologia avanzata",
                danno: 35
            ),
            "Spada di Ossidiana": EquipmentItem(
                nome: "Spada di Ossidiana",
                tipo: .arma,
                prezzo: 12000,
                descrizione: "Lama vulcanica tagliente",
                danno: 40
            ),
            "Spada di Diamante": EquipmentItem(
                nome: "Spada di Diamante",
                tipo: .arma,
                prezzo: 15000,
                descrizione: "Durezza suprema",
                danno: 45
            ),
            "Spada di Mithril": EquipmentItem(
                nome: "Spada di Mithril",
                tipo: .arma,
                prezzo: 20000,
                descrizione: "Metallo mitologico",
                danno: 50
            ),
            "Spada di Cristallo Runico": EquipmentItem(
                nome: "Spada di Cristallo Runico",
                tipo: .arma,
                prezzo: 25000,
                descrizione: "Amplifica potere magico",
                danno: 55,
                bonus: "Magia+"
            ),
            "Spada di Essenza Divina": EquipmentItem(
                nome: "Spada di Essenza Divina",
                tipo: .arma,
                prezzo: 35000,
                descrizione: "Potere celestiale",
                danno: 60,
                bonus: "Divina"
            ),
            "Spada di Scaglie di Drago": EquipmentItem(
                nome: "Spada di Scaglie di Drago",
                tipo: .arma,
                prezzo: 50000,
                descrizione: "ARMA FINALE",
                danno: 70,
                bonus: "Suprema"
            ),
            
            // SCUDI - Progression dal legno al drago
            "Scudo di Legno": EquipmentItem(
                nome: "Scudo di Legno",
                tipo: .scudo,
                prezzo: 100,
                descrizione: "Protezione base",
                difesa: 2
            ),
            "Scudo di Pietra": EquipmentItem(
                nome: "Scudo di Pietra",
                tipo: .scudo,
                prezzo: 300,
                descrizione: "Protezione solida",
                difesa: 3
            ),
            "Scudo di Rame": EquipmentItem(
                nome: "Scudo di Rame",
                tipo: .scudo,
                prezzo: 600,
                descrizione: "Protezione metallica",
                difesa: 5
            ),
            "Scudo di Bronzo": EquipmentItem(
                nome: "Scudo di Bronzo",
                tipo: .scudo,
                prezzo: 900,
                descrizione: "Protezione antica",
                difesa: 8
            ),
            "Scudo di Ferro": EquipmentItem(
                nome: "Scudo di Ferro",
                tipo: .scudo,
                prezzo: 1400,
                descrizione: "Protezione pesante",
                difesa: 12
            ),
            "Scudo di Acciaio": EquipmentItem(
                nome: "Scudo di Acciaio",
                tipo: .scudo,
                prezzo: 2000,
                descrizione: "Protezione d'acciaio",
                difesa: 15
            ),
            "Scudo di Acciaio Temprato": EquipmentItem(
                nome: "Scudo di Acciaio Temprato",
                tipo: .scudo,
                prezzo: 2800,
                descrizione: "Protezione temprata",
                difesa: 20
            ),
            "Scudo d'Argento": EquipmentItem(
                nome: "Scudo d'Argento",
                tipo: .scudo,
                prezzo: 3200,
                descrizione: "Protezione magica",
                difesa: 18,
                bonus: "Anti-magia"
            ),
            "Scudo d'Oro": EquipmentItem(
                nome: "Scudo d'Oro",
                tipo: .scudo,
                prezzo: 4500,
                descrizione: "Protezione nobile",
                difesa: 25
            ),
            "Scudo di Platino": EquipmentItem(
                nome: "Scudo di Platino",
                tipo: .scudo,
                prezzo: 6000,
                descrizione: "Protezione preziosa",
                difesa: 30
            ),
            "Scudo di Titanio": EquipmentItem(
                nome: "Scudo di Titanio",
                tipo: .scudo,
                prezzo: 7500,
                descrizione: "Protezione moderna",
                difesa: 35
            ),
            "Scudo di Ossidiana": EquipmentItem(
                nome: "Scudo di Ossidiana",
                tipo: .scudo,
                prezzo: 9000,
                descrizione: "Protezione vulcanica",
                difesa: 40
            ),
            "Scudo di Diamante": EquipmentItem(
                nome: "Scudo di Diamante",
                tipo: .scudo,
                prezzo: 12000,
                descrizione: "Protezione indistruttibile",
                difesa: 45
            ),
            "Scudo di Mithril": EquipmentItem(
                nome: "Scudo di Mithril",
                tipo: .scudo,
                prezzo: 15000,
                descrizione: "Protezione magica",
                difesa: 50
            ),
            "Scudo di Cristallo Runico": EquipmentItem(
                nome: "Scudo di Cristallo Runico",
                tipo: .scudo,
                prezzo: 20000,
                descrizione: "Assorbe magia nemica",
                difesa: 55,
                bonus: "Assorbi-magia"
            ),
            "Scudo di Essenza Divina": EquipmentItem(
                nome: "Scudo di Essenza Divina",
                tipo: .scudo,
                prezzo: 28000,
                descrizione: "Protezione divina",
                difesa: 60,
                bonus: "Divina"
            ),
            "Scudo di Scaglie di Drago": EquipmentItem(
                nome: "Scudo di Scaglie di Drago",
                tipo: .scudo,
                prezzo: 40000,
                descrizione: "PROTEZIONE FINALE",
                difesa: 70,
                bonus: "Suprema"
            ),
            
            // ARMATURE - Progression completa
            "Armatura di Cuoio": EquipmentItem(
                nome: "Armatura di Cuoio",
                tipo: .armatura,
                prezzo: 200,
                descrizione: "Protezione leggera",
                difesa: 2
            ),
            "Elmo di Bronzo": EquipmentItem(
                nome: "Elmo di Bronzo",
                tipo: .armatura,
                prezzo: 800,
                descrizione: "Protezione testa",
                difesa: 6
            ),
            "Armatura di Ferro": EquipmentItem(
                nome: "Armatura di Ferro",
                tipo: .armatura,
                prezzo: 2000,
                descrizione: "Protezione completa",
                difesa: 10
            ),
            "Armatura di Acciaio": EquipmentItem(
                nome: "Armatura di Acciaio",
                tipo: .armatura,
                prezzo: 3000,
                descrizione: "Armatura da cavaliere",
                difesa: 15
            ),
            "Armatura da Gladiatore": EquipmentItem(
                nome: "Armatura da Gladiatore",
                tipo: .armatura,
                prezzo: 4000,
                descrizione: "Armatura da combattimento",
                difesa: 20
            ),
            "Esoscheletro": EquipmentItem(
                nome: "Esoscheletro",
                tipo: .armatura,
                prezzo: 12000,
                descrizione: "Tecnologia futuristica",
                difesa: 25,
                danno: 5,
                bonus: "+5 forza"
            ),
            "Armatura di Mithril": EquipmentItem(
                nome: "Armatura di Mithril",
                tipo: .armatura,
                prezzo: 25000,
                descrizione: "Leggera ma indistruttibile",
                difesa: 35
            ),
            "Armatura di Scaglie di Drago": EquipmentItem(
                nome: "Armatura di Scaglie di Drago",
                tipo: .armatura,
                prezzo: 60000,
                descrizione: "ARMATURA FINALE",
                difesa: 50,
                bonus: "Suprema"
            )
        ]
    }
    
    // MARK: - Area-Specific Items
    func getAreaItems() -> [String: [String]] {
        return [
            "Villaggio": [
                "🍖 Carne Fresca",
                "🥛 Latte Caldo", 
                "🧶 Gomitolo di Lana",
                "⚔️ Spada del Villaggio",
                "🛡️ Scudo del Guardiano"
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
    
    // MARK: - Shop Items by Player Level
    func getShopItemsForLevel(_ level: Int) -> [ShopItem] {
        let allEquipment = getEquipmentDatabase()
        var shopItems: [ShopItem] = []
        
        // Armi disponibili basate sul livello
        let weaponTiers = [
            (1, ["Spada di Legno", "Spada di Pietra"]),
            (5, ["Spada di Rame", "Spada di Bronzo"]),
            (10, ["Spada di Ferro", "Spada di Acciaio"]),
            (15, ["Spada di Acciaio Temprato", "Spada d'Argento"]),
            (20, ["Spada d'Oro", "Spada di Platino"]),
            (25, ["Spada di Titanio", "Spada di Ossidiana"]),
            (30, ["Spada di Diamante", "Spada di Mithril"]),
            (35, ["Spada di Cristallo Runico", "Spada di Essenza Divina"]),
            (40, ["Spada di Scaglie di Drago"])
        ]
        
        // Scudi disponibili basati sul livello
        let shieldTiers = [
            (1, ["Scudo di Legno", "Scudo di Pietra"]),
            (5, ["Scudo di Rame", "Scudo di Bronzo"]),
            (10, ["Scudo di Ferro", "Scudo di Acciaio"]),
            (15, ["Scudo di Acciaio Temprato", "Scudo d'Argento"]),
            (20, ["Scudo d'Oro", "Scudo di Platino"]),
            (25, ["Scudo di Titanio", "Scudo di Ossidiana"]),
            (30, ["Scudo di Diamante", "Scudo di Mithril"]),
            (35, ["Scudo di Cristallo Runico", "Scudo di Essenza Divina"]),
            (40, ["Scudo di Scaglie di Drago"])
        ]
        
        // Aggiungi oggetti disponibili per il livello attuale
        for (requiredLevel, items) in weaponTiers {
            if level >= requiredLevel {
                for itemName in items {
                    if let equipment = allEquipment[itemName] {
                        let recommended = level >= requiredLevel && level < requiredLevel + 5
                        shopItems.append(ShopItem(equipment: equipment, recommended: recommended))
                    }
                }
            }
        }
        
        for (requiredLevel, items) in shieldTiers {
            if level >= requiredLevel {
                for itemName in items {
                    if let equipment = allEquipment[itemName] {
                        let recommended = level >= requiredLevel && level < requiredLevel + 5
                        shopItems.append(ShopItem(equipment: equipment, recommended: recommended))
                    }
                }
            }
        }
        
        // Sempre disponibili: armature base
        let alwaysAvailable = ["Armatura di Cuoio", "Elmo di Bronzo"]
        for itemName in alwaysAvailable {
            if let equipment = allEquipment[itemName] {
                shopItems.append(ShopItem(equipment: equipment))
            }
        }
        
        // Armature avanzate per livelli alti
        if level >= 15 {
            let advancedArmor = ["Armatura di Ferro", "Armatura di Acciaio", "Armatura da Gladiatore"]
            for itemName in advancedArmor {
                if let equipment = allEquipment[itemName] {
                    shopItems.append(ShopItem(equipment: equipment))
                }
            }
        }
        
        if level >= 30 {
            let legendaryArmor = ["Esoscheletro", "Armatura di Mithril"]
            for itemName in legendaryArmor {
                if let equipment = allEquipment[itemName] {
                    shopItems.append(ShopItem(equipment: equipment))
                }
            }
        }
        
        if level >= 40 {
            if let equipment = allEquipment["Armatura di Scaglie di Drago"] {
                shopItems.append(ShopItem(equipment: equipment, recommended: true))
            }
        }
        
        return shopItems.sorted { $0.equipment.prezzo < $1.equipment.prezzo }
    }
}