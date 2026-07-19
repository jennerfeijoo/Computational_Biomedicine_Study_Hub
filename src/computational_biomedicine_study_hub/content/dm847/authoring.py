"""DM847-local access to the validated trilingual authoring helpers.

The helpers currently live in the DM857 package. This compatibility layer keeps
DM847 modules independent from that implementation detail and provides one place
for a later move to a shared content-level authoring module.
"""

from ..dm857.authoring import (
    Triple,
    authored_item,
    concept,
    example,
    objective,
    objective_mcq,
    objective_tf,
    option,
    practice,
    same,
    t,
    tutor_support,
)

__all__ = [
    "Triple",
    "authored_item",
    "concept",
    "example",
    "objective",
    "objective_mcq",
    "objective_tf",
    "option",
    "practice",
    "same",
    "t",
    "tutor_support",
]
