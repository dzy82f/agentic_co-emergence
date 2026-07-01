from agentic_co_emergence.core.runtime_controller import RuntimeController

def run_session(session_id, reset_memory=False):
    c=RuntimeController(session_id)
    c.reset_session()
    if reset_memory: c.reset_memory()
    q="What should ethical governance look like when technological systems outrun institutions?"
    for i in range(40):
        r=c.run_next_step(q if i==0 else None)
        p,kp,mp,sp=r.projection,r.knowledge_projection,r.memory_projection,r.semantic_projection
        print("="*72)
        print(f"{session_id} | STEP {i+1}: {r.status}")
        print(r.output)
        print(f"STATE: {p['state']} | ROUND: {p['current_round']} | COMPLETED: {p['completed_rounds']}")
        print(f"KNOWLEDGE OBJECTS: {len(kp['objects'])} | MEMORY OBJECTS: {len(mp['objects'])} | SEMANTIC NODES: {len(sp['nodes'])} | EDGES: {len(sp['edges'])} | CLUSTERS: {len(sp['clusters'])}")
        if r.semantic_events:
            print("SEMANTIC EVENTS THIS STEP:")
            for e in r.semantic_events:
                print(f"  - {e['event_type']} | {e.get('semantic_id')}")
        if p["state"]=="ARCHIVE": break

def main():
    run_session("demo-session-v5-a", reset_memory=True)
    print("\n\nSECOND SESSION: reinforces memory and semantic graph\n")
    run_session("demo-session-v5-b", reset_memory=False)

if __name__=="__main__":
    main()
