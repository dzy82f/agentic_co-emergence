class SemanticFeedback:
    """
    Converts semantic graph state into compact prompt feedback.
    """

    def __init__(self, semantic_projection, max_items: int = 8):
        self.semantic_projection = semantic_projection
        self.max_items = max_items

    def build(self) -> str:
        nodes = list(self.semantic_projection.nodes.values())
        edges = list(self.semantic_projection.edges.values())
        clusters = list(self.semantic_projection.clusters.values())

        if not nodes and not edges and not clusters:
            return "[No semantic memory available yet.]"

        lines = []

        if clusters:
            lines.append("Key semantic clusters:")
            clusters = sorted(clusters, key=lambda c: c.get("size", 0), reverse=True)
            for cluster in clusters[:self.max_items]:
                lines.append(f"- {cluster.get('concept')} (size={cluster.get('size')})")

        if nodes:
            lines.append("")
            lines.append("High-confidence memory nodes:")
            nodes = sorted(nodes, key=lambda n: n.get("confidence", 0), reverse=True)
            for node in nodes[:self.max_items]:
                lines.append(f"- {node.get('kind')}: {node.get('text')}")

        if edges:
            lines.append("")
            lines.append("Relevant semantic relations:")
            for edge in edges[:self.max_items]:
                lines.append(
                    f"- {edge.get('from')} --{edge.get('relation')}--> {edge.get('to')}"
                )

        return "\n".join(lines).strip()
