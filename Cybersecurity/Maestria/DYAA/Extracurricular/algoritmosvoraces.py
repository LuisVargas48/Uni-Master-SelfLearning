import random
from typing import List, Dict

# Lista de nombres posibles de amenazas
threat_names = [
    "Malware", "Phishing", "Ransomware", "DDoS", "Spyware",
    "Rootkit", "Brute Force", "SQL Injection", "Zero-Day", "Botnet",
    "Man-in-the-Middle", "Trojan", "Keylogger", "Worm", "Cryptojacking"
]

# Generar amenazas aleatorias con nombres realistas
def generate_threats(n: int) -> List[Dict]:
    selected_names = random.sample(threat_names, n)
    threats = []
    for name in selected_names:
        threat = {
            "name": name,
            "criticality": random.randint(1, 10),
            "resource_needed": random.randint(1, 5)
        }
        threats.append(threat)
    return threats

# Algoritmo voraz para asignar recursos
def greedy_resource_allocation(threats: List[Dict], total_resource: int) -> List[Dict]:
    sorted_threats = sorted(threats, key=lambda x: x["criticality"], reverse=True)
    allocation = []
    used_resource = 0

    for threat in sorted_threats:
        if used_resource + threat["resource_needed"] <= total_resource:
            allocation.append(threat)
            used_resource += threat["resource_needed"]

    return allocation

# Parámetros
num_threats = 6
total_resource = 10

# Generar amenazas aleatorias y aplicar algoritmo
threats = generate_threats(num_threats)
assigned_threats = greedy_resource_allocation(threats, total_resource)

# Mostrar amenazas generadas
print("Amenazas registradas en la BD:")
for t in threats:
    print(f"- {t['name']}: criticidad={t['criticality']}, recurso requerido={t['resource_needed']}")

# Mostrar asignación de recursos
print("\nAmenazas con recursos asignados:")
for t in assigned_threats:
    print(f"- {t['name']} (criticidad: {t['criticality']}, recurso usado: {t['resource_needed']})")

print(f"\nTotal de recursos usados: {sum(t['resource_needed'] for t in assigned_threats)} de {total_resource}")
