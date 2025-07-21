import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QGridLayout, QFrame, QTextEdit,
                             QApplication, QDesktopWidget, QGraphicsDropShadowEffect,
                             QScrollArea, QSizePolicy)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect, QParallelAnimationGroup
from PyQt5.QtGui import (QFont, QPixmap, QPalette, QBrush, QPainter, QLinearGradient, 
                         QRadialGradient, QColor, QFontMetrics)
import random
import datetime
import math

class DesktopIcon(QPushButton):
    def __init__(self, name, emoji, app_callback=None):
        super().__init__()
        self.app_callback = app_callback
        self.name = name
        self.emoji = emoji
        self.setFixedSize(120, 120)
        self.setText(f"{emoji}\n{name}")
        
        # Add Vista-style glass effect
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(15)
        self.shadow_effect.setColor(QColor(0, 255, 255, 100))
        self.shadow_effect.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow_effect)
        
        # Animation properties
        self.hover_animation = QPropertyAnimation(self, b"geometry")
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.OutBounce)
        
        self.glow_timer = QTimer()
        self.glow_timer.timeout.connect(self.update_glow)
        self.glow_intensity = 0
        self.glow_direction = 1
        
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 40),
                    stop:0.1 rgba(255, 255, 255, 25),
                    stop:0.5 rgba(100, 100, 100, 15),
                    stop:0.9 rgba(50, 50, 50, 25),
                    stop:1 rgba(0, 0, 0, 40));
                border: 2px solid rgba(255, 255, 255, 60);
                border-radius: 15px;
                color: white;
                font-size: 11px;
                font-weight: bold;
                font-family: 'Segoe UI';
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 80);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 255, 255, 60),
                    stop:0.1 rgba(0, 255, 255, 40),
                    stop:0.5 rgba(0, 150, 255, 25),
                    stop:0.9 rgba(0, 100, 200, 40),
                    stop:1 rgba(0, 50, 150, 60));
                border: 2px solid rgba(0, 255, 255, 100);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 0, 255, 80),
                    stop:0.5 rgba(150, 0, 255, 60),
                    stop:1 rgba(100, 0, 200, 80));
                border: 2px solid rgba(255, 0, 255, 120);
            }
        """)
        
        if app_callback:
            self.clicked.connect(app_callback)
            
    def enterEvent(self, event):
        # Start hover animation
        current_rect = self.geometry()
        new_rect = QRect(current_rect.x() - 5, current_rect.y() - 5, 
                        current_rect.width() + 10, current_rect.height() + 10)
        
        self.hover_animation.setStartValue(current_rect)
        self.hover_animation.setEndValue(new_rect)
        self.hover_animation.start()
        
        # Start glow effect
        self.glow_timer.start(50)
        
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        # Reverse hover animation
        current_rect = self.geometry()
        new_rect = QRect(current_rect.x() + 5, current_rect.y() + 5, 
                        current_rect.width() - 10, current_rect.height() - 10)
        
        self.hover_animation.setStartValue(current_rect)
        self.hover_animation.setEndValue(new_rect)
        self.hover_animation.start()
        
        # Stop glow effect
        self.glow_timer.stop()
        self.glow_intensity = 0
        self.update_shadow()
        
        super().leaveEvent(event)
        
    def update_glow(self):
        self.glow_intensity += self.glow_direction * 5
        if self.glow_intensity >= 100:
            self.glow_direction = -1
        elif self.glow_intensity <= 0:
            self.glow_direction = 1
            
        self.update_shadow()
        
    def update_shadow(self):
        if hasattr(self, 'shadow_effect'):
            self.shadow_effect.setBlurRadius(15 + self.glow_intensity // 5)
            self.shadow_effect.setColor(QColor(0, 255, 255, 50 + self.glow_intensity))

class TaskBar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(60)
        
        # Add Vista-style glass effect
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(20)
        self.shadow_effect.setColor(QColor(0, 0, 0, 150))
        self.shadow_effect.setOffset(0, -3)
        self.setGraphicsEffect(self.shadow_effect)
        
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 80),
                    stop:0.1 rgba(200, 200, 255, 60),
                    stop:0.5 rgba(100, 150, 255, 40),
                    stop:0.9 rgba(50, 100, 200, 60),
                    stop:1 rgba(0, 50, 150, 80));
                border-top: 1px solid rgba(255, 255, 255, 100);
                border-radius: 0px;
            }
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Quick Launch area (like Vista)
        quick_launch = QWidget()
        quick_launch_layout = QHBoxLayout()
        quick_launch_layout.setContentsMargins(5, 5, 5, 5)
        quick_launch_layout.setSpacing(3)
        
        # Start button (Brainrot menu) with Vista orb style
        self.start_btn = QPushButton("🧠")
        self.start_btn.setFixedSize(50, 50)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background: qradialgradient(cx:0.5, cy:0.3, radius:0.8,
                    stop:0 rgba(255, 255, 255, 200),
                    stop:0.3 rgba(0, 255, 255, 150),
                    stop:0.7 rgba(0, 150, 255, 120),
                    stop:1 rgba(0, 100, 200, 180));
                border: 2px solid rgba(255, 255, 255, 100);
                border-radius: 25px;
                color: black;
                font-weight: bold;
                font-size: 20px;
                font-family: 'Segoe UI';
            }
            QPushButton:hover {
                background: qradialgradient(cx:0.5, cy:0.3, radius:0.8,
                    stop:0 rgba(255, 255, 255, 255),
                    stop:0.3 rgba(255, 255, 0, 200),
                    stop:0.7 rgba(255, 150, 0, 150),
                    stop:1 rgba(255, 100, 0, 200));
            }
            QPushButton:pressed {
                background: qradialgradient(cx:0.5, cy:0.7, radius:0.8,
                    stop:0 rgba(255, 0, 255, 200),
                    stop:0.5 rgba(150, 0, 255, 150),
                    stop:1 rgba(100, 0, 200, 180));
            }
        """)
        
        # Quick Launch icons (like Vista)
        quick_launch_icons = [
            ("🌐", "Internet Explorer"),
            ("📁", "File Explorer"),
            ("🎵", "Media Player"),
            ("📝", "Notepad"),
            ("🎮", "Games")
        ]
        
        for icon, tooltip in quick_launch_icons:
            btn = QPushButton(icon)
            btn.setFixedSize(32, 32)
            btn.setToolTip(tooltip)
            btn.setStyleSheet("""
                QPushButton {
                    background: rgba(255, 255, 255, 30);
                    border: 1px solid rgba(255, 255, 255, 50);
                    border-radius: 4px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 60);
                    border: 1px solid rgba(255, 255, 255, 100);
                }
                QPushButton:pressed {
                    background: rgba(255, 255, 255, 80);
                }
            """)
            quick_launch_layout.addWidget(btn)
            
        quick_launch.setLayout(quick_launch_layout)
        
        # Running applications area
        self.running_apps = QWidget()
        self.running_apps_layout = QHBoxLayout()
        self.running_apps_layout.setContentsMargins(5, 5, 5, 5)
        self.running_apps_layout.setSpacing(2)
        self.running_apps.setLayout(self.running_apps_layout)
        
        # Add some default "running" apps
        self.add_running_app("🧠 BrainrotOS", True)
        self.add_running_app("📷 Gyatt Cam", False)
        self.add_running_app("🔊 Meme Player", False)
        
        # Add glow animation to start button
        self.start_glow_timer = QTimer()
        self.start_glow_timer.timeout.connect(self.animate_start_button)
        self.start_glow_timer.start(100)
        self.start_glow_phase = 0
        
        # Vibe level indicator with glass effect
        self.vibe_label = QLabel("Vibe Level: 💯")
        self.vibe_label.setStyleSheet("""
            QLabel {
                background: rgba(255, 255, 255, 30);
                color: white;
                font-size: 12px;
                font-weight: bold;
                font-family: 'Segoe UI';
                padding: 8px 15px;
                border: 1px solid rgba(255, 255, 255, 50);
                border-radius: 15px;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 100);
            }
        """)
        
        # Clock with glass effect
        self.clock_label = QLabel()
        self.clock_label.setStyleSheet("""
            QLabel {
                background: rgba(255, 255, 255, 30);
                color: white;
                font-size: 12px;
                font-weight: bold;
                font-family: 'Segoe UI';
                padding: 8px 15px;
                border: 1px solid rgba(255, 255, 255, 50);
                border-radius: 15px;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 100);
            }
        """)
        
        # System tray area with animated icons
        self.system_tray = QLabel("🔊 📶 🔋")
        self.system_tray.setStyleSheet("""
            QLabel {
                background: rgba(255, 255, 255, 20);
                color: white;
                font-size: 14px;
                padding: 8px 12px;
                border: 1px solid rgba(255, 255, 255, 40);
                border-radius: 12px;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 100);
            }
        """)
        
        # Update clock
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        self.update_clock()
        
        # Animate system tray icons
        self.tray_timer = QTimer()
        self.tray_timer.timeout.connect(self.animate_tray)
        self.tray_timer.start(3000)
        
        layout.addWidget(self.start_btn)
        
        # Add separator
        separator1 = QWidget()
        separator1.setFixedWidth(2)
        separator1.setStyleSheet("background: rgba(255, 255, 255, 30);")
        layout.addWidget(separator1)
        
        # Add quick launch
        layout.addWidget(quick_launch)
        
        # Add separator
        separator2 = QWidget()
        separator2.setFixedWidth(2)
        separator2.setStyleSheet("background: rgba(255, 255, 255, 30);")
        layout.addWidget(separator2)
        
        # Add running apps
        layout.addWidget(self.running_apps)
        
        layout.addStretch()
        layout.addWidget(self.vibe_label)
        layout.addWidget(self.system_tray)
        layout.addWidget(self.clock_label)
        
        self.setLayout(layout)
        
    def animate_start_button(self):
        self.start_glow_phase += 1
        intensity = int(50 + 30 * math.sin(self.start_glow_phase * 0.1))
        
        glow_effect = QGraphicsDropShadowEffect()
        glow_effect.setBlurRadius(20)
        glow_effect.setColor(QColor(0, 255, 255, intensity))
        glow_effect.setOffset(0, 0)
        self.start_btn.setGraphicsEffect(glow_effect)
        
    def animate_tray(self):
        icons = ["🔊 📶 🔋", "🔇 📶 🔋", "🔊 📵 🔋", "🔊 📶 🪫", "🔊 📶 ⚡"]
        self.system_tray.setText(random.choice(icons))
        
    def add_running_app(self, name, is_active=False):
        """Add a running application to the taskbar"""
        app_btn = QPushButton(name)
        app_btn.setFixedSize(120, 32)
        
        if is_active:
            app_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(255, 255, 255, 60);
                    border: 2px solid rgba(255, 255, 255, 100);
                    border-radius: 4px;
                    color: white;
                    font-size: 10px;
                    font-weight: bold;
                    text-align: left;
                    padding-left: 5px;
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 80);
                }
            """)
        else:
            app_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(255, 255, 255, 20);
                    border: 1px solid rgba(255, 255, 255, 40);
                    border-radius: 4px;
                    color: rgba(255, 255, 255, 180);
                    font-size: 10px;
                    text-align: left;
                    padding-left: 5px;
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 40);
                    color: white;
                }
            """)
        
        self.running_apps_layout.addWidget(app_btn)
        return app_btn
    
    def update_clock(self):
        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M:%S")
        self.clock_label.setText(f"⏰ {time_str}")
        
        # Random vibe updates
        if random.randint(1, 30) == 1:  # 1/30 chance each second
            vibes = ["💯", "🔥", "💀", "😭", "🤡", "👑", "💎", "⚡", "🌟", "🚀"]
            self.vibe_label.setText(f"Vibe Level: {random.choice(vibes)}")

