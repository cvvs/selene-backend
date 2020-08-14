# Mycroft Server - Backend
# Copyright (C) 2019 Mycroft AI Inc
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
"""Step functions for the wake word sample upload feature."""
import os
from datetime import date
from pathlib import Path

from behave import then, when  # pylint: disable=no-name-in-module
from hamcrest import assert_that, equal_to, is_in, none

from selene.data.wake_word import WakeWordRepository, SampleRepository


@when("the device uploads a wake word sample")
def upload_file(context):
    """Upload a wake word sample file using the public API"""
    resources_dir = Path(os.path.dirname(__file__)).joinpath("resources")
    audio_file_path = str(resources_dir.joinpath("wake_word_test.wav"))
    access_token = context.device_login["accessToken"]
    with open(audio_file_path, "rb") as audio_file:
        wake_word_request = dict(
            wake_word="selene_test_wake_word",
            engine="precise",
            timestamp="12345",
            model="selene_test_model",
            audio_file=(audio_file, "wake_word.wav"),
        )
        response = context.client.post(
            f"/v1/device/{context.device_id}/wake-word-sample",
            headers=dict(Authorization="Bearer {token}".format(token=access_token)),
            data=wake_word_request,
            content_type="multipart/form-data",
        )
    context.response = response


@then("the audio file is saved to a temporary directory")
def check_file_save(context):
    """The audio file containing the wake word sample is saved to the right location."""
    file_name = context.account.id + ".12345.wav"
    file_path = Path(context.wake_word_dir).joinpath(file_name)
    assert file_path.exists()


@then("a reference to the sample is stored in the database")
def check_sample_table(context):
    """The data representing the audio file is stored correctly on the database."""
    sample_repository = SampleRepository(context.db)
    account_samples = sample_repository.retrieve_by_account(context.account.id)
    assert_that(len(account_samples), equal_to(1))
    sample = account_samples[0]
    assert_that(sample.audio_file_name, equal_to(context.account.id + ".12345.wav"))
    assert_that(sample.wake_word, equal_to("selene_test_wake_word"))
    assert_that(sample.audio_file_date, equal_to(date.today()))
    assert_that(sample.directory_group, none())
