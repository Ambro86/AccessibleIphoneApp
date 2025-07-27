//
//  InventoryView.swift
//  Avventura epica
//
//  Created by Ambrogio Riili on 27/07/25.
//

import SwiftUI

struct InventoryView: View {
    @ObservedObject var gameManager: GameManager
    @State private var selectedEquipmentType: EquipmentType = .arma
    @State private var showingItemDetails = false
    @State private var selectedItem: InventoryItem?
    
    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // Header con soldi
                HStack {
                    Text("💰 \(gameManager.gameState.inventario.money) monete")
                        .font(.headline)
                        .fontWeight(.bold)
                        .foregroundColor(.yellow)
                    
                    Spacer()
                    
                    // Stats totali
                    VStack(alignment: .trailing, spacing: 2) {
                        Text("⚔️ +\(gameManager.gameState.inventario.stats.totalDamage)")
                            .font(.caption)
                            .foregroundColor(.red)
                        Text("🛡️ +\(gameManager.gameState.inventario.stats.totalDefense)")
                            .font(.caption)
                            .foregroundColor(.blue)
                    }
                }
                .padding()
                .background(Color.black.opacity(0.1))
                
                // Equipment type selector
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 15) {
                        ForEach(EquipmentType.allCases, id: \.self) { type in
                            EquipmentTypeButton(
                                type: type,
                                isSelected: selectedEquipmentType == type,
                                equippedItem: gameManager.gameState.inventario.getEquippedItem(type)
                            ) {
                                selectedEquipmentType = type
                            }
                        }
                    }
                    .padding(.horizontal)
                }
                .padding(.vertical, 10)
                
                // Inventory grid
                ScrollView {
                    if filteredItems.isEmpty {
                        VStack(spacing: 20) {
                            Image(systemName: "bag")
                                .font(.system(size: 60))
                                .foregroundColor(.gray.opacity(0.5))
                            
                            Text("Nessun \(selectedEquipmentType.displayName.lowercased())")
                                .font(.headline)
                                .foregroundColor(.secondary)
                            
                            Text("Visita il negozio per acquistare equipaggiamento!")
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                                .multilineTextAlignment(.center)
                            
                            Button("🏪 Vai al Negozio") {
                                gameManager.navigateToScreen(.shop)
                            }
                            .padding()
                            .background(Color.green.opacity(0.2))
                            .cornerRadius(10)
                        }
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                        .padding()
                    } else {
                        LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 2), spacing: 15) {
                            ForEach(filteredItems, id: \.id) { item in
                                InventoryItemCard(
                                    item: item,
                                    onTap: {
                                        selectedItem = item
                                        showingItemDetails = true
                                    },
                                    onEquipToggle: {
                                        toggleEquipment(item)
                                    }
                                )
                            }
                        }
                        .padding()
                    }
                }
                
                // Bottom actions
                HStack(spacing: 20) {
                    Button("🏪 Negozio") {
                        gameManager.navigateToScreen(.shop)
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.green.opacity(0.2))
                    .cornerRadius(10)
                    
                    Button("🎮 Gioco") {
                        gameManager.navigateToScreen(.game)
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.blue.opacity(0.2))
                    .cornerRadius(10)
                }
                .padding()
                .background(Color.black.opacity(0.05))
            }
            .navigationTitle("🎒 Inventario")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Indietro") {
                        gameManager.goBack()
                    }
                }
            }
        }
        .sheet(isPresented: $showingItemDetails) {
            if let item = selectedItem {
                ItemDetailsView(
                    item: item,
                    gameManager: gameManager,
                    onDismiss: { showingItemDetails = false }
                )
            }
        }
    }
    
    private var filteredItems: [InventoryItem] {
        return gameManager.gameState.inventario.items.values
            .filter { $0.equipment.tipo == selectedEquipmentType }
            .sorted { $0.equipment.prezzo > $1.equipment.prezzo }
    }
    
    private func toggleEquipment(_ item: InventoryItem) {
        if item.isEquipped {
            gameManager.gameState.inventario.unequip(item.equipment.nome)
        } else {
            gameManager.gameState.inventario.equip(item.equipment.nome)
        }
        gameManager.saveGame()
        
        // Play sound
        AudioManager.shared.playCollectItemSound()
    }
}

struct EquipmentTypeButton: View {
    let type: EquipmentType
    let isSelected: Bool
    let equippedItem: InventoryItem?
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            VStack(spacing: 8) {
                ZStack {
                    Circle()
                        .fill(isSelected ? Color.blue.opacity(0.3) : Color.gray.opacity(0.1))
                        .frame(width: 60, height: 60)
                    
                    Text(type.emoji)
                        .font(.title2)
                    
                    if equippedItem != nil {
                        VStack {
                            HStack {
                                Spacer()
                                Circle()
                                    .fill(Color.green)
                                    .frame(width: 12, height: 12)
                                    .overlay(
                                        Text("✓")
                                            .font(.caption2)
                                            .fontWeight(.bold)
                                            .foregroundColor(.white)
                                    )
                            }
                            Spacer()
                        }
                    }
                }
                
                Text(type.displayName)
                    .font(.caption)
                    .fontWeight(isSelected ? .semibold : .regular)
                    .foregroundColor(isSelected ? .blue : .secondary)
            }
        }
        .buttonStyle(PlainButtonStyle())
    }
}

struct InventoryItemCard: View {
    let item: InventoryItem
    let onTap: () -> Void
    let onEquipToggle: () -> Void
    
