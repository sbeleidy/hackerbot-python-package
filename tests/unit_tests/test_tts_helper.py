################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.05.13
#
# This module contains the unit tests for the TTSHelper class.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


import os
import unittest
from unittest import mock
from unittest.mock import patch, MagicMock, mock_open
import requests
from huggingface_hub import hf_hub_url
from hackerbot.utils.tts_helper import TTSHelper  # Adjust if module is named differently

class TestTTSHelper(unittest.TestCase):

    def setUp(self):
        self.test_dir = "/tmp/test_piper_models"
        self.helper = TTSHelper(cache_dir=self.test_dir)

    @patch("os.makedirs")
    def test_init_creates_cache_dir(self, mock_makedirs):
        TTSHelper(cache_dir=self.test_dir)
        mock_makedirs.assert_called_once_with(self.test_dir, exist_ok=True)

    @patch("os.path.isfile", return_value=True)
    def test_get_or_download_model_local_path(self, mock_isfile):
        model_path = "/some/local/model.onnx"
        result = self.helper.get_or_download_model(model_path)
        self.assertEqual(result, model_path)
        mock_isfile.assert_called_once_with(model_path)

    @patch("hackerbot.utils.tts_helper.TTSHelper._download_model_from_huggingface", return_value="/downloaded/model.onnx")
    @patch("os.path.isfile", return_value=False)
    def test_get_or_download_model_downloads(self, mock_isfile, mock_download):
        result = self.helper.get_or_download_model("en_US-amy-low")
        self.assertEqual(result, "/downloaded/model.onnx")
        mock_download.assert_called_once_with("en_US-amy-low")

    def test_download_model_invalid_voice_format(self):
        with self.assertRaises(RuntimeError) as cm:
            self.helper._download_model_from_huggingface("invalid-name")
        self.assertIn("Invalid voice model name", str(cm.exception))

    @patch("hackerbot.utils.tts_helper.TTSHelper._download_file")
    @patch("os.path.exists", side_effect=[False, False])
    @patch("hackerbot.utils.tts_helper.hf_hub_url", side_effect=lambda repo_id, filename: f"https://mock/{filename}")
    def test_download_model_success(self, mock_hf_url, mock_exists, mock_download_file):
        voice = "en_US-amy-low"
        expected_path = os.path.join(self.test_dir, f"{voice}.onnx")
        result = self.helper._download_model_from_huggingface(voice)

        self.assertEqual(result, expected_path)
        self.assertEqual(mock_download_file.call_count, 2)  # .onnx and .json

    @patch("builtins.open", new_callable=mock_open)
    @patch("requests.get")
    def test_download_file_success(self, mock_get, mock_file):
        mock_response = MagicMock()
        mock_response.iter_content = lambda chunk_size: [b'data']
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        self.helper._download_file("https://mock.url/model.onnx", "/tmp/model.onnx")
        mock_get.assert_called_once_with("https://mock.url/model.onnx", stream=True)
        mock_file.assert_called_once_with("/tmp/model.onnx", 'wb')

    @patch("requests.get", side_effect=requests.exceptions.RequestException("fail"))
    def test_download_file_failure(self, mock_get):
        with self.assertRaises(RuntimeError) as cm:
            self.helper._download_file("https://fail.url/model.onnx", "/tmp/model.onnx")
        self.assertIn("Failed to download", str(cm.exception))


if __name__ == '__main__':
    unittest.main()
