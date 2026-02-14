"""
Code Generator: draw.io XML -> Java Source Files

This script parses a draw.io (.drawio) XML file containing a Class Diagram-like
model and generates corresponding Java source code files.

Translational Semantics:
    Rectangle (vertex)                -> Java class
    Arrow with empty triangle head    -> extends (inheritance)
    Simple arrow with label "name (1)" -> private single-reference field
    Simple arrow with label "name (N)" -> private List<T> field

Usage:
    python codegen.py <input.drawio> <output_directory>
"""

import xml.etree.ElementTree as ET
import os
import sys
import re


def strip_html(text):
    """
    Strip HTML tags from a string.
    draw.io sometimes wraps text in HTML elements like <p style="...">Text</p>.
    """
    if not text:
        return text
    clean = re.sub(r'<[^>]+>', '', text)
    return clean.strip()


def parse_drawio(file_path):
    """
    Parse a draw.io XML file and extract classes and relationships.

    Algorithm:
    1. Parse the XML tree.
    2. Iterate over all mxCell elements.
    3. Identify vertices (rectangles) by the vertex="1" attribute -> these are classes.
    4. Identify edges (arrows) by the edge="1" attribute -> these are relationships.
    5. For edges, determine the type:
       a. If the style contains "endArrow=block;endFill=0" or "shape=flexArrow" -> inheritance.
       b. Otherwise -> association (directed relationship).
    6. For associations, parse the label to extract the relationship name and cardinality.
    7. Return structured data: a dict of classes and a list of relationships.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    classes = {}        # id -> class_name
    associations = []   # list of {source, target, name, cardinality}
    inheritances = []   # list of {child, parent}

    # Find all mxCell elements anywhere in the XML tree
    for cell in root.iter("mxCell"):
        cell_id = cell.get("id")
        value = strip_html(cell.get("value", ""))
        style = cell.get("style", "")
        source = cell.get("source")
        target = cell.get("target")

        # Skip root and default layer cells
        if cell_id in ("0", "1"):
            continue

        # Identify vertices (rectangles = classes)
        # Skip edge labels: they have vertex="1" but also connectable="0"
        if cell.get("vertex") == "1" and cell.get("connectable") != "0":
            if value.strip():
                classes[cell_id] = value.strip()

        # Identify edges (arrows = relationships)
        elif cell.get("edge") == "1":
            if source and target:
                # Check if this is an inheritance arrow (empty triangle head)
                if ("endArrow=block" in style and "endFill=0" in style) or "shape=flexArrow" in style:
                    inheritances.append({
                        "child": source,
                        "parent": target
                    })
                else:
                    # This is an association - parse label for name and cardinality
                    name, cardinality = parse_label(value)
                    associations.append({
                        "source": source,
                        "target": target,
                        "name": name,
                        "cardinality": cardinality
                    })

        # Check for edge labels (connectable="0" children of edges)
        elif cell.get("connectable") == "0" and value.strip():
            # This is a label on an edge - find the parent edge
            parent_id = cell.get("parent")
            if parent_id:
                # Update the association that has this parent edge
                for assoc in associations:
                    pass  # Labels on edges with value on the edge cell itself
                # If the parent edge didn't have a value, we need to add it
                # We handle this by checking if any association's edge matches
                name, cardinality = parse_label(value)
                # Find the parent edge and update
                for edge_cell in root.iter("mxCell"):
                    if edge_cell.get("id") == parent_id and edge_cell.get("edge") == "1":
                        src = edge_cell.get("source")
                        tgt = edge_cell.get("target")
                        if src and tgt:
                            # Check if we already have this association
                            found = False
                            for assoc in associations:
                                if assoc["source"] == src and assoc["target"] == tgt:
                                    # Update with label info if the association has no name
                                    if not assoc["name"]:
                                        assoc["name"] = name
                                        assoc["cardinality"] = cardinality
                                    found = True
                                    break
                            if not found:
                                edge_style = edge_cell.get("style", "")
                                if not ("endArrow=block" in edge_style and "endFill=0" in edge_style):
                                    associations.append({
                                        "source": src,
                                        "target": tgt,
                                        "name": name,
                                        "cardinality": cardinality
                                    })
                        break

    return classes, associations, inheritances


def parse_label(label):
    """
    Parse a relationship label like "drives (1)" or "has (N)" into
    a name and cardinality.

    Returns: (name, cardinality) where cardinality is "1" or "N".
    """
    if not label or not label.strip():
        return ("", "1")

    label = label.strip()

    # Match pattern: "name (cardinality)"
    match = re.match(r"^(.+?)\s*\((\w+)\)\s*$", label)
    if match:
        name = match.group(1).strip()
        cardinality = match.group(2).strip().upper()
        return (name, cardinality)

    # If no cardinality in parentheses, treat the whole label as the name
    return (label, "1")


def to_java_class_name(name):
    """
    Convert a name to a valid Java class name (PascalCase).
    E.g., "Licence plate" -> "LicencePlate"
    """
    parts = name.split()
    return "".join(word.capitalize() for word in parts)


def to_java_field_name(name):
    """
    Convert a relationship name to a valid Java field name (camelCase).
    E.g., "drives" -> "drives", "enrolled in" -> "enrolledIn"
    """
    parts = name.lower().split()
    if not parts:
        return "ref"
    result = parts[0]
    for part in parts[1:]:
        result += part.capitalize()
    return result


def generate_java(classes, associations, inheritances, output_dir):
    """
    Generate Java source files from the parsed model.

    Algorithm:
    1. For each class, determine:
       a. Its parent class (from inheritances).
       b. Its outgoing associations (fields it needs).
    2. Generate a Java file for each class with:
       a. Import statements (java.util.List, java.util.ArrayList if needed).
       b. Class declaration with optional extends.
       c. Private fields for each outgoing association.
       d. A default constructor.
       e. Getters and setters for all fields.
    3. Write each file to the output directory.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Build a map of child_id -> parent_id for inheritance
    parent_map = {}
    for inh in inheritances:
        parent_map[inh["child"]] = inh["parent"]

    # Build a map of source_id -> list of associations
    assoc_map = {}
    for assoc in associations:
        src = assoc["source"]
        if src not in assoc_map:
            assoc_map[src] = []
        assoc_map[src].append(assoc)

    generated_files = []

    for class_id, class_name in classes.items():
        java_class_name = to_java_class_name(class_name)
        outgoing = assoc_map.get(class_id, [])
        parent_id = parent_map.get(class_id)
        parent_class_name = to_java_class_name(classes[parent_id]) if parent_id and parent_id in classes else None

        # Determine if we need List import
        needs_list = any(a["cardinality"] == "N" for a in outgoing)

        lines = []

        # Import statements
        if needs_list:
            lines.append("import java.util.ArrayList;")
            lines.append("import java.util.List;")
            lines.append("")

        # Class declaration
        class_decl = f"public class {java_class_name}"
        if parent_class_name:
            class_decl += f" extends {parent_class_name}"
        class_decl += " {"
        lines.append(class_decl)

        # Fields - derive field names from the target class name to avoid
        # duplicate names (e.g., two "has" associations from the same class).
        # For cardinality N, pluralize the name. For cardinality 1, use camelCase.
        fields = []
        used_field_names = set()
        for assoc in outgoing:
            target_id = assoc["target"]
            if target_id not in classes:
                continue
            target_class = to_java_class_name(classes[target_id])
            cardinality = assoc["cardinality"]

            # Derive field name from target class (standard Java convention)
            base_field_name = target_class[0].lower() + target_class[1:]
            if cardinality == "N":
                field_name = base_field_name + "s"
                field_type = f"List<{target_class}>"
            else:
                field_name = base_field_name
                field_type = target_class

            # Handle duplicate field names
            if field_name in used_field_names:
                field_name = field_name + "2"
            used_field_names.add(field_name)

            fields.append((field_type, field_name, target_class, cardinality == "N"))

        if fields:
            lines.append("")
            for field_type, field_name, _, _ in fields:
                lines.append(f"    private {field_type} {field_name};")

        # Constructor
        lines.append("")
        lines.append(f"    public {java_class_name}() {{")
        for field_type, field_name, target_class, is_list in fields:
            if is_list:
                lines.append(f"        this.{field_name} = new ArrayList<>();")
        lines.append("    }")

        # Getters and Setters
        for field_type, field_name, target_class, is_list in fields:
            capitalized = field_name[0].upper() + field_name[1:]
            lines.append("")

            # Getter
            lines.append(f"    public {field_type} get{capitalized}() {{")
            lines.append(f"        return this.{field_name};")
            lines.append("    }")

            # Setter
            lines.append("")
            lines.append(f"    public void set{capitalized}({field_type} {field_name}) {{")
            lines.append(f"        this.{field_name} = {field_name};")
            lines.append("    }")

            # Add method for lists
            if is_list:
                singular = field_name.rstrip("s") if field_name.endswith("s") else field_name
                param_name = singular if singular != field_name else "item"
                lines.append("")
                lines.append(f"    public void add{target_class}({target_class} {param_name}) {{")
                lines.append(f"        this.{field_name}.add({param_name});")
                lines.append("    }")

        lines.append("}")
        lines.append("")

        # Write file
        file_path = os.path.join(output_dir, f"{java_class_name}.java")
        with open(file_path, "w") as f:
            f.write("\n".join(lines))

        generated_files.append(file_path)
        print(f"  Generated: {java_class_name}.java")

    return generated_files


def main():
    if len(sys.argv) < 3:
        print("Usage: python codegen.py <input.drawio> <output_directory>")
        print("Example: python codegen.py car.drawio examples/default/src-gen")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)

    print(f"Parsing model: {input_file}")
    classes, associations, inheritances = parse_drawio(input_file)

    print(f"Found {len(classes)} classes, {len(associations)} associations, {len(inheritances)} inheritance relationships.")
    print()

    print("Classes:")
    for cid, cname in classes.items():
        print(f"  - {cname}")

    print("\nAssociations:")
    for assoc in associations:
        src_name = classes.get(assoc["source"], "?")
        tgt_name = classes.get(assoc["target"], "?")
        print(f"  - {src_name} --{assoc['name']} ({assoc['cardinality']})--> {tgt_name}")

    print("\nInheritance:")
    for inh in inheritances:
        child_name = classes.get(inh["child"], "?")
        parent_name = classes.get(inh["parent"], "?")
        print(f"  - {child_name} extends {parent_name}")

    print(f"\nGenerating Java code to: {output_dir}")
    generated = generate_java(classes, associations, inheritances, output_dir)
    print(f"\nDone! Generated {len(generated)} Java files.")


if __name__ == "__main__":
    main()