class EnhancedWeatherWidget(QWidget):
    """Enhanced weather widget with live updates"""
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 150)
        self.setup_ui()
        self.setup_timer()
        
    def setup_ui(self):
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(15)
        self.shadow_effect.setColor(QColor(0, 0, 0, 100))
        self.shadow_effect.setOffset(2, 2)
        self.setGraphicsEffect(self.shadow_effect)
        
        layout = QVBoxLayout()
        
        # Title bar
        title_label = QLabel("🌤️ Weather")
        title_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 100),
                    stop:1 rgba(200, 200, 255, 80));
                color: black;
                font-size: 12px;
                font-weight: bold;
                font-family: 'Segoe UI';
                padding: 8px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 120);
            }
        """)
        
        # Content area
        self.content_label = QLabel()
        self.content_label.setWordWrap(True)
        self.content_label.setStyleSheet("""
            QLabel {
                background: rgba(255, 255, 255, 40);
                color: white;
                font-size: 10px;
                font-family: 'Segoe UI';
                padding: 10px;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 60);
                border-top: none;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 100);
            }
        """)
        
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(title_label)
        layout.addWidget(self.content_label)
        self.setLayout(layout)
        self.update_weather()
        
    def setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_weather)
        self.timer.start(10000)  # Update every 10 seconds
        
    def update_weather(self):
        conditions = ["Sunny", "Cloudy", "Rainy", "Snowy", "Foggy", "Windy"]
        temps = ["15°C", "20°C", "25°C", "30°C", "35°C"]
        humidity = ["30%", "45%", "60%", "75%", "90%"]
        
        condition = random.choice(conditions)
        temp = random.choice(temps)
        hum = random.choice(humidity)
        
        self.content_label.setText(f"Currently: {condition}\nTemp: {temp}\nHumidity: {hum}\nWind: 5 mph")

class EnhancedCalendarWidget(QWidget):
    """Enhanced calendar widget with events"""
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 150)
        self.setup_ui()
        
    def setup_ui(self):
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(15)
        self.shadow_effect.setColor(QColor(0, 0, 0, 100))
        self.shadow_effect.setOffset(2, 2)
        self.setGraphicsEffect(self.shadow_effect)
        
        layout = QVBoxLayout()
        
        title_label = QLabel("📅 Calendar")
        title_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 100),
                    stop:1 rgba(200, 200, 255, 80));
                color: black;
                font-size: 12px;
                font-weight: bold;
                font-family: 'Segoe UI';
                padding: 8px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 120);
            }
        """)
        
        now = datetime.datetime.now()
        content = f"Today: {now.strftime('%B %d')}\nEvents:\n• Rizz meeting @ 3PM\n• Vibe check @ 5PM\n• Touch grass (pending)"
        
        content_label = QLabel(content)
        content_label.setWordWrap(True)
        content_label.setStyleSheet("""
            QLabel {
                background: rgba(255, 255, 255, 40);
                color: white;
                font-size: 10px;
                font-family: 'Segoe UI';
                padding: 10px;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 60);
                border-top: none;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 100);
            }
        """)
        
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(title_label)
        layout.addWidget(content_label)
        self.setLayout(layout)

