# -*- coding: utf-8 -*-
""" GoPlay API """

from collections import OrderedDict

CHANNELS = OrderedDict([
    ('Play 4', {
        'name': 'Play 4',
        'epg_id': 'vier',
        'logo': 'play4.png',
        'background': 'play4-background.png',
        'iptv_preset': 4,
        'iptv_id': 'play4.be',
        'youtube': [
            {'label': 'GoPlay', 'logo': 'goplay.png', 'path': 'plugin://plugin.video.youtube/user/viertv/'},
        ]
    }),
    ('Play 5', {
        'name': 'Play 5',
        'epg_id': 'vijf',
        'logo': 'play5.png',
        'background': 'play5-background.png',
        'iptv_preset': 5,
        'iptv_id': 'play5.be',
        'youtube': [
            {'label': 'GoPlay', 'logo': 'goplay.png', 'path': 'plugin://plugin.video.youtube/user/viertv/'},
        ]
    }),
    ('Play 6', {
        'name': 'Play 6',
        'epg_id': 'zes',
        'logo': 'play6.png',
        'background': 'play6-background.png',
        'iptv_preset': 6,
        'iptv_id': 'play6.be',
        'youtube': [
            {'label': 'GoPlay', 'logo': 'goplay.png', 'path': 'plugin://plugin.video.youtube/user/viertv/'},
        ]
    }),
    ('Play 7', {
        'name': 'Play 7',
        'epg_id': 'zeven',
        'url': 'https://www.goplay.be',
        'logo': 'play7.png',
        'background': 'play7-background.png',
        'iptv_preset': 17,
        'iptv_id': 'play7.be',
        'youtube': []
    }),
        ('Play Crime', {
        'name': 'Play Crime',
        'epg_id': 'crime',
        'url': 'https://www.goplay.be',
        'logo': 'playcrime.png',
        'background': 'playcrime-background.png',
        'iptv_preset': 18,
        'iptv_id': 'playcrime7.be',
        'youtube': []
    }),
    ('GoPlay', {
        'name': 'Go Play',
        'url': 'https://www.goplay.be',
        'logo': 'goplay.png',
        'background': 'goplay-background.png',
        'youtube': []
    })
])



STREAM_DICT = {
    'codec': 'h264',
    'height': 544,
    'width': 960,
}


class ResolvedStream:
    """ Defines a stream that we can play"""

    def __init__(self, uuid=None, url=None, stream_type=None, license_key=None):
        """
        :type uuid: str
        :type url: str
        :type stream_type: str
        :type license_key: str
        """
        self.uuid = uuid
        self.url = url
        self.stream_type = stream_type
        self.license_key = license_key

    def __repr__(self):
        return "%r" % self.__dict__
