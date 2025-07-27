//
//  ContentView.swift
//  Avventura epica
//
//  Created by Ambrogio Riili on 26/07/25.
//

import SwiftUI

struct ContentView: View {
    @StateObject private var gameManager = GameManager()
    
    var body: some View {
        NavigationView {
            switch gameManager.currentScreen {
            case .mainMenu:
                MainMenuView(gameManager: gameManager)
            case .game:
                GameView(gameManager: gameManager)
            case .cats:
                CatsView(gameManager: gameManager)
            case .areas:
                AreasView(gameManager: gameManager)
            case .settings:
                SettingsView(gameManager: gameManager)
            case .inventory:
                InventoryView(gameManager: gameManager)
            case .shop:
                ShopView(gameManager: gameManager)
            case .info:
                InfoView(gameManager: gameManager)
            }
        }
        .navigationViewStyle(StackNavigationViewStyle())
        .sheet(isPresented: $gameManager.gameState.showingBossNotification) {
            BossNotificationView(gameManager: gameManager)
        }
    }
}

#Preview {
    ContentView()
}
