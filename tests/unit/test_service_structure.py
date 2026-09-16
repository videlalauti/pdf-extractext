"""Structural tests: verify each microservice has the expected layered modules."""

import os


def test_validation_service_has_routes_module():
    assert os.path.exists("services/validation-service/routes.py")


def test_extraction_service_has_routes_module():
    assert os.path.exists("services/extraction-service/routes.py")


def test_persistence_service_has_repository():
    assert os.path.exists("services/persistence-service/repository.py") or os.path.exists(
        "services/persistence-service/persistence/repository.py"
    )
