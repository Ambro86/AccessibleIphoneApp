//
//  CombatView.swift
//  Avventura epica
//
//  Created by Ambrogio Riili on 27/07/25.
//

import SwiftUI

struct CombatView: View {
    @ObservedObject var gameManager: GameManager
    @Environment(\.dismiss) var dismiss
    @State private var combatLog: [String] = []
    @State private var showingVictory = false
    @State private var showingDefeat = false
    
    var body: some View {
        VStack(spacing: 15) {
            // Title - exactly as main.py
            Text("Arena di Combattimento")
                .font(.title)
                .fontWeight(.bold)
                .foregroundColor(.red)
                .padding(.top)
            
            ScrollView {
                VStack(spacing: 20) {
                    // Debug widget info (like main.py)
                    if let activeCat = gameManager.gameState.gatti[gameManager.gameState.gattoAttivo] {
                        HStack {
                            Text("🎯 Lv.\(gameManager.gameState.livello)")
                            Spacer()
                            Text("❤️ \(activeCat.fame)/100")
                            Spacer()
                            if let monster = gameManager.currentMonster {
                                Text("👹 \(monster.nome): \(gameManager.monsterCurrentHP)/\(monster.hp)")
                            }
                        }
                        .font(.caption)
                        .foregroundColor(.white)
                        .padding(.horizontal)
                    }
                    
                    // Sezione Combattenti (Player VS Monster) - horizontal layout like main.py
                    if let activeCat = gameManager.gameState.gatti[gameManager.gameState.gattoAttivo],
                       let monster = gameManager.currentMonster {
                        HStack(spacing: 30) {
                            // Player (left)
                            VStack {
                                Text(activeCat.emoji)
                                    .font(.system(size: 40))
                                Text(activeCat.nome)
                                    .font(.headline)
                                Text("❤️ \(activeCat.fame)/100")
                                    .font(.caption)
                                    .foregroundColor(.green)
                            }
                            
                            // VS
                            Text("VS")
                                .font(.title2)
                                .fontWeight(.bold)
                                .foregroundColor(.yellow)
                            
                            // Monster (right)
                            VStack {
                                Text(monster.emoji)
                                    .font(.system(size: 40))
                                Text(monster.nome)
                                    .font(.headline)
                                Text("❤️ \(gameManager.monsterCurrentHP)/\(monster.hp)")
                                    .font(.caption)
                                    .foregroundColor(.red)
                            }
                        }
                        .padding()
                        .background(Color.black.opacity(0.3))
                        .cornerRadius(12)
                    }
                    
                    // Storia del Combattimento - exactly as main.py (height=160)
                    VStack(alignment: .leading, spacing: 5) {
                        Text("📜 Storia del Combattimento")
                            .font(.headline)
                            .foregroundColor(.yellow)
                        
                        ScrollView {
                            LazyVStack(alignment: .leading, spacing: 3) {
                                ForEach(combatLog.indices, id: \.self) { index in
                                    Text(combatLog[index])
                                        .font(.caption)
                                        .foregroundColor(.white)
                                }
                            }
                        }
                        .frame(height: 160)
                        .padding(8)
                        .background(Color.black.opacity(0.5))
                        .cornerRadius(8)
                    }
                    
                    // Azioni di Combattimento - 2x3 grid exactly as main.py
                    VStack(spacing: 15) {
                        Text("⚔️ Azioni")
                            .font(.headline)
                            .foregroundColor(.red)
                        
                        LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 2), spacing: 15) {
                            CombatGridButton(title: "🔍 Cerca Mostri", color: .orange) {
                                searchForMonsters()
                            }
                            
                            CombatGridButton(title: "⚔️ Attacca", color: .red, disabled: gameManager.isAutoCombat) {
                                performAttack()
                            }
                            
                            CombatGridButton(title: "🛡️ Difendi", color: .blue, disabled: gameManager.isAutoCombat) {
                                performDefend()
                            }
                            
                            CombatGridButton(title: "🩹 Cura", color: gameManager.gameState.risorse.pozioni > 0 ? .green : .gray, disabled: gameManager.isAutoCombat || gameManager.gameState.risorse.pozioni == 0) {
                                usePotion()
                            }
                            
                            CombatGridButton(title: "🏃 Fuggi", color: .purple, disabled: gameManager.isAutoCombat) {
                                fleeCombat()
                            }
                            
                            CombatGridButton(title: gameManager.isAutoCombat ? "🛑 Stop Auto" : "🤖 Auto", color: gameManager.isAutoCombat ? .gray : .yellow) {
                                toggleAutoCombat()
                            }
                        }
                        .frame(height: 200) // Like main.py
                    }
                    
                    // Navigazione rapida - exactly as main.py (3 buttons, 90x45px)
                    VStack(spacing: 10) {
                        Text("🧭 Navigazione")
                            .font(.subheadline)
                            .foregroundColor(.cyan)
                        
                        HStack(spacing: 15) {
                            NavigationButton(title: "🎮 Gioco", color: .blue, width: 90, height: 45) {
                                dismiss()
                            }
                            
                            NavigationButton(title: "🐱 Gatti", color: .pink, width: 90, height: 45) {
                                gameManager.navigateToScreen(.cats)
                                dismiss()
                            }
                            
                            NavigationButton(title: "🛒 Shop", color: .orange, width: 90, height: 45) {
                                gameManager.navigateToScreen(.shop)
                                dismiss()
                            }
                        }
                    }
                }
                .padding()
            }
        }
        .background(
            LinearGradient(
                gradient: Gradient(colors: [Color.red.opacity(0.3), Color.black.opacity(0.5)]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()
        )
        .navigationBarHidden(true)
        .alert("🏆 Vittoria!", isPresented: $showingVictory) {
            Button("Continua") {
                dismiss()
            }
        } message: {
            Text("Hai sconfitto il nemico e ottenuto ricompense!")
        }
        .alert("💀 Sconfitta!", isPresented: $showingDefeat) {
            Button("Riprova") {
                dismiss()
            }
        } message: {
            Text("Il tuo gatto è stato sconfitto. Usa una pozione e riprova!")
        }
    }
    
    private func performAttack() {
        // Play cat attack sound
        AudioManager.shared.playCatAttackSound()
        
        let result = gameManager.performAttack()
        
        let playerDamageText = "🗡️ Hai inflitto \(result.playerDamage) danni!"
        combatLog.append(playerDamageText)
        
        if result.playerWins {
            combatLog.append("🏆 Nemico sconfitto!")
            showingVictory = true
        } else if result.monsterDamage > 0 {
            let monsterDamageText = "💥 Hai subito \(result.monsterDamage) danni!"
            combatLog.append(monsterDamageText)
            
            if result.monsterWins {
                combatLog.append("💀 Il tuo gatto è stato sconfitto!")
                showingDefeat = true
            }
        }
        
        // Keep only last 6 messages
        if combatLog.count > 6 {
            combatLog.removeFirst()
        }
    }
    
    private func performDefend() {
        // Implement defend logic
        combatLog.append("🛡️ Ti sei messo in difesa!")
        if combatLog.count > 6 {
            combatLog.removeFirst()
        }
    }
    
    private func usePotion() {
        if gameManager.useCombatPotion() {
            combatLog.append("💊 Hai usato una pozione! +50 HP")
        } else {
            combatLog.append("❌ Non puoi usare pozioni!")
        }
        
        if combatLog.count > 6 {
            combatLog.removeFirst()
        }
    }
    
    private func useFood() {
        if gameManager.useCombatFood() {
            combatLog.append("🍖 Hai usato del cibo! +15 HP")
        } else {
            combatLog.append("❌ Non puoi usare cibo!")
        }
        
        if combatLog.count > 6 {
            combatLog.removeFirst()
        }
    }
    
    private func useWater() {
        if gameManager.useCombatWater() {
            combatLog.append("💧 Hai bevuto acqua! +10 HP")
        } else {
            combatLog.append("❌ Non puoi bere acqua!")
        }
        
        if combatLog.count > 6 {
            combatLog.removeFirst()
        }
    }
    
    private func toggleAutoCombat() {
        gameManager.toggleAutoCombat()
        
        if gameManager.isAutoCombat {
            combatLog.append("🤖 Auto-combattimento attivato!")
        } else {
            combatLog.append("🛑 Auto-combattimento disattivato!")
        }
        
        if combatLog.count > 6 {
            combatLog.removeFirst()
        }
    }
    
    private func searchForMonsters() {
        let monster = gameManager.getRandomMonsterForArea(gameManager.gameState.areaAttuale)
        gameManager.startCombat(with: monster)
        combatLog.append("🔍 Hai trovato: \(monster.nome)!")
        
        if combatLog.count > 6 {
            combatLog.removeFirst()
        }
    }
    
    private func fleeCombat() {
        combatLog.append("🏃 Sei fuggito dal combattimento!")
        dismiss()
        
        if combatLog.count > 6 {
            combatLog.removeFirst()
        }
    }
}

