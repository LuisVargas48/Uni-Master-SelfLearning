from flask import Flask, request, make_response
import os
import pickle
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>CTF Lab: Nivel 1</h1><p>Busca los endpoints /ping y /profile</p>"

# Vulnerabilidad 1: Command Injection
@app.route('/ping')
def ping():
    target = request.args.get('ip')
    if target:
        # ¡Peligro! Uso directo de entrada del usuario en el sistema
        command = f"ping -c 1 {target}"
        output = os.popen(command).read()
        return f"<pre>{output}</pre>"
    return "Uso: /ping?ip=8.8.8.8"

# Vulnerabilidad 2: Insecure Deserialization (Pickle)
@app.route('/profile')
def profile():
    cookie = request.cookies.get('session')
    if not cookie:
        # Crear una sesión inicial "segura"
        user_data = {'name': 'Invitado', 'role': 'user'}
        pickled_data = base64.b64encode(pickle.dumps(user_data)).decode()
        resp = make_response("Perfil creado. Revisa tus cookies.")
        resp.set_cookie('session', pickled_data)
        return resp
    
    # ¡Peligro! Deserialización sin validar
    data = pickle.loads(base64.b64decode(cookie))
    return f"Hola, {data.get('name')}. Tu rol es: {data.get('role')}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)