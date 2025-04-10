from pyshacl import validate
from rdflib import Graph

# Load the data graph (policy in JSON-LD)
data_graph = Graph()
data_graph.parse("policy.jsonld", format="json-ld")

# Load the SHACL shape graph
shacl_graph = Graph()
shacl_graph.parse("shape2.ttl", format="turtle")

# Run validation
conforms, results_graph, results_text = validate(
    data_graph,
    shacl_graph=shacl_graph,
    inference='rdfs',   # optional; you can also use 'none'
    abort_on_first=False,
    meta_shacl=False,
    advanced=True,
    debug=False
)

# Output results
print("Conforms:", conforms)
print("Validation Report:\n")
print(results_text)
