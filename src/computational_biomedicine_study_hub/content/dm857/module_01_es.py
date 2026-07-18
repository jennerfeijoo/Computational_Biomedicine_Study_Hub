"""Spain-localized public view of DM857 module 1 content."""

from __future__ import annotations

from dataclasses import replace

from .module_01_foundations import MODULE as _SOURCE_MODULE


def _localize_first_example() -> tuple:
    first, *remaining = _SOURCE_MODULE.worked_examples
    localized_first = replace(
        first,
        title="Calcular el rendimiento útil de un proceso de secuenciación",
        problem=(
            "Un proceso de secuenciación produce 48_000_000 lecturas. El 92.5 % supera "
            "el control de calidad. Calcular cuántas lecturas útiles se esperan y mostrar "
            "el resultado como entero."
        ),
    )
    return (localized_first, *remaining)


MODULE = replace(
    _SOURCE_MODULE,
    worked_examples=_localize_first_example(),
)

__all__ = ["MODULE"]
