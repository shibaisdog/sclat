# Sclat

Python-based YouTube video player with ASCII art functionality.

<p align="center">
    <img src="./asset/sclatLogo.png" width="248" alt="Sclat Logo">
</p>

## 🌐 Language | 언어

[한국어](README.md) | [English](README.en.md)

## ⚙️ Requirements

> **Important**: pytubefix must be version 7.1rc2 for streaming video compatibility

-   Python 3.8+
-   pygame
-   OpenCV (cv2)
-   FFmpeg
-   chardet==5.2.0
-   pytubefix==7.1rc2
-   pyvidplayer2==0.9.24

## 🌟 Key Features

-   YouTube video playback and download functionality
-   Real-time ASCII art conversion mode
-   Intuitive keyboard controls
-   Video search functionality
-   Volume and playback control
-   GUI and CLI interfaces

## 🚀 How to Run

### Installation

**Windows**

```batch
install.bat
```

**Terminal**

```bash
pip install -r requirements.txt
```

### Usage

**Windows**

```batch
# GUI mode
start.bat
```

**Terminal**

```bash
# GUI mode
python main.py

# CLI mode
python main.py --nogui

# Single playback
python main.py --once

# Playlist mode
python main.py --play [URL1] [URL2]...
```

## 🎮 Video Controls

### Playback Control

| Key | Function          |
| --- | ----------------- |
| `R` | Restart video     |
| `P` | Play/Pause        |
| `M` | Mute/Unmute       |
| `L` | Toggle loop       |
| `A` | Toggle ASCII mode |

### Navigation

| Key | Function        |
| --- | --------------- |
| `↑` | Increase volume |
| `↓` | Decrease volume |
| `←` | Rewind 15s      |
| `→` | Forward 15s     |

## 🔍 Search Interface

-   Enter video URL or search term
-   Paste URL with `Ctrl+V`
-   Navigate results with arrow keys
-   Select and play with Enter
