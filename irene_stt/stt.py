"""
Support for Irene STT.
"""
import logging
import requests
import async_timeout
import voluptuous as vol
from homeassistant.components import stt
from homeassistant.components.stt import (
    AudioBitRates,
    AudioChannels,
    AudioCodecs,
    AudioFormats,
    AudioSampleRates,
    SpeechMetadata,
    SpeechResult,
    SpeechResultState,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from .const import CONF_URL

_LOGGER = logging.getLogger(__name__)

DEFAULT_LANG = 'ru-RU'

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Irene speech-to-text."""
    _LOGGER.debug("async_setup_entry")
    async_add_entities(
        [
            IreneSTTProvider(
                hass, config_entry
            ),
        ]
    )

    return

class IreneSTTProvider(stt.SpeechToTextEntity):
    """The Irene STT API provider."""

    def __init__(self, hass, config_entry: ConfigEntry):
        """Initialize Irene STT provider."""
        self.hass = hass
        self._language = DEFAULT_LANG
        self._config = config_entry
        self._url = config_entry.data[CONF_URL] + "/api/willow"
        self._attr_name = "IRENE STT"
        self._attr_unique_id = f"{config_entry.entry_id}-stt"

    @property
    def default_language(self) -> str:
        """Return the default language."""
        return self._language

    @property
    def supported_languages(self) -> list[str]:
        """Return the list of supported languages."""
        return [self._language]

    @property
    def supported_formats(self) -> list[AudioFormats]:
        """Return a list of supported formats."""
        return [AudioFormats.WAV]

    @property
    def supported_codecs(self) -> list[AudioCodecs]:
        """Return a list of supported codecs."""
        return [AudioCodecs.PCM]

    @property
    def supported_bit_rates(self) -> list[AudioBitRates]:
        """Return a list of supported bitrates."""
        return [AudioBitRates.BITRATE_16]

    @property
    def supported_sample_rates(self) -> list[AudioSampleRates]:
        """Return a list of supported samplerates."""
        return [AudioSampleRates.SAMPLERATE_16000]

    @property
    def supported_channels(self) -> list[AudioChannels]:
        """Return a list of supported channels."""
        return [AudioChannels.CHANNEL_MONO]


    async def async_process_audio_stream(
        self, metadata: SpeechMetadata, stream
    ) -> SpeechResult:
        # Collect data
        _LOGGER.debug("async_process_audio_stream")
        audio_data = b""
        async for chunk in stream:
            audio_data += chunk
        _LOGGER.debug("async_process_audio_stream chunkend")
        headers = {
            'x-audio-sample-rate': '16000',
            'x-audio-channel': '1',
            'x-audio-bits': '16',
            'x-audio-codec': 'pcm',
            'Content-Type': 'multipart/form-data'
        }
        def job():
            _LOGGER.debug("job '%s'",self._url)
            response = requests.post(self._url, headers=headers, data=audio_data, verify=False)
            if response.status_code == 200:
                _LOGGER.debug("job response.text: '%s'",response.text)
                return response.text.replace("\"","")
            else:
                _LOGGER.error("%s", response.text)
                return ''

        async with async_timeout.timeout(10):
            assert self.hass
            response = await self.hass.async_add_executor_job(job)
            if len(response) > 0:
                _LOGGER.debug("job async_timeout: '%s'",response)
                return SpeechResult(
                    response,
                    SpeechResultState.SUCCESS,
                )
            return SpeechResult("", SpeechResultState.ERROR)
