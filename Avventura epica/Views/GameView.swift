//
//  GameView.swift
//  Avventura epica
//
//  Created by Ambrogio Riili on 27/07/25.
//

import SwiftUI

struct GameView: View {
    @ObservedObject var gameManager: GameManager
    @State private var showingCombat = false
    @State private var actionMessage = ""
    @State private var showingActionMessage = false
    
    var body: some View {
        VStack(spacing: 20) {
            // Title - exactly as main.py
            Text("AVVENTURA IN CORSO")
                .font(.title)
                .fontWeight(.bold)
                .foregroundColor(.yellow)
                .padding(.top)
            
            ScrollView {
                VStack(spacing: 15) {
                    // Area Storia - like main.py
                    VStack(alignment: .leading, spacing: 10) {
                        Text("📜 Storia")
                            .font(.headline)
                            .foregroundColor(.yellow)
                        
                        Text(getStoryText())
                            .font(.body)
                            .foregroundColor(.yellow)
                            .padding()
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .background(Color.purple.opacity(0.8))
                            .cornerRadius(8)
                    }
                    
                    // Area Statistiche - like main.py
                    VStack(alignment: .leading, spacing: 10) {
                        Text("📊 Statistiche")
                            .font(.headline)
                            .foregroundColor(.blue)
                        
                        Text(getPlayerStats())
                            .font(.caption)
                            .foregroundColor(.white)
                            .padding()
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .background(Color.gray.opacity(0.8))
                            .cornerRadius(8)
                    }
                    
                    // Pulsanti Azioni - exactly as main.py order
                    VStack(spacing: 15) {
                        // Dynamic action buttons (green)
                        GameActionButton(
                            title: "🔍 Esplora Area",
                            color: .green,
                            width: 280,
                            height: 50
                        ) { exploreArea() }
                        
                        // Cambia Area (if multiple unlocked)
                        if gameManager.gameState.areeSbloccate.count > 1 {
                            GameActionButton(
                                title: "🗺️ Cambia Area", 
                                color: .blue,
                                width: 280,
                                height: 50
                            ) { gameManager.navigateToScreen(.areas) }
                        }
                        
                        // Main navigation buttons - exact order as main.py
                        GameActionButton(
                            title: "⚔️ Combattimento",
                            color: .red,
                            width: 280,
                            height: 50
                        ) { startCombat() }
                        
                        GameActionButton(
                            title: "🛒 Negozio",
                            color: .orange,
                            width: 280,
                            height: 50
                        ) { gameManager.navigateToScreen(.shop) }
                        
                        GameActionButton(
                            title: "🐱 Gatti",
                            color: .pink,
                            width: 280,
                            height: 50
                        ) { gameManager.navigateToScreen(.cats) }
                        
                        // Boss button if available
                        if shouldShowBossButton() {
                            GameActionButton(
                                title: "👑 Combatti Boss dell'Area!",
                                color: .purple,
                                width: 280,
                                height: 50
                            ) { startBossFight() }
                        }
                        
                        GameActionButton(
                            title: "💾 Salva Partita",
                            color: .purple,
                            width: 280,
                            height: 50
                        ) { gameManager.saveGame() }
                    }
                }
                .padding()
            }
            
            // Bottom back button - exactly as main.py
            Button("Torna al Menu") {
                gameManager.navigateToScreen(.mainMenu)
            }
            .frame(width: 200, height: 40)
            .background(Color.gray.opacity(0.6))
            .foregroundColor(.white)
            .cornerRadius(8)
            .padding(.bottom)
        }
        .background(areaBackground.ignoresSafeArea())
        .overlay(
            // Action message overlay
            VStack {
                if showingActionMessage {
                    Text(actionMessage)
                        .padding()
                        .background(Color.black.opacity(0.8))
                        .foregroundColor(.white)
                        .cornerRadius(10)
                        .transition(.scale.combined(with: .opacity))
                }
                Spacer()
            }
            .animation(.easeInOut(duration: 0.3), value: showingActionMessage)
        )
        .sheet(isPresented: $showingCombat) {
            CombatView(gameManager: gameManager)
        }
        .onChange(of: gameManager.isInCombat) { isInCombat in
            showingCombat = isInCombat
        }
    }
    
