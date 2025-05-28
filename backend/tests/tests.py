import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from telegram import Update, Message
from telegram.ext import ContextTypes, MessageHandler, filters, Application

import bot_server
from backend.app.handlers.logging_handler import log_update_json, register_logging
from backend.app.services.yandex_service import YandexService


@pytest.mark.asyncio
async def test_log_update_json():

    mock_update = MagicMock(spec=Update)
    mock_update.to_dict.return_value = {"message": "test"}

    mock_context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)

    with patch("backend.app.handlers.logging_handler.logger.info") as mock_logger:
        await log_update_json(mock_update, mock_context)

    mock_update.to_dict.assert_called_once()

    mock_logger.assert_called_once_with(
        "Incoming Telegram update JSON:\n%s",
        {"message": "test"}
    )

def test_register_logging():
    mock_app = MagicMock(spec=Application)

    register_logging(mock_app)

    mock_app.add_handler.assert_called_once()
    called_handler = mock_app.add_handler.call_args[0][0]
    assert isinstance(called_handler, MessageHandler)
    assert called_handler.filters == filters.ALL
    assert called_handler.callback == log_update_json


def test_yandex_service_complete():
    test_prompt = "Test prompt"
    expected_response = {
        "result": {
            "alternatives": [{
                "message": {"text": "Test response"}
            }]
        }
    }

    mock_response = MagicMock()
    mock_response.json.return_value = expected_response
    with patch('requests.post', return_value=mock_response) as mock_post:
        result = YandexService.complete(test_prompt)

    assert result == "Test response"

@pytest.mark.asyncio
async def test_bot_server_start():
    mock_update = MagicMock(spec=Update)
    mock_message = MagicMock(spec=Message)
    mock_update.message = mock_message
    mock_context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)

    await bot_server.start(mock_update, mock_context)

    mock_message.reply_text.assert_called_once_with(
        'Привет! Я эхо-бот. Отправь мне сообщение, и я повторю его.'
    )

@pytest.mark.asyncio
async def test_bot_server_echo():
    mock_update = MagicMock(spec=Update)
    mock_message = MagicMock(spec=Message)
    mock_update.message = mock_message
    mock_context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)

    await bot_server.echo(mock_update, mock_context)

    mock_message.reply_text.assert_called_once_with(
        mock_update.message.text
    )