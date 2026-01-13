from graphlib import TopologicalSorter, CycleError
import random

def parse(netlist): # This function parses the netlist
    inputs = set()
    outputs = set()
    gates = []
    dag = dict()
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
                        gate_inputs = parts[1][5:-1].split(",")
                        gate_type = "not"
                    elif parts[1][:4] == " BUF":
                        gate_inputs = parts[1][5:-1].split(",")
                        gate_type = "buf"
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
                    
                    gates.append((gate_type, gate_name, gate_inputs, len(gate_inputs)))
    
    return inputs, outputs, gates

def topological_sort(dag, gates): # This function topologically sorts gates, ensuring the circuit is sequential
    returnlist = []
    ts = TopologicalSorter()
    
    # Add nodes and dependencies
    for node, dependencies in dag.items():
        ts.add(node, *dependencies)
    
    # Either use prepare() + get_ready()/done() style (manual iteration)
    # OR just use static_order() (automatic), but not both!
    try:
        # Option 1: Automatic (recommended for simple cases)
        order = list(ts.static_order())  # This internally calls prepare()
        for o in order:
            i = 0
            while i < len(gates):
                if o == gates[i][1]:
                    returnlist.append(gates[i])
                i += 1
        return returnlist
        
        # Option 2: Manual (if you need incremental processing)
        # ts.prepare()
        # order = []
        # while ts.is_active():
        #     ready_nodes = ts.get_ready()
        #     order.extend(ready_nodes)
        #     ts.done(*ready_nodes)
        # return order
        
    except CycleError as e:
        print(f"Graph contains a cycle: {e}")
        return None


def select_gates(netlist, t): # This function applies our algorithm for each type of logic, and returns the list of chosen gates
    inputs, outputs, gates = parse(netlist)
    total = dict()
    dag = dict()

    for g in gates: # ensures no whitespace, parenthesis, etc.
        i = 0
        while i < len(g[2]):
            g[2][i] = g[2][i].strip()
            g[2][i] = g[2][i].strip(" ")
            g[2][i] = g[2][i].strip("(")
            g[2][i] = g[2][i].strip(")")
            i += 1
        dag[g[1]] = g[2]
    sortedgates = topological_sort(dag, gates)
    
    # in form of [p0, p1]

    for i in inputs:
        total[i] = [0.5, 0.5]
    
    for g in sortedgates:
        p0 = 1
        p1 = 1

        if g[0] == "buf": # forwards probabilities
            total[g[1]] = total[g[2][0].strip("(")]   
        elif g[0] == "not": # inverts probabilities
            p0 = (total[g[2][0]])[1]
            p1 = (total[g[2][0]])[0]
            total[g[1]] = [p0, p1]
        elif g[0] == "and":
            p1 = 1
            for andgate in g[2]: # multiplies P(1)'s of each input
                p1 *= (total[andgate])[1]
            p0 = 1 - p1
            total[g[1]] = [p0, p1]
        elif g[0] == "nand":
            p1 = 1
            for andgate in g[2]: # multiplies P(1)'s of each input and inverts probabilities
                p1 *= (total[andgate])[1]
            p0 = 1 - p1
            total[g[1]] = [p1, p0]
        elif g[0] == "or":
            p0 = 1
            for andgate in g[2]: # multiplies P(0)'s of each input
                p0 *= (total[andgate])[0]
            p1 = 1 - p0
            total[g[1]] = [p0, p1]
        elif g[0] == "nor":
            p0 = 1
            for andgate in g[2]: # multiplies P(0)'s of each input and inverts probabiliites
                p0 *= (total[andgate])[0]
            p1 = 1 - p0
            total[g[1]] = [p1, p0]
        elif g[0] == "xor":
            temp = 1
            p1 = 0
            i = 0
            while i < 2 ** g[3]:
                if bin(i).count("1") % 2 == 1: # odd number of 1's
                    string = bin(i)[2:]
                    temp = 1
                    if len(string) == g[3]:
                        j = 0
                        while j < g[3]:
                            if string[j] == "0":
                                temp *= (total[g[2][j]])[0] # multiply by P(0)
                            elif string[j] == "1":
                                temp *= (total[g[2][j]])[1] # multiply by P(1)
                            j += 1
                    else:
                        while len(string) < g[3]:
                            string = string.split()
                            string.insert(0, "0")
                            string = "".join(string)
                        j = 0
                        while j < g[3]:
                            if string[j] == "0":
                                temp *= (total[g[2][j]])[0] # multiply by P(0)
                            elif string[j] == "1":
                                temp *= (total[g[2][j]])[1] # multiply by P(1)
                            j += 1
                    p1 += temp
                i += 1
            total[g[1]] = [1 - p1, p1]
        elif g[0] == "xnor":
            temp = 1
            p1 = 0
            i = 0
            while i < 2 ** g[3]:
                if bin(i).count("1") % 2 == 0: # even number of 1's
                    string = bin(i)[2:]
                    temp = 1
                    if len(string) == g[3]:
                        j = 0
                        while j < g[3]:
                            if string[j] == "0":
                                temp *= (total[g[2][j]])[0] # multiply by P(0)
                            elif string[j] == "1":
                                temp *= (total[g[2][j]])[1] # multiply by P(1)
                            j += 1
                    else:
                        while len(string) < g[3]:
                            string = string.split()
                            string.insert(0, "0")
                            string = "".join(string)
                        j = 0
                        while j < g[3]:
                            if string[j] == "0":
                                temp *= (total[g[2][j]])[0] # multiply by P(0)
                            elif string[j] == "1":
                                temp *= (total[g[2][j]])[1] # multiply by P(1)
                            j += 1
                    p1 += temp
                i += 1
            total[g[1]] = [1 - p1, p1]

    for i in inputs: # ensures polymorphic gates cannot be inputs
        if i in total.keys():
            del total[i]
    for o in outputs: # ensures polymorphic gates cannot be outputs
        if o in total.keys():
            del total[o]
    for g in sortedgates: # ensures polymorphic gates must have 2 inputs
        if g[1] in total.keys() and g[3] != 2:
            del total[g[1]]    

    if t == "highest": # highest P(1) | lowest P(0)
        sorted_items = sorted(total.items(), key=lambda item: item[1][1], reverse=True)
        return [item[0] for item in sorted_items[:45]] # choose 45 gates
    elif t == "lowest": # highest P(0) | lowest P(1)
        sorted_items = sorted(total.items(), key=lambda item: item[1][0], reverse=True)
        return [item[0] for item in sorted_items[:45]] # choose 45 gates
    elif t == "5050": # 50/50
        nums = [22, 23]
        N = random.choice(nums) # number of highest probability gates
        M = nums[0] if N == nums[1] else nums[1] # number of lowest probability gates
        final = []
        sorted_items = sorted(total.items(), key=lambda item: item[1][1], reverse=True)
        for item in sorted_items[:N]:
            final.append(item[0])
        sorted_items = sorted(total.items(), key=lambda item: item[1][0], reverse=True)
        for item in sorted_items[:M]:
            final.append(item[0])
        return final # choose 45 gates
    elif t == "random":
        N = random.randint(0, 45)
        M = 45 - N
        final = []
        sorted_items = list(item[0] for item in total.items())
        for f in random.sample(sorted_items, 45):
            final.append(f)
        return final