import logging


class TestLogConfiguration:
    """[config set up]"""

    def test_INFO__level_log(self, test_client):
        """
        Verify log for INFO level
        """
        user_logs = test_client.get("/")
        logger = logging.getLogger("webapp")
        logger.setLevel(logging.INFO)

        assert len(logger.output) == 4
        assert len(logger.records) == 4
        assert "Info log information" in logger.output[0]
        assert "Debug log information" in logger.output[1]
        assert "Warning log information" in logger.output[2]
        assert "Error log information" in logger.output[3]
        assert user_logs.status_code == 200

    def test_WARNING__level_log(self, test_client):
        """
        Verify log for WARNING level
        """
        user_logs = test_client.get("/")
        logger = logging.getLogger("webapp")
        logger.setLevel(logging.INFO)

        assert len(logger.output) == 4
        assert "Warning log info" in logger.output[1]

    def test_ERROR__level_log(self, test_client):
        """
        Verify log for ERROR level
        """
        user_logs = test_client.get("/")
        logger = logging.getLogger("webapp")
        logger.setLevel(logging.INFO)

        assert len(logger.output) == 4
        assert "Error log info" in logger.output[2]
