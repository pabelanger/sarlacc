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

from cStringIO import StringIO
from mock import patch
from sarlacc.tests.asterisk.agi import test


class TestCase(test.TestCase):

    def test_say_digits_failure(self):
        with patch('sys.stdin', StringIO("200 result=-1")
                   ), patch('sys.stdout',
                            new_callable=StringIO) as mocked_out:
            res, dtmf = self.agi.say_digits(string='2000')
            self.assertEqual(mocked_out.getvalue(), 'SAY DIGITS 2000 ""\n')
            self.assertFalse(res)
            self.assertEqual(dtmf, '')

    def test_say_digits_success(self):
        with patch('sys.stdin', StringIO("200 result=0")
                   ), patch('sys.stdout',
                            new_callable=StringIO) as mocked_out:
            res, dtmf = self.agi.say_digits(string='25000')
            self.assertEqual(mocked_out.getvalue(), 'SAY DIGITS 25000 ""\n')
            self.assertTrue(res)
            self.assertEqual(dtmf, '')

    def test_say_digits_digit_pressed(self):
        with patch('sys.stdin', StringIO("200 result=49")
                   ), patch('sys.stdout',
                            new_callable=StringIO) as mocked_out:
            res, dtmf = self.agi.say_digits(string='5000', digits='1234')
            self.assertEqual(mocked_out.getvalue(), 'SAY DIGITS 5000 "1234"\n')
            self.assertTrue(res)
            self.assertEqual(dtmf, '1')
