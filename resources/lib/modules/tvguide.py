# -*- coding: utf-8 -*-
""" Menu code related to channels """

from __future__ import absolute_import, division, unicode_literals

import logging
from datetime import datetime, timedelta

from resources.lib import kodiutils
from resources.lib.kodiutils import TitleItem
from resources.lib.goplay import STREAM_DICT
from resources.lib.goplay.content import UnavailableException
from resources.lib.goplay.epg import EpgApi

_LOGGER = logging.getLogger(__name__)


class TvGuide:
    """ Menu code related to the TV Guide """

    def __init__(self):
        """ Initialise object """
        self._epg = EpgApi()

    @staticmethod
    def get_dates(date_format):
        """ Return a dict of dates.
        :rtype: list[dict]
        """
        dates = []
        today = datetime.today()

        # The API provides 7 days in the past and 8 days in the future
        for i in range(-7, 8):
            day = today + timedelta(days=i)

            if i == -1:
                dates.append({
                    'title': '%s, %s' % (kodiutils.localize(30301), day.strftime(date_format)),  # Yesterday
                    'key': 'yesterday',
                    'date': day.strftime('%d.%m.%Y'),
                    'highlight': False,
                })
            elif i == 0:
                dates.append({
                    'title': '%s, %s' % (kodiutils.localize(30302), day.strftime(date_format)),  # Today
                    'key': 'today',
                    'date': day.strftime('%d.%m.%Y'),
                    'highlight': True,
                })
            elif i == 1:
                dates.append({
                    'title': '%s, %s' % (kodiutils.localize(30303), day.strftime(date_format)),  # Tomorrow
                    'key': 'tomorrow',
                    'date': day.strftime('%d.%m.%Y'),
                    'highlight': False,
                })
            else:
                dates.append({
                    'title': day.strftime(date_format),
                    'key': day.strftime('%Y-%m-%d'),
                    'date': day.strftime('%d.%m.%Y'),
                    'highlight': False,
                })

        return dates

    def show_channel(self, channel):
        """ Shows the dates in the tv guide
        :type channel: str
        """
        listing = []
        for day in self.get_dates('%A %d %B %Y'):
            if day.get('highlight'):
                title = '[B][COLOR=yellow]{title}[/COLOR][/B]'.format(title=day.get('title'))
            else:
                title = day.get('title')

            listing.append(
                TitleItem(title=title,
                          path=kodiutils.url_for('show_channel_tvguide_detail', channel=channel, date=day.get('key')),
                          art_dict={
                              'icon': 'DefaultYear.png',
                              'thumb': 'DefaultYear.png',
                          },
                          info_dict={
                              'plot': None,
                              'date': day.get('date'),
                          })
            )

        kodiutils.show_listing(listing, 30013, content='files', sort=['date'])

    def show_detail(self, channel=None, date=None):
        """ Shows the programs of a specific date in the tv guide
        :type channel: str
        :type date: str
        """
        try:
            programs = self._epg.get_epg(channel=channel, date=date)
        except UnavailableException as ex:
            kodiutils.notification(message=str(ex))
            kodiutils.end_of_directory()
            return

        listing = []
        for program in programs:
            # print(f"Context_Menu for {program.program_title}")
            if program.program_url:
                context_menu = [(
                    kodiutils.localize(30102),  # Go to Program
                    'Container.Update(%s)' %
                    kodiutils.url_for('show_catalog_program', uuid=program.program_url)
                    # kodiutils.url_for('show_catalog_program', channel=channel, program=program.program_url)
                )]
            else:
                context_menu = None

            title = '{time} - {title}'.format(
                time=program.start.strftime('%H:%M'),
                title=program.program_title
            )

            if program.airing:
                title = '[COLOR=yellow][B]{title}[/B][/COLOR]'.format(title=title)

            if program.video_url:
                path = kodiutils.url_for('play_catalog', uuid=program.video_url, content_type='video')
            else:
                path=None
                title = '[COLOR gray]' + title + '[/COLOR]'

            stream_dict = STREAM_DICT.copy()
            stream_dict.update({
                'duration': program.duration,
            })

            info_dict = {
                'title': title,
                'plot': program.description,
                'studio': program.channel,
                'duration': program.duration,
                'tvshowtitle': program.program_title,
                'season': program.season,
                'episode': program.number,
                'mediatype': 'episode',
            }

            listing.append(
                TitleItem(title=title,
                          path=path,
                          art_dict={
                              'thumb': program.thumb,
                          },
                          info_dict=info_dict,
                          stream_dict=stream_dict,
                          context_menu=context_menu,
                          is_playable=True)
            )

        kodiutils.show_listing(listing, 30013, content='episodes', sort=['unsorted'])