class EnhancedSystemWidget(QWidget):
    """Enhanced system monitor widget"""
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 150)
        self.setup_ui()
        self.setup_timer()
        
    def setup_ui(self):
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(15)
        self.shadow_effect.setColor(QColor(0, 0, 0, 100))
        self.shadow_effect.setOffset(2, 2)
        self.setGraphicsEffect(self.shadow_effect)
        
        layout = QVBoxLayout()
        
        title_label = QLabel("💻 System")
        title_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 100),
                    stop:1 rgba(200, 200, 255, 80));
                color: black;
                font-size: 12px;
                font-weight: bold;
                font-family: 'Segoe UI';
                padding: 8px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 120);
            }
        """)
        
        self.content_label = QLabel()
        self.content_label.setWordWrap(True)
        self.content_label.setStyleSheet("""
            QLabel {
                background: rgba(255, 255, 255, 40);
                color: white;
                font-size: 10px;
                font-family: 'Segoe UI';
                padding: 10px;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 60);
                border-top: none;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 100);
            }
        """)
        
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(title_label)
        layout.addWidget(self.content_label)
        self.setLayout(layout)
        self.update_stats()
        
    def setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(2000)  # Update every 2 seconds
        
    def update_stats(self):
        cpu = random.randint(10, 95)
        ram = random.randint(2, 8)
        disk = random.randint(100, 500)
        
        self.content_label.setText(f"CPU: {cpu}%\nRAM: {ram}GB used\nDisk: {disk}GB free\nVibes: Maximum")

class EnhancedMusicWidget(QWidget):
    """Enhanced music player widget"""
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 150)
        self.setup_ui()
        self.setup_timer()
        
    def setup_ui(self):
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(15)
        self.shadow_effect.setColor(QColor(0, 0, 0, 100))
        self.shadow_effect.setOffset(2, 2)
        self.setGraphicsEffect(self.shadow_effect)
        
        layout = QVBoxLayout()
        
        title_label = QLabel("🎵 Now Playing")
        title_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 100),
                    stop:1 rgba(200, 200, 255, 80));
                color: black;
                font-size: 12px;
                font-weight: bold;
                font-family: 'Segoe UI';
                padding: 8px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 120);
            }
        """)
        
        self.content_label = QLabel()
        self.content_label.setWordWrap(True)
        self.content_label.setStyleSheet("""
            QLabel {
                background: rgba(255, 255, 255, 40);
                color: white;
                font-size: 10px;
                font-family: 'Segoe UI';
                padding: 10px;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 60);
                border-top: none;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 100);
            }
        """)
        
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(title_label)
        layout.addWidget(self.content_label)
        self.setLayout(layout)
        self.update_track()
        
    def setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_track)
        self.timer.start(15000)  # Change track every 15 seconds
        
    def update_track(self):
        tracks = [
            ("Skibidi Bop", "DJ Gyatt", "Ohio Hits"),
            ("Rizz Anthem", "Gen Alpha", "Brainrot Vol. 1"),
            ("Sigma Grindset", "Chad Music", "Based Beats"),
            ("No Cap", "Zoomer Collective", "TikTok Bangers")
        ]
        
        track, artist, album = random.choice(tracks)
        self.content_label.setText(f"Track: {track}\nArtist: {artist}\nAlbum: {album}\nVolume: 💯")

