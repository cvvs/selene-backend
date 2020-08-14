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
"""Data access and manipulation for the wake_word.sample table."""
from ..entity.sample import WakeWordSample
from ...repository_base import RepositoryBase


class SampleRepository(RepositoryBase):
    """Data access and manipulation for the wake_word.sample table."""

    def __init__(self, db):
        super(SampleRepository, self).__init__(db, __file__)

    def add(self, sample: WakeWordSample):
        """Adds a row to the wake word sample table

        :param sample: a wake word sample not yet classified by the community
        :return wake word id
        """
        db_request = self._build_db_request(
            sql_file_name="add_sample.sql",
            args=dict(
                wake_word_id=sample.wake_word_id,
                account_id=sample.account_id,
                audio_file_name=sample.audio_file_name,
            ),
        )
        self.cursor.insert(db_request)

    def retrieve_by_account(self, account_id: str):
        """Get a sample file reference based on the file name.

        :param account_id: identifies the user that submitted the sample.
        :return: UnclassifiedSample object containing the retrieved row
        """
        return self._select_all_into_dataclass(
            dataclass=WakeWordSample,
            sql_file_name="get_samples_by_account.sql",
            args=dict(account_id=account_id),
        )
