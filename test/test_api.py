# -*- coding: utf-8 -*-
""" Tests for Content API """

# pylint: disable=missing-docstring,no-self-use

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import unittest

import resources.lib.kodiutils as kodiutils
from resources.lib.viervijfzes.content import ContentApi, Program, Episode
from resources.lib.viervijfzes.auth import AuthApi

_LOGGER = logging.getLogger('test-api')


class TestApi(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestApi, self).__init__(*args, **kwargs)
        self._api = ContentApi()

    def test_programs(self):
        for channel in ['vier', 'vijf', 'zes']:
            channels = self._api.get_programs(channel)
            self.assertIsInstance(channels, list)

    def test_episodes(self):
        for channel, program in [('vier', 'auwch'), ('vijf', 'zo-man-zo-vrouw')]:
            program = self._api.get_program(channel, program)
            self.assertIsInstance(program, Program)
            self.assertIsInstance(program.seasons, dict)
            # self.assertIsInstance(program.seasons[0], Season)
            self.assertIsInstance(program.episodes, list)
            self.assertIsInstance(program.episodes[0], Episode)
            _LOGGER.info('Got program: %s', program)

    def test_get_stream(self):
        program = self._api.get_program('vier', 'auwch')
        episode = program.episodes[0]

        auth = AuthApi(kodiutils.get_setting('username'), kodiutils.get_setting('password'), kodiutils.get_tokens_path())
        api_authed = ContentApi(auth.get_token())
        video = api_authed.get_stream(episode.channel, episode.uuid)
        self.assertTrue(video)

        _LOGGER.info('Got video URL: %s', video)


if __name__ == '__main__':
    unittest.main()
