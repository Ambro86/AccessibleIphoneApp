import 'package:flutter/material.dart';
import 'dart:math';

void main() {
  runApp(const AdventureGameApp());
}

class AdventureGameApp extends StatelessWidget {
  const AdventureGameApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '🗡️ Dungeon Adventure',
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF8B4513),
          brightness: Brightness.dark,
        ),
      ),
      home: const MenuScreen(),
    );
  }
}

// Modello di gioco
class GameData {
  int playerRow = 0;
  int playerCol = 0;
  int playerHp = 100;
  int maxHp = 100;
  int level = 1;
  int exp = 0;
  int expToNext = 100;
  int gold = 50;
  int attack = 10;
  int defense = 5;
  List<String> inventory = [];
  
  // Oggetti nelle stanze
  Map<String, String> roomItems = {
    'cucina': 'torcia',
    'bagno': 'pettine',
    'salotto': 'libro',
    'camera': 'chiave'
  };
  
  // Mostri nelle stanze
  Map<String, Map<String, int>> monsters = {
    'cucina': {'hp': 15, 'maxHp': 15, 'attack': 8, 'exp': 20, 'gold': 10},
    'bagno': {'hp': 30, 'maxHp': 30, 'attack': 12, 'exp': 35, 'gold': 20},
    'salotto': {'hp': 25, 'maxHp': 25, 'attack': 15, 'exp': 30, 'gold': 15},
    'camera': {'hp': 50, 'maxHp': 50, 'attack': 20, 'exp': 100, 'gold': 50}
  };
  
  bool gameWon = false;
  bool gameOver = false;
}

class MenuScreen extends StatelessWidget {
  const MenuScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Color(0xFF2C1810), Color(0xFF8B4513), Color(0xFF2C1810)],
          ),
        ),
        child: SafeArea(
          child: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Spacer(),
                // Logo
                Container(
                  padding: const EdgeInsets.all(24),
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(20),
                    color: Colors.black.withValues(alpha: 0.4),
                  ),
                  child: const Column(
                    children: [
                      Text(
                        '🗡️',
                        style: TextStyle(fontSize: 60),
                      ),
                      Text(
                        'DUNGEON\nADVENTURE',
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          fontSize: 28,
                          fontWeight: FontWeight.bold,
                          color: Colors.amber,
                          height: 1.2,
                        ),
                      ),
                    ],
                  ),
                ),
                
                const SizedBox(height: 60),
                
                // Pulsanti menu
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 40),
                  child: Column(
                    children: [
                      MenuButton(
                        text: '🆕 Nuovo Gioco',
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => GameScreen(gameData: GameData()),
                            ),
                          );
                        },
                      ),
                      const SizedBox(height: 16),
                      MenuButton(
                        text: '💾 Carica Gioco',
                        onPressed: () {
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(content: Text('💾 Funzione in sviluppo')),
                          );
                        },
                      ),
                      const SizedBox(height: 16),
                      MenuButton(
                        text: '❓ Come Giocare',
                        onPressed: () {
                          showDialog(
                            context: context,
                            builder: (context) => const HelpDialog(),
                          );
                        },
                      ),
                    ],
                  ),
                ),
                
                const Spacer(),
                const Text(
                  'Un\'avventura epica ti aspetta...',
                  style: TextStyle(
                    color: Colors.amber,
                    fontSize: 16,
                    fontStyle: FontStyle.italic,
                  ),
                ),
                const SizedBox(height: 40),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class MenuButton extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;
  
  const MenuButton({
    super.key,
    required this.text,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: double.infinity,
      height: 60,
      child: ElevatedButton(
        onPressed: onPressed,
        style: ElevatedButton.styleFrom(
          backgroundColor: const Color(0xFF8B4513),
          foregroundColor: Colors.white,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(15),
          ),
          elevation: 8,
        ),
        child: Text(
          text,
          style: const TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }
}

class HelpDialog extends StatelessWidget {
  const HelpDialog({super.key});

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      backgroundColor: const Color(0xFF2C1810),
      title: const Text(
        '❓ Come Giocare',
        style: TextStyle(color: Colors.amber),
      ),
      content: const SingleChildScrollView(
        child: Text(
          '🎯 OBIETTIVO:\n'
          'Trova la chiave nella camera da letto!\n\n'
          '🕹️ CONTROLLI:\n'
          '• Muoviti con i pulsanti direzionali\n'
          '• Raccogli oggetti utili\n'
          '• Combatti mostri per EXP e oro\n'
          '• Compra nel negozio per potenziarti\n\n'
          '⚔️ COMBATTIMENTO:\n'
          '• Attacca per sconfiggere i mostri\n'
          '• Sali di livello con l\'esperienza\n'
          '• Usa pozioni per curarti\n\n'
          '🏪 NEGOZIO:\n'
          '• Compra armi, armature e pozioni\n'
          '• Migliora le tue statistiche\n'
          '• Spendi l\'oro guadagnato\n\n'
          '💡 SUGGERIMENTO:\n'
          'Esplora tutto e potenziati prima del boss finale!',
          style: TextStyle(color: Colors.white),
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: const Text(
            'Capito!',
            style: TextStyle(color: Colors.amber),
          ),
        ),
      ],
    );
  }
}

