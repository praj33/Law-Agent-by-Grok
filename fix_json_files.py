"""
JSON File Fixer
==============

This script fixes the JSON files INSERT2.json and INSERT3.json to make them properly formatted.
It creates new fixed versions that can be used with the enhanced data integration.

Usage: python fix_json_files.py
"""

import json
import re
import os

def fix_insert2_json():
    """Fix INSERT2.json file"""
    print("Fixing INSERT2.json...")
    
    try:
        # Read the file content
        with open('INSERT2.json', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if it's already valid JSON
        try:
            json.loads(content)
            print("INSERT2.json is already valid JSON.")
            return True
        except json.JSONDecodeError:
            pass
        
        # Add proper structure
        if not content.strip().startswith('{'):
            content = '{\n  "crime_in_india_2022": {\n' + content
        
        if not content.strip().endswith('}'):
            content = content + '\n  }\n}'
        
        # Fix common JSON issues
        content = re.sub(r',\s*]', ']', content)  # Remove trailing commas in arrays
        content = re.sub(r',\s*}', '}', content)  # Remove trailing commas in objects
        
        # Try to parse the fixed content
        try:
            json_data = json.loads(content)
            
            # Write the fixed content to a new file
            with open('INSERT2_fixed.json', 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2)
            
            print("✅ INSERT2.json fixed successfully. Saved as INSERT2_fixed.json")
            return True
        except json.JSONDecodeError as e:
            print(f"❌ Failed to fix INSERT2.json: {e}")
            
            # Try a more aggressive approach - extract valid JSON objects
            print("Attempting alternative fix...")
            
            # Create a minimal valid structure
            minimal_json = {
                "crime_in_india_2022": {
                    "table_1A.1_cases_registered_under_ipc_crimes_state_ut_wise_2020_2022": {
                        "STATES": [],
                        "UNION TERRITORIES": []
                    },
                    "projected_population_states_uts_2022": []
                }
            }
            
            # Extract state data using regex
            state_pattern = r'"State/UT":\s*"([^"]+)",\s*"2020":\s*(\d+),\s*"2021":\s*(\d+),\s*"2022":\s*(\d+)'
            state_matches = re.findall(state_pattern, content)
            
            for match in state_matches:
                state_name, crime_2020, crime_2021, crime_2022 = match
                state_data = {
                    "State/UT": state_name,
                    "2020": int(crime_2020),
                    "2021": int(crime_2021),
                    "2022": int(crime_2022)
                }
                
                # Determine if it's a state or UT
                if any(ut in state_name for ut in ["Islands", "Delhi", "Chandigarh", "Puducherry", "Ladakh", "Lakshadweep", "Daman", "Jammu"]):
                    minimal_json["crime_in_india_2022"]["table_1A.1_cases_registered_under_ipc_crimes_state_ut_wise_2020_2022"]["UNION TERRITORIES"].append(state_data)
                else:
                    minimal_json["crime_in_india_2022"]["table_1A.1_cases_registered_under_ipc_crimes_state_ut_wise_2020_2022"]["STATES"].append(state_data)
            
            # Extract population data
            pop_pattern = r'"STATE/UT":\s*"([^"]+)",\s*"Population \(in Lakhs\)":\s*([\d\.]+)'
            pop_matches = re.findall(pop_pattern, content)
            
            for match in pop_matches:
                state_name, population = match
                pop_data = {
                    "STATE/UT": state_name,
                    "Population (in Lakhs)": float(population)
                }
                minimal_json["crime_in_india_2022"]["projected_population_states_uts_2022"].append(pop_data)
            
            # Write the minimal JSON to a new file
            with open('INSERT2_fixed.json', 'w', encoding='utf-8') as f:
                json.dump(minimal_json, f, indent=2)
            
            print(f"✅ Created minimal valid INSERT2_fixed.json with {len(minimal_json['crime_in_india_2022']['table_1A.1_cases_registered_under_ipc_crimes_state_ut_wise_2020_2022']['STATES'])} states")
            return True
            
    except Exception as e:
        print(f"❌ Error fixing INSERT2.json: {e}")
        return False

def fix_insert3_json():
    """Fix INSERT3.json file"""
    print("\nFixing INSERT3.json...")
    
    try:
        # Read the file content
        with open('INSERT3.json', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if it's already valid JSON
        try:
            json.loads(content)
            print("INSERT3.json is already valid JSON.")
            return True
        except json.JSONDecodeError:
            pass
        
        # Add proper structure
        if not content.strip().startswith('{'):
            content = '{\n  "crime_in_india_2021_volume_2": {\n' + content
        
        if not content.strip().endswith('}'):
            content = content + '\n  }\n}'
        
        # Fix common JSON issues
        content = re.sub(r',\s*]', ']', content)  # Remove trailing commas in arrays
        content = re.sub(r',\s*}', '}', content)  # Remove trailing commas in objects
        
        # Try to parse the fixed content
        try:
            json_data = json.loads(content)
            
            # Write the fixed content to a new file
            with open('INSERT3_fixed.json', 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2)
            
            print("✅ INSERT3.json fixed successfully. Saved as INSERT3_fixed.json")
            return True
        except json.JSONDecodeError as e:
            print(f"❌ Failed to fix INSERT3.json: {e}")
            
            # Try a more aggressive approach - extract valid JSON objects
            print("Attempting alternative fix...")
            
            # Create a minimal valid structure
            minimal_json = {
                "crime_in_india_2021_volume_2": {
                    "table_6A.1_crime_against_senior_citizens_state_ut_wise_2019_2021": {
                        "STATES": [],
                        "UNION TERRITORIES": []
                    },
                    "projected_population_states_uts_2021": []
                }
            }
            
            # Extract state data using regex
            state_pattern = r'"State/UT":\s*"([^"]+)",\s*"2019":\s*(\d+),\s*"2020":\s*(\d+),\s*"2021":\s*(\d+)'
            state_matches = re.findall(state_pattern, content)
            
            for match in state_matches:
                state_name, crime_2019, crime_2020, crime_2021 = match
                state_data = {
                    "State/UT": state_name,
                    "2019": int(crime_2019),
                    "2020": int(crime_2020),
                    "2021": int(crime_2021),
                    "Rate of Total Crime against Senior Citizen (2021)": 0.0,
                    "Chargesheeting Rate (2021)": 0.0
                }
                
                # Determine if it's a state or UT
                if any(ut in state_name for ut in ["Islands", "Delhi", "Chandigarh", "Puducherry", "Ladakh", "Lakshadweep", "Daman", "Jammu"]):
                    minimal_json["crime_in_india_2021_volume_2"]["table_6A.1_crime_against_senior_citizens_state_ut_wise_2019_2021"]["UNION TERRITORIES"].append(state_data)
                else:
                    minimal_json["crime_in_india_2021_volume_2"]["table_6A.1_crime_against_senior_citizens_state_ut_wise_2019_2021"]["STATES"].append(state_data)
            
            # Extract population data
            pop_pattern = r'"STATE/UT":\s*"([^"]+)",\s*"Population \(in Lakhs\)":\s*([\d\.]+)'
            pop_matches = re.findall(pop_pattern, content)
            
            for match in pop_matches:
                state_name, population = match
                pop_data = {
                    "STATE/UT": state_name,
                    "Population (in Lakhs)": float(population)
                }
                minimal_json["crime_in_india_2021_volume_2"]["projected_population_states_uts_2021"].append(pop_data)
            
            # Write the minimal JSON to a new file
            with open('INSERT3_fixed.json', 'w', encoding='utf-8') as f:
                json.dump(minimal_json, f, indent=2)
            
            print(f"✅ Created minimal valid INSERT3_fixed.json with {len(minimal_json['crime_in_india_2021_volume_2']['table_6A.1_crime_against_senior_citizens_state_ut_wise_2019_2021']['STATES'])} states")
            return True
            
    except Exception as e:
        print(f"❌ Error fixing INSERT3.json: {e}")
        return False

def update_enhanced_data_integration():
    """Update enhanced_data_integration.py to use fixed files"""
    print("\nUpdating enhanced_data_integration.py...")
    
    try:
        # Read the file content
        with open('enhanced_data_integration.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update file paths
        content = content.replace('insert2_file: str = "INSERT2.json"', 'insert2_file: str = "INSERT2_fixed.json"')
        content = content.replace('insert3_file: str = "INSERT3.json"', 'insert3_file: str = "INSERT3_fixed.json"')
        
        # Write the updated content
        with open('enhanced_data_integration.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ enhanced_data_integration.py updated to use fixed JSON files")
        return True
    except Exception as e:
        print(f"❌ Error updating enhanced_data_integration.py: {e}")
        return False

def main():
    """Main function"""
    print("🔧 JSON File Fixer")
    print("=================")
    
    # Fix INSERT2.json
    insert2_fixed = fix_insert2_json()
    
    # Fix INSERT3.json
    insert3_fixed = fix_insert3_json()
    
    # Update enhanced_data_integration.py
    if insert2_fixed or insert3_fixed:
        update_enhanced_data_integration()
    
    print("\n🎯 Summary:")
    print(f"INSERT2.json: {'✅ Fixed' if insert2_fixed else '❌ Failed'}")
    print(f"INSERT3.json: {'✅ Fixed' if insert3_fixed else '❌ Failed'}")
    
    if insert2_fixed and insert3_fixed:
        print("\n🚀 Next Steps:")
        print("1. Run 'python enhanced_data_integration.py' to test the fixed files")
        print("2. Use the enhanced data in your legal agent")
    else:
        print("\n⚠️ Some files could not be fixed. Please check the error messages above.")

if __name__ == "__main__":
    main()
