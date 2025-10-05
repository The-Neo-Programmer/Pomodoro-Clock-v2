import customtkinter as ctk
import threading
import time
import tkinter.messagebox as msgbox
from tkinter import Canvas
import math
import random

class PomodoroTimer:
    def __init__(self):
        # Appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Window
        self.root = ctk.CTk()
        self.root.title("Pomodoro Timer")
        self.root.geometry("400x650")
        self.root.minsize(350, 650)

        # Colors
        self.colors = {
            "bg_primary": "#0d0d0d",
            "bg_secondary": "#1a1a1a",
            "bg_tertiary": "#2a2a2a",
            "accent_sage": "#87a96b",
            "accent_slate": "#708090",
            "accent_rust": "#b7472a",
            "accent_navy": "#2c3e50",
            "accent_amber": "#d4a574",
            "text_primary": "#f5f5f5",
            "text_secondary": "#b8b8b8",
            "text_tertiary": "#888888",
            "halo_blue": "#4a90e2",
            "halo_green": "#7ed321",
            "halo_orange": "#f5a623",
        }

        self.root.configure(fg_color=self.colors["bg_primary"])

        # Timer
        self.is_running = False
        self.is_paused = False
        self.current_session = "work"
        self.session_count = 0
        self.layout_horizontal = False

        self.work_time = 25 * 60
        self.short_break_time = 5 * 60
        self.long_break_time = 15 * 60
        self.time_remaining = self.work_time

        # Motivational messages
        self.motivational_messages = [
            "Let's concentrate", "Time to focus", "Deep work ahead",
            "Stay focused", "Excellence awaits", "Mindful productivity",
            "Focused energy", "Calm concentration", "Present moment"
        ]

        # Animation
        self.halo_animation = 0
        self.sphere_rotation = 0

        self.setup_ui()
        self.update_display()
        self.animate_halo()
        self.show_motivational_message()

    def show_motivational_message(self):
        message = random.choice(self.motivational_messages)
        self.motivation_label.configure(text=message)

    # ------------------- UI -------------------
    def setup_ui(self):
        self.main_frame = ctk.CTkScrollableFrame(
            self.root,
            fg_color=self.colors["bg_secondary"],
            corner_radius=12,
            scrollbar_button_color=self.colors["accent_slate"],
            scrollbar_button_hover_color=self.colors["accent_sage"]
        )
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        self.create_layout_toggle()

        self.content_container = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        self.content_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.create_title_section()
        self.create_motivational_section()
        self.create_sphere_section()
        self.create_time_display()
        self.create_session_indicator()
        self.create_control_buttons()
        self.create_preset_buttons()
        self.update_layout()

    def create_layout_toggle(self):
        toggle_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent",
            height=40
        )
        toggle_frame.pack(fill="x", padx=10, pady=(5, 0))

        self.layout_button = ctk.CTkButton(
            toggle_frame,
            text="⟷ HORIZONTAL",
            command=self.toggle_layout,
            font=ctk.CTkFont(family="Helvetica", size=10, weight="bold"),
            fg_color=self.colors["accent_slate"],
            hover_color=self.colors["accent_sage"],
            width=100,
            height=30,
            corner_radius=15
        )
        self.layout_button.pack(anchor="ne")

    def create_title_section(self):
        self.title_frame = ctk.CTkFrame(
            self.content_container,
            fg_color="transparent",
            height=60
        )
        self.title_frame.pack(fill="x", pady=(0, 15))
        self.title_frame.pack_propagate(False)

        accent_frame = ctk.CTkFrame(
            self.title_frame,
            fg_color="transparent"
        )
        accent_frame.pack(expand=True, fill="both")

        ctk.CTkFrame(accent_frame, fg_color=self.colors["accent_sage"], height=2).pack(fill="x", pady=(10, 5))

        self.title_label = ctk.CTkLabel(
            accent_frame,
            text="POMODORO TIMER",
            font=ctk.CTkFont(family="Helvetica", size=20, weight="bold"),
            text_color=self.colors["text_primary"]
        )
        self.title_label.pack(pady=5)

        ctk.CTkFrame(accent_frame, fg_color=self.colors["accent_rust"], height=2).pack(fill="x", pady=(5, 10))

    def create_motivational_section(self):
        self.motivation_frame = ctk.CTkFrame(
            self.content_container,
            fg_color=self.colors["bg_tertiary"],
            corner_radius=8,
            height=40
        )
        self.motivation_frame.pack(fill="x", pady=(0, 15))
        self.motivation_frame.pack_propagate(False)

        self.motivation_label = ctk.CTkLabel(
            self.motivation_frame,
            text="Let's concentrate",
            font=ctk.CTkFont(family="Helvetica", size=12, slant="italic"),
            text_color=self.colors["accent_amber"]
        )
        self.motivation_label.pack(expand=True)

    def create_sphere_section(self):
        self.sphere_frame = ctk.CTkFrame(
            self.content_container,
            fg_color="transparent",
            height=160
        )
        self.sphere_frame.pack(fill="x", pady=(0, 15))
        self.sphere_frame.pack_propagate(False)

        self.canvas = Canvas(
            self.sphere_frame,
            width=160,
            height=160,
            bg=self.colors["bg_secondary"],
            highlightthickness=0,
            relief='flat'
        )
        self.canvas.pack(expand=True)

    def create_time_display(self):
        self.time_frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.time_frame.pack(fill="x", pady=(0, 10))

        self.time_label = ctk.CTkLabel(
            self.time_frame,
            text="25:00",
            font=ctk.CTkFont(family="Helvetica", size=28, weight="bold"),
            text_color=self.colors["text_primary"]
        )
        self.time_label.pack()

    def create_session_indicator(self):
        self.indicator_frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.indicator_frame.pack(fill="x", pady=(0, 10))

        self.session_label = ctk.CTkLabel(
            self.indicator_frame,
            text="WORK SESSION",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            text_color=self.colors["accent_rust"]
        )
        self.session_label.pack()

        self.counter_label = ctk.CTkLabel(
            self.indicator_frame,
            text="Session 1 of 4",
            font=ctk.CTkFont(family="Helvetica", size=10),
            text_color=self.colors["text_secondary"]
        )
        self.counter_label.pack(pady=(3, 0))

    def create_control_buttons(self):
        self.control_frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.control_frame.pack(fill="x", pady=(0, 10))

        self.start_button = ctk.CTkButton(
            self.control_frame,
            text="START",
            command=self.toggle_timer,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors["accent_sage"],
            hover_color=self.colors["accent_amber"],
            width=100, height=35, corner_radius=18
        )
        self.start_button.pack(side="left", padx=(0, 10))

        self.reset_button = ctk.CTkButton(
            self.control_frame,
            text="RESET",
            command=self.reset_timer,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors["accent_slate"],
            hover_color=self.colors["accent_rust"],
            width=100, height=35, corner_radius=18
        )
        self.reset_button.pack(side="right", padx=(10, 0))

    def create_preset_buttons(self):
        self.preset_frame = ctk.CTkFrame(self.content_container, fg_color=self.colors["bg_tertiary"], corner_radius=10)
        self.preset_frame.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            self.preset_frame,
            text="QUICK PRESETS",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.colors["text_secondary"]
        ).pack(pady=(10, 5))

        self.preset_buttons_frame = ctk.CTkFrame(self.preset_frame, fg_color="transparent")
        self.preset_buttons_frame.pack(fill="x", padx=10, pady=(0, 10))

        presets = [("30 min", 30), ("1 hr", 60), ("1.5 hr", 90), ("2 hr", 120)]
        for i, (text, minutes) in enumerate(presets):
            btn = ctk.CTkButton(
                self.preset_buttons_frame,
                text=text,
                command=lambda m=minutes: self.set_preset(m),
                font=ctk.CTkFont(size=10, weight="bold"),
                fg_color=self.colors["accent_navy"],
                hover_color=self.colors["accent_sage"],
                width=70, height=25, corner_radius=12
            )
            btn.grid(row=0, column=i, padx=3, pady=3, sticky="ew")

        for i in range(4):
            self.preset_buttons_frame.grid_columnconfigure(i, weight=1)

    # ------------------- Timer & animation -------------------
    def toggle_layout(self):
        self.layout_horizontal = not self.layout_horizontal
        if self.layout_horizontal:
            self.root.geometry("700x400")
            self.layout_button.configure(text="⟱ VERTICAL")
        else:
            self.root.geometry("400x550")
            self.layout_button.configure(text="⟷ HORIZONTAL")

    def toggle_timer(self):
        if not self.is_running:
            self.start_timer()
        else:
            self.pause_timer()

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.is_paused = False
            self.start_button.configure(text="PAUSE")
            threading.Thread(target=self.run_timer, daemon=True).start()

    def pause_timer(self):
        self.is_running = False
        self.is_paused = True
        self.start_button.configure(text="RESUME")

    def reset_timer(self):
        self.is_running = False
        self.is_paused = False
        self.start_button.configure(text="START")
        self.current_session = "work"
        self.time_remaining = self.work_time
        self.session_count = 0
        self.update_display()
        self.show_motivational_message()

    def run_timer(self):
        while self.is_running and self.time_remaining > 0:
            time.sleep(1)
            if self.is_running:
                self.time_remaining -= 1
                self.root.after(0, self.update_display)
        if self.is_running:
            self.root.after(0, self.session_complete)

    def session_complete(self):
        self.is_running = False
        self.start_button.configure(text="START")
        msgbox.showinfo("Session Complete", f"{self.current_session.replace('_',' ').title()} completed!")
        self.next_session()
        self.show_motivational_message()

    def next_session(self):
        if self.current_session == "work":
            self.session_count += 1
            if self.session_count % 4 == 0:
                self.current_session = "long_break"
                self.time_remaining = self.long_break_time
            else:
                self.current_session = "short_break"
                self.time_remaining = self.short_break_time
        else:
            self.current_session = "work"
            self.time_remaining = self.work_time
        self.update_display()

    def set_preset(self, minutes):
        if not self.is_running:
            self.time_remaining = minutes * 60
            self.work_time = minutes * 60
            self.update_display()
            self.show_motivational_message()

    def update_display(self):
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        self.time_label.configure(text=f"{minutes:02d}:{seconds:02d}")

        session_names = {"work": "WORK SESSION", "short_break": "SHORT BREAK", "long_break": "LONG BREAK"}
        session_colors = {"work": self.colors["accent_rust"], "short_break": self.colors["accent_sage"], "long_break": self.colors["accent_navy"]}

        self.session_label.configure(text=session_names[self.current_session], text_color=session_colors[self.current_session])
        self.counter_label.configure(text=f"Session {self.session_count+1} of 4" if self.current_session=="work" else "Break Time")

    # ------------------- Sphere Animation -------------------
    def animate_halo(self):
        self.halo_animation += 0.1
        self.sphere_rotation += 0.02
        if self.halo_animation > 2*math.pi: self.halo_animation = 0
        if self.sphere_rotation > 2*math.pi: self.sphere_rotation = 0

        total_time = {"work": self.work_time, "short_break": self.short_break_time, "long_break": self.long_break_time}[self.current_session]
        progress = 1 - (self.time_remaining/total_time)
        self.draw_3d_sphere(progress)
        self.root.after(100, self.animate_halo)

    def draw_3d_sphere(self, progress):
        self.canvas.delete("all")
        cx, cy = 80, 80  # smaller center
        base_radius = 60
        layers = 15

        halo_radius = base_radius + 15
        halo_intensity = math.sin(self.halo_animation) * 0.3 + 0.7
        for i in range(5, 0, -1):
            halo_color = self.get_halo_color()
            self.canvas.create_oval(cx-halo_radius+i*1.5, cy-halo_radius+i*1.5,
                                    cx+halo_radius-i*1.5, cy+halo_radius-i*1.5,
                                    outline=halo_color, width=1)

        for layer in range(layers):
            layer_progress = layer / layers
            radius = base_radius * (1 - layer_progress*0.3)
            base_color = self.get_sphere_color()
            brightness = 0.3 + 0.7*(1-layer_progress)
            sphere_color = self.interpolate_color(base_color, "#ffffff", min(brightness,1)) 
            self.canvas.create_oval(cx-radius, cy-radius, cx+radius, cy+radius, fill=sphere_color, outline="")

    def get_halo_color(self):
        return random.choice([self.colors["halo_blue"], self.colors["halo_green"], self.colors["halo_orange"]])

    def get_sphere_color(self):
        return self.colors["accent_sage"]

    def interpolate_color(self, color1, color2, t):
        c1 = [int(color1[i:i+2], 16) for i in (1,3,5)]
        c2 = [int(color2[i:i+2], 16) for i in (1,3,5)]
        ci = [int(c1[j]*(1-t)+c2[j]*t) for j in range(3)]
        return "#" + "".join(f"{v:02x}" for v in ci)

    def update_layout(self):
        pass  # optional future layout changes

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = PomodoroTimer()
    app.run()
