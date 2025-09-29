import random

def make(line, n, inputs):
    htriggera = random.choice(list(inputs))
    htriggerb = random.choice(list(inputs))
    zeroone = random.choice(list(inputs))

    keys = []
    endlist = []
    start = (n - 1) * 8 + 1
    end = n * 8
    for num in range(start, end + 1):
        if num == end:
            keys.append(f"keyinput{num}")
        else:
            keys.append(f"keyinput{num}")
    
    ins = line.split()
    total_output = ins[0]
    a = (ins[2].split("("))[1][:-1]
    b = ins[3][:-1]
    
    zero = "zero_%d = XOR(%s, %s)" % (n, zeroone, zeroone)
    one = "one_%d = XNOR(%s, %s)" % (n, zeroone, zeroone)

    rng = []
    rng.append("zero_%d" % n)
    rng.append("one_%d" % n)

    ht_a = "htriggerA_%d = BUF(%s)" % (n, htriggera)
    ht_b = "htriggerB_%d = BUF(%s)" % (n, htriggerb)

    indA = "indA_%d = AND(%s, %s, %s)" % (n, a, htriggera, random.choice(rng))

    notk1 = "not_%s = NOT(%s)" % (keys[0], keys[0])

    w1A = "w1A_%d = AND(indA_%d, not_%s)" % (n, n, keys[0])
    w2A = "w2A_%d = AND(%s, %s)" % (n, a, keys[0])

    dynamicA = "dynamicA_%d = OR(w1A_%d, w2A_%d)" % (n, n, n)
    notdynamicA = "not_dynamicA_%d = NOT(dynamicA_%d)" % (n, n)

    indB = "indB_%d = AND(%s, %s, %s)" % (n, b, htriggerb, random.choice(rng))

    notk2 = "not_%s = NOT(%s)" % (keys[1], keys[1])

    w1B = "w1B_%d = AND(indB_%d, not_%s)" % (n, n, keys[1])
    w2B = "w2B_%d = AND(%s, %s)" % (n, b, keys[1])

    dynamicB = "dynamicB_%d = OR(w1B_%d, w2B_%d)" % (n, n, n)
    notdynamicB = "not_dynamicB_%d = NOT(dynamicB_%d)" % (n, n)

    i0 = "i0_%d = NAND(dynamicA_%d, dynamicB_%d)" % (n, n, n) # a NAND b
    i1 = "i1_%d = AND(dynamicA_%d, dynamicB_%d)" % (n, n, n) # a AND b
    i2 = "i2_%d = NOR(dynamicA_%d, dynamicB_%d)" % (n, n, n) # a NOR b
    i3 = "i3_%d = OR(dynamicA_%d, dynamicB_%d)" % (n, n, n) # a OR b
    i4 = "i4_%d = XOR(dynamicA_%d, dynamicB_%d)" % (n, n, n) # a XOR b
    i5 = "i5_%d = XNOR(dynamicA_%d, dynamicB_%d)" % (n, n, n) # a XNOR b
    i6 = "i6_%d = NOT(dynamicA_%d)" % (n, n) # NOT a
    i7 = "i7_%d = BUF(dynamicA_%d)" % (n, n) # BUF a
    i8 = "i8_%d = AND(dynamicA_%d, not_dynamicB_%d)" % (n, n, n) # a AND NOT b
    i9 = "i9_%d = AND(not_dynamicA_%d, dynamicB_%d)" % (n, n, n) # NOT a AND b
    i10 = "i10_%d = OR(dynamicA_%d, not_dynamicB_%d)" % (n, n, n) # a OR NOT b
    i11 = "i11_%d = OR(not_dynamicA_%d, dynamicB_%d)" % (n, n, n) # NOT a OR b
    i12 = "i12_%d = NOT(dynamicB_%d)" % (n, n) # NOT b
    i13 = "i13_%d = BUF(dynamicB_%d)" % (n, n) # BUF b
    i14 = "i14_%d = BUF(one_%d)" % (n, n) # TRUE
    i15 = "i15_%d = BUF(zero_%d)" % (n, n) # FALSE

    notk3 = "not_%s = NOT(%s)" % (keys[2], keys[2])
    w0s0 = "w0s0_%d = AND(zero_%d, not_%s)" % (n, n, keys[2])
    w1s0 = "w1s0_%d = AND(one_%d, %s)" % (n, n, keys[2])
    s1 = "s1_%d = OR(w0s0_%d, w1s0_%d)" % (n, n, n)
    nots1 = "not_s1_%d = NOT(s1_%d)" % (n, n)

    notk4 = "not_%s = NOT(%s)" % (keys[3], keys[3])
    w2s0 = "w2s0_%d = AND(s1_%d, not_%s)" % (n, n, keys[3])
    w3s0 = "w3s0_%d = AND(not_s1_%d, %s)" % (n, n, keys[3])
    s0 = "s0_%d = OR(w2s0_%d, w3s0_%d)" % (n, n, n)
    nots0 = "not_s0_%d = NOT(s0_%d)" % (n, n)

    notk5 = "not_%s = NOT(%s)" % (keys[4], keys[4])
    notk6 = "not_%s = NOT(%s)" % (keys[5], keys[5])
    w0s2 = "w0s2_%d = AND(zero_%d, not_%s, not_%s)" % (n, n, keys[4], keys[5])
    w1s2 = "w1s2_%d = AND(one_%d, not_%s, %s)" % (n, n, keys[4], keys[5])
    w2s2 = "w2s2_%d = AND(%s, %s, not_%s)" % (n, b, keys[4], keys[5])
    w3s2 = "w3s2_%d = AND(%s, %s, %s)" % (n, a, keys[4], keys[5])
    s2 = "s2_%d = OR(w0s2_%d, w1s2_%d, w2s2_%d, w3s2_%d)" % (n, n, n, n, n)
    nots2 = "not_s2_%d = NOT(s2_%d)" % (n, n)

    notk7 = "not_%s = NOT(%s)" % (keys[6], keys[6])
    notk8 = "not_%s = NOT(%s)" % (keys[7], keys[7])
    w0s3 = "w0s3_%d = AND(zero_%d, not_%s, not_%s)" % (n, n, keys[6], keys[7])
    w1s3 = "w1s3_%d = AND(one_%d, not_%s, %s)" % (n, n, keys[6], keys[7])
    w2s3 = "w2s3_%d = AND(%s, %s, not_%s)" % (n, b, keys[6], keys[7])
    w3s3 = "w3s3_%d = AND(%s, %s, %s)" % (n, a, keys[6], keys[7])
    s3 = "s3_%d = OR(w0s3_%d, w1s3_%d, w2s3_%d, w3s3_%d)" % (n, n, n, n, n)
    nots3 = "not_s3_%d = NOT(s3_%d)" % (n, n)

    and0mux0 = "and0mux0_%d = AND(i0_%d, not_s0_%d, not_s1_%d)" % (n, n, n, n)
    and1mux0 = "and1mux0_%d = AND(i1_%d, not_s0_%d, s1_%d)" % (n, n, n, n)
    and2mux0 = "and2mux0_%d = AND(i2_%d, s0_%d, not_s1_%d)" % (n, n, n, n)
    and3mux0 = "and3mux0_%d = AND(i3_%d, s0_%d, s1_%d)" % (n, n, n, n)
    mux0 = "mux0_%d = OR(and0mux0_%d, and1mux0_%d, and2mux0_%d, and3mux0_%d)" % (n, n, n, n, n)

    and0mux1 = "and0mux1_%d = AND(i4_%d, not_s0_%d, not_s1_%d)" % (n, n, n, n)
    and1mux1 = "and1mux1_%d = AND(i5_%d, not_s0_%d, s1_%d)" % (n, n, n, n)
    and2mux1 = "and2mux1_%d = AND(i6_%d, s0_%d, not_s1_%d)" % (n, n, n, n)
    and3mux1 = "and3mux1_%d = AND(i7_%d, s0_%d, s1_%d)" % (n, n, n, n)
    mux1 = "mux1_%d = OR(and0mux1_%d, and1mux1_%d, and2mux1_%d, and3mux1_%d)" % (n, n, n, n, n)

    and0mux2 = "and0mux2_%d = AND(i8_%d, not_s0_%d, not_s1_%d)" % (n, n, n, n)
    and1mux2 = "and1mux2_%d = AND(i9_%d, not_s0_%d, s1_%d)" % (n, n, n, n)
    and2mux2 = "and2mux2_%d = AND(i10_%d, s0_%d, not_s1_%d)" % (n, n, n, n)
    and3mux2 = "and3mux2_%d = AND(i11_%d, s0_%d, s1_%d)" % (n, n, n, n)
    mux2 = "mux2_%d = OR(and0mux2_%d, and1mux2_%d, and2mux2_%d, and3mux2_%d)" % (n, n, n, n, n)

    and0mux3 = "and0mux3_%d = AND(i12_%d, not_s0_%d, not_s1_%d)" % (n, n, n, n)
    and1mux3 = "and1mux3_%d = AND(i13_%d, not_s0_%d, s1_%d)" % (n, n, n, n)
    and2mux3 = "and2mux3_%d = AND(i14_%d, s0_%d, not_s1_%d)" % (n, n, n, n)
    and3mux3 = "and3mux3_%d = AND(i15_%d, s0_%d, s1_%d)" % (n, n, n, n)
    mux3 = "mux3_%d = OR(and0mux3_%d, and1mux3_%d, and2mux3_%d, and3mux3_%d)" % (n, n, n, n, n)

    and0mux4 = "and0mux4_%d = AND(mux0_%d, not_s2_%d, not_s3_%d)" % (n, n, n, n)
    and1mux4 = "and1mux4_%d = AND(mux1_%d, not_s2_%d, s3_%d)" % (n, n, n, n)
    and2mux4 = "and2mux4_%d = AND(mux2_%d, s2_%d, not_s3_%d)" % (n, n, n, n)
    and3mux4 = "and3mux4_%d = AND(mux3_%d, s2_%d, s3_%d)" % (n, n, n, n)
    totaloutput = "%s = OR(and0mux4_%d, and1mux4_%d, and2mux4_%d, and3mux4_%d)" % (total_output, n, n, n, n)
    srb = "srb%d = XNOR(%s, keyinput%d)" % (n, total_output, n + 360)

    endlist.append(zero)
    endlist.append(one)
    endlist.append(ht_a)
    endlist.append(ht_b)
    endlist.append(indA)
    endlist.append(notk1)
    endlist.append(w1A)
    endlist.append(w2A)
    endlist.append(dynamicA)
    endlist.append(notdynamicA)
    endlist.append(indB)
    endlist.append(notk2)
    endlist.append(w1B)
    endlist.append(w2B)
    endlist.append(dynamicB)
    endlist.append(notdynamicB)
    endlist.append(i0)
    endlist.append(i1)
    endlist.append(i2)
    endlist.append(i3)
    endlist.append(i4)
    endlist.append(i5)
    endlist.append(i6)
    endlist.append(i7)
    endlist.append(i8)
    endlist.append(i9)
    endlist.append(i10)
    endlist.append(i11)
    endlist.append(i12)
    endlist.append(i13)
    endlist.append(i14)
    endlist.append(i15)
    endlist.append(notk3)
    endlist.append(w0s0)
    endlist.append(w1s0)
    endlist.append(s1)
    endlist.append(nots1)
    endlist.append(notk4)
    endlist.append(w2s0)
    endlist.append(w3s0)
    endlist.append(s0)
    endlist.append(nots0)
    endlist.append(notk5)
    endlist.append(notk6)
    endlist.append(w0s2)
    endlist.append(w1s2)
    endlist.append(w2s2)
    endlist.append(w3s2)
    endlist.append(s2)
    endlist.append(nots2)
    endlist.append(notk7)
    endlist.append(notk8)
    endlist.append(w0s3)
    endlist.append(w1s3)
    endlist.append(w2s3)
    endlist.append(w3s3)
    endlist.append(s3)
    endlist.append(nots3)
    endlist.append(and0mux0)
    endlist.append(and1mux0)
    endlist.append(and2mux0)
    endlist.append(and3mux0)
    endlist.append(mux0)
    endlist.append(and0mux1)
    endlist.append(and1mux1)
    endlist.append(and2mux1)
    endlist.append(and3mux1)
    endlist.append(mux1)
    endlist.append(and0mux2)
    endlist.append(and1mux2)
    endlist.append(and2mux2)
    endlist.append(and3mux2)
    endlist.append(mux2)
    endlist.append(and0mux3)
    endlist.append(and1mux3)
    endlist.append(and2mux3)
    endlist.append(and3mux3)
    endlist.append(mux3)
    endlist.append(and0mux4)
    endlist.append(and1mux4)
    endlist.append(and2mux4)
    endlist.append(and3mux4)
    endlist.append(totaloutput)
    endlist.append(srb)

    return endlist