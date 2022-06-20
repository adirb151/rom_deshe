# Testing Meshi Project
## Django Website Unit Tests
These are tests for the website located in [tests.py](djangonautic/queries/tests.py), they test its responsivness, if it displays correct information, if it doesn't display incorrect information and other functionality. They all use a "puppet" client that simulates a real client and can send and receive requests.

To run these tests, run these commands from the *rom_deshe* folder:
```
cd ./djangonautic
python3 manage.py test
```
For more information regarding running tests in Django, please see [this documentation](https://docs.djangoproject.com/en/4.0/topics/testing/overview/).

|Test |Goal  |Good Scenario |Bad Scenario |
|-----|------|--------------|-------------|
|test_get_homepage|Test if the homepage can be accessed|The website is responsive and may be accessed|The website isn't responsive and cannot be accessed|
|test_add_query|Test if a query is added to the database|A query has been added and the number of queries is updated|A query hasn't added|
|test_delete_query|Test if a query is deleted from the database|A query has been removed and the number of queries is updated|A query hasn't been removed|
|test_filter_by_target|Test if you can filter queries by their target name|The query list page displays the correctly filtered queries|The query list page displays nothing|
|test_bad_filter_by_target|Test if you can't filter queries by a bad filter|The query list page displays nothing|N/A|
|test_query_detail|Test if you can access the details of an existing query|The query details page displays the specific query's information|The query details page can't be accessed|
|test_bad_query_detail|Test if you can't access the details of a nonexistent query|The query details page can't be accesed|N/A|

## Email Receiver Unit Tests
These are tests from [test_email_receiver.py](test_email_receiver.py) for the [email_receiver.py](email_receiver.py) file, which is responsible for receiving emails from the competition containing the data of the query to be processed.

To run these tests, from the *rom_deshe* folder run the command `python3 test_email_receiver.py`.
|Test |Goal  |Good Scenario |Bad Scenario |
|-----|------|--------------|-------------|
|test_bad_email_connect|Test that you may not connect to the email with incorrect credentials|Establishing a connection has failed and an error message is shown|N/A|
|test_email_connect|Test that you may connect to the email with correct credentials|A connection is established|Not able to establish a connection and an error message is shown|
|test_send_and_receive_mail|Test that you may send an email using the connection established beforehand, and then test that you are able to receive that same email via the same connection and view its data|An email containing a protein sequence has been sent and once received, its target and data are printed|Sending and receiving a message has fail and an error message is printed|

## Database Unit Tests
These are tests for the [db_utils.py](db_utils.py) file located in [db_utils_tests.py](db_utils_tests.py). these tests are responsible to different scenarios of adding new queries to the database and updating an existing query in the database. They all use a “puppet” query that simulates a real target of the CASP competition.

To run these tests, run `python3 db_utils_tests.py` from the *rom_deshe* folder.

|Test	|Goal	|Good Scenarios	|Bad Scenarios|
|-----|-----|---------------|-------------|
|check_add_happy|Test if you can add a new valid query to the database|The query was added to the database|The query wasn’t added to the database|
|check_add_bad|Test if you can’t add a new query to the database with invalid parameters|The database remains without any change|The database has changed, and invalid query was added|
|check_update_happy|Test if you can update the log of an existing query in the database|The log of the query was updated in the database|The log of the query wasn’t updated in the database|
|check_update_sad|Test if you can’t update the log of a query which is not in the database|The database remains without change|The database has changed|
|check_update_status|Test if you can update the status of a query in the database|The status of the query was updated in the database|The status of the query was not updated in the database, or was updated with the wrong status|
|check_add_same_target|Test if you can’t add a new query to the database when there is already a query in the database with the same target name|The database remains without changes|The database has changed, and a new query with the same target name was added|

