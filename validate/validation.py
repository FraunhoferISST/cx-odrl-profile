import sys
from rdflib import Graph
from pyshacl import validate

def main(shapes_file, policy_file, ontology_file=None):
    # Load SHACL shapes graph
    shapes_graph = Graph()
    shapes_graph.parse(shapes_file, format='turtle')

    # Initialize data graph
    data_graph = Graph()

    # Load ontology if provided
    if ontology_file:
        data_graph.parse(ontology_file, format='turtle')

    # Load and parse policy JSON-LD
    try:
        data_graph.parse(policy_file, format='json-ld')
    except Exception as e:
        print(f"Error parsing policy file: {e}")
        sys.exit(1)

    # Perform validation
    conforms, results_graph, results_text = validate(
        data_graph,
        shacl_graph=shapes_graph,
        inference='none',
        serialize_report_graph=True
    )

    # Output results
    print(f"Conformance: {'Success' if conforms else 'Failure'}")
    if not conforms:
        print("\nValidation Report:")
        print(results_text)

    return 0 if conforms else 1

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Validate a JSON-LD policy against SHACL shapes"
    )
    parser.add_argument(
        "shapes_file",
        help="Path to SHACL shapes file in Turtle format"
    )
    parser.add_argument(
        "policy_file",
        help="Path to policy file in JSON-LD format"
    )
    parser.add_argument(
        "--ontology",
        help="Path to ontology file in Turtle format (optional)",
        required=False
    )
    args = parser.parse_args()

    sys.exit(main(args.shapes_file, args.policy_file, args.ontology))