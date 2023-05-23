from flask import Flask
from app import app

import logging
import unittest


class TestLogConfiguration(unittest.TestCase):
    """[config set up]"""

    def test_INFO__level_log(self):
        """
        Verify log for INFO level
        """
        self.app = app
        self.client = self.app.test_client

        with self.assertLogs() as log:
            user_logs = self.client().get("/")
            self.assertEqual(len(log.output), 4)
            self.assertEqual(len(log.records), 4)
            self.assertIn("Info log information", log.output[0])
            self.assertIn("Debug log information", log.output[1])
            self.assertIn("Warning log information", log.output[2])
            self.assertIn("Error log information", log.output[3])
            self.assertEqual(user_logs.status_code, 200)

    def test_WARNING__level_log(self):
        """
        Verify log for WARNING level
        """
        self.app = app
        self.client = self.app.test_client

        with self.assertLogs() as log:
            user_logs = self.client().get("/")
            self.assertEqual(len(log.output), 4)
            self.assertIn("Warning log info", log.output[1])

    def test_ERROR__level_log(self):
        """
        Verify log for ERROR level
        """
        self.app = app
        self.client = self.app.test_client

        with self.assertLogs() as log:
            user_logs = self.client().get("/")
            self.assertEqual(len(log.output), 4)
            self.assertIn("Error log info", log.output[2])
