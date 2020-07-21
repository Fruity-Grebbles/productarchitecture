import os, sys
from graphviz import Graph


def main(argv):
    try:
        ifilename = argv[1]
        with open(ifilename, "r") as ifile:
            makedot(ifile)

    except IndexError:
        print("Must include filename argument")


def parse(parentgraph, l, lines):
    if len(lines) > 0:
        n = l.replace("\t", "").replace(" ", "")
        spaces = len(l) - len(l.lstrip())
        nextspaces = len(lines[0]) - len(lines[0].lstrip())

        if nextspaces > spaces:
            print("Subgraph")
            n = "cluster_" + n
            with parentgraph.subgraph(name="cluster_"+l.strip()) as c:
                c.attr(label=l.rstrip().lstrip())
                parse(c, lines[0], lines[1:])
        else:
            print("node")
            c = parentgraph.node(n, l.rstrip().lstrip())
            parse(parentgraph, lines[0], lines[1:])


def makedot(ifile):
    lines = [line for line in ifile.readlines()]
    graphname = os.path.splitext(os.path.basename(ifile.name))[0]
    dot = Graph(graphname.replace(" ", ""), filename=graphname+".dot", format="pdf")
    dot.attr(label=graphname)
    dot.body.append(
        """
    fontname="avenir-medium"
    labelloc=t
    labeljust=l
    smoothing="true"
    pack="true"
    packmode="array_cl50"
    pad=1
    nodesep=".125"
    quantum=2
    node [shape="box", fontname="avenir",labelloc="t"]"""
    )

    parse(dot, lines[0], lines[1:])

    # print (dot.source)

    dot.render()


if __name__ == "__main__":
    main(sys.argv)
    exit(0)
