//
//  GameManager.swift
//  Avventura epica
//
//  Created by Ambrogio Riili on 27/07/25.
//

import Foundation
import Combine

class GameManager: ObservableObject {
    @Published var gameState = GameState()
    @Published var currentScreen: GameScreen = .mainMenu
    
    // Combat state
    @Published var isInCombat = false
    @Published var currentMonster: Monster?
    @Published var monsterCurrentHP = 0
    @Published var combatRound = 0
    @Published var isAutoCombat = false
    
    // Auto combat timer
    private var autoCombatTimer: Timer?
    
    // Heartbeat timer for low health
    private var heartbeatTimer: Timer?
    
    // Audio state
    @Published var audioEnabled = true
    @Published var hapticEnabled = true
    
    // Logging
    private var logger = Logger()
    
    init() {
        setupGame()
        setupStartingEquipment()
        loadGame()
    }
    
    // MARK: - Game Setup
    private func setupGame() {
        logger.log("🎮 Inizializzazione gioco...")
        setupMonsters()
        setupEvolutions()
        setupRelics()
        logger.log("✅ Gioco inizializzato con successo")
    }
    
    private func setupStartingEquipment() {
        // Give starting equipment for the village
        let equipment = getEquipmentDatabase()
        
        // Starting items in village
        if let spadaVillaggio = equipment["Spada di Legno"] {
            gameState.inventario.addItem(spadaVillaggio)
        }
        
        if let scudoVillaggio = equipment["Scudo di Legno"] {
            gameState.inventario.addItem(scudoVillaggio)
        }
        
        logger.log("🏠 Equipaggiamento iniziale del villaggio aggiunto")
    }
    
    // MARK: - Navigation
    func navigateToScreen(_ screen: GameScreen) {
        logger.log("🧭 Navigazione a schermata: \(screen)")
        currentScreen = screen
        gameState.schermataCorrente = screen
        
        // Haptic feedback
        if hapticEnabled {
            hapticFeedback(.light)
        }
    }
    
    func goBack() {
        if !gameState.stackSchermate.isEmpty {
            let previousScreen = gameState.stackSchermate.removeLast()
            navigateToScreen(previousScreen)
        } else {
            navigateToScreen(.mainMenu)
        }
    }
    
    // MARK: - Cat Management
    func selectActiveCat(_ catId: String) {
        guard gameState.gatti[catId]?.sbloccato == true else { return }
        gameState.gattoAttivo = catId
        logger.log("🐱 Gatto attivo cambiato: \(gameState.gatti[catId]?.nome ?? catId)")
        saveGame()
    }
    
    func unlockCat(_ catId: String) {
        gameState.gatti[catId]?.sbloccato = true
        gameState.gatti[catId]?.affinita = 30
        logger.log("🔓 Gatto sbloccato: \(gameState.gatti[catId]?.nome ?? catId)")
        saveGame()
    }
    
    func evolveCat(_ catId: String) {
        guard let cat = gameState.gatti[catId], 
              cat.affinita >= 200 else { return }
        
        gameState.gatti[catId]?.formaEvoluta = true
        logger.log("✨ Gatto evoluto: \(cat.nome)")
        saveGame()
    }
    
    func increaseCatAffinity(_ catId: String, amount: Int = 5) {
        let currentAffinity = gameState.gatti[catId]?.affinita ?? 0
        gameState.gatti[catId]?.affinita = min(currentAffinity + amount, 250)
        saveGame()
    }
    
    // MARK: - Area Management
    func changeArea(_ newArea: String) {
        guard gameState.areeSbloccate.contains(newArea) else {
            logger.log("❌ Area non sbloccata: \(newArea)")
            return
        }
        
        gameState.areaAttuale = newArea
        gameState.turniInArea = 0
        
        // Change background music and ambient sounds
        AudioManager.shared.playAreaMusic(newArea)
        AudioManager.shared.playAreaAmbient(newArea)
        
        logger.log("🗺️ Area cambiata: \(newArea)")
        saveGame()
    }
    
    func unlockNextArea() {
        guard let currentIndex = gameState.areeOrdinate.firstIndex(of: gameState.areaAttuale),
              currentIndex < gameState.areeOrdinate.count - 1 else { return }
        
        let nextArea = gameState.areeOrdinate[currentIndex + 1]
        if !gameState.areeSbloccate.contains(nextArea) {
            gameState.areeSbloccate.append(nextArea)
            logger.log("🔓 Nuova area sbloccata: \(nextArea)")
        }
        saveGame()
    }
    
    func increaseAreaProgress(_ amount: Int = 10) {
        let currentProgress = gameState.progressioneArea[gameState.areaAttuale] ?? 0
        let newProgress = min(currentProgress + amount, 100)
        gameState.progressioneArea[gameState.areaAttuale] = newProgress
        
        // Check for boss unlock when progress reaches 100
        if newProgress >= 100 && currentProgress < 100 {
            checkBossUnlock()
        }
        
        saveGame()
    }
    
