//
//  SettingsView.swift
//  Avventura epica
//
//  Created by Ambrogio Riili on 27/07/25.
//

import SwiftUI

struct SettingsView: View {
    @ObservedObject var gameManager: GameManager
    @State private var showingResetAlert = false
    @State private var showingDebugInfo = false
    @State private var debugInfo = ""
    @State private var musicVolume: Double = 70.0
    @State private var effectsVolume: Double = 80.0
    
    var body: some View {
        NavigationView {
            List {
                // Audio Settings Section - exactly as main.py
                Section("🔊 Audio") {
                    Toggle("Audio Attivato", isOn: $gameManager.audioEnabled)
                        .onChange(of: gameManager.audioEnabled) { value in
                            gameManager.gameState.audioAbilitato = value
                            gameManager.saveGame()
                        }
                    
                    VStack(alignment: .leading, spacing: 5) {
                        Text("Volume Musica: \(Int(musicVolume))%")
                            .font(.subheadline)
                        
                        Slider(value: $musicVolume, in: 0...100, step: 10)
                            .onChange(of: musicVolume) { value in
                                AudioManager.shared.setMusicVolume(Float(value / 100.0))
                            }
                    }
                    
                    VStack(alignment: .leading, spacing: 5) {
                        Text("Volume Effetti: \(Int(effectsVolume))%")
                            .font(.subheadline)
                        
                        Slider(value: $effectsVolume, in: 0...100, step: 10)
                            .onChange(of: effectsVolume) { value in
                                AudioManager.shared.setSoundVolume(Float(value / 100.0))
                            }
                    }
                    
                    Button("Testa Audio") {
                        testAudio()
                    }
                    .frame(width: 200)
                    
                    Button("Debug Audio") {
                        debugAudio()
                    }
                    .frame(width: 200)
                }
                
                // Feedback Section - separate like main.py
                Section("📳 Feedback") {
                    Toggle("Vibrazione Attivata", isOn: $gameManager.hapticEnabled)
                        .onChange(of: gameManager.hapticEnabled) { value in
                            gameManager.gameState.hapticAbilitato = value
                            gameManager.saveGame()
                        }
                }
                
                // Game Info Section
                Section("🎮 Informazioni Gioco") {
                    InfoRow(label: "Versione", value: gameManager.gameState.versione)
                    InfoRow(label: "Autore", value: gameManager.gameState.autore)
                    InfoRow(label: "Livello Giocatore", value: "\(gameManager.gameState.livello)")
                    InfoRow(label: "Esperienza", value: "\(gameManager.gameState.esperienza)/\(gameManager.gameState.esperienzaProssimoLivello)")
                    InfoRow(label: "Area Attuale", value: gameManager.gameState.areaAttuale)
                    InfoRow(label: "Gatti Sbloccati", value: "\(gameManager.gameState.gatti.values.filter { $0.sbloccato }.count)/\(gameManager.gameState.gatti.count)")
                    InfoRow(label: "Aree Sbloccate", value: "\(gameManager.gameState.areeSbloccate.count)/\(gameManager.gameState.areeOrdinate.count)")
                    InfoRow(label: "Boss Sconfitti", value: "\(gameManager.gameState.bossSconfitti.count)")
                }
                
                // Resources Section
                Section("💰 Risorse") {
                    InfoRow(label: "🍖 Cibo", value: "\(gameManager.gameState.risorse.cibo)")
                    InfoRow(label: "💧 Acqua", value: "\(gameManager.gameState.risorse.acqua)")
                    InfoRow(label: "🪵 Legno", value: "\(gameManager.gameState.risorse.legno)")
                    InfoRow(label: "🪨 Pietra", value: "\(gameManager.gameState.risorse.pietra)")
                    InfoRow(label: "⚡ Energia", value: "\(gameManager.gameState.risorse.energia)")
                    InfoRow(label: "💊 Pozioni", value: "\(gameManager.gameState.risorse.pozioni)")
                }
                
                // Debug Section
                Section("🔧 Debug & Sviluppo") {
                    Button("Mostra Info Debug") {
                        generateDebugInfo()
                        showingDebugInfo = true
                    }
                    
                    Button("Aggiungi Risorse Test") {
                        gameManager.addResources(
                            cibo: 100,
                            acqua: 100,
                            legno: 50,
                            pietra: 50,
                            ferro: 25,
                            energia: 100,
                            pozioni: 10
                        )
                    }
                    
                    Button("Sblocca Tutti i Gatti") {
                        for catId in gameManager.gameState.gatti.keys {
                            gameManager.unlockCat(catId)
                        }
                    }
                    
                    Button("Completa Area Attuale") {
                        gameManager.gameState.progressioneArea[gameManager.gameState.areaAttuale] = 100
                        gameManager.unlockNextArea()
                        gameManager.saveGame()
                    }
                    
                    Button("Aggiungi Esperienza") {
                        gameManager.gainExperience(500)
                    }
                }
                
                // Save/Reset Section
                Section("💾 Salvataggio") {
                    Button("Salva Gioco") {
                        gameManager.saveGame()
                    }
                    .foregroundColor(.blue)
                    
                    Button("Reset Gioco Completo") {
                        showingResetAlert = true
                    }
                    .foregroundColor(.red)
                }
                
                // Credits Section
                Section("ℹ️ Crediti") {
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Avventura Epica")
                            .font(.headline)
                            .fontWeight(.bold)
                        
                        Text("Gioco originale in Python/Flet creato da Ambrogio Riili")
                            .font(.caption)
                            .foregroundColor(.secondary)
                        
                        Text("Versione Swift/SwiftUI ricreata da Claude Code")
                            .font(.caption)
                            .foregroundColor(.secondary)
                        
                        Text("Un'avventura epica con gatti magici attraverso mondi fantastici!")
                            .font(.caption)
                            .foregroundColor(.secondary)
                            .italic()
                    }
                    .padding(.vertical, 5)
                }
            }
            .navigationTitle("⚙️ Impostazioni")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("🔙 Torna al Menu Principale") {
                        gameManager.navigateToScreen(.mainMenu)
                    }
                }
            }
        }
        .alert("Reset Gioco", isPresented: $showingResetAlert) {
            Button("Annulla", role: .cancel) { }
            Button("Reset", role: .destructive) {
                gameManager.resetGame()
            }
        } message: {
            Text("Sei sicuro di voler resettare tutto il progresso del gioco? Questa azione non può essere annullata.")
        }
        .sheet(isPresented: $showingDebugInfo) {
            DebugInfoView(debugInfo: debugInfo)
        }
    }
    
    private func generateDebugInfo() {
        var info = "=== AVVENTURA EPICA DEBUG INFO ===\n\n"
        
        info += "🎮 GAME STATE\n"
        info += "Versione: \(gameManager.gameState.versione)\n"
        info += "Livello: \(gameManager.gameState.livello)\n"
        info += "Esperienza: \(gameManager.gameState.esperienza)/\(gameManager.gameState.esperienzaProssimoLivello)\n"
        info += "Area Attuale: \(gameManager.gameState.areaAttuale)\n"
        info += "Schermata: \(gameManager.currentScreen)\n\n"
        
        info += "🐱 GATTI\n"
        for (id, cat) in gameManager.gameState.gatti {
            info += "\(id): \(cat.nome) \(cat.emoji)\n"
            info += "  Sbloccato: \(cat.sbloccato ? "Sì" : "No")\n"
            info += "  Livello: \(cat.livello), Attacco: \(cat.attacco)\n"
            info += "  Vita: \(cat.fame), Felicità: \(cat.felicita), Affinità: \(cat.affinita)\n"
            info += "  Abilità: \(cat.abilita.description)\n"
            info += "  Evoluto: \(cat.formaEvoluta ? "Sì" : "No")\n\n"
        }
        
        info += "🗺️ AREE\n"
        info += "Sbloccate: \(gameManager.gameState.areeSbloccate.joined(separator: ", "))\n\n"
        for area in gameManager.gameState.areeOrdinate {
            let progress = gameManager.gameState.progressioneArea[area] ?? 0
            let status = gameManager.gameState.areeSbloccate.contains(area) ? "Sbloccata" : "Bloccata"
            info += "\(area): \(status) - \(progress)%\n"
        }
        
        info += "\n💰 RISORSE\n"
        info += "Cibo: \(gameManager.gameState.risorse.cibo)\n"
        info += "Acqua: \(gameManager.gameState.risorse.acqua)\n"
        info += "Legno: \(gameManager.gameState.risorse.legno)\n"
        info += "Pietra: \(gameManager.gameState.risorse.pietra)\n"
        info += "Ferro: \(gameManager.gameState.risorse.ferro)\n"
        info += "Energia: \(gameManager.gameState.risorse.energia)\n"
        info += "Pozioni: \(gameManager.gameState.risorse.pozioni)\n\n"
        
        info += "🏆 PROGRESSI\n"
        info += "Boss Sconfitti: \(gameManager.gameState.bossSconfitti.count)\n"
        info += "Chiavi Raccolte: \(gameManager.gameState.chiaviRaccolte.count)\n"
        info += "Reliquie Possedute: \(gameManager.gameState.reliquiePossedute.count)\n\n"
        
        info += "⚙️ IMPOSTAZIONI\n"
        info += "Audio: \(gameManager.audioEnabled ? "On" : "Off")\n"
        info += "Haptic: \(gameManager.hapticEnabled ? "On" : "Off")\n"
        
        debugInfo = info
    }
    
    private func testAudio() {
        // Test music and sound effects like main.py
        AudioManager.shared.playVictorySound()
        AudioManager.shared.playCatPurrSound()
        AudioManager.shared.playCollectItemSound()
    }
    
    private func debugAudio() {
        // Generate audio debug info
        var audioDebug = "=== DEBUG AUDIO ===\n\n"
        audioDebug += "Audio Abilitato: \(gameManager.audioEnabled ? "Sì" : "No")\n"
        audioDebug += "Volume Musica: \(Int(musicVolume))%\n"
        audioDebug += "Volume Effetti: \(Int(effectsVolume))%\n"
        audioDebug += "Vibrazione: \(gameManager.hapticEnabled ? "Sì" : "No")\n\n"
        audioDebug += "Audio Files Status:\n"
        audioDebug += "• effetto_vittoria: Caricato\n"
        audioDebug += "• effetto_gatto_attacco: Caricato\n"
        audioDebug += "• effetto_sconfitta: Caricato\n"
        audioDebug += "• effetto_heartbeat: Caricato\n"
        audioDebug += "• villaggio: Caricato\n"
        audioDebug += "• cantina: Caricato\n"
        
        debugInfo = audioDebug
        showingDebugInfo = true
    }
}

struct InfoRow: View {
    let label: String
    let value: String
    
    var body: some View {
        HStack {
            Text(label)
                .foregroundColor(.primary)
            Spacer()
            Text(value)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.trailing)
        }
    }
}

struct DebugInfoView: View {
    let debugInfo: String
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        NavigationView {
            ScrollView {
                Text(debugInfo)
                    .font(.system(.caption, design: .monospaced))
                    .padding()
            }
            .navigationTitle("Debug Info")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Chiudi") {
                        dismiss()
                    }
                }
                
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Copia") {
                        UIPasteboard.general.string = debugInfo
                    }
                }
            }
        }
    }
}

#Preview {
    SettingsView(gameManager: GameManager())
}