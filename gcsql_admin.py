"""sample helper class for working with the Cloud SQL admin API
"""
import os
from typing import List

import googleapiclient.discovery  # pylint: disable=E0401

from config import APP_CREDENTIALS


class CloudSqlAdmin:
    """Wrapper class for the Cloud SQL admin APIs
    """

    def __init__(self):
        """Initializes the service resource wrapper for Cloud SQL.
        """

        # Add the contained objects for entity-specific functionality.
        self.database = Database(self)
        self.instance = Instance(self)
        self.user = User(self)

        self.service: googleapiclient.discovery.Resource = service_client()

        self.response: dict = {}  # response to the last API call


class Database:
    """Handles database API calls as a contained member of CloudSqlAdmin.

    This class contains methods to wrap API calls documented here:
    https://developers.google.com/resources/api-libraries/documentation/sqladmin/v1beta4/python/latest/sqladmin_v1beta4.databases.html
    """

    def __init__(self, admin: CloudSqlAdmin):
        """Registers CloudSqlAdmin object for use in API calls.

        Args:
            admin: the container object, which is a CloudSqlADmin instance
        Returns:
            None
        """
        self.admin = admin

    def delete(self, project: str, instance: str, database: str) -> bool:
        """Deletes a database from a Cloud SQL instance.

        Args:
            project: project name
            instance: instance name
            database: database name

        Returns:
            True if database is successfully deleted, False if an error occurs.
        """
        request: googleapiclient.http.HttpRequest
        request = self.admin.service.databases().delete(
            project=project, instance=instance, database=database
        )
        try:
            self.admin.response = request.execute()
        except googleapiclient.errors.HttpError:
            self.admin.response = {"error": "googleapiclient.errors.HttpError"}
            return False
        if self.admin.response.get("error", ""):
            return False
        return True

    def get(self, project: str, instance: str, database: str) -> dict:
        """Get metadata for a database in a Cloud SQL instance.

        Args:
            project: project name
            instance: instance name
            database: database name

        Returns:
            A database object (dict) as documented here:
            https://developers.google.com/resources/api-libraries/documentation/sqladmin/v1beta4/python/latest/sqladmin_v1beta4.databases.html#get
            If an error occurred, the returned dict is empty.
        """
        request: googleapiclient.http.HttpRequest
        request = self.admin.service.databases().get(
            project=project, instance=instance, database=database
        )
        try:
            self.admin.response = request.execute()
        except googleapiclient.errors.HttpError:
            self.admin.response = {}
        return self.admin.response

    def insert(
        self,
        project: str,
        instance: str,
        database: str,
        charset: str = "utf8mb4",
        collation: str = "utf8mb4_unicode_520_ci",
        selflink: str = "",
    ) -> bool:
        """Creates a new database in a Cloud SQL instance

        Args:
            project: project name
            instance: Cloud SQL instance name
            database: name of the database
            charset: character set; defaults to "utf8mb4" which is a good choice
                for MySQL
            collation: collation setting; defaults to "utf8mb4_unicode_520_ci"
                which is a good choice for MySQL
            selflink: addressable URI for this database

        Returns:
            True if success, false if error occurred.
        """
        request_body = {
            "kind": "sql#user",
            "name": database,
            "charset": charset,
            "project": project,
            "instance": instance,
            "etag": "",
            "collation": collation,
            "selfLink": selflink,
        }
        request: googleapiclient.http.HttpRequest
        request = self.admin.service.databases().insert(
            project=project, instance=instance, body=request_body
        )
        self.admin.response = request.execute()
        if self.admin.response.get("error", ""):
            return False
        return True

    def list(self, project: str, instance: str) -> List[dict]:
        """Gets a list of the databases in a Cloud SQL instance.

        Args:
            project: project name
            instance: instance name

        Returns:
            List of databases; each database is a dict dict of properties.
            properties.
        """
        request: googleapiclient.http.HttpRequest
        request = self.admin.service.databases().list(
            project=project, instance=instance
        )
        self.admin.response = request.execute()
        return self.admin.response["items"]


