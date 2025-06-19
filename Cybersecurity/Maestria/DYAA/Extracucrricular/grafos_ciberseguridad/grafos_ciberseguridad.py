import networkx as nx
import matplotlib.pyplot as plt

def crear_red():
    G = nx.Graph()
    enlaces = [
        ("PC1", "Switch1"),
        ("Switch1", "Router1"),
        ("Router1", "Firewall"),
        ("Firewall", "Server"),
        ("Switch1", "PC2"),
        ("PC2", "Router1"),
        ("Router1", "Router2"),
        ("Router2", "Server"),
        ("PC1", "PC3"),
        ("PC3", "Switch2"),
        ("Switch2", "Router2")
    ]
    G.add_edges_from(enlaces)
    return G

def mostrar_topologia(G):
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8,6))
    nx.draw(G, pos, with_labels=True, node_size=800, node_color="lightblue", font_size=8)
    plt.title("Topología de la red simulada")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

def mostrar_rutas(G, origen, destino):
    print(f"\n🔍 Rutas desde {origen} hasta {destino}:\n")
    try:
        rutas = list(nx.all_simple_paths(G, source=origen, target=destino))
        if not rutas:
            print("❌ No se encontraron rutas.")
        for i, ruta in enumerate(rutas, 1):
            print(f"Ruta {i}: {' -> '.join(ruta)}  ({len(ruta)-1} saltos)")
    except nx.NetworkXNoPath:
        print("❌ No hay camino posible entre los nodos seleccionados.")

def main():
    red = crear_red()
    mostrar_topologia(red)

    print("💻 Nodos disponibles:", list(red.nodes))
    nodo_infectado = input("Ingrese el nodo infectado (ej. PC1): ")
    servidor_critico = input("Ingrese el servidor crítico (ej. Server): ")

    if nodo_infectado not in red or servidor_critico not in red:
        print("⚠️ Uno o ambos nodos no existen en la red.")
        return

    mostrar_rutas(red, nodo_infectado, servidor_critico)

if __name__ == "__main__":
    main()
