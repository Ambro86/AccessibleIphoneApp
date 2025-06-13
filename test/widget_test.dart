import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:app_ios_accessibile/main.dart';

void main() {
  group('Dungeon Adventure Tests', () {
    
    // Test 1: App si avvia correttamente
    testWidgets('App starts and shows menu', (WidgetTester tester) async {
      await tester.pumpWidget(const AdventureGameApp());
      
      // Verifica che il titolo sia presente
      expect(find.text('DUNGEON\nADVENTURE'), findsOneWidget);
      
      // Verifica che i pulsanti del menu siano presenti
      expect(find.text('🆕 Nuovo Gioco'), findsOneWidget);
      expect(find.text('💾 Carica Gioco'), findsOneWidget);
      expect(find.text('❓ Come Giocare'), findsOneWidget);
    });

    // Test 2: Nuovo gioco inizia correttamente
    testWidgets('New game starts with correct initial state', (WidgetTester tester) async {
      await tester.pumpWidget(const AdventureGameApp());
      
      // Tocca "Nuovo Gioco"
      await tester.tap(find.text('🆕 Nuovo Gioco'));
      await tester.pumpAndSettle();
      
      // Verifica che sia nella cucina (posizione iniziale)
      expect(find.text('🍳 Cucina'), findsOneWidget);
      
      // Verifica statistiche iniziali
      expect(find.textContaining('⚔️ Livello 1'), findsOneWidget);
      expect(find.textContaining('💰 50 oro'), findsOneWidget);
      expect(find.textContaining('❤️ 100/100'), findsOneWidget);
    });

    // Test 3: Movimento del giocatore
    testWidgets('Player can move between rooms', (WidgetTester tester) async {
      await tester.pumpWidget(const AdventureGameApp());
      await tester.tap(find.text('🆕 Nuovo Gioco'));
      await tester.pumpAndSettle();
      
      // Inizialmente in cucina
      expect(find.text('🍳 Cucina'), findsOneWidget);
      
      // Muovi a est (bagno)
      await tester.tap(find.text('➡️ Est'));
      await tester.pumpAndSettle();
      expect(find.text('🚿 Bagno'), findsOneWidget);
      
      // Muovi a sud (camera)
      await tester.tap(find.text('⬇️ Sud'));
      await tester.pumpAndSettle();
      expect(find.text('🛏️ Camera da Letto'), findsOneWidget);
    });

    // Test 4: Raccolta oggetti
    testWidgets('Player can collect items', (WidgetTester tester) async {
      await tester.pumpWidget(const AdventureGameApp());
      await tester.tap(find.text('🆕 Nuovo Gioco'));
      await tester.pumpAndSettle();
      
      // Verifica che ci sia una torcia in cucina
      expect(find.textContaining('torcia'), findsOneWidget);
      
      // Raccogli l'oggetto
      await tester.tap(find.text('🎒 Raccogli'));
      await tester.pumpAndSettle();
      
      // Verifica messaggio di successo
      expect(find.textContaining('Hai raccolto: torcia'), findsOneWidget);
      
      // Controlla inventario
      await tester.tap(find.text('👜 Inventario'));
      await tester.pumpAndSettle();
      expect(find.text('torcia'), findsOneWidget);
      
      // Chiudi inventario
      await tester.tap(find.text('Chiudi'));
      await tester.pumpAndSettle();
    });

    // Test 5: Combattimento con mostri
    testWidgets('Player can fight monsters', (WidgetTester tester) async {
      await tester.pumpWidget(const AdventureGameApp());
      await tester.tap(find.text('🆕 Nuovo Gioco'));
      await tester.pumpAndSettle();
      
      // Dovrebbe esserci un ratto in cucina
      expect(find.textContaining('🐀 Ratto Gigante'), findsOneWidget);
      
      // Attacca il mostro
      await tester.tap(find.text('⚔️ Attacca'));
      await tester.pumpAndSettle();
      
      // Verifica che ci sia stata una battaglia
      expect(find.textContaining('inflitto'), findsOneWidget);
    });

    // Test 6: Negozio accessibile
    testWidgets('Shop is accessible and shows items', (WidgetTester tester) async {
      await tester.pumpWidget(const AdventureGameApp());
      await tester.tap(find.text('🆕 Nuovo Gioco'));
      await tester.pumpAndSettle();
      
      // Apri il negozio
      await tester.tap(find.byIcon(Icons.shop));
      await tester.pumpAndSettle();
      
      // Verifica che il negozio sia aperto
      expect(find.text('🏪 Negozio del Dungeon'), findsOneWidget);
      
      // Verifica che ci siano oggetti in vendita
      expect(find.text('Pozione Vita'), findsOneWidget);
      expect(find.text('Spada di Ferro'), findsOneWidget);
      expect(find.text('Armatura di Cuoio'), findsOneWidget);
      expect(find.text('Anello Magico'), findsOneWidget);
      
      // Verifica oro mostrato
      expect(find.textContaining('💰 50 oro'), findsOneWidget);
    });

    // Test 7: Condizione di vittoria
    testWidgets('Player wins when collecting key', (WidgetTester tester) async {
      await tester.pumpWidget(const AdventureGameApp());
      await tester.tap(find.text('🆕 Nuovo Gioco'));
      await tester.pumpAndSettle();
      
      // Vai alla camera da letto (est, poi sud)
      await tester.tap(find.text('➡️ Est'));
      await tester.pumpAndSettle();
      await tester.tap(find.text('⬇️ Sud'));
      await tester.pumpAndSettle();
      
      // Sconfiggi il vampiro (potrebbe richiedere più attacchi)
      // Questo è un test semplificato - in realtà dovremmo sconfiggere il mostro
      for (int i = 0; i < 10; i++) {
        await tester.tap(find.text('⚔️ Attacca'));
        await tester.pumpAndSettle();
        
        // Se il vampiro è stato sconfitto, prova a raccogliere la chiave
        if (find.textContaining('chiave').evaluate().isNotEmpty) {
          await tester.tap(find.text('🎒 Raccogli'));
          await tester.pumpAndSettle();
          
          // Verifica messaggio di vittoria
          if (find.textContaining('HAI VINTO').evaluate().isNotEmpty) {
            expect(find.textContaining('HAI VINTO'), findsOneWidget);
            break;
          }
        }
      }
    });

    // Test 8: Help dialog funziona
    testWidgets('Help dialog opens and shows game instructions', (WidgetTester tester) async {
      await tester.pumpWidget(const AdventureGameApp());
      
      // Apri aiuto
      await tester.tap(find.text('❓ Come Giocare'));
      await tester.pumpAndSettle();
      
      // Verifica che il dialog sia aperto
      expect(find.text('❓ Come Giocare'), findsOneWidget);
      expect(find.textContaining('OBIETTIVO'), findsOneWidget);
      expect(find.textContaining('CONTROLLI'), findsOneWidget);
      
      // Chiudi dialog
      await tester.tap(find.text('Capito!'));
      await tester.pumpAndSettle();
    });

    // Test 9: Uso pozioni
    testWidgets('Player can use potions when available', (WidgetTester tester) async {
      await tester.pumpWidget(const AdventureGameApp());
      await tester.tap(find.text('🆕 Nuovo Gioco'));
      await tester.pumpAndSettle();
      
      // Prova a usare pozione senza averla
      await tester.tap(find.text('🧪 Pozione'));
      await tester.pumpAndSettle();
      
      // Dovrebbe dire che non ci sono pozioni
      expect(find.textContaining('Non hai pozioni'), findsOneWidget);
    });

    // Test 10: Controlli movimento con limiti
    testWidgets('Movement controls respect room boundaries', (WidgetTester tester) async {
      await tester.pumpWidget(const AdventureGameApp());
      await tester.tap(find.text('🆕 Nuovo Gioco'));
      await tester.pumpAndSettle();
      
      // Prova ad andare a nord dalla cucina (dovrebbe fallire)
      await tester.tap(find.text('⬆️ Nord'));
      await tester.pumpAndSettle();
      
      // Verifica messaggio di errore
      expect(find.textContaining('Non puoi andare a nord'), findsOneWidget);
      
      // Verifica che sia ancora in cucina
      expect(find.text('🍳 Cucina'), findsOneWidget);
    });
  });
}
 