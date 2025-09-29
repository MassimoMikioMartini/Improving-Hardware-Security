def make(line, n, inputs):
    key = "keyinput%d" % n
    endlist = []
    
    ins = line.split()
    total_output = ins[0]
    a = (ins[2].split("("))[1][:-1]
    b = ins[3][:-1]
    
    notk1 = "not_%s = NOT(%s)" % (key, key)

    i0 = "i0_%d = AND(%s, %s)" % (n, a, b) # a NAND b
    i1 = "i1_%d = OR(%s, %s)" % (n, a, b) # a NOR b

    and0 = "and0_%d = AND(i0_%d, not_%s)" % (n, n, key)
    and1 = "and1_%d = AND(i1_%d, %s)" % (n, n, key)

    output = "%s = OR(and0_%d, and1_%d)" % (total_output, n, n)
    srb = "srb%d = XNOR(%s, keyinput%d)" % (n, total_output, n + 45)
    
    endlist.append(notk1)
    endlist.append(i0)
    endlist.append(i1)
    endlist.append(and0)
    endlist.append(and1)
    endlist.append(output)
    endlist.append(srb)

    return endlist