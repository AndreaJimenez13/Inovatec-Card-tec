"""styles.py — Paleta de colores y helpers de UI"""
import tkinter as tk

# Paleta: gris carbón, blanco hueso, acento teal oscuro
BG_DARK      = "#1c1f26"   # carbón profundo
BG_MEDIUM    = "#252a35"   # carbón medio
BG_LIGHT     = "#f4f5f7"   # gris muy claro / blanco hueso
WHITE        = "#ffffff"
CARD_BG      = "#ffffff"
CARD_BORDER  = "#dde1e9"
TEXT_DARK    = "#12151c"
TEXT_MID     = "#3d4452"
TEXT_MUTED   = "#7a8394"
ACCENT       = "#1a7a6e"   # teal oscuro profesional
ACCENT_LIGHT = "#e6f4f2"   # teal muy claro para fondos
ACCENT_HOVER = "#155f55"
DANGER       = "#c0392b"
DANGER_HOVER = "#992d22"
SUCCESS      = "#1e7c47"
SUCCESS_BG   = "#eaf7f0"

FONT_TITLE   = ("Georgia", 20, "bold")
FONT_H2      = ("Georgia", 15, "bold")
FONT_H3      = ("Helvetica", 12, "bold")
FONT_LABEL   = ("Helvetica", 10, "bold")
FONT_BODY    = ("Helvetica", 11)
FONT_SMALL   = ("Helvetica", 9)
FONT_MONO    = ("Courier New", 10)
FONT_CAPTION = ("Helvetica", 9)


def apply_entry_style(entry, width=None):
    kw = dict(
        font=FONT_BODY, relief="flat", bg=WHITE, fg=TEXT_DARK,
        insertbackground=TEXT_DARK, highlightthickness=1,
        highlightbackground=CARD_BORDER, highlightcolor=ACCENT,
    )
    if width:
        kw["width"] = width
    entry.configure(**kw)


def make_button(parent, text, command, style="primary", **kw):
    paleta = {
        "primary": (ACCENT,    WHITE,      ACCENT_HOVER),
        "danger":  (DANGER,    WHITE,      DANGER_HOVER),
        "outline": (WHITE,     ACCENT,     ACCENT_LIGHT),
        "ghost":   (BG_LIGHT,  TEXT_MID,   "#e0e3ea"),
    }
    bg, fg, active_bg = paleta.get(style, paleta["primary"])
    return tk.Button(
        parent, text=text, command=command, font=FONT_H3,
        bg=bg, fg=fg, activebackground=active_bg, activeforeground=fg,
        relief="flat", cursor="hand2", padx=18, pady=10, **kw,
    )


def separator(parent, color=CARD_BORDER, pady=0):
    tk.Frame(parent, bg=color, height=1).pack(fill="x", pady=pady)