    var body: some View {
        VStack(spacing: 12) {
            // Item header
            HStack {
                Text(item.equipment.emoji)
                    .font(.title2)
                
                Spacer()
                
                if item.quantity > 1 {
                    Text("x\(item.quantity)")
                        .font(.caption)
                        .padding(.horizontal, 6)
                        .padding(.vertical, 2)
                        .background(Color.orange.opacity(0.2))
                        .cornerRadius(4)
                }
            }
            
            // Item name
            Text(item.equipment.nome)
                .font(.subheadline)
                .fontWeight(.semibold)
                .multilineTextAlignment(.center)
                .lineLimit(2)
            
            // Stats
            VStack(spacing: 4) {
                if item.equipment.danno > 0 {
                    HStack {
                        Text("⚔️")
                        Text("+\(item.equipment.danno)")
                            .fontWeight(.medium)
                        Spacer()
                    }
                    .font(.caption)
                }
                
                if item.equipment.difesa > 0 {
                    HStack {
                        Text("🛡️")
                        Text("+\(item.equipment.difesa)")
                            .fontWeight(.medium)
                        Spacer()
                    }
                    .font(.caption)
                }
            }
            
            // Action buttons
            HStack(spacing: 8) {
                Button("Info") {
                    onTap()
                }
                .font(.caption)
                .padding(.horizontal, 8)
                .padding(.vertical, 4)
                .background(Color.gray.opacity(0.2))
                .cornerRadius(6)
                
                Button(item.isEquipped ? "Rimuovi" : "Equipaggia") {
                    onEquipToggle()
                }
                .font(.caption)
                .fontWeight(.semibold)
                .padding(.horizontal, 8)
                .padding(.vertical, 4)
                .background(item.isEquipped ? Color.red.opacity(0.2) : Color.green.opacity(0.2))
                .foregroundColor(item.isEquipped ? .red : .green)
                .cornerRadius(6)
            }
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 12)
                .fill(item.isEquipped ? Color.blue.opacity(0.1) : Color.white.opacity(0.1))
                .overlay(
                    RoundedRectangle(cornerRadius: 12)
                        .stroke(item.isEquipped ? Color.blue.opacity(0.5) : Color.gray.opacity(0.3), lineWidth: item.isEquipped ? 2 : 1)
                )
        )
        .scaleEffect(item.isEquipped ? 1.02 : 1.0)
        .animation(.easeInOut(duration: 0.2), value: item.isEquipped)
    }
}

struct ItemDetailsView: View {
    let item: InventoryItem
    @ObservedObject var gameManager: GameManager
    let onDismiss: () -> Void
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                // Item icon
                Text(item.equipment.emoji)
                    .font(.system(size: 80))
                
                // Item info
                VStack(spacing: 15) {
                    Text(item.equipment.nome)
                        .font(.title)
                        .fontWeight(.bold)
                        .multilineTextAlignment(.center)
                    
                    Text(item.equipment.descrizione)
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                        .multilineTextAlignment(.center)
                    
                    // Stats
                    VStack(spacing: 10) {
                        if item.equipment.danno > 0 {
                            StatRow(icon: "⚔️", label: "Danno", value: "+\(item.equipment.danno)")
                        }
                        
                        if item.equipment.difesa > 0 {
                            StatRow(icon: "🛡️", label: "Difesa", value: "+\(item.equipment.difesa)")
                        }
                        
                        if let bonus = item.equipment.bonus {
                            StatRow(icon: "✨", label: "Bonus", value: bonus)
                        }
                        
                        StatRow(icon: "💰", label: "Valore", value: "\(item.equipment.prezzo) monete")
                        
                        if item.quantity > 1 {
                            StatRow(icon: "📦", label: "Quantità", value: "\(item.quantity)")
                        }
                    }
                }
                
                Spacer()
                
                // Actions
                VStack(spacing: 15) {
                    if item.isEquipped {
                        Button("🔓 Rimuovi Equipaggiamento") {
                            gameManager.gameState.inventario.unequip(item.equipment.nome)
                            gameManager.saveGame()
                            onDismiss()
                        }
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.red.opacity(0.2))
                        .foregroundColor(.red)
                        .cornerRadius(10)
                    } else {
                        Button("⚔️ Equipaggia") {
                            gameManager.gameState.inventario.equip(item.equipment.nome)
                            gameManager.saveGame()
                            onDismiss()
                        }
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.green.opacity(0.2))
                        .foregroundColor(.green)
                        .cornerRadius(10)
                    }
                    
                    Button("💰 Vendi (\(item.equipment.prezzo / 2) monete)") {
                        gameManager.gameState.inventario.sellItem(item.equipment.nome)
                        gameManager.saveGame()
                        AudioManager.shared.playCollectMoneySound()
                        onDismiss()
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.orange.opacity(0.2))
                    .foregroundColor(.orange)
                    .cornerRadius(10)
                }
            }
            .padding()
            .navigationTitle("Dettagli Oggetto")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Chiudi") {
                        onDismiss()
                    }
                }
            }
        }
    }
}

struct StatRow: View {
    let icon: String
    let label: String
    let value: String
    
    var body: some View {
        HStack {
            Text(icon)
                .font(.subheadline)
            
            Text(label)
                .font(.subheadline)
                .foregroundColor(.secondary)
            
            Spacer()
            
            Text(value)
                .font(.subheadline)
                .fontWeight(.medium)
        }
        .padding(.horizontal)
        .padding(.vertical, 8)
        .background(Color.gray.opacity(0.1))
        .cornerRadius(8)
    }
}

#Preview {
    InventoryView(gameManager: GameManager())
}