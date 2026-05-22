"""screens/registro.py — Formulario de registro de acceso"""
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import random
import string

from styles import (
    BG_DARK, BG_MEDIUM, BG_LIGHT, WHITE, CARD_BG, ACCENT, ACCENT_LIGHT,
    TEXT_DARK, TEXT_MID, TEXT_MUTED, CARD_BORDER,
    FONT_TITLE, FONT_H2, FONT_H3, FONT_LABEL, FONT_BODY, FONT_SMALL,
    FONT_MONO, FONT_CAPTION, SUCCESS, SUCCESS_BG, DANGER,
    make_button, apply_entry_style, separator,
)
import db

PROGRAMAS = [
    "TIC's",
    "Ingenieria Industrial",
    "Inteligencia Artificial",
    "Mecatronica",
    "Logistica",
    "Gestion Empresarial",
    "Maestria",
    "Doctorado",
]
MODALIDADES = ["Escolarizado", "Sabatino"]

MOTIVOS_VISITA = [
    "Recoger a alguien",
    "Visita a oficinas",
    "Visita general",
]

DEPARTAMENTOS = [
    "Direccion General",
    "Recursos Humanos",
    "Servicios Escolares",
    "Finanzas y Contabilidad",
    "Tecnologias de Informacion",
    "Biblioteca",
    "Vinculacion y Extension",
    "Mantenimiento",
    "Seguridad",
    "Otro",
]


