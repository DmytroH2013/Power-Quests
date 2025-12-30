import tkinter as tk
import time
import os
import re
import json
import random

class TerminalHUD:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True, "-alpha", 0.95)
        self.root.geometry("550x700+100+100")
        self.root.configure(bg="#000000")

        # --- PORTABLE PATH LOGIC ---
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.FILE_PATH = os.path.join(self.BASE_DIR, "quests.json")
        self.STATS_PATH = os.path.join(self.BASE_DIR, "quest_stats.json")
        
        self.C_GREEN = "#00FF41"
        self.C_RED = "#FF3131"
        self.C_DIM = "#003B00"
        
        self.active_quests = {} 
        self.current_index = 0
        self.wait_until = 0
        self.start_session_time = time.time()

        self.stats = self.load_stats()
        self.setup_ui()
        
        self.system_log("KERNEL_BOOT_SEQUENCE_INITIALIZED...")
        self.system_log(f"BASE_DIR_DETECTED: {self.BASE_DIR}")
        self.update_loop()

    def system_log(self, message):
        """Prints high-density technical logs to the UI console."""
        timestamp = time.strftime("%H:%M:%S")
        memory_addr = hex(random.randint(0x1000, 0xFFFF))
        log_entry = f"[{timestamp}] {memory_addr} | {message}\n"
        
        self.console_output.config(state="normal")
        self.console_output.insert("end", log_entry)
        # Keep only the last 50 lines to prevent memory lag
        if float(self.console_output.index('end-1c')) > 50:
            self.console_output.delete("1.0", "2.0")
        self.console_output.see("end")
        self.console_output.config(state="disabled")

    def load_stats(self):
        default = {"quest_done": 0, "time_ran": 0}
        if os.path.exists(self.STATS_PATH):
            try:
                with open(self.STATS_PATH, "r") as f:
                    return json.load(f)
            except: return default
        return default

    def save_stats(self):
        curr_session = int(time.time() - self.start_session_time)
        data = {"quest_done": self.stats["quest_done"], "time_ran": self.stats["time_ran"] + curr_session}
        with open(self.STATS_PATH, "w") as f:
            json.dump(data, f, indent=4)
        self.system_log("STATS_BUFFER_FLUSHED_TO_DISK...")

    def process_json_file(self):
        if not os.path.exists(self.FILE_PATH):
            self.system_log("CRITICAL_ERR: quests.json_NOT_FOUND")
            return
        
        if time.time() < self.wait_until:
            self.system_log(f"THREAD_SLEEP: {int(self.wait_until - time.time())}s_REMAINING")
            return

        try:
            with open(self.FILE_PATH, "r") as f:
                data_list = json.load(f)
            
            if self.current_index < len(data_list):
                item = data_list[self.current_index]
                self.system_log(f"PARSING_INDEX_{self.current_index}: {item['type'].upper()}")
                
                if item["type"] == "quest":
                    name = item["task"].strip().lower().replace(" ", "_")
                    if name not in self.active_quests:
                        self.active_quests[name] = time.time() + 120 
                        self.current_index += 1
                        self.system_log(f"NEW_QUEST_PUSHED: {name}")
                
                elif item["type"] == "wait":
                    match = re.search(r'(\d+)\s*(sec|min|h)', item["duration"].lower())
                    val = int(match.group(1))
                    unit = match.group(2)
                    mult = 3600 if unit == 'h' else 60 if unit == 'min' else 1
                    seconds = val * mult
                    
                    self.wait_until = time.time() + seconds
                    self.current_index += 1
                    self.system_log(f"TIMER_SET: {seconds}s_DELAY_ENGAGED")
        except Exception as e:
            self.system_log(f"JSON_EXCEPTION: {str(e)[:30]}")

    def update_loop(self):
        self.process_json_file()
        self.save_stats()
        
        # Random technical "background noise"
        if random.random() > 0.8:
            noise = ["SCRUBBING_MEM_CACHE...", "ENCRYPTING_SESSION...", "STABILIZING_PIPES...", "FETCHING_CORE_TEMP..."]
            self.system_log(random.choice(noise))

        # Update HUD Text
        now = time.time()
        total_time = self.stats["time_ran"] + int(now - self.start_session_time)
        self.stats_lbl.config(text=f"DONE: {self.stats['quest_done']} | RUN: {total_time}s | INDEX: {self.current_index}")

        # Refresh Quest Display
        self.quest_display.config(state="normal")
        self.quest_display.delete("1.0", "end")
        for name, expiry in list(self.active_quests.items()):
            color_code = "[OK]" if now < expiry else "[!!]"
            self.quest_display.insert("end", f"{color_code} >> {name}\n")
        self.quest_display.config(state="disabled")

        self.root.after(1000, self.update_loop)

    def setup_ui(self):
        # Stats Bar
        self.stats_lbl = tk.Label(self.root, text="", fg=self.C_GREEN, bg="#000000", font=("Consolas", 9))
        self.stats_lbl.pack(fill="x", pady=5)

        # Active Quest Display
        self.quest_display = tk.Text(self.root, bg="#000000", fg=self.C_GREEN, font=("Consolas", 14, "bold"), height=5, borderwidth=0)
        self.quest_display.pack(fill="x", padx=20)

        tk.Label(self.root, text="--- SYSTEM LOG ---", fg=self.C_DIM, bg="#000000", font=("Consolas", 8)).pack()

        # Verbose Console Output
        self.console_output = tk.Text(self.root, bg="#000000", fg=self.C_GREEN, font=("Consolas", 8), height=20, borderwidth=0)
        self.console_output.pack(fill="both", expand=True, padx=20)

        # Input Area
        input_frame = tk.Frame(self.root, bg="#000000")
        input_frame.pack(fill="x", side="bottom", padx=10, pady=10)
        tk.Label(input_frame, text=">>>", fg=self.C_GREEN, bg="#000000", font=("Consolas", 12)).pack(side="left")
        self.entry = tk.Entry(input_frame, bg="#000000", fg=self.C_GREEN, borderwidth=0, font=("Consolas", 12), insertbackground=self.C_GREEN)
        self.entry.pack(side="left", fill="x", expand=True, padx=5)
        self.entry.bind("<Return>", self.process_input)
        
        self.root.bind("<Button-1>", self.start_move); self.root.bind("<B1-Motion>", self.do_move)

    def process_input(self, event):
        cmd = self.entry.get().strip().lower().replace(" ", "_")
        self.system_log(f"USER_INPUT_RECEIVED: {cmd}")
        if cmd in self.active_quests:
            del self.active_quests[cmd]
            self.stats["quest_done"] += 1
            self.system_log(f"QUEST_VALIDATED_AND_PURGED: {cmd}")
        elif cmd == "exit": self.root.destroy()
        else: self.system_log(f"UNRECOGNIZED_COMMAND: {cmd}")
        self.entry.delete(0, "end")

    def start_move(self, e): self.x, self.y = e.x, e.y
    def do_move(self, e): self.root.geometry(f"+{self.root.winfo_x()+(e.x-self.x)}+{self.root.winfo_y()+(e.y-self.y)}")

if __name__ == "__main__":
    root = tk.Tk(); app = TerminalHUD(root); root.mainloop()