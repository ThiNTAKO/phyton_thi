word_to_guess = "banane"
user_word = ["_"] * len(word_to_guess)
errors = 10
guessed_letters = []

while errors > 0 and "_" in user_word:
    input_letter = input("Enter a letter: ").lower()
    
    if input_letter in guessed_letters:
        print("You have already guessed that letter. Try again.")
        continue
    
    guessed_letters.append(input_letter)
    
    # Vérifier si la lettre est correcte
    if input_letter in word_to_guess:
        # Vérifier si la lettre a été devinée plus de fois que nécessaire
        if user_word.count(input_letter) >= word_to_guess.count(input_letter):
            errors -= 1
            print(f"You have guessed the letter '{input_letter}' more than necessary. You lose one life.")
        else:
            for i in range(len(word_to_guess)):
                if word_to_guess[i] == input_letter:
                    user_word[i] = input_letter
    else:
        errors -= 1
    
    print(f"Current word: {' '.join(user_word)}. You have {errors} lives left.")

if "_" not in user_word:
    print("You won!")
else:
    print("You lose.")