    private func checkBossUnlock() {
        let area = gameState.areaAttuale
        
        // Check if area has a boss and it's not defeated yet
        guard let boss = getAreaBoss(area),
              !gameState.bossSconfitti.contains(boss.nome),
              !gameState.bossNotificationsMostrate.contains(area) else {
            // If boss already defeated, unlock next area
            if gameState.bossSconfitti.contains(getAreaBoss(area)?.nome ?? "") {
                unlockNextArea()
            }
            return
        }
        
        // Mark notification as shown and trigger boss notification
        gameState.bossNotificationsMostrate.insert(area)
        gameState.showingBossNotification = true
        gameState.currentBossArea = area
        
        logger.log("🔔 Boss sbloccato per area: \(area)")
        
        // Play boss unlock sound
        AudioManager.shared.playBossSound()
        AudioManager.shared.hapticWarning()
        
        saveGame()
    }
    
    private func getAreaBoss(_ area: String) -> Monster? {
        // Get base boss stats
        var boss: Monster?
        
        switch area {
        case "Villaggio":
            boss = Monster(nome: "🐕 Cane Randagio", emoji: "🐕", hp: 180, attacco: 40, area: area, chiave: "🗝️ Chiave della Cantina", audioFile: "effetto_boss_1")
        case "🏠 Cantina":
            boss = Monster(nome: "🕷️ Regina dei Ragni", emoji: "🕷️", hp: 240, attacco: 50, area: area, chiave: "🗝️ Chiave della Cantina", audioFile: "effetto_boss_regina_ragni")
        case "🚰 Fogne":
            boss = Monster(nome: "🐀 Boss Topo delle Fogne", emoji: "🐀", hp: 360, attacco: 65, area: area, chiave: "🌀 Chiave del Labirinto")
        case "🌀 Labirinto Antico":
            boss = Monster(nome: "🗿 Guardiano di Pietra", emoji: "🗿", hp: 480, attacco: 80, area: area, chiave: "❄️ Chiave dell'Inverno")
        case "❄️ Area Innevata":
            boss = Monster(nome: "🐺 Alpha del Branco", emoji: "🐺", hp: 600, attacco: 95, area: area, chiave: "🌿 Chiave della Natura")
        case "🌿 Giungla Selvaggia":
            boss = Monster(nome: "🐍 Serpente Ancestrale", emoji: "🐍", hp: 720, attacco: 110, area: area, chiave: "🌲 Chiave del Bosco")
        case "🌲 Bosco Profondo":
            boss = Monster(nome: "🦌 Cervo Mistico", emoji: "🦌", hp: 840, attacco: 125, area: area, chiave: "⚰️ Chiave dei Morti")
        case "⚰️ Cimitero":
            boss = Monster(nome: "💀 Lich Supremo", emoji: "💀", hp: 960, attacco: 140, area: area, chiave: "🏚️ Chiave dell'Orrore")
        case "🏚️ Casa degli Orrori":
            boss = Monster(nome: "👻 Spirito Maledetto", emoji: "👻", hp: 1080, attacco: 155, area: area, chiave: "🏭 Chiave Industriale")
        case "🏭 Fabbrica Abbandonata":
            boss = Monster(nome: "🤖 Automa Corrotto", emoji: "🤖", hp: 1200, attacco: 170, area: area, chiave: "⛏️ Chiave della Miniera")
        case "⛏️ Miniera Profonda":
            boss = Monster(nome: "⛰️ Elementale di Terra", emoji: "⛰️", hp: 1320, attacco: 185, area: area, chiave: "🌙 Chiave Oscura")
        case "🌙 Cripta Maledetta":
            boss = Monster(nome: "🧙‍♂️ Necromante Antico", emoji: "🧙‍♂️", hp: 1440, attacco: 200, area: area, chiave: "🌊 Chiave dell'Oceano")
        case "🌊 Mare":
            boss = Monster(nome: "🐙 Kraken Leggendario", emoji: "🐙", hp: 1560, attacco: 215, area: area, chiave: "🏔️ Chiave Sacra")
        case "🏔️ Montagna Sacra":
            boss = Monster(nome: "🦅 Fenice Dorata", emoji: "🦅", hp: 1680, attacco: 230, area: area, chiave: "🌋 Chiave del Fuoco")
        case "🌋 Vulcano Attivo":
            boss = Monster(nome: "🔥 Drago di Magma", emoji: "🔥", hp: 1800, attacco: 245, area: area, chiave: "👑 Chiave Finale")
        case "👑 Palazzo Finale":
            boss = Monster(nome: "👑 Imperatore Oscuro", emoji: "👑", hp: 2000, attacco: 300, area: area, chiave: "🌌 Chiave degli Incubi")
        case "🌌 Regno degli Incubi":
            boss = Monster(nome: "🌌 Signore degli Incubi", emoji: "🌌", hp: 2500, attacco: 350, area: area)
        default:
            return nil
        }
        
        // Apply boss scaling if player is under-leveled
        if var scaledBoss = boss {
            let requiredLevel = calculateMinimumBossLevel(area)
            if gameState.livello < requiredLevel {
                // Boss becomes 3x stronger if player is under-leveled
                scaledBoss.hp = Int(Double(scaledBoss.hp) * 3.0)
                scaledBoss.attacco = Int(Double(scaledBoss.attacco) * 3.0)
                logger.log("⚠️ Boss potenziato 3x! Livello richiesto: \(requiredLevel), Attuale: \(gameState.livello)")
            }
            return scaledBoss
        }
        
        return boss
    }
    
    private func calculateMinimumBossLevel(_ area: String) -> Int {
        // Calculate required level based on area index
        // Village (index 0) = no boss
        // Cantina (index 1) = level 4
        // Fogne (index 2) = level 8, etc.
        
        guard let areaIndex = gameState.areeOrdinate.firstIndex(of: area) else {
            return 20 // High level for unknown areas
        }
        
        if areaIndex <= 0 {
            return 1 // No boss in village
        }
        
        return areaIndex * 4 // Each area requires 4 more levels
    }
    
