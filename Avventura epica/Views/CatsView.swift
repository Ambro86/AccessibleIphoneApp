//
//  CatsView.swift
//  Avventura epica
//
//  Created by Ambrogio Riili on 27/07/25.
//

import SwiftUI

struct CatsView: View {
    @ObservedObject var gameManager: GameManager
    @State private var selectedCat: String?
    @State private var showingRenameAlert = false
    @State private var newCatName = ""
    
    var body: some View {
        VStack(spacing: 20) {
            // Title - exactly as main.py
            Text("Gestione Gatti")
                .font(.title)
                .fontWeight(.bold)
                .foregroundColor(.pink)
                .padding(.top)
            
            // Subtitle - exactly as main.py
            Text("Scegli il tuo gatto attivo tra quelli disponibili")
                .font(.subheadline)
                .foregroundColor(.gray)
                .multilineTextAlignment(.center)
                .padding(.horizontal)
            
            ScrollView {
                VStack(spacing: 15) {
                    // Lista Gatti - exactly as main.py (Container height=400)
                    VStack(spacing: 15) {
                        ForEach(Array(gameManager.gameState.gatti.keys.sorted()), id: \.self) { catId in
                            if let cat = gameManager.gameState.gatti[catId] {
                                CatListItem(
                                    cat: cat,
                                    catId: catId,
                                    isActive: catId == gameManager.gameState.gattoAttivo,
                                    onSelect: {
                                        if cat.sbloccato {
                                            gameManager.selectActiveCat(catId)
                                        }
                                    }
                                )
                            }
                        }
                    }
                    .frame(maxHeight: 400) // Like main.py
                    
                    // Pulsanti Azioni - exactly as main.py (if active cat available)
                    if let activeCat = gameManager.gameState.gatti[gameManager.gameState.gattoAttivo], activeCat.sbloccato {
                        VStack(spacing: 15) {
                            // Rinomina Gatto Attivo (purple, 250x50px)
                            GameActionButton(
                                title: "Rinomina Gatto Attivo",
                                color: .purple,
                                width: 250,
                                height: 50
                            ) {
                                selectedCat = gameManager.gameState.gattoAttivo
                                newCatName = activeCat.nome
                                showingRenameAlert = true
                            }
                            
                            // Gestisci Reliquie (amber, 250x50px)
                            GameActionButton(
                                title: "Gestisci Reliquie",
                                color: .yellow,
                                width: 250,
                                height: 50
                            ) {
                                // Implementa gestione reliquie se necessario
                                // gameManager.navigateToScreen(.relics)
                            }
                        }
                    }
                }
                .padding()
            }
            
            // Pulsante Indietro - bottom
            Button("Indietro") {
                gameManager.navigateToScreen(.mainMenu)
            }
            .frame(width: 200, height: 40)
            .background(Color.gray.opacity(0.6))
            .foregroundColor(.white)
            .cornerRadius(8)
            .padding(.bottom)
        }
        .background(
            LinearGradient(
                gradient: Gradient(colors: [Color.pink.opacity(0.1), Color.orange.opacity(0.1)]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()
        )
        .alert("Rinomina Gatto", isPresented: $showingRenameAlert) {
            TextField("Nome del gatto", text: $newCatName)
            Button("Annulla", role: .cancel) { }
            Button("Salva") {
                if let catId = selectedCat, !newCatName.isEmpty {
                    gameManager.gameState.gatti[catId]?.nome = newCatName
                    gameManager.gameState.gatti[catId]?.nomePersonalizzato = true
                    gameManager.saveGame()
                }
            }
        } message: {
            Text("Inserisci un nuovo nome per il tuo gatto")
        }
    }
}

// Cat list item exactly as main.py layout
struct CatListItem: View {
    let cat: Cat
    let catId: String
    let isActive: Bool
    let onSelect: () -> Void
    
    var body: some View {
        VStack(spacing: 10) {
            // Emoji + Nome (size=18, bold, centrato)
            Text("\(cat.emoji) \(cat.nome)")
                .font(.system(size: 18))
                .fontWeight(.bold)
                .multilineTextAlignment(.center)
            
            if cat.sbloccato {
                // "Livello: X | Abilità: Y" (size=14, centrato)
                Text("Livello: \(cat.livello) | Abilità: \(cat.abilita.description)")
                    .font(.system(size: 14))
                    .multilineTextAlignment(.center)
                    .foregroundColor(.primary)
                
                // "Affinità: X/100 | Felicità: Y/100" (size=12, centrato)
                Text("Affinità: \(cat.affinita)/250 | Felicità: \(cat.felicita)/100")
                    .font(.system(size: 12))
                    .multilineTextAlignment(.center)
                    .foregroundColor(.secondary)
                
                // Pulsante "ATTIVO" (GREEN_600, disabled) o "Seleziona" (BLUE_600)
                if isActive {
                    Text("ATTIVO")
                        .font(.subheadline)
                        .fontWeight(.semibold)
                        .foregroundColor(.white)
                        .frame(width: 120, height: 40)
                        .background(Color.green.opacity(0.8))
                        .cornerRadius(8)
                } else {
                    Button("Seleziona") {
                        onSelect()
                    }
                    .font(.subheadline)
                    .fontWeight(.semibold)
                    .foregroundColor(.white)
                    .frame(width: 120, height: 40)
                    .background(Color.blue.opacity(0.8))
                    .cornerRadius(8)
                }
            } else {
                Text("🔒 Bloccato")
                    .font(.system(size: 14))
                    .foregroundColor(.gray)
                
                Text("Progredisci nel gioco per sbloccare")
                    .font(.system(size: 12))
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
            }
        }
        .padding(15)
        .frame(maxWidth: .infinity)
        .background(Color.gray.opacity(0.8)) // GREY_800 like main.py
        .cornerRadius(12)
    }
}

struct ActiveCatDisplayCard: View {
    let cat: Cat
    
    var body: some View {
        HStack(spacing: 15) {
            Text(cat.emoji)
                .font(.system(size: 40))
            
            VStack(alignment: .leading, spacing: 5) {
                Text(cat.nome)
                    .font(.title2)
                    .fontWeight(.bold)
                
                Text("Lv. \(cat.livello) • \(cat.abilita.description)")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                
                HStack {
                    Text("❤️ \(cat.fame)")
                    Text("😊 \(cat.felicita)")
                    Text("💖 \(cat.affinita)")
                }
                .font(.caption)
            }
            
            Spacer()
            
            if cat.formaEvoluta {
                Text("✨")
                    .font(.title)
            }
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 12)
                .fill(Color.blue.opacity(0.1))
                .overlay(
                    RoundedRectangle(cornerRadius: 12)
                        .stroke(Color.blue.opacity(0.3), lineWidth: 2)
                )
        )
    }
}

struct CatCard: View {
    let cat: Cat
    let isActive: Bool
    let onSelect: () -> Void
    let onRename: () -> Void
    let onEvolve: () -> Void
    