class EnhancedNotesWidget(QWidget):
    """Enhanced notes widget"""
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 150)
        self.setup_ui()
        
    def setup_ui(self):
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(15)
        self.shadow_effect.setColor(QColor(0, 0, 0, 100))
        self.shadow_effect.setOffset(2, 2)
        self.setGraphicsEffect(self.shadow_effect)
        
        layout = QVBoxLayout()
        
        title_label = QLabel("📝 Quick Notes")
        title_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 100),
                    stop:1 rgba(200, 200, 255, 80));
                color: black;
                font-size: 12px;
                font-weight: bold;
                font-family: 'Segoe UI';
                padding: 8px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 120);
            }
        """)
        
        content = "• Touch grass (postponed)\n• Learn new rizz lines\n• Update vibe check\n• Stream on Twitch\n• Buy more RGB"
        
        content_label = QLabel(content)
        content_label.setWordWrap(True)
        content_label.setStyleSheet("""
            QLabel {
                background: rgba(255, 255, 255, 40);
                color: white;
                font-size: 10px;
                font-family: 'Segoe UI';
                padding: 10px;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 60);
                border-top: none;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 100);
            }
        """)
        
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(title_label)
        layout.addWidget(content_label)
        self.setLayout(layout)

class VistaWidget(QWidget):
    """Vista-style sidebar widget"""
    def __init__(self, title, content):
        super().__init__()
        self.setFixedSize(200, 150)
        
        # Add glass effect
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(15)
        self.shadow_effect.setColor(QColor(0, 0, 0, 100))
        self.shadow_effect.setOffset(2, 2)
        self.setGraphicsEffect(self.shadow_effect)
        
        layout = QVBoxLayout()
        
        # Title bar
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 100),
                    stop:1 rgba(200, 200, 255, 80));
                color: black;
                font-size: 12px;
                font-weight: bold;
                font-family: 'Segoe UI';
                padding: 8px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 120);
            }
        """)
        
        # Content area
        content_label = QLabel(content)
        content_label.setWordWrap(True)
        content_label.setStyleSheet("""
            QLabel {
                background: rgba(255, 255, 255, 40);
                color: white;
                font-size: 10px;
                font-family: 'Segoe UI';
                padding: 10px;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 60);
                border-top: none;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 100);
            }
        """)
        
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(title_label)
        layout.addWidget(content_label)
        self.setLayout(layout)

