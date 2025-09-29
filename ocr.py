def calculate_ocr(file):
    sum = 0
    num = []
    with open(file) as f:
        for line in f:
            l = line.split()
            if len(l) == 2:
                a = l[0][7:]
                b = l[1][7:]
                num.append(a == b)
            else:
                t = num.count(False)
                sum += (t / (len(num)))
                num = []
    return ((1 / 10000) * 100 * sum)

netlist = "cN7552.bench"
i = 0
while i < 10:
    print(calculate_ocr(netlist[:-6] + ("_%d" % i) + "_output.txt"))
    i += 1