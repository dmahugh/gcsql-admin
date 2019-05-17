# gcsql-admin
The great thing about working with an SQL-oriented cloud database service such as Cloud SQL is that you can use all of the same tools and libraries that you've used with other SQL databases. For example, [here's a sample](https://github.com/dmahugh/weather-tracker) that uses ```pymysql``` to read and write data to a MySQL database in Cloud SQL, and the code in that sample would be exactly the same if the MySQL database were hosted locally on my laptop or anywhere else. Standardization for the win!

The _administration_ of a SQL database in the cloud, however, can be a different story. Each vendor typically has their own approach to deploying a database, setting up users and roles, or configuring replication, auto-scaling, billing, and other options.

The [Google Cloud Platform console](https://console.cloud.google.com) provides a web interface that spans the full range of GCP services, including Cloud SQL. Just click "go to the SQL dashboard" to get to the SQL dashboard, and there you'll find options for creating and managing instances.

You can do pretty much anything in the web console, but if you'd like to _automate_ administrative tasks (to handle CI and/or testing, for example), then you'll need to use the REST API or client libraries.

I've recently started working with the Python client library for this API, and this repo contains an overview of some things I've learned, as well as a few code samples that demonstrate how to handle common administrative tasks. Here's what's included:

* A brief overview of [GCP projects and Cloud SQL instances](projects-instances.md), which may be useful if you're creating your first project.
* Some information about the [Cloud SQL Admin API](admin-api.md), including examples of how to use the Python client library.
* An [overview of a Python helper class](helper-class.md) to simplify working with the admin APIs.
* Source code for the helper class is [here](gcsql_admin.py).
* Samples that show how to use the helper class are [here](samples.py).

I'm using Python 3.7, but the same general concepts should apply to any supported language.

## Running the samples

To run the sample code, follow these steps:

* Read the [overview](helper-class.md) of the ```CloudSqlAdmin``` class.
* You should have Python 3.6 or higher installed. You can get Python from [python.org](https://www.python.org/).
* Clone this repo into a local project folder.
* At a command prompt in the project folder, install the Google API Client Library for Python as covered [here](https://developers.google.com/api-client-library/python/start/installation).
* You'll need a Google account to proceed. If you don't have one, [sign up here](https://support.google.com/accounts/answer/27441?hl=en).
* The samples assume you already have a GCP project created, and a Cloud SQL instance within the project. If you don't have these, [here's where to create a GCP project](https://console.developers.google.com/cloud-resource-manager) and [here's how to create a Cloud SQL instance](https://cloud.google.com/sql/docs/mysql/create-instance).
* Edit the ```config.py``` file and set MY_PROJECT and MY_INSTANCE to the names of your project and instance.
* Enable the Cloud SQL Admin API for your project, as covered [here](https://console.cloud.google.com/flows/enableapi?apiid=sqladmin
).
* The samples can be run under your own Google identity, but this approach is not recommended and may be slow or unreliable. The best practice is to create a service account and download an application credentials JSON file for it, as covered [here](https://cloud.google.com/iam/docs/creating-managing-service-account-keys). If you do that, edit ```config.py``` to set APP_CREDENTIALS to the name of the JSON file in the project folder, and the service account will be used by default.
* The quickest way to run samples is to try some of the examples at the bottom of the ```samples.py``` file. There are several examples there, commented out &mdash; just remove the ```#``` at the start of a line and run ```sample.py``` to run that sample. Each sample is in a function in that same file, and most are just a few lines of code.

## Resources

* The Python client library documentation for the Cloud SQL Admin API: [https://developers.google.com/resources/api-libraries/documentation/sqladmin/v1beta4/python/latest/](https://developers.google.com/resources/api-libraries/documentation/sqladmin/v1beta4/python/latest/)
* Overview of libraries and samples for Cloud SQL (all languages): [https://cloud.google.com/sql/docs/mysql/admin-api/libraries](https://cloud.google.com/sql/docs/mysql/admin-api/libraries)
* To register an application and enable the Admin API, start here: [https://console.cloud.google.com/flows/enableapi?apiid=sqladmin](https://console.cloud.google.com/flows/enableapi?apiid=sqladmin)
* Cloud SQL Admin REST API reference documentation: [https://cloud.google.com/sql/docs/mysql/admin-api/v1beta4/](https://cloud.google.com/sql/docs/mysql/admin-api/v1beta4/)
* Documentation for the Google Cloud Platform management console: [https://cloud.google.com/cloud-console/](https://cloud.google.com/cloud-console/)
* Google Cloud SQL discussion forum: [https://groups.google.com/forum/#!forum/google-cloud-sql-discuss](https://groups.google.com/forum/#!forum/google-cloud-sql-discuss)