    func getBossScalingInfo(_ area: String) -> (isScaled: Bool, requiredLevel: Int, currentLevel: Int) {
        let requiredLevel = calculateMinimumBossLevel(area)
        let isScaled = gameState.livello < requiredLevel
        return (isScaled, requiredLevel, gameState.livello)
    }
    
    func startBossFight() {
        guard let boss = getAreaBoss(gameState.currentBossArea ?? gameState.areaAttuale) else { return }
        
        gameState.showingBossNotification = false
        startCombat(with: boss)
        
        logger.log("⚔️ Iniziato combattimento con boss: \(boss.nome)")
    }
    
    func dismissBossNotification() {
        gameState.showingBossNotification = false
        gameState.currentBossArea = nil
        saveGame()
    }
    
    // MARK: - Random Monsters System
    func getRandomMonsterForArea(_ area: String) -> Monster {
        switch area {
        case "Villaggio":
            return getRandomVillageMonster()
        case "🏠 Cantina":
            return getRandomCellarMonster()
        default:
            return getFixedAreaMonster(area)
        }
    }
    
    private func getRandomVillageMonster() -> Monster {
        let villageMonsters = [
            (nome: "👨‍🌾 Contadino Arrabbiato", emoji: "👨‍🌾", hp: 70, attacco: 8, audio: "effetto_mostro_1"),
            (nome: "🐗 Cinghiale Affamato", emoji: "🐗", hp: 90, attacco: 12, audio: "effetto_mostro_2"),
            (nome: "🐂 Toro Scatenato", emoji: "🐂", hp: 110, attacco: 15, audio: "effetto_mostro_3"),
            (nome: "🐴 Cavallo Pazzo", emoji: "🐴", hp: 85, attacco: 10, audio: "effetto_mostro_4"),
            (nome: "🐐 Capra Indemoniata", emoji: "🐐", hp: 80, attacco: 11, audio: "effetto_mostro_5")
        ]
        
        let randomMonster = villageMonsters.randomElement()!
        return Monster(
            nome: randomMonster.nome,
            emoji: randomMonster.emoji,
            hp: randomMonster.hp,
            attacco: randomMonster.attacco,
            area: "Villaggio",
            audioFile: randomMonster.audio
        )
    }
    
    private func getRandomCellarMonster() -> Monster {
        let cellarMonsters = [
            (nome: "🕷️ Ragno Peloso", emoji: "🕷️", hp: 95, attacco: 13, audio: "effetto_cantina_ragno"),
            (nome: "🦇 Sciame di Pipistrelli", emoji: "🦇", hp: 80, attacco: 11, audio: "effetto_cantina_pipistrelli"),
            (nome: "🟢 Muffa Vivente", emoji: "🟢", hp: 110, attacco: 9, audio: "effetto_cantina_muffa"),
            (nome: "🪲 Insetto Carapace", emoji: "🪲", hp: 105, attacco: 14, audio: "effetto_cantina_insetto"),
            (nome: "🟣 Melma Posseduta", emoji: "🟣", hp: 100, attacco: 12, audio: "effetto_cantina_melma")
        ]
        
        let randomMonster = cellarMonsters.randomElement()!
        return Monster(
            nome: randomMonster.nome,
            emoji: randomMonster.emoji,
            hp: randomMonster.hp,
            attacco: randomMonster.attacco,
            area: "🏠 Cantina",
            audioFile: randomMonster.audio
        )
    }
    
    private func getFixedAreaMonster(_ area: String) -> Monster {
        // Fixed monsters for other areas - only Villaggio and Cantina have specific audio files
        switch area {
        case "🚰 Fogne":
            return Monster(nome: "🐀 Ratto delle Fogne", emoji: "🐀", hp: 120, attacco: 16, area: area)
        case "🌀 Labirinto Antico":
            return Monster(nome: "🗿 Guardiano di Pietra", emoji: "🗿", hp: 140, attacco: 18, area: area)
        case "❄️ Area Innevata":
            return Monster(nome: "🐺 Lupo Gelido", emoji: "🐺", hp: 160, attacco: 20, area: area)
        case "🌿 Giungla Selvaggia":
            return Monster(nome: "🐍 Serpente Velenoso", emoji: "🐍", hp: 180, attacco: 22, area: area)
        case "🌲 Bosco Profondo":
            return Monster(nome: "🐻 Orso Bruno", emoji: "🐻", hp: 200, attacco: 24, area: area)
        case "⚰️ Cimitero":
            return Monster(nome: "💀 Scheletro Errante", emoji: "💀", hp: 220, attacco: 26, area: area)
        case "🏚️ Casa degli Orrori":
            return Monster(nome: "👻 Fantasma Tormentato", emoji: "👻", hp: 240, attacco: 28, area: area)
        case "🏭 Fabbrica Abbandonata":
            return Monster(nome: "🤖 Robot Malfunzionante", emoji: "🤖", hp: 260, attacco: 30, area: area)
        case "⛏️ Miniera Profonda":
            return Monster(nome: "⛰️ Golem di Ferro", emoji: "⛰️", hp: 280, attacco: 32, area: area)
        case "🌙 Cripta Maledetta":
            return Monster(nome: "🧙‍♂️ Lich Minore", emoji: "🧙‍♂️", hp: 300, attacco: 34, area: area)
        case "🌊 Mare":
            return Monster(nome: "🐙 Kraken Giovane", emoji: "🐙", hp: 320, attacco: 36, area: area)
        case "🏔️ Montagna Sacra":
            return Monster(nome: "🐉 Drago di Montagna", emoji: "🐉", hp: 340, attacco: 38, area: area)
        case "🌋 Vulcano Attivo":
            return Monster(nome: "🔥 Elementale del Fuoco", emoji: "🔥", hp: 360, attacco: 40, area: area)
        case "👑 Palazzo Finale":
            return Monster(nome: "⚔️ Guardia Reale", emoji: "⚔️", hp: 380, attacco: 42, area: area)
        case "🌌 Regno degli Incubi":
            return Monster(nome: "🌌 Ombra dell'Incubo", emoji: "🌌", hp: 400, attacco: 45, area: area)
        default:
            return Monster(nome: "👹 Mostro Misterioso", emoji: "👹", hp: 50, attacco: 8, area: area)
        }
    }
    
