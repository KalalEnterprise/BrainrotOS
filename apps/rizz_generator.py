from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QTextEdit, QFrame)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import random

class RizzGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("💘 Rizz Generator 9000")
        self.setGeometry(200, 200, 500, 400)
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a2e;
                color: white;
                font-family: 'Courier New';
            }
        """)
        
        self.setup_ui()
        
        # Rizz lines database
        self.rizz_lines = [
            "Are you Ohio? Because you're making me feel sus 😳",
            "Girl, are you a sigma? Because you got that grindset 💪",
            "Are you TikTok? Because I can't stop scrolling through my feelings for you 📱",
            "Damn girl, you got more rizz than a Level 100 Gyatt 🔥",
            "Are you Wi-Fi? Because I'm feeling a connection (no cap) 📶",
            "Girl, you're bussin like a fresh batch of chicken nuggets 🐔",
            "Are you my phone battery? Because you're at 100% and I need you all day 🔋",
            "You must be from Ohio because you're making me act unwise 🤪",
            "Are you a Discord mod? Because you just banned me from being normal 🎮",
            "Girl, you're more fire than my mixtape (and that's saying something) 🎵",
            "Are you a rare Pokémon? Because I choose you (periodt) ⚡",
            "You got that main character energy and I'm just an NPC in love 💕",
            "Are you a meme? Because you make me laugh and I want to share you with everyone 😂",
            "Girl, you're giving me butterflies like I just hit a TikTok dance perfectly 🦋",
            "Are you my sleep schedule? Because you're messed up but I can't live without you 😴",
            "You're more addictive than scrolling through memes at 3 AM 🌙",
            "Are you a notification? Because you always make my day better 📲",
            "Girl, you're the only cheat code I need in this game called life 🎮",
            "Are you my screen time? Because you're embarrassingly high but worth it 📊",
            "You must be a limited edition because you're one of a kind (no printer) 🖨️"
        ]
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("💘 RIZZ GENERATOR 9000 💘")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #ff00ff;
                margin: 20px;
                border: 2px solid #00ff00;
                padding: 10px;
                border-radius: 10px;
            }
        """)
        
        # Subtitle
        subtitle = QLabel("Generate premium Gen Z pickup lines")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #00ff00;
                margin-bottom: 20px;
            }
        """)
        
        # Rizz display area
        self.rizz_display = QTextEdit()
        self.rizz_display.setReadOnly(True)
        self.rizz_display.setPlainText("Click 'Generate Rizz' to get your premium pickup line! 🔥")
        self.rizz_display.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d44;
                border: 2px solid #00ff00;
                border-radius: 10px;
                padding: 15px;
                font-size: 16px;
                color: #ffffff;
                min-height: 150px;
            }
        """)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.generate_btn = QPushButton("🔥 Generate Rizz")
        self.generate_btn.clicked.connect(self.generate_rizz)
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff00ff;
                color: black;
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
                border: none;
                border-radius: 10px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #00ff00;
            }
            QPushButton:pressed {
                background-color: #ffff00;
            }
        """)
        
        self.copy_btn = QPushButton("📋 Copy to Clipboard")
        self.copy_btn.clicked.connect(self.copy_rizz)
        self.copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #00ff00;
                color: black;
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
                border: none;
                border-radius: 10px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #ffff00;
            }
        """)
        
        self.rate_btn = QPushButton("⭐ Rate This Rizz")
        self.rate_btn.clicked.connect(self.rate_rizz)
        self.rate_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffff00;
                color: black;
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
                border: none;
                border-radius: 10px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #ff00ff;
            }
        """)
        
        button_layout.addWidget(self.generate_btn)
        button_layout.addWidget(self.copy_btn)
        button_layout.addWidget(self.rate_btn)
        
        # Stats
        self.stats_label = QLabel("Rizz Level: Beginner | Success Rate: 0%")
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.stats_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #888888;
                margin: 10px;
            }
        """)
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.rizz_display)
        layout.addLayout(button_layout)
        layout.addWidget(self.stats_label)
        
        self.setLayout(layout)
        
        self.current_rizz = ""
        self.rizz_count = 0
        
    def generate_rizz(self):
        self.current_rizz = random.choice(self.rizz_lines)
        self.rizz_display.setPlainText(self.current_rizz)
        self.rizz_count += 1
        
        # Update stats
        rizz_levels = ["Beginner", "Mid", "Decent", "Fire", "Sigma", "Gigachad"]
        level = rizz_levels[min(self.rizz_count // 3, len(rizz_levels) - 1)]
        success_rate = min(self.rizz_count * 5, 100)
        self.stats_label.setText(f"Rizz Level: {level} | Success Rate: {success_rate}% | Lines Generated: {self.rizz_count}")
        
    def copy_rizz(self):
        if self.current_rizz:
            from PyQt5.QtWidgets import QApplication
            clipboard = QApplication.clipboard()
            clipboard.setText(self.current_rizz)
            
            # Show feedback
            original_text = self.copy_btn.text()
            self.copy_btn.setText("✅ Copied!")
            QTimer.singleShot(1000, lambda: self.copy_btn.setText(original_text))
        
    def rate_rizz(self):
        if not self.current_rizz:
            return
            
        ratings = [
            "💀 This ain't it chief",
            "😬 Kinda sus ngl",
            "🤔 Mid rizz energy",
            "🔥 That's bussin!",
            "👑 Sigma level rizz",
            "🚀 Absolute unit energy"
        ]
        
        rating = random.choice(ratings)
        self.rizz_display.setPlainText(f"{self.current_rizz}\n\n--- RATING ---\n{rating}")
