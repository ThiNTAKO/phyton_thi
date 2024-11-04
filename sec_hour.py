def convert_seconds(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# Demande à l'utilisateur d'entrer les secondes
total_seconds = int(input("Entrez le nombre de secondes à convertir : "))
formatted_time = convert_seconds(total_seconds)
print(f"Le temps formaté est : {formatted_time}")
