import re
import csv
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Fonctions d'extraction
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

def detect_vulnerabilities(data):
    vulnerabilities = []
    for entry in data:
        log_format = entry[0]
        details = entry[1:]
        if log_format == 'WSC':
            ip, user, timestamp, request, status_code, size = details
            if "../" in request or ";" in request:
                vulnerabilities.append(f"[WSC] {ip} {size} - Possible Intrusion or Command Injection")
        elif log_format == 'NCA':
            date_time, ip, action, status, username, extra = details
            if action == 'login' and status == 'failed':
                vulnerabilities.append(f"[NCA] {ip} - Failed Login Attempt for user {username}")
        elif log_format == 'IIS':
            date, time, method, uri, status_code, size, user_agent = details
            if "wget" in user_agent or "curl" in user_agent:
                vulnerabilities.append(f"[IIS] Suspicious User Agent Detected: {user_agent}")
    return vulnerabilities

def calculate_percentages(data):
    total_lines = len(data)
    if total_lines == 0:
        return 0, 0

    vulnerable_count = sum(
        1 for entry in data if detect_vulnerabilities([entry])
    )
    success_percentage = ((total_lines - vulnerable_count) / total_lines) * 100
    vulnerable_percentage = (vulnerable_count / total_lines) * 100

    return success_percentage, vulnerable_percentage

def generate_pdf_report(data, filename):
    try:
        doc = SimpleDocTemplate(filename, pagesize=A4)
        elements = []

        title = [["          Rapport de Vulnérabilités"]]
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

        table._argW[0] = 1.5 * inch
        table._argW[1] = 3.5 * inch
        elements.append(table)
        doc.build(elements)
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la génération du PDF : {e}")

def save_to_csv(data, output_file):
    headers = ['Log Format', 'Field 1', 'Field 2', 'Field 3', 'Field 4', 'Field 5', 'Field 6', 'Field 7']
    try:
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'enregistrement du fichier CSV : {e}")

def main():
    # Configuration Tkinter
    root = tk.Tk()
    root.title("Analyseur de Logs")

    # Widgets
    tk.Label(root, text="Fichier de Log TXT ou CSV :").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    log_file_entry = tk.Entry(root, width=50)
    log_file_entry.grid(row=0, column=1, padx=5, pady=5)
    tk.Button(root, text="Parcourir", command=lambda: browse_log_file(log_file_entry)).grid(row=0, column=2, padx=5, pady=5)

    tk.Label(root, text="Fichier de Sortie (CSV) :").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    output_file_entry = tk.Entry(root, width=50)
    output_file_entry.grid(row=1, column=1, padx=5, pady=5)
    tk.Button(root, text="Parcourir", command=lambda: browse_output_file(output_file_entry)).grid(row=1, column=2, padx=5, pady=5)

    tk.Button(root, text="Analyser", command=lambda: analyze_logs(log_file_entry, output_file_entry)).grid(row=2, column=0, columnspan=3, pady=10)

    tk.Label(root, text="Vulnérabilités Détectées :").grid(row=3, column=0, columnspan=3, pady=5)
    vulnerabilities_text = ScrolledText(root, height=15, width=80)
    vulnerabilities_text.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
