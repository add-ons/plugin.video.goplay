# -*- coding: utf-8 -*-
""" Channels module """

from __future__ import absolute_import, division, unicode_literals

import logging

from resources.lib import kodiutils
from resources.lib.kodiutils import TitleItem
from resources.lib.goplay import STREAM_DICT
from resources.lib.goplay.auth import AuthApi
from resources.lib.goplay.content import ContentApi

_LOGGER = logging.getLogger(__name__)


class Channels:
    """ Menu code related to channels """

    def __init__(self):
        """ Initialise object """
        auth = AuthApi(kodiutils.get_setting('username'), kodiutils.get_setting('password'), kodiutils.get_tokens_path())
        self._api = ContentApi(auth, cache_path=kodiutils.get_cache_path())

    def show_channels(self):
        """ Shows TV channels """
        try:
            items = self._api.get_live_channels()
        except Exception as ex:
            kodiutils.notification(message=str(ex))
            raise

        listing = []

        for channel in items:

            listing.append(
                TitleItem(
                    title=channel.title,
                    path=kodiutils.url_for('show_channel_menu', uuid=channel.uuid),
                    art_dict={
                        'icon': channel.logo,
                        'thumb': channel.logo,
                        'fanart': channel.fanart,
                    },
                    info_dict={
                        'plot': None,
                        'playcount': 0,
                        'mediatype': 'video',
                    },
                    stream_dict=STREAM_DICT,
                ),
            )

        kodiutils.show_listing(listing, 30007)

    def show_channel_menu(self, uuid):
        """ Shows a TV channel
        :type uuid: str
        """
        channel_info = {}

        try:
            items = self._api.get_live_channels()
        except Exception as ex:
            kodiutils.notification(message=str(ex))
            raise

        channel = next(channel for channel in items if channel.uuid == uuid)

        listing = []

        listing.append(
            TitleItem(
                title=kodiutils.localize(30055, channel=channel.title),  # Catalog for {channel}
                path=kodiutils.url_for('show_channel_catalog', channel=channel.title),
                art_dict={
                    'icon': 'DefaultMovieTitle.png',
                    'fanart': channel.fanart,
                },
                info_dict={
                    'plot': kodiutils.localize(30056, channel=channel.title),  # Browse the Catalog for {channel}
                }
            )
        )

        listing.append(
            TitleItem(
                title=kodiutils.localize(30052, channel=channel.title),  # Watch live {channel}
                path=kodiutils.url_for('play_live', channel=channel.uuid) + '?.pvr',
                art_dict={
                    'icon': channel.logo,
                    'fanart': channel.fanart,
                },
                info_dict={
                    'plot': kodiutils.localize(30052, channel=channel.title),  # Watch live {channel}
                    'playcount': 0,
                    'mediatype': 'video',
                },
                is_playable=True,
            )
        )

        # Add YouTube channels
        if kodiutils.get_cond_visibility('System.HasAddon(plugin.video.youtube)') != 0:
            for youtube in channel_info.get('youtube', []):
                listing.append(
                    TitleItem(
                        title=kodiutils.localize(30206, label=youtube.get('label')),  # Watch {label} on YouTube
                        path=youtube.get('path'),
                        info_dict={
                            'plot': kodiutils.localize(30206, label=youtube.get('label')),  # Watch {label} on YouTube
                        }
                    )
                )

        kodiutils.show_listing(listing, 30007, sort=['unsorted'])