    // MARK: - Combat System
    func startCombat(with monster: Monster) {
        isInCombat = true
        currentMonster = monster
        monsterCurrentHP = monster.hp
        combatRound = 0
        gameState.inCombattimento = true
        gameState.mostroAttuale = monster
        gameState.hpMostroAttuale = monster.hp
        
        logger.log("⚔️ Combattimento iniziato contro: \(monster.nome)")
        
        // Play combat music and sounds
        let isBoss = monster.chiave != nil
        let isFinalBoss = monster.area == "👑 Palazzo Finale"
        AudioManager.shared.playCombatMusic(isBoss, isFinalBoss: isFinalBoss)
        AudioManager.shared.playCombatStartSound()
        
        // Play monster-specific roar sound
        if let audioFile = monster.audioFile {
            AudioManager.shared.playMonsterRoar(audioFile)
        } else if isBoss {
            // Fallback generic boss sound for bosses without specific audio
            AudioManager.shared.playBossSound()
        } else {
            // Generic monster sounds for regular monsters without specific audio
            AudioManager.shared.playMonsterSound(Int.random(in: 1...5))
        }
    }
    
    func performAttack() -> (playerDamage: Int, monsterDamage: Int, playerWins: Bool, monsterWins: Bool) {
        guard let monster = currentMonster,
              let activeCat = gameState.gatti[gameState.gattoAttivo] else {
            return (0, 0, false, false)
        }
        
        combatRound += 1
        gameState.roundCombattimento = combatRound
        
        // Calculate damage
        let playerDamage = calculatePlayerDamage(cat: activeCat, against: monster)
        let monsterDamage = calculateMonsterDamage(monster: monster, against: activeCat)
        
        // Apply damage
        monsterCurrentHP = max(0, monsterCurrentHP - playerDamage)
        gameState.hpMostroAttuale = monsterCurrentHP
        
        // Check if monster is defeated
        if monsterCurrentHP <= 0 {
            endCombat(playerWins: true)
            return (playerDamage, 0, true, false)
        }
        
        // Monster attacks back
        let catHP = gameState.gatti[gameState.gattoAttivo]?.fame ?? 0
        let newCatHP = max(0, catHP - monsterDamage)
        gameState.gatti[gameState.gattoAttivo]?.fame = newCatHP
        
        // Check if cat is defeated
        if newCatHP <= 0 {
            endCombat(playerWins: false)
            return (playerDamage, monsterDamage, false, true)
        }
        
        // Check for low health heartbeat after taking damage
        checkLowHealth()
        
        saveGame()
        return (playerDamage, monsterDamage, false, false)
    }
    
    private func calculatePlayerDamage(cat: Cat, against monster: Monster) -> Int {
        var damage = cat.attacco
        
        // Apply cat ability bonuses
        switch cat.abilita {
        case .combattimento:
            damage += 3
        case .partner:
            damage += 2
        default:
            break
        }
        
        // Apply equipment bonuses
        damage += gameState.inventario.stats.totalDamage
        
        // Special equipment bonuses
        if monster.nome.contains("Fantasma") || monster.nome.contains("Zombie") || monster.nome.contains("Scheletro") {
            // Anti-undead weapons do extra damage
            for item in gameState.inventario.items.values {
                if item.isEquipped && item.equipment.bonus?.contains("Anti-non morti") == true {
                    damage += 5
                }
            }
        }
        
        // Random factor
        let randomFactor = Double.random(in: 0.8...1.2)
        return Int(Double(damage) * randomFactor)
    }
    
    private func calculateMonsterDamage(monster: Monster, against cat: Cat) -> Int {
        var damage = monster.attacco
        
        // Apply cat defensive abilities
        if cat.abilita == .guarigione {
            damage = max(1, damage - 2)
        }
        
        // Apply equipment defense
        damage = max(1, damage - gameState.inventario.stats.totalDefense)
        
        // Special equipment bonuses
        for item in gameState.inventario.items.values {
            if item.isEquipped {
                if item.equipment.bonus?.contains("Anti-magia") == true && monster.nome.contains("Magia") {
                    damage = max(1, damage - 3)
                }
                if item.equipment.bonus?.contains("Assorbi-magia") == true {
                    damage = max(1, damage / 2)
                }
            }
        }
        
        let randomFactor = Double.random(in: 0.8...1.2)
        return Int(Double(damage) * randomFactor)
    }
    
