//
//  MainMenuView.swift
//  Avventura epica
//
//  Created by Ambrogio Riili on 27/07/25.
//

import SwiftUI

struct MainMenuView: View {
    @ObservedObject var gameManager: GameManager
    @State private var showingInfo = false
    
    var body: some View {
        ZStack {
            // Background gradient - yellow/amber theme like main.py
            LinearGradient(
                gradient: Gradient(colors: [Color.yellow.opacity(0.2), Color.orange.opacity(0.2)]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()
            
            VStack(spacing: 40) {
                Spacer()
                
                // Title - match main.py exactly
                VStack(spacing: 10) {
                    Text("Avventura Epica")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                        .foregroundColor(.yellow)
                        .multilineTextAlignment(.center)
                    
                    Text("v\(gameManager.gameState.versione)")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                
                Spacer()
                
                // Main menu buttons - exactly as in main.py
                VStack(spacing: 20) {
                    // 1. Inizia Gioco (verde)
                    MainMenuButton(
                        title: "Inizia Gioco",
                        tooltip: "Inizia una nuova avventura o continua",
                        color: Color.green.opacity(0.8),
                        width: 300,
                        height: 60
                    ) {
                        gameManager.navigateToScreen(.game)
                    }
                    
                    // 2. Carica Gioco (blu)  
                    MainMenuButton(
                        title: "Carica Gioco",
                        tooltip: "Carica partita salvata",
                        color: Color.blue.opacity(0.8),
                        width: 300,
                        height: 60
                    ) {
                        gameManager.loadGame()
                        gameManager.navigateToScreen(.game)
                    }
                    
                    // 3. Impostazioni (viola)
                    MainMenuButton(
                        title: "Impostazioni", 
                        tooltip: "Impostazioni audio e vibrazione",
                        color: Color.purple.opacity(0.8),
                        width: 300,
                        height: 60
                    ) {
                        gameManager.navigateToScreen(.settings)
                    }
                    
                    // 4. Info (arancione)
                    MainMenuButton(
                        title: "Info",
                        tooltip: "Informazioni sul gioco",
                        color: Color.orange.opacity(0.8),
                        width: 300,
                        height: 60
                    ) {
                        showingInfo = true
                    }
                }
                
                Spacer()
                Spacer()
            }
            .padding()
        }
        .sheet(isPresented: $showingInfo) {
            InfoView(gameManager: gameManager)
        }
    }
}

// Main menu button that matches main.py styling exactly
struct MainMenuButton: View {
    let title: String
    let tooltip: String
    let color: Color
    let width: CGFloat
    let height: CGFloat
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.title2)
                .fontWeight(.semibold)
                .foregroundColor(.white)
                .frame(width: width, height: height)
                .background(color)
                .cornerRadius(8)
        }
        .buttonStyle(PlainButtonStyle())
        .scaleEffect(1.0)
        .animation(.easeInOut(duration: 0.1), value: false)
        .help(tooltip) // Tooltip like main.py
    }
}

// Keep old MenuButton for other views that might use it
struct MenuButton: View {
    let title: String
    let subtitle: String
    let color: Color
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            VStack(alignment: .leading, spacing: 5) {
                Text(title)
                    .font(.headline)
                    .fontWeight(.semibold)
                
                Text(subtitle)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            .frame(maxWidth: .infinity, alignment: .leading)
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
        .scaleEffect(1.0)
        .animation(.easeInOut(duration: 0.1), value: false)
    }
}

#Preview {
    MainMenuView(gameManager: GameManager())
}