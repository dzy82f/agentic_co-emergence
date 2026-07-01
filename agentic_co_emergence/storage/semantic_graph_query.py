class SemanticGraphQuery:
    def __init__(self, graph):
        self.graph=graph
    def neighbours(self,node_id):
        edges=[e for e in self.graph.edges.values() if e.get("from")==node_id or e.get("to")==node_id]
        return edges
    def by_relation(self,relation):
        return [e for e in self.graph.edges.values() if e.get("relation")==relation]
    def clusters(self):
        return sorted(self.graph.clusters.values(),key=lambda c:c.get("size",0),reverse=True)
    def trace(self,node_id):
        lines=[]
        node=self.graph.nodes.get(node_id)
        if node: lines.append(f"{node_id} | {node['kind']} | {node['text']}")
        for e in self.neighbours(node_id):
            other=e["to"] if e["from"]==node_id else e["from"]
            other_node=self.graph.nodes.get(other,{})
            direction="-->" if e["from"]==node_id else "<--"
            lines.append(f"  {direction} {e['relation']} {other} | {other_node.get('kind')} | {other_node.get('text')}")
        return lines
