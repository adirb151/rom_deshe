# Testing Meshi Project
## Django Website Tests
These are tests for the website, they test its responsivness, if it displays correct information, if it doesn't display incorrect information and other functionality.

All of the following tests are located in [tests.py](djangonautic/queries/tests.py).

To run these tests, run these commands from the *rom_deshe* folder:
```
cd ./djangonautic
python3 manage.py test
```
For more information regarding running tests, please see [this documentation](https://docs.djangoproject.com/en/4.0/topics/testsing/overview).

|Test |Goal  |Good Scenario |Bad Scenario |
|-----|------|--------------|-------------|
|test_get_homepage|Test if the homepage can be accessed|The website is responsive and may be accessed|The website isn't responsive and cannot be accessed|
|test_add_query|Test if a query is added to the database|A query has been added and the number of queries is updated|A query hasn't added|
|test_delete_query|Test if a query is deleted from the database|A query has been removed and the number of queries is updated|A query hasn't been removed|
|test_filter_by_target|Test if you can filter queries by their target name|The query list page displays the correctly filtered queries|The query list page displays nothing|
|test_bad_filter_by_target|Test if you can't filter queries by a bad filter|The query list page displays nothing|N/A|
|test_query_detail|Test if you can access the details of an existing query|The query details page displays the specific query's information|The query details page can't be accessed|
|test_bad_query_detail|Test if you can't access the details of a nonexistent query|The query details page can't be accesed|N/A|