class GameScreen extends StatefulWidget {
  final GameData gameData;
  
  const GameScreen({super.key, required this.gameData});

  @override
  GameScreenState createState() => GameScreenState();
}

class GameScreenState extends State<GameScreen> {
  late GameData game;
  String statusMessage = '';
  String combatLog = '';
  
  final List<List<String>> gameMap = [
    ['cucina', 'bagno'],
    ['salotto', 'camera']
  ];
  
  final Map<String, String> roomNames = {
    'cucina': '🍳 Cucina',
    'bagno': '🚿 Bagno', 
    'salotto': '🛋️ Salotto',
    'camera': '🛏️ Camera da Letto'
  };
  
  final Map<String, String> roomDescriptions = {
    'cucina': 'Una cucina medievale con pentole fumanti...',
    'bagno': 'Un bagno antico con specchi appannati.',
    'salotto': 'Un salotto buio pieno di mobili polverosi.',
    'camera': 'Una camera da letto lugubre con un letto a baldacchino.'
  };

  final Map<String, String> monsterNames = {
    'cucina': '🐀 Ratto Gigante',
    'bagno': '🧟 Zombie Putrefatto',
    'salotto': '💀 Scheletro Guerriero', 
    'camera': '🧛 Vampiro Antico'
  };

  @override
  void initState() {
    super.initState();
    game = widget.gameData;
    statusMessage = 'Benvenuto nel dungeon! Trova la chiave per vincere!';
  }

  String getCurrentRoom() {
    return gameMap[game.playerRow][game.playerCol];
  }

  void movePlayer(String direction) {
    int newRow = game.playerRow;
    int newCol = game.playerCol;
    
    switch (direction) {
      case 'nord':
        if (newRow > 0) {
          newRow--;
        } else {
          setState(() {
            statusMessage = '🚫 Non puoi andare a nord!';
          });
          return;
        }
        break;
      case 'sud':
        if (newRow < 1) {
          newRow++;
        } else {
          setState(() {
            statusMessage = '🚫 Non puoi andare a sud!';
          });
          return;
        }
        break;
      case 'ovest':
        if (newCol > 0) {
          newCol--;
        } else {
          setState(() {
            statusMessage = '🚫 Non puoi andare a ovest!';
          });
          return;
        }
        break;
      case 'est':
        if (newCol < 1) {
          newCol++;
        } else {
          setState(() {
            statusMessage = '🚫 Non puoi andare a est!';
          });
          return;
        }
        break;
    }
    
    setState(() {
      game.playerRow = newRow;
      game.playerCol = newCol;
      String room = getCurrentRoom();
      statusMessage = 'Ti sei spostato in: ${roomNames[room]}';
      combatLog = '';
    });
  }

  void collectItem() {
    String room = getCurrentRoom();
    String? item = game.roomItems[room];
    
    if (item != null && item.isNotEmpty) {
      setState(() {
        game.inventory.add(item);
        game.roomItems[room] = '';
        statusMessage = '🎒 Hai raccolto: $item!';
        
        if (item == 'chiave') {
          game.gameWon = true;
          statusMessage = '🏆 HAI VINTO! Hai trovato la chiave del dungeon!';
        }
      });
    } else {
      setState(() {
        statusMessage = '❌ Non c\'è nulla da raccogliere qui.';
      });
    }
  }

