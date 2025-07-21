import sys
from PyQt5.QtWidgets import QApplication, QSplashScreen, QLabel, QVBoxLayout, QWidget, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPixmap, QFont, QMovie, QPainter, QLinearGradient, QRadialGradient, QColor, QBrush
import random
import math

class BrainrotSplashScreen(QSplashScreen):
    finished = pyqtSignal()
    
    def __init__(self):
        # Create a transparent pixmap for custom painting
        pixmap = QPixmap(900, 700)
        pixmap.fill(Qt.transparent)
        super().__init__(pixmap)
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setFixedSize(900, 700)
        
        # Animation properties
        self.animation_phase = 0
        self.orb_positions = []
        self.text_glow_intensity = 0
        self.text_glow_direction = 1
        
        # Initialize floating orbs
        for i in range(8):
            self.orb_positions.append({
                'x': random.randint(50, 850),
                'y': random.randint(50, 650),
                'dx': random.uniform(-2, 2),
                'dy': random.uniform(-2, 2),
                'size': random.randint(20, 60),
                'color_phase': random.randint(0, 360)
            })
        
        # Meme loading texts
        self.meme_texts = [
            "Initializing Vista glass effects...",
            "Loading premium rizz protocols...",
            "Calibrating Aero transparency...",
            "Downloading Ohio.dll (sus version)...",
            "Installing Skibidi drivers...",
            "Activating sigma grindset mode...",
            "Touching grass.exe not found...",
            "Loading TikTok brain damage...",
            "Gyatt detector calibration complete...",
            "NPC.dll loaded successfully...",
            "Vibe check protocols online...",
            "Brainrot OS ready to deploy..."
        ]
        
        self.current_text = self.meme_texts[0]
        self.text_index = 0
        
        # Animation timer
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(50)  # 20 FPS
        
        # Text update timer
        self.text_timer = QTimer()
        self.text_timer.timeout.connect(self.update_text)
        self.text_timer.start(800)
        
        # Close timer
        self.close_timer = QTimer()
        self.close_timer.timeout.connect(self.close_splash)
        self.close_timer.start(5000)  # 5 seconds for dramatic effect
        
    def update_animation(self):
        self.animation_phase += 1
        
        # Update orb positions
        for orb in self.orb_positions:
            orb['x'] += orb['dx']
            orb['y'] += orb['dy']
            orb['color_phase'] = (orb['color_phase'] + 2) % 360
            
            # Bounce off edges
            if orb['x'] <= 0 or orb['x'] >= 900:
                orb['dx'] *= -1
            if orb['y'] <= 0 or orb['y'] >= 700:
                orb['dy'] *= -1
                
            # Keep in bounds
            orb['x'] = max(0, min(900, orb['x']))
            orb['y'] = max(0, min(700, orb['y']))
        
        # Update text glow
        self.text_glow_intensity += self.text_glow_direction * 3
        if self.text_glow_intensity >= 100:
            self.text_glow_direction = -1
        elif self.text_glow_intensity <= 20:
            self.text_glow_direction = 1
            
        self.update()
        
    def update_text(self):
        if not self.isVisible():
            return
            
        # Cycle through meme texts
        self.text_index = (self.text_index + 1) % len(self.meme_texts)
        self.current_text = self.meme_texts[self.text_index]
        
    def close_splash(self):
        # Stop timers safely
        if hasattr(self, 'animation_timer') and self.animation_timer:
            self.animation_timer.stop()
        if hasattr(self, 'text_timer') and self.text_timer:
            self.text_timer.stop()
        if hasattr(self, 'close_timer') and self.close_timer:
            self.close_timer.stop()
        
        self.finished.emit()
        self.close()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Vista-style gradient background
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(135, 206, 250, 255))  # Sky blue
        gradient.setColorAt(0.3, QColor(70, 130, 180, 255))  # Steel blue
        gradient.setColorAt(0.7, QColor(25, 25, 112, 255))   # Midnight blue
        gradient.setColorAt(1, QColor(0, 0, 139, 255))       # Dark blue
        
        painter.fillRect(self.rect(), QBrush(gradient))
        
        # Draw animated orbs
        for orb in self.orb_positions:
            # Create radial gradient for each orb
            orb_gradient = QRadialGradient(orb['x'], orb['y'], orb['size'])
            
            # Color based on phase for animation
            hue = (orb['color_phase'] + self.animation_phase) % 360
            color1 = QColor.fromHsv(hue, 255, 255, 150)
            color2 = QColor.fromHsv((hue + 60) % 360, 200, 200, 80)
            color3 = QColor.fromHsv((hue + 120) % 360, 150, 150, 20)
            
            orb_gradient.setColorAt(0, color1)
            orb_gradient.setColorAt(0.5, color2)
            orb_gradient.setColorAt(1, color3)
            
            painter.setBrush(QBrush(orb_gradient))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(int(orb['x'] - orb['size']/2), 
                              int(orb['y'] - orb['size']/2), 
                              orb['size'], orb['size'])
        
        # Draw main title with glow effect
        title_color = QColor(255, 255, 255, 200 + int(self.text_glow_intensity))
        painter.setPen(title_color)
        painter.setFont(QFont('Segoe UI', 56, QFont.Bold))
        
        title_rect = self.rect()
        title_rect.setHeight(200)
        painter.drawText(title_rect, Qt.AlignCenter, "🧠 BrainrotOS Vista")
        
        # Draw subtitle with glass effect
        subtitle_color = QColor(200, 255, 255, 180)
        painter.setPen(subtitle_color)
        painter.setFont(QFont('Segoe UI', 24, QFont.Normal))
        
        subtitle_rect = self.rect()
        subtitle_rect.setTop(200)
        subtitle_rect.setHeight(100)
        painter.drawText(subtitle_rect, Qt.AlignCenter, "The Most Cursed OS Experience")
        
        # Draw loading text with animated dots
        loading_color = QColor(255, 255, 0, 150 + int(self.text_glow_intensity // 2))
        painter.setPen(loading_color)
        painter.setFont(QFont('Segoe UI', 18, QFont.Normal))
        
        dots = "." * ((self.animation_phase // 10) % 4)
        loading_text = f"Loading{dots}"
        
        loading_rect = self.rect()
        loading_rect.setTop(self.height() - 200)
        loading_rect.setHeight(50)
        painter.drawText(loading_rect, Qt.AlignCenter, loading_text)
        
        # Draw current meme text
        meme_color = QColor(255, 200, 255, 200)
        painter.setPen(meme_color)
        painter.setFont(QFont('Segoe UI', 14, QFont.Normal))
        
        meme_rect = self.rect()
        meme_rect.setTop(self.height() - 150)
        meme_rect.setHeight(100)
        painter.drawText(meme_rect, Qt.AlignCenter | Qt.TextWordWrap, self.current_text)
        
        # Draw progress bar effect
        progress = min(100, (self.animation_phase // 10) % 120)
        progress_rect = self.rect()
        progress_rect.setTop(self.height() - 50)
        progress_rect.setHeight(20)
        progress_rect.setLeft(100)
        progress_rect.setRight(self.width() - 100)
        
        # Progress bar background
        painter.setBrush(QBrush(QColor(255, 255, 255, 50)))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(progress_rect, 10, 10)
        
        # Progress bar fill
        fill_width = int((progress_rect.width() * progress) / 100)
        fill_rect = progress_rect
        fill_rect.setWidth(fill_width)
        
        progress_gradient = QLinearGradient(fill_rect.left(), 0, fill_rect.right(), 0)
        progress_gradient.setColorAt(0, QColor(0, 255, 255, 200))
        progress_gradient.setColorAt(0.5, QColor(0, 200, 255, 255))
        progress_gradient.setColorAt(1, QColor(0, 150, 255, 200))
        
        painter.setBrush(QBrush(progress_gradient))
        painter.drawRoundedRect(fill_rect, 10, 10)
