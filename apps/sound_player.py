from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QSlider, QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import random
import pygame
import numpy as np
import os

class SoundPlayerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔊 Meme Sound Player")
        self.setGeometry(300, 200, 500, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a2e;
                color: white;
                font-family: 'Courier New';
            }
        """)
        
        # Initialize pygame mixer for audio
        try:
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
            pygame.mixer.init()
            self.audio_enabled = True
            print("🎵 Audio system initialized successfully!")
        except Exception as e:
            print(f"⚠️ Audio initialization failed: {e}")
            self.audio_enabled = False
            
        # Generate sounds on first run
        self.sounds = {}
        self.generate_meme_sounds()
        
        self.setup_ui()
        
        # Update meme sounds to match generated sounds
        self.meme_sounds = []
        for sound_name in self.sounds.keys():
            # Extract duration info (approximate)
            duration = "0:01" if "Beep" in sound_name or "Ding" in sound_name else "0:03"
            if "Startup" in sound_name or "Trombone" in sound_name:
                duration = "0:05"
            
            vibe = "Epic"
            if "Error" in sound_name or "Buzzer" in sound_name:
                vibe = "Ominous"
            elif "Success" in sound_name or "Ding" in sound_name:
                vibe = "Positive"
            elif "Boom" in sound_name or "Bass" in sound_name:
                vibe = "Powerful"
            elif "Static" in sound_name or "Zap" in sound_name:
                vibe = "Chaotic"
                
            self.meme_sounds.append({
                "name": sound_name,
                "duration": duration,
                "vibe": vibe,
                "pygame_sound": self.sounds[sound_name]
            })
        
        self.current_sound = None
        self.is_playing = False
        self.current_pygame_sound = None
        self.populate_playlist()
        
    def generate_tone(self, frequency, duration, sample_rate=22050, amplitude=0.5):
        """Generate a simple sine wave tone"""
        frames = int(duration * sample_rate)
        arr = np.zeros(frames)
        
        for i in range(frames):
            arr[i] = amplitude * np.sin(2 * np.pi * frequency * i / sample_rate)
        
        # Convert to 16-bit integers and make stereo
        arr = (arr * 32767).astype(np.int16)
        stereo_arr = np.column_stack((arr, arr))  # Make stereo
        return stereo_arr
    
    def generate_sweep(self, start_freq, end_freq, duration, sample_rate=22050, amplitude=0.5):
        """Generate a frequency sweep"""
        frames = int(duration * sample_rate)
        arr = np.zeros(frames)
        
        for i in range(frames):
            freq = start_freq + (end_freq - start_freq) * (i / frames)
            arr[i] = amplitude * np.sin(2 * np.pi * freq * i / sample_rate)
        
        # Apply envelope to avoid clicks
        envelope_len = frames // 10
        envelope = np.linspace(0, 1, envelope_len)
        arr[:envelope_len] *= envelope
        arr[-envelope_len:] *= envelope[::-1]
        
        arr = (arr * 32767).astype(np.int16)
        stereo_arr = np.column_stack((arr, arr))
        return stereo_arr
    
    def generate_noise_burst(self, duration, sample_rate=22050, amplitude=0.3):
        """Generate a noise burst"""
        frames = int(duration * sample_rate)
        arr = np.random.normal(0, amplitude, frames)
        
        # Apply envelope
        envelope = np.exp(-np.linspace(0, 5, frames))
        arr *= envelope
        
        arr = (arr * 32767).astype(np.int16)
        stereo_arr = np.column_stack((arr, arr))
        return stereo_arr
    
    def generate_meme_sounds(self):
        """Generate all meme sounds"""
        if not self.audio_enabled:
            return
            
        try:
            print("🎵 Generating meme sounds...")
            
            # Generate different meme sounds
            sound_generators = {
                '🔊 MLG Airhorn': lambda: self.generate_tone(1000, 0.3, amplitude=0.6),
                '🗿 Vine Boom': lambda: self.generate_sweep(80, 40, 0.5, amplitude=0.8),
                '💻 Windows XP Startup': lambda: self.generate_sweep(200, 800, 1.0, amplitude=0.4),
                '🚫 Error Sound': lambda: self.generate_sweep(600, 200, 0.8, amplitude=0.5),
                '✅ Success Sound': lambda: self.generate_sweep(300, 600, 0.6, amplitude=0.4),
                '🔔 Notification': lambda: self.generate_tone(800, 0.2, amplitude=0.3),
                '🌪️ Whoosh': lambda: self.generate_sweep(1000, 100, 0.4, amplitude=0.4),
                '📺 Static': lambda: self.generate_noise_burst(0.3, amplitude=0.2),
                '🔔 Ding': lambda: self.generate_tone(1200, 0.5, amplitude=0.3),
                '🚨 Buzzer': lambda: self.generate_tone(150, 0.8, amplitude=0.5),
                '🎺 Sad Trombone': lambda: self.generate_sweep(200, 100, 1.2, amplitude=0.4),
                '⚡ Zap': lambda: self.generate_noise_burst(0.1, amplitude=0.5),
                '🔊 Bass Drop': lambda: self.generate_sweep(60, 30, 0.8, amplitude=0.9),
                '🎸 Guitar Riff': lambda: self.generate_tone(440, 0.4, amplitude=0.5),
                '🤖 Robot Beep': lambda: self.generate_tone(1500, 0.15, amplitude=0.4)
            }
            
            for name, generator in sound_generators.items():
                try:
                    audio_data = generator()
                    sound = pygame.sndarray.make_sound(audio_data)
                    self.sounds[name] = sound
                except Exception as e:
                    print(f"⚠️ Failed to generate {name}: {e}")
                    
            print(f"✅ Generated {len(self.sounds)} meme sounds!")
            
        except Exception as e:
            print(f"⚠️ Sound generation failed: {e}")
            self.audio_enabled = False
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("🔊 MEME SOUND PLAYER 🔊")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #ff00ff;
                margin: 15px;
                border: 2px solid #00ff00;
                padding: 10px;
                border-radius: 10px;
            }
        """)
        
        # Now playing
        self.now_playing = QLabel("🎵 Select a meme to play")
        self.now_playing.setAlignment(Qt.AlignCenter)
        self.now_playing.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #00ff00;
                margin: 10px;
                padding: 10px;
                background-color: #2d2d44;
                border-radius: 8px;
            }
        """)
        
        # Playlist
        playlist_label = QLabel("📋 Meme Playlist:")
        playlist_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #ffff00;
                margin: 10px 0 5px 0;
                font-weight: bold;
            }
        """)
        
        self.playlist = QListWidget()
        self.playlist.setStyleSheet("""
            QListWidget {
                background-color: #2d2d44;
                border: 2px solid #00ff00;
                border-radius: 10px;
                padding: 10px;
                font-size: 12px;
                color: white;
                min-height: 200px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #444;
            }
            QListWidget::item:selected {
                background-color: #ff00ff;
                color: black;
            }
            QListWidget::item:hover {
                background-color: #00ff00;
                color: black;
            }
        """)
        self.playlist.itemClicked.connect(self.select_sound)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        self.play_btn = QPushButton("▶️ Play")
        self.play_btn.clicked.connect(self.toggle_play)
        self.play_btn.setStyleSheet(self.get_button_style("#00ff00"))
        
        self.stop_btn = QPushButton("⏹️ Stop")
        self.stop_btn.clicked.connect(self.stop_sound)
        self.stop_btn.setStyleSheet(self.get_button_style("#ff4444"))
        
        self.random_btn = QPushButton("🎲 Random")
        self.random_btn.clicked.connect(self.play_random)
        self.random_btn.setStyleSheet(self.get_button_style("#ffff00"))
        
        controls_layout.addWidget(self.play_btn)
        controls_layout.addWidget(self.stop_btn)
        controls_layout.addWidget(self.random_btn)
        
        # Volume control
        volume_layout = QHBoxLayout()
        volume_label = QLabel("🔊 Volume:")
        volume_label.setStyleSheet("color: #888888; font-size: 12px;")
        
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: #2d2d44;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #ff00ff;
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
            QSlider::sub-page:horizontal {
                background: #00ff00;
                border-radius: 4px;
            }
        """)
        
        self.volume_label = QLabel("50%")
        self.volume_label.setStyleSheet("color: #888888; font-size: 12px; min-width: 40px;")
        self.volume_slider.valueChanged.connect(self.update_volume)
        
        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(self.volume_slider)
        volume_layout.addWidget(self.volume_label)
        
        # Chaos mode
        chaos_layout = QHBoxLayout()
        
        self.chaos_btn = QPushButton("🌪️ CHAOS MODE")
        self.chaos_btn.clicked.connect(self.chaos_mode)
        self.chaos_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ff0000, stop:0.33 #ffff00, stop:0.66 #00ff00, stop:1 #ff00ff);
                color: black;
                font-size: 14px;
                font-weight: bold;
                padding: 15px;
                border: none;
                border-radius: 10px;
                margin: 10px;
            }
            QPushButton:hover {
                background: white;
            }
        """)
        
        chaos_layout.addWidget(self.chaos_btn)
        
        layout.addWidget(title)
        layout.addWidget(self.now_playing)
        layout.addWidget(playlist_label)
        layout.addWidget(self.playlist)
        layout.addLayout(controls_layout)
        layout.addLayout(volume_layout)
        layout.addLayout(chaos_layout)
        
        self.setLayout(layout)
        
    def get_button_style(self, color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: black;
                font-size: 12px;
                font-weight: bold;
                padding: 12px;
                border: none;
                border-radius: 8px;
                margin: 5px;
            }}
            QPushButton:hover {{
                background-color: white;
            }}
        """
        
    def populate_playlist(self):
        for sound in self.meme_sounds:
            item_text = f"{sound['name']} - {sound['duration']} ({sound['vibe']})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, sound)
            self.playlist.addItem(item)
            
    def select_sound(self, item):
        self.current_sound = item.data(Qt.UserRole)
        self.now_playing.setText(f"🎵 Selected: {self.current_sound['name']}")
        
    def toggle_play(self):
        if not self.current_sound:
            self.now_playing.setText("❌ No sound selected!")
            return
            
        if not self.is_playing:
            self.play_sound()
        else:
            self.pause_sound()
            
    def play_sound(self):
        if not self.current_sound:
            return
            
        if not self.audio_enabled:
            self.now_playing.setText("❌ Audio system not available!")
            return
            
        self.is_playing = True
        self.play_btn.setText("⏸️ Pause")
        self.now_playing.setText(f"🎵 Playing: {self.current_sound['name']} 🔊")
        
        # Play the actual pygame sound
        try:
            if 'pygame_sound' in self.current_sound:
                self.current_pygame_sound = self.current_sound['pygame_sound']
                # Set volume based on slider
                volume = self.volume_slider.value() / 100.0
                self.current_pygame_sound.set_volume(volume)
                self.current_pygame_sound.play()
                
                # Auto-stop when sound finishes (estimate duration)
                duration_ms = int(float(self.current_sound['duration'].split(':')[1]) * 1000)
                QTimer.singleShot(duration_ms, self.finish_playback)
            else:
                # Fallback to simulation
                QTimer.singleShot(3000, self.finish_playback)
        except Exception as e:
            print(f"⚠️ Playback error: {e}")
            self.now_playing.setText(f"❌ Playback failed: {self.current_sound['name']}")
            self.finish_playback()
        
    def pause_sound(self):
        self.is_playing = False
        self.play_btn.setText("▶️ Play")
        self.now_playing.setText(f"⏸️ Paused: {self.current_sound['name']}")
        
    def stop_sound(self):
        self.is_playing = False
        self.play_btn.setText("▶️ Play")
        
        # Stop pygame sound if playing
        if self.current_pygame_sound and self.audio_enabled:
            try:
                self.current_pygame_sound.stop()
            except:
                pass
                
        if self.current_sound:
            self.now_playing.setText(f"⏹️ Stopped: {self.current_sound['name']}")
        else:
            self.now_playing.setText("🎵 Select a meme to play")
            
    def finish_playback(self):
        if self.is_playing:
            self.stop_sound()
            
    def play_random(self):
        if not self.meme_sounds:
            self.now_playing.setText("❌ No sounds available!")
            return
            
        random_sound = random.choice(self.meme_sounds)
        self.current_sound = random_sound
        self.play_sound()
        
        # Highlight the random selection in playlist
        for i in range(self.playlist.count()):
            item = self.playlist.item(i)
            if item.data(Qt.UserRole) == random_sound:
                self.playlist.setCurrentItem(item)
                break
                
    def update_volume(self, value):
        self.volume_label.setText(f"{value}%")
        
    def chaos_mode(self):
        # Play multiple random sounds in sequence
        self.now_playing.setText("🌪️ CHAOS MODE ACTIVATED! 🌪️")
        
        chaos_sounds = random.sample(self.meme_sounds, min(5, len(self.meme_sounds)))
        
        def play_next_chaos_sound(index=0):
            if index < len(chaos_sounds):
                self.current_sound = chaos_sounds[index]
                self.now_playing.setText(f"🌪️ CHAOS: {self.current_sound['name']} ({index+1}/{len(chaos_sounds)})")
                QTimer.singleShot(1000, lambda: play_next_chaos_sound(index + 1))
            else:
                self.now_playing.setText("🌪️ Chaos complete! Your ears have been blessed 🙏")
                
        play_next_chaos_sound()
