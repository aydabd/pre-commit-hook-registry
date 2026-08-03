"""Deterministic Markdown catalog reference generation."""

from pathlib import Path

from pre_commit_hook_registry.models import Catalog


def render_catalog(catalog: Catalog) -> str:
    """Render the public catalog reference as Markdown."""
    lines = ["# Curated hook catalog\n", "<!-- Generated; edit catalog data instead. -->\n\n"]
    for upstream in sorted(catalog.upstreams, key=lambda item: item.name):
        lines.extend(
            [
                f"## {upstream.name}\n\n",
                f"- Upstream: [{upstream.url}]({upstream.url})\n",
                f"- Reviewed tag: `{upstream.tag}`\n",
                f"- Commit: `{upstream.sha}`\n",
                f"- License: `{upstream.license}`\n",
                f"- Adapter: `{upstream.runtime_adapter}`\n",
                f"- Review: [{upstream.review_record}](../{upstream.review_record})\n",
                "- Hook IDs: " + ", ".join(f"`{item}`" for item in upstream.approved_ids) + "\n\n",
            ]
        )
    return "".join(lines)


def generate_catalog_document(output_path: Path) -> None:
    """Write the packaged catalog's generated Markdown reference."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_catalog(Catalog.load()), encoding="utf-8")
