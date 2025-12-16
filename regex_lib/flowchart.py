import json
import sys
import argparse
import math


def main():
    parser = argparse.ArgumentParser(
        description="Generate SVG image for automata from JSON"
    )
    parser.add_argument("--output", default="flowchart.svg", help="Output SVG file")
    args = parser.parse_args()

    data = json.load(sys.stdin)
    states = sorted(data["states"])
    transitions = data["transitions"]
    start = data["start"]
    accept = set(data["accept"])

    # Simple layout: states in a circle
    n = len(states)
    radius = 100
    center_x, center_y = 200, 200
    positions = {}
    for i, s in enumerate(states):
        angle = 2 * math.pi * i / n
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        positions[s] = (x, y)

    svg = []
    svg.append('<svg width="400" height="400" xmlns="http://www.w3.org/2000/svg">')

    # Edges
    for s, trans in transitions.items():
        s = int(s)
        sx, sy = positions[s]
        for sym, targets in trans.items():
            label = sym if sym != "" else "ε"
            if isinstance(targets, list):  # NFA
                for t in targets:
                    tx, ty = positions[t]
                    if s == t:
                        # Self-loop
                        svg.append(
                            f'<ellipse cx="{sx}" cy="{sy - 20}" rx="15" ry="10" fill="none" stroke="black" stroke-width="2"/>'
                        )
                        svg.append(
                            f'<text x="{sx}" y="{sy - 30}" text-anchor="middle" font-size="12">{label}</text>'
                        )
                    else:
                        svg.append(
                            f'<line x1="{sx}" y1="{sy}" x2="{tx}" y2="{ty}" stroke="black" stroke-width="2"/>'
                        )
                        # Label in middle
                        mx, my = (sx + tx) / 2, (sy + ty) / 2
                        svg.append(
                            f'<text x="{mx}" y="{my}" text-anchor="middle" font-size="12">{label}</text>'
                        )
            else:  # DFA
                tx, ty = positions[targets]
                if s == targets:
                    # Self-loop
                    svg.append(
                        f'<ellipse cx="{sx}" cy="{sy - 20}" rx="15" ry="10" fill="none" stroke="black" stroke-width="2"/>'
                    )
                    svg.append(
                        f'<text x="{sx}" y="{sy - 30}" text-anchor="middle" font-size="12">{label}</text>'
                    )
                else:
                    svg.append(
                        f'<line x1="{sx}" y1="{sy}" x2="{tx}" y2="{ty}" stroke="black" stroke-width="2"/>'
                    )
                    mx, my = (sx + tx) / 2, (sy + ty) / 2
                    svg.append(
                        f'<text x="{mx}" y="{my}" text-anchor="middle" font-size="12">{label}</text>'
                    )

    # Nodes
    for s in states:
        x, y = positions[s]
        fill = "green" if s == start else "lightblue"
        stroke = "red" if s in accept else "black"
        stroke_width = "4" if s in accept else "2"
        svg.append(
            f'<circle cx="{x}" cy="{y}" r="20" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
        )
        svg.append(
            f'<text x="{x}" y="{y + 5}" text-anchor="middle" font-size="14" fill="black">{s}</text>'
        )

    svg.append("</svg>")

    with open(args.output, "w") as f:
        f.write("\n".join(svg))

    print(f"SVG image saved to {args.output}")


if __name__ == "__main__":
    main()
