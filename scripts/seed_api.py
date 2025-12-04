#!/usr/bin/env python3
"""scripts/seed_api.py

Insère 5 persons et 3 projects dans l'API en local (/api/v1).
Usage: python scripts/seed_api.py --base-url http://localhost:8017

Le script ne lance pas le serveur. Il suppose que l'API est disponible à l'URL donnée.
"""
from __future__ import annotations
import os
import sys
import argparse
from typing import List, Optional

try:
    import requests
except Exception:  # pragma: no cover
    print("Le module 'requests' est requis. Installez-le: pip install requests")
    sys.exit(1)

DEFAULT_BASE = os.environ.get("BASE_URL", "http://localhost:8000")

PERSONS = [
    {
        "first_name": "Alice",
        "last_name": "Dupont",
        "personal_email": "alice.dupont@example.com",
        "position": "Engineer",
        "team": "Platform",
    },
    {
        "first_name": "Bob",
        "last_name": "Martin",
        "personal_email": "bob.martin@example.com",
        "position": "Product Owner",
        "team": "Products",
    },
    {
        "first_name": "Carla",
        "last_name": "Nguyen",
        "personal_email": "carla.nguyen@example.com",
        "position": "Lead Developer",
        "team": "Platform",
    },
    {
        "first_name": "David",
        "last_name": "Bernard",
        "personal_email": "david.bernard@example.com",
        "position": "Developer",
        "team": "Mobile",
    },
    {
        "first_name": "Eva",
        "last_name": "Moreau",
        "personal_email": "eva.moreau@example.com",
        "position": "QA",
        "team": "Quality",
    },
]

# Projects require lead_developer_id (int). We'll attach ids after creating persons.
PROJECTS = [
    {"name": "Site web v1", "description": "Refonte du site institutionnel"},
    {"name": "API interne", "description": "Mise en place d'une API interne pour services"},
    {"name": "Mobile app", "description": "Prototype d'application mobile"},
]


def post_json(url: str, payload: dict, timeout: int = 10) -> Optional[dict]:
    try:
        r = requests.post(url, json=payload, timeout=timeout)
        r.raise_for_status()
        try:
            return r.json()
        except ValueError:
            return {"raw_text": r.text}
    except requests.RequestException as e:
        print(f"Erreur requête POST {url}: {e}")
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed API with sample persons and projects")
    parser.add_argument("--base-url", default=DEFAULT_BASE, help="Base URL de l'API (ex: http://localhost:8000)")
    args = parser.parse_args()

    base = args.base_url.rstrip("/")
    persons_endpoint = f"{base}/api/v1/persons/"
    projects_endpoint = f"{base}/api/v1/projects/"

    created_persons: List[dict] = []

    print("Création des persons...")
    for p in PERSONS:
        resp = post_json(persons_endpoint, p)
        if resp is None:
            print(f"  ❌ Échec création person: {p.get('first_name')} {p.get('last_name')}")
            continue
        # Essayer d'extraire un identifiant commun: 'id' ou 'uuid' ou 'pk'
        pid = None
        if isinstance(resp, dict):
            for key in ("id", "uuid", "pk"):
                if key in resp:
                    pid = resp[key]
                    break
            # parfois l'API retourne l'objet créé sous une clé 'data' ou 'person'
            if pid is None:
                for container in ("data", "person", "result"):
                    if container in resp and isinstance(resp[container], dict):
                        for key in ("id", "uuid", "pk"):
                            if key in resp[container]:
                                pid = resp[container][key]
                                break
                        if pid is not None:
                            break
        created_persons.append({"sent": p, "resp": resp, "id": pid})
        print(f"  ✓ {p['first_name']} {p['last_name']} -> id={pid}")

    if not created_persons:
        print("Aucune person créée, arrêt.")
        return

    # Construire owner_id / lead_developer_id pour projets si possible
    person_ids = [c["id"] for c in created_persons if c["id"] is not None]
    if not person_ids:
        print("Aucun id de person récupéré, impossibilité de créer des projets qui requièrent lead_developer_id")
        return

    print("\nCréation des projects...")
    for idx, proj in enumerate(PROJECTS):
        payload = dict(proj)
        # assigner lead_developer_id cycliquement parmi les personnes créées
        payload["lead_developer_id"] = person_ids[idx % len(person_ids)]
        # optionnel: définir project_manager_id pour le second projet
        if idx == 1 and len(person_ids) > 1:
            payload["project_manager_id"] = person_ids[(idx + 1) % len(person_ids)]
        # optionnel: définir dev_line_id pour le premier projet
        if idx == 0 and len(person_ids) > 2:
            payload["dev_line_id"] = person_ids[(idx + 2) % len(person_ids)]

        resp = post_json(projects_endpoint, payload)
        if resp is None:
            print(f"  ❌ Échec création project: {proj.get('name')}")
            continue
        # extraire id si possible
        pid = None
        if isinstance(resp, dict):
            for key in ("id", "uuid", "pk"):
                if key in resp:
                    pid = resp[key]
                    break
        print(f"  ✓ {proj['name']} -> id={pid} (lead_developer_id={payload['lead_developer_id']})")

    print("\nRésumé:")
    print(f"  Persons envoyées: {len(PERSONS)}")
    print(f"  Persons créées (avec id): {sum(1 for c in created_persons if c['id'] is not None)}")
    print(f"  Projects envoyés: {len(PROJECTS)}")
    print("Terminé.")


if __name__ == "__main__":
    main()

