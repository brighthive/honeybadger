"""Application Configuration."""

import os
import json


class ConfigurationError(Exception):
    """Raise this error whenever issues with the configuration are detected."""
    pass


class Configuration(object):
    """Base configuration class."""

    __slots__ = ['mci_url', 'data_resources_url', 'client_id',
                 'client_secret', 'oauth2_url', 'audience', 'github_client_id',
                 'github_client_secret', 'github_oauth2_url', 'github_profile_url',
                 'authserver_client_id', 'authserver_client_secret', 'authserver_oauth2_url',
                 'authserver_profile_url', 'authserver_redirect_url', 'environment', 'debug',
                 'testing']

    def find_json_config_file(self):
        """Find JSON configuration file.

        Locate the JSON configuration relative to the application path.

        Returns:
            str: Configuration file.

        Raises:
            ConfigurationError: If the configuration file cannot be found.

        """

        absolute_path = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(absolute_path, 'config.json')

        if os.path.exists(config_file) and os.path.isfile(config_file):
            return config_file
        else:
            raise ConfigurationError(
                'Cannot find configuration file in path {}.'.format(absolute_path))

    def load_json_config(self, config_file: str):
        """Load application configuration from JSON file.

        Args:
            config_file (str): The path and name of the configuration file to load.

        Returns:
            dict: Configuration object.

        Raises:
            ConfigurationError: If the configuration file doesn't exist or
                cannot be loaded because of a syntax erorr.

        """

        if not os.path.exists(config_file) or not os.path.isfile(config_file):
            raise ConfigurationError(
                'Error loading configuration file {}.'.format(config_file))

        try:
            with open(config_file, 'r') as f:
                data = json.load(f)
            return data
        except Exception:
            raise ConfigurationError(
                'Failed to load configuration file {}. Please check the configuration file.'.format(config_file))

    def from_json(self, environment='development'):
        """Load application configuration from JSON object based on the configuration type.

        Args:
            environment (str): The environment to load.

        Raises:
            ConfigurationError: If the JSON configuration cannot be loaded.

        """

        config_file = self.find_json_config_file()
        data = self.load_json_config(config_file)
        if environment in data.keys():
            fields = data[environment]
            try:
                self.mci_url = fields['data_trust']['mci_url']
                self.data_resources_url = fields['data_trust']['data_resources_url']
                self.client_id = fields['auth']['client_id']
                self.client_secret = fields['auth']['client_secret']
                self.oauth2_url = fields['auth']['oauth2_url']
                self.audience = fields['auth']['audience']
                self.github_client_id = fields['github']['client_id']
                self.github_client_secret = fields['github']['client_secret']
                self.github_oauth2_url = fields['github']['oauth2_url']
                self.github_profile_url = fields['github']['profile_url']

                self.authserver_client_id = fields['authserver']['client_id']
                self.authserver_client_secret = fields['authserver']['client_secret']
                self.authserver_oauth2_url = fields['authserver']['oauth2_url']
                self.authserver_profile_url = fields['authserver']['profile_url']
                self.authserver_redirect_url = fields['authserver']['redirect_url']

                self.environment = environment
                self.debug = True
                self.testing = True
            except Exception:
                raise ConfigurationError(
                    'Invalid key in JSON configuration. Please check the configuration.')
        else:
            raise ConfigurationError(
                'Cannot find environment \'{}\' in JSON configuration.')

    def from_env(self):
        """Load application configuration from environment.

        Note:
            The expectation is that the application will use the configuration
            file when loading for development or testing environments; however
            production will be loaded from environment variables.

        """

        self.mci_url = os.getenv('MCI_URL')
        self.data_resources_url = os.getenv('DATA_RESOURCE_URL')
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.oauth2_url = os.getenv('OAUTH2_URL')
        self.audience = os.getenv('AUDIENCE')
        self.github_client_id = os.getenv('GITHUB_CLIENT_ID')
        self.github_client_secret = os.getenv('GITHUB_CLIENT_SECRET')
        self.github_oauth2_url = os.getenv('GITHUB_OAUTH2_URL')
        self.github_profile_url = os.getenv('GITHUB_PROFILE_URL')
        self.environment = 'production'


class DevelopmentConfiguration(Configuration):
    """Development configuration class."""

    def __init__(self):
        self.from_json()
        self.debug = True
        self.testing = False


class TestConfiguration(Configuration):
    """Test Configuration class."""

    def __init__(self):
        self.from_json('testing')
        self.debug = True
        self.testing = True


class ProductionConfiguration(Configuration):
    """Production configuratuon class."""

    def __init__(self):
        self.from_env()
        self.debug = False
        self.testing = False


class ConfigurationFactory(object):
    """Application configuration factory."""

    @staticmethod
    def from_env():
        """Load configuration object from the Flask environment.

        Returns:
            object: Configuration object based on the environment.

        """
        environment = os.getenv('FLASK_ENV', 'development')
        return ConfigurationFactory.get_configuration(environment)

    @staticmethod
    def get_configuration(environment='development'):
        """Load configuration objects.

        Args:
            environment (str): The name of the environment to load configuration for.

        Returns:
            object: Configuration object based on the environment.

        Raises:
            ConfigurationError: If the specified environment is not one of 'development', 'testing', 'production'.

        """

        if environment.lower() == 'development':
            return DevelopmentConfiguration()
        elif environment.lower() == 'testing':
            return TestConfiguration()
        elif environment.lower() == 'production':
            return ProductionConfiguration()
        else:
            raise ConfigurationError(
                'Cannot find configuration object for configuration type \'{}\',').format(environment)

    @staticmethod
    def generate_secret_key():
        """Generate a secret for securing the Flask session.

        Returns:
            byte: A random string of bytes for secret.

        """
        environment = os.getenv('FLASK_ENV', 'development')
        if environment.lower() == 'production':
            return os.urandom(16)
        else:
            return 'supersecretaccesscode'