    var body: some View {
        VStack(spacing: 12) {
            // Cat emoji and status
            ZStack {
                Text(cat.emoji)
                    .font(.system(size: 40))
                
                if !cat.sbloccato {
                    Rectangle()
                        .fill(Color.black.opacity(0.7))
                        .cornerRadius(8)
                    
                    Text("🔒")
                        .font(.title)
                        .foregroundColor(.white)
                }
                
                if cat.formaEvoluta {
                    VStack {
                        HStack {
                            Spacer()
                            Text("✨")
                                .font(.title2)
                        }
                        Spacer()
                    }
                }
            }
            .frame(height: 60)
            
            // Cat info
            VStack(spacing: 5) {
                Text(cat.nome)
                    .font(.headline)
                    .fontWeight(.semibold)
                    .foregroundColor(isActive ? .blue : .primary)
                
                if cat.sbloccato {
                    Text("Lv. \(cat.livello)")
                        .font(.caption)
                        .foregroundColor(.secondary)
                    
                    Text(cat.abilita.description)
                        .font(.caption2)
                        .foregroundColor(.secondary)
                        .multilineTextAlignment(.center)
                    
                    // Stats bars
                    VStack(spacing: 3) {
                        StatBar(label: "❤️", value: cat.fame, maxValue: 100, color: .red)
                        StatBar(label: "😊", value: cat.felicita, maxValue: 100, color: .yellow)
                        StatBar(label: "💖", value: cat.affinita, maxValue: 250, color: .pink)
                    }
                } else {
                    Text("Bloccato")
                        .font(.caption)
                        .foregroundColor(.secondary)
                    
                    Text("Progredisci nel gioco per sbloccare")
                        .font(.caption2)
                        .foregroundColor(.secondary)
                        .multilineTextAlignment(.center)
                }
            }
            
            // Action buttons
            if cat.sbloccato {
                VStack(spacing: 8) {
                    if !isActive {
                        Button("Seleziona") {
                            onSelect()
                        }
                        .font(.caption)
                        .padding(.horizontal, 12)
                        .padding(.vertical, 4)
                        .background(Color.blue.opacity(0.2))
                        .cornerRadius(6)
                    } else {
                        Text("Attivo")
                            .font(.caption)
                            .fontWeight(.semibold)
                            .foregroundColor(.blue)
                    }
                    
                    HStack(spacing: 8) {
                        Button("Rinomina") {
                            onRename()
                        }
                        .font(.caption2)
                        .padding(.horizontal, 8)
                        .padding(.vertical, 3)
                        .background(Color.gray.opacity(0.2))
                        .cornerRadius(4)
                        
                        if cat.affinita >= 200 && !cat.formaEvoluta {
                            Button("Evolvi") {
                                onEvolve()
                            }
                            .font(.caption2)
                            .padding(.horizontal, 8)
                            .padding(.vertical, 3)
                            .background(Color.purple.opacity(0.2))
                            .cornerRadius(4)
                        }
                    }
                }
            }
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 12)
                .fill(isActive ? Color.blue.opacity(0.1) : Color.white.opacity(0.1))
                .overlay(
                    RoundedRectangle(cornerRadius: 12)
                        .stroke(isActive ? Color.blue.opacity(0.5) : Color.gray.opacity(0.3), lineWidth: isActive ? 2 : 1)
                )
        )
        .scaleEffect(isActive ? 1.02 : 1.0)
        .animation(.easeInOut(duration: 0.2), value: isActive)
    }
}

