def make(line, n, inputs):
    key = "keyinput%d" % n
    endlist = []
    
    ins = line.split()
    total_output = ins[0]
    a = (ins[2].split("("))[1][:-1]
    b = ins[3][:-1]
    
    output = "%s = AND(%s, %s, %s)" % (total_output, a, b, key)
    srb = "srb%d = XNOR(%s, keyinput%d)" % (n, total_output, n + 45)
    
    endlist.append(output)
    endlist.append(srb)

    return endlist