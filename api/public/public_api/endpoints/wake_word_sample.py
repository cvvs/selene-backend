# Mycroft Server - Backend
# Copyright (C) 2020 Mycroft AI Inc
# SPDX-License-Identifier: 	AGPL-3.0-or-later
#
# This file is part of the Mycroft Server.
#
# The Mycroft Server is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""Public Device API endpoint for uploading a sample wake word for tagging."""
from http import HTTPStatus
from logging import getLogger
from os import environ
from pathlib import Path

from flask import jsonify
from schematics import Model
from schematics.types import StringType
from schematics.exceptions import DataError

from selene.api import PublicEndpoint
from selene.data.account import Account, AccountRepository
from selene.data.wake_word import (
    SampleRepository,
    WakeWordSample,
    WakeWord,
    WakeWordRepository,
)

_log = getLogger(__package__)


class UploadRequest(Model):
    """Data class for validating the content of the POST request."""

    wake_word = StringType(required=True)
    engine = StringType(required=True)
    timestamp = StringType(required=True)
    model = StringType(required=True)


class WakeWordSampleUpload(PublicEndpoint):
    """Endpoint for submitting and retrieving wake word samples.

    Samples will be saved to a temporary location on the API host until a daily batch
    job moves them to a permanent one.  Each file will be logged on the sample table
    for their location and classification data.
    """

    def __init__(self):
        super(WakeWordSampleUpload, self).__init__()
        self.request_data = None

    def post(self, device_id):
        """
        Process a HTTP POST request submitting a wake word sample from a device.

        :param device_id: UUID of the device that originated the request.
        :return:  HTTP response indicating status of the request.
        """
        self._authenticate(device_id)
        self._validate_post_request()
        account = self._get_account(device_id)
        wake_word = self._get_wake_word(account)
        if wake_word is not None:
            audio_file_path = self._build_audio_file_path(account)
            self.request.files["audio_file"].save(audio_file_path)
            self._add_wake_word_sample(account, wake_word, audio_file_path)

        return jsonify("Wake word sample uploaded successfully"), HTTPStatus.OK

    def _validate_post_request(self):
        """Load the post request into the validation class and perform validations."""
        upload_request = UploadRequest(
            dict(
                wake_word=self.request.form.get("wake_word"),
                engine=self.request.form.get("engine"),
                timestamp=self.request.form.get("timestamp"),
                model=self.request.form.get("model"),
            )
        )
        upload_request.validate()
        self.request_data = upload_request.to_native()
        if "audio_file" not in self.request.files:
            raise DataError(dict(audio_file="No audio file included in request"))

    def _get_account(self, device_id: str):
        """Use the device ID to find the account.

        :param device_id: The database ID for the device that made this API call
        """
        account_repository = AccountRepository(self.db)
        return account_repository.get_account_by_device_id(device_id)

    def _build_audio_file_path(self, account: Account):
        """Build the file path for the audio file.

        :param account: the account from which sample originated
        """
        data_dir = Path(environ["SELENE_DATA_DIR"])
        wake_word_dir = data_dir.joinpath("wake_word")
        wake_word_dir = wake_word_dir.joinpath(self.request_data["wake_word"])
        wake_word_dir.mkdir(parents=True, exist_ok=True)
        file_name = "{account_id}.{timestamp}.wav".format(
            account_id=account.id, timestamp=self.request_data["timestamp"],
        )
        file_path = wake_word_dir.joinpath(file_name)

        return file_path

    def _get_wake_word(self, account: Account):
        """Get the WakeWord object for the wake word related to the sample.

        :param account: the account from which sample originated
        """
        wake_word = None
        wake_word_repository = WakeWordRepository(self.db)
        account_wake_words = wake_word_repository.get_wake_words(account.id)
        for acct_wake_word in account_wake_words:
            if acct_wake_word.setting_name == self.request_data["wake_word"]:
                wake_word = acct_wake_word

        return wake_word

    def _add_wake_word_sample(
        self, account: Account, wake_word: WakeWord, audio_file_path: Path
    ):
        """Add the sample to the database for reference and classification.

        :param account: the account from which sample originated
        :param wake_word: wake word entity from the database
        :param audio_file_path: temporary location of the file
        """
        sample = WakeWordSample(
            wake_word_id=wake_word.id,
            account_id=account.id,
            audio_file_name=audio_file_path.name,
        )
        sample_repository = SampleRepository(self.db)
        sample_repository.add(sample)
