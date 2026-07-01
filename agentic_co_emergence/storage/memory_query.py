class MemoryQuery:
    def __init__(self, memory_projection): self.memory=memory_projection
    def search(self,text):
        q=text.lower().split()
        out=[]
        for o in self.memory.objects.values():
            hay=f"{o.get('kind','')} {o.get('text','')}".lower()
            if all(t in hay for t in q): out.append(o)
        return sorted(out,key=lambda o:o.get("confidence",0),reverse=True)
    def top(self,n=10): return sorted(self.memory.objects.values(),key=lambda o:o.get("confidence",0),reverse=True)[:n]
