import probability_selection as p
import hybridshielding as h

i = 0
while i < 10:
    netlist = "cN6288.bench"
    percent = 50
    t = "gshe"
    m = "random"
    name = t + "_" + str(percent) + "_" + m + "_" + str(i) + "_" + netlist
    selected_gates = p.select_gates(netlist, m)
    inputs = (p.parse(netlist))[0]
    outputs = (p.parse(netlist))[1]
    h.replace(netlist, selected_gates, t, name, inputs, outputs, percent)
    i += 1