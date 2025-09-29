def make(line, n, inputs):
    keys = []
    endlist = []
    start = (n - 1) * 2 + 1
    end = n * 2
    for num in range(start, end + 1):
        if num == end:
            keys.append(f"keyinput{num}")
        else:
            keys.append(f"keyinput{num}")
    
    ins = line.split()
    total_output = ins[0]
    a = (ins[2].split("("))[1][:-1]
    b = ins[3][:-1]
    
    notk1 = "not_%s = NOT(%s)" % (keys[0], keys[0])
    notk2 = "not_%s = NOT(%s)" % (keys[1], keys[1])

    i0 = "i0_%d = XOR(%s, %s)" % (n, a, b) # a XOR b
    i1 = "i1_%d = NAND(%s, %s)" % (n, a, b) # a NAND b
    i2 = "i2_%d = NOR(%s, %s)" % (n, a, b) # a NOR b

    and0 = "and0_%d = AND(i0_%d, not_%s, not_%s)" % (n, n, keys[0], keys[1])
    and1 = "and1_%d = AND(i1_%d, not_%s, %s)" % (n, n, keys[0], keys[1])
    and2 = "and2_%d = AND(i2_%d, %s, not_%s)" % (n, n, keys[0], keys[1])

    output = "%s = OR(and0_%d, and1_%d, and2_%d)" % (total_output, n, n, n)
    srb = "srb%d = XNOR(%s, keyinput%d)" % (n, total_output, n + 90)
    
    endlist.append(notk1)
    endlist.append(notk2)
    endlist.append(i0)
    endlist.append(i1)
    endlist.append(i2)
    endlist.append(and0)
    endlist.append(and1)
    endlist.append(and2)
    endlist.append(output)
    endlist.append(srb)

    return endlist