# EDF Data Engineer Test

To set up this repo you will need to have uv installed, you can install uv by running `pip install uv`.
uv will manage the dependencies for you.

Navigate to the root directory of the repo and run `uv sync`.

Then navigate to the `scripts` directory and run `python sql_db.py`, this will create the database and populate it with the data from the csv file.

Then you can run
```bash
python data_quality_eval.py
python data_gov_access_control.py
python data_cleaning.py
python data_lineage_logging.py
```

which creates a csv with the output data for each script.


## Question 2

The current setup for dataset access policies for each department and dataset_id.

As the number of datasets, departments and roles within each department ie manager, analyst etc. increases, the number of policies will increase. Also increased fine tuning may be required, some employees may require access to certain datasets and another employee with the same role may require access to different datasets.

One solution for this is to have split the data_access_policies table into two tables, one with roles and another with policies for specific datasets. The role table would have secondary key(s) with the specific dataset(s) access level, this normalises the data and makes it easier to manage and update.

This approach would follow more closely to Identity and Access Management (IAM), where access is granted using roles and each role has a number of policies attached.

This makes adhering to the principle of least privilege (PoLP) easier, as each role can be assigned a specific set of permissions, and the permissions can be easily modified for a specific role.