    private func endCombat(playerWins: Bool) {
        isInCombat = false
        isAutoCombat = false
        autoCombatTimer?.invalidate()
        autoCombatTimer = nil
        gameState.inCombattimento = false
        gameState.mostroAttuale = nil
        
        if playerWins {
            logger.log("🏆 Combattimento vinto!")
            
            // Play victory sound and cat purr
            AudioManager.shared.playVictorySound()
            AudioManager.shared.playCatPurrSound()
            
            // Add rewards
            gainExperience(50)
            addResources(cibo: 10, energia: 20)
            increaseAreaProgress(25)
            increaseCatAffinity(gameState.gattoAttivo, amount: 10)
            
            // Play money/collection sound for rewards
            AudioManager.shared.playCollectMoneySound()
            
            // Add boss to defeated list and unlock next area
            if let monster = currentMonster, !gameState.bossSconfitti.contains(monster.nome) {
                gameState.bossSconfitti.append(monster.nome)
                
                // Give key if boss has one
                if let key = monster.chiave, !gameState.chiaviRaccolte.contains(key) {
                    gameState.chiaviRaccolte.append(key)
                    logger.log("🗝️ Chiave ottenuta: \(key)")
                }
                
                // If this was an area boss, unlock the next area
                if getAreaBoss(gameState.areaAttuale)?.nome == monster.nome {
                    unlockNextArea()
                    logger.log("🌟 Area boss sconfitto - prossima area sbloccata!")
                }
            }
        } else {
            logger.log("💀 Combattimento perso!")
            AudioManager.shared.playDefeatSound()
            AudioManager.shared.playHeartbeatSound()
        }
        
        // Stop heartbeat when combat ends
        if gameState.heartbeatAttivo {
            stopHeartbeat()
        }
        
        // Check for heartbeat after combat
        checkLowHealth()
        
        // Return to area music after combat
        AudioManager.shared.playAreaMusic(gameState.areaAttuale)
        
        currentMonster = nil
        saveGame()
    }
    
    // MARK: - Auto Combat System
    func toggleAutoCombat() {
        guard isInCombat else { return }
        
        isAutoCombat.toggle()
        
        if isAutoCombat {
            logger.log("🤖 Auto-combat attivato")
            startAutoCombat()
        } else {
            logger.log("🛑 Auto-combat disattivato")
            stopAutoCombat()
        }
    }
    
    private func startAutoCombat() {
        autoCombatTimer = Timer.scheduledTimer(withTimeInterval: 2.0, repeats: true) { [weak self] _ in
            guard let self = self else { return }
            
            DispatchQueue.main.async {
                guard self.isInCombat && self.isAutoCombat else {
                    self.stopAutoCombat()
                    return
                }
                
                // Auto-use healing items if health is low
                if let activeCat = self.gameState.gatti[self.gameState.gattoAttivo],
                   activeCat.fame < 30 && self.gameState.risorse.pozioni > 0 {
                    self.useCombatPotion()
                }
                
                // Perform auto attack
                let _ = self.performAttack()
            }
        }
    }
    
    private func stopAutoCombat() {
        autoCombatTimer?.invalidate()
        autoCombatTimer = nil
        isAutoCombat = false
    }
    
    // MARK: - Combat Items
    @discardableResult
    func useCombatPotion() -> Bool {
        guard isInCombat,
              gameState.risorse.pozioni > 0,
              var activeCat = gameState.gatti[gameState.gattoAttivo] else { return false }
        
        let currentHP = activeCat.fame
        let maxHP = 100
        
        // Don't use if already at full health
        guard currentHP < maxHP else { return false }
        
        gameState.risorse.pozioni -= 1
        let healAmount = 50
        let newHP = min(maxHP, currentHP + healAmount)
        activeCat.fame = newHP
        gameState.gatti[gameState.gattoAttivo] = activeCat
        
        logger.log("💊 Pozione usata in combattimento: \(currentHP) → \(newHP) HP")
        AudioManager.shared.playPotionUseSound()
        AudioManager.shared.playCatPurrSound()
        
        // Check if health is no longer critical
        checkLowHealth()
        
        saveGame()
        
        return true
    }
    
    func useCombatFood() -> Bool {
        guard isInCombat,
              gameState.risorse.cibo > 0,
              var activeCat = gameState.gatti[gameState.gattoAttivo] else { return false }
        
        let currentHP = activeCat.fame
        let maxHP = 100
        
        // Don't use if already at full health
        guard currentHP < maxHP else { return false }
        
        gameState.risorse.cibo -= 1
        let healAmount = 15
        let newHP = min(maxHP, currentHP + healAmount)
        activeCat.fame = newHP
        gameState.gatti[gameState.gattoAttivo] = activeCat
        
        logger.log("🍖 Cibo usato in combattimento: \(currentHP) → \(newHP) HP")
        AudioManager.shared.playEatingSound()
        AudioManager.shared.playCatFishSound()
        
        // Check if health is no longer critical
        checkLowHealth()
        
        saveGame()
        
        return true
    }
    
