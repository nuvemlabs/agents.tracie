"""Tests for core agent functionality."""

from unittest.mock import patch

import pytest

from agent.core import create_agent, create_search_tool, run


def test_run_with_empty_input():
    """Test that empty input returns appropriate message."""
    result = run("")
    assert "Please provide a valid query" in result


def test_run_with_whitespace_input():
    """Test that whitespace-only input returns appropriate message."""
    result = run("   ")
    assert "Please provide a valid query" in result


@patch("agent.core.settings")
def test_create_search_tool_without_api_key(mock_settings):
    """Test search tool creation when API key is missing."""
    mock_settings.serpapi_api_key = None
    tool = create_search_tool()
    assert tool is None


@patch("agent.core.settings")
@patch("agent.core.SerpAPIWrapper")
def test_create_search_tool_with_api_key(mock_serp, mock_settings):
    """Test search tool creation when API key is available."""
    mock_settings.serpapi_api_key = "test_key"
    tool = create_search_tool()
    assert tool is not None
    assert tool.name == "search"


@patch("agent.core.settings")
def test_create_agent(mock_settings):
    """Test agent creation."""
    mock_settings.openai_api_key = "test_key"
    mock_settings.model_name = "gpt-3.5-turbo"
    mock_settings.model_temperature = 0.0
    mock_settings.model_max_tokens = 2000
    mock_settings.agent_verbose = True
    mock_settings.serpapi_api_key = None

    agent = create_agent()
    assert agent is not None


def test_run_basic_query():
    """Test running a basic query (integration test - requires API key)."""
    # This test requires actual API keys to run
    # Skip if not in integration test environment
    from agent.settings import settings

    if (
        not settings.openai_api_key
        or settings.openai_api_key == "test-api-key-for-testing"
    ):
        pytest.skip("Integration test requires real OPENAI_API_KEY")

    # Use a simpler question that doesn't require tools
    result = run("Hello, how are you?")
    assert isinstance(result, str)
    assert len(result) > 0
    # Check that we get some kind of response (not an error)
    assert not result.startswith("Error:")
    # The response should contain typical greeting/response words
    assert any(
        word in result.lower()
        for word in ["hello", "hi", "good", "well", "fine", "how", "assistant", "help"]
    )
