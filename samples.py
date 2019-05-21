"""examples of how to use the CloudSqlAdmin wrapper class
"""
from pprint import pprint
from time import sleep
from timeit import default_timer
import uuid  # used to generate a random password for user_insert

from gcsql_admin import CloudSqlAdmin

# For convenience during dev/test, config.py contains some default values.
from config import MY_PROJECT, MY_INSTANCE


def databases_delete(project: str, instance: str, database: str):
    """Deletes a database from a Cloud SQL instance.
    Demonstrates use of CloudSqlAdmin.databases.delete() method.

    Args:
        project: name of the Cloud SQL project
        instance: name of the Cloud SQL instance
        database: database name

    Returns:
        None. Database is deleted, and a summary is printed to the console.
    """
    sql_admin = CloudSqlAdmin()
    if sql_admin.databases.delete(project, instance, database):
        print(f"database {database} deleted, status = {sql_admin.response['status']}")
    else:
        print(f"ERROR deleting database {database}!")
        print(sql_admin.response["error"])


def databases_get(project: str, instance: str, database: str):
    """gets metadata for database in a Cloud SQL instance.
    Demonstrates use of CloudSqlAdmin.databases.get() method.

    Args:
        project: name of the Cloud SQL project
        instance: name of the Cloud SQL instance
        database: database name

    Returns:
        None. Prints the database metadata to the console.
    """
    sql_admin = CloudSqlAdmin()
    metadata = sql_admin.databases.get(project, instance, database)
    print(f"metadata for project {project}, instance {instance}, database {database}:")
    pprint(metadata)


def databases_insert(project: str, instance: str, database: str):
    """Inserts a new database in a Cloud SQL instance.
    Demonstrates use of CloudSqlAdmin.databases.insert() method.

    Args:
        project: name of the Cloud SQL project
        instance: name of the Cloud SQL instance
        database: name of the database

    Returns:
        None. database is created, and a summary is printed to the console.
    """
    sql_admin = CloudSqlAdmin()

    if sql_admin.databases.insert(project, instance, database):
        print(f"Database created: {database}, status = {sql_admin.response['status']}")
    else:
        print(f"ERROR creating database: {sql_admin.response}")


def databases_insert_delete():
    """Inserts a new database, then deletes the database.
    """
    databases_insert(MY_PROJECT, MY_INSTANCE, "testdb")
    databases_get(MY_PROJECT, MY_INSTANCE, "testdb")
    databases_delete(MY_PROJECT, MY_INSTANCE, "testdb")
    databases_get(MY_PROJECT, MY_INSTANCE, "testdb")


def databases_list(project: str, instance: str):
    """Prints a summary of the databases in a Cloud SQL instance.
    Demonstrates use of CloudSqlAdmin.databases.list() method.

    Args:
        project: name of the Cloud SQL project
        instance: name of the Cloud SQL instance

    Returns:
        None - prints output to console.
    """
    print(f"PROJECT/INSTANCE: {project} / {instance}")

    sql_admin = CloudSqlAdmin()
    for database in sql_admin.databases.list(project, instance):
        print(f"        Database: {database['name']}")


def instances_delete(project: str, instance: str):
    """Deletes a Cloud SQL instance.
    Demonstrates use of CloudSqlAdmin.instances.delete() method.

    Args:
        project: name of the Cloud SQL project
        instance: name of the Cloud SQL instance

    Returns:
        None. Instance is deleted, and a summary is printed to the console.
    """
    sql_admin = CloudSqlAdmin()
    if sql_admin.instances.delete(project, instance):
        print(f"instance {instance} deleted, status = {sql_admin.response['status']}")
    else:
        print(f"ERROR deleting instance {instance}!")
        print(sql_admin.response["error"])


def instances_get(project: str, instance: str):
    """gets metadata for a Cloud SQL instance.
    Demonstrates use of CloudSqlAdmin.instances.get() method.

    Args:
        project: name of the Cloud SQL project
        instance: name of the Cloud SQL instance

    Returns:
        None. Prints the instance metadata to the console.
    """
    sql_admin = CloudSqlAdmin()
    metadata = sql_admin.instances.get(project, instance)
    print(f"metadata for project {project}, instance {instance}:")
    pprint(metadata)