class PantallaRegistro(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_DARK)
        self.master = master
        self._tipo  = tk.StringVar(value="Estudiante")
        self._motivo_visita = tk.StringVar(value=MOTIVOS_VISITA[0])
        self._uid   = tk.StringVar(value="")
        self._reloj_id = None
        self._build()
        self._iniciar_reloj()

    # ─────────────────────────────────────────────────────────────────────────
    # Construccion de la interfaz
    # ─────────────────────────────────────────────────────────────────────────

    def _build(self):
        # ── Barra lateral izquierda (identidad + reloj) ──────────────────────
        sidebar = tk.Frame(self, bg=BG_DARK, width=230)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Frame(sidebar, bg=BG_DARK, height=40).pack()

        # Logo / titulo institucional
        logo_f = tk.Frame(sidebar, bg=BG_DARK)
        logo_f.pack(padx=24, pady=(0, 8))

        tk.Frame(logo_f, bg=ACCENT, width=3, height=36).pack(
            side="left", padx=(0, 12))

        lbl_f = tk.Frame(logo_f, bg=BG_DARK)
        lbl_f.pack(side="left")
        tk.Label(lbl_f, text="CONTROL", font=("Helvetica", 11, "bold"),
                 bg=BG_DARK, fg=WHITE).pack(anchor="w")
        tk.Label(lbl_f, text="DE ACCESO", font=("Helvetica", 11, "bold"),
                 bg=BG_DARK, fg=WHITE).pack(anchor="w")
        tk.Label(lbl_f, text="RFID", font=("Helvetica", 11, "bold"),
                 bg=BG_DARK, fg=ACCENT).pack(anchor="w")

        tk.Frame(sidebar, bg="#2e3340", height=1).pack(
            fill="x", padx=24, pady=20)

        # Reloj en tiempo real
        reloj_f = tk.Frame(sidebar, bg=BG_DARK)
        reloj_f.pack(padx=24, pady=(0, 6))

        tk.Label(reloj_f, text="HORA ACTUAL", font=("Helvetica", 8),
                 bg=BG_DARK, fg=TEXT_MUTED).pack(anchor="w")
        self.lbl_hora = tk.Label(reloj_f, text="",
                                  font=("Courier New", 22, "bold"),
                                  bg=BG_DARK, fg=WHITE)
        self.lbl_hora.pack(anchor="w", pady=(2, 0))

        # Fecha
        fecha_f = tk.Frame(sidebar, bg=BG_DARK)
        fecha_f.pack(padx=24, pady=(0, 20))
        tk.Label(fecha_f, text="FECHA", font=("Helvetica", 8),
                 bg=BG_DARK, fg=TEXT_MUTED).pack(anchor="w")
        self.lbl_fecha = tk.Label(fecha_f, text="",
                                   font=("Helvetica", 10),
                                   bg=BG_DARK, fg="#a0aab8")
        self.lbl_fecha.pack(anchor="w", pady=(2, 0))

        tk.Frame(sidebar, bg="#2e3340", height=1).pack(
            fill="x", padx=24, pady=(0, 20))

        # Info adicional en sidebar
        info_items = [
            ("Registra tu entrada",   "#a0aab8"),
            ("Acerca tu tarjeta RFID", "#a0aab8"),
            ("Completa el formulario", "#a0aab8"),
        ]
        for texto, color in info_items:
            fila = tk.Frame(sidebar, bg=BG_DARK)
            fila.pack(fill="x", padx=24, pady=3)
            tk.Frame(fila, bg=ACCENT, width=4, height=4).pack(
                side="left", padx=(0, 8))
            tk.Label(fila, text=texto, font=FONT_SMALL,
                     bg=BG_DARK, fg=color, anchor="w").pack(side="left")

        # Version
        tk.Label(sidebar, text="v1.0", font=FONT_CAPTION,
                 bg=BG_DARK, fg="#3d4452").pack(side="bottom", pady=12)

        # ── Divisor vertical ────────────────────────────────────────────────
        tk.Frame(self, bg="#2e3340", width=1).pack(side="left", fill="y")

        # ── Area principal (formulario) ──────────────────────────────────────
        main_f = tk.Frame(self, bg=BG_LIGHT)
        main_f.pack(side="left", fill="both", expand=True)

        # Header del formulario
        header = tk.Frame(main_f, bg=WHITE,
                          highlightthickness=1,
                          highlightbackground=CARD_BORDER)
        header.pack(fill="x")

        tk.Label(header, text="Registro de Acceso",
                 font=FONT_H2, bg=WHITE, fg=TEXT_DARK).pack(
                     side="left", padx=28, pady=16)

        # Badge de estado RFID en header
        self._badge_f = tk.Frame(header, bg="#f4f5f7",
                                  highlightthickness=1,
                                  highlightbackground=CARD_BORDER)
        self._badge_f.pack(side="right", padx=20, pady=12, ipadx=10, ipady=4)
        self._badge_lbl = tk.Label(self._badge_f,
                                    text="Sin tarjeta",
                                    font=FONT_SMALL, bg="#f4f5f7", fg=TEXT_MUTED)
        self._badge_lbl.pack()

        # Canvas con scroll
        canvas = tk.Canvas(main_f, bg=BG_LIGHT, highlightthickness=0)
        sb = tk.Scrollbar(main_f, orient="vertical", command=canvas.yview)
        sf = tk.Frame(canvas, bg=BG_LIGHT)
        sf.bind("<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=sf, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self._build_form(sf)

    def _build_form(self, parent):
        pad = dict(padx=28, pady=0)

        # ── Tarjeta RFID ─────────────────────────────────────────────────────
        tk.Frame(parent, bg=BG_LIGHT, height=18).pack()
        self._rfid_f = tk.Frame(
            parent, bg=ACCENT_LIGHT, cursor="hand2",
            highlightthickness=1, highlightbackground="#a8d5cf")
        self._rfid_f.pack(fill="x", padx=28, pady=(0, 16))

        rfid_inner = tk.Frame(self._rfid_f, bg=ACCENT_LIGHT)
        rfid_inner.pack(padx=20, pady=16)

        self._rfid_ico = tk.Label(rfid_inner, text="[RFID]",
                                   font=("Helvetica", 9, "bold"),
                                   bg=ACCENT_LIGHT, fg=ACCENT)
        self._rfid_ico.pack(side="left", padx=(0, 14))

        rfid_txt = tk.Frame(rfid_inner, bg=ACCENT_LIGHT)
        rfid_txt.pack(side="left")
        tk.Label(rfid_txt, text="Lectura de tarjeta",
                 font=FONT_LABEL, bg=ACCENT_LIGHT, fg=TEXT_DARK).pack(anchor="w")
        self._rfid_sub = tk.Label(
            rfid_txt,
            text="Haz clic aqui para simular la lectura RFID",
            font=FONT_SMALL, bg=ACCENT_LIGHT, fg=TEXT_MUTED)
        self._rfid_sub.pack(anchor="w", pady=(2, 0))

        self._uid_lbl = tk.Label(rfid_inner, textvariable=self._uid,
                                  font=FONT_MONO, bg=ACCENT_LIGHT, fg=ACCENT)
        self._uid_lbl.pack(side="right")

        for w in self._rfid_f.winfo_children() + [self._rfid_f]:
            w.bind("<Button-1>", self._simular_rfid)
        for w in rfid_inner.winfo_children() + [rfid_inner]:
            w.bind("<Button-1>", self._simular_rfid)

        # ── Nombre ───────────────────────────────────────────────────────────
        self._lbl(parent, "Nombre completo", pad)
        self.entry_nombre = tk.Entry(parent)
        apply_entry_style(self.entry_nombre)
        self.entry_nombre.pack(fill="x", ipady=7, **pad)
        tk.Frame(parent, bg=BG_LIGHT, height=14).pack()

        # ── Tipo de acceso ────────────────────────────────────────────────────
        self._lbl(parent, "Tipo de acceso", pad)
        tog = tk.Frame(parent, bg=WHITE,
                       highlightthickness=1, highlightbackground=CARD_BORDER)
        tog.pack(fill="x", **pad)
        self.btn_est = tk.Button(tog, text="Estudiante", font=FONT_H3,
                                  relief="flat", cursor="hand2",
                                  command=lambda: self._set_tipo("Estudiante"))
        self.btn_adm = tk.Button(tog, text="Administrativo", font=FONT_H3,
                                  relief="flat", cursor="hand2",
                                  command=lambda: self._set_tipo("Administrativo"))
        self.btn_vis = tk.Button(tog, text="Visitante", font=FONT_H3,
                                  relief="flat", cursor="hand2",
                                  command=lambda: self._set_tipo("Visitante"))
        self.btn_est.pack(side="left", expand=True, fill="x", ipady=10)
        tk.Frame(tog, bg=CARD_BORDER, width=1).pack(side="left", fill="y")
        self.btn_adm.pack(side="left", expand=True, fill="x", ipady=10)
        tk.Frame(tog, bg=CARD_BORDER, width=1).pack(side="left", fill="y")
        self.btn_vis.pack(side="left", expand=True, fill="x", ipady=10)
        self._update_toggle()
        tk.Frame(parent, bg=BG_LIGHT, height=14).pack()

        separator(parent, pady=0)
        tk.Frame(parent, bg=BG_LIGHT, height=14).pack()

        # ── Campos solo para estudiante ───────────────────────────────────────
        self._fm = tk.Frame(parent, bg=BG_LIGHT)
        self._lbl(self._fm, "Numero de matricula", pad)
        self.entry_matricula = tk.Entry(self._fm)
        apply_entry_style(self.entry_matricula)
        self.entry_matricula.pack(fill="x", ipady=7, **pad)
        tk.Frame(self._fm, bg=BG_LIGHT, height=14).pack()
        self._fm.pack(fill="x")

        self._fp = tk.Frame(parent, bg=BG_LIGHT)
        self._lbl(self._fp, "Programa academico", pad)
        self.var_prog = tk.StringVar(value=PROGRAMAS[0])
        om = tk.OptionMenu(self._fp, self.var_prog, *PROGRAMAS)
        om.configure(font=FONT_BODY, bg=WHITE, fg=TEXT_DARK,
                     activebackground=ACCENT_LIGHT, relief="flat",
                     highlightthickness=1, highlightbackground=CARD_BORDER,
                     anchor="w")
        om["menu"].configure(font=FONT_BODY, bg=WHITE,
                              activebackground=ACCENT_LIGHT)
        om.pack(fill="x", ipady=4, **pad)
        tk.Frame(self._fp, bg=BG_LIGHT, height=14).pack()
        self._fp.pack(fill="x")

        self._fmod = tk.Frame(parent, bg=BG_LIGHT)
        self._lbl(self._fmod, "Modalidad", pad)
        self.var_mod = tk.StringVar(value=MODALIDADES[0])
        om2 = tk.OptionMenu(self._fmod, self.var_mod, *MODALIDADES)
        om2.configure(font=FONT_BODY, bg=WHITE, fg=TEXT_DARK,
                      activebackground=ACCENT_LIGHT, relief="flat",
                      highlightthickness=1, highlightbackground=CARD_BORDER,
                      anchor="w")
        om2["menu"].configure(font=FONT_BODY, bg=WHITE,
                               activebackground=ACCENT_LIGHT)
        om2.pack(fill="x", ipady=4, **pad)
        tk.Frame(self._fmod, bg=BG_LIGHT, height=14).pack()
        self._fmod.pack(fill="x")

        separator(parent, pady=0)

        # ── Campos solo para Administrativo ──────────────────────────────────
        self._fadm = tk.Frame(parent, bg=BG_LIGHT)
        self._lbl(self._fadm, "Departamento al que pertenece", pad)
        self.var_depto = tk.StringVar(value=DEPARTAMENTOS[0])
        om_depto = tk.OptionMenu(self._fadm, self.var_depto, *DEPARTAMENTOS)
        om_depto.configure(font=FONT_BODY, bg=WHITE, fg=TEXT_DARK,
                           activebackground=ACCENT_LIGHT, relief="flat",
                           highlightthickness=1, highlightbackground=CARD_BORDER,
                           anchor="w")
        om_depto["menu"].configure(font=FONT_BODY, bg=WHITE,
                                    activebackground=ACCENT_LIGHT)
        om_depto.pack(fill="x", ipady=4, **pad)
        tk.Frame(self._fadm, bg=BG_LIGHT, height=14).pack()
        separator(parent, pady=0)

        # ── Campos solo para Visitante ────────────────────────────────────────
        self._fvis = tk.Frame(parent, bg=BG_LIGHT)
        self._lbl(self._fvis, "Motivo de visita", pad)
        self.var_motivo = tk.StringVar(value=MOTIVOS_VISITA[0])
        om_motivo = tk.OptionMenu(self._fvis, self.var_motivo, *MOTIVOS_VISITA)
        om_motivo.configure(font=FONT_BODY, bg=WHITE, fg=TEXT_DARK,
                            activebackground=ACCENT_LIGHT, relief="flat",
                            highlightthickness=1, highlightbackground=CARD_BORDER,
                            anchor="w")
        om_motivo["menu"].configure(font=FONT_BODY, bg=WHITE,
                                     activebackground=ACCENT_LIGHT)
        om_motivo.pack(fill="x", ipady=4, **pad)
        tk.Frame(self._fvis, bg=BG_LIGHT, height=14).pack()
        separator(parent, pady=0)

        # ── Resumen de fecha/hora que se guardara ────────────────────────────
        resumen_f = tk.Frame(parent, bg=WHITE,
                              highlightthickness=1, highlightbackground=CARD_BORDER)
        resumen_f.pack(fill="x", padx=28, pady=16)

        tk.Label(resumen_f, text="Datos que se registraran",
                 font=FONT_LABEL, bg=WHITE, fg=TEXT_MID).pack(
                     anchor="w", padx=16, pady=(12, 4))

        campos_f = tk.Frame(resumen_f, bg=WHITE)
        campos_f.pack(fill="x", padx=16, pady=(0, 12))

        # Fecha
        col1 = tk.Frame(campos_f, bg=WHITE)
        col1.pack(side="left", expand=True, fill="x")
        tk.Label(col1, text="FECHA", font=("Helvetica", 8),
                 bg=WHITE, fg=TEXT_MUTED).pack(anchor="w")
        self.lbl_fecha_reg = tk.Label(col1, text="",
                                       font=("Helvetica", 11, "bold"),
                                       bg=WHITE, fg=TEXT_DARK)
        self.lbl_fecha_reg.pack(anchor="w")

        tk.Frame(campos_f, bg=CARD_BORDER, width=1).pack(
            side="left", fill="y", padx=12)

        # Hora
        col2 = tk.Frame(campos_f, bg=WHITE)
        col2.pack(side="left", expand=True, fill="x")
        tk.Label(col2, text="HORA", font=("Helvetica", 8),
                 bg=WHITE, fg=TEXT_MUTED).pack(anchor="w")
        self.lbl_hora_reg = tk.Label(col2, text="",
                                      font=("Helvetica", 11, "bold"),
                                      bg=WHITE, fg=TEXT_DARK)
        self.lbl_hora_reg.pack(anchor="w")

        tk.Frame(campos_f, bg=CARD_BORDER, width=1).pack(
            side="left", fill="y", padx=12)

        # Dia de la semana
        col3 = tk.Frame(campos_f, bg=WHITE)
        col3.pack(side="left", expand=True, fill="x")
        tk.Label(col3, text="DIA", font=("Helvetica", 8),
                 bg=WHITE, fg=TEXT_MUTED).pack(anchor="w")
        self.lbl_dia_reg = tk.Label(col3, text="",
                                     font=("Helvetica", 11, "bold"),
                                     bg=WHITE, fg=TEXT_DARK)
        self.lbl_dia_reg.pack(anchor="w")

        # ── Boton de registro ────────────────────────────────────────────────
        make_button(parent, "Registrar entrada", self._registrar).pack(
            fill="x", padx=28, ipady=4)

        self.lbl_msg = tk.Label(parent, text="", font=FONT_BODY,
                                 bg=BG_LIGHT, wraplength=500)
        self.lbl_msg.pack(pady=(10, 0), padx=28, anchor="w")

        tk.Frame(parent, bg=BG_LIGHT, height=30).pack()

    # ─────────────────────────────────────────────────────────────────────────
    # Reloj
    # ─────────────────────────────────────────────────────────────────────────

    def _iniciar_reloj(self):
        self._actualizar_reloj()

    def _actualizar_reloj(self):
        ahora = datetime.now()
        dias = {
            "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miercoles",
            "Thursday": "Jueves", "Friday": "Viernes",
            "Saturday": "Sabado", "Sunday": "Domingo",
        }
        meses = {
            1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
            5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
            9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre",
        }
        dia_semana = dias.get(ahora.strftime("%A"), ahora.strftime("%A"))
        mes_texto  = meses.get(ahora.month, str(ahora.month))

        hora_str  = ahora.strftime("%H:%M:%S")
        fecha_str = f"{dia_semana} {ahora.day} de {mes_texto} de {ahora.year}"
        fecha_reg = ahora.strftime("%d/%m/%Y")
        hora_reg  = ahora.strftime("%H:%M:%S")

        self.lbl_hora.configure(text=hora_str)
        self.lbl_fecha.configure(text=fecha_str)
        self.lbl_fecha_reg.configure(text=fecha_reg)
        self.lbl_hora_reg.configure(text=hora_reg)
        self.lbl_dia_reg.configure(text=dia_semana)

        self._reloj_id = self.after(1000, self._actualizar_reloj)

    # ─────────────────────────────────────────────────────────────────────────
    # Helpers de UI
    # ─────────────────────────────────────────────────────────────────────────

    def _lbl(self, parent, text, pack_kw=None):
        kw = {k: v for k, v in (pack_kw or {}).items() if k != "pady"}
        tk.Label(parent, text=text.upper(), font=("Helvetica", 9, "bold"),
                 bg=parent.cget("bg"), fg=TEXT_MUTED, anchor="w").pack(
                     fill="x", pady=(0, 4), **kw)

    def _set_tipo(self, tipo):
        self._tipo.set(tipo)
        self._update_toggle()
        self._toggle_campos()

    def _update_toggle(self):
        tipo = self._tipo.get()
        active   = dict(bg=ACCENT,    fg=WHITE,    activebackground="#155f55")
        inactive = dict(bg=WHITE,     fg=TEXT_MID, activebackground=ACCENT_LIGHT)
        self.btn_est.configure(**(active if tipo == "Estudiante"     else inactive))
        self.btn_adm.configure(**(active if tipo == "Administrativo" else inactive))
        self.btn_vis.configure(**(active if tipo == "Visitante"      else inactive))

    def _toggle_campos(self):
        tipo = self._tipo.get()

        # Mostrar/ocultar panel RFID segun tipo
        if tipo == "Estudiante":
            self._rfid_f.pack(fill="x", padx=28, pady=(0, 16))
        else:
            self._rfid_f.pack_forget()
            self._uid.set("")
            self._badge_f.configure(bg="#f4f5f7", highlightbackground=CARD_BORDER)
            self._badge_lbl.configure(text="Sin tarjeta", fg=TEXT_MUTED, bg="#f4f5f7")

        # Campos estudiante
        if tipo == "Estudiante":
            self._fm.pack(fill="x")
            self._fp.pack(fill="x")
            self._fmod.pack(fill="x")
        else:
            self._fm.pack_forget()
            self._fp.pack_forget()
            self._fmod.pack_forget()

        # Campos administrativo
        if tipo == "Administrativo":
            self._fadm.pack(fill="x")
        else:
            self._fadm.pack_forget()

        # Campos visitante
        if tipo == "Visitante":
            self._fvis.pack(fill="x")
        else:
            self._fvis.pack_forget()

    def _simular_rfid(self, _=None):
        """
        Simulacion de lectura RFID.
        En produccion: reemplaza con lectura real del puerto serial.

            import serial
            ser = serial.Serial('COM3', 9600)
            uid = ser.readline().decode().strip()
        """
        uid = "UID-" + "".join(
            random.choices(string.ascii_uppercase + string.digits, k=8))
        self._uid.set(uid)

        self._rfid_f.configure(bg="#e8f7f5", highlightbackground="#6abfb5")
        self._rfid_ico.configure(bg="#e8f7f5", fg=ACCENT)
        self._rfid_sub.configure(
            text=f"Tarjeta leida correctamente — {uid}",
            fg=SUCCESS, bg="#e8f7f5")
        for w in self._rfid_f.winfo_children():
            try:
                w.configure(bg="#e8f7f5")
            except Exception:
                pass

        self._badge_f.configure(bg="#e8f7f5", highlightbackground="#6abfb5")
        self._badge_lbl.configure(text="Tarjeta detectada", fg=SUCCESS, bg="#e8f7f5")

    # ─────────────────────────────────────────────────────────────────────────
    # Registro
    # ─────────────────────────────────────────────────────────────────────────

    def _registrar(self):
        nombre = self.entry_nombre.get().strip()
        uid    = self._uid.get().strip()
        tipo   = self._tipo.get()

        if not nombre:
            self._msg("El nombre es obligatorio.", error=True)
            return

        # Solo Estudiante requiere RFID
        if tipo == "Estudiante" and not uid:
            self._msg("Primero debes leer la tarjeta RFID.", error=True)
            return

        ahora    = datetime.now()
        fecha_db = ahora.strftime("%Y-%m-%d")
        hora_db  = ahora.strftime("%H:%M:%S")

        matricula = programa = modalidad = departamento = motivo = None

        if tipo == "Estudiante":
            matricula = self.entry_matricula.get().strip()
            programa  = self.var_prog.get()
            modalidad = self.var_mod.get()
            if not matricula:
                self._msg("La matricula es obligatoria.", error=True)
                return

        elif tipo == "Administrativo":
            departamento = self.var_depto.get()
            uid = "ADM-" + nombre[:4].upper().replace(" ", "")

        elif tipo == "Visitante":
            motivo = self.var_motivo.get()
            uid = "VIS-" + nombre[:4].upper().replace(" ", "")

        try:
            db.registrar_acceso(
                uid, nombre, tipo,
                fecha_db, hora_db,
                matricula, programa, modalidad,
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self._msg(
            f"Entrada registrada — {nombre} ({tipo}) a las {hora_db}",
            error=False,
        )
        self._limpiar()

    def _limpiar(self):
        self.entry_nombre.delete(0, "end")
        self._uid.set("")
        self.entry_matricula.delete(0, "end")
        self.var_depto.set(DEPARTAMENTOS[0])
        self.var_motivo.set(MOTIVOS_VISITA[0])

        # Restaurar zona RFID
        self._rfid_f.configure(bg=ACCENT_LIGHT, highlightbackground="#a8d5cf")
        self._rfid_ico.configure(bg=ACCENT_LIGHT, fg=ACCENT)
        self._rfid_sub.configure(
            text="Haz clic aqui para simular la lectura RFID",
            fg=TEXT_MUTED, bg=ACCENT_LIGHT)

        # Restaurar badge
        self._badge_f.configure(bg="#f4f5f7", highlightbackground=CARD_BORDER)
        self._badge_lbl.configure(text="Sin tarjeta", fg=TEXT_MUTED, bg="#f4f5f7")

    def _msg(self, texto, error=True):
        color = DANGER if error else SUCCESS
        self.lbl_msg.configure(text=texto, fg=color, bg=BG_LIGHT)
        self.after(5000, lambda: self.lbl_msg.configure(text=""))