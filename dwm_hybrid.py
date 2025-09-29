def make(line, n, inputs):
    keys = []
    endlist = []
    start = (n - 1) * 3 + 1
    end = n * 3
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
    notk3 = "not_%s = NOT(%s)" % (keys[2], keys[2])

    i0 = "i0_%d = XNOR(%s, %s)" % (n, a, b) # a XNOR b
    i1 = "i1_%d = XOR(%s, %s)" % (n, a, b) # a XOR b
    i2 = "i2_%d = OR(%s, %s)" % (n, a, b) # a OR b
    i3 = "i3_%d = NOR(%s, %s)" % (n, a, b) # a NOR b
    i4 = "i4_%d = NOT(%s)" % (n, a) # NOT a
    i6 = "i6_%d = AND(%s, %s)" % (n, a, b) # a AND b
    i7 = "i7_%d = NAND(%s, %s)" % (n, a, b) # a NAND b

    and0 = "and0_%d = AND(i0_%d, not_%s, not_%s, not_%s)" % (n, n, keys[0], keys[1], keys[2])
    and1 = "and1_%d = AND(i1_%d, not_%s, not_%s, %s)" % (n, n, keys[0], keys[1], keys[2])
    and2 = "and2_%d = AND(i2_%d, not_%s, %s, not_%s)" % (n, n, keys[0], keys[1], keys[2])
    and3 = "and3_%d = AND(i3_%d, not_%s, %s, %s)" % (n, n, keys[0], keys[1], keys[2])
    and4 = "and4_%d = AND(i4_%d, %s, not_%s, not_%s)" % (n, n, keys[0], keys[1], keys[2])
    and6 = "and6_%d = AND(i6_%d, %s, %s, not_%s)" % (n, n, keys[0], keys[1], keys[2])
    and7 = "and7_%d = AND(i7_%d, %s, %s, %s)" % (n, n, keys[0], keys[1], keys[2])

    output = "%s = OR(and0_%d, and1_%d, and2_%d, and3_%d, and4_%d, and6_%d, and7_%d)" % (total_output, n, n, n, n, n, n, n)
    srb = "srb%d = XNOR(%s, keyinput%d)" % (n, total_output, n + 135)
    
    endlist.append(notk1)
    endlist.append(notk2)
    endlist.append(notk3)
    endlist.append(i0)
    endlist.append(i1)
    endlist.append(i2)
    endlist.append(i3)
    endlist.append(i4)
    endlist.append(i6)
    endlist.append(i7)
    endlist.append(and0)
    endlist.append(and1)
    endlist.append(and2)
    endlist.append(and3)
    endlist.append(and4)
    endlist.append(and6)
    endlist.append(and7)
    endlist.append(output)
    endlist.append(srb)

    return endlist