struct StatBar: View {
    let label: String
    let value: Int
    let maxValue: Int
    let color: Color
    
    var body: some View {
        HStack(spacing: 4) {
            Text(label)
                .font(.caption2)
            
            ProgressView(value: Double(value), total: Double(maxValue))
                .tint(color)
                .frame(height: 4)
            
            Text("\(value)")
                .font(.caption2)
                .frame(width: 25, alignment: .trailing)
        }
    }
}

struct EvolutionInfoSection: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("✨ Informazioni Evoluzione")
                .font(.headline)
                .fontWeight(.bold)
            
            VStack(alignment: .leading, spacing: 8) {
                EvolutionTip(icon: "💖", text: "Raggiungi 200 affinità per sbloccare l'evoluzione")
                EvolutionTip(icon: "⭐", text: "I gatti evoluti ottengono abilità speciali")
                EvolutionTip(icon: "🎯", text: "Usa i gatti in battaglia per aumentare l'affinità")
                EvolutionTip(icon: "🏆", text: "I gatti evoluti sono più forti in combattimento")
            }
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 12)
                .fill(Color.purple.opacity(0.1))
                .overlay(
                    RoundedRectangle(cornerRadius: 12)
                        .stroke(Color.purple.opacity(0.3), lineWidth: 1)
                )
        )
    }
}

struct EvolutionTip: View {
    let icon: String
    let text: String
    
    var body: some View {
        HStack(spacing: 10) {
            Text(icon)
                .font(.subheadline)
            
            Text(text)
                .font(.caption)
                .foregroundColor(.secondary)
            
            Spacer()
        }
    }
}

#Preview {
    CatsView(gameManager: GameManager())
}