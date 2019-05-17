"""examples of how to use the CloudSqlAdmin wrapper class
"""
from pprint import pprint
import uuid  # used to generate a random password for user_insert

from gcsql_admin import CloudSqlAdmin

# For convenience during dev/test, config.py contains some default values.
from config import MY_PROJECT, MY_INSTANCE


def database_delete(project: str, instance: str, database: str):
    """Deletes a database from a Cloud SQL instance.
    Demonstrates use of CloudSqlAdmin.database.delete() method.

    Args:
        project: name of the Cloud SQL project
        instance: name of the Cloud SQL instance
        database: database name

    Returns:
        None. Database is deleted, and a summary is printed to the console.
    """
    sql_admin = CloudSqlAdmin()
    if sql_admin.database.delete(project, instance, database):
        print(f"database {database} deleted, status = {sql_admin.response['status']}")
    else:
        print(f"ERROR deleting database {database}!")
        print(sql_admin.response["error"])


def database_get(project: str, instance: str, database: str):
    """gets metadata for database in a Cloud SQL instance.
    Demonstrates use of CloudSqlAdmin.database.get() method.

    Args:
        project: name of the Cloud SQL project
        instance: name of the Cloud SQL instance
        database: database name

    Returns:
        None. Prints the database metadata to the console.
    """
    sql_admin = CloudSqlAdmin()
    metadata = sql_admin.database.get(project, instance, database)
    print(f"metadata for project {project}, instance {instance}, database {database}:")
    pprint(metadata)


def database_insert(project: str, instance: str, database: str):
    """Inserts a new database in a Cloud SQL instance.
    Demonstrates use of CloudSqlAdmin.database.insert() method.

    Args:
        project: name of the Cloud SQL project
        instance: name of the Cloud SQL instance
        database: name of the database

    Returns:
        None. database is created, and a summary is printed to the console.
    """
    sql_admin = CloudSqlAdmin()

    if sql_admin.database.insert(project, instance, database):
        print(f"Database created: {database}, status = {sql_admin.response['status']}")
    else:
        print(f"ERROR creating database: {sql_admin.response}")


def database_insert_delete():
    """Inserts a new database, then deletes the database.
    """
    database_insert(MY_PROJECT, MY_INSTANCE, "testdb")
    database_get(MY_PROJECT, MY_INSTANCE, "testdb")
    database_delete(MY_PROJECT, MY_INSTANCE, "testdb")
    database_get(MY_PROJECT, MY_INSTANCE, "testdb")


def database_list(project: str, instance: str):
    """Prints a summary of the databases in a Cloud SQL instance.
    Demonstrates use of CloudSqlAdmin.database.list() method.

    Args:
        project: name of the Cloud SQL project
        instance: name of the Cloud SQL instance

    Returns:
        None - prints output to console.
    """
    print(f"PROJECT/INSTANCE: {project} / {instance}")

    sql_admin = CloudSqlAdmin()
    for database in sql_admin.database.list(project, instance):
        print(f"        Database: {database['name']}")


def instance_get(project: str, instance: str):
    """gets metadata for a Cloud SQL instance.
    Demonstrates use of CloudSqlAdmin.instance.get() method.

    Args:
        project: name of the Cloud SQL project
        instance: name of the Cloud SQL instance

    Returns:
        None. Prints the instance metadata to the console.
    """
    sql_admin = CloudSqlAdmin()
    metadata = sql_admin.instance.get(project, instance)
    print(f"metadata for project {project}, instance {instance}:")
    pprint(metadata)


def instance_list(project: str):
    """Prints a summary of the list of Cloud SQL instances in a project.
    Demonstrates use of CloudSqlAdmin.instance.list() method.

    Args:
        project: name of the Cloud SQL project

    Returns:
        None - prints output to console.
    """
    print(f"PROJECT NAME: {project}")

    sql_admin = CloudSqlAdmin()
    for instance in sql_admin.instance.list(project):
        print(f"Instance -->: {instance['name']}")
        print(f"  DB Version: {instance['databaseVersion']}")
        print(f"        Tier: {instance['settings']['tier']}")
        print(f"     Pricing: {instance['settings']['pricingPlan']}")
        print(f"       State: {instance['state']}")


def tiers_list(project: str):
    """Prints out the available Cloud SQL tiers (machine types) for a project.

    This sample demonstrates how to use the CloudSqlAdmin.service resource to
    make an API call that has not been implemented in the entity-specific
    classes contained in CloudSqlAdmin.

    Documentation for the API used:
    https://developers.google.com/resources/api-libraries/documentation/sqladmin/v1beta4/python/latest/sqladmin_v1beta4.tiers.html
    """
    sql_admin = CloudSqlAdmin()
    request = sql_admin.service.tiers().list(project=project)
    response: dict = request.execute()
    print(response)


def user_delete(project: str, instance: str, host: str, username: str):
    """Deletes a user from a Cloud SQL instance.
    Demonstrates use of CloudSqlAdmin.user.delete() method.

    Args:
        project: name of the Cloud SQL project
        instance: name of the Cloud SQL instance
        host: the user's host IP address
        username: user name

    Returns:
        None. User is deleted, and a summary is printed to the console.
    """
    sql_admin = CloudSqlAdmin()

    if sql_admin.user.delete(project, instance, host, username):
        print(f"user {username} deleted, status = {sql_admin.response['status']}")
    else:
        print(f"ERROR deleting user {username}!")
        print(sql_admin.response["error"])


def user_insert(project: str, instance: str, host: str, username: str, password: str):
    """Inserts a new user in a Cloud SQL instance.
    Demonstrates use of CloudSqlAdmin.user.insert() method.

    Args:
        project: name of the Cloud SQL project
        instance: name of the Cloud SQL instance
        host: the user's host IP address
        username: user name
        password: password for the new user

    Returns:
        None. User is created, and a summary is printed to the console.
    """
    sql_admin = CloudSqlAdmin()

    if sql_admin.user.insert(project, instance, host, username, password):
        print(f"User created: {username}")
    else:
        print(f"ERROR inserting user: {sql_admin.response}")


def user_insert_delete():
    """Inserts a new user, then deletes the user.
    """

    user_insert(
        project=MY_PROJECT,
        instance=MY_INSTANCE,
        host="localhost",
        username="testuser",
        password=str(uuid.uuid4()),
    )

    user_list(MY_PROJECT, MY_INSTANCE)  # this list will include testuser

    user_delete(
        project=MY_PROJECT, instance=MY_INSTANCE, host="localhost", username="testuser"
    )

    user_list(MY_PROJECT, MY_INSTANCE)  # this list will not include testuser


def user_list(project: str, instance: str):
    """Prints a summary of the users in a Cloud SQL instance.
    Demonstrates use of CloudSqlAdmin.user.list() method.

    Args:
        project: name of the Cloud SQL project
        instance: name of the Cloud SQL instance

    Returns:
        None - prints output to console.
    """
    print(f"PROJECT/INSTANCE: {project} / {instance}")

    sql_admin = CloudSqlAdmin()
    for user in sql_admin.user.list(project, instance):
        print(f"       User Name: {user['name']}")


if __name__ == "__main__":
    # examples of running the samples:
    # database_insert_delete()
    # database_list(MY_PROJECT, MY_INSTANCE)
    instance_get(MY_PROJECT, MY_INSTANCE)
    # instance_list(MY_PROJECT)
    # tiers_list(MY_PROJECT)
    # user_insert_delete()
    pass
