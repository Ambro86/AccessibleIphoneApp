//
//  AudioManager.swift
//  Avventura epica
//
//  Created by Ambrogio Riili on 27/07/25.
//

import Foundation
import AVFoundation
import UIKit

class AudioManager: ObservableObject {
    private var musicPlayer: AVAudioPlayer?
    private var soundPlayers: [String: AVAudioPlayer] = [:]
    private var currentMusicTrack: String?
    
    @Published var isMusicEnabled = true
    @Published var isSoundEnabled = true
    @Published var musicVolume: Float = 0.7
    @Published var soundVolume: Float = 0.8
    
    private let logger = Logger()
    
    init() {
        setupAudioSession()
        preloadSounds()
    }
    
    // MARK: - Audio Session Setup
    private func setupAudioSession() {
        do {
            let audioSession = AVAudioSession.sharedInstance()
            try audioSession.setCategory(.playback, mode: .default, options: [.mixWithOthers])
            try audioSession.setActive(true)
            logger.log("🔊 Audio session configurata con successo")
        } catch {
            logger.log("❌ Errore configurazione audio session: \(error)")
        }
    }
    
    // MARK: - Music Management
    func playMusic(_ trackName: String, loop: Bool = true) {
        guard isMusicEnabled else { return }
        
        // Don't restart the same track
        if currentMusicTrack == trackName && musicPlayer?.isPlaying == true {
            return
        }
        
        stopMusic()
        
        guard let url = Bundle.main.url(forResource: trackName, withExtension: "mp3", subdirectory: "Audio") else {
            logger.log("❌ File musicale non trovato: \(trackName)")
            // Fallback to a generic ambient sound or silence
            return
        }
        
        do {
            musicPlayer = try AVAudioPlayer(contentsOf: url)
            musicPlayer?.numberOfLoops = loop ? -1 : 0
            musicPlayer?.volume = musicVolume
            musicPlayer?.prepareToPlay()
            
            let success = musicPlayer?.play() ?? false
            if success {
                currentMusicTrack = trackName
                logger.log("🎵 Riproduzione musica: \(trackName)")
            } else {
                logger.log("❌ Errore riproduzione musica: \(trackName)")
            }
        } catch {
            logger.log("❌ Errore caricamento musica \(trackName): \(error)")
        }
    }
    
    func stopMusic() {
        musicPlayer?.stop()
        musicPlayer = nil
        currentMusicTrack = nil
        logger.log("🔇 Musica fermata")
    }
    
    func pauseMusic() {
        musicPlayer?.pause()
        logger.log("⏸️ Musica in pausa")
    }
    
    func resumeMusic() {
        guard isMusicEnabled else { return }
        musicPlayer?.play()
        logger.log("▶️ Musica ripresa")
    }
    
    func setMusicVolume(_ volume: Float) {
        musicVolume = max(0.0, min(1.0, volume))
        musicPlayer?.volume = musicVolume
    }
    
    // MARK: - Sound Effects Management
    func playSound(_ soundName: String, volume: Float? = nil) {
        guard isSoundEnabled else { return }
        
        let effectiveVolume = volume ?? soundVolume
        
        // Try to get existing player first
        if let existingPlayer = soundPlayers[soundName] {
            existingPlayer.stop()
            existingPlayer.currentTime = 0
            existingPlayer.volume = effectiveVolume
            existingPlayer.play()
            logger.log("🔊 Suono riprodotto (cached): \(soundName)")
            return
        }
        
        // Create new player if not exists
        guard let url = Bundle.main.url(forResource: soundName, withExtension: "mp3", subdirectory: "Audio") else {
            logger.log("❌ File audio non trovato: \(soundName)")
            return
        }
        
        do {
            let player = try AVAudioPlayer(contentsOf: url)
            player.volume = effectiveVolume
            player.prepareToPlay()
            soundPlayers[soundName] = player
            
            let success = player.play()
            if success {
                logger.log("🔊 Suono riprodotto: \(soundName)")
            } else {
                logger.log("❌ Errore riproduzione suono: \(soundName)")
            }
        } catch {
            logger.log("❌ Errore caricamento suono \(soundName): \(error)")
        }
    }
    
    func setSoundVolume(_ volume: Float) {
        soundVolume = max(0.0, min(1.0, volume))
        for player in soundPlayers.values {
            player.volume = soundVolume
        }
    }
    
    // MARK: - Preload Common Sounds
    private func preloadSounds() {
        let commonSounds = [
            "effetto_gatto_attacco",
            "effetto_vittoria",
            "effetto_sconfitta",
            "effetto_livello_up",
            "effetto_bere_pozione",
            "effetto_raccolta",
            "effetto_monete",
            "effetto_mangiare",
            "effetto_bere_acqua",
            "effetto_fusa",
            "effetto_gatto_raccolta",
            "effetto_heartbeat"
        ]
        
        for soundName in commonSounds {
            preloadSound(soundName)
        }
    }
    
