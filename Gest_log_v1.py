import os
import re
import csv
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
import PyPDF2

# Extraction des logs
def extract_wsc(line):
    regex = r'(\d+\.\d+\.\d+\.\d+) - (\S+) \[(.+?)\] "(.*?)" (\d+) (\d+)'
    match = re.match(regex, line)
    return match.groups() if match else None

def extract_nca(line):
    regex = r'(\d+-\d+-\d+ \d+:\d+:\d+),(\d+\.\d+\.\d+\.\d+),(\w+),(\w+),(\w+),(.*)'
    match = re.match(regex, line)
    return match.groups() if match else None

def extract_iis(line):
    regex = r'(\d+-\d+-\d+) (\d+:\d+:\d+) (\w+) (.+?) (\d+) (\d+) (.+)'
    match = re.match(regex, line)
    return match.groups() if match else None

def detect_log_format(line):
    if re.match(r'^\d+\.\d+\.\d+\.\d+ - ', line):
        return 'WSC'
    elif re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},', line):
        return 'NCA'
    elif re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d+', line):
        return 'IIS'
    return None

# Analyse des logs
def process_logs(log_file):
    extracted_data = []
    unmatched_lines = []
    try:
        with open(log_file, 'r') as file:
            for line in file:
                log_format = detect_log_format(line)
                if log_format == 'WSC':
                    data = extract_wsc(line)
                elif log_format == 'NCA':
                    data = extract_nca(line)
                elif log_format == 'IIS':
                    data = extract_iis(line)
                else:
                    unmatched_lines.append(line)
                    continue

                if data:
                    extracted_data.append((log_format,) + data)
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la lecture du fichier : {e}")
    return extracted_data, unmatched_lines

# Détection des vulnérabilités
def detect_vulnerabilities(data):
    vulnerabilities = []
    for entry in data:
        log_format = entry[0]
        details = entry[1:]
        if log_format == 'WSC':
            ip, user, timestamp, request, status_code, size = details
            if "../" in request or ";" in request:
                vulnerabilities.append(f"[WSC] {ip} - Commande malveillante détectée")
        elif log_format == 'NCA':
            date_time, ip, action, status, username, extra = details
            if action == 'login' and status == 'failed':
                vulnerabilities.append(f"[NCA] {ip} - Échec de connexion pour l'utilisateur {username}")
        elif log_format == 'IIS':
            date, time, method, uri, status_code, size, user_agent = details
            if "wget" in user_agent or "curl" in user_agent:
                vulnerabilities.append(f"[IIS] Agent utilisateur suspect détecté : {user_agent}")
    return vulnerabilities

# Calcul des pourcentages pour les graphes
def calculate_percentages(data):
    total_lines = len(data)
    if total_lines == 0:
        return 0, 0

    vulnerable_count = sum(1 for entry in data if detect_vulnerabilities([entry]))
    success_percentage = ((total_lines - vulnerable_count) / total_lines) * 100
    vulnerable_percentage = (vulnerable_count / total_lines) * 100

    return success_percentage, vulnerable_percentage

# Sauvegarde des résultats en CSV
def save_to_csv(data, output_file):
    headers = ['Log Format', 'Champ 1', 'Champ 2', 'Champ 3', 'Champ 4', 'Champ 5', 'Champ 6', 'Champ 7']
    try:
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'enregistrement du fichier CSV : {e}")

# Génération du rapport PDF
def generate_pdf_report(data, filename):
    try:
        doc = SimpleDocTemplate(filename, pagesize=A4)
        elements = []
        title = [["Rapport des vulnérabilités détectées"]]
        table_data = title + [["Log Format", "Détails"]] + [
            [entry[0], Paragraph(" | ".join(map(str, entry[1:])), getSampleStyleSheet()['BodyText'])] for entry in data
        ]

        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        doc.build(elements)
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la génération du PDF : {e}")

# Génération d'un graphique et conversion en PDF
def generate_graph(data):
    success, vulnerable = calculate_percentages(data)
    labels = ['Connexions réussies', 'Connexions vulnérables']
    sizes = [success, vulnerable]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#4CAF50', '#FF5733'])
    ax.axis('equal')
    plt.savefig("Graph.png")
    plt.show()

def convert_image_to_pdf(image_path, pdf_path):
    try:
        canvas_obj = canvas.Canvas(pdf_path, pagesize=letter)
        canvas_obj.drawImage(image_path, 0, 0, width=letter[0], height=letter[1], preserveAspectRatio=True)
        canvas_obj.showPage()
        canvas_obj.save()
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la conversion de l'image en PDF : {e}")

# Fusion des rapports
def merge_pdfs(input_pdfs, output_pdf):
    merger = PyPDF2.PdfMerger()
    try:
        for pdf in input_pdfs:
            merger.append(pdf)
        with open(output_pdf, 'wb') as merged_pdf:
            merger.write(merged_pdf)
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la fusion des PDF : {e}")

# Interface utilisateur
def browse_log_file():
    file_path = filedialog.askopenfilename(title="Sélectionner un fichier de log")
    log_file_entry.delete(0, tk.END)
    log_file_entry.insert(0, file_path)

def browse_output_file():
    file_path = filedialog.asksaveasfilename(title="Enregistrer le fichier CSV", defaultextension=".csv")
    output_file_entry.delete(0, tk.END)
    output_file_entry.insert(0, file_path)

def analyze_logs():
    log_file = log_file_entry.get()
    output_file = output_file_entry.get()
    if not log_file or not output_file:
        messagebox.showwarning("Attention", "Veuillez sélectionner un fichier de log et un fichier de sortie.")
        return

    data, unmatched_lines = process_logs(log_file)
    if data:
        save_to_csv(data, output_file)
        vulnerabilities = detect_vulnerabilities(data)
        generate_pdf_report(data, "rapport.pdf")
        generate_graph(data)
        convert_image_to_pdf("Graph.png", "graph.pdf")
        merge_pdfs(["rapport.pdf", "graph.pdf"], "rapport_complet.pdf")
        messagebox.showinfo("Succès", "Rapport généré avec succès : rapport_complet.pdf")

root = tk.Tk()
root.title("Analyseur de Logs")
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Fichier de log :").grid(row=0, column=0, padx=5, pady=5)
log_file_entry = tk.Entry(frame, width=50)
log_file_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame, text="Parcourir", command=browse_log_file).grid(row=0, column=2, padx=5, pady=5)

tk.Label(frame, text="Fichier de sortie CSV :").grid(row=1, column=0, padx=5, pady=5)
output_file_entry = tk.Entry(frame, width=50)
output_file_entry.grid(row=1, column=1, padx=5, pady=5)
tk.Button(frame, text="Parcourir", command=browse_output_file).grid(row=1, column=2, padx=5, pady=5)

tk.Button(frame, text="Analyser", command=analyze_logs).grid(row=2, column=0, columnspan=3, pady=10)

vulnerabilities_text = ScrolledText(root, height=15, width=70)
vulnerabilities_text.pack(pady=10)

root.mainloop()
