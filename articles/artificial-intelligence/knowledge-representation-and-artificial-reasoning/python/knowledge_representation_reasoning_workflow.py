"""
Knowledge Representation and Artificial Reasoning Mini-Workflow

This script demonstrates:
- symbolic facts as triples
- simple inference rules
- forward chaining
- explanation traces

It is educational and does not require private data.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import pandas as pd


OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

Fact = tuple[str, str, str]


@dataclass(frozen=True)
class Rule:
    """A simple forward-chaining rule."""
    name: str
    apply: Callable[[set[Fact]], set[Fact]]


def subclass_inheritance(facts: set[Fact]) -> set[Fact]:
    """Infer class membership through subclass relations."""
    inferred: set[Fact] = set()

    memberships = [
        (entity, parent_class)
        for entity, predicate, parent_class in facts
        if predicate == "isA"
    ]

    subclass_edges = [
        (child_class, parent_class)
        for child_class, predicate, parent_class in facts
        if predicate == "subClassOf"
    ]

    for entity, entity_class in memberships:
        for child_class, parent_class in subclass_edges:
            if entity_class == child_class:
                inferred.add((entity, "isA", parent_class))

    return inferred


def transitive_subclass(facts: set[Fact]) -> set[Fact]:
    """Infer transitive subclass relationships."""
    inferred: set[Fact] = set()

    subclass_edges = [
        (child_class, parent_class)
        for child_class, predicate, parent_class in facts
        if predicate == "subClassOf"
    ]

    for child, middle in subclass_edges:
        for possible_middle, parent in subclass_edges:
            if middle == possible_middle:
                inferred.add((child, "subClassOf", parent))

    return inferred


def forward_chain(initial_facts: set[Fact], rules: list[Rule], max_steps: int = 20):
    """Apply rules until no new facts are inferred."""
    facts = set(initial_facts)
    trace: list[dict] = []

    for step in range(max_steps):
        new_facts: set[Fact] = set()

        for rule in rules:
            inferred = rule.apply(facts) - facts

            for fact in inferred:
                trace.append(
                    {
                        "step": step,
                        "rule": rule.name,
                        "subject": fact[0],
                        "predicate": fact[1],
                        "object": fact[2],
                    }
                )

            new_facts.update(inferred)

        if not new_facts:
            break

        facts.update(new_facts)

    return facts, trace


def main() -> None:
    initial_facts: set[Fact] = {
        ("Socrates", "isA", "Human"),
        ("Human", "subClassOf", "Mortal"),
        ("Mortal", "subClassOf", "Entity"),
        ("AI Governance", "requires", "Auditability"),
        ("Knowledge Representation", "supports", "Auditability"),
    }

    rules = [
        Rule("subclass_inheritance", subclass_inheritance),
        Rule("transitive_subclass", transitive_subclass),
    ]

    all_facts, explanation_trace = forward_chain(initial_facts, rules)

    facts_table = pd.DataFrame(
        [
            {"subject": s, "predicate": p, "object": o}
            for s, p, o in sorted(all_facts)
        ]
    )

    trace_table = pd.DataFrame(explanation_trace)

    facts_table.to_csv(OUTPUT_DIR / "inferred_facts.csv", index=False)
    trace_table.to_csv(OUTPUT_DIR / "reasoning_trace.csv", index=False)

    print("All inferred facts:")
    print(facts_table)
    print()
    print("Reasoning trace:")
    print(trace_table)


if __name__ == "__main__":
    main()