    private func preloadSound(_ soundName: String) {
        guard let url = Bundle.main.url(forResource: soundName, withExtension: "mp3", subdirectory: "Audio") else {
            // Sound file doesn't exist, that's OK for now
            return
        }
        
        do {
            let player = try AVAudioPlayer(contentsOf: url)
            player.volume = 0.0 // Silent preload
            player.prepareToPlay()
            soundPlayers[soundName] = player
            logger.log("📦 Suono precaricato: \(soundName)")
        } catch {
            logger.log("❌ Errore precaricamento suono \(soundName): \(error)")
        }
    }
    
    // MARK: - Haptic Feedback
    func hapticFeedback(_ style: UIImpactFeedbackGenerator.FeedbackStyle = .light) {
        let impactFeedback = UIImpactFeedbackGenerator(style: style)
        impactFeedback.impactOccurred()
    }
    
    func hapticSuccess() {
        let feedback = UINotificationFeedbackGenerator()
        feedback.notificationOccurred(.success)
    }
    
    func hapticError() {
        let feedback = UINotificationFeedbackGenerator()
        feedback.notificationOccurred(.error)
    }
    
    func hapticWarning() {
        let feedback = UINotificationFeedbackGenerator()
        feedback.notificationOccurred(.warning)
    }
    
    // MARK: - Area-Specific Music
    func playAreaMusic(_ area: String) {
        let musicTrack: String
        
        // Usa i file musicali originali dall'asset
        switch area {
        case "Villaggio":
            musicTrack = "villaggio"
        case "🏠 Cantina":
            musicTrack = "cantina"
        case "🚰 Fogne":
            musicTrack = "fogne"
        case "🌀 Labirinto Antico":
            musicTrack = "labirinto"
        case "❄️ Area Innevata":
            musicTrack = "area_innevata"
        case "🌿 Giungla Selvaggia":
            musicTrack = "giungla"
        case "🌲 Bosco Profondo":
            musicTrack = "bosco"
        case "⚰️ Cimitero":
            musicTrack = "cimitero"
        case "🏚️ Casa degli Orrori":
            musicTrack = "casa_orrori"
        case "🏭 Fabbrica Abbandonata":
            musicTrack = "fabbrica"
        case "⛏️ Miniera Profonda":
            musicTrack = "miniera"
        case "🌙 Cripta Maledetta":
            musicTrack = "cripta"
        case "🌊 Mare":
            musicTrack = "mare"
        case "🏔️ Montagna Sacra":
            musicTrack = "montagna_sacra"
        case "🌋 Vulcano Attivo":
            musicTrack = "vulcano"
        case "👑 Palazzo Finale":
            musicTrack = "palazzo_finale"
        case "🌌 Regno degli Incubi":
            musicTrack = "regno_incubi"
        default:
            musicTrack = "villaggio" // Default fallback
        }
        
        playMusic(musicTrack)
    }
    
    // MARK: - Ambient Sounds for Areas
    func playAreaAmbient(_ area: String) {
        let ambientTrack: String
        
        switch area {
        case "Villaggio":
            ambientTrack = "ambient_villaggio_uccelli"
        case "🏠 Cantina":
            ambientTrack = "ambient_cantina_gocce"
        case "🚰 Fogne":
            ambientTrack = "ambient_fogne_topi"
        case "🌀 Labirinto Antico":
            ambientTrack = "ambient_labirinto_vento"
        case "❄️ Area Innevata":
            ambientTrack = "ambient_neve_vento"
        case "🌿 Giungla Selvaggia":
            ambientTrack = "ambient_giungla_animali"
        case "🌲 Bosco Profondo":
            ambientTrack = "ambient_bosco_foglie"
        case "⚰️ Cimitero":
            ambientTrack = "ambient_cimitero_spettri"
        case "🏚️ Casa degli Orrori":
            ambientTrack = "ambient_orrori_porta"
        case "🏭 Fabbrica Abbandonata":
            ambientTrack = "ambient_fabbrica_macchinari"
        case "⛏️ Miniera Profonda":
            ambientTrack = "ambient_miniera_picconate"
        case "🌙 Cripta Maledetta":
            ambientTrack = "ambient_cripta_magia"
        case "🌊 Mare":
            ambientTrack = "ambient_mare_onde"
        case "🏔️ Montagna Sacra":
            ambientTrack = "ambient_montagna_vento"
        case "🌋 Vulcano Attivo":
            ambientTrack = "ambient_vulcano_lava"
        case "👑 Palazzo Finale":
            ambientTrack = "ambient_palazzo_eco"
        case "🌌 Regno degli Incubi":
            ambientTrack = "ambient_incubi"
        default:
            ambientTrack = "ambient_villaggio_uccelli"
        }
        
        playSound(ambientTrack, volume: 0.3) // Volume più basso per ambient
    }
    
