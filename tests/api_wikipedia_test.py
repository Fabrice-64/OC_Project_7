"""
   This module manages the tests with the wikipedia API.
   It starts with the unitary test, to end with a functional
   test of the whole exchange between the app and the website.
   These tests use mock data iot limit the connection to Wikipedia.

    Classes:
    TestApiWikipedia: regroups all the methods involved in the API.

    Exceptions:
    NIL

    Functions:
    NIL
    """
import requests
from app.controller.api_folder.api_wikipedia import WikipediaApi
from config import WikipediaPath as WP
from tests.conftest import TestWikipediaRequest
from nose.tools import assert_true, assert_equal
from unittest.mock import Mock, patch


class TestApiWikipedia(WikipediaApi, TestWikipediaRequest):
    """
        Inherits from the Wikipedia API class, where all the API is played
        and from TestWikipediaRequest which ecompasses all the test data.

        Methods:
        test_connection_ok

        test_get_draft_location_when_response_is_ok

        test_sort_out_exact_location_name

        test_get_location_summary

        test_extract_location_summary

        test_filter_location_summary

        test_get_coordinates:
        not used in this current version. However remains tested.

        test_filter_coordinates:
        idem

        test_from_location_to_summary:
        functional test

        test_from_location_to_summary_not_ok
        checks that a wrong question or
        the absence of response is properly handled with.
        """

    def test_connection_ok(self):
        response = requests.get(WP.WIKI_ROOT)
        assert_true(response.ok)

    @patch('app.controller.api_folder.api_wikipedia.requests.get')
    def test_get_draft_location_when_response_is_ok(self, mock_get):
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = self.mock_draft_location
        response = self._get_draft_location(self.location_search)
        assert_equal(response, self.mock_draft_location)

    def test_sort_out_exact_location_name(self):
        real_location_name = \
            self._sort_out_exact_location_name(self.mock_draft_location)
        assert_equal(self.mock_location_name, real_location_name)

    def test_push_exact_location_name(self):
        exact_loc_name = self.push_exact_location_name(self.location_search)
        assert_equal(self.mock_location_name, exact_loc_name)

    @patch('app.controller.api_folder.api_wikipedia.requests.get')
    def test_get_location_summary(self, mock_get):
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = self.mock_location_summary
        response = self._get_location_summary(self.mock_location_name)
        assert_equal(response, self.mock_location_summary)

    def test_extract_location_summary(self):
        response = self._extract_location_summary(self.mock_location_summary)
        assert_equal(response, self.non_filtered_description)

    def test_filter_location_summary(self):
        response = self._filter_location_summary(self.non_filtered_description)
        assert_equal(response, self.filtered_description)

    @patch('app.controller.api_folder.api_wikipedia.requests.get')
    def test_get_coordinates(self, mock_get):
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = self.mock_draft_coordinates
        response = self._get_coordinates(self.mock_location_name)
        assert_equal(response, self.mock_draft_coordinates)

    def test_filter_coordinates(self):
        response = self._filter_coordinates(self.mock_draft_coordinates)
        assert_equal(response, self.filtered_coordinates)

    def test_from_location_to_summary(self):
        summary = self.from_location_to_summary(self.mock_location_name)
        assert all(map(lambda w: w in summary, self.check_important_words))

    def test_from_location_to_summary_not_ok(self):
        summary = self.from_location_to_summary(self.non_existant_article)
        assert summary == self.non_existant_article
