# 🎵 Setup Audio per Xcode

## Passi per aggiungere i file audio al progetto:

### 1. Aprire Xcode
- Apri il file `Avventura epica.xcodeproj`

### 2. Aggiungere file audio al progetto
1. **Seleziona la cartella principale** del progetto "Avventura epica" nel navigator
2. **Click destro** → "Add Files to 'Avventura epica'"
3. **Seleziona tutti i file .mp3** dalla cartella del progetto Swift
4. **Assicurati che sia selezionato**:
   - ✅ "Add to target: Avventura epica"
   - ✅ "Copy items if needed"
5. **Click "Add"**

### 3. File audio copiati nel progetto:

#### 🎼 Musiche di sottofondo per aree:
- `villaggio.mp3` - Musica principale del villaggio
- `cantina.mp3` - Atmosfera misteriosa della cantina
- `fogne.mp3` - Suoni inquietanti delle fogne
- `labirinto.mp3` - Musica puzzle del labirinto
- `area_innevata.mp3` - Melodie gelide dell'area innevata
- `giungla.mp3` - Suoni selvaggi della giungla
- `bosco.mp3` - Atmosfera magica del bosco
- `cimitero.mp3` - Melodie spettrali del cimitero
- `casa_orrori.mp3` - Musica terrificante della casa degli orrori
- `fabbrica.mp3` - Suoni industriali della fabbrica
- `miniera.mp3` - Echi profondi della miniera
- `cripta.mp3` - Atmosfera oscura della cripta
- `mare.mp3` - Onde e melodie marine
- `montagna_sacra.mp3` - Musica epica della montagna
- `vulcano.mp3` - Intensità lavica del vulcano
- `palazzo_finale.mp3` - Tema epico del boss finale
- `regno_incubi.mp3` - Area segreta degli incubi

#### 🎵 Musiche di combattimento:
- `battaglia.mp3` - Combattimento normale
- `battaglia_boss.mp3` - Combattimento contro boss
- `battaglia_boss_finale.mp3` - Boss finale epico

#### 🌿 Suoni ambientali:
- `ambient_villaggio_uccelli.mp3` - Cinguettii del villaggio
- `ambient_cantina_gocce.mp3` - Gocce nella cantina
- `ambient_fogne_topi.mp3` - Topi nelle fogne
- `ambient_labirinto_vento.mp3` - Vento nel labirinto
- `ambient_neve_vento.mp3` - Vento gelido
- `ambient_giungla_animali.mp3` - Versi di animali selvaggi
- `ambient_bosco_foglie.mp3` - Fruscio di foglie
- `ambient_cimitero_spettri.mp3` - Sussurri spettrali
- `ambient_orrori_porta.mp3` - Scricchiolii inquietanti
- `ambient_fabbrica_macchinari.mp3` - Rumori industriali
- `ambient_miniera_picconate.mp3` - Suoni di scavo
- `ambient_cripta_magia.mp3` - Energia magica oscura
- `ambient_mare_onde.mp3` - Onde del mare
- `ambient_montagna_vento.mp3` - Vento delle vette
- `ambient_vulcano_lava.mp3` - Bolle di lava
- `ambient_palazzo_eco.mp3` - Echi nel palazzo
- `ambient_incubi.mp3` - Atmosfera da incubo

#### 🔊 Effetti sonori:
- `effetto_vittoria.mp3` - Suono di vittoria
- `effetto_sconfitta.mp3` - Suono di sconfitta
- `effetto_livello_up.mp3` - Level up!
- `effetto_bere_pozione.mp3` - Uso pozione
- `effetto_bere_acqua.mp3` - Bere acqua
- `effetto_raccolta.mp3` - Raccogliere oggetti
- `effetto_monete.mp3` - Raccogliere monete/ricompense
- `effetto_mangiare.mp3` - Mangiare cibo
- `effetto_fusa.mp3` - Fusa dei gatti
- `effetto_gatto_attacco.mp3` - Attacco del gatto
- `effetto_gatto_raccolta.mp3` - Gatto che raccoglie
- `effetto_gatto_mangia_pesce.mp3` - Gatto mangia pesce
- `effetto_heartbeat.mp3` - Battito cardiaco (tensione)

#### 👹 Suoni mostri:
- `effetto_mostro_1.mp3` - Verso mostro tipo 1
- `effetto_mostro_2.mp3` - Verso mostro tipo 2
- `effetto_mostro_3.mp3` - Verso mostro tipo 3
- `effetto_mostro_4.mp3` - Verso mostro tipo 4
- `effetto_mostro_5.mp3` - Verso mostro tipo 5
- `effetto_boss_1.mp3` - Ruggito boss generico
- `effetto_boss_regina_ragni.mp3` - Boss regina dei ragni

#### 🏠 Effetti area cantina:
- `effetto_cantina_insetto.mp3` - Insetti nella cantina
- `effetto_cantina_melma.mp3` - Melma che sgocciola
- `effetto_cantina_muffa.mp3` - Suono di muffa
- `effetto_cantina_pipistrelli.mp3` - Pipistrelli
- `effetto_cantina_ragno.mp3` - Ragni

### 4. Verifica
Dopo aver aggiunto i file:
1. **Compila il progetto** (Cmd+B)
2. **Controlla che i file appaiano** nel Project Navigator
3. **Testa l'audio** lanciando l'app nel simulatore

### 5. Note Importanti
- ✅ I file sono già nella cartella corretta del progetto
- ✅ L'AudioManager è configurato per usare questi file specifici
- ✅ Tutti i mapping area→musica sono corretti
- ✅ Gli effetti sono collegati alle azioni di gioco

### 6. Controllo Audio nel Simulatore
- Il simulatore iOS supporta l'audio
- Assicurati che il volume del Mac sia attivo
- Controlla le impostazioni audio nelle Settings dell'app

## 🎮 Funzionalità Audio Implementate

### Musica dinamica per area
- **Cambia automaticamente** quando si cambia area
- **Musica di combattimento** speciale per battaglie
- **Suoni ambientali** che si sovrappongono alla musica

### Effetti sonori reattivi
- **Feedback audio** per ogni azione
- **Suoni specifici** per gatti e mostri
- **Effetti di victory/defeat** epici

### Controlli audio
- **Toggle per musica** e effetti nelle impostazioni
- **Controllo volume** separato
- **Haptic feedback** su dispositivi fisici

---

🎵 **Il tuo gioco Avventura Epica ora ha un audio completo e immersivo!** 🎵