struct MonsterCard: View {
    let monster: Monster
    let currentHP: Int
    
    var body: some View {
        VStack(spacing: 15) {
            Text(monster.emoji)
                .font(.system(size: 60))
            
            Text(monster.nome)
                .font(.title2)
                .fontWeight(.bold)
            
            // Monster HP bar
            VStack(spacing: 5) {
                Text("❤️ \(currentHP) / \(monster.hp)")
                    .font(.headline)
                    .foregroundColor(.red)
                
                ProgressView(value: Double(currentHP), total: Double(monster.hp))
                    .tint(.red)
                    .frame(height: 12)
            }
            
            Text("⚔️ Attacco: \(monster.attacco)")
                .font(.subheadline)
                .foregroundColor(.secondary)
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 15)
                .fill(Color.red.opacity(0.1))
                .overlay(
                    RoundedRectangle(cornerRadius: 15)
                        .stroke(Color.red.opacity(0.3), lineWidth: 2)
                )
        )
    }
}

struct CatCombatCard: View {
    let cat: Cat
    
    var body: some View {
        VStack(spacing: 15) {
            Text(cat.emoji)
                .font(.system(size: 50))
            
            Text(cat.nome)
                .font(.title3)
                .fontWeight(.semibold)
            
            // Cat HP bar
            VStack(spacing: 5) {
                Text("❤️ \(cat.fame) / 100")
                    .font(.subheadline)
                    .foregroundColor(.green)
                
                ProgressView(value: Double(cat.fame), total: 100)
                    .tint(.green)
                    .frame(height: 8)
            }
            
            HStack {
                Text("⚔️ \(cat.attacco)")
                    .font(.caption)
                Spacer()
                Text("🎯 \(cat.abilita.description)")
                    .font(.caption)
            }
            .foregroundColor(.secondary)
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 12)
                .fill(Color.blue.opacity(0.1))
                .overlay(
                    RoundedRectangle(cornerRadius: 12)
                        .stroke(Color.blue.opacity(0.3), lineWidth: 1)
                )
        )
    }
}