    func useCombatWater() -> Bool {
        guard isInCombat,
              gameState.risorse.acqua > 0,
              var activeCat = gameState.gatti[gameState.gattoAttivo] else { return false }
        
        let currentHP = activeCat.fame
        let maxHP = 100
        
        // Don't use if already at full health
        guard currentHP < maxHP else { return false }
        
        gameState.risorse.acqua -= 1
        let healAmount = 10
        let newHP = min(maxHP, currentHP + healAmount)
        activeCat.fame = newHP
        gameState.gatti[gameState.gattoAttivo] = activeCat
        
        logger.log("💧 Acqua usata in combattimento: \(currentHP) → \(newHP) HP")
        AudioManager.shared.playDrinkingSound()
        saveGame()
        
        return true
    }
    
    // MARK: - Heartbeat System for Low Health in Combat
    func checkLowHealth() {
        // Heartbeat only works during combat
        guard isInCombat else {
            // Stop heartbeat if not in combat
            if gameState.heartbeatAttivo {
                stopHeartbeat()
            }
            return
        }
        
        guard let activeCat = gameState.gatti[gameState.gattoAttivo] else { return }
        
        let healthPercentage = Double(activeCat.fame) / 100.0 * 100.0
        
        if healthPercentage <= 20 && activeCat.fame > 0 {
            // Start heartbeat if not already active
            if !gameState.heartbeatAttivo {
                startHeartbeat()
            }
        } else {
            // Stop heartbeat if health is above 20% or cat is dead
            if gameState.heartbeatAttivo {
                stopHeartbeat()
            }
        }
    }
    
    private func startHeartbeat() {
        gameState.heartbeatAttivo = true
        logger.log("💓 Heartbeat attivato - vita critica!")
        
        // Play immediate heartbeat
        AudioManager.shared.playHeartbeatSound()
        
        // Start continuous heartbeat timer (every 2 seconds)
        heartbeatTimer = Timer.scheduledTimer(withTimeInterval: 2.0, repeats: true) { [weak self] _ in
            guard let self = self else { return }
            
            DispatchQueue.main.async {
                // Check if we should continue heartbeat - only in combat
                guard self.isInCombat,
                      let activeCat = self.gameState.gatti[self.gameState.gattoAttivo] else {
                    self.stopHeartbeat()
                    return
                }
                
                let healthPercentage = Double(activeCat.fame) / 100.0 * 100.0
                
                if healthPercentage <= 20 && activeCat.fame > 0 && self.gameState.heartbeatAttivo {
                    AudioManager.shared.playHeartbeatSound()
                } else {
                    self.stopHeartbeat()
                }
            }
        }
    }
    
    private func stopHeartbeat() {
        gameState.heartbeatAttivo = false
        heartbeatTimer?.invalidate()
        heartbeatTimer = nil
        logger.log("💓 Heartbeat fermato")
    }
    
    // MARK: - Resource Management
    func addResources(cibo: Int = 0, acqua: Int = 0, legno: Int = 0, 
                     pietra: Int = 0, ferro: Int = 0, energia: Int = 0, pozioni: Int = 0) {
        gameState.risorse.cibo += cibo
        gameState.risorse.acqua += acqua
        gameState.risorse.legno += legno
        gameState.risorse.pietra += pietra
        gameState.risorse.ferro += ferro
        gameState.risorse.energia += energia
        gameState.risorse.pozioni += pozioni
        
        saveGame()
    }
    
    // MARK: - Nutrition System
    func nutriGatto() -> (success: Bool, message: String) {
        guard !gameState.gattoAttivo.isEmpty,
              var activeCat = gameState.gatti[gameState.gattoAttivo] else {
            return (false, "❌ Nessun gatto attivo!")
        }
        
        // Emergency situation: no food but very low energy
        if gameState.risorse.cibo == 0 {
            if gameState.risorse.energia <= 10 {
                // Emergency help from cat
                let energiaRecuperata = 30
                gameState.risorse.energia = min(100, gameState.risorse.energia + energiaRecuperata)
                
                // Cat gets some happiness for helping
                activeCat.felicita = min(100, activeCat.felicita + 10)
                gameState.gatti[gameState.gattoAttivo] = activeCat
                
                AudioManager.shared.playCatPurrSound()
                AudioManager.shared.hapticSuccess()
                
                let message = """
                🆘 EMERGENZA! \(activeCat.nome) condivide le sue riserve segrete!
                Il tuo gatto ti ha salvato dalla situazione impossibile!
                Energia recuperata: +\(energiaRecuperata) (ora: \(gameState.risorse.energia)/100)
                😊 \(activeCat.nome) è felice di averti aiutato! Felicità: \(activeCat.felicita)/100
                🔄 Ora puoi raccogliere risorse per ottenere cibo!
                """
                
                saveGame()
                return (true, message)
            } else {
                return (false, "🍽️ Non hai cibo per nutrire il gatto!\n\nCome ottenere cibo:\n• Esplora le aree\n• Raccogli risorse\n• Combatti i nemici")
            }
        }
        
        // Normal feeding
        _ = gameState.risorse.cibo >= 5 ? 5 : gameState.risorse.cibo
        let energiaRecuperata: Int
        let messaggio: String
        
        if gameState.risorse.cibo >= 5 {
            gameState.risorse.cibo -= 5
            energiaRecuperata = 50
            messaggio = "🐱 \(activeCat.nome) condivide il cibo con te!"
        } else {
            let ciboDisponibile = gameState.risorse.cibo
            gameState.risorse.cibo = 0
            let efficacia = Double(ciboDisponibile) / 5.0
            energiaRecuperata = Int(50 * efficacia)
            messaggio = "🐱 \(activeCat.nome) condivide il poco cibo rimasto!"
        }
        
        // Recover energy
        gameState.risorse.energia = min(100, gameState.risorse.energia + energiaRecuperata)
        
        // Update cat stats
        activeCat.fame = min(100, activeCat.fame + 15)
        activeCat.felicita = min(100, activeCat.felicita + 20)
        gameState.gatti[gameState.gattoAttivo] = activeCat
        
        // Bonus if cat is very happy
        var finalMessage = "\(messaggio)\nEnergia recuperata: +\(energiaRecuperata) (ora: \(gameState.risorse.energia)/100)\n"
        
        if activeCat.felicita > 80 {
            let expBonus = 2
            gainExperience(expBonus)
            finalMessage += "😊 \(activeCat.nome) è molto felice! Bonus: +\(expBonus) EXP"
            AudioManager.shared.playCatPurrSound()
        } else {
            finalMessage += "😊 Felicità: \(activeCat.felicita)/100"
        }
        
        AudioManager.shared.playEatingSound()
        AudioManager.shared.hapticSuccess()
        saveGame()
        
        return (true, finalMessage)
    }
    
