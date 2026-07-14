"""Tests for the Response Validator (SAGE_BLUEPRINT.md Section 28)."""
from app.agent.runtime.response_validator import ResponseValidator
from app.providers.base import ProviderResponse


def _response(content: str) -> ProviderResponse:
    return ProviderResponse(content=content, model="test-model", provider_name="test")


def test_normal_response_is_valid_with_no_warnings():
    result = ResponseValidator().validate(_response("Here's the answer."))
    assert result.is_valid is True
    assert result.warnings == []


def test_empty_response_is_invalid():
    """Section 28: empty responses must be caught."""
    result = ResponseValidator().validate(_response(""))
    assert result.is_valid is False
    assert result.warnings


def test_whitespace_only_response_is_invalid():
    """Edge case."""
    result = ResponseValidator().validate(_response("   \n  "))
    assert result.is_valid is False


def test_unavailable_capabilities_produce_a_warning_not_a_failure():
    result = ResponseValidator().validate(_response("I can't search the web yet."), ["web_search"])
    assert result.is_valid is True
    assert any("web_search" in w for w in result.warnings)


def test_unbalanced_code_fence_produces_a_warning():
    result = ResponseValidator().validate(_response("Here's some code:\n```python\nprint(1)"))
    assert result.is_valid is True
    assert any("code block" in w for w in result.warnings)


def test_balanced_code_fence_produces_no_warning():
    result = ResponseValidator().validate(_response("```python\nprint(1)\n```"))
    assert result.warnings == []