struct CombatLogView: View {
    let combatLog: [String]
    
    var body: some View {
        VStack(alignment: .leading, spacing: 5) {
            Text("📜 Log Combattimento")
                .font(.headline)
                .fontWeight(.semibold)
            
            ScrollView {
                LazyVStack(alignment: .leading, spacing: 3) {
                    ForEach(combatLog.indices, id: \.self) { index in
                        Text(combatLog[index])
                            .font(.caption)
                            .foregroundColor(.primary)
                    }
                }
            }
            .frame(maxHeight: 100)
            .padding(.horizontal, 10)
            .padding(.vertical, 8)
            .background(
                RoundedRectangle(cornerRadius: 8)
                    .fill(Color.black.opacity(0.2))
            )
        }
    }
}

struct CombatActionButtons: View {
    @ObservedObject var gameManager: GameManager
    let onAttack: () -> Void
    let onDefend: () -> Void
    let onUsePotion: () -> Void
    let onUseFood: () -> Void
    let onUseWater: () -> Void
    let onToggleAuto: () -> Void
    
    var body: some View {
        VStack(spacing: 15) {
            // Main combat actions
            HStack(spacing: 15) {
                CombatButton(
                    title: "⚔️ Attacca",
                    color: .red,
                    action: onAttack,
                    disabled: gameManager.isAutoCombat
                )
                
                CombatButton(
                    title: "🛡️ Difendi", 
                    color: .blue,
                    action: onDefend,
                    disabled: gameManager.isAutoCombat
                )
                
                CombatButton(
                    title: gameManager.isAutoCombat ? "🛑 Stop Auto" : "🤖 Auto",
                    color: gameManager.isAutoCombat ? .gray : .orange,
                    action: onToggleAuto
                )
            }
            
            // Healing items
            HStack(spacing: 10) {
                CombatItemButton(
                    title: "💊",
                    subtitle: "\(gameManager.gameState.risorse.pozioni)",
                    color: .purple,
                    action: onUsePotion,
                    available: gameManager.gameState.risorse.pozioni > 0,
                    disabled: gameManager.isAutoCombat
                )
                
                CombatItemButton(
                    title: "🍖",
                    subtitle: "\(gameManager.gameState.risorse.cibo)",
                    color: .brown,
                    action: onUseFood,
                    available: gameManager.gameState.risorse.cibo > 0,
                    disabled: gameManager.isAutoCombat
                )
                
                CombatItemButton(
                    title: "💧",
                    subtitle: "\(gameManager.gameState.risorse.acqua)",
                    color: .cyan,
                    action: onUseWater,
                    available: gameManager.gameState.risorse.acqua > 0,
                    disabled: gameManager.isAutoCombat
                )
            }
            
            if gameManager.isAutoCombat {
                Text("🤖 Combattimento automatico attivo")
                    .font(.caption)
                    .foregroundColor(.orange)
                    .fontWeight(.semibold)
            }
        }
    }
}