class BrainrotDesktop(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧠 BrainrotOS Vista Edition")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set window to be fullscreen-ish
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, screen.width(), screen.height())
        
        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Main layout with sidebar
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Desktop area layout
        desktop_layout = QVBoxLayout()
        desktop_layout.setContentsMargins(0, 0, 0, 0)
        
        # Desktop area
        self.desktop_area = QWidget()
        self.setup_desktop()
        
        # Taskbar
        self.taskbar = TaskBar()
        
        desktop_layout.addWidget(self.desktop_area)
        desktop_layout.addWidget(self.taskbar)
        
        desktop_widget = QWidget()
        desktop_widget.setLayout(desktop_layout)
        
        # Vista-style sidebar
        self.sidebar = self.create_sidebar()
        
        main_layout.addWidget(desktop_widget)
        main_layout.addWidget(self.sidebar)
        
        main_widget.setLayout(main_layout)
        
        # Set Vista-style background with animated elements
        self.background_phase = 0
        self.background_timer = QTimer()
        self.background_timer.timeout.connect(self.animate_background)
        self.background_timer.start(100)
        
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(135, 206, 250, 255),
                    stop:0.3 rgba(70, 130, 180, 255),
                    stop:0.7 rgba(25, 25, 112, 255),
                    stop:1 rgba(0, 0, 139, 255));
            }
        """)
        
        # Store app windows
        self.app_windows = {}
        
    def create_sidebar(self):
        sidebar = QWidget()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 20);
                border-left: 1px solid rgba(255, 255, 255, 40);
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(15)
        
        # Create enhanced sidebar widgets with real functionality
        widgets = [
            EnhancedWeatherWidget(),
            EnhancedCalendarWidget(), 
            EnhancedSystemWidget(),
            EnhancedMusicWidget(),
            EnhancedNotesWidget()
        ]
        
        for widget in widgets:
            layout.addWidget(widget)
            
        layout.addStretch()
        
        # Animated Vista logo
        self.vista_logo = QLabel("🌌 Vista Vibes")
        self.vista_logo.setAlignment(Qt.AlignCenter)
        self.vista_logo.setStyleSheet("""
            QLabel {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                    stop:0 rgba(255, 255, 255, 100),
                    stop:0.5 rgba(0, 255, 255, 80),
                    stop:1 rgba(0, 100, 200, 100));
                color: white;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI';
                padding: 15px;
                border: 2px solid rgba(255, 255, 255, 80);
                border-radius: 20px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 150);
            }
        """)
        
        layout.addWidget(self.vista_logo)
        
        sidebar.setLayout(layout)
        return sidebar
        
    def animate_background(self):
        self.background_phase += 1
        # Create subtle color shifting effect
        hue_shift = int(20 * math.sin(self.background_phase * 0.02))
        
        self.setStyleSheet(f"""
            QMainWindow {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba({135 + hue_shift}, {206 + hue_shift//2}, 250, 255),
                    stop:0.3 rgba({70 + hue_shift}, {130 + hue_shift//2}, 180, 255),
                    stop:0.7 rgba({25 + hue_shift//2}, {25 + hue_shift//2}, 112, 255),
                    stop:1 rgba(0, 0, {139 + hue_shift//3}, 255));
            }}
        """)
        
    def setup_desktop(self):
        # Set desktop area style
        self.desktop_area.setStyleSheet("""
            QWidget {
                background: transparent;
            }
        """)
        
        layout = QGridLayout()
        layout.setSpacing(30)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Desktop icons with Vista-style arrangement
        icons = [
            ("Rizz Gen", "💘", self.open_rizz_generator),
            ("NPC Chat", "🤖", self.open_npc_chat),
            ("Meme Player", "🔊", self.open_sound_player),
            ("Vibe Check", "✅", self.open_vibe_check),
            ("Ohio Files", "📁", self.open_file_manager),
            ("Sigma Notes", "📝", self.open_notepad),
            ("Gyatt Cam", "📷", self.open_camera),
            ("Touch Grass", "🌱", self.touch_grass),
        ]
        
        self.desktop_icons = []
        row, col = 0, 0
        for name, emoji, callback in icons:
            icon = DesktopIcon(name, emoji, callback)
            self.desktop_icons.append(icon)
            layout.addWidget(icon, row, col)
            col += 1
            if col > 3:  # 4 icons per row for better Vista layout
                col = 0
                row += 1
        
        # Add floating animation to icons
        self.float_timer = QTimer()
        self.float_timer.timeout.connect(self.animate_floating_icons)
        self.float_timer.start(50)
        self.float_phase = 0
        
        # Add some stretch to push icons to top-left
        layout.setRowStretch(row + 1, 1)
        layout.setColumnStretch(4, 1)
        
        self.desktop_area.setLayout(layout)
        
    def animate_floating_icons(self):
        """Create subtle floating animation for desktop icons"""
        self.float_phase += 1
        
        for i, icon in enumerate(self.desktop_icons):
            # Each icon floats with a different phase
            offset_y = int(3 * math.sin((self.float_phase + i * 20) * 0.05))
            current_margins = icon.contentsMargins()
            icon.setContentsMargins(current_margins.left(), 
                                  offset_y, 
                                  current_margins.right(), 
                                  current_margins.bottom())
        
    def open_rizz_generator(self):
        if "rizz" not in self.app_windows:
            from apps.rizz_generator import RizzGeneratorApp
            self.app_windows["rizz"] = RizzGeneratorApp()
        self.app_windows["rizz"].show()
        self.app_windows["rizz"].raise_()
        
    def open_npc_chat(self):
        if "npc" not in self.app_windows:
            from apps.npc_chat import NPCChatApp
            self.app_windows["npc"] = NPCChatApp()
        self.app_windows["npc"].show()
        self.app_windows["npc"].raise_()
        
    def open_sound_player(self):
        if "sound" not in self.app_windows:
            from apps.sound_player import SoundPlayerApp
            self.app_windows["sound"] = SoundPlayerApp()
        self.app_windows["sound"].show()
        self.app_windows["sound"].raise_()
        
    def open_vibe_check(self):
        if "vibe" not in self.app_windows:
            from apps.vibe_check import VibeCheckApp
            self.app_windows["vibe"] = VibeCheckApp()
        self.app_windows["vibe"].show()
        self.app_windows["vibe"].raise_()
        
    def open_file_manager(self):
        # Placeholder for file manager
        self.show_placeholder("Ohio Files", "📁 Your files are in another castle (Ohio)")
        
    def open_notepad(self):
        # Placeholder for notepad
        self.show_placeholder("Sigma Notes", "📝 Write your sigma thoughts here")
        
    def open_camera(self):
        if "camera" not in self.app_windows:
            from apps.gyatt_cam import GyattCam
            self.app_windows["camera"] = GyattCam()
        self.app_windows["camera"].show()
        self.app_windows["camera"].raise_()
        
    def touch_grass(self):
        # Easter egg
        self.show_placeholder("Touch Grass", "🌱 grass.exe not found\nPlease install outside.dll")
        
    def show_placeholder(self, title, message):
        from PyQt5.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1a1a2e;
                color: #00ff00;
                font-family: 'Courier New';
            }
            QMessageBox QPushButton {
                background-color: #ff00ff;
                color: black;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
        """)
        msg.exec_()