    @ViewBuilder
    private var areaBackground: some View {
        let area = gameManager.gameState.areaAttuale
        
        if area.contains("❄️") || area.contains("🏔️") {
            LinearGradient(
                gradient: Gradient(colors: [Color.blue.opacity(0.3), Color.white.opacity(0.2)]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
        } else if area.contains("🌿") || area.contains("🌲") {
            LinearGradient(
                gradient: Gradient(colors: [Color.green.opacity(0.3), Color.brown.opacity(0.2)]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
        } else if area.contains("🌊") {
            LinearGradient(
                gradient: Gradient(colors: [Color.blue.opacity(0.4), Color.cyan.opacity(0.2)]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
        } else if area.contains("🌋") {
            LinearGradient(
                gradient: Gradient(colors: [Color.red.opacity(0.4), Color.orange.opacity(0.2)]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
        } else if area.contains("🏚️") || area.contains("⚰️") {
            LinearGradient(
                gradient: Gradient(colors: [Color.purple.opacity(0.4), Color.black.opacity(0.3)]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
        } else {
            LinearGradient(
                gradient: Gradient(colors: [Color.blue.opacity(0.2), Color.green.opacity(0.2)]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
        }
    }
    
    private func showActionMessage(_ message: String) {
        actionMessage = message
        showingActionMessage = true
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            showingActionMessage = false
        }
    }
    
    private func getStoryText() -> String {
        return "Ti trovi nell'area: \(gameManager.gameState.areaAttuale)\n\nUn mondo misterioso ti circonda. I tuoi gatti magici sono pronti per l'avventura! Esplora l'area, combatti i nemici e scopri i segreti nascosti."
    }
    
    private func getPlayerStats() -> String {
        if let activeCat = gameManager.gameState.gatti[gameManager.gameState.gattoAttivo] {
            return """
            🎯 Livello: \(gameManager.gameState.livello) | EXP: \(gameManager.gameState.esperienza)/\(gameManager.gameState.esperienzaProssimoLivello)
            🐱 Gatto Attivo: \(activeCat.emoji) \(activeCat.nome) (Lv.\(activeCat.livello))
            ❤️ Vita: \(activeCat.fame)/100 | 😊 Felicità: \(activeCat.felicita)/100 | 💖 Affinità: \(activeCat.affinita)/250
            🍖 Cibo: \(gameManager.gameState.risorse.cibo) | 💧 Acqua: \(gameManager.gameState.risorse.acqua) | ⚡ Energia: \(gameManager.gameState.risorse.energia) | 💊 Pozioni: \(gameManager.gameState.risorse.pozioni)
            📍 Progresso Area: \(gameManager.gameState.progressioneArea[gameManager.gameState.areaAttuale] ?? 0)%
            """
        }
        return "Nessun gatto attivo"
    }
    
    private func exploreArea() {
        gameManager.increaseAreaProgress(10)
        gameManager.gainExperience(10)
        gameManager.addResources(cibo: 5, energia: -10)
        gameManager.increaseCatAffinity(gameManager.gameState.gattoAttivo)
        
        AudioManager.shared.playCatCollectSound()
        AudioManager.shared.playCollectItemSound()
        
        showActionMessage("🔍 Hai esplorato l'area e trovato risorse!")
    }
    
    private func startCombat() {
        gameManager.navigateToScreen(.game) // This will trigger combat in the combat view
        // The actual combat logic is handled in CombatView
    }
    
    private func shouldShowBossButton() -> Bool {
        let area = gameManager.gameState.areaAttuale
        let progress = gameManager.gameState.progressioneArea[area] ?? 0
        
        guard progress >= 100 else { return false }
        
        let bossName = getBossName(for: area)
        return bossName != nil && !gameManager.gameState.bossSconfitti.contains(bossName!)
    }
    
    private func getBossName(for area: String) -> String? {
        switch area {
        case "Villaggio": return "🐕 Cane Randagio"
        case "🏠 Cantina": return "🕷️ Regina dei Ragni"
        case "🚰 Fogne": return "🐀 Boss Topo delle Fogne"
        case "🌀 Labirinto Antico": return "🗿 Guardiano di Pietra"
        case "❄️ Area Innevata": return "🐺 Alpha del Branco"
        case "🌿 Giungla Selvaggia": return "🐍 Serpente Ancestrale"
        case "🌲 Bosco Profondo": return "🦌 Cervo Mistico"
        case "⚰️ Cimitero": return "💀 Lich Supremo"
        case "🏚️ Casa degli Orrori": return "👻 Spirito Maledetto"
        case "🏭 Fabbrica Abbandonata": return "🤖 Automa Corrotto"
        case "⛏️ Miniera Profonda": return "⛰️ Elementale di Terra"
        case "🌙 Cripta Maledetta": return "🧙‍♂️ Necromante Antico"
        case "🌊 Mare": return "🐙 Kraken Leggendario"
        case "🏔️ Montagna Sacra": return "🦅 Fenice Dorata"
        case "🌋 Vulcano Attivo": return "🔥 Drago di Magma"
        case "👑 Palazzo Finale": return "👑 Imperatore Oscuro"
        case "🌌 Regno degli Incubi": return "🌌 Signore degli Incubi"
        default: return nil
        }
    }
    
    private func startBossFight() {
        gameManager.startBossFight()
    }
}

// Game action button matching main.py specifications
struct GameActionButton: View {
    let title: String
    let color: Color
    let width: CGFloat
    let height: CGFloat
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.subheadline)
                .fontWeight(.semibold)
                .foregroundColor(.white)
                .frame(width: width, height: height)
                .background(color.opacity(0.8))
                .cornerRadius(8)
        }
        .buttonStyle(PlainButtonStyle())
    }
}

struct TopStatusBar: View {
    @ObservedObject var gameManager: GameManager
    
    var body: some View {
        HStack {
            // Back button
            Button(action: {
                gameManager.goBack()
            }) {
                Image(systemName: "chevron.left")
                    .font(.title2)
                    .foregroundColor(.primary)
            }
            
            Spacer()
            
            // Level and experience
            VStack(alignment: .trailing, spacing: 2) {
                Text("Lv. \(gameManager.gameState.livello)")
                    .font(.headline)
                    .fontWeight(.bold)
                
                ProgressView(
                    value: Double(gameManager.gameState.esperienza),
                    total: Double(gameManager.gameState.esperienzaProssimoLivello)
                )
                .frame(width: 100)
                .scaleEffect(0.8)
            }
        }
        .padding()
        .background(Color.black.opacity(0.1))
    }
}

struct AreaDisplayCard: View {
    @ObservedObject var gameManager: GameManager
    
    var body: some View {
        VStack(spacing: 15) {
            Text(gameManager.gameState.areaAttuale)
                .font(.title)
                .fontWeight(.bold)
                .multilineTextAlignment(.center)
            
            // Area progress
            VStack(spacing: 5) {
                Text("Progresso Area")
                    .font(.caption)
                    .foregroundColor(.secondary)
                
                let progress = gameManager.gameState.progressioneArea[gameManager.gameState.areaAttuale] ?? 0
                ProgressView(value: Double(progress), total: 100)
                    .frame(height: 8)
                
                Text("\(progress)/100")
                    .font(.caption2)
                    .foregroundColor(.secondary)
            }
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 15)
                .fill(Color.white.opacity(0.2))
                .overlay(
                    RoundedRectangle(cornerRadius: 15)
                        .stroke(Color.white.opacity(0.3), lineWidth: 1)
                )
        )
    }
}

struct ActiveCatCard: View {
    @ObservedObject var gameManager: GameManager
    
    var body: some View {
        if let activeCat = gameManager.gameState.gatti[gameManager.gameState.gattoAttivo] {
            VStack(spacing: 10) {
                HStack {
                    Text("\(activeCat.emoji) \(activeCat.nome)")
                        .font(.title2)
                        .fontWeight(.semibold)
                    
                    Spacer()
                    
                    Text("Lv. \(activeCat.livello)")
                        .font(.caption)
                        .padding(.horizontal, 8)
                        .padding(.vertical, 4)
                        .background(Color.blue.opacity(0.2))
                        .cornerRadius(8)
                }
                
                HStack {
                    // Health
                    VStack(alignment: .leading, spacing: 2) {
                        Text("❤️ Vita")
                            .font(.caption)
                        ProgressView(value: Double(activeCat.fame), total: 100)
                            .tint(.red)
                        Text("\(activeCat.fame)/100")
                            .font(.caption2)
                    }
                    
                    Spacer()
                    
                    // Happiness
                    VStack(alignment: .leading, spacing: 2) {
                        Text("😊 Felicità")
                            .font(.caption)
                        ProgressView(value: Double(activeCat.felicita), total: 100)
                            .tint(.yellow)
                        Text("\(activeCat.felicita)/100")
                            .font(.caption2)
                    }
                    
                    Spacer()
                    
                    // Affinity
                    VStack(alignment: .leading, spacing: 2) {
                        Text("💖 Affinità")
                            .font(.caption)
                        ProgressView(value: Double(activeCat.affinita), total: 250)
                            .tint(.pink)
                        Text("\(activeCat.affinita)/250")
                            .font(.caption2)
                    }
                }
                
                // Ability
                Text("Abilità: \(activeCat.abilita.description)")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            .padding()
            .background(
                RoundedRectangle(cornerRadius: 12)
                    .fill(Color.white.opacity(0.15))
                    .overlay(
                        RoundedRectangle(cornerRadius: 12)
                            .stroke(Color.white.opacity(0.3), lineWidth: 1)
                    )
            )
        }
    }
}

struct ActionButtonsGrid: View {
    @ObservedObject var gameManager: GameManager
    let onAction: (String) -> Void
    
    var body: some View {
        VStack(spacing: 20) {
            // Main actions
            LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 2), spacing: 15) {
                ActionButton(
                    title: "🔍 Esplora",
                    subtitle: "Cerca tesori e risorse",
                    color: .blue
                ) {
                    exploreArea()
                }
                
                ActionButton(
                    title: "⚔️ Combatti",
                    subtitle: "Affronta i nemici",
                    color: .red
                ) {
                    startCombat()
                }
                
                ActionButton(
                    title: "🍖 Raccogli Cibo",
                    subtitle: "Nutrire i tuoi gatti",
                    color: .green
                ) {
                    collectFood()
                }
                
                ActionButton(
                    title: "💊 Usa Pozione",
                    subtitle: "Cura il gatto attivo",
                    color: .purple
                ) {
                    usePotion()
                }
            }
            
            // Boss button if available
            if shouldShowBossButton() {
                ActionButton(
                    title: "👑 Combatti Boss",
                    subtitle: getBossButtonSubtitle(),
                    color: .red
                ) {
                    startBossFight()
                }
            }
            
            // Area shop button if available
            if shouldShowShopButton() {
                ActionButton(
                    title: "🏪 Negozio Locale",
                    subtitle: getShopButtonSubtitle(),
                    color: .mint
                ) {
                    openAreaShop()
                }
            }
            
            // Nutrition actions
            Text("🍽️ Nutrizione")
                .font(.headline)
                .fontWeight(.semibold)
                .foregroundColor(.secondary)
            
            LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 3), spacing: 10) {
                NutritionButton(
                    title: "🐱 Nutri",
                    subtitle: "Energia +50",
                    resource: gameManager.gameState.risorse.cibo,
                    cost: 5,
                    color: .orange
                ) {
                    nutriGatto()
                }
                
                NutritionButton(
                    title: "🍽️ Mangia",
                    subtitle: "HP +45",
                    resource: gameManager.gameState.risorse.cibo,
                    cost: 10,
                    color: .brown
                ) {
                    consumaCibo()
                }
                
                NutritionButton(
                    title: "💧 Bevi",
                    subtitle: "Felicità +10",
                    resource: gameManager.gameState.risorse.acqua,
                    cost: 5,
                    color: .cyan
                ) {
                    beviAcqua()
                }
            }
        }
    }
    
    private func exploreArea() {
        gameManager.increaseAreaProgress(10)
        gameManager.gainExperience(10)
        gameManager.addResources(cibo: 5, energia: -10)
        gameManager.increaseCatAffinity(gameManager.gameState.gattoAttivo)
        
        // Play exploration sounds
        AudioManager.shared.playCatCollectSound()
        AudioManager.shared.playCollectItemSound()
        
        onAction("🔍 Hai esplorato l'area e trovato risorse!")
    }
    
    private func startCombat() {
        // Check if player has enough energy
        let energyCheck = gameManager.canStartCombat()
        
        if !energyCheck.canFight {
            onAction(energyCheck.message)
            return
        }
        
        // Spend energy for combat
        if gameManager.spendResources(energia: 20) {
            // Create a random monster for this area
            let monster = createAreaMonster()
            gameManager.startCombat(with: monster)
        } else {
            onAction("❌ Energia insufficiente per combattere!")
        }
    }
    
    private func collectFood() {
        gameManager.addResources(cibo: 15, energia: -5)
        gameManager.increaseCatAffinity(gameManager.gameState.gattoAttivo, amount: 3)
        
        // Play food collection sounds
        AudioManager.shared.playCollectItemSound()
        AudioManager.shared.playEatingSound()
        
        onAction("🍖 Hai raccolto del cibo!")
    }
    
    private func usePotion() {
        if gameManager.gameState.risorse.pozioni > 0 {
            gameManager.useHealthPotion()
            onAction("💊 Pozione usata! Il tuo gatto si sente meglio.")
        } else {
            onAction("❌ Non hai pozioni!")
        }
    }
    
    private func nutriGatto() {
        let result = gameManager.nutriGatto()
        onAction(result.message)
    }
    
    private func consumaCibo() {
        let result = gameManager.consumaCibo()
        onAction(result.message)
    }
    
    private func beviAcqua() {
        let result = gameManager.beviAcqua()
        onAction(result.message)
    }
    
    private func shouldShowBossButton() -> Bool {
        let area = gameManager.gameState.areaAttuale
        let progress = gameManager.gameState.progressioneArea[area] ?? 0
        
        // Show boss button if:
        // 1. Area progress is 100%
        // 2. Area has a boss
        // 3. Boss is not defeated yet
        guard progress >= 100 else { return false }
        
        let bossName = getBossName(for: area)
        return bossName != nil && !gameManager.gameState.bossSconfitti.contains(bossName!)
    }
    
    private func getBossButtonSubtitle() -> String {
        let area = gameManager.gameState.areaAttuale
        return getBossName(for: area) ?? "Boss dell'Area"
    }
    
    private func getBossName(for area: String) -> String? {
        switch area {
        case "Villaggio": return "🐕 Cane Randagio"
        case "🏠 Cantina": return "🕷️ Regina dei Ragni"
        case "🚰 Fogne": return "🐀 Boss Topo delle Fogne"
        case "🌀 Labirinto Antico": return "🗿 Guardiano di Pietra"
        case "❄️ Area Innevata": return "🐺 Alpha del Branco"
        case "🌿 Giungla Selvaggia": return "🐍 Serpente Ancestrale"
        case "🌲 Bosco Profondo": return "🦌 Cervo Mistico"
        case "⚰️ Cimitero": return "💀 Lich Supremo"
        case "🏚️ Casa degli Orrori": return "👻 Spirito Maledetto"
        case "🏭 Fabbrica Abbandonata": return "🤖 Automa Corrotto"
        case "⛏️ Miniera Profonda": return "⛰️ Elementale di Terra"
        case "🌙 Cripta Maledetta": return "🧙‍♂️ Necromante Antico"
        case "🌊 Mare": return "🐙 Kraken Leggendario"
        case "🏔️ Montagna Sacra": return "🦅 Fenice Dorata"
        case "🌋 Vulcano Attivo": return "🔥 Drago di Magma"
        case "👑 Palazzo Finale": return "👑 Imperatore Oscuro"
        case "🌌 Regno degli Incubi": return "🌌 Signore degli Incubi"
        default: return nil
        }
    }
    
    private func startBossFight() {
        gameManager.startBossFight()
    }
    
    private func shouldShowShopButton() -> Bool {
        return gameManager.hasShop(gameManager.gameState.areaAttuale)
    }
    
    private func getShopButtonSubtitle() -> String {
        switch gameManager.gameState.areaAttuale {
        case "Villaggio": return "Materiali di Legno"
        case "🏠 Cantina": return "Materiali di Pietra"
        case "🚰 Fogne": return "Materiali di Rame"
        case "🌀 Labirinto Antico": return "Materiali di Bronzo"
        case "❄️ Area Innevata": return "Materiali di Ferro"
        case "🌿 Giungla Selvaggia": return "Materiali d'Acciaio"
        case "🌲 Bosco Profondo": return "Acciaio Temprato"
        case "⚰️ Cimitero": return "Materiali d'Argento"
        case "🏚️ Casa degli Orrori": return "Materiali d'Oro"
        case "🏭 Fabbrica Abbandonata": return "Materiali di Platino"
        case "⛏️ Miniera Profonda": return "Materiali di Titanio"
        case "🌙 Cripta Maledetta": return "Materiali d'Ossidiana"
        case "🌊 Mare": return "Materiali di Diamante"
        case "🏔️ Montagna Sacra": return "Materiali di Mithril"
        case "🌋 Vulcano Attivo": return "Cristalli Runici"
        case "👑 Palazzo Finale": return "Essenza Divina"
        case "🌌 Regno degli Incubi": return "Scaglie di Drago"
        default: return "Negozio Locale"
        }
    }
    
    private func openAreaShop() {
        gameManager.navigateToScreen(.shop)
    }
    
    private func createAreaMonster() -> Monster {
        return gameManager.getRandomMonsterForArea(gameManager.gameState.areaAttuale)
    }
}

struct ActionButton: View {
    let title: String
    let subtitle: String
    let color: Color
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            VStack(spacing: 8) {
                Text(title)
                    .font(.headline)
                    .fontWeight(.semibold)
                    .multilineTextAlignment(.center)
                
                Text(subtitle)
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
            }
            .frame(maxWidth: .infinity)
            .frame(height: 80)
            .padding()
            .background(
                RoundedRectangle(cornerRadius: 12)
                    .fill(color.opacity(0.1))
                    .overlay(
                        RoundedRectangle(cornerRadius: 12)
                            .stroke(color.opacity(0.3), lineWidth: 1)
                    )
            )
        }
        .buttonStyle(PlainButtonStyle())
    }
}

struct BottomNavigationBar: View {
    @ObservedObject var gameManager: GameManager
    
    var body: some View {
        HStack {
            // Resources display
            HStack(spacing: 15) {
                ResourceDisplay(icon: "🍖", value: gameManager.gameState.risorse.cibo)
                ResourceDisplay(icon: "💧", value: gameManager.gameState.risorse.acqua)
                ResourceDisplay(icon: "⚡", value: gameManager.gameState.risorse.energia)
                ResourceDisplay(icon: "💊", value: gameManager.gameState.risorse.pozioni)
            }
            
            Spacer()
            
            // Menu button
            Button("Menu") {
                gameManager.navigateToScreen(.mainMenu)
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 8)
            .background(Color.blue.opacity(0.2))
            .cornerRadius(8)
        }
        .padding()
        .background(Color.black.opacity(0.1))
    }
}

struct ResourceDisplay: View {
    let icon: String
    let value: Int
    
    var body: some View {
        VStack(spacing: 2) {
            Text(icon)
                .font(.caption)
            Text("\(value)")
                .font(.caption2)
                .fontWeight(.medium)
        }
    }
}

struct NutritionButton: View {
    let title: String
    let subtitle: String
    let resource: Int
    let cost: Int
    let color: Color
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            VStack(spacing: 6) {
                Text(title)
                    .font(.subheadline)
                    .fontWeight(.semibold)
                    .multilineTextAlignment(.center)
                
                Text(subtitle)
                    .font(.caption2)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
                
                Text("\(resource)/\(cost)")
                    .font(.caption2)
                    .fontWeight(.bold)
                    .foregroundColor(resource >= cost ? .green : .red)
            }
            .frame(maxWidth: .infinity)
            .frame(height: 70)
            .padding(.horizontal, 8)
            .padding(.vertical, 6)
            .background(
                RoundedRectangle(cornerRadius: 10)
                    .fill(color.opacity(0.1))
                    .overlay(
                        RoundedRectangle(cornerRadius: 10)
                            .stroke(color.opacity(0.3), lineWidth: 1)
                    )
            )
        }
        .buttonStyle(PlainButtonStyle())
        .disabled(resource < cost)
        .opacity(resource >= cost ? 1.0 : 0.6)
    }
}

#Preview {
    GameView(gameManager: GameManager())
}