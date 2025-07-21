from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QProgressBar, QTextEdit)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QPalette
import random
import datetime

class VibeCheckApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("✅ Vibe Check Station")
        self.setGeometry(350, 250, 450, 500)
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a2e;
                color: white;
                font-family: 'Courier New';
            }
        """)
        
        self.setup_ui()
        
        # Vibe check results
        self.vibe_results = {
            "pass": [
                "✅ VIBE CHECK PASSED! You're absolutely radiating main character energy! 👑",
                "✅ IMMACULATE VIBES DETECTED! Your aura is literally glowing! ✨",
                "✅ VIBE STATUS: ELITE! You understood the assignment! 💯",
                "✅ CERTIFIED VIBE MASTER! Your energy could power a small city! ⚡",
                "✅ VIBES ARE ASTRONOMICAL! NASA wants to study your energy! 🚀",
                "✅ PEAK PERFORMANCE VIBES! You're operating on a different frequency! 📡",
                "✅ LEGENDARY VIBE STATUS! Historians will write about this moment! 📚",
                "✅ DIVINE VIBE ENERGY! Even the universe is taking notes! 🌌",
                "✅ VIBE CHECK COMPLETE: FLAWLESS VICTORY! Fatality! 🎮",
                "✅ MAXIMUM VIBE OVERDRIVE! Your energy just broke the meter! 📊"
            ],
            "fail": [
                "❌ VIBE CHECK FAILED! Your energy is giving 'forgot to charge phone' vibes 📱💀",
                "❌ VIBES ARE QUESTIONABLE! Please touch grass and try again 🌱",
                "❌ VIBE STATUS: SUS! Something ain't right here chief 🤔",
                "❌ ENERGY LEVELS CRITICALLY LOW! Have you tried turning yourself off and on again? 🔄",
                "❌ VIBE CHECK UNSUCCESSFUL! Your aura needs a software update 💾",
                "❌ NEGATIVE VIBES DETECTED! You're radiating NPC energy 🤖",
                "❌ VIBE MALFUNCTION! Error 404: Good vibes not found 🚫",
                "❌ CHAOTIC ENERGY ALERT! Your vibes are giving 'homework on Sunday' 📝😭",
                "❌ VIBE CHECK DENIED! Please consult your local grass-touching specialist 🌿",
                "❌ CURSED VIBE ENERGY! Someone call an exorcist for these vibes 👻"
            ]
        }
        
        self.vibe_score = 50
        self.total_checks = 0
        self.passed_checks = 0
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("✅ VIBE CHECK STATION ✅")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #00ff00;
                margin: 15px;
                border: 2px solid #ff00ff;
                padding: 15px;
                border-radius: 10px;
                background-color: #2d2d44;
            }
        """)
        
        # Subtitle
        subtitle = QLabel("🔍 Analyzing your energy levels...")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #ffff00;
                margin-bottom: 20px;
            }
        """)
        
        # Current vibe score
        self.vibe_display = QLabel(f"Current Vibe Score: {self.vibe_score}/100")
        self.vibe_display.setAlignment(Qt.AlignCenter)
        self.vibe_display.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #00ff00;
                margin: 10px;
                padding: 10px;
                background-color: #2d2d44;
                border-radius: 8px;
                border: 1px solid #00ff00;
            }
        """)
        
        # Vibe meter (progress bar)
        self.vibe_meter = QProgressBar()
        self.vibe_meter.setRange(0, 100)
        self.vibe_meter.setValue(self.vibe_score)
        self.vibe_meter.setStyleSheet("""
            QProgressBar {
                border: 2px solid #00ff00;
                border-radius: 10px;
                background-color: #2d2d44;
                text-align: center;
                font-weight: bold;
                height: 30px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ff0000, stop:0.5 #ffff00, stop:1 #00ff00);
                border-radius: 8px;
            }
        """)
        
        # Check button
        self.check_btn = QPushButton("🎯 INITIATE VIBE CHECK")
        self.check_btn.clicked.connect(self.perform_vibe_check)
        self.check_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ff00ff, stop:0.5 #00ff00, stop:1 #ffff00);
                color: black;
                font-size: 16px;
                font-weight: bold;
                padding: 20px;
                border: none;
                border-radius: 15px;
                margin: 20px;
            }
            QPushButton:hover {
                background: white;
            }
            QPushButton:pressed {
                background: #888888;
            }
        """)
        
        # Result display
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setPlainText("🎯 Ready for vibe analysis! Click the button to check your energy levels.")
        self.result_display.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d44;
                border: 2px solid #ff00ff;
                border-radius: 10px;
                padding: 15px;
                font-size: 14px;
                color: #ffffff;
                min-height: 120px;
                max-height: 120px;
            }
        """)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        self.boost_btn = QPushButton("⚡ Boost Vibes")
        self.boost_btn.clicked.connect(self.boost_vibes)
        self.boost_btn.setStyleSheet(self.get_button_style("#00ff00"))
        
        self.reset_btn = QPushButton("🔄 Reset Score")
        self.reset_btn.clicked.connect(self.reset_score)
        self.reset_btn.setStyleSheet(self.get_button_style("#ffff00"))
        
        self.chaos_btn = QPushButton("🌪️ Chaos Mode")
        self.chaos_btn.clicked.connect(self.chaos_mode)
        self.chaos_btn.setStyleSheet(self.get_button_style("#ff4444"))
        
        action_layout.addWidget(self.boost_btn)
        action_layout.addWidget(self.reset_btn)
        action_layout.addWidget(self.chaos_btn)
        
        # Stats
        self.stats_label = QLabel("📊 Checks: 0 | Passed: 0 | Success Rate: 0%")
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.stats_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #888888;
                margin: 10px;
                padding: 5px;
            }
        """)
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.vibe_display)
        layout.addWidget(self.vibe_meter)
        layout.addWidget(self.check_btn)
        layout.addWidget(self.result_display)
        layout.addLayout(action_layout)
        layout.addWidget(self.stats_label)
        
        self.setLayout(layout)
        
    def get_button_style(self, color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: black;
                font-size: 12px;
                font-weight: bold;
                padding: 10px;
                border: none;
                border-radius: 8px;
                margin: 5px;
            }}
            QPushButton:hover {{
                background-color: white;
            }}
        """
        
    def perform_vibe_check(self):
        self.check_btn.setText("🔄 ANALYZING...")
        self.check_btn.setEnabled(False)
        
        # Simulate analysis time
        QTimer.singleShot(1500, self.complete_vibe_check)
        
        # Show loading animation
        self.result_display.setPlainText("🔍 Scanning energy levels...\n⚡ Analyzing aura frequency...\n🌟 Calculating vibe coefficient...")
        
    def complete_vibe_check(self):
        # Random vibe check result with slight bias based on current score
        bias = (self.vibe_score - 50) / 100  # -0.5 to 0.5
        random_chance = random.random() + bias
        
        passed = random_chance > 0.4  # Slightly easier to pass
        
        self.total_checks += 1
        if passed:
            self.passed_checks += 1
            result = random.choice(self.vibe_results["pass"])
            score_change = random.randint(5, 15)
            self.vibe_score = min(100, self.vibe_score + score_change)
        else:
            result = random.choice(self.vibe_results["fail"])
            score_change = random.randint(3, 10)
            self.vibe_score = max(0, self.vibe_score - score_change)
            
        # Update displays
        self.result_display.setPlainText(result)
        self.update_displays()
        
        # Re-enable button
        self.check_btn.setText("🎯 INITIATE VIBE CHECK")
        self.check_btn.setEnabled(True)
        
    def boost_vibes(self):
        boost_amount = random.randint(10, 25)
        self.vibe_score = min(100, self.vibe_score + boost_amount)
        
        boost_messages = [
            f"⚡ VIBE BOOST ACTIVATED! +{boost_amount} energy!",
            f"🚀 ENERGY SURGE! Your vibes increased by {boost_amount}!",
            f"✨ AURA ENHANCEMENT! +{boost_amount} to your vibe score!",
            f"💎 PREMIUM VIBES UNLOCKED! +{boost_amount} points!"
        ]
        
        self.result_display.setPlainText(random.choice(boost_messages))
        self.update_displays()
        
    def reset_score(self):
        self.vibe_score = 50
        self.total_checks = 0
        self.passed_checks = 0
        self.result_display.setPlainText("🔄 Vibe score reset! Ready for a fresh start!")
        self.update_displays()
        
    def chaos_mode(self):
        # Rapidly change vibe score multiple times
        self.result_display.setPlainText("🌪️ CHAOS MODE ACTIVATED! Your vibes are going WILD!")
        
        def chaos_update(count=0):
            if count < 10:
                self.vibe_score = random.randint(0, 100)
                self.update_displays()
                QTimer.singleShot(200, lambda: chaos_update(count + 1))
            else:
                final_score = random.randint(20, 80)
                self.vibe_score = final_score
                self.result_display.setPlainText(f"🌪️ Chaos complete! Your vibes have stabilized at {final_score}/100")
                self.update_displays()
                
        chaos_update()
        
    def update_displays(self):
        self.vibe_display.setText(f"Current Vibe Score: {self.vibe_score}/100")
        self.vibe_meter.setValue(self.vibe_score)
        
        # Update stats
        success_rate = (self.passed_checks / self.total_checks * 100) if self.total_checks > 0 else 0
        self.stats_label.setText(f"📊 Checks: {self.total_checks} | Passed: {self.passed_checks} | Success Rate: {success_rate:.1f}%")
        
        # Update vibe display color based on score
        if self.vibe_score >= 80:
            color = "#00ff00"  # Green
        elif self.vibe_score >= 60:
            color = "#ffff00"  # Yellow
        elif self.vibe_score >= 40:
            color = "#ff8800"  # Orange
        else:
            color = "#ff0000"  # Red
            
        self.vibe_display.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                color: {color};
                margin: 10px;
                padding: 10px;
                background-color: #2d2d44;
                border-radius: 8px;
                border: 1px solid {color};
            }}
        """)
