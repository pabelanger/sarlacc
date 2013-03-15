#!/usr/bin/env python

# Copyright (C) 2013 PolyBeacon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.

"""
Asterisk AGI
"""

import logging
from sarlacc.utils import agi_send, agi_setup_env

LOG = logging.getLogger(__name__)


class AGI(object):
    env = {}

    def __init__(self):
        self.env = agi_setup_env()

    def answer(self):
        """
        Answers the channel.

        :returns:
            Failure: False
            Success: True
        """
        cmd = 'ANSWER'
        res = agi_send(cmd)[1]
        if res != '0':
            return False
        return True

    def get_data(self, filename, digits, timeout=0):
        """
        Plays the audio file to the current channel.

        :param filename:
            Name of the file you wish to be played. The extension must not be
            included in the filename.

        :type filename:
            str

        :param digits:
            Number of DTMF to interrupt the audio stream. Note: The value must
            be greater the 0 otherwise asterisk will return failure.

        :type digits:
            str

        :param timeout:
            The amount of time, in milliseconds, to wait after the last DTMF is
            recieved.

        :type timeout:
            str

        :returns:
            Failure: False
            Success: True
        """
        ret_timeout = False
        result = True

        cmd = 'GET DATA %s %s %s' % (filename, timeout, digits)
        res, args = agi_send(cmd)[1:]
        dtmf = res

        if res == '-1':
            dtmf = ''
            result = False

        if args[1:-1] == 'timeout':
            ret_timeout = True

        return result, dtmf, ret_timeout

    def get_variable(self, name):
        """
        Gets a channel variable.

        :param name:
            Channel name

        :type name:
            str

        :returns:
            Failure: False, ''
            Success: True, Value
        """
        cmd = 'GET VARIABLE %s' % name
        res, args = agi_send(cmd)[1:]

        if res != '1':
            return False, ''
        return True, args[1:-1]

    def hangup(self, channel=None):
        """
        Hangs up the specified channel.  If no channel is given, hangs up the
        current channel.

        :param channel:
            Name of the channel to hangup

        :type channel:
            str

        :returns:
            Failure: False
            Success: True
        """
        cmd = 'HANGUP'
        if channel is not None:
            cmd += ' %s' % channel
        res = agi_send(cmd)[1]

        if res != '1':
            return False
        return True

    def set_variable(self, name, value):
        """
        Sets a channel variable.

        :param name:
            Name of the channel variable

        :type name:
            str

        :param value:
            Value of the channel variable

        :type value:
            str

        :returns:
            True
        """
        cmd = 'SET VARIABLE %s %s' % (name, value)
        agi_send(cmd)

        return True

    def stream_file(self, name, digits="", offset="0"):
        """
        Plays the audio file to the current channel.

        :param name:
            Filename to play.  The extension must not be included in the
            filename.

        :type name:
            str

        :param digits:
            Digits to interrupt audio stream.

        :type digits:
            str

        :param offset:
            If an offset is provided the audio will seek to the offset before
            play starts.

        :type offset:
            str

        :returns:
            Failure: False
            Success: True
        """
        result = True
        dtmf = ''

        cmd = 'STREAM FILE %s "%s" %s' % (name, digits, offset)
        res, args = agi_send(cmd)[1:]
        endpos = args.replace('endpos=', '')

        if res == '-1':
            result = False
        elif res == '0' and endpos == '0':
            result = False
        if res > '0':
            dtmf = chr(int(res))

        return result, dtmf, endpos

    def verbose(self, level, message):
        """
        Log a message to the asterisk verbose log.

        :param level:
            Verbosity level

        :type level:
            int

        :param message:
            Text to be logged

        :type message:
            str

        :returns:
            True
        """
        cmd = 'VERBOSE "%s" %s' % (message, level)
        agi_send(cmd)

        return True
