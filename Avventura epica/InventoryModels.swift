//
//  InventoryModels.swift
//  Avventura epica
//
//  Created by Ambrogio Riili on 27/07/25.
//

import Foundation

// MARK: - Equipment Types
enum EquipmentType: String, CaseIterable {
    case arma = "arma"
    case scudo = "scudo"
    case armatura = "armatura"
    case accessorio = "accessorio"
    
    var displayName: String {
        switch self {
        case .arma: return "Arma"
        case .scudo: return "Scudo"
        case .armatura: return "Armatura"
        case .accessorio: return "Accessorio"
        }
    }
    
    var emoji: String {
        switch self {
        case .arma: return "⚔️"
        case .scudo: return "🛡️"
        case .armatura: return "🦺"
        case .accessorio: return "💍"
        }
    }
}

// MARK: - Equipment Item
struct EquipmentItem: Identifiable, Codable {
    let id = UUID()
    let nome: String
    let tipo: EquipmentType
    let prezzo: Int
    let descrizione: String
    let danno: Int
    let difesa: Int
    let bonus: String?
    
    init(nome: String, tipo: EquipmentType, prezzo: Int, descrizione: String, danno: Int = 0, difesa: Int = 0, bonus: String? = nil) {
        self.nome = nome
        self.tipo = tipo
        self.prezzo = prezzo
        self.descrizione = descrizione
        self.danno = danno
        self.difesa = difesa
        self.bonus = bonus
    }
    
    var displayStats: String {
        var stats: [String] = []
        if danno > 0 { stats.append("+\(danno) danno") }
        if difesa > 0 { stats.append("+\(difesa) difesa") }
        if let bonus = bonus { stats.append(bonus) }
        return stats.joined(separator(", "))
    }
    
    var emoji: String {
        return tipo.emoji
    }
}

// MARK: - Inventory Item
struct InventoryItem: Identifiable, Codable {
    let id = UUID()
    let equipment: EquipmentItem
    var quantity: Int
    var isEquipped: Bool
    
    init(equipment: EquipmentItem, quantity: Int = 1, isEquipped: Bool = false) {
        self.equipment = equipment
        self.quantity = quantity
        self.isEquipped = isEquipped
    }
}

// MARK: - Shop Item
struct ShopItem: Identifiable {
    let id = UUID()
    let equipment: EquipmentItem
    var inStock: Bool
    var recommended: Bool
    
    init(equipment: EquipmentItem, inStock: Bool = true, recommended: Bool = false) {
        self.equipment = equipment
        self.inStock = inStock
        self.recommended = recommended
    }
}

// MARK: - Equipment Stats
struct EquipmentStats: Codable {
    var totalDamage: Int = 0
    var totalDefense: Int = 0
    var specialBonuses: [String] = []
    
    mutating func addEquipment(_ item: EquipmentItem) {
        totalDamage += item.danno
        totalDefense += item.difesa
        if let bonus = item.bonus {
            specialBonuses.append(bonus)
        }
    }
    
    mutating func removeEquipment(_ item: EquipmentItem) {
        totalDamage = max(0, totalDamage - item.danno)
        totalDefense = max(0, totalDefense - item.difesa)
        if let bonus = item.bonus {
            specialBonuses.removeAll { $0 == bonus }
        }
    }
    
    mutating func reset() {
        totalDamage = 0
        totalDefense = 0
        specialBonuses.removeAll()
    }
}

// MARK: - Player Inventory and Equipment
struct PlayerInventory: Codable {
    var items: [String: InventoryItem] = [:]
    var equipped: [EquipmentType: String] = [:]
    var stats: EquipmentStats = EquipmentStats()
    var money: Int = 1000 // Soldi per comprare nel negozio
    
    // MARK: - Equipment Management
    mutating func equip(_ itemName: String) -> Bool {
        guard let inventoryItem = items[itemName],
              !inventoryItem.isEquipped else { return false }
        
        let equipment = inventoryItem.equipment
        
        // Unequip current item of same type
        if let currentEquipped = equipped[equipment.tipo] {
            unequip(currentEquipped)
        }
        
        // Equip new item
        items[itemName]?.isEquipped = true
        equipped[equipment.tipo] = itemName
        stats.addEquipment(equipment)
        
        return true
    }
    
    mutating func unequip(_ itemName: String) -> Bool {
        guard let inventoryItem = items[itemName],
              inventoryItem.isEquipped else { return false }
        
        let equipment = inventoryItem.equipment
        
        items[itemName]?.isEquipped = false
        equipped.removeValue(forKey: equipment.tipo)
        stats.removeEquipment(equipment)
        
        return true
    }
    
    mutating func addItem(_ equipment: EquipmentItem, quantity: Int = 1) {
        if let existingItem = items[equipment.nome] {
            items[equipment.nome]?.quantity += quantity
        } else {
            items[equipment.nome] = InventoryItem(equipment: equipment, quantity: quantity)
        }
    }
    
    mutating func removeItem(_ itemName: String, quantity: Int = 1) -> Bool {
        guard let item = items[itemName],
              item.quantity >= quantity else { return false }
        
        if item.isEquipped && quantity >= item.quantity {
            unequip(itemName)
        }
        
        items[itemName]?.quantity -= quantity
        
        if items[itemName]?.quantity == 0 {
            items.removeValue(forKey: itemName)
        }
        
        return true
    }
    
    mutating func buyItem(_ equipment: EquipmentItem) -> Bool {
        guard money >= equipment.prezzo else { return false }
        
        money -= equipment.prezzo
        addItem(equipment)
        return true
    }
    
    mutating func sellItem(_ itemName: String) -> Bool {
        guard let item = items[itemName] else { return false }
        
        let sellPrice = item.equipment.prezzo / 2 // Vendi a metà prezzo
        
        if item.isEquipped {
            unequip(itemName)
        }
        
        money += sellPrice
        return removeItem(itemName)
    }
    
    func getEquippedItem(_ type: EquipmentType) -> InventoryItem? {
        guard let itemName = equipped[type],
              let item = items[itemName] else { return nil }
        return item
    }
    
    func canAfford(_ price: Int) -> Bool {
        return money >= price
    }
}