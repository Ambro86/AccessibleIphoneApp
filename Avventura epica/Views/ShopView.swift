//
//  ShopView.swift
//  Avventura epica
//
//  Created by Ambrogio Riili on 27/07/25.
//

import SwiftUI

struct ShopView: View {
    @ObservedObject var gameManager: GameManager
    @State private var selectedCategory: EquipmentType = .arma
    @State private var showingPurchaseConfirmation = false
    @State private var itemToPurchase: ShopItem?
    @State private var purchaseMessage = ""
    @State private var showingMessage = false
    
    var body: some View {
        VStack(spacing: 20) {
            // Title - exactly as main.py
            Text("Negozio")
                .font(.title)
                .fontWeight(.bold)
                .foregroundColor(.orange)
                .padding(.top)
            
            // Monete disponibili - exactly as main.py
            Text("💰 Monete disponibili: \(gameManager.gameState.inventario.money)")
                .font(.headline)
                .foregroundColor(.yellow)
            
            ScrollView {
                VStack(spacing: 15) {
                    // Lista Oggetti - exactly as main.py (verticale, spacing=15)
                    ForEach(filteredShopItems, id: \.id) { shopItem in
                        ShopItemContainer(
                            shopItem: shopItem,
                            playerMoney: gameManager.gameState.inventario.money,
                            isOwned: gameManager.gameState.inventario.items[shopItem.equipment.nome] != nil,
                            onPurchase: {
                                attemptPurchase(shopItem)
                            }
                        )
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
                gradient: Gradient(colors: [Color.orange.opacity(0.1), Color.yellow.opacity(0.1)]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()
        )
        .alert("Conferma Acquisto", isPresented: $showingPurchaseConfirmation) {
            Button("Annulla", role: .cancel) { }
            Button("Acquista") {
                if let item = itemToPurchase {
                    completePurchase(item)
                }
            }
        } message: {
            if let item = itemToPurchase {
                Text("Vuoi acquistare \(item.equipment.nome) per \(item.equipment.prezzo) monete?")
            }
        }
        .overlay(
            // Purchase message overlay
            VStack {
                if showingMessage {
                    Text(purchaseMessage)
                        .padding()
                        .background(Color.black.opacity(0.8))
                        .foregroundColor(.white)
                        .cornerRadius(10)
                        .transition(.scale.combined(with: .opacity))
                }
                Spacer()
            }
            .animation(.easeInOut(duration: 0.3), value: showingMessage)
        )
    }
    
    private var shopItems: [ShopItem] {
        // Get items from current area shop
        let areaShop = gameManager.getAreaShop(gameManager.gameState.areaAttuale)
        return areaShop.values.map { equipment in
            ShopItem(equipment: equipment)
        }
    }
    
    private var filteredShopItems: [ShopItem] {
        return shopItems.filter { $0.equipment.tipo == selectedCategory }
    }
    
    private func attemptPurchase(_ shopItem: ShopItem) {
        itemToPurchase = shopItem
        showingPurchaseConfirmation = true
    }
    
    private func completePurchase(_ shopItem: ShopItem) {
        let success = gameManager.gameState.inventario.buyItem(shopItem.equipment)
        
        if success {
            purchaseMessage = "✅ \(shopItem.equipment.nome) acquistato!"
            AudioManager.shared.playCollectMoneySound()
            AudioManager.shared.playCollectItemSound()
        } else {
            purchaseMessage = "❌ Soldi insufficienti!"
            AudioManager.shared.playErrorSound()
        }
        
        gameManager.saveGame()
        showingMessage = true
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            showingMessage = false
        }
    }
    
    private func showMessage(_ message: String) {
        purchaseMessage = message
        showingMessage = true
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            showingMessage = false
        }
    }
    
    private func getAreaShopName() -> String {
        switch gameManager.gameState.areaAttuale {
        case "Villaggio": return "Villaggio"
        case "🏠 Cantina": return "Cantina"
        case "🚰 Fogne": return "Fogne"
        case "🌀 Labirinto Antico": return "Labirinto"
        case "❄️ Area Innevata": return "Area Innevata"
        case "🌿 Giungla Selvaggia": return "Giungla"
        case "🌲 Bosco Profondo": return "Bosco"
        case "⚰️ Cimitero": return "Cimitero"
        case "🏚️ Casa degli Orrori": return "Casa degli Orrori"
        case "🏭 Fabbrica Abbandonata": return "Fabbrica"
        case "⛏️ Miniera Profonda": return "Miniera"
        case "🌙 Cripta Maledetta": return "Cripta"
        case "🌊 Mare": return "Mare"
        case "🏔️ Montagna Sacra": return "Montagna"
        case "🌋 Vulcano Attivo": return "Vulcano"
        case "👑 Palazzo Finale": return "Palazzo"
        case "🌌 Regno degli Incubi": return "Regno degli Incubi"
        default: return "Negozio Locale"
        }
    }
    
    private func getAreaMaterial() -> String {
        switch gameManager.gameState.areaAttuale {
        case "Villaggio": return "Legno"
        case "🏠 Cantina": return "Pietra"
        case "🚰 Fogne": return "Rame"
        case "🌀 Labirinto Antico": return "Bronzo"
        case "❄️ Area Innevata": return "Ferro"
        case "🌿 Giungla Selvaggia": return "Acciaio"
        case "🌲 Bosco Profondo": return "Acciaio Temprato"
        case "⚰️ Cimitero": return "Argento"
        case "🏚️ Casa degli Orrori": return "Oro"
        case "🏭 Fabbrica Abbandonata": return "Platino"
        case "⛏️ Miniera Profonda": return "Titanio"
        case "🌙 Cripta Maledetta": return "Ossidiana"
        case "🌊 Mare": return "Diamante"
        case "🏔️ Montagna Sacra": return "Mithril"
        case "🌋 Vulcano Attivo": return "Cristallo Runico"
        case "👑 Palazzo Finale": return "Essenza Divina"
        case "🌌 Regno degli Incubi": return "Scaglie di Drago"
        default: return "Materiale Base"
        }
    }
}

// Shop item container exactly as main.py (Container 300x120px, GREY_700)
struct ShopItemContainer: View {
    let shopItem: ShopItem
    let playerMoney: Int
    let isOwned: Bool
    let onPurchase: () -> Void
    
    var body: some View {
        VStack(spacing: 10) {
            // Nome oggetto (size=16, bold, centrato)
            Text(shopItem.equipment.nome)
                .font(.system(size: 16))
                .fontWeight(.bold)
                .multilineTextAlignment(.center)
            
            // Descrizione (size=12, centrato)
            Text(shopItem.equipment.descrizione)
                .font(.system(size: 12))
                .multilineTextAlignment(.center)
                .foregroundColor(.secondary)
                .lineLimit(2)
            
            // Prezzo in monete (size=11, AMBER_400, centrato)
            Text("💰 \(shopItem.equipment.prezzo) monete")
                .font(.system(size: 11))
                .foregroundColor(.yellow)
                .multilineTextAlignment(.center)
            
            // Pulsante "Acquista" (GREEN_600, 140px width)
            Button(action: onPurchase) {
                Text(isOwned ? "Posseduto" : "Acquista")
                    .font(.subheadline)
                    .fontWeight(.semibold)
                    .foregroundColor(.white)
                    .frame(width: 140, height: 35)
                    .background(isOwned ? Color.gray : (canAfford ? Color.green.opacity(0.8) : Color.red.opacity(0.6)))
                    .cornerRadius(8)
            }
            .disabled(isOwned || !canAfford)
        }
        .frame(width: 300, height: 120) // Exact dimensions as main.py
        .padding(10)
        .background(Color.gray.opacity(0.7)) // GREY_700 like main.py
        .cornerRadius(12)
    }
    
    private var canAfford: Bool {
        playerMoney >= shopItem.equipment.prezzo
    }
}

struct CategoryButton: View {
    let category: EquipmentType
    let isSelected: Bool
    let itemCount: Int
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            VStack(spacing: 8) {
                ZStack {
                    RoundedRectangle(cornerRadius: 12)
                        .fill(isSelected ? Color.blue.opacity(0.3) : Color.gray.opacity(0.1))
                        .frame(width: 80, height: 60)
                    
                    VStack(spacing: 4) {
                        Text(category.emoji)
                            .font(.title2)
                        
                        Text("\(itemCount)")
                            .font(.caption2)
                            .fontWeight(.bold)
                            .foregroundColor(isSelected ? .blue : .secondary)
                    }
                }
                
                Text(category.displayName)
                    .font(.caption)
                    .fontWeight(isSelected ? .semibold : .regular)
                    .foregroundColor(isSelected ? .blue : .secondary)
            }
        }
        .buttonStyle(PlainButtonStyle())
    }
}

