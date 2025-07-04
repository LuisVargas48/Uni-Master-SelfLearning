import string

# Definimos el conjunto de caracteres base
lowercase = string.ascii_lowercase
uppercase = string.ascii_uppercase
digits = string.digits
specials = "!@#$%^&*"

# Parámetros
min_length = 4
max_length = 6
include_upper = True
include_digits = True
include_specials = True

# Generar el alfabeto permitido
alphabet = lowercase
if include_upper:
    alphabet += uppercase
if include_digits:
    alphabet += digits
if include_specials:
    alphabet += specials

# Restricciones específicas (para poda)
def is_valid(password):
    if len(password) < min_length:
        return False
    if include_upper and not any(c in uppercase for c in password):
        return False
    if include_digits and not any(c in digits for c in password):
        return False
    if include_specials and not any(c in specials for c in password):
        return False
    return True

# Backtracking
def generate_passwords(current_password):
    if len(current_password) > max_length:
        return
    if is_valid(current_password):
        print("Contraseña válida:", current_password)
    
    for char in alphabet:
        generate_passwords(current_password + char)

# Ejecutar
print("Generando contraseñas...")
generate_passwords("")
