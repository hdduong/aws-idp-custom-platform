from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def load_validator():
    path = Path(__file__).resolve().parents[1] / "scripts" / "validate-repository.py"
    spec = importlib.util.spec_from_file_location("repository_validator", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_workflow_trigger_names_supports_all_github_yaml_forms() -> None:
    validator = load_validator()
    path = Path("workflow.yml")

    assert validator.workflow_trigger_names("pull_request", path) == {"pull_request"}
    assert validator.workflow_trigger_names(["push", "workflow_dispatch"], path) == {
        "push",
        "workflow_dispatch",
    }
    assert validator.workflow_trigger_names(
        {"pull_request_target": {"types": ["opened"]}}, path
    ) == {"pull_request_target"}


@pytest.mark.parametrize("value", [None, 17, ["push", 17], {17: {}}])
def test_workflow_trigger_names_rejects_invalid_values(value: object) -> None:
    validator = load_validator()

    with pytest.raises(ValueError):
        validator.workflow_trigger_names(value, Path("workflow.yml"))
