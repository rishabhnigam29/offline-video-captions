# 🎬 Offline Video Captions (Unlimited & Free)

Generate **WebVTT captions** for **unlimited videos** completely **offline** using **OpenAI Whisper**.  
No subscriptions. No per-minute pricing. No uploads. Your videos never leave your computer.

This tool is ideal for **YouTubers, Udemy instructors, and course creators** who want fast, accurate captions at scale.

---

## ✨ Features

- ✅ **Unlimited captions** (no usage limits)
- 🔒 **100% offline** – your videos stay on your machine
- 💸 **Free & open source**
- ⚡ **Batch processing** for entire folders
- 🧠 Powered by **OpenAI Whisper**
- 📁 **Folder structure preserved** automatically
- 📄 Outputs **WebVTT (.vtt)** files
- 🐳 Simple **Docker-based setup**

---

## 🚀 How It Works

1. Put all your videos into a folder (subfolders supported)
2. Run the tool once using Docker
3. Captions are generated automatically
4. Upload captions anywhere you want

---

## 📂 Folder Structure

### Input
```
course/
├── Module 1/
│   ├── lesson1.mp4
│   └── lesson2.mp4
└── Module 2/
    └── lesson3.mp4
```

### Output
```
captions/
├── Module 1/
│   ├── lesson1.vtt
│   └── lesson2.vtt
└── Module 2/
    └── lesson3.vtt
```

---

## 🛠 Requirements

- Docker Desktop (Free)
- Windows / macOS / Linux

Download: https://www.docker.com/products/docker-desktop/

---

## ▶️ Usage

### Build the Image
```
docker build -t offline-video-captions .
```

### Run
```
docker run --rm \
  -v /path/to/course:/app/course \
  -v /path/to/captions:/app/captions \
  offline-video-captions
```

---

## ⚙️ Configuration

Edit in `generate_vtt.py`:

```
MODEL_SIZE = "small"   # tiny | base | small | medium | large
LANGUAGE = "en"
```

---

## 📦 Tech Stack

- Python 3.10
- OpenAI Whisper
- FFmpeg
- Docker
- CPU-only

---

## 📜 License

MIT License
