# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014-2017 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

from __future__ import absolute_import, division, print_function

from selenium.common.exceptions import (
    ElementNotVisibleException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from inspirehep.bat.EC import GetText

from . import holdingpen_author_list
from ..arsenic import Arsenic, ArsenicResponse


ACCEPTED_MESSAGE = '//div[@class="alert ng-scope alert-accept"]'
REJECTED_MESSAGE = '//div[@class="alert ng-scope alert-reject"]'
ACCEPTED_WITH_CURATION_MESSAGE = '//span[@ng-switch-when="accept_curate"]'


def go_to():
    holdingpen_author_list.go_to()
    holdingpen_author_list.click_first_record()


def load_submitted_record(input_data):
    def _assert_has_no_errors():
        assert (
            'M. Twain' in record and
            'Twain, Mark' in record and
            'retired' in record and
            'ATLAS' in record and
            '2002' in record and
            '2005' in record and
            'Submitted by admin@inspirehep.net\non' in record and
            'Some comments about the author' in record and
            'http://www.example1.com' in record and
            'http://www.example3.com' in record and
            'http://www.example4.com' in record and
            'http://www.example5.com' in record and
            'cond-mat' in record and
            'astro-ph' in record and
            'Bob White' in record and
            'CERN' in record and
            '2000' in record and
            '2001' in record
        )

    wait = WebDriverWait(Arsenic(), 10)
    try:
        record = wait.until(GetText((By.ID, 'hp-panel-detailed-info')))
        record += wait.until(GetText((By.ID, 'hp-panel-links')))
        record += wait.until(GetText((By.ID, 'hp-panel-notes')))
        record += wait.until(GetText((By.ID, 'hp-panel-submission-info')))
        record += wait.until(GetText((By.ID, 'hp-panel-subjects')))
        record += wait.until(GetText((By.ID, 'hp-panel-positions')))
        record += wait.until(GetText((By.ID, 'hp-panel-experiments')))
        record += wait.until(GetText((By.ID, 'hp-panel-advisors')))
    except (ElementNotVisibleException, WebDriverException):
        go_to()
        record = load_submitted_record(input_data)

    return ArsenicResponse(assert_has_no_errors_func=_assert_has_no_errors)


def accept_record():
    def _assert_has_no_errors():
        assert (
            'Accepted as Non-CORE' in WebDriverWait(Arsenic(), 10).until(
                GetText((By.XPATH, ACCEPTED_MESSAGE))
            )
        )

    Arsenic().find_element_by_id('btn-accept').click()
    return ArsenicResponse(assert_has_no_errors_func=_assert_has_no_errors)


def reject_record():
    def _assert_has_no_errors():
        assert (
            'Rejected' in WebDriverWait(Arsenic(), 10).until(
                GetText((By.XPATH, REJECTED_MESSAGE))
            )
        )

    Arsenic().find_element_by_id('btn-reject-submission').click()
    return ArsenicResponse(assert_has_no_errors_func=_assert_has_no_errors)


def curation_record():
    def _assert_has_no_errors():
        assert (
            'Accepted with Curation' in WebDriverWait(Arsenic(), 10).until(
                GetText((By.XPATH, ACCEPTED_WITH_CURATION_MESSAGE))
            )
        )

    Arsenic().find_element_by_id('btn-accept-curation').click()
    return ArsenicResponse(assert_has_no_errors_func=_assert_has_no_errors)


def review_record(input_data):
    def _assert_has_no_errors():
        def _assert_text_in_element(element_id, text):
            try:
                assert (
                    text in Arsenic().find_element_by_id(
                        element_id
                    ).get_attribute('value')
                )
            except TypeError:
                assert text in Arsenic().find_element_by_id(element_id).text

        assert WebDriverWait(Arsenic(), 10).until(
            EC.visibility_of_element_located((By.ID, 'inspireid'))
        )
        assert WebDriverWait(Arsenic(), 10).until(
            EC.visibility_of_element_located((By.ID, 'bai'))
        )
        for element_id, text in input_data.iteritems():
            _assert_text_in_element(element_id, text)

    Arsenic().find_element_by_id('btn-review-submission').click()
    return ArsenicResponse(assert_has_no_errors_func=_assert_has_no_errors)
