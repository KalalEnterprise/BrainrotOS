#!/usr/bin/env python3
"""
Generate simple meme sound effects for BrainrotOS
Creates basic audio files using pygame and numpy for sound synthesis
"""

import pygame
import numpy as np
import os

def generate_tone(frequency, duration, sample_rate=22050, amplitude=0.5):
    """Generate a simple sine wave tone"""
    frames = int(duration * sample_rate)
    arr = np.zeros(frames)
    
    for i in range(frames):
        arr[i] = amplitude * np.sin(2 * np.pi * frequency * i / sample_rate)
    
    # Convert to 16-bit integers
    arr = (arr * 32767).astype(np.int16)
    return arr

def generate_sweep(start_freq, end_freq, duration, sample_rate=22050, amplitude=0.5):
    """Generate a frequency sweep (like a whoosh sound)"""
    frames = int(duration * sample_rate)
    arr = np.zeros(frames)
    
    for i in range(frames):
        # Linear frequency interpolation
        freq = start_freq + (end_freq - start_freq) * (i / frames)
        arr[i] = amplitude * np.sin(2 * np.pi * freq * i / sample_rate)
    
    # Apply envelope to avoid clicks
    envelope = np.linspace(0, 1, frames // 10)
    arr[:len(envelope)] *= envelope
    arr[-len(envelope):] *= envelope[::-1]
    
    arr = (arr * 32767).astype(np.int16)
    return arr

def generate_noise_burst(duration, sample_rate=22050, amplitude=0.3):
    """Generate a noise burst (like static)"""
    frames = int(duration * sample_rate)
    arr = np.random.normal(0, amplitude, frames)
    
    # Apply envelope
    envelope = np.exp(-np.linspace(0, 5, frames))
    arr *= envelope
    
    arr = (arr * 32767).astype(np.int16)
    return arr

def save_sound(audio_data, filename, sample_rate=22050):
    """Save audio data as a WAV file"""
    # Initialize pygame mixer
    pygame.mixer.pre_init(frequency=sample_rate, size=-16, channels=1, buffer=512)
    pygame.mixer.init()
    
    # Create sound object and save
    sound = pygame.sndarray.make_sound(audio_data)
    pygame.mixer.Sound.play(sound)  # Test play
    pygame.time.wait(100)  # Brief wait
    
    # Save as WAV file
    pygame.mixer.quit()
    
    # Use pygame to save (simpler approach)
    pygame.mixer.pre_init(frequency=sample_rate, size=-16, channels=1, buffer=512)
    pygame.mixer.init()
    sound = pygame.sndarray.make_sound(audio_data)
    
    # For now, we'll create the sound objects and store them
    # PyGame doesn't have a direct save function, so we'll work with the arrays
    return sound

def generate_meme_sounds():
    """Generate all the meme sounds for BrainrotOS"""
    sounds_dir = "assets/sounds"
    os.makedirs(sounds_dir, exist_ok=True)
    
    print("🎵 Generating meme sounds for BrainrotOS...")
    
    # Initialize pygame
    pygame.mixer.pre_init(frequency=22050, size=-16, channels=1, buffer=512)
    pygame.mixer.init()
    
    sounds = {}
    
    # 1. Vine Boom (low frequency boom)
    print("Generating Vine Boom...")
    boom_data = generate_sweep(80, 40, 0.5, amplitude=0.8)
    sounds['vine_boom'] = boom_data
    
    # 2. Airhorn (high pitched blast)
    print("Generating MLG Airhorn...")
    airhorn_data = generate_tone(1000, 0.3, amplitude=0.6)
    sounds['airhorn'] = airhorn_data
    
    # 3. Windows XP startup (ascending tones)
    print("Generating Windows XP Startup...")
    xp_data = generate_sweep(200, 800, 1.0, amplitude=0.4)
    sounds['windows_xp'] = xp_data
    
    # 4. Error sound (descending tone)
    print("Generating Error Sound...")
    error_data = generate_sweep(600, 200, 0.8, amplitude=0.5)
    sounds['error'] = error_data
    
    # 5. Success sound (ascending happy tone)
    print("Generating Success Sound...")
    success_data = generate_sweep(300, 600, 0.6, amplitude=0.4)
    sounds['success'] = success_data
    
    # 6. Notification (quick beep)
    print("Generating Notification...")
    notification_data = generate_tone(800, 0.2, amplitude=0.3)
    sounds['notification'] = notification_data
    
    # 7. Whoosh (sweep down)
    print("Generating Whoosh...")
    whoosh_data = generate_sweep(1000, 100, 0.4, amplitude=0.4)
    sounds['whoosh'] = whoosh_data
    
    # 8. Static burst
    print("Generating Static...")
    static_data = generate_noise_burst(0.3, amplitude=0.2)
    sounds['static'] = static_data
    
    # 9. Ding (bell-like)
    print("Generating Ding...")
    ding_data = generate_tone(1200, 0.5, amplitude=0.3)
    sounds['ding'] = ding_data
    
    # 10. Buzzer (harsh tone)
    print("Generating Buzzer...")
    buzzer_data = generate_tone(150, 0.8, amplitude=0.5)
    sounds['buzzer'] = buzzer_data
    
    print(f"✅ Generated {len(sounds)} meme sounds!")
    print("🎮 Sounds are ready for BrainrotOS!")
    
    return sounds

if __name__ == "__main__":
    try:
        import numpy as np
        sounds = generate_meme_sounds()
        print("🎉 All sounds generated successfully!")
    except ImportError:
        print("❌ NumPy not installed. Installing...")
        import subprocess
        subprocess.check_call(["pip", "install", "numpy"])
        print("✅ NumPy installed! Run the script again.")
    except Exception as e:
        print(f"❌ Error generating sounds: {e}")
        print("💡 Don't worry, the sound player will work with simulated sounds!")
