# EDF Data Engineer Test

To set up this repo you will need to have uv installed, you can install uv by running `pip install uv`.
uv will manage the dependencies for you.

Navigate to the root directory of the repo and run `uv sync`.

Then you can run:
```bash
cd scripts
uv run python sql_db.py
uv run python data_quality_eval.py
uv run python data_gov_access_control.py
uv run python data_cleaning.py
uv run python data_lineage_logging.py
```

which creates a csv or log file with the output data for each script.


## Question 2

The current setup for dataset access policies for each department and dataset_id.

As the number of datasets, departments and roles within each department ie manager, analyst etc. increases, the number of policies will increase. Also increased fine tuning may be required, some employees may require access to certain datasets and another employee with the same role may require access to different datasets.

One solution for this is to have split the data_access_policies table into two tables, one with roles and another with policies for specific datasets. The role table would have secondary key(s) with the specific dataset(s) access level, this normalises the data and makes it easier to manage and update.

This approach would follow more closely to Identity and Access Management (IAM), where access is granted using roles and each role has a number of policies attached.

This makes adhering to the principle of least privilege (PoLP) easier, as each role can be assigned a specific set of permissions, and the permissions can be easily modified for a specific role.

# General notes

I know that it's not strictly necessary to use classes for this task, but I wanted to show that I can use classes and OOP principles.

I am mainly using Python for this task rather than SQL as many methods are in pandas and other libraries meaning less code to do the same job. Also there are other operations like data logging and writing to local files that would not be possible/recommended as SQL queries. However, my script does include one SELECT SQL query to extract data from an SQL database to show a realistic use case of how Python and pandas can be used to interact with SQL databases.

I mainly use vectorised pandas operations for data manipulation as they are more efficient than looping.

If I was doing logging in a real project I would send the custom logs to a cloud logging service like AWS CloudWatch.

I am using uv for package management as it has detailed dependency resolution, is faster, has less commands, and is more automatic than pip.

If you have any issues setting this up please let me know benldale93@gmail.com.