def instances_insert(
    project: str, instance_name: str, root_password: str, database_type: str = "MySQL"
):
    """Creates a new Cloud SQL instance.
    Demonstrates use of CloudSqlAdmin.instances.insert() method.

    Args:
        project: name of the Cloud SQL project
        instance_name: name of the Cloud SQL instance to be created
        root_password: password for root user
        database_type: the type of database; must be "MySQL" or "PostgreSQL"

    Returns:
        None. instance is created, and a summary is printed to the console.
    """
    sql_admin = CloudSqlAdmin()
    if sql_admin.instances.insert(
        project=project,
        instance_name=instance_name,
        root_password=root_password,
        database_type=database_type,
    ):
        print(
            f"Cloud SQL instance {instance_name} created, status = {sql_admin.response['status']}"
        )
    else:
        print(f"ERROR creating instance {instance_name}: {sql_admin.response}")


def instances_list(project: str):
    """Prints a summary of the list of Cloud SQL instances in a project.
    Demonstrates use of CloudSqlAdmin.instances.list() method.

    Args:
        project: name of the Cloud SQL project

    Returns:
        None - prints output to console.
    """
    print(f"PROJECT NAME: {project}")

    sql_admin = CloudSqlAdmin()
    for instance in sql_admin.instances.list(project):
        print(f"Instance -->: {instance['name']}")
        print(f"  DB Version: {instance['databaseVersion']}")
        print(f"        Tier: {instance['settings']['tier']}")
        print(f"     Pricing: {instance['settings']['pricingPlan']}")
        print(f"       State: {instance['state']}")


def instance_state_polling(project: str, instance: str):
    """Prints state of an instance to the console every 5 seconds.
    """
    start_time = default_timer()
    sql_admin = CloudSqlAdmin()
    while True:
        metadata = sql_admin.instances.get(project, instance)
        if "state" in metadata:
            state = metadata["state"]
        else:
            state = "not found"
        print(
            (
                f"{default_timer() - start_time:9.4} seconds elapsed - "
                f"project: {project}, instance: {instance}, state: {state}"
            )
        )
        sleep(5)


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


def users_delete(project: str, instance: str, host: str, username: str):
    """Deletes a user from a Cloud SQL instance.
    Demonstrates use of CloudSqlAdmin.users.delete() method.

    Args:
        project: name of the Cloud SQL project
        instance: name of the Cloud SQL instance
        host: the user's host IP address
        username: user name

    Returns:
        None. User is deleted, and a summary is printed to the console.
    """
    sql_admin = CloudSqlAdmin()

    if sql_admin.users.delete(project, instance, host, username):
        print(f"user {username} deleted, status = {sql_admin.response['status']}")
    else:
        print(f"ERROR deleting user {username}!")
        print(sql_admin.response["error"])


def users_insert(project: str, instance: str, host: str, username: str, password: str):
    """Inserts a new user in a Cloud SQL instance.
    Demonstrates use of CloudSqlAdmin.users.insert() method.

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

    if sql_admin.users.insert(project, instance, host, username, password):
        print(f"User created: {username}")
    else:
        print(f"ERROR inserting user: {sql_admin.response}")


def users_insert_delete():
    """Inserts a new user, then deletes the user.
    """

    users_insert(
        project=MY_PROJECT,
        instance=MY_INSTANCE,
        host="localhost",
        username="testuser",
        password=str(uuid.uuid4()),
    )

    users_list(MY_PROJECT, MY_INSTANCE)  # this list will include testuser

    users_delete(
        project=MY_PROJECT, instance=MY_INSTANCE, host="localhost", username="testuser"
    )

    users_list(MY_PROJECT, MY_INSTANCE)  # this list will not include testuser


def users_list(project: str, instance: str):
    """Prints a summary of the users in a Cloud SQL instance.
    Demonstrates use of CloudSqlAdmin.users.list() method.

    Args:
        project: name of the Cloud SQL project
        instance: name of the Cloud SQL instance

    Returns:
        None - prints output to console.
    """
    print(f"PROJECT/INSTANCE: {project} / {instance}")

    sql_admin = CloudSqlAdmin()
    for user in sql_admin.users.list(project, instance):
        print(f"       User Name: {user['name']}")


if __name__ == "__main__":
    # typical examples of running the samples:
    # databases_insert_delete()
    databases_list(MY_PROJECT, MY_INSTANCE)
    # instances_get(MY_PROJECT, MY_INSTANCE)
    instances_list(MY_PROJECT)
    tiers_list(MY_PROJECT)
    # users_insert_delete()
    pass
