# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 07.04.22
Time: 18:17

"""
import numpy as np
import Key_Parser as KP
import Key_Generator as KG
import Database_Handler as DH
import Result_Parser as RP
import Meta_reader as MR
import Load_Creator as LC
import Key_Folder_Creator as KFC
import Geom_Generator as GG
import Abaqus_Runner as AR
import Strain_Result_Check as SRC
import data_access_layer as DAL
import os





# "Pre-Processing"

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
Results_Dict = DH.Read_Database_From_Json("Data_Base.json")
load_cases = "sigdata1.txt"
loads = np.genfromtxt(load_cases)
Source_Path = os.getcwd()
os.chdir('..')
Current_Path = os.getcwd()
print(Current_Path)


# "Main Process"

# TODO: optimize time complexity
for counter, load in enumerate(loads):
    Key = KG.Key_Generator(load)
    if Key in Results_Dict.keys():
        print("The key is already found in JSON file")
        continue
    else:
        print("The key was not found in JSON file")
        KFC.Create_Sub_Folder(Key)
        scaling_factor = 50
        print ("initial load: {}".format(load))
        scaled_load = load * scaling_factor
        Max_Strain = 0
        itertation = 0
        Lower_Strain_Limit = 0.0001
        Upper_Strain_Limit = 100
        while (Upper_Strain_Limit < Max_Strain or Lower_Strain_Limit > Max_Strain ):
            itertation += 1
            print ("scaling factor {} -> applied load in iteration {}: {}".format(scaling_factor, itertation, scaled_load))
            LC.Load_File_Generator(scaled_load, Key)
            GG.Abaqus_Input_Generator(Key)
            # AR.Abaqus_Runner(Key, 1)
            Max_Strain = SRC.Max_Strain_Finder(Key)
            print ("Max Strain: {}".format(Max_Strain))
            if Max_Strain < Lower_Strain_Limit:
                scaling_factor *= 1.05
                scaled_load = load * scaling_factor

            elif Max_Strain > Upper_Strain_Limit:
                scaling_factor *= 0.95
                scaled_load = load * scaling_factor

    # TODO: turn the next dictionary into the new schema
        system_info = MR.Meta_reader(Key)
        persistent_info = DH.Read_Database_From_Json('src/p_test.json')
        #Insert Results to the Data Base
        Results_Dict[Key] = {
            "$schema": "https://json-schema.org/draft/2019-09/schema",
            "identifier" : persistent_info['description'],
            "title" : persistent_info['title'],
            "creator" : persistent_info['creator'],
            "creator_ORCID" : persistent_info['creator_ORCID'],
            "contributor_affiliation" : persistent_info["contributor_affiliation"],
            "creator_institute" : persistent_info["creator_institute"],
            "creator_group" : persistent_info["creator_group"],
            "contributor" : persistent_info["contributor"],
            "contributor_ORCID" : persistent_info["contributor_ORCID"],
            "contributor_affiliation" : persistent_info["contributor_affiliation"],
            "contributor_institute" : persistent_info["contributor_institute"],
            "contributor_group" : persistent_info["contributor_group"],
            "description" : persistent_info["description"],
            "rights" : persistent_info["rights"],
            "rights_holder" : persistent_info["rights_holder"],
            "funder_name" : persistent_info["funder_name"],
            "fund_identifier" : persistent_info["fund_identifier"],
            "publisher" : persistent_info["publisher"],
            "relation" : persistent_info["relation"],
            "keywords" : persistent_info["keywords"],
            "software" : persistent_info["software"],
            "software_version" : system_info["Abaqus-Version"],
            "system": persistent_info['system'],
            "system_version": persistent_info["system_version"],
            "processor_specifications" : persistent_info["processor_specifications"],
            "input_path" : persistent_info['input_path'],
            "results_path" : persistent_info["results_path"],
            "RVE_size" : system_info['RVE_Size'],
            "RVE_continuity" : True, #TODO: find this value, defaulting to True
            "discretization_type" : "",
            "discretization_unit_size" : [0,0,0], #TODO: find this value, defaulting to [0,0,0]
            "discretization_count" : 1, #TODO: find this value, defaulting to 1
            "solid_volume_fraction" :  50, #TODO: find this value, defaulting to 50%
            "origin" : {
                "software" : persistent_info["software"],
                "software_version" : persistent_info["software_version"],
                "system" : persistent_info['system'],
                "system_version" : persistent_info["system_version"],
                "input_path" : persistent_info["input_path"],
                "results_path" : persistent_info["results_path"],
                },
            "golbal_temperature" : 298, #TODO: find this value, defaulting to 298
            "mechanical_BC" : {},
            "thermal_BC" : {},
            "material" : system_info['Material'],
            "stress": [], # read .out files S, S11, S12, S13, S22, S23, S33
            "total_strain": [], # read .out files E, E11, E12, E13, E22, E23, E33
            "plastic_strain" : {}, #TODO: find values 
            "units" : {}, #TODO: need to find
        }         
            
            
            
            
            
            
            
            
            # "Meta_Data": {
            #                   **MR.Meta_reader(Key),
            #                  "Scaling_Factor": scaling_factor,
            #                  "Initial_Load": load.tolist(),
            #                  "Applied_Load": scaled_load.tolist(),
            #                  "Max_Total_Strain": Max_Strain,
            #                     },
            #                  "Results": RP.Results_Reader(Key)}

    DH.Json_Database_Creator(Results_Dict, "Data_Base_Updated.json")



print("*************************************************************we're trying to get the new DATA NOW!!!!***********************************************************************")








# "Meta_Data": MR.Meta_reader(Key),
# "Post Processing"
# Keys = Data_Base.keys()
# Desired_Keys = KP.Key_Finder(Keys, [1, 1, 1, 0, 0, 0])
# Found_Keys_Name = KP.Found_Keys_Generator(Desired_Keys)
# for Key in Found_Keys_Name:
#     print (Data_Base[Key]["Applied_Load"])

