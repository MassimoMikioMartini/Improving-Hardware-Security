import probability_selection as p
import random

def old(netlist, iternum):
    inputs, outputs, gates = p.parse(netlist)
    ga = [g[1] for g in gates]

    with open(netlist[:-6] + ("_%d" % iternum) + ".v", "w") as file:
        file.write("module %s(input %s, output %s);" % (netlist[:-6], ", input ".join(list(inputs)), ", output ".join(list(outputs))))
        file.write("\n\twire %s;\n" % ";\n\twire ".join(ga))

        for g in gates:
            i = 0
            while i < len(g[2]):
                g[2][i] = g[2][i].strip()
                g[2][i] = g[2][i].strip(" ")
                g[2][i] = g[2][i].strip("(")
                g[2][i] = g[2][i].strip(")")
                i += 1
            if g[0] == "and":
                file.write("\tassign %s = %s;\n" % (g[1], " & ".join(g[2])))
            elif g[0] == "or":
                file.write("\tassign %s = %s;\n" % (g[1], " | ".join(g[2])))
            elif g[0] == "xor":
                file.write("\tassign %s = %s;\n" % (g[1], " ^ ".join(g[2])))
            elif g[0] == "nand":
                file.write("\tassign %s = ~%s;\n" % (g[1], " & ~".join(g[2])))
            elif g[0] == "nor":
                file.write("\tassign %s = ~%s;\n" % (g[1], " | ~".join(g[2])))
            elif g[0] == "xnor":
                file.write("\tassign %s = ~%s;\n" % (g[1], " ^ ~".join(g[2])))
            elif g[0] == "buf":
                file.write("\tassign %s = %s;\n" % (g[1], g[2][0]))
            elif g[0] == "not":
                file.write("\tassign %s = ~%s;\n" % (g[1], g[2][0]))
        
        file.write("endmodule")

