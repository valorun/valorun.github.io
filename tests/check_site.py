"""Contrôle statique du site : python3 tests/check_site.py (sans dépendance)."""

import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
EMAIL = "valorun@proton.me"


class Page(HTMLParser):
    def __init__(self, path: Path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.nodes: list[tuple[str, dict[str, str | None]]] = []
        self.ids: set[str] = set()
        self.text: list[str] = []
        self.json_data = ""
        self.in_json = False
        self.feed(path.read_text(encoding="utf-8"))
        self.close()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.nodes.append((tag, attrs))
        if identifier := attrs.get("id"):
            assert identifier not in self.ids, f"{self.path}: id dupliqué {identifier}"
            self.ids.add(identifier)
        if tag == "script":
            assert attrs.get("type") == "application/ld+json", "JavaScript inattendu"
            assert "src" not in attrs, "Script distant inattendu"
            self.in_json = True

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_json = False

    def handle_data(self, data):
        self.text.append(data)
        if self.in_json:
            self.json_data += data

    def elements(self, tag):
        return [attrs for name, attrs in self.nodes if name == tag]


pages = {ROOT / "index.html": Page(ROOT / "index.html"), ROOT / "en/index.html": Page(ROOT / "en/index.html")}
resources: set[Path] = set()


def local_reference(source: Path, reference: str) -> Path | None:
    url = urlsplit(reference)
    if url.scheme in {"http", "https"}:
        assert url.scheme == "https", f"Lien non chiffré : {reference}"
        return None
    if url.scheme == "mailto":
        assert url.path == EMAIL, f"Mauvais destinataire : {reference}"
        return None
    assert not url.scheme and not url.netloc, f"Protocole inattendu : {reference}"
    assert not url.path.startswith("/"), f"Chemin incompatible avec un dépôt Pages : {reference}"
    target = (source.parent / unquote(url.path)).resolve() if url.path else source
    if target.is_dir():
        target /= "index.html"
    assert target.is_relative_to(ROOT) and target.is_file(), f"Ressource absente : {source.name} → {reference}"
    resources.add(target)
    if url.fragment:
        if target in pages:
            identifiers = pages[target].ids
        else:
            assert target.suffix == ".svg", f"Fragment non vérifiable : {reference}"
            identifiers = {element.get("id") for element in ElementTree.parse(target).iter()}
        assert unquote(url.fragment) in identifiers, f"Ancre absente : {reference}"
    return target


for path, page in pages.items():
    expected_language = "en" if path.parent.name == "en" else "fr"
    assert page.elements("html")[0]["lang"] == expected_language
    for tag in ("title", "h1", "main"):
        assert len(page.elements(tag)) == 1, f"{path}: un seul {tag} attendu"
    assert "Valorun OÜ" in "".join(page.text)
    assert len(page.elements("h2")) == 5, f"{path}: section manquante"
    assert len(page.elements("article")) == 7, f"{path}: offre ou projet manquant"
    assert any(meta.get("name") == "description" and meta.get("content") for meta in page.elements("meta"))
    assert any(meta.get("name") == "viewport" for meta in page.elements("meta"))
    assert {"services", "experience", "approach", "about", "contact", "main-content"} <= page.ids
    organization = json.loads(page.json_data)
    assert organization["@type"] == "Organization" and organization["name"] == "Valorun OÜ"
    assert organization["founder"]["name"] == "Ronan Collier"
    assert organization["founder"]["sameAs"].endswith("/ronan-collier/")
    assert organization["email"] == f"mailto:{EMAIL}"

    alternates = {}
    for tag, attrs in page.nodes:
        assert not any(name.startswith("on") for name in attrs), "Gestionnaire JavaScript inattendu"
        for identifier in (attrs.get("aria-labelledby") or "").split():
            assert identifier in page.ids, f"Libellé absent : {identifier}"
        if tag == "img":
            assert "alt" in attrs and attrs.get("width") and attrs.get("height"), "Image sans alternative ou dimensions"
        reference = attrs.get("src") or attrs.get("href")
        if not reference:
            continue
        target = local_reference(path, reference)
        if tag in {"img", "use"} or (tag == "link" and attrs.get("rel") not in {"alternate", "canonical"}):
            assert target is not None, f"Ressource de rendu distante : {reference}"
        if tag == "link" and attrs.get("rel") == "alternate":
            alternates[attrs["hreflang"]] = target or reference
    assert set(alternates) == {"fr", "en", "x-default"}
    if all(isinstance(target, Path) for target in alternates.values()):
        assert alternates == {"fr": ROOT / "index.html", "en": ROOT / "en/index.html", "x-default": ROOT / "index.html"}
    else:
        assert all(isinstance(target, str) and target.startswith("https://") for target in alternates.values())
        assert alternates["fr"] == alternates["x-default"]
        assert urljoin(alternates["fr"], "en/") == alternates["en"], "URLs de langue incohérentes"
    current_language = [link for link in page.elements("a") if link.get("aria-current") == "page"]
    assert len(current_language) == 1 and current_language[0].get("lang") == expected_language
    assert sum(link.get("href", "").startswith(f"mailto:{EMAIL}") for link in page.elements("a")) >= 3
    assert {
        "https://github.com/valorun",
        "https://www.linkedin.com/in/ronan-collier/",
        "https://valorun.github.io/corvus-website/index.html",
        "https://clarius-robot.com/",
    } <= {link.get("href") for link in page.elements("a")}
    print(f"OK {path.relative_to(ROOT)} — langue, contenu, métadonnées, liens et accessibilité structurelle")

assert pages[ROOT / "index.html"].ids == pages[ROOT / "en/index.html"].ids, "Ancres FR/EN différentes"
css_path = ROOT / "assets/styles.css"
css = css_path.read_text(encoding="utf-8")
assert "@import" not in css, "Feuille de style importée inattendue"
for reference in re.findall(r"url\([\"']?([^\"')]+)", css):
    assert local_reference(css_path, reference), "Ressource CSS distante"
for licence in ("DM-Sans-OFL.txt", "Instrument-Serif-OFL.txt"):
    assert (ROOT / "assets/fonts" / licence).is_file(), f"Licence absente : {licence}"
assert (ROOT / ".nojekyll").is_file(), "Configuration GitHub Pages absente"
total = sum(path.stat().st_size for path in resources)
print(f"OK {len(resources)} ressources locales vérifiées — {total / 1024:.0f} Kio pour les deux pages et leurs ressources partagées")
