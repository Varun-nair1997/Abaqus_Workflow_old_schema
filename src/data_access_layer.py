__author__ = "Varun Nair"

import sqlite3
import json
import Database_Handler as DH


schema_columns = [
    "$schema", "identifier", "title", "creator", "creator_ORCID",
    "creator_affiliation", "creator_institute", "creator_group", "contributor",
    "contributor_ORCID", "contributor_affiliation", "contributor_institute",
    "contributor_group", "date", "shared_with", "description", "rights",
    "rights_holder", "funder_name", "fund_identifier", "publisher", "relation",
    "keywords", "software", "software_version", "system", "system_version",
    "processor_specifications", "input_path", "results_path", "RVE_size",
    "RVE_continuity", "discretization_type", "discretization_unit_size",
    "discretization_count", "origin.software", "origin.software Version",
    "origin.system", "origin.system Version", "origin.Input Path",
    "origin.Results Path", "global_temperature", "mechanical_BC", "material",
    "stress.stress_11", "stress.stress_22", "stress.stress_33",
    "stress.stress_12", "stress.stress_13", "stress.stress_23",
    "total_strain.strain_11", "total_strain.strain_22",
    "total_strain.strain_33", "total_strain.strain_12",
    "total_strain.strain_13", "total_strain.strain_23",
    "plastic_strain.plastic_strain_11", "plastic_strain.plastic_strain_22",
    "plastic_strain.plastic_strain_33", "plastic_strain.plastic_strain_12",
    "plastic_strain.plastic_strain_13", "plastic_strain.plastic_strain_23",
    "units.Stress", "units.Strain", "units.Length", "units.Angle",
    "units.Temperature", "units.Force", "units.Stiffness"
]





def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


# Sample JSON object
data = DH.Read_Database_From_Json("p_test.json")


# Serialize JSON object to a string
json_data = json.dumps(data)

# Connect to SQLite database (or create it if it doesn't exist)
connection = sqlite3.connect("sim_data_store1.db")
cursor = connection.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS [sim_data] (
   [$schema] TEXT,
   [identifier] TEXT,
   [title] TEXT,
   [creator] TEXT,
   [creator_ORCID] TEXT,
   [creator_affiliation] TEXT,
   [creator_institute] TEXT,
   [creator_group] TEXT,
   [contributor] TEXT,
   [contributor_ORCID] TEXT,
   [contributor_affiliation] TEXT,
   [contributor_institute] TEXT,
   [contributor_group] TEXT,
   [date] TEXT,
   [shared_with] TEXT,
   [description] TEXT,
   [rights] TEXT,
   [rights_holder] TEXT,
   [funder_name] TEXT,
   [fund_identifier] TEXT,
   [publisher] TEXT,
   [relation] TEXT,
   [keywords] TEXT,
   [software] TEXT,
   [software_version] TEXT,
   [system] TEXT,
   [system_version] TEXT,
   [processor_specifications] TEXT,
   [input_path] TEXT,
   [results_path] TEXT,
   [RVE_size] TEXT,
   [RVE_continuity] INT,
   [discretization_type] TEXT,
   [discretization_unit_size] TEXT,
   [discretization_count] INT,
   [origin.software] TEXT,
   [origin.software Version] TEXT,
   [origin.system] TEXT,
   [origin.system Version] TEXT,
   [origin.Input Path] TEXT,
   [origin.Results Path] TEXT,
   [global_temperature] INT,
   [mechanical_BC] TEXT,
   [material] TEXT,
   [stress.stress_11] TEXT,
   [stress.stress_22] TEXT,
   [stress.stress_33] TEXT,
   [stress.stress_12] TEXT,
   [stress.stress_13] TEXT,
   [stress.stress_23] TEXT,
   [total_strain.strain_11] TEXT,
   [total_strain.strain_22] TEXT,
   [total_strain.strain_33] TEXT,
   [total_strain.strain_12] TEXT,
   [total_strain.strain_13] TEXT,
   [total_strain.strain_23] TEXT,
   [plastic_strain.plastic_strain_11] TEXT,
   [plastic_strain.plastic_strain_22] TEXT,
   [plastic_strain.plastic_strain_33] TEXT,
   [plastic_strain.plastic_strain_12] TEXT,
   [plastic_strain.plastic_strain_13] TEXT,
   [plastic_strain.plastic_strain_23] TEXT,
   [units.Stress] TEXT,
   [units.Strain] INT,
   [units.Length] TEXT,
   [units.Angle] TEXT,
   [units.Temperature] TEXT,
   [units.Force] TEXT,
   [units.Stiffness] TEXT
   );

""")







# Insert JSON data into the table
print(type(data))

test_Obj = DH.Read_Database_From_Json("c779c1a4.json")

print(test_Obj["material"][0]["material_identifier"])

cursor.execute("INSERT INTO sim_data VALUES (?)", (test_Obj,))
connection.commit()
print("done")
# Retrieve and deserialize JSON data
cursor.execute("SELECT * FROM sim_data")
retrieved_data = cursor.fetchone()[0]  # Fetch the first row's 'info' column
deserialized_data = json.loads(retrieved_data)

# Output the retrieved JSON data
print("Retrieved JSON:", deserialized_data)

# Clean up
cursor.close()
connection.close()