  void attackMonster() {
    String room = getCurrentRoom();
    Map<String, int>? monster = game.monsters[room];
    
    if (monster == null || monster['hp']! <= 0) {
      setState(() {
        statusMessage = '👻 Non ci sono mostri da attaccare qui!';
      });
      return;
    }
    
    // Attacco del giocatore
    int damage = game.attack + Random().nextInt(8);
    monster['hp'] = monster['hp']! - damage;
    
    String battleText = '⚔️ Hai inflitto $damage danni al ${monsterNames[room]}!\n';
    
    if (monster['hp']! <= 0) {
      // Mostro sconfitto
      int expGained = monster['exp']!;
      int goldGained = monster['gold']!;
      
      setState(() {
        game.exp += expGained;
        game.gold += goldGained;
        statusMessage = '🎉 Hai sconfitto il ${monsterNames[room]}!';
        combatLog = '$battleText💰 +$goldGained oro, ⭐ +$expGained EXP';
        
        // Rimuovi mostro
        game.monsters.remove(room);
        
        // Controlla level up
        checkLevelUp();
      });
    } else {
      // Mostro contrattacca
      int monsterDamage = (monster['attack']! - game.defense + Random().nextInt(5)).clamp(1, 999);
      
      setState(() {
        game.playerHp -= monsterDamage;
        combatLog = '$battleText🩸 Il ${monsterNames[room]!} ti infligge $monsterDamage danni!';
        
        if (game.playerHp <= 0) {
          game.gameOver = true;
          statusMessage = '💀 GAME OVER! Sei stato sconfitto!';
          game.playerHp = 0;
        } else {
          statusMessage = '⚔️ Battaglia in corso! HP: ${game.playerHp}/${game.maxHp}';
        }
      });
    }
  }

  void checkLevelUp() {
    if (game.exp >= game.expToNext) {
      setState(() {
        game.level++;
        game.exp -= game.expToNext;
        game.expToNext = (game.expToNext * 1.5).round();
        game.maxHp += 20;
        game.playerHp = game.maxHp; // Guarigione completa
        game.attack += 3;
        game.defense += 2;
        statusMessage = '🎊 LEVEL UP! Ora sei livello ${game.level}!';
      });
    }
  }

