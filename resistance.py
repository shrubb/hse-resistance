__author__ = 'shrubb'

import sys
from time import time
from xml.dom.minidom import parse
import resistancecalc

if len(sys.argv) < 3:
    print(
        """Usage:
        Argument 1: input file (*.xml),
        Argument 2: output file (*.csv)""")
    exit()

# parsing XML
try:
    tree = parse(sys.argv[1])
except Exception as e:
    print(e), exit()

# extracting node IDs
temp = sorted(
    tree.getElementsByTagName("net"),
    key=lambda x: int(x.getAttribute("id")))
idents = {temp[i].getAttribute("id"): i for i in range(len(temp))}
del temp

# extracting edges
raw_edge_list = \
    tree.getElementsByTagName("diode") + \
    tree.getElementsByTagName("resistor") + \
    tree.getElementsByTagName("capactor")
edge_list = []


class Edge:
    def __init__(self, _from, _to, _resistance):
        self.fr = _from
        self.to = _to
        self.resistance = _resistance

for edge in raw_edge_list:
    v_from = idents[edge.getAttribute("net_from")]
    v_to = idents[edge.getAttribute("net_to")]
    resistance = edge.getAttribute("resistance")
    rev_resistance = edge.getAttribute("reverse_resistance")

    edge_list.append(
        Edge(v_from,
             v_to,
             float(resistance)))
    edge_list.append(
        Edge(v_to,
             v_from,
             float(rev_resistance) if rev_resistance else float(resistance)))

N = len(idents)


# calculating global resistances
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return float("inf")

d = [[0.0 if x == y else float("inf") for x in range(N)] for y in range(N)]
for edge in edge_list:
    d[edge.fr][edge.to] = \
        divide(
            1.0,
            divide(
                1.0,
                d[edge.fr][edge.to]) + divide(1.0, edge.resistance))

d_cpp = [row.copy() for row in d]

print("Calculating in Python...", end="")
start_time = time()

for k in range(N):
    for i in range(N):
        for j in range(N):
            d[i][j] = \
                divide(
                    1.0,
                    divide(1.0, d[i][j]) + divide(1.0, d[i][k] + d[k][j]))

py_time = time() - start_time
print("done")

print("Calculating in C...", end="")
start_time = time()

resistancecalc.Floyd_Warshall(d_cpp)

c_time = time() - start_time
print("done")
print("Pure Python was {} times slower".format(py_time / c_time))

for i in range(N):
    for j in range(N):
        if d[i][j] != d_cpp[i][j]:
            raise Exception("C and Python calculations return different results")

# CSV export
try:
    outfile = open(sys.argv[2], 'w')
except Exception as e:
    print(e), exit()

outfile.writelines(["%.6f," * N % tuple(row) + '\n' for row in d])
outfile.close()
