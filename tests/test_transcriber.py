import os
from unittest.mock import MagicMock, patch

import pytest

from transcriber import transcribe_audio


def test_transcribe_audio_success(tmp_path):
    """Test successful audio transcription."""

    audio_file = tmp_path / "test_audio.mp3"
    audio_file.write_bytes(b"fake audio data")

    mock_transcription = "Hello, this is a test transcription."

    with patch("transcriber.Groq") as mock_groq:
        mock_client = MagicMock()
        mock_groq.return_value = mock_client

        mock_client.audio.transcriptions.create.return_value = mock_transcription

        with patch.dict(os.environ, {"GROQ_API_KEY": "test-api-key"}):
            result = transcribe_audio(str(audio_file))

        assert result == mock_transcription

        mock_groq.assert_called_once_with(api_key="test-api-key")

        mock_client.audio.transcriptions.create.assert_called_once_with(
            file=("test_audio.mp3", b"fake audio data"),
            model="whisper-large-v3-turbo",
            response_format="text",
        )


def test_missing_api_key(tmp_path):
    """Test that ValueError is raised when GROQ_API_KEY is missing."""

    audio_file = tmp_path / "test_audio.mp3"
    audio_file.write_bytes(b"fake audio data")

    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="GROQ_API_KEY is missing"):
            transcribe_audio(str(audio_file))


def test_audio_file_not_found():
    """Test that FileNotFoundError is raised for a missing audio file."""

    with patch.dict(os.environ, {"GROQ_API_KEY": "test-api-key"}):
        with pytest.raises(
            FileNotFoundError,
            match="Audio file not found",
        ):
            transcribe_audio("nonexistent_audio.mp3")


def test_transcribe_empty_audio_file(tmp_path):
    """Test transcription when the audio file is empty."""

    audio_file = tmp_path / "empty.mp3"
    audio_file.write_bytes(b"")

    mock_transcription = ""

    with patch("transcriber.Groq") as mock_groq:
        mock_client = MagicMock()
        mock_groq.return_value = mock_client

        mock_client.audio.transcriptions.create.return_value = mock_transcription

        with patch.dict(os.environ, {"GROQ_API_KEY": "test-api-key"}):
            result = transcribe_audio(str(audio_file))

        assert result == ""