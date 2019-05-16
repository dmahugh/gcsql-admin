# Cloud SQL Admin API

There are [REST APIs](https://cloud.google.com/sql/docs/mysql/admin-api/v1beta4/) for managing Cloud SQL services. If you're already comfortable with directly calling REST APIs, the [API Explorer](https://developers.google.com/apis-explorer/#p/sqladmin/v1beta4/) is a great way to get a feel for what's possible.

For most developers, however, the [Cloud SQL client libraries](https://cloud.google.com/sql/docs/mysql/admin-api/libraries) are a better option. Each client library provides a language-specific API that sits on top of the underlying REST APIs, which will make you much more productive. If you use the REST APIs you'll need to take on management of [OAuth 2.0 authentication flows](https://cloud.google.com/docs/authentication/getting-started) and other details, whereas the client libraries let you get right to work solving business problems, because they handle those things for you.

### Client library examples

As a typical example of using the [Python client library](https://developers.google.com/resources/api-libraries/documentation/sqladmin/v1beta4/python/latest/) to call the Cloud SQL Admin API, here's how to insert a new user into a Cloud SQL instance:

```python
# instantiate the service resource
import googleapiclient.discovery
service = googleapiclient.discovery.build("sqladmin", "v1beta4")

# assemble the request body
request_body = {
    "kind": "sql#user",
    "name": "NEW_USER_NAME",
    "project": "PROJECT_NAME",
    "instance": "INSTANCE_NAME",
    "host": "HOST_IP_ADDRESS",
    "etag": "DEPRECATED",
    "password": "PASSWORD",
}

# make the API call
request = service.users().insert(
    project="MY_PROJECT",
    instance="MY_INSTANCE",
    body=request_body
    )
response = request.execute()

# check for errors
if response.get("error", ""):
    # the request failed
    print(response["error"])
# the request succeeded
```

If you're requesting a list of entities from the Cloud SQL Admin API, you may need to deal with pagination. For example, here's how to retrieve a list of the Cloud SQL instances in a project:

```python
instances = []
request = self.admin.service.instances().list(project="MY_PROJECT")
while request is not None:
    response = request.execute()
    instances.extend(response["items"]) # add these instances to the list
    # get the next page of results:
    request = self.admin.service.instances().list_next(
        previous_request=request, previous_response=response
    )
# instances now contains a complete list of instances for this project
```

### But what about auth?

Hold on a second &mdash; the above examples don't include any authentication! Surely Cloud SQL won't let just anyone have read/write access to our data. What's going on?

The Cloud SQL Admin APIs (and all other Google Cloud Platform APIs) have multiple options for handling authentication when you attempt to make an API call. At a minimum, if you don't bother to do anything at all about authentication, the default mechanism is that the API will look to the current Google account you're logged in under (the one you see in the top right corner if you browser to [google.com](https://google.com)), and use _that_ identity.

This is not a good approach for a variety of reasons, but it works if you're in a hurry and just want to check something out. For example, you can past the above add-user code sample into a ```.py``` file, replace all the placeholders with your own information, and the sample will run. If you do this, you'll see this warning displayed on the console:

```
UserWarning: Your application has authenticated using end user credentials from Google Cloud SDK. We recommend that most server applications use service accounts instead. If your application continues to use end user credentials from Cloud SDK, you might receive a "quota exceeded" or "API not enabled" error. For more information about service accounts, see https://cloud.google.com/docs/authentication/

warnings.warn(_CLOUD_SDK_CREDENTIALS_WARNING)
```

That URL for the [Authentication Overview](https://cloud.google.com/docs/authentication/) will lead you to information about the various other options available, such as using an API key (works for some APIs but not all of them), using an environment variable to point to an app registration JSON file, or kicking off an OAuth 2.0 authentication flow.
