import re
import csv
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

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
    unmatched_lines = []  # Pour stocker les lignes non reconnues
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

        title = [["Rapport des connexions vulnérables"]]
        table_data = title + [["Log Format", "Détails"]] + [
            [entry[0], " | ".join(map(str, entry[1:]))] for entry in data
        ]

        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ]))

        elements.append(table)
        doc.build(elements)
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la génération du PDF : {e}")

# Interface Graphique
def browse_log_file():
    file_path = filedialog.askopenfilename(title="Sélectionner un fichier de log")
    if file_path:
        log_file_entry.delete(0, tk.END)
        log_file_entry.insert(0, file_path)

def browse_output_file():
    file_path = filedialog.asksaveasfilename(title="Enregistrer le fichier CSV", defaultextension=".csv")
    if file_path:
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
        vulnerabilities_text.delete(1.0, tk.END)

        if vulnerabilities:
            vulnerabilities_text.insert(tk.END, "\n".join(vulnerabilities))
            generate_pdf_report(data, "rapport_vulnerabilites.pdf")
            messagebox.showinfo("Résultat", f"Analyse terminée avec des vulnérabilités détectées. Résultat enregistré dans {output_file}.")
        else:
            vulnerabilities_text.insert(tk.END, "Aucune vulnérabilité détectée.")
            messagebox.showinfo("Résultat", f"Analyse terminée. Résultat enregistré dans {output_file}.")
        
        # Diagramme circulaire
        success, vulnerable = calculate_percentages(data)
        labels = 'Connexions réussies', 'Connexions vulnérables'
        sizes = [success, vulnerable]
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#4CAF50', '#FF5733'])
        ax.axis('equal')  # Cercle parfait
        plt.show()
    else:
        messagebox.showwarning("Attention", "Aucune donnée valide trouvée dans le fichier.")

def save_to_csv(data, output_file):
    headers = ['Log Format', 'Field 1', 'Field 2', 'Field 3', 'Field 4', 'Field 5', 'Field 6', 'Field 7']
    try:
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'enregistrement du fichier CSV : {e}")

# Configuration Tkinter
root = tk.Tk()
root.title("Analyseur de Logs @ThiNTA")

# Widgets
tk.Label(root, text="Fichier de Log TXT ou CSV :").grid(row=0, column=0, padx=5, pady=5, sticky="e")
log_file_entry = tk.Entry(root, width=50)
log_file_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Parcourir", command=browse_log_file).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="Fichier de Sortie (CSV) :").grid(row=1, column=0, padx=5, pady=5, sticky="e")
output_file_entry = tk.Entry(root, width=50)
output_file_entry.grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Parcourir", command=browse_output_file).grid(row=1, column=2, padx=5, pady=5)

tk.Button(root, text="Analyser", command=analyze_logs).grid(row=2, column=0, columnspan=3, pady=10)

tk.Label(root, text="Vulnérabilités Détectées :").grid(row=3, column=0, columnspan=3, pady=5)
vulnerabilities_text = ScrolledText(root, height=15, width=80)
vulnerabilities_text.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
