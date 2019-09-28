"""Configuration factory unit tests."""

from expects import expect, be, raise_error, be_a
from honeybadger.config import Configuration, ConfigurationFactory, ConfigurationError


class TestConfigurationFactory():
    def test_load_configuration(self):
        """Load configuration objects from factory."""

        config = ConfigurationFactory.from_env()

        config = Configuration()
        config.from_json()
        print(config.github_client_id)
        print(config.github_client_secret)
        print(ConfigurationFactory.generate_secret_key())
        # expect(lambda: config.from_json('/this/path/does/not/exist.json')
        #        ).to(raise_error(ConfigurationError))
        # config.from_json('/Users/gregorymundy/Work/honeybadger/honeybadger/config.json')
