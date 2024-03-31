from flask import Flask, render_template, request, redirect, url_for
import json
import pandas as pd
import networkx as nx

app = Flask(__name__, static_url_path='/static')
G1 = None

def analyze_graph(file_path):
    df = pd.read_csv(file_path)
    nodes = df.columns[1:]
    edges = [(row['Unnamed: 0'], node) for _, row in df.iterrows() for node in nodes if row[node] > 0]
    global G1
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    G1 = G
    undirected_G = G.to_undirected()
    is_connected = nx.is_connected(undirected_G)
    nodes_data = [{'id': node} for node in G.nodes()]
    links_data = [{'source': edge[0], 'target': edge[1]} for edge in G.edges()]
    graph_data = {'nodes': nodes_data, 'links': links_data}
    print(graph_data)
    is_dag = nx.is_directed_acyclic_graph(G)
    print(is_dag)
    is_tree = is_dag and all(len(list(G.predecessors(node))) == 1 for node in nodes if node != nodes[0])
    graph_type = "general graph"
    if is_dag:
        if is_tree:
            graph_type = "tree"
        else:
            graph_type = "DAG"
    elif is_connected:
        graph_type = "general graph"
    return is_connected, graph_type

@app.route("/", methods=["GET", "POST"])
def i():
    return render_template('index2.html')

@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            is_connected, graph_type = analyze_graph(file)
            print(is_connected)
            if is_connected:
                if graph_type == "general graph":
                    print("general")
                    return render_template("general_graph_select.html")
                elif graph_type == "tree":
                    return render_template("tree_select.html")
                elif graph_type == "DAG":
                    return render_template("dag_select.html")
                else:
                    return f"The graph is {graph_type}."
            else:
                return "The graph is not connected."
    return render_template("index.html")

@app.route("/dag_select", methods=["GET", "POST"])
def dag_select():
    diagram_type = request.form.get("diagram_type")
    print(diagram_type)
    if diagram_type == "sugiyama":
        nodes_data = [{'id': node} for node in G1.nodes()]
        links_data = [{'source': edge[0], 'target': edge[1]} for edge in G1.edges()]
        graph_data = {'nodes': nodes_data, 'links': links_data}
        print(graph_data)
        return render_template("sougyama.html", graph_data=json.dumps(graph_data))
    elif diagram_type == "r_sugiyama":
        nodes_data = [{'id': node} for node in G1.nodes()]
        links_data = [{'source': edge[0], 'target': edge[1]} for edge in G1.edges()]
        graph_data = {'nodes': nodes_data, 'links': links_data}
        print(graph_data)
        return render_template("r_sugiyama.html", graph_data=json.dumps(graph_data))

@app.route("/general_graph_select", methods=["GET", "POST"])
def general_graph_select():
    diagram_type = request.form.get("diagram_type")
    print(diagram_type)
    if diagram_type == "grid":
        nodes_data = [{'id': node} for node in G1.nodes()]
        links_data = [{'source': edge[0], 'target': edge[1]} for edge in G1.edges()]
        graph_data = {'nodes': nodes_data, 'links': links_data}
        print(graph_data)
        return render_template("grid_layout.html", graph_data=json.dumps(graph_data))
    elif diagram_type == "chord":
        nodes_data = [{'id': node} for node in G1.nodes()]
        links_data = [{'source': edge[0], 'target': edge[1]} for edge in G1.edges()]
        graph_data = {'nodes': nodes_data, 'links': links_data}
        print(graph_data)
        return render_template("chord.html", graph_data=json.dumps(graph_data))

@app.route("/tree_select", methods=["GET", "POST"])
def tree_select():
    diagram_type = request.form.get("diagram_type")
    print(diagram_type)
    if diagram_type == "Rheingold Tilford Layout":
        nodes_data = [{'id': node} for node in G1.nodes()]
        links_data = [{'source': edge[0], 'target': edge[1]} for edge in G1.edges()]
        graph_data = {'nodes': nodes_data, 'links': links_data}
        print("Rheingold Tilford Layout")
        return render_template("tillford.html", graph_data=json.dumps(graph_data))
    elif diagram_type == "Icicle Tree Layout":
        nodes_data = [{'id': node} for node in G1.nodes()]
        links_data = [{'source': edge[0], 'target': edge[1]} for edge in G1.edges()]
        graph_data = {'nodes': nodes_data, 'links': links_data}
        print(graph_data)
        return render_template("icicle.html", graph_data=json.dumps(graph_data))

if __name__ == "__main__":
    app.run(debug=True)