  void usePotion() {
    if (game.inventory.contains('Pozione Vita')) {
      setState(() {
        game.inventory.remove('Pozione Vita');
        game.playerHp = (game.playerHp + 30).clamp(0, game.maxHp);
        statusMessage = '🧪 Hai usato una Pozione Vita! HP: ${game.playerHp}/${game.maxHp}';
      });
    } else {
      setState(() {
        statusMessage = '❌ Non hai pozioni da usare!';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    String currentRoom = getCurrentRoom();
    Map<String, int>? currentMonster = game.monsters[currentRoom];
    String? currentItem = game.roomItems[currentRoom];
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('🗡️ Dungeon Adventure'),
        backgroundColor: const Color(0xFF8B4513),
        actions: [
          IconButton(
            icon: const Icon(Icons.shop),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => ShopScreen(gameData: game),
                ),
              ).then((_) => setState(() {}));
            },
          ),
        ],
      ),
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Color(0xFF1A1A1A), Color(0xFF2C1810)],
          ),
        ),
        child: Column(
          children: [
            // Status del giocatore
            Container(
              padding: const EdgeInsets.all(16),
              color: Colors.black.withValues(alpha: 0.3),
              child: Row(
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '⚔️ Livello ${game.level} | 💰 ${game.gold} oro',
                          style: const TextStyle(
                            color: Colors.amber,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 4),
                        LinearProgressIndicator(
                          value: game.playerHp / game.maxHp,
                          backgroundColor: Colors.red.withValues(alpha: 0.3),
                          valueColor: const AlwaysStoppedAnimation<Color>(Colors.red),
                        ),
                        Text(
                          '❤️ ${game.playerHp}/${game.maxHp}',
                          style: const TextStyle(color: Colors.white, fontSize: 12),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '⭐ EXP: ${game.exp}/${game.expToNext}',
                          style: const TextStyle(
                            color: Colors.cyan,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 4),
                        LinearProgressIndicator(
                          value: game.exp / game.expToNext,
                          backgroundColor: Colors.cyan.withValues(alpha: 0.3),
                          valueColor: const AlwaysStoppedAnimation<Color>(Colors.cyan),
                        ),
                        Text(
                          '🗡️ ATK: ${game.attack} | 🛡️ DEF: ${game.defense}',
                          style: const TextStyle(color: Colors.white, fontSize: 12),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            
            Expanded(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  children: [
                    // Descrizione stanza
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: Colors.black.withValues(alpha: 0.5),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            roomNames[currentRoom]!,
                            style: const TextStyle(
                              fontSize: 20,
                              fontWeight: FontWeight.bold,
                              color: Colors.amber,
                            ),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            roomDescriptions[currentRoom]!,
                            style: const TextStyle(color: Colors.white, fontSize: 16),
                          ),
                          if (currentItem != null && currentItem.isNotEmpty) ...[
                            const SizedBox(height: 8),
                            Text(
                              '✨ Vedi: $currentItem',
                              style: const TextStyle(color: Colors.yellow),
                            ),
                          ],
                          if (currentMonster != null && currentMonster['hp']! > 0) ...[
                            const SizedBox(height: 8),
                            Container(
                              padding: const EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: Colors.red.withValues(alpha: 0.2),
                                borderRadius: BorderRadius.circular(8),
                                border: Border.all(color: Colors.red),
                              ),
                              child: Column(
                                children: [
                                  Text(
                                    '${monsterNames[currentRoom]} appare!',
                                    style: const TextStyle(
                                      color: Colors.red,
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                  const SizedBox(height: 4),
                                  LinearProgressIndicator(
                                    value: currentMonster['hp']! / currentMonster['maxHp']!,
                                    backgroundColor: Colors.red.withValues(alpha: 0.3),
                                    valueColor: const AlwaysStoppedAnimation<Color>(Colors.red),
                                  ),
                                  Text(
                                    'HP: ${currentMonster['hp']}/${currentMonster['maxHp']}',
                                    style: const TextStyle(color: Colors.white, fontSize: 12),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ],
                      ),
                    ),
                    
                    const SizedBox(height: 16),
                    
                    // Messaggi
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: Colors.blue.withValues(alpha: 0.2),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Column(
                        children: [
                          Text(
                            statusMessage,
                            style: const TextStyle(color: Colors.white, fontSize: 14),
                          ),
                          if (combatLog.isNotEmpty) ...[
                            const SizedBox(height: 8),
                            Text(
                              combatLog,
                              style: const TextStyle(color: Colors.orange, fontSize: 12),
                            ),
                          ],
                        ],
                      ),
                    ),
                    
                    const Spacer(),
                    
                    // Controlli movimento
                    GameButton(
                      text: '⬆️ Nord',
                      onPressed: () => movePlayer('nord'),
                    ),
                    const SizedBox(height: 8),
                    Row(
                      children: [
                        Expanded(
                          child: GameButton(
                            text: '⬅️ Ovest',
                            onPressed: () => movePlayer('ovest'),
                          ),
                        ),
                        const SizedBox(width: 8),
                        Expanded(
                          child: GameButton(
                            text: '➡️ Est',
                            onPressed: () => movePlayer('est'),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    GameButton(
                      text: '⬇️ Sud',
                      onPressed: () => movePlayer('sud'),
                    ),
                    
                    const SizedBox(height: 16),
                    
                    // Azioni
                    Row(
                      children: [
                        Expanded(
                          child: GameButton(
                            text: '🎒 Raccogli',
                            onPressed: collectItem,
                          ),
                        ),
                        const SizedBox(width: 8),
                        Expanded(
                          child: GameButton(
                            text: '⚔️ Attacca',
                            onPressed: attackMonster,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    Row(
                      children: [
                        Expanded(
                          child: GameButton(
                            text: '🧪 Pozione',
                            onPressed: usePotion,
                          ),
                        ),
                        const SizedBox(width: 8),
                        Expanded(
                          child: GameButton(
                            text: '👜 Inventario',
                            onPressed: () {
                              showDialog(
                                context: context,
                                builder: (context) => InventoryDialog(inventory: game.inventory),
                              );
                            },
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class GameButton extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;
  
  const GameButton({
    super.key,
    required this.text,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 45,
      child: ElevatedButton(
        onPressed: onPressed,
        style: ElevatedButton.styleFrom(
          backgroundColor: const Color(0xFF8B4513),
          foregroundColor: Colors.white,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(10),
          ),
        ),
        child: Text(
          text,
          style: const TextStyle(fontSize: 14),
        ),
      ),
    );
  }
}

class InventoryDialog extends StatelessWidget {
  final List<String> inventory;
  
  const InventoryDialog({super.key, required this.inventory});

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      backgroundColor: const Color(0xFF2C1810),
      title: const Text(
        '🎒 Inventario',
        style: TextStyle(color: Colors.amber),
      ),
      content: SizedBox(
        width: double.maxFinite,
        height: 200,
        child: inventory.isEmpty
            ? const Center(
                child: Text(
                  'Inventario vuoto',
                  style: TextStyle(color: Colors.white),
                ),
              )
            : ListView.builder(
                itemCount: inventory.length,
                itemBuilder: (context, index) {
                  return ListTile(
                    leading: const Icon(Icons.inventory, color: Colors.amber),
                    title: Text(
                      inventory[index],
                      style: const TextStyle(color: Colors.white),
                    ),
                  );
                },
              ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: const Text(
            'Chiudi',
            style: TextStyle(color: Colors.amber),
          ),
        ),
      ],
    );
  }
}

class ShopScreen extends StatefulWidget {
  final GameData gameData;
  
  const ShopScreen({super.key, required this.gameData});

  @override
  ShopScreenState createState() => ShopScreenState();
}

class ShopScreenState extends State<ShopScreen> {
  final Map<String, Map<String, dynamic>> shopItems = {
    'Pozione Vita': {'price': 25, 'type': 'potion', 'effect': 30, 'emoji': '🧪'},
    'Spada di Ferro': {'price': 100, 'type': 'weapon', 'effect': 5, 'emoji': '⚔️'},
    'Armatura di Cuoio': {'price': 80, 'type': 'armor', 'effect': 3, 'emoji': '🛡️'},
    'Anello Magico': {'price': 150, 'type': 'magic', 'effect': 10, 'emoji': '💍'},
  };

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('🏪 Negozio del Dungeon'),
        backgroundColor: const Color(0xFF8B4513),
      ),
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Color(0xFF1A1A1A), Color(0xFF2C1810)],
          ),
        ),
        child: Column(
          children: [
            // Status oro
            Container(
              padding: const EdgeInsets.all(16),
              color: Colors.black.withValues(alpha: 0.3),
              child: Row(
                children: [
                  const Icon(Icons.account_balance_wallet, color: Colors.amber),
                  const SizedBox(width: 8),
                  Text(
                    '💰 ${widget.gameData.gold} oro',
                    style: const TextStyle(
                      color: Colors.amber,
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ),
            
            // Lista oggetti
            Expanded(
              child: ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: shopItems.length,
                itemBuilder: (context, index) {
                  String itemName = shopItems.keys.elementAt(index);
                  Map<String, dynamic> item = shopItems[itemName]!;
                  bool canAfford = widget.gameData.gold >= item['price'];
                  
                  return Card(
                    color: const Color(0xFF3D2817),
                    margin: const EdgeInsets.only(bottom: 8),
                    child: ListTile(
                      leading: Text(
                        item['emoji'],
                        style: const TextStyle(fontSize: 24),
                      ),
                      title: Text(
                        itemName,
                        style: const TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      subtitle: Text(
                        'Prezzo: ${item['price']} oro\nEffetto: +${item['effect']}',
                        style: const TextStyle(color: Colors.grey),
                      ),
                      trailing: ElevatedButton(
                        onPressed: canAfford
                            ? () {
                                setState(() {
                                  widget.gameData.gold -= (item['price'] as int);
                                  
                                  switch (item['type']) {
                                    case 'potion':
                                      widget.gameData.inventory.add(itemName);
                                      break;
                                    case 'weapon':
widget.gameData.attack += (item['effect'] as int);
widget.gameData.inventory.add(itemName);
break;
case 'armor':
widget.gameData.defense += (item['effect'] as int);
widget.gameData.inventory.add(itemName);
break;
case 'magic':
widget.gameData.attack += (item['effect'] as int) ~/ 2;
widget.gameData.defense += (item['effect'] as int) ~/ 2;
                                      widget.gameData.inventory.add(itemName);
                                      break;
                                  }
                                });
                                
                                ScaffoldMessenger.of(context).showSnackBar(
                                  SnackBar(
                                    content: Text('🛒 Hai comprato: $itemName!'),
                                  ),
                                );
                              }
                            : null,
                       style: ElevatedButton.styleFrom(
                         backgroundColor: canAfford
                             ? const Color(0xFF8B4513)
                             : Colors.grey,
                       ),
                       child: const Text(
                         'Compra',
                         style: TextStyle(color: Colors.white),
                       ),
                     ),
                   ),
                 );
               },
             ),
           ),
         ],
       ),
     ),
   );
 }
}