    func consumaCibo() -> (success: Bool, message: String) {
        guard !gameState.gattoAttivo.isEmpty,
              var activeCat = gameState.gatti[gameState.gattoAttivo] else {
            return (false, "❌ Nessun gatto attivo!")
        }
        
        if gameState.risorse.cibo == 0 {
            return (false, "🍽️ Non hai cibo!\n\nCome ottenere cibo:\n• Esplora le aree\n• Raccogli risorse\n• Combatti i nemici")
        }
        
        let ciboNecessario = min(gameState.risorse.cibo, 10)
        let hpMax = 100
        let currentHP = activeCat.fame
        
        if currentHP >= hpMax {
            return (false, "❤️ \(activeCat.nome) ha già la vita al massimo (\(currentHP)/\(hpMax))")
        }
        
        // Calculate healing
        let efficacia = Double(ciboNecessario) / 10.0
        let hpRecuperatiMassimi = Int(45 * efficacia)
        let hpRecuperati = min(hpRecuperatiMassimi, hpMax - currentHP)
        
        gameState.risorse.cibo -= ciboNecessario
        activeCat.fame = min(hpMax, currentHP + hpRecuperati)
        gameState.gatti[gameState.gattoAttivo] = activeCat
        
        let message = """
        🍽️ \(activeCat.nome) consuma cibo per curarsi:
        HP recuperati: +\(hpRecuperati) (ora: \(activeCat.fame)/\(hpMax))
        Cibo utilizzato: \(ciboNecessario)
        """
        
        AudioManager.shared.playEatingSound()
        AudioManager.shared.hapticSuccess()
        saveGame()
        
        return (true, message)
    }
    
    func beviAcqua() -> (success: Bool, message: String) {
        guard !gameState.gattoAttivo.isEmpty,
              var activeCat = gameState.gatti[gameState.gattoAttivo] else {
            return (false, "❌ Nessun gatto attivo!")
        }
        
        if gameState.risorse.acqua == 0 {
            return (false, "💧 Non hai acqua!\n\nCome ottenere acqua:\n• Esplora le aree\n• Raccogli risorse nelle zone con acqua\n• Combatti nemici marini")
        }
        
        let acquaNecessaria = min(gameState.risorse.acqua, 5)
        let efficacia = Double(acquaNecessaria) / 5.0
        let durataEffetto = max(1, Int(5 * efficacia))
        
        gameState.risorse.acqua -= acquaNecessaria
        
        // Water gives temporary bonuses (simplified - could be expanded)
        activeCat.felicita = min(100, activeCat.felicita + 10)
        gameState.gatti[gameState.gattoAttivo] = activeCat
        
        let message = """
        💧 \(activeCat.nome) beve acqua rinfrescante:
        Felicità aumentata: +10 (ora: \(activeCat.felicita)/100)
        Effetto idratazione per \(durataEffetto) turni
        Acqua utilizzata: \(acquaNecessaria)
        """
        
        AudioManager.shared.playDrinkingSound()
        AudioManager.shared.hapticSuccess()
        saveGame()
        
        return (true, message)
    }
    
    // MARK: - Energy Check for Combat
    func canStartCombat() -> (canFight: Bool, message: String) {
        let energiaNecessaria = 20
        
        if gameState.risorse.energia >= energiaNecessaria {
            return (true, "")
        }
        
        var message = "⚡ Energia Insufficiente!\n\n"
        message += "Energia attuale: \(gameState.risorse.energia)/\(energiaNecessaria) necessari\n\n"
        message += "Come recuperare energia:\n"
        
        if gameState.risorse.cibo > 0 {
            message += "• 🐱 Nutri il tuo gatto per recuperare energia\n"
        } else {
            message += "• 🔍 Raccogli risorse per ottenere cibo\n"
            message += "• 🐱 Nutri il gatto con il cibo ottenuto\n"
        }
        
        message += "• 💤 Usa la funzione 'Riposa' se disponibile\n"
        message += "• 🍖 Raccogli più cibo esplorando le aree"
        
        return (false, message)
    }
    
