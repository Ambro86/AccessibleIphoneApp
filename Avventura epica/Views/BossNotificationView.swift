//
//  BossNotificationView.swift
//  Avventura epica
//
//  Created by Ambrogio Riili on 27/07/25.
//

import SwiftUI

struct BossNotificationView: View {
    @ObservedObject var gameManager: GameManager
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        ZStack {
            // Dramatic background
            LinearGradient(
                gradient: Gradient(colors: [Color.red.opacity(0.8), Color.black.opacity(0.9)]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()
            
            VStack(spacing: 40) {
                Spacer()
                
                // Boss unlocked title
                Text("🔥 BOSS SBLOCCATO! 🔥")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                    .foregroundColor(.red)
                    .multilineTextAlignment(.center)
                    .shadow(color: .black, radius: 2, x: 1, y: 1)
                
                // Boss information
                if let area = gameManager.gameState.currentBossArea,
                   let boss = getBossInfo(for: area) {
                    VStack(spacing: 20) {
                        // Boss emoji and name
                        Text(boss.emoji)
                            .font(.system(size: 80))
                            .shadow(color: .black, radius: 3, x: 2, y: 2)
                        
                        Text(boss.nome)
                            .font(.title)
                            .fontWeight(.bold)
                            .foregroundColor(.white)
                            .multilineTextAlignment(.center)
                            .shadow(color: .black, radius: 1, x: 1, y: 1)
                        
                        // Boss stats preview
                        HStack(spacing: 30) {
                            VStack {
                                Text("❤️")
                                    .font(.title2)
                                Text("\(boss.hp)")
                                    .font(.headline)
                                    .fontWeight(.bold)
                                    .foregroundColor(.red)
                            }
                            
                            VStack {
                                Text("⚔️")
                                    .font(.title2)
                                Text("\(boss.attacco)")
                                    .font(.headline)
                                    .fontWeight(.bold)
                                    .foregroundColor(.orange)
                            }
                        }
                        .padding()
                        .background(
                            RoundedRectangle(cornerRadius: 15)
                                .fill(Color.black.opacity(0.3))
                                .overlay(
                                    RoundedRectangle(cornerRadius: 15)
                                        .stroke(Color.red.opacity(0.5), lineWidth: 2)
                                )
                        )
                        
                        // Challenge message
                        Text("Hai raggiunto il 100% di progressione in quest'area!")
                            .font(.title3)
                            .foregroundColor(.yellow)
                            .multilineTextAlignment(.center)
                            .padding(.horizontal)
                        
                        // Boss scaling warning if applicable
                        if let area = gameManager.gameState.currentBossArea {
                            let scalingInfo = gameManager.getBossScalingInfo(area)
                            if scalingInfo.isScaled {
                                VStack(spacing: 8) {
                                    Text("⚠️ AVVISO: BOSS POTENZIATO ⚠️")
                                        .font(.headline)
                                        .fontWeight(.bold)
                                        .foregroundColor(.red)
                                    
                                    Text("Livello richiesto: \(scalingInfo.requiredLevel)")
                                        .font(.subheadline)
                                        .foregroundColor(.orange)
                                    
                                    Text("Il tuo livello: \(scalingInfo.currentLevel)")
                                        .font(.subheadline)
                                        .foregroundColor(.orange)
                                    
                                    Text("Il boss sarà 3x più forte!")
                                        .font(.caption)
                                        .foregroundColor(.red)
                                        .fontWeight(.semibold)
                                }
                                .padding()
                                .background(
                                    RoundedRectangle(cornerRadius: 10)
                                        .fill(Color.red.opacity(0.2))
                                        .overlay(
                                            RoundedRectangle(cornerRadius: 10)
                                                .stroke(Color.red.opacity(0.6), lineWidth: 2)
                                        )
                                )
                            }
                        }
                        
                        Text("Vuoi affrontare il boss ora?")
                            .font(.headline)
                            .foregroundColor(.white)
                            .multilineTextAlignment(.center)
                    }
                }
                
                Spacer()
                
                // Action buttons
                VStack(spacing: 15) {
                    Button(action: {
                        gameManager.startBossFight()
                        dismiss()
                    }) {
                        Text("⚔️ AFFRONTA SUBITO!")
                            .font(.title2)
                            .fontWeight(.bold)
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 16)
                            .background(
                                RoundedRectangle(cornerRadius: 12)
                                    .fill(Color.red.opacity(0.8))
                                    .overlay(
                                        RoundedRectangle(cornerRadius: 12)
                                            .stroke(Color.red, lineWidth: 2)
                                    )
                            )
                    }
                    .scaleEffect(1.0)
                    .animation(.easeInOut(duration: 0.1), value: false)
                    
                    Button(action: {
                        gameManager.dismissBossNotification()
                        dismiss()
                    }) {
                        Text("🚪 Più Tardi")
                            .font(.headline)
                            .fontWeight(.semibold)
                            .foregroundColor(.gray)
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 12)
                            .background(
                                RoundedRectangle(cornerRadius: 12)
                                    .fill(Color.black.opacity(0.3))
                                    .overlay(
                                        RoundedRectangle(cornerRadius: 12)
                                            .stroke(Color.gray.opacity(0.5), lineWidth: 1)
                                    )
                            )
                    }
                }
                .padding(.horizontal, 30)
                
                Spacer()
            }
            .padding()
        }
        .navigationBarHidden(true)
        .preferredColorScheme(.dark)
    }
    
    private func getBossInfo(for area: String) -> (nome: String, emoji: String, hp: Int, attacco: Int)? {
        // Match the boss info from GameManager.getAreaBoss()
        switch area {
        case "🏠 Cantina":
            return ("🕷️ Regina dei Ragni", "🕷️", 240, 50)
        case "🚰 Fogne":
            return ("🐀 Boss Topo delle Fogne", "🐀", 360, 65)
        case "🌀 Labirinto Antico":
            return ("🗿 Guardiano di Pietra", "🗿", 480, 80)
        case "❄️ Area Innevata":
            return ("🐺 Alpha del Branco", "🐺", 600, 95)
        case "🌿 Giungla Selvaggia":
            return ("🐍 Serpente Ancestrale", "🐍", 720, 110)
        case "🌲 Bosco Profondo":
            return ("🦌 Cervo Mistico", "🦌", 840, 125)
        case "⚰️ Cimitero":
            return ("💀 Lich Supremo", "💀", 960, 140)
        case "🏚️ Casa degli Orrori":
            return ("👻 Spirito Maledetto", "👻", 1080, 155)
        case "🏭 Fabbrica Abbandonata":
            return ("🤖 Automa Corrotto", "🤖", 1200, 170)
        case "⛏️ Miniera Profonda":
            return ("⛰️ Elementale di Terra", "⛰️", 1320, 185)
        case "🌙 Cripta Maledetta":
            return ("🧙‍♂️ Necromante Antico", "🧙‍♂️", 1440, 200)
        case "🌊 Mare":
            return ("🐙 Kraken Leggendario", "🐙", 1560, 215)
        case "🏔️ Montagna Sacra":
            return ("🦅 Fenice Dorata", "🦅", 1680, 230)
        case "🌋 Vulcano Attivo":
            return ("🔥 Drago di Magma", "🔥", 1800, 245)
        case "👑 Palazzo Finale":
            return ("👑 Imperatore Oscuro", "👑", 2000, 300)
        case "🌌 Regno degli Incubi":
            return ("🌌 Signore degli Incubi", "🌌", 2500, 350)
        default:
            return nil
        }
    }
}

#Preview {
    BossNotificationView(gameManager: GameManager())
}