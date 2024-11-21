def generate_secure_password(length):
    if length < 4:
        raise ValueError("Password length must be at least 4 characters")

    # Assurer au moins un de chaque type de caractère
    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]

    # Compléter le mot de passe avec des caractères aléatoires
    if length > 4:
        all_characters = string.ascii_letters + string.digits + string.punctuation
        password += [random.choice(all_characters) for _ in range(length - 4)]
    
    # Mélanger les caractères pour plus de sécurité
    random.shuffle(password)
    return ''.join(password)

# Demander à l'utilisateur la longueur du mot de passe
length = int(input("Enter the length of the password: "))

# Générer et afficher le mot de passe sécurisé
password = generate_secure_password(length)
print(f"Generated secure password: {password}")
