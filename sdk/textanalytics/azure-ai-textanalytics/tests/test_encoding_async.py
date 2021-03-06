# coding=utf-8
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

import pytest
import platform
import functools

from azure.core.exceptions import HttpResponseError, ClientAuthenticationError
from azure.core.credentials import AzureKeyCredential
from testcase import GlobalTextAnalyticsAccountPreparer
from asynctestcase import AsyncTextAnalyticsTest
from testcase import TextAnalyticsClientPreparer as _TextAnalyticsClientPreparer
from azure.ai.textanalytics.aio import TextAnalyticsClient

# pre-apply the client_cls positional argument so it needn't be explicitly passed below
# the first one
TextAnalyticsClientPreparer = functools.partial(_TextAnalyticsClientPreparer, TextAnalyticsClient)

class TestEncoding(AsyncTextAnalyticsTest):
    @GlobalTextAnalyticsAccountPreparer()
    @TextAnalyticsClientPreparer()
    async def test_emoji(self, client):
        result = await client.recognize_pii_entities(["๐ฉ SSN: 859-98-0987"])
        self.assertEqual(result[0].entities[0].offset, 7)

    @GlobalTextAnalyticsAccountPreparer()
    @TextAnalyticsClientPreparer()
    async def test_emoji_with_skin_tone_modifier(self, client):
        result = await client.recognize_pii_entities(["๐ฉ๐ป SSN: 859-98-0987"])
        self.assertEqual(result[0].entities[0].offset, 8)

    @GlobalTextAnalyticsAccountPreparer()
    @TextAnalyticsClientPreparer()
    async def test_emoji_family(self, client):
        result = await client.recognize_pii_entities(["๐ฉโ๐ฉโ๐งโ๐ง SSN: 859-98-0987"])
        self.assertEqual(result[0].entities[0].offset, 13)

    @GlobalTextAnalyticsAccountPreparer()
    @TextAnalyticsClientPreparer()
    async def test_emoji_family_with_skin_tone_modifier(self, client):
        result = await client.recognize_pii_entities(["๐ฉ๐ปโ๐ฉ๐ฝโ๐ง๐พโ๐ฆ๐ฟ SSN: 859-98-0987"])
        self.assertEqual(result[0].entities[0].offset, 17)

    @GlobalTextAnalyticsAccountPreparer()
    @TextAnalyticsClientPreparer()
    async def test_diacritics_nfc(self, client):
        result = await client.recognize_pii_entities(["aรฑo SSN: 859-98-0987"])
        self.assertEqual(result[0].entities[0].offset, 9)

    @GlobalTextAnalyticsAccountPreparer()
    @TextAnalyticsClientPreparer()
    async def test_diacritics_nfd(self, client):
        result = await client.recognize_pii_entities(["anฬo SSN: 859-98-0987"])
        self.assertEqual(result[0].entities[0].offset, 10)

    @GlobalTextAnalyticsAccountPreparer()
    @TextAnalyticsClientPreparer()
    async def test_korean_nfc(self, client):
        result = await client.recognize_pii_entities(["์๊ฐ SSN: 859-98-0987"])
        self.assertEqual(result[0].entities[0].offset, 8)

    @GlobalTextAnalyticsAccountPreparer()
    @TextAnalyticsClientPreparer()
    async def test_korean_nfd(self, client):
        result = await client.recognize_pii_entities(["์๊ฐ SSN: 859-98-0987"])
        self.assertEqual(result[0].entities[0].offset, 8)

    @GlobalTextAnalyticsAccountPreparer()
    @TextAnalyticsClientPreparer()
    async def test_zalgo_text(self, client):
        result = await client.recognize_pii_entities(["oฬตฬฬฬฬอฬฬอฬอฬออฬฬฬฬฬออฬณฬฬอออฬงฬญฬงฬฬออฬฬขอmฬตอฬฬฬอ?อฬฬฬฝออฬgฬตฬอออ?ฬฬฬฬฬอฬอฬอฬฬอฬฟฬฬอฬฬอฬฬฬอฬฬฬพออฬอฬขฬฬกฬฏฬ?ฬคฬฃอฬขฬฬซฬซฬผฬฐออฬกฬจฬฆฬกออฬงฬฃฬฃอ SSN: 859-98-0987"])


        self.assertEqual(result[0].entities[0].offset, 121)
