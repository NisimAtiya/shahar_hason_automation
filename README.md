# Shahar Hason Ticket Availability Automation 🎭

This project automates the process of checking for new Shahar Hason stand-up shows and notifies the user when new events are published.

![Screenshot 1](images/Screenshot%202025-07-01%20at%2012.44.05.png)
![Screenshot 2](images/Screenshot%202025-07-01%20at%2012.44.21.png)

---

## 🚀 Features

- ✅ Automatically scans for new shows from a predefined source (e.g., event ticket site)
- 🔔 Sends desktop notifications or alerts when a new event is found
- 🧠 Remembers previously seen events using a local JSON file to avoid duplicate alerts
- 🖼️ Includes UI previews (see screenshots above)

---

## 📁 Project Structure

``` bash
shahar_hason_automation/
│
├── main.py # Entry point for the automation
├── checker/
│ └── checker.py # Handles scraping and event detection
│
├── notify/
│ └── notify.py # Manages notifications
│
├── data/
│ └── seen.json # Keeps track of already notified events
│
├── images/ # Screenshots for documentation
├── requirements.txt # Python dependencies
└── .gitignore

yaml
Copy
Edit

```
---

## ⚙️ Installation

1. **Clone the repository**  
```bash
git clone https://github.com/NisimAtiya/shahar_hason_automation.git
cd shahar_hason_automation
pip install -r requirements.txt

```
---

## ▶️ Usage

```bash 
python main.py
```

---


 ## 🙌 Credits
```bash
Developed by NisimAtiya && Eliya-shlomo
```

---




