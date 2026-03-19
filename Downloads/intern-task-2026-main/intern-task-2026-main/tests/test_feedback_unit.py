import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from app.models import FeedbackRequest, FeedbackResponse
from app.feedback import get_feedback

def _mock_completion(response_dict):
    """Helper to mock the OpenAI parsed response structure"""
    mock_parsed = FeedbackResponse(**response_dict)
    mock_msg = MagicMock()
    mock_msg.parsed = mock_parsed
    mock_choice = MagicMock()
    mock_choice.message = mock_msg
    mock_completion = MagicMock()
    mock_completion.choices = [mock_choice]
    return mock_completion

@pytest.mark.asyncio
async def test_feedback_with_errors():
    mock_response = {
        "corrected_sentence": "Yo fui al mercado ayer.",
        "is_correct": False,
        "errors": [
            {
                "original": "soy fue",
                "correction": "fui",
                "error_type": "conjugation",
                "explanation": "You mixed two verb forms.",
            }
        ],
        "difficulty": "A2",
    }

    with patch("app.feedback.AsyncOpenAI") as MockClient:
        instance = MockClient.return_value
        instance.beta.chat.completions.parse = AsyncMock(
            return_value=_mock_completion(mock_response)
        )

        request = FeedbackRequest(
            sentence="Yo soy fue al mercado ayer.",
            target_language="Spanish",
            native_language="English",
        )
        result = await get_feedback(request)

    assert result.is_correct is False
    assert result.corrected_sentence == "Yo fui al mercado ayer."
    assert len(result.errors) == 1
    assert result.errors[0].error_type == "conjugation"

@pytest.mark.asyncio
async def test_feedback_correct_sentence():
    mock_response = {
        "corrected_sentence": "Yo fui al mercado ayer.",
        "is_correct": True,
        "errors": [],
        "difficulty": "A2",
    }

    with patch("app.feedback.AsyncOpenAI") as MockClient:
        instance = MockClient.return_value
        instance.beta.chat.completions.parse = AsyncMock(
            return_value=_mock_completion(mock_response)
        )

        request = FeedbackRequest(
            sentence="Yo fui al mercado ayer.",
            target_language="Spanish",
            native_language="English",
        )
        result = await get_feedback(request)

    assert result.is_correct is True
    assert len(result.errors) == 0

@pytest.mark.asyncio
async def test_feedback_multiple_errors():
    mock_response = {
        "corrected_sentence": "Le chat noir est sur la table.",
        "is_correct": False,
        "errors": [
            {
                "original": "La chat",
                "correction": "Le chat",
                "error_type": "gender_agreement",
                "explanation": "'Chat' is masculine.",
            },
            {
                "original": "le table",
                "correction": "la table",
                "error_type": "gender_agreement",
                "explanation": "'Table' is feminine.",
            },
        ],
        "difficulty": "A1",
    }

    with patch("app.feedback.AsyncOpenAI") as MockClient:
        instance = MockClient.return_value
        instance.beta.chat.completions.parse = AsyncMock(
            return_value=_mock_completion(mock_response)
        )

        request = FeedbackRequest(
            sentence="La chat noir est sur le table.",
            target_language="French",
            native_language="English",
        )
        result = await get_feedback(request)

    assert result.is_correct is False
    assert len(result.errors) == 2
    assert all(e.error_type == "gender_agreement" for e in result.errors)