struct CombatButton: View {
    let title: String
    let color: Color
    let action: () -> Void
    var disabled: Bool = false
    
    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.subheadline)
                .fontWeight(.semibold)
                .foregroundColor(.white)
                .frame(maxWidth: .infinity)
                .padding(.vertical, 12)
                .background(
                    RoundedRectangle(cornerRadius: 8)
                        .fill(disabled ? Color.gray : color)
                )
        }
        .disabled(disabled)
        .opacity(disabled ? 0.6 : 1.0)
    }
}

struct CombatItemButton: View {
    let title: String
    let subtitle: String
    let color: Color
    let action: () -> Void
    let available: Bool
    var disabled: Bool = false
    
    var body: some View {
        Button(action: action) {
            VStack(spacing: 2) {
                Text(title)
                    .font(.title3)
                
                Text(subtitle)
                    .font(.caption2)
                    .fontWeight(.bold)
            }
            .foregroundColor(.white)
            .frame(width: 60, height: 50)
            .background(
                RoundedRectangle(cornerRadius: 8)
                    .fill(available && !disabled ? color : Color.gray)
            )
        }
        .disabled(!available || disabled)
        .opacity(!available || disabled ? 0.5 : 1.0)
    }
}

// Combat grid button matching main.py 2x3 grid
struct CombatGridButton: View {
    let title: String
    let color: Color
    var disabled: Bool = false
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.subheadline)
                .fontWeight(.semibold)
                .foregroundColor(.white)
                .frame(maxWidth: .infinity)
                .frame(height: 50)
                .background(disabled ? Color.gray : color.opacity(0.8))
                .cornerRadius(8)
        }
        .disabled(disabled)
        .opacity(disabled ? 0.6 : 1.0)
        .buttonStyle(PlainButtonStyle())
    }
}

// Navigation button matching main.py specs (90x45px)
struct NavigationButton: View {
    let title: String
    let color: Color
    let width: CGFloat
    let height: CGFloat
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.caption)
                .fontWeight(.semibold)
                .foregroundColor(.white)
                .frame(width: width, height: height)
                .background(color.opacity(0.8))
                .cornerRadius(6)
        }
        .buttonStyle(PlainButtonStyle())
    }
}

#Preview {
    CombatView(gameManager: GameManager())
}