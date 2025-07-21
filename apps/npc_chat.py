from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QTextEdit, QLineEdit, QScrollArea)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import random
import datetime

class NPCChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🤖 NPC Chat v2.0")
        self.setGeometry(250, 150, 600, 500)
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a2e;
                color: white;
                font-family: 'Courier New';
            }
        """)
        
        self.setup_ui()
        
        # NPC responses database
        self.npc_responses = [
            "Hello there! I used to be an adventurer like you...",
            "Have you seen my sweet roll?",
            "I work for Belethor, at the general goods store.",
            "The weather's been good lately, hasn't it?",
            "I mostly deal with petty thievery and drunken brawls.",
            "Do you get to the Cloud District very often?",
            "I find your hand empty of coin.",
            "Stay safe out there.",
            "Another wanderer, here to lick my father's boots.",
            "I've got my eye on you.",
            "The gods gave you two hands, and you use them both for your weapon.",
            "You look like you could use a drink.",
            "I don't know you, and I don't care to know you.",
            "Keep your nose out of trouble.",
            "What brings you to our humble town?",
            "I haven't seen you around here before.",
            "Times are tough, but we make do.",
            "The roads aren't safe these days.",
            "I heard there's trouble brewing in the capital.",
            "You remind me of my cousin's friend's neighbor."
        ]
        
        self.gen_z_responses = [
            "That's so Ohio fr fr 💀",
            "No cap, you're speaking facts rn",
            "This conversation is giving main character energy ✨",
            "Periodt, that's the tea ☕",
            "You're lowkey spitting bars ngl 🔥",
            "That's bussin, not gonna lie",
            "I'm deceased 💀💀💀",
            "This is sending me to another dimension",
            "You understood the assignment 💯",
            "That's a whole mood honestly",
            "I'm living for this energy rn",
            "This hits different though 🎯",
            "You're the main character fr",
            "That's so valid bestie ✅",
            "I'm obsessed with this vibe",
            "This is giving sigma energy 👑",
            "You're speaking my language rn",
            "That's absolutely sending me 🚀",
            "This conversation is elite tier",
            "You're literally iconic for this"
        ]
        
        self.chat_history = []
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("🤖 NPC CHAT SIMULATOR 🤖")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #00ff00;
                margin: 15px;
                border: 2px solid #ff00ff;
                padding: 10px;
                border-radius: 10px;
            }
        """)
        
        # Mode selector
        mode_layout = QHBoxLayout()
        
        self.classic_btn = QPushButton("🏰 Classic NPC")
        self.classic_btn.clicked.connect(lambda: self.set_mode("classic"))
        self.classic_btn.setStyleSheet(self.get_button_style("#8B4513"))
        
        self.genz_btn = QPushButton("📱 Gen Z NPC")
        self.genz_btn.clicked.connect(lambda: self.set_mode("genz"))
        self.genz_btn.setStyleSheet(self.get_button_style("#ff00ff"))
        
        self.random_btn = QPushButton("🎲 Random Mode")
        self.random_btn.clicked.connect(lambda: self.set_mode("random"))
        self.random_btn.setStyleSheet(self.get_button_style("#00ff00"))
        
        mode_layout.addWidget(self.classic_btn)
        mode_layout.addWidget(self.genz_btn)
        mode_layout.addWidget(self.random_btn)
        
        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d44;
                border: 2px solid #00ff00;
                border-radius: 10px;
                padding: 15px;
                font-size: 14px;
                color: #ffffff;
                min-height: 250px;
            }
        """)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message to the NPC...")
        self.message_input.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d44;
                border: 2px solid #ff00ff;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                color: white;
            }
        """)
        self.message_input.returnPressed.connect(self.send_message)
        
        self.send_btn = QPushButton("📤 Send")
        self.send_btn.clicked.connect(self.send_message)
        self.send_btn.setStyleSheet(self.get_button_style("#00ff00"))
        
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_btn)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        self.poke_btn = QPushButton("👆 Poke NPC")
        self.poke_btn.clicked.connect(self.poke_npc)
        self.poke_btn.setStyleSheet(self.get_button_style("#ffff00"))
        
        self.clear_btn = QPushButton("🗑️ Clear Chat")
        self.clear_btn.clicked.connect(self.clear_chat)
        self.clear_btn.setStyleSheet(self.get_button_style("#ff4444"))
        
        action_layout.addWidget(self.poke_btn)
        action_layout.addWidget(self.clear_btn)
        
        layout.addWidget(title)
        layout.addLayout(mode_layout)
        layout.addWidget(self.chat_display)
        layout.addLayout(input_layout)
        layout.addLayout(action_layout)
        
        self.setLayout(layout)
        
        self.current_mode = "classic"
        self.add_system_message("🤖 NPC Chat initialized. Select a mode and start chatting!")
        
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
        
    def set_mode(self, mode):
        self.current_mode = mode
        mode_messages = {
            "classic": "🏰 Classic NPC mode activated. Prepare for generic medieval dialogue!",
            "genz": "📱 Gen Z NPC mode activated. About to be absolutely unhinged!",
            "random": "🎲 Random mode activated. Chaos incoming!"
        }
        self.add_system_message(mode_messages[mode])
        
    def add_system_message(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.chat_display.append(f"<span style='color: #888888;'>[{timestamp}] SYSTEM: {message}</span>")
        
    def add_user_message(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.chat_display.append(f"<span style='color: #00ff00;'>[{timestamp}] YOU: {message}</span>")
        
    def add_npc_message(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.chat_display.append(f"<span style='color: #ff00ff;'>[{timestamp}] NPC: {message}</span>")
        
    def send_message(self):
        message = self.message_input.text().strip()
        if not message:
            return
            
        self.add_user_message(message)
        self.message_input.clear()
        
        # Generate NPC response
        QTimer.singleShot(500, self.generate_npc_response)  # Slight delay for realism
        
    def generate_npc_response(self):
        if self.current_mode == "classic":
            response = random.choice(self.npc_responses)
        elif self.current_mode == "genz":
            response = random.choice(self.gen_z_responses)
        else:  # random mode
            all_responses = self.npc_responses + self.gen_z_responses
            response = random.choice(all_responses)
            
        self.add_npc_message(response)
        
    def poke_npc(self):
        poke_responses = [
            "Ow! Why did you do that?",
            "Stop poking me!",
            "That's rude...",
            "I don't like being poked.",
            "Personal space, please!",
            "Hands to yourself!",
            "What was that for?",
            "Ouch! That hurt!",
            "Don't touch me!",
            "Why are you like this?"
        ]
        
        genz_poke_responses = [
            "Bestie, we don't poke people 💀",
            "That's giving harassment energy ngl",
            "Touch grass, not me 🌱",
            "I'm calling the vibe police 🚨",
            "That's not very cash money of you",
            "Periodt, keep your hands to yourself",
            "This ain't it chief 😬",
            "You're giving creepy uncle vibes",
            "I'm uncomfy, please stop 🛑",
            "That's a whole red flag fr"
        ]
        
        if self.current_mode == "genz" or (self.current_mode == "random" and random.choice([True, False])):
            response = random.choice(genz_poke_responses)
        else:
            response = random.choice(poke_responses)
            
        self.add_npc_message(response)
        
    def clear_chat(self):
        self.chat_display.clear()
        self.add_system_message("Chat cleared. Ready for new conversations!")