def new(netlist, iternum):
    keys = []
    srb = []
    srb.append(" isb")
    srb.append(" reinstatein")
    srb.append(" reinstateout")
    for num in range(1, 190):
        keys.append(f"keyinput{num}")
        srb.append(f" keyinput{num}")
    for num in range (1, 46):
        srb.append(f" srb{num}")
        srb.append(f" newin{num}")
        srb.append(f" newout{num}")
    inputs, outputs, gates = p.parse(netlist)
    selected_gates = p.select_gates(netlist, "random")
    ga = [g[1] for g in gates]
    randomoutputs = random.sample(list(outputs), (len(outputs) // (100 // 50))) # percent = 50%

    with open(netlist[:-6] + ("_%d" % iternum) + "_hybrid.v", "w") as file:
        file.write("module %s_hybrid(input %s, input %s, output %s);" % (netlist[:-6], ", input ".join(list(inputs)), ", input ".join(keys), ", output ".join(list(outputs))))
        file.write("\n\twire %s;\n\twire%s;\n" % (";\n\twire ".join(ga), ";\n\twire".join(srb)))

        j = 1
        for g in gates:
            i = 0
            while i < len(g[2]):
                g[2][i] = g[2][i].strip()
                g[2][i] = g[2][i].strip(" ")
                g[2][i] = g[2][i].strip("(")
                g[2][i] = g[2][i].strip(")")
                i += 1
            if g[1] in selected_gates:
                a = g[2][0]
                b = g[2][1]

                keyinputs = []
                start = (j - 1) * 3 + 1
                end = j * 3
                for num in range(start, end + 1):
                    keyinputs.append(f"keyinput{num}")

                i0 = "~(%s ^ %s)" % (a, b)
                i1 = "%s ^ %s" % (a, b)
                i2 = "%s | %s" % (a, b)
                i3 = "~(%s | %s)" % (a, b)
                i4 = "~%s" % a
                i6 = "%s & %s" % (a, b)
                i7 = "~(%s & %s)" % (a, b)
                file.write("\tassign %s = (%s & ~%s & ~%s & ~%s) | (%s & ~%s & ~%s & %s) | (%s & ~%s & %s & ~%s) | (%s & ~%s & %s & %s) | (%s & %s & ~%s & ~%s) | (%s & %s & %s & ~%s) | (%s & %s & %s & %s);\n" % (g[1], i0, keyinputs[0], keyinputs[1], keyinputs[2], i1, keyinputs[0], keyinputs[1], keyinputs[2], i2, keyinputs[0], keyinputs[1], keyinputs[2], i3, keyinputs[0], keyinputs[1], keyinputs[2], i4, keyinputs[0], keyinputs[1], keyinputs[2], i6, keyinputs[0], keyinputs[1], keyinputs[2], i7, keyinputs[0], keyinputs[1], keyinputs[2]))
                file.write("\tassign srb%d = ~(%s ^ keyinput%d);\n" % (j, g[1], j + 135))
                j += 1
                if j == 45:
                    x = 181
                    a = "reinstatein"
                    b = "keyinput%d" % x
                    htriggera = random.choice(list(inputs))
                    htriggerb = random.choice(list(inputs))
                    rng = random.choice(["1'b0", "1'b1"])
                    keyinputs = ["keyinput%d" % (x + 1), "keyinput%d" % (x + 2), "keyinput%d" % (x + 3), "keyinput%d" % (x + 4), "keyinput%d" % (x + 5), "keyinput%d" % (x + 6), "keyinput%d" % (x + 7), "keyinput%d" % (x + 8)]
                    file.write("\tassign reinstatein = srb1 & srb2 & srb3 & srb4 & srb5 & srb6 & srb7 & srb8 & srb9 & srb10 & srb11 & srb12 & srb13 & srb14 & srb15 & srb16 & srb17 & srb18 & srb19 & srb20 & srb21 & srb22 & srb23 & srb24 & srb25 & srb26 & srb27 & srb28 & srb29 & srb30 & srb31 & srb32 & srb33 & srb34 & srb35 & srb36 & srb37 & srb38 & srb39 & srb40 & srb41 & srb42 & srb43 & srb44 & srb45;\n")

                    dya = "((%s & %s & %s) & ~%s) | (%s & %s)" % (a, htriggera, rng, keyinputs[0], a, keyinputs[0])
                    dyb = "((%s & %s & %s) & ~%s) | (%s & %s)" % (b, htriggerb, rng, keyinputs[1], b, keyinputs[1])
                    s0 = "(~((1'b0 & ~%s) | (1'b1 & %s)) & ~%s) | (((1'b0 & ~%s) | (1'b1 & %s)) & %s)" % (keyinputs[2], keyinputs[2], keyinputs[3], keyinputs[2], keyinputs[2], keyinputs[3])
                    s1 = "(1'b0 & ~%s) | (1'b1 & %s)" % (keyinputs[2], keyinputs[2])
                    s2 = "(~%s & %s & ~%s) | (~%s & %s & %s) | (%s & 1'b0 & ~%s) | (%s & 1'b1 & %s)" % (keyinputs[4], a, keyinputs[5], keyinputs[4], b, keyinputs[5], keyinputs[4], keyinputs[5], keyinputs[4], keyinputs[5])
                    s3 = "(~%s & %s & ~%s) | (~%s & %s & %s) | (%s & 1'b0 & ~%s) | (%s & 1'b1 & %s)" % (keyinputs[6], a, keyinputs[7], keyinputs[6], b, keyinputs[7], keyinputs[6], keyinputs[7], keyinputs[6], keyinputs[7])

                    i0 = "(~(%s) & (~(%s) & ~(%s)) & ~(%s)) | (~(%s) & ((%s) & (%s)) & (%s)) | ((%s) & (~(%s) | ~(%s)) & ~(%s)) | ((%s) & ((%s) | (%s)) & (%s))" % (s0, dya, dyb, s1, s0, dya, dyb, s1, s0, dya, dyb, s1, s0, dya, dyb, s1)
                    i1 = "(~(%s) & (%s ^ %s) & ~(%s)) | (~(%s) & (~%s ^ ~%s) & (%s)) | ((%s) & ~%s & ~(%s)) | ((%s) & %s & (%s))" % (s0, dya, dyb, s1, s0, dya, dyb, s1, s0, dya, s1, s0, dya, s1)
                    i2 = "(~(%s) & (%s & ~%s) & ~(%s)) | (~(%s) & (~%s & %s) & (%s)) | ((%s) & (%s | ~%s) & ~(%s)) | ((%s) & (~%s | %s) & (%s))" % (s0, dya, dyb, s1, s0, dya, dyb, s1, s0, dya, dyb, s1, s0, dya, dyb, s1)
                    i3 = "(~(%s) & ~%s & ~(%s)) | (~(%s) & %s & (%s)) | ((%s) & 1'b1 & ~(%s)) | ((%s) & 1'b0 & (%s))" % (s0, dyb, s1, s0, dyb, s1, s0, s1, s0, s1)
                    file.write("\tassign reinstateout = ((~(%s) & (%s) & ~(%s)) | (~(%s) & (%s) & (%s)) | ((%s) & (%s) & ~(%s)) | ((%s) & (%s) & (%s)));\n" % (s2, i0, s3, s2, i1, s3, s2, i2, s3, s2, i3, s3))

            else:
                if g[1] in randomoutputs:
                    n = randomoutputs.index(g[1])
                    if g[0] == "and":
                        file.write("\tassign newout%d = %s;\n" % (n, " & ".join(g[2])))
                    elif g[0] == "or":
                        file.write("\tassign newout%d = %s;\n" % (n, " | ".join(g[2])))
                    elif g[0] == "xor":
                        file.write("\tassign newout%d = %s;\n" % (n, " ^ ".join(g[2])))
                    elif g[0] == "nand":
                        file.write("\tassign newout%d = ~%s;\n" % (n, " & ~".join(g[2])))
                    elif g[0] == "nor":
                        file.write("\tassign newout%d = ~%s;\n" % (n, " | ~".join(g[2])))
                    elif g[0] == "xnor":
                        file.write("\tassign newout%d = ~%s;\n" % (n, " ^ ~".join(g[2])))
                    elif g[0] == "buf":
                        file.write("\tassign newout%d = %s;\n" % (n, g[2][0]))
                    elif g[0] == "not":
                        file.write("\tassign newout%d = ~%s;\n" % (n, g[2][0]))
                    file.write("\tassign newin%d = newout%d ^ reinstatein;\n" % (n, n))
                    file.write("\tassign %s = newin%d ^ reinstateout;\n" % (g[1], n))
                else:
                    if g[0] == "and":
                        file.write("\tassign %s = %s;\n" % (g[1], " & ".join(g[2])))
                    elif g[0] == "or":
                        file.write("\tassign %s = %s;\n" % (g[1], " | ".join(g[2])))
                    elif g[0] == "xor":
                        file.write("\tassign %s = %s;\n" % (g[1], " ^ ".join(g[2])))
                    elif g[0] == "nand":
                        file.write("\tassign %s = ~%s;\n" % (g[1], " & ~".join(g[2])))
                    elif g[0] == "nor":
                        file.write("\tassign %s = ~%s;\n" % (g[1], " | ~".join(g[2])))
                    elif g[0] == "xnor":
                        file.write("\tassign %s = ~%s;\n" % (g[1], " ^ ~".join(g[2])))
                    elif g[0] == "buf":
                        file.write("\tassign %s = %s;\n" % (g[1], g[2][0]))
                    elif g[0] == "not":
                        file.write("\tassign %s = ~%s;\n" % (g[1], g[2][0]))
            
        file.write("endmodule")

def tb(netlist, iternum):
    inputs, outputs, gates = p.parse(netlist)
    inputs = list(inputs)
    outputs = list(outputs)

    old(netlist, iternum) # creates original verilog
    new(netlist, iternum) # creates hybrid shielding + polymorphic gate verilog
    keys = []
    normalout = []
    hybridout = []
    for num in range(1, 190):
        keys.append(f"keyinput{num}")
    for i in outputs:
        normalout.append(i + "_n")
        hybridout.append(i + "_h")
    I = len(inputs) # number of inputs
    k = 189 # number of keys

    P = outputs
    c_sum = 0
    with open(netlist[:-6] + ("_%d" % iternum) + "_tb.v", "w") as file:
        file.write("`timescale 1ns/1ps\n")
        file.write("module tb;\n")
        file.write("\tinteger file;\n")
        file.write("\treg %s;\n\treg %s;\n\twire %s;\n\twire %s;\n" % (", ".join(inputs), ", ".join(keys), ", ".join(normalout), ", ".join(hybridout)))
        file.write("\t%s uut_n(%s, %s);\n" % (netlist[:-6], ", ".join(inputs), ", ".join(normalout)))
        file.write("\t%s uut_h(%s, %s, %s);\n" % (netlist[:-6] + "_hybrid", ", ".join(inputs), ", ".join(keys), ", ".join(hybridout)))
        file.write("\t\n\tinitial begin\n\t\t")
        file.write('file = $fopen("%s", "w");\n\t\t' % (netlist[:-6] + ("_%d" % iternum) + "_output.txt"))
        for i in range(1, 10001): # 10000 random input/key patterns (starting with 10)
            inputstr = bin(random.randint(0, (2 ** I)))
            inputstr = inputstr[2:]
            if len(inputstr) < I: # adds leading 0's
                inputstr = ((I - len(inputstr)) * "0") + inputstr
            keystr = bin(random.randint(0, (2 ** k)))
            keystr = keystr[2:]
            if len(keystr) < k: # adds leading 0's
                keystr = ((k - len(keystr)) * "0") + keystr
            o = 0
            while o < I:
                file.write("%s = %s; " % (inputs[o], inputstr[o]))
                o += 1
            l = 1
            while l < k + 1:
                file.write("keyinput%d = %s; #10;" % (l, keystr[l - 1]))
                l += 1
            u = 0
            while u < len(outputs):
                file.write('\n\t\t#10 $fwrite(file, "normal=%s hybrid=%s\\n", %s, %s);' % (("%b"), ("%b"), normalout[u], hybridout[u]))
                u += 1
            file.write('\n\t\t#10 $fwrite(file, "break\\n");')
            file.write("\n\t\t")
        file.write("$fclose(file);\n\tend\nendmodule")

netlist = "cN432.bench"
i = 0
while i < 10:
    tb(netlist, i)
    print(netlist[:-6], i, "Finish")
    i += 1