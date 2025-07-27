//
//  AreasView.swift
//  Avventura epica
//
//  Created by Ambrogio Riili on 27/07/25.
//

import SwiftUI

struct AreasView: View {
    @ObservedObject var gameManager: GameManager
    @State private var selectedArea: String?
    
    var body: some View {
        VStack(spacing: 20) {
            // Title - exactly as main.py
            Text("Scegli Area")
                .font(.title)
                .fontWeight(.bold)
                .foregroundColor(.blue)
                .padding(.top)
            
            ScrollView {
                VStack(spacing: 15) {
                    // Lista Aree - exactly as main.py (spacing=15)
                    ForEach(gameManager.gameState.areeOrdinate, id: \.self) { area in
                        AreaListButton(
                            area: area,
                            isCurrent: area == gameManager.gameState.areaAttuale,
                            isUnlocked: gameManager.gameState.areeSbloccate.contains(area),
                            onSelect: {
                                if gameManager.gameState.areeSbloccate.contains(area) {
                                    gameManager.changeArea(area)
                                    gameManager.navigateToScreen(.game)
                                }
                            }
                        )
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
                gradient: Gradient(colors: [Color.blue.opacity(0.1), Color.cyan.opacity(0.1)]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()
        )
    }
}

// Area list button exactly as main.py (280x50px)
struct AreaListButton: View {
    let area: String
    let isCurrent: Bool
    let isUnlocked: Bool
    let onSelect: () -> Void
    
    var body: some View {
        Button(action: onSelect) {
            HStack {
                if isCurrent {
                    // "Nome Area (ATTUALE)" (GREEN_600)
                    Text("\(area) (ATTUALE)")
                        .font(.subheadline)
                        .fontWeight(.semibold)
                        .foregroundColor(.white)
                } else if isUnlocked {
                    // "Nome Area" (BLUE_600)
                    Text(area)
                        .font(.subheadline)
                        .fontWeight(.semibold)
                        .foregroundColor(.white)
                } else {
                    // Bloccata
                    Text("🔒 \(area)")
                        .font(.subheadline)
                        .fontWeight(.semibold)
                        .foregroundColor(.white)
                }
                
                Spacer()
            }
            .frame(width: 280, height: 50)
            .background(buttonColor)
            .cornerRadius(8)
        }
        .disabled(!isUnlocked)
        .buttonStyle(PlainButtonStyle())
    }
    
    private var buttonColor: Color {
        if isCurrent {
            return Color.green.opacity(0.8) // GREEN_600
        } else if isUnlocked {
            return Color.blue.opacity(0.8) // BLUE_600
        } else {
            return Color.gray.opacity(0.6) // Bloccata
        }
    }
}

struct CurrentAreaCard: View {
    @ObservedObject var gameManager: GameManager
    
    var body: some View {
        VStack(spacing: 15) {
            Text("Area Attuale")
                .font(.headline)
                .foregroundColor(.blue)
            
            Text(gameManager.gameState.areaAttuale)
                .font(.title2)
                .fontWeight(.bold)
                .multilineTextAlignment(.center)
            
            // Progress in current area
            let progress = gameManager.gameState.progressioneArea[gameManager.gameState.areaAttuale] ?? 0
            VStack(spacing: 8) {
                Text("Progresso: \(progress)/100")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                
                ProgressView(value: Double(progress), total: 100)
                    .tint(.blue)
                    .frame(height: 12)
                
                if progress >= 100 {
                    Text("✅ Area completata!")
                        .font(.caption)
                        .fontWeight(.semibold)
                        .foregroundColor(.green)
                } else {
                    Text("Continua a esplorare per progredire")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 15)
                .fill(Color.blue.opacity(0.1))
                .overlay(
                    RoundedRectangle(cornerRadius: 15)
                        .stroke(Color.blue.opacity(0.3), lineWidth: 2)
                )
        )
    }
}

struct AreaProgressCard: View {
    let area: String
    let index: Int
    let isUnlocked: Bool
    let isCurrent: Bool
    let progress: Int
    let onSelect: () -> Void
    
    var body: some View {
        Button(action: onSelect) {
            HStack(spacing: 15) {
                // Area number and status
                ZStack {
                    Circle()
                        .fill(circleColor)
                        .frame(width: 40, height: 40)
                    
                    if !isUnlocked {
                        Text("🔒")
                            .font(.subheadline)
                    } else if progress >= 100 {
                        Text("✅")
                            .font(.subheadline)
                    } else {
                        Text("\(index + 1)")
                            .font(.subheadline)
                            .fontWeight(.semibold)
                            .foregroundColor(.white)
                    }
                }
                
                // Area info
                VStack(alignment: .leading, spacing: 5) {
                    Text(area)
                        .font(.headline)
                        .fontWeight(.semibold)
                        .foregroundColor(isCurrent ? .blue : .primary)
                    
                    if isUnlocked {
                        // Progress bar
                        HStack {
                            ProgressView(value: Double(progress), total: 100)
                                .tint(progressColor)
                                .frame(height: 6)
                            
                            Text("\(progress)%")
                                .font(.caption)
                                .foregroundColor(.secondary)
                                .frame(width: 35, alignment: .trailing)
                        }
                        
                        Text(areaDescription)
                            .font(.caption)
                            .foregroundColor(.secondary)
                    } else {
                        Text("Area bloccata - Completa l'area precedente")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                }
                
                Spacer()
                
                // Current indicator
                if isCurrent {
                    Text("📍")
                        .font(.title2)
                }
            }
            .padding()
            .background(
                RoundedRectangle(cornerRadius: 12)
                    .fill(backgroundColor)
                    .overlay(
                        RoundedRectangle(cornerRadius: 12)
                            .stroke(borderColor, lineWidth: isCurrent ? 2 : 1)
                    )
            )
        }
        .buttonStyle(PlainButtonStyle())
        .disabled(!isUnlocked)
    }
    
    private var circleColor: Color {
        if !isUnlocked {
            return Color.gray.opacity(0.3)
        } else if progress >= 100 {
            return Color.green
        } else if isCurrent {
            return Color.blue
        } else {
            return Color.orange
        }
    }
    
    private var progressColor: Color {
        if progress >= 100 {
            return .green
        } else if isCurrent {
            return .blue
        } else {
            return .orange
        }
    }
    
    private var backgroundColor: Color {
        if !isUnlocked {
            return Color.gray.opacity(0.1)
        } else if isCurrent {
            return Color.blue.opacity(0.1)
        } else {
            return Color.white.opacity(0.1)
        }
    }
    
    private var borderColor: Color {
        if !isUnlocked {
            return Color.gray.opacity(0.3)
        } else if isCurrent {
            return Color.blue.opacity(0.5)
        } else {
            return Color.gray.opacity(0.3)
        }
    }
    
    private var areaDescription: String {
        switch area {
        case "Villaggio":
            return "Il punto di partenza della tua avventura"
        case "🏠 Cantina":
            return "Tunnel sotterranei pieni di misteri"
        case "🚰 Fogne":
            return "Passaggi umidi e pericolosi"
        case "🌀 Labirinto Antico":
            return "Un labirinto pieno di enigmi"
        case "❄️ Area Innevata":
            return "Terre ghiacciate e creature artiche"
        case "🌿 Giungla Selvaggia":
            return "Foresta tropicale ricca di vita"
        case "🌲 Bosco Profondo":
            return "Antichi alberi e creature magiche"
        case "⚰️ Cimitero":
            return "Luogo inquietante pieno di non morti"
        case "🏚️ Casa degli Orrori":
            return "Un luogo che mette alla prova la sanità mentale"
        case "🏭 Fabbrica Abbandonata":
            return "Rovine industriali e macchinari arrugginiti"
        case "⛏️ Miniera Profonda":
            return "Tunnel sotterranei ricchi di minerali"
        case "🌙 Cripta Maledetta":
            return "Tomba antica con poteri oscuri"
        case "🌊 Mare":
            return "Vaste distese d'acqua e creature marine"
        case "🏔️ Montagna Sacra":
            return "Vette elevate con templi mistici"
        case "🌋 Vulcano Attivo":
            return "Terre di fuoco e lava bollente"
        case "👑 Palazzo Finale":
            return "La sfida finale ti attende"
        default:
            return "Area misteriosa da esplorare"
        }
    }
}

struct AreaLegendSection: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("📖 Legenda")
                .font(.headline)
                .fontWeight(.bold)
            
            VStack(alignment: .leading, spacing: 8) {
                LegendItem(icon: "🔒", text: "Area bloccata - Completa l'area precedente")
                LegendItem(icon: "📍", text: "La tua posizione attuale")
                LegendItem(icon: "✅", text: "Area completata al 100%")
                LegendItem(icon: "🎯", text: "Tocca un'area sbloccata per viaggiare")
            }
            
            Divider()
                .padding(.vertical, 5)
            
            VStack(alignment: .leading, spacing: 5) {
                Text("💡 Consigli")
                    .font(.subheadline)
                    .fontWeight(.semibold)
                
                Text("• Esplora completamente ogni area per sbloccare la successiva")
                    .font(.caption)
                    .foregroundColor(.secondary)
                
                Text("• Ogni area ha nemici unici e ricompense speciali")
                    .font(.caption)
                    .foregroundColor(.secondary)
                
                Text("• Alcune aree richiedono gatti specifici o chiavi speciali")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 12)
                .fill(Color.yellow.opacity(0.1))
                .overlay(
                    RoundedRectangle(cornerRadius: 12)
                        .stroke(Color.yellow.opacity(0.3), lineWidth: 1)
                )
        )
    }
}

struct LegendItem: View {
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
    AreasView(gameManager: GameManager())
}