    // MARK: - Combat Music
    func playCombatMusic(_ isBoss: Bool = false, isFinalBoss: Bool = false) {
        let combatTrack: String
        
        if isFinalBoss {
            combatTrack = "battaglia_boss_finale"
        } else if isBoss {
            combatTrack = "battaglia_boss"
        } else {
            combatTrack = "battaglia"
        }
        
        playMusic(combatTrack)
    }
    
    // MARK: - Game Event Sounds usando i file originali
    func playCombatStartSound() {
        playSound("effetto_gatto_attacco", volume: 0.9)
    }
    
    func playCatAttackSound() {
        playSound("effetto_gatto_attacco", volume: 0.8)
    }
    
    func playVictorySound() {
        playSound("effetto_vittoria", volume: 0.8)
    }
    
    func playDefeatSound() {
        playSound("effetto_sconfitta", volume: 0.7)
    }
    
    func playErrorSound() {
        playSound("effetto_sconfitta", volume: 0.6)
    }
    
    func playLevelUpSound() {
        playSound("effetto_livello_up", volume: 0.9)
    }
    
    func playPotionUseSound() {
        playSound("effetto_bere_pozione", volume: 0.6)
    }
    
    func playCollectItemSound() {
        playSound("effetto_raccolta", volume: 0.7)
    }
    
    func playCollectMoneySound() {
        playSound("effetto_monete", volume: 0.6)
    }
    
    func playEatingSound() {
        playSound("effetto_mangiare", volume: 0.5)
    }
    
    func playDrinkingSound() {
        playSound("effetto_bere_acqua", volume: 0.5)
    }
    
    func playCatPurrSound() {
        playSound("effetto_fusa", volume: 0.4)
    }
    
    func playCatCollectSound() {
        playSound("effetto_gatto_raccolta", volume: 0.6)
    }
    
    func playCatFishSound() {
        playSound("effetto_gatto_mangia_pesce", volume: 0.6)
    }
    
    func playHeartbeatSound() {
        playSound("effetto_heartbeat", volume: 0.8)
    }
    
    // Monster sounds
    func playMonsterSound(_ monsterType: Int = 1) {
        let soundName = "effetto_mostro_\(min(max(monsterType, 1), 5))"
        playSound(soundName, volume: 0.7)
    }
    
    func playBossSound() {
        playSound("effetto_boss_1", volume: 0.8)
    }
    
    func playSpiderQueenSound() {
        playSound("effetto_boss_regina_ragni", volume: 0.8)
    }
    
    func playMonsterRoar(_ audioFile: String) {
        playSound(audioFile, volume: 0.7)
    }
    
    // Area-specific effect sounds
    func playCellarSounds() {
        let cellarSounds = ["effetto_cantina_insetto", "effetto_cantina_melma", 
                           "effetto_cantina_muffa", "effetto_cantina_pipistrelli", "effetto_cantina_ragno"]
        let randomSound = cellarSounds.randomElement() ?? "effetto_cantina_ragno"
        playSound(randomSound, volume: 0.5)
    }
    
    // MARK: - Audio State Management
    func enableMusic(_ enabled: Bool) {
        isMusicEnabled = enabled
        if !enabled {
            stopMusic()
        } else if let currentTrack = currentMusicTrack {
            playMusic(currentTrack)
        }
        logger.log("🎵 Musica \(enabled ? "abilitata" : "disabilitata")")
    }
    
    func enableSounds(_ enabled: Bool) {
        isSoundEnabled = enabled
        if !enabled {
            // Stop all currently playing sounds
            for player in soundPlayers.values {
                player.stop()
            }
        }
        logger.log("🔊 Suoni \(enabled ? "abilitati" : "disabilitati")")
    }
    
    // MARK: - App Lifecycle
    func handleAppDidEnterBackground() {
        pauseMusic()
        logger.log("📱 App in background - audio in pausa")
    }
    
    func handleAppWillEnterForeground() {
        guard isMusicEnabled else { return }
        resumeMusic()
        logger.log("📱 App in foreground - audio ripreso")
    }
    
    // MARK: - Memory Management
    func clearSoundCache() {
        for player in soundPlayers.values {
            player.stop()
        }
        soundPlayers.removeAll()
        logger.log("🗑️ Cache audio pulita")
    }
    
    deinit {
        stopMusic()
        clearSoundCache()
        logger.log("🧹 AudioManager deallocato")
    }
}

// MARK: - Audio Extensions for GameManager
extension GameManager {
    func setupAudio() {
        // Initialize audio manager if needed
        AudioManager.shared.enableMusic(gameState.audioAbilitato)
        AudioManager.shared.enableSounds(gameState.audioAbilitato)
    }
    
    func playAreaMusic(_ area: String) {
        AudioManager.shared.playAreaMusic(area)
    }
    
    func playGameSound(_ soundName: String) {
        AudioManager.shared.playSound(soundName)
    }
}

// MARK: - Singleton Pattern
extension AudioManager {
    static let shared = AudioManager()
}