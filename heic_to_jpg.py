#!/usr/bin/env python3
import os
from tkinter import Tk, Label, Button, filedialog, StringVar, ttk
from PIL import Image
import pyheif

# Funktion zur Prüfung und Konvertierung
def check_and_convert(folder):
    if not folder:
        status_label.set("Bitte wählen Sie einen Ordner aus!")
        return

    heic_files = [f for f in os.listdir(folder) if f.lower().endswith('.heic')]
    total_files = len(heic_files)

    if total_files == 0:
        status_label.set("Keine HEIC-Dateien gefunden!")
        return

    # Dateien filtern, die noch nicht konvertiert wurden
    files_to_convert = [
        f for f in heic_files
        if not os.path.exists(os.path.join(folder, f"{os.path.splitext(f)[0]}.jpg"))
    ]
    total_to_convert = len(files_to_convert)

    if total_to_convert == 0:
        status_label.set("Alle Dateien wurden bereits konvertiert.")
        return

    # Fortschrittsbalken konfigurieren
    progress["maximum"] = total_to_convert
    progress["value"] = 0
    files_count_label.set(f"Zu konvertieren: {total_to_convert}/{total_files} HEIC-Dateien")

    # Konvertierung starten
    for index, filename in enumerate(files_to_convert):
        filepath = os.path.join(folder, filename)
        heif_file = pyheif.read(filepath)
        image = Image.frombytes(
            heif_file.mode, heif_file.size, heif_file.data, "raw", heif_file.mode, heif_file.stride
        )
        output_path = os.path.join(folder, f"{os.path.splitext(filename)[0]}.jpg")
        image.save(output_path, "JPEG")

        # Fortschritt aktualisieren
        progress["value"] = index + 1
        status_label.set(f"Konvertiere: {filename} ({index + 1}/{total_to_convert})")
        app.update_idletasks()

    status_label.set("Konvertierung abgeschlossen!")
    files_count_label.set(f"Zu konvertieren: 0/{total_files} HEIC-Dateien")

# Funktion zum Ordner auswählen
def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_path.set(folder)
        status_label.set("Ordner ausgewählt.")
        update_file_count(folder)

# Funktion zum Aktualisieren der Dateianzahl
def update_file_count(folder):
    heic_files = [f for f in os.listdir(folder) if f.lower().endswith('.heic')]
    total_files = len(heic_files)
    files_to_convert = [
        f for f in heic_files
        if not os.path.exists(os.path.join(folder, f"{os.path.splitext(f)[0]}.jpg"))
    ]
    total_to_convert = len(files_to_convert)
    files_count_label.set(f"Zu konvertieren: {total_to_convert}/{total_files} HEIC-Dateien")

# GUI erstellen
app = Tk()
app.title("HEIC zu JPG Konverter")

# Variablen
folder_path = StringVar()
status_label = StringVar()
status_label.set("Bitte wählen Sie einen Ordner aus.")
files_count_label = StringVar()
files_count_label.set("Zu konvertieren: 0 HEIC-Dateien")

# GUI-Elemente
Label(app, text="HEIC zu JPG Konverter", font=("Arial", 16)).pack(pady=10)
Label(app, text="Ordner:").pack(pady=5)
Label(app, textvariable=folder_path).pack(pady=5)
Button(app, text="Ordner auswählen", command=select_folder).pack(pady=5)
Button(app, text="Konvertieren", command=lambda: check_and_convert(folder_path.get())).pack(pady=10)

# Fortschrittsanzeige und Status
progress = ttk.Progressbar(app, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=10)
Label(app, textvariable=status_label, fg="green").pack(pady=5)
Label(app, textvariable=files_count_label).pack(pady=5)

# Beenden-Button
Button(app, text="Beenden", command=app.quit).pack(pady=10)

app.mainloop()