struct ShopItemCard: View {
    let shopItem: ShopItem
    let playerMoney: Int
    let isOwned: Bool
    let onPurchase: () -> Void
    
    private var canAfford: Bool {
        return playerMoney >= shopItem.equipment.prezzo
    }
    
    var body: some View {
        HStack(spacing: 15) {
            // Item icon and recommended badge
            ZStack {
                RoundedRectangle(cornerRadius: 12)
                    .fill(Color.gray.opacity(0.1))
                    .frame(width: 80, height: 80)
                
                Text(shopItem.equipment.emoji)
                    .font(.title)
                
                if shopItem.recommended {
                    VStack {
                        HStack {
                            Spacer()
                            Text("⭐")
                                .font(.caption)
                                .padding(4)
                                .background(Color.yellow.opacity(0.3))
                                .clipShape(Circle())
                        }
                        Spacer()
                    }
                }
            }
            
            // Item details
            VStack(alignment: .leading, spacing: 8) {
                HStack {
                    Text(shopItem.equipment.nome)
                        .font(.headline)
                        .fontWeight(.semibold)
                        .lineLimit(2)
                    
                    Spacer()
                    
                    if isOwned {
                        Text("✅")
                            .font(.title2)
                    }
                }
                
                Text(shopItem.equipment.descrizione)
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .lineLimit(2)
                
                // Stats
                HStack(spacing: 15) {
                    if shopItem.equipment.danno > 0 {
                        HStack(spacing: 2) {
                            Text("⚔️")
                            Text("+\(shopItem.equipment.danno)")
                                .fontWeight(.medium)
                        }
                        .font(.caption)
                    }
                    
                    if shopItem.equipment.difesa > 0 {
                        HStack(spacing: 2) {
                            Text("🛡️")
                            Text("+\(shopItem.equipment.difesa)")
                                .fontWeight(.medium)
                        }
                        .font(.caption)
                    }
                    
                    Spacer()
                }
                
                // Price and purchase button
                HStack {
                    Text("💰 \(shopItem.equipment.prezzo)")
                        .font(.subheadline)
                        .fontWeight(.bold)
                        .foregroundColor(canAfford ? .green : .red)
                    
                    Spacer()
                    
                    if isOwned {
                        Text("Posseduto")
                            .font(.caption)
                            .padding(.horizontal, 8)
                            .padding(.vertical, 4)
                            .background(Color.green.opacity(0.2))
                            .foregroundColor(.green)
                            .cornerRadius(6)
                    } else if canAfford {
                        Button("Acquista") {
                            onPurchase()
                        }
                        .font(.caption)
                        .fontWeight(.semibold)
                        .padding(.horizontal, 12)
                        .padding(.vertical, 6)
                        .background(Color.blue.opacity(0.2))
                        .foregroundColor(.blue)
                        .cornerRadius(8)
                    } else {
                        Text("Non disponibile")
                            .font(.caption)
                            .padding(.horizontal, 8)
                            .padding(.vertical, 4)
                            .background(Color.red.opacity(0.2))
                            .foregroundColor(.red)
                            .cornerRadius(6)
                    }
                }
            }
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 15)
                .fill(shopItem.recommended ? Color.yellow.opacity(0.1) : Color.white.opacity(0.1))
                .overlay(
                    RoundedRectangle(cornerRadius: 15)
                        .stroke(
                            shopItem.recommended ? Color.yellow.opacity(0.5) : Color.gray.opacity(0.3),
                            lineWidth: shopItem.recommended ? 2 : 1
                        )
                )
        )
        .opacity(canAfford || isOwned ? 1.0 : 0.6)
    }
}

#Preview {
    ShopView(gameManager: GameManager())
}