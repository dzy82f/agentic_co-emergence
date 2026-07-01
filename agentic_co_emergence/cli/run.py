"""
python -m agentic_co_emergence.cli.run

Practical command-line runner for Agentic Co-Emergence v0.1.

Usage:
    python python -m agentic_co_emergence.cli.run "What should ethical governance look like?"

Optional:
    python python -m agentic_co_emergence.cli.run "Question here" --session my-session
    python python -m agentic_co_emergence.cli.run "Question here" --reset-memory
    python python -m agentic_co_emergence.cli.run "Question here" --max-steps 40

This script assumes it sits in the same folder as runtime_controller.py.
"""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path

from agentic_co_emergence.core.runtime_controller import RuntimeController


def safe_session_id(question: str) -> str:
    """
    Create a readable session id from the question plus timestamp.
    """
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", question.lower()).strip("-")
    slug = slug[:60] or "tychevia-session"
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{slug}-{timestamp}"


def write_report(session_id: str, final_result, output_dir: Path) -> Path:
    """
    Write a simple markdown report from the final runtime projections.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{session_id}_report.md"

    p = final_result.projection
    memory = final_result.memory_projection
    semantic = final_result.semantic_projection

    lines = []
    lines.append(f"# Agentic Co-Emergence Runtime Report")
    lines.append("")
    lines.append(f"**Session:** `{session_id}`")
    lines.append(f"**Final state:** `{p['state']}`")
    lines.append(f"**Completed rounds:** {p['completed_rounds']}")
    lines.append("")
    lines.append("## Issue")
    lines.append("")
    issue = p.get("issue", {})
    lines.append(issue.get("framed_question") or issue.get("raw_user_question") or "")
    lines.append("")
    lines.append("## Organisational Memory")
    lines.append("")
    lines.append(f"- Memory objects: {len(memory.get('objects', {}))}")
    lines.append(f"- Indexed sessions: {len(memory.get('indexed_sessions', []))}")
    lines.append("")
    lines.append("## Top Memory Objects")
    lines.append("")

    objects = list(memory.get("objects", {}).values())
    objects.sort(key=lambda obj: obj.get("confidence", 0), reverse=True)

    for obj in objects[:12]:
        lines.append(
            f"- **{obj.get('kind')}** "
            f"`{obj.get('id')}` "
            f"(confidence={obj.get('confidence')}, mentions={obj.get('mentions')})"
        )
        lines.append(f"  - {obj.get('text')}")
        lines.append("")

    lines.append("## Semantic Graph")
    lines.append("")
    lines.append(f"- Nodes: {len(semantic.get('nodes', {}))}")
    lines.append(f"- Edges: {len(semantic.get('edges', {}))}")
    lines.append(f"- Clusters: {len(semantic.get('clusters', {}))}")
    lines.append("")

    if semantic.get("clusters"):
        lines.append("### Clusters")
        lines.append("")
        clusters = list(semantic["clusters"].values())
        clusters.sort(key=lambda c: c.get("size", 0), reverse=True)
        for cluster in clusters:
            lines.append(f"- **{cluster.get('concept')}** — size {cluster.get('size')}")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a Agentic Co-Emergence v0.1 session from a single question."
    )
    parser.add_argument(
        "question",
        help="The issue or question for Tychevia to discuss.",
    )
    parser.add_argument(
        "--session",
        default=None,
        help="Optional session id. If omitted, one is created automatically.",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=40,
        help="Maximum number of runtime steps before stopping.",
    )
    parser.add_argument(
        "--reset-memory",
        action="store_true",
        help="Reset organisational memory before running. Use with care.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Reduce console output.",
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Do not write a markdown report.",
    )

    args = parser.parse_args()

    session_id = args.session or safe_session_id(args.question)

    # ChatGPTAdapter requires OPENAI_API_KEY.
    import os
    if not os.getenv("OPENAI_API_KEY"):
        print()
        print("OPENAI_API_KEY is not set.")
        print("Set it first, for example:")
        print('  $env:OPENAI_API_KEY="sk-..."')
        print()
        print("You can also create a .env file containing:")
        print("  OPENAI_API_KEY=sk-...")
        return 1

    controller = RuntimeController(session_id)
    controller.reset_session()

    if args.reset_memory:
        controller.reset_memory()

    print()
    print("Agentic Co-Emergence v0.1")
    print("=" * 72)
    print(f"Session: {session_id}")
    print(f"Issue: {args.question}")
    print("=" * 72)

    final_result = None

    for step in range(1, args.max_steps + 1):
        if step == 1:
            result = controller.run_next_step(args.question)
        else:
            result = controller.run_next_step()

        final_result = result
        p = result.projection
        kp = result.knowledge_projection
        mp = result.memory_projection
        sp = result.semantic_projection

        if not args.quiet:
            print()
            print("-" * 72)
            print(f"STEP {step}: {result.status}")
            print(f"STATE: {p['state']}")
            print(f"ROUND: {p['current_round']} | COMPLETED: {p['completed_rounds']}")
            print(f"NEXT SPEAKER: {p['current_speaker']}")
            print(
                f"KNOWLEDGE: {len(kp['objects'])} objects | "
                f"MEMORY: {len(mp['objects'])} objects | "
                f"SEMANTIC: {len(sp['nodes'])} nodes, {len(sp['edges'])} edges"
            )
            if result.output:
                print()
                print(result.output)

        if result.status == "rejected":
            print()
            print("Runtime rejected model output.")
            print(f"Reason: {result.reason}")
            return 1

        if p["state"] == "ARCHIVE":
            print()
            print("=" * 72)
            print("SESSION COMPLETE")
            print("=" * 72)
            print(f"Completed rounds: {p['completed_rounds']}")
            print(f"Knowledge objects: {len(kp['objects'])}")
            print(f"Memory objects: {len(mp['objects'])}")
            print(f"Semantic nodes: {len(sp['nodes'])}")
            print(f"Semantic edges: {len(sp['edges'])}")
            print(f"Semantic clusters: {len(sp['clusters'])}")
            break

    if final_result is None:
        print("No runtime steps executed.")
        return 1

    if final_result.projection["state"] != "ARCHIVE":
        print()
        print("Stopped before ARCHIVE.")
        print(f"Final state: {final_result.projection['state']}")

    if not args.no_report:
        report_path = write_report(
            session_id=session_id,
            final_result=final_result,
            output_dir=Path("runtime_reports"),
        )
        print()
        print(f"Report written to: {report_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
