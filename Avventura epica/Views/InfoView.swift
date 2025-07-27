//
//  InfoView.swift
//  Avventura epica
//
//  Created by Ambrogio Riili on 27/07/25.
//

import SwiftUI

struct InfoView: View {
    @ObservedObject var gameManager: GameManager
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    // Title - match main.py
                    VStack(spacing: 10) {
                        Text("Info Gioco")
                            .font(.largeTitle)
                            .fontWeight(.bold)
                            .foregroundColor(.orange)
                        
                        Text("AVVENTURA EPICA")
                            .font(.title)
                            .fontWeight(.bold)
                            .multilineTextAlignment(.center)
                    }
                    .frame(maxWidth: .infinity)
                    .padding(.bottom, 20)
                    
                    // Game Info - exactly as in main.py
                    VStack(alignment: .leading, spacing: 15) {
                        InfoSectionRow(label: "Versione:", value: gameManager.gameState.versione)
                        InfoSectionRow(label: "Autore:", value: gameManager.gameState.autore)
                        InfoSectionRow(label: "Data rilascio:", value: "18 giugno 2025")
                        
                        VStack(alignment: .leading, spacing: 8) {
                            Text("Descrizione:")
                                .font(.headline)
                                .fontWeight(.semibold)
                            
                            Text("Un'avventura epica con gatti magici attraverso 16 mondi fantastici! Combatti mostri, sblocca nuovi compagni felini, raccogli tesori e diventa il leggendario Guardiano dei Gatti!")
                                .font(.body)
                                .foregroundColor(.secondary)
                        }
                        
                        VStack(alignment: .leading, spacing: 8) {
                            Text("Caratteristiche:")
                                .font(.headline)
                                .fontWeight(.semibold)
                            
                            VStack(alignment: .leading, spacing: 4) {
                                Text("• 16 aree uniche da esplorare")
                                Text("• 5 gatti speciali con abilità uniche")
                                Text("• Sistema di combattimento strategico con auto-combat")
                                Text("• Negozi e equipaggiamento evoluto")
                                Text("• Boss epic e sfide leggendarie")
                                Text("• Sistema di affinità e evoluzione gatti")
                                Text("• Audio atmosferico e effetti coinvolgenti")
                                Text("• Reliquie misteriose e poteri speciali")
                                Text("• Sistema di salvataggio automatico")
                                Text("• Progressione non lineare e multiple aree")
                                Text("• Nutrizione e gestione risorse")
                                Text("• Heartbeat system in combattimenti critici")
                            }
                            .font(.caption)
                            .foregroundColor(.secondary)
                        }
                        
                        VStack(alignment: .leading, spacing: 8) {
                            Text("Credits:")
                                .font(.headline)
                                .fontWeight(.semibold)
                            
                            VStack(alignment: .leading, spacing: 4) {
                                Text("Gioco originale creato in Python/Flet")
                                Text("Versione Swift/SwiftUI ricreata da Claude Code")
                                Text("Tutti i diritti riservati ad Ambrogio Riili")
                                Text("Un progetto indie di pura passione! 🎮❤️")
                            }
                            .font(.caption)
                            .foregroundColor(.secondary)
                            .italic()
                        }
                    }
                    .padding()
                    .background(
                        RoundedRectangle(cornerRadius: 12)
                            .fill(Color.orange.opacity(0.1))
                            .overlay(
                                RoundedRectangle(cornerRadius: 12)
                                    .stroke(Color.orange.opacity(0.3), lineWidth: 1)
                            )
                    )
                    
                    Spacer(minLength: 50)
                }
                .padding()
            }
            .navigationTitle("Info")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Indietro") {
                        dismiss()
                    }
                }
            }
        }
    }
}

struct InfoSectionRow: View {
    let label: String
    let value: String
    
    var body: some View {
        HStack {
            Text(label)
                .font(.subheadline)
                .fontWeight(.semibold)
            
            Text(value)
                .font(.subheadline)
                .foregroundColor(.secondary)
            
            Spacer()
        }
    }
}

#Preview {
    InfoView(gameManager: GameManager())
}