    func spendResources(cibo: Int = 0, acqua: Int = 0, legno: Int = 0,
                       pietra: Int = 0, ferro: Int = 0, energia: Int = 0, pozioni: Int = 0) -> Bool {
        // Check if we have enough resources
        guard gameState.risorse.cibo >= cibo,
              gameState.risorse.acqua >= acqua,
              gameState.risorse.legno >= legno,
              gameState.risorse.pietra >= pietra,
              gameState.risorse.ferro >= ferro,
              gameState.risorse.energia >= energia,
              gameState.risorse.pozioni >= pozioni else {
            return false
        }
        
        // Spend resources
        gameState.risorse.cibo -= cibo
        gameState.risorse.acqua -= acqua
        gameState.risorse.legno -= legno
        gameState.risorse.pietra -= pietra
        gameState.risorse.ferro -= ferro
        gameState.risorse.energia -= energia
        gameState.risorse.pozioni -= pozioni
        
        saveGame()
        return true
    }
    
    func useHealthPotion() {
        guard gameState.risorse.pozioni > 0,
              var activeCat = gameState.gatti[gameState.gattoAttivo] else { return }
        
        gameState.risorse.pozioni -= 1
        activeCat.fame = min(100, activeCat.fame + 50)
        gameState.gatti[gameState.gattoAttivo] = activeCat
        
        logger.log("💊 Pozione usata")
        AudioManager.shared.playPotionUseSound()
        AudioManager.shared.playCatPurrSound()
        saveGame()
    }
    
    // MARK: - Experience System
    func gainExperience(_ amount: Int) {
        gameState.esperienza += amount
        
        // Check for level up
        while gameState.esperienza >= gameState.esperienzaProssimoLivello {
            levelUp()
        }
        
        saveGame()
    }
    
    private func levelUp() {
        gameState.livello += 1
        gameState.esperienza -= gameState.esperienzaProssimoLivello
        gameState.esperienzaProssimoLivello = Int(Double(gameState.esperienzaProssimoLivello) * 1.5)
        
        // Reward for leveling up
        addResources(energia: 20, pozioni: 2)
        
        logger.log("⬆️ Level up! Nuovo livello: \(gameState.livello)")
        
        // Play level up sound (not victory sound!)
        AudioManager.shared.playLevelUpSound()
        AudioManager.shared.hapticSuccess()
    }
    
    // MARK: - Audio System
    private func changeAreaMusic(_ area: String) {
        let musicFile: String
        
        switch area {
        case "Villaggio":
            musicFile = "villaggio"
        case "🏠 Cantina", "🚰 Fogne":
            musicFile = "underground"
        case "❄️ Area Innevata", "🏔️ Montagna Sacra":
            musicFile = "snow"
        case "🌿 Giungla Selvaggia", "🌲 Bosco Profondo":
            musicFile = "forest"
        case "🏚️ Casa degli Orrori", "⚰️ Cimitero":
            musicFile = "horror"
        case "🌊 Mare":
            musicFile = "ocean"
        case "🌋 Vulcano Attivo":
            musicFile = "volcano"
        case "👑 Palazzo Finale":
            musicFile = "final_boss"
        default:
            musicFile = "ambient"
        }
        
        playMusic(musicFile)
    }
    
    private func playMusic(_ filename: String) {
        guard audioEnabled else { return }
        AudioManager.shared.playMusic(filename)
    }
    
    private func playSound(_ filename: String) {
        guard audioEnabled else { return }
        AudioManager.shared.playSound(filename)
    }
    
    private func hapticFeedback(_ type: HapticType) {
        guard hapticEnabled else { return }
        switch type {
        case .light:
            AudioManager.shared.hapticFeedback(.light)
        case .medium:
            AudioManager.shared.hapticFeedback(.medium)
        case .heavy:
            AudioManager.shared.hapticFeedback(.heavy)
        }
    }
    
    // MARK: - Save/Load System
    func saveGame() {
        do {
            let data = try JSONEncoder().encode(gameState)
            UserDefaults.standard.set(data, forKey: "AvventuraEpicaSaveData")
            logger.log("💾 Gioco salvato")
        } catch {
            logger.log("❌ Errore nel salvare: \(error)")
        }
    }
    
    func loadGame() {
        guard let data = UserDefaults.standard.data(forKey: "AvventuraEpicaSaveData") else {
            logger.log("📁 Nessun salvataggio trovato, nuovo gioco")
            return
        }
        
        do {
            gameState = try JSONDecoder().decode(GameState.self, from: data)
            currentScreen = gameState.schermataCorrente
            logger.log("📂 Gioco caricato")
        } catch {
            logger.log("❌ Errore nel caricare: \(error)")
        }
    }
    
    func resetGame() {
        gameState = GameState()
        currentScreen = .mainMenu
        UserDefaults.standard.removeObject(forKey: "AvventuraEpicaSaveData")
        logger.log("🔄 Gioco resettato")
    }
    
    // MARK: - Data Setup
    private func setupMonsters() {
        // This would be populated with monster data from the original game
        logger.log("👹 Database mostri caricato")
    }
    
    private func setupEvolutions() {
        // This would be populated with evolution data
        logger.log("✨ Database evoluzioni caricato")
    }
    
    private func setupRelics() {
        // This would be populated with relic data
        logger.log("🔮 Database reliquie caricato")
    }
}

// MARK: - Helper Types
enum HapticType {
    case light
    case medium
    case heavy
}

class Logger {
    func log(_ message: String) {
        print("[\(Date())] \(message)")
    }
}