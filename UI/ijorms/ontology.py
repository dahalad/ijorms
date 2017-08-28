import csv


class Node:
    """
    Class to define node in ontology tree
    """
    def __init__(self, value, subClassOf, parentOf, depth):
        self.value = value  # value of the node
        self.subClassOf = subClassOf  # the node(s) that is/are the parent this node
        self.parentOf = parentOf  # the node(s) that this node is parent of
        self.depth = depth


def createNode(value, subClassOf, parentOf, depth):
    """
    Creates Node in the ontology tree
    :param value: Value of the node
    :param subClassOf: subclass of this node
    :param parentOf: parent of this/these node
    :param depth: depth from root
    :return: this node
    """
    return Node(value, subClassOf, parentOf, depth)


def getObject(val, ont):
    """
    Get value from ontology tree
    :param val: value to be searched
    :param ont: ontology
    :return: return value
    """
    for i in ont:
        if(i.value == val):
            return i

def getValues(ont):
    values = []
    for i in ont:
        values.append(i.value.lower())
    return values

def display(ont):
    result = {}
    temp = {}
    for o in ont:
        if (o.depth == 1):
            temp[o.value] = []
            for p in o.parentOf:
                temp[o.value].append(p.value)
    result["programming language"] = temp
    print(result)


def creatOntology():
    """
    Creates ontology
    :return:  ontology
    """
    Ontology = []
    Ontology.append(createNode("programming language", None, [], 0))
    with open('skillsWiki.csv', 'r') as inp:
        reader = list(csv.reader(inp, delimiter=','))
        root = getObject("programming language", Ontology)
        depth1 = set()
        for i in reader:
            length = len(depth1)
            depth1.add(i[1])
            if (length != len(depth1)):
                depth1Node = createNode(i[1], root, [], 1)
                Ontology.append(depth1Node)
                root.parentOf.append(depth1Node)
        for i in reader:
            parent = getObject(i[1], Ontology)
            depth2Node = createNode(i[0], parent, [], 2)
            Ontology.append(depth2Node)
            parent.parentOf.append(depth2Node)
    inp.close()
    return Ontology
