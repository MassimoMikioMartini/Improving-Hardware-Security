def replace(netlist, selected_gates, t, output, e, inputs):
    newfile = "%s" % output
    with open(newfile, "w") as file:
        if t == "gshe":
            import gshe as g
        elif t == "dwm":
            import dwm as g
        if e == "hybrid shielding":
            import hybridshielding as e
        with open(netlist) as f:
            i = 1
            k = 0
            for line in f:
                s = line.split()
                if len(s) > 0:
                    if line.startswith("# c"):
                        file.write("%s" % line)
                        if t == "gshe":
                            for num in range(1, 361):
                                file.write(f"INPUT(keyinput{num})\n")
                        elif t == "dwm":
                            for num in range (1, 136):
                                file.write(f"INPUT(keyinput{num})\n")
                    if s[0] in selected_gates:
                        for l in g.make(line, i, inputs):
                            file.write("%s\n" % l)
                        i += 1
                    else:
                        file.write("%s" % line)

    print("File Done!")