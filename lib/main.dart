import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/services.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'App Accessibile iOS',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        // Ottimizzato per iOS con San Francisco font
        brightness: Brightness.light,
        fontFamily: '.SF Pro Text', // Font nativo iOS
        textTheme: TextTheme(
          bodyLarge: TextStyle(fontSize: 18),
          bodyMedium: TextStyle(fontSize: 16),
          titleLarge: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
        ),
        // Stile iOS per gli elementi dell'interfaccia
        appBarTheme: AppBarTheme(
          systemOverlayStyle: SystemUiOverlayStyle.light,
          elevation: 0,
          scrolledUnderElevation: 0,
        ),
        tabBarTheme: TabBarThemeData(
          indicatorSize: TabBarIndicatorSize.label,
          labelStyle: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
        ),
      ),
      home: MainScreen(),
    );
  }
}

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  MainScreenState createState() => MainScreenState();
}

class MainScreenState extends State<MainScreen> with TickerProviderStateMixin {
  late TabController _tabController;
  String _statusMessage = 'Benvenuto nell\'app!';

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 4, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  void _updateStatus(String message) {
    setState(() {
      _statusMessage = message;
    });
    // Feedback aptico per iOS
    HapticFeedback.lightImpact();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'App iOS Accessibile',
          semanticsLabel: 'Titolo applicazione: App iOS Accessibile',
        ),
        backgroundColor: CupertinoColors.systemBlue,
        foregroundColor: Colors.white,
        centerTitle: true, // Stile iOS
        bottom: TabBar(
          controller: _tabController,
          indicatorColor: Colors.white,
          labelColor: Colors.white,
          unselectedLabelColor: Colors.white70,
          indicatorWeight: 3,
          tabs: [
            Tab(
              icon: Icon(CupertinoIcons.home, semanticLabel: 'Scheda Home'),
              text: 'Home',
            ),
            Tab(
              icon: Icon(CupertinoIcons.heart_fill, semanticLabel: 'Scheda Preferiti'),
              text: 'Preferiti',
            ),
            Tab(
              icon: Icon(CupertinoIcons.settings, semanticLabel: 'Scheda Impostazioni'),
              text: 'Impostazioni',
            ),
            Tab(
              icon: Icon(CupertinoIcons.info_circle, semanticLabel: 'Scheda Informazioni'),
              text: 'Info',
            ),
          ],
        ),
      ),
      body: Column(
        children: [
          // Barra di stato accessibile
          Container(
            width: double.infinity,
            padding: EdgeInsets.all(16),
            color: Colors.grey[100],
            child: Text(
              _statusMessage,
              style: Theme.of(context).textTheme.bodyMedium,
              semanticsLabel: 'Messaggio di stato: $_statusMessage',
            ),
          ),
          Expanded(
            child: TabBarView(
              controller: _tabController,
              children: [
                HomeTab(onStatusUpdate: _updateStatus),
                FavoritesTab(onStatusUpdate: _updateStatus),
                SettingsTab(onStatusUpdate: _updateStatus),
                InfoTab(onStatusUpdate: _updateStatus),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class HomeTab extends StatelessWidget {
  const HomeTab({super.key, required this.onStatusUpdate});

  final Function(String) onStatusUpdate;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text(
            'Benvenuto nella Home',
            style: Theme.of(context).textTheme.titleLarge,
            textAlign: TextAlign.center,
            semanticsLabel: 'Titolo sezione: Benvenuto nella Home',
          ),
          SizedBox(height: 24),
          
          // Pulsanti principali con icone iOS
          AccessibleButton(
            text: 'Inizia',
            icon: CupertinoIcons.play_fill,
            color: CupertinoColors.systemGreen,
            onPressed: () => onStatusUpdate('Avvio in corso...'),
            semanticsLabel: 'Pulsante Inizia - Avvia l\'applicazione',
          ),
          SizedBox(height: 12),
          
          AccessibleButton(
            text: 'Carica Dati',
            icon: CupertinoIcons.cloud_download,
            color: CupertinoColors.systemBlue,
            onPressed: () => onStatusUpdate('Caricamento dati...'),
            semanticsLabel: 'Pulsante Carica Dati - Scarica informazioni dal server',
          ),
          SizedBox(height: 12),
          
          AccessibleButton(
            text: 'Sincronizza',
            icon: CupertinoIcons.arrow_2_circlepath,
            color: CupertinoColors.systemOrange,
            onPressed: () => onStatusUpdate('Sincronizzazione in corso...'),
            semanticsLabel: 'Pulsante Sincronizza - Aggiorna i dati locali',
          ),
          SizedBox(height: 24),
          
          // Sezione azioni rapide
          Text(
            'Azioni Rapide',
            style: Theme.of(context).textTheme.titleMedium,
            semanticsLabel: 'Sezione Azioni Rapide',
          ),
          SizedBox(height: 16),
          
          Row(
            children: [
              Expanded(
                child: AccessibleButton(
                  text: 'Scan',
                  icon: CupertinoIcons.qrcode_viewfinder,
                  color: CupertinoColors.systemPurple,
                  onPressed: () => onStatusUpdate('Scanner attivato'),
                  semanticsLabel: 'Pulsante Scan - Attiva scanner QR',
                ),
              ),
              SizedBox(width: 12),
              Expanded(
                child: AccessibleButton(
                  text: 'Foto',
                  icon: CupertinoIcons.camera_fill,
                  color: CupertinoColors.systemTeal,
                  onPressed: () => onStatusUpdate('Fotocamera aperta'),
                  semanticsLabel: 'Pulsante Foto - Apri fotocamera',
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class FavoritesTab extends StatefulWidget {
  const FavoritesTab({super.key, required this.onStatusUpdate});

  final Function(String) onStatusUpdate;

  @override
  FavoritesTabState createState() => FavoritesTabState();
}

class FavoritesTabState extends State<FavoritesTab> {
  List<String> favorites = ['Elemento 1', 'Elemento 2', 'Elemento 3'];

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text(
            'I Tuoi Preferiti',
            style: Theme.of(context).textTheme.titleLarge,
            textAlign: TextAlign.center,
            semanticsLabel: 'Titolo sezione: I Tuoi Preferiti',
          ),
          SizedBox(height: 24),
          
          AccessibleButton(
            text: 'Aggiungi Preferito',
            icon: Icons.add,
            color: Colors.green,
            onPressed: () {
              setState(() {
                favorites.add('Nuovo elemento ${favorites.length + 1}');
              });
              widget.onStatusUpdate('Preferito aggiunto');
            },
            semanticsLabel: 'Pulsante Aggiungi Preferito - Aggiunge un nuovo elemento ai preferiti',
          ),
          SizedBox(height: 16),
          
          AccessibleButton(
            text: 'Ordina Preferiti',
            icon: Icons.sort,
            color: Colors.blue,
            onPressed: () {
              setState(() {
                favorites.sort();
              });
              widget.onStatusUpdate('Preferiti ordinati');
            },
            semanticsLabel: 'Pulsante Ordina Preferiti - Riordina gli elementi in ordine alfabetico',
          ),
          SizedBox(height: 24),
          
          Text(
            'Lista Preferiti (${favorites.length} elementi)',
            style: Theme.of(context).textTheme.titleMedium,
            semanticsLabel: 'Lista Preferiti con ${favorites.length} elementi',
          ),
          SizedBox(height: 16),
          
          Expanded(
            child: ListView.builder(
              itemCount: favorites.length,
              itemBuilder: (context, index) {
                return Card(
                  margin: EdgeInsets.only(bottom: 8),
                  child: ListTile(
                    leading: Icon(Icons.favorite, color: Colors.red),
                    title: Text(
                      favorites[index],
                      semanticsLabel: 'Elemento preferito: ${favorites[index]}',
                    ),
                    trailing: IconButton(
                      icon: Icon(Icons.delete, color: Colors.grey[600]),
                      onPressed: () {
                        setState(() {
                          favorites.removeAt(index);
                        });
                        widget.onStatusUpdate('Preferito rimosso');
                      },
                      tooltip: 'Rimuovi ${favorites[index]}',
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

class SettingsTab extends StatefulWidget {
  const SettingsTab({super.key, required this.onStatusUpdate});

  final Function(String) onStatusUpdate;

  @override
  SettingsTabState createState() => SettingsTabState();
}

class SettingsTabState extends State<SettingsTab> {
  bool _notificationsEnabled = true;
  bool _darkMode = false;
  double _fontSize = 16.0;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text(
            'Impostazioni',
            style: Theme.of(context).textTheme.titleLarge,
            textAlign: TextAlign.center,
            semanticsLabel: 'Titolo sezione: Impostazioni',
          ),
          SizedBox(height: 24),
          
          // Toggle per notifiche
          Card(
            child: SwitchListTile(
              title: Text('Notifiche'),
              subtitle: Text('Ricevi notifiche push'),
              value: _notificationsEnabled,
              onChanged: (bool value) {
                setState(() {
                  _notificationsEnabled = value;
                });
                widget.onStatusUpdate(
                  'Notifiche ${value ? 'attivate' : 'disattivate'}'
                );
              },
              secondary: Icon(Icons.notifications),
            ),
          ),
          SizedBox(height: 12),
          
          // Toggle per modalità scura
          Card(
            child: SwitchListTile(
              title: Text('Modalità Scura'),
              subtitle: Text('Tema scuro per l\'interfaccia'),
              value: _darkMode,
              onChanged: (bool value) {
                setState(() {
                  _darkMode = value;
                });
                widget.onStatusUpdate(
                  'Modalità scura ${value ? 'attivata' : 'disattivata'}'
                );
              },
              secondary: Icon(Icons.dark_mode),
            ),
          ),
          SizedBox(height: 24),
          
          // Slider per dimensione font
          Text(
            'Dimensione Testo: ${_fontSize.round()}px',
            style: Theme.of(context).textTheme.titleMedium,
            semanticsLabel: 'Dimensione testo impostata a ${_fontSize.round()} pixel',
          ),
          Slider(
            value: _fontSize,
            min: 12.0,
            max: 24.0,
            divisions: 12,
            label: '${_fontSize.round()}px',
            onChanged: (double value) {
              setState(() {
                _fontSize = value;
              });
            },
            onChangeEnd: (double value) {
              widget.onStatusUpdate('Dimensione testo: ${value.round()}px');
            },
            semanticFormatterCallback: (double value) {
              return 'Dimensione testo ${value.round()} pixel';
            },
          ),
          SizedBox(height: 24),
          
          AccessibleButton(
            text: 'Salva Impostazioni',
            icon: Icons.save,
            color: Colors.green,
            onPressed: () => widget.onStatusUpdate('Impostazioni salvate'),
            semanticsLabel: 'Pulsante Salva Impostazioni - Conferma e salva le modifiche',
          ),
          SizedBox(height: 12),
          
          AccessibleButton(
            text: 'Ripristina Default',
            icon: Icons.restore,
            color: Colors.orange,
            onPressed: () {
              setState(() {
                _notificationsEnabled = true;
                _darkMode = false;
                _fontSize = 16.0;
              });
              widget.onStatusUpdate('Impostazioni ripristinate');
            },
            semanticsLabel: 'Pulsante Ripristina Default - Reimposta tutte le impostazioni ai valori predefiniti',
          ),
        ],
      ),
    );
  }
}

class InfoTab extends StatelessWidget {
  const InfoTab({super.key, required this.onStatusUpdate});

  final Function(String) onStatusUpdate;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text(
            'Informazioni',
            style: Theme.of(context).textTheme.titleLarge,
            textAlign: TextAlign.center,
            semanticsLabel: 'Titolo sezione: Informazioni',
          ),
          SizedBox(height: 24),
          
          Card(
            child: Padding(
              padding: EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'App Flutter Accessibile',
                    style: Theme.of(context).textTheme.titleMedium,
                    semanticsLabel: 'Nome applicazione: App Flutter Accessibile',
                  ),
                  SizedBox(height: 8),
                  Text('Versione: 1.0.0'),
                  Text('Sviluppata con Flutter'),
                  Text('Ottimizzata per l\'accessibilità'),
                ],
              ),
            ),
          ),
          SizedBox(height: 24),
          
          AccessibleButton(
            text: 'Contatta Supporto',
            icon: Icons.support_agent,
            color: Colors.blue,
            onPressed: () => onStatusUpdate('Apertura supporto...'),
            semanticsLabel: 'Pulsante Contatta Supporto - Apre il canale di assistenza clienti',
          ),
          SizedBox(height: 12),
          
          AccessibleButton(
            text: 'Valuta App',
            icon: Icons.star_rate,
            color: Colors.amber,
            onPressed: () => onStatusUpdate('Apertura store per valutazione...'),
            semanticsLabel: 'Pulsante Valuta App - Apre lo store per lasciare una recensione',
          ),
          SizedBox(height: 12),
          
          AccessibleButton(
            text: 'Condividi App',
            icon: Icons.share,
            color: Colors.green,
            onPressed: () => onStatusUpdate('Apertura menu condivisione...'),
            semanticsLabel: 'Pulsante Condividi App - Apre le opzioni per condividere l\'applicazione',
          ),
          SizedBox(height: 12),
          
          AccessibleButton(
            text: 'Tutorial',
            icon: Icons.help_outline,
            color: Colors.purple,
            onPressed: () => onStatusUpdate('Avvio tutorial...'),
            semanticsLabel: 'Pulsante Tutorial - Avvia la guida interattiva dell\'applicazione',
          ),
        ],
      ),
    );
  }
}

// Widget pulsante accessibile personalizzato
class AccessibleButton extends StatelessWidget {
  final String text;
  final IconData icon;
  final Color color;
  final VoidCallback onPressed;
  final String semanticsLabel;

  const AccessibleButton({
    super.key,
    required this.text,
    required this.icon,
    required this.color,
    required this.onPressed,
    required this.semanticsLabel,
  });

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: semanticsLabel,
      button: true,
      child: ElevatedButton.icon(
        onPressed: onPressed,
        icon: Icon(
          icon,
          size: 24,
          semanticLabel: null, // Evita duplicazione del semantic label
        ),
        label: Text(
          text,
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w600,
          ),
        ),
        style: ElevatedButton.styleFrom(
          backgroundColor: color,
          foregroundColor: Colors.white,
          padding: EdgeInsets.symmetric(vertical: 16, horizontal: 20),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          elevation: 2,
          // Migliora l'area di tocco per l'accessibilità
          minimumSize: Size(double.infinity, 56),
        ),
      ),
    );
  }
}
 
 