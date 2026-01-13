# This file is the main file—it will generate 10 encrypted circuits which may be used for the SAT Tool

import probability_selection as p # Our algorithm—returns the selected gates ranked based on probability
import hybridshielding as h # This file is what takes the original netlist, chosen gates from our algorithm, and all other parameters and creates a new encrypted circuit

i = 0
while i < 10:
    netlist = "cN499.bench" # Replace with any benchmark e.g. c880 (cN880), c6288 (cN6288), etc.
    percent = 50 # You can change the percent of outputs connected to Reinstate Blocks
    t = "gshe" # You can also change the type of polymorphic device: GSHE, DWM, etc.
    m = "highest" # You can lastly change the mode: highest (highest probability), lowest (lowest probability), 50/50, and random
    name = t + "_" + str(percent) + "_" + m + "_" + str(i) + "_" + netlist
    selected_gates = p.select_gates(netlist, m)
    inputs = (p.parse(netlist))[0]
    outputs = (p.parse(netlist))[1]
    h.replace(netlist, selected_gates, t, name, inputs, outputs, percent)
    i += 1