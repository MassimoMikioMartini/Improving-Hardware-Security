import networkx as nx

def parse(netlist):
    inputs = set()
    outputs = set()
    gates = []
    temp = []
    keywords = ["AND", "NAND", "OR", "NOR", "NOT", "XNOR", "XOR", "BUF"]
    
    with open(netlist) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("INPUT"):
                inputs.add(line.split('(')[1].split(')')[0])
            elif line.startswith("OUTPUT"):
                outputs.add(line.split('(')[1].split(')')[0])
            elif any(line.split()[2].startswith(kw) for kw in keywords):
                parts = line.split('=')
                if len(parts) == 2:
                    gate_name = parts[0].strip()
                    if parts[1][:4] == " NOT":
                        continue
                    elif parts[1][:4] == " BUF":
                        continue
                    elif parts[1][:4] == " AND":
                        gate_inputs = parts[1][5:-1].split(",")
                        gate_inputs[1] = gate_inputs[1].strip(" ")
                        gate_type = "and"
                    elif parts[1][:4] == " NAN":
                        gate_inputs = parts[1][6:-1].split(",")
                        gate_inputs[1] = gate_inputs[1].strip(" ")
                        gate_type = "nand"
                    elif parts[1][:4] == " OR(":
                        gate_inputs = parts[1][4:-1].split(",")
                        gate_inputs[1] = gate_inputs[1].strip(" ")
                        gate_type = "or"
                    elif parts[1][:4] == " NOR":
                        gate_inputs = parts[1][5:-1].split(",")
                        gate_inputs[1] = gate_inputs[1].strip(" ")
                        gate_type = "nor"
                    elif parts[1][:4] == " XNO":
                        gate_inputs = parts[1][6:-1].split(",")
                        gate_inputs[1] = gate_inputs[1].strip(" ")
                        gate_type = "xnor"
                    elif parts[1][:4] == " XOR":
                        gate_inputs = parts[1][5:-1].split(",")
                        gate_inputs[1] = gate_inputs[1].strip(" ")
                        gate_type = "xor"
                    
                    # Only include gates with exactly 2 inputs
                    if len(gate_inputs) == 2:
                        gates.append((gate_type, gate_name, gate_inputs))
                    else:
                        continue
    
    return inputs, outputs, gates

def build_graph(inputs, outputs, gates):
    G = nx.DiGraph()

    # Add primary inputs and outputs
    for pi in inputs:
        G.add_node(pi, type="PI")
    for po in outputs:
        G.add_node(po, type="PO")

    # Add gates and connections
    for gate_type, gate_name, gate_inputs in gates:
        G.add_node(gate_name, type=gate_type)
        for input_wire in gate_inputs:
            G.add_edge(input_wire, gate_name)
    
    return G

def compute_weights(G, primary_outputs):
    weights = {}
    po_paths = {po: set(nx.ancestors(G, po)) for po in primary_outputs}
    for node in G.nodes():
        node_type = G.nodes[node].get('type')
        if node_type not in ['PI', 'PO']:  # Skip I/Os
            weights[node] = sum(1 for po in primary_outputs if node in po_paths[po])
    return weights

def estimate_stability(G, node, primary_outputs):
    gate_type = G.nodes[node].get('type')
    try:
        depth = nx.shortest_path_length(G, node, next(iter(primary_outputs)))
    except (nx.NetworkXNoPath, StopIteration):
        return 0.0
        
    if gate_type in ['and', 'or', 'nand', 'nor', 'buf']:
        stability = 0.7
    elif gate_type in ['xor', 'xnor']:
        stability = 0.3
    elif gate_type == 'not':
        stability = 0.5
    else:
        stability = 0.5
    return stability * (1 / (1 + 0.1 * depth))

def select_gates(netlist_file, n=45):
    inputs, outputs, gates = parse(netlist_file)
    G = build_graph(inputs, outputs, gates)
    
    # Create a set of gate names from the parsed gates for quick lookup
    gate_names = {gate[1] for gate in gates}
    
    weights = compute_weights(G, outputs)
    stabilities = {
        node: estimate_stability(G, node, outputs)
        for node in G.nodes()
        if G.nodes[node].get('type') not in ['PI', 'PO']  # Exclude primary I/Os
        and node in gate_names  # Only include gates from the parsed list
    }
    
    # Filter out output nodes and gates with wrong number of inputs
    candidate_nodes = [
        node for node in stabilities.keys()
        if node not in outputs 
        and G.nodes[node].get('type') != 'not'
        and node in gate_names  # Ensure it's in our gates list
    ]
    
    ranked = sorted(
        [(node, stabilities[node], weights[node]) for node in candidate_nodes],
        key=lambda x: (-x[1], -x[2])  # Sort by stability (desc), then weight (desc)
    )
    
    return [gate[0] for gate in ranked[:n]]