class Instance:
    """Handles instance API calls as a contained member of CloudSqlAdmin.

    This class contains methods to wrap API calls documented here:
    https://developers.google.com/resources/api-libraries/documentation/sqladmin/v1beta4/python/latest/sqladmin_v1beta4.instances.html
    """

    def __init__(self, admin: CloudSqlAdmin):
        """Registers CloudSqlAdmin object for use in API calls.

        Args:
            admin: the container object, which is a CloudSqlADmin instance
        Returns:
            None
        """
        self.admin = admin

    def list(self, project: str) -> List[dict]:
        """Gets a list of the Cloud SQL instances for a project.

        Args:
            project: project name

        Returns:
            List of instances; each instance is a dict containing instance
            properties.
        """

        sql_instances: List[dict] = []
        request: googleapiclient.http.HttpRequest
        request = self.admin.service.instances().list(project=project)

        while request is not None:
            self.admin.response = request.execute()
            sql_instances.extend(self.admin.response["items"])
            request = self.admin.service.instances().list_next(
                previous_request=request, previous_response=self.admin.response
            )

        return sql_instances


class User:
    """Handles user API calls as a contained member of CloudSqlAdmin.

    This class contains methods to wrap API calls documented here:
    https://developers.google.com/resources/api-libraries/documentation/sqladmin/v1beta4/python/latest/sqladmin_v1beta4.users.html
    """

    def __init__(self, admin: CloudSqlAdmin):
        """Registers CloudSqlAdmin object for use in API calls.

        Args:
            admin: the container object, which is a CloudSqlADmin instance
        Returns:
            None
        """
        self.admin = admin

    def delete(self, project: str, instance: str, host: str, username: str) -> bool:
        """Deletes a user from a Cloud SQL instance

        Args:
            project: project name
            instance: Cloud SQL instance name
            host: the user's host address
            username: name for the new user

        Returns:
            True if user was deleted successfully, False if an error occurred.
        """
        request: googleapiclient.http.HttpRequest
        request = self.admin.service.users().delete(
            project=project, instance=instance, host=host, name=username
        )
        try:
            self.admin.response = request.execute()
        except googleapiclient.errors.HttpError:
            self.admin.response = {"error": "googleapiclient.errors.HttpError"}
            return False
        if self.admin.response.get("error", ""):
            return False
        return True

    def insert(
        self, project: str, instance: str, host: str, username: str, password: str
    ) -> bool:
        """Creates a new user in a Cloud SQL instance

        Args:
            project: project name
            instance: Cloud SQL instance name
            host: the host IP address from which this user can be used
                "localhost" = user must be on same machine as database
                "%" = user may be connected from any IP address
            username: name for the new user
            password: password for the new user

        Returns:
            True if success, false if error occurred.
        """
        request_body = {
            "kind": "sql#user",
            "name": username,
            "project": project,
            "instance": instance,
            "host": host,
            "etag": "",
            "password": password,
        }
        request: googleapiclient.http.HttpRequest
        request = self.admin.service.users().insert(
            project=project, instance=instance, body=request_body
        )
        self.admin.response = request.execute()
        if self.admin.response.get("error", ""):
            return False
        return True

    def list(self, project: str, instance: str) -> List[dict]:
        """Gets a list of the users in a Cloud SQL instance.

        Args:
            project: project name
            instance: instance name

        Returns:
            List of users; each user is a dict  of user properties.
        """
        request: googleapiclient.http.HttpRequest
        request = self.admin.service.users().list(project=project, instance=instance)
        self.admin.response = request.execute()
        return self.admin.response["items"]


def service_client(
    name: str = "sqladmin", version: str = "v1beta4"
) -> googleapiclient.discovery.Resource:
    """Creates the Cloud SLQL admin API service resource object.

    Args:
        name: the service name
        version: the API version

    Returns:
        googleapiclient.discovery.Resource - an instantiated and authenticated
        sqladmin resource, ready to use.
    """

    # Recommended best practice is to create a service account for the app
    # and set the GOOGLE_APPLICATION_CREDENTIALS environment variable to
    # point to the app registration JSON for the service account.

    # If the environment variable is not set but a filename has been specified,
    # in the APP_CREDENTIALS setting in config.py, those credentials are used.
    # Note that APP_CREDENTIALS should contain the name of an app registration
    # JSON file in the current working directory.
    env_var = "GOOGLE_APPLICATION_CREDENTIALS"
    if not os.environ.get(env_var) and APP_CREDENTIALS:
        os.environ[env_var] = f"{os.getcwd()}\\{APP_CREDENTIALS}"

    # If neither of the above options is provided, your current Google identity
    # will be used. Not recommended, and a warning will be displayed.

    return googleapiclient.discovery.build(name, version)
