
#⚡ POWER QUESTS: Terminal HUD v2.5

    Real-time Python Quest Tracker & System Kernel Simulator

Power Quests is a minimalist, portable HUD designed for developers who want to gamify their workflow. It floats above your IDE, providing a live "System Kernel" feed of your current objectives, automated timeouts, and persistent progress tracking.
📸 Preview

    [Insert a Screenshot of your HUD running here]

🎯 Features

    👾 Hacker Aesthetic: CRT-style phosphor green interface with high-density logging.

    📦 100% Portable: No installation required. Self-contained directory logic.

    ⏱️ Scripted Timers: Native support for wait commands to pace your workflow.

    📊 Performance Metrics: Automated persistence of XP and Uptime in JSON format.

    🪟 Stealth Mode: Borderless window with adjustable transparency (Alpha 0.95).

🛠️ Installation & Usage
1. Clone the Repository
Bash

git clone https://github.com/DmytroH2013/Power-Quests/tree/main
cd power-quests

2. Configure Your Mission (quests.json)

The kernel processes tasks sequentially. Use the following structure:
JSON

[
    { "type": "quest", "task": "Refactor Login logic" },
    { "type": "wait", "duration": "10sec" },
    { "type": "quest", "task": "Deploy to Staging" }
]

3. Launch the HUD
PowerShell

python main.py

⌨️ Command Protocol
Command	Description
[task_name]	Validates and purges the active mission from the kernel.
exit	Safely flushes stats to disk and terminates the process.
help	(Upcoming) Displays internal system manual.
🧩 Technical Architecture

The HUD operates on a non-blocking after() loop, allowing the UI to remain responsive while the background thread monitors the filesystem and timers.

<details> <summary><b>Click to expand File System Logic</b></summary>

    BASE_DIR: Automatically calculated at runtime to ensure portability.

    quest_stats.json: Updated every 1000ms to prevent data loss on crash.

    Regex Parser: Interprets human-readable time (sec/min/h) into integer seconds for the Python time module.

</details>
🤝 Contributing

    Fork the Project.

    Create your Feature Branch (git checkout -b feature/AmazingFeature).

    Commit your Changes (git commit -m 'Add some AmazingFeature').

    Push to the Branch (git push origin feature/AmazingFeature).

    Open a Pull Request.

📄 License

Distributed under the MIT License. See LICENSE for more information.
👑 System Admin

Dmytr - https://github.com/DmytroH2013

Project Link: https://github.com/YOUR_USERNAME/power-quests
🚀 Next Steps for you:

    Take a screenshot of the app running.

    Upload the screenshot to your GitHub repository folder.

    Replace the [Insert a Screenshot...] line in the README with ![HUD Preview](your_screenshot_name.png).
