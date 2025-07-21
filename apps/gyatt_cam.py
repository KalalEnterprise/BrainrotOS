from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFrame, QGridLayout, QSlider, QComboBox,
                             QGraphicsDropShadowEffect, QProgressBar)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QPixmap, QPainter, QLinearGradient, QRadialGradient, QColor, QBrush
import random
import datetime
import math

class GyattCam(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📷 Gyatt Cam Pro Vista Edition")
        self.setGeometry(200, 150, 700, 600)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(135, 206, 250, 255),
                    stop:0.3 rgba(70, 130, 180, 255),
                    stop:0.7 rgba(25, 25, 112, 255),
                    stop:1 rgba(0, 0, 139, 255));
                color: white;
                font-family: 'Segoe UI';
            }
        """)
        
        self.setup_ui()
        
        # Camera simulation properties
        self.is_recording = False
        self.gyatt_level = 50
        self.detection_active = False
        self.detected_objects = []
        
        # Animation timers
        self.detection_timer = QTimer()
        self.detection_timer.timeout.connect(self.update_detection)
        
        self.gyatt_animation_timer = QTimer()
        self.gyatt_animation_timer.timeout.connect(self.animate_gyatt_level)
        self.gyatt_animation_timer.start(100)
        
        self.animation_phase = 0
        
    def setup_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)
        
        # Left panel - Camera view
        camera_panel = self.create_camera_panel()
        
        # Right panel - Controls
        controls_panel = self.create_controls_panel()
        
        main_layout.addWidget(camera_panel, 2)
        main_layout.addWidget(controls_panel, 1)
        
        self.setLayout(main_layout)
        
    def create_camera_panel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 20);
                border: 2px solid rgba(255, 255, 255, 60);
                border-radius: 15px;
            }
        """)
        
        # Add glass effect
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(20)
        shadow_effect.setColor(QColor(0, 0, 0, 100))
        shadow_effect.setOffset(3, 3)
        panel.setGraphicsEffect(shadow_effect)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Camera title
        title = QLabel("📷 GYATT DETECTION CAMERA")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: white;
                background: rgba(0, 0, 0, 50);
                padding: 10px;
                border-radius: 8px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 100);
            }
        """)
        
        # Camera viewport (simulated)
        self.camera_viewport = QLabel()
        self.camera_viewport.setMinimumSize(400, 300)
        self.camera_viewport.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0, 0, 0, 200),
                    stop:0.5 rgba(20, 20, 40, 180),
                    stop:1 rgba(0, 0, 0, 200));
                border: 3px solid rgba(0, 255, 255, 100);
                border-radius: 10px;
                color: #00ff00;
                font-size: 14px;
                font-family: 'Courier New';
            }
        """)
        self.camera_viewport.setAlignment(Qt.AlignCenter)
        self.camera_viewport.setText("📷 CAMERA INITIALIZING...\n\n🔍 Scanning for gyatt levels...\n\n⚡ AI Detection: STANDBY")
        
        # Status bar
        self.status_bar = QLabel("📊 Status: Ready | 🎯 Gyatt Level: 0% | 📡 Objects: 0")
        self.status_bar.setStyleSheet("""
            QLabel {
                background: rgba(0, 0, 0, 100);
                color: #00ff00;
                font-size: 12px;
                font-family: 'Courier New';
                padding: 8px;
                border-radius: 5px;
                border: 1px solid rgba(0, 255, 0, 50);
            }
        """)
        
        layout.addWidget(title)
        layout.addWidget(self.camera_viewport)
        layout.addWidget(self.status_bar)
        
        panel.setLayout(layout)
        return panel
        
    def create_controls_panel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 15);
                border: 2px solid rgba(255, 255, 255, 40);
                border-radius: 15px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Controls title
        controls_title = QLabel("🎛️ GYATT CONTROLS")
        controls_title.setAlignment(Qt.AlignCenter)
        controls_title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: white;
                background: rgba(255, 0, 255, 30);
                padding: 8px;
                border-radius: 8px;
                border: 1px solid rgba(255, 0, 255, 60);
            }
        """)
        
        # Start/Stop Detection button
        self.detection_btn = QPushButton("🔍 START DETECTION")
        self.detection_btn.clicked.connect(self.toggle_detection)
        self.detection_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 255, 0, 150),
                    stop:1 rgba(0, 150, 0, 200));
                color: black;
                font-size: 14px;
                font-weight: bold;
                padding: 15px;
                border: 2px solid rgba(255, 255, 255, 100);
                border-radius: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 255, 255, 150),
                    stop:1 rgba(0, 200, 255, 200));
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 0, 255, 150),
                    stop:1 rgba(200, 0, 255, 200));
            }
        """)
        
        # Gyatt Sensitivity slider
        sensitivity_label = QLabel("🎯 Gyatt Sensitivity:")
        sensitivity_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 12px;
                font-weight: bold;
            }
        """)
        
        self.sensitivity_slider = QSlider(Qt.Horizontal)
        self.sensitivity_slider.setRange(1, 100)
        self.sensitivity_slider.setValue(50)
        self.sensitivity_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 2px solid rgba(255, 255, 255, 100);
                height: 8px;
                background: rgba(0, 0, 0, 100);
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                    stop:0 rgba(255, 255, 255, 255),
                    stop:0.5 rgba(255, 0, 255, 200),
                    stop:1 rgba(150, 0, 255, 255));
                border: 2px solid rgba(255, 255, 255, 150);
                width: 20px;
                margin: -6px 0;
                border-radius: 10px;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255, 0, 255, 150),
                    stop:1 rgba(0, 255, 255, 150));
                border-radius: 4px;
            }
        """)
        
        # Detection mode combo
        mode_label = QLabel("🤖 Detection Mode:")
        mode_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 12px;
                font-weight: bold;
            }
        """)
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "🎯 Standard Gyatt",
            "🔥 Ohio Mode", 
            "💀 Sigma Detection",
            "🌟 Rizz Scanner",
            "⚡ Skibidi Tracker"
        ])
        self.mode_combo.setStyleSheet("""
            QComboBox {
                background: rgba(255, 255, 255, 30);
                color: white;
                font-size: 12px;
                padding: 8px;
                border: 2px solid rgba(255, 255, 255, 60);
                border-radius: 8px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
            }
        """)
        
        # Gyatt Level meter
        meter_label = QLabel("📊 Current Gyatt Level:")
        meter_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 12px;
                font-weight: bold;
            }
        """)
        
        self.gyatt_meter = QProgressBar()
        self.gyatt_meter.setRange(0, 100)
        self.gyatt_meter.setValue(0)
        self.gyatt_meter.setStyleSheet("""
            QProgressBar {
                border: 2px solid rgba(255, 255, 255, 100);
                border-radius: 8px;
                background-color: rgba(0, 0, 0, 100);
                text-align: center;
                font-weight: bold;
                color: white;
                height: 25px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255, 0, 0, 200),
                    stop:0.5 rgba(255, 255, 0, 200),
                    stop:1 rgba(0, 255, 0, 200));
                border-radius: 6px;
            }
        """)
        
        # Action buttons
        buttons_layout = QVBoxLayout()
        
        self.screenshot_btn = QPushButton("📸 Take Screenshot")
        self.screenshot_btn.clicked.connect(self.take_screenshot)
        self.screenshot_btn.setStyleSheet(self.get_button_style("#ffff00"))
        
        self.record_btn = QPushButton("🎥 Start Recording")
        self.record_btn.clicked.connect(self.toggle_recording)
        self.record_btn.setStyleSheet(self.get_button_style("#ff00ff"))
        
        self.calibrate_btn = QPushButton("⚙️ Calibrate Gyatt")
        self.calibrate_btn.clicked.connect(self.calibrate_gyatt)
        self.calibrate_btn.setStyleSheet(self.get_button_style("#00ffff"))
        
        buttons_layout.addWidget(self.screenshot_btn)
        buttons_layout.addWidget(self.record_btn)
        buttons_layout.addWidget(self.calibrate_btn)
        
        # Add everything to layout
        layout.addWidget(controls_title)
        layout.addWidget(self.detection_btn)
        layout.addWidget(sensitivity_label)
        layout.addWidget(self.sensitivity_slider)
        layout.addWidget(mode_label)
        layout.addWidget(self.mode_combo)
        layout.addWidget(meter_label)
        layout.addWidget(self.gyatt_meter)
        layout.addLayout(buttons_layout)
        layout.addStretch()
        
        panel.setLayout(layout)
        return panel
        
    def get_button_style(self, color):
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {color},
                    stop:1 rgba(100, 100, 100, 200));
                color: black;
                font-size: 12px;
                font-weight: bold;
                padding: 10px;
                border: 2px solid rgba(255, 255, 255, 100);
                border-radius: 8px;
                margin: 3px;
            }}
            QPushButton:hover {{
                background: white;
            }}
            QPushButton:pressed {{
                background: rgba(200, 200, 200, 200);
            }}
        """
        
    def toggle_detection(self):
        self.detection_active = not self.detection_active
        
        if self.detection_active:
            self.detection_btn.setText("🛑 STOP DETECTION")
            self.detection_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(255, 0, 0, 150),
                        stop:1 rgba(150, 0, 0, 200));
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 15px;
                    border: 2px solid rgba(255, 255, 255, 100);
                    border-radius: 10px;
                }
            """)
            self.detection_timer.start(500)
            self.camera_viewport.setText("🔍 SCANNING ACTIVE...\n\n🎯 Detecting gyatt levels...\n\n⚡ AI Status: ONLINE")
        else:
            self.detection_btn.setText("🔍 START DETECTION")
            self.detection_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(0, 255, 0, 150),
                        stop:1 rgba(0, 150, 0, 200));
                    color: black;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 15px;
                    border: 2px solid rgba(255, 255, 255, 100);
                    border-radius: 10px;
                }
            """)
            self.detection_timer.stop()
            self.camera_viewport.setText("📷 DETECTION PAUSED\n\n🔍 Ready to scan...\n\n⚡ AI Status: STANDBY")
            
    def update_detection(self):
        # Simulate gyatt detection
        sensitivity = self.sensitivity_slider.value()
        mode = self.mode_combo.currentText()
        
        # Generate random detection results
        detection_chance = sensitivity / 100.0
        
        if random.random() < detection_chance:
            # Detected something!
            gyatt_level = random.randint(10, 100)
            self.gyatt_level = gyatt_level
            
            detection_messages = [
                f"🎯 GYATT DETECTED!\nLevel: {gyatt_level}%\n\n📍 Location: Center frame\n⚡ Confidence: {random.randint(85, 99)}%",
                f"🔥 OHIO ENERGY SPIKE!\nIntensity: {gyatt_level}%\n\n🌟 Rizz Factor: HIGH\n💀 Sigma Level: MAXIMUM",
                f"⚡ SKIBIDI DETECTED!\nPower: {gyatt_level}%\n\n🎮 Brainrot Index: CRITICAL\n🚨 Alert: TOUCH GRASS",
                f"💎 PREMIUM GYATT!\nQuality: {gyatt_level}%\n\n👑 Tier: S-RANK\n🎯 Accuracy: PERFECT"
            ]
            
            self.camera_viewport.setText(random.choice(detection_messages))
        else:
            # No detection
            scanning_messages = [
                "🔍 SCANNING...\n\n📡 Searching for targets...\n⚡ AI Status: ANALYZING",
                "🎯 SWEEP MODE ACTIVE\n\n🔄 Rotating sensors...\n📊 Data: COLLECTING",
                "⚡ DEEP SCAN INITIATED\n\n🧠 Neural networks: ACTIVE\n🎮 Brainrot: DETECTED"
            ]
            
            self.camera_viewport.setText(random.choice(scanning_messages))
            self.gyatt_level = max(0, self.gyatt_level - random.randint(1, 5))
        
        # Update status
        object_count = random.randint(0, 5) if self.detection_active else 0
        status = "ACTIVE" if self.detection_active else "STANDBY"
        self.status_bar.setText(f"📊 Status: {status} | 🎯 Gyatt Level: {self.gyatt_level}% | 📡 Objects: {object_count}")
        
    def animate_gyatt_level(self):
        self.animation_phase += 1
        
        # Animate the gyatt meter
        current_value = self.gyatt_meter.value()
        target_value = self.gyatt_level
        
        if current_value < target_value:
            self.gyatt_meter.setValue(min(target_value, current_value + 2))
        elif current_value > target_value:
            self.gyatt_meter.setValue(max(target_value, current_value - 2))
            
        # Add some visual flair
        if self.detection_active and self.animation_phase % 20 == 0:
            # Flash the border occasionally
            if random.random() < 0.3:
                self.camera_viewport.setStyleSheet("""
                    QLabel {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                            stop:0 rgba(0, 0, 0, 200),
                            stop:0.5 rgba(20, 20, 40, 180),
                            stop:1 rgba(0, 0, 0, 200));
                        border: 3px solid rgba(255, 0, 255, 200);
                        border-radius: 10px;
                        color: #ff00ff;
                        font-size: 14px;
                        font-family: 'Courier New';
                    }
                """)
                QTimer.singleShot(200, self.reset_camera_style)
                
    def reset_camera_style(self):
        self.camera_viewport.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0, 0, 0, 200),
                    stop:0.5 rgba(20, 20, 40, 180),
                    stop:1 rgba(0, 0, 0, 200));
                border: 3px solid rgba(0, 255, 255, 100);
                border-radius: 10px;
                color: #00ff00;
                font-size: 14px;
                font-family: 'Courier New';
            }
        """)
        
    def take_screenshot(self):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        filename = f"gyatt_screenshot_{timestamp.replace(':', '-')}.png"
        
        messages = [
            f"📸 Screenshot saved!\nFile: {filename}\n\n🎯 Gyatt Level: {self.gyatt_level}%\n✅ Quality: PREMIUM",
            f"📷 Image captured!\nName: {filename}\n\n🔥 Ohio Factor: MAXIMUM\n💎 Clarity: CRYSTAL",
            f"🎮 Screenshot acquired!\nPath: {filename}\n\n⚡ Brainrot: PRESERVED\n👑 Status: LEGENDARY"
        ]
        
        self.camera_viewport.setText(random.choice(messages))
        QTimer.singleShot(3000, lambda: self.camera_viewport.setText("📷 Ready for next capture..."))
        
    def toggle_recording(self):
        self.is_recording = not self.is_recording
        
        if self.is_recording:
            self.record_btn.setText("⏹️ Stop Recording")
            self.camera_viewport.setText("🎥 RECORDING ACTIVE\n\n🔴 REC • LIVE\n\n📊 Capturing gyatt data...")
        else:
            self.record_btn.setText("🎥 Start Recording")
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            filename = f"gyatt_video_{timestamp.replace(':', '-')}.mp4"
            self.camera_viewport.setText(f"🎬 Recording saved!\nFile: {filename}\n\n🎯 Duration: {random.randint(10, 60)}s\n✅ Quality: 4K ULTRA HD")
            QTimer.singleShot(3000, lambda: self.camera_viewport.setText("📷 Ready to record..."))
            
    def calibrate_gyatt(self):
        self.camera_viewport.setText("⚙️ CALIBRATING...\n\n🔧 Adjusting sensors...\n⚡ Optimizing detection...")
        
        # Simulate calibration process
        QTimer.singleShot(2000, lambda: self.camera_viewport.setText("✅ CALIBRATION COMPLETE!\n\n🎯 Accuracy: +25%\n🔥 Sensitivity: OPTIMIZED\n💎 Quality: ENHANCED"))
        QTimer.singleShot(5000, lambda: self.camera_viewport.setText("📷 CAMERA READY\n\n🎯 All systems: ONLINE\n⚡ Status: CALIBRATED"))
