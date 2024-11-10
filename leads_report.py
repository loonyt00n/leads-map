from leads_geomapper import pair_entities
from leads_data import read_leads_list_from_excel, read_rm_list_from_excel
from collections import defaultdict

print('Reading Leads/RM List form Excel')
print("------------------------------------\n")
leads_file_path = 'data/leads_list.xlsx' 
leads_list = read_leads_list_from_excel(leads_file_path)
print(f'READ: Leads List with {len(leads_list)} records\n')

rm_file_path = 'data/rm_list.xlsx' 
rm_list = read_rm_list_from_excel(rm_file_path)
print(f'READ: RMs List with {len(rm_list)} records\n')


# Function to generate email reports for each RM based on their matched leads
def generate_email_reports(pairs):
    reports = defaultdict(list)

    for pair in pairs:
        lead = pair['lead']
        rm = pair['rm']
        distance = pair['distance']
        maps_link = pair['maps_link']
        reason = pair['reason']

        report = (
            f"Lead Name: {lead['name']}\n"
            f"Lead Channel: {lead['lead_channel']}\n"
            f"Product to Pitch: {lead['product_to_pitch']}\n"
            f"Last Active: {lead['last_active']}\n"
            f"Preferred Time of Day: {lead['preferred_time_of_day']}\n"
            f"Preferred Day of Week: {lead['preferred_day_of_week']}\n"
            f"Propensity Score: {lead['propensity_score']}\n"
            f"High Net Worth: {'Yes' if lead['is_high_net_worth'] else 'No'}\n"
            f"Distance from RM: {distance:.2f} km\n"
            f"Reason for Pairing: {reason}\n"
            f"Google Maps Link: {maps_link}\n"
        )
        
        reports[rm['name']].append(report)

    return reports




# Pair entities based on updated criteria
matched_pairs, unpaired_leads = pair_entities(leads_list, rm_list)

# print(f"matched_pairs: {json.dumps(matched_pairs)}")
# print(f"unpaired_leads: {json.dumps(unpaired_leads)}")

# Generate email reports based on the matched pairs
email_reports = generate_email_reports(matched_pairs)

# Print email reports for each RM
print("------------------------------------\n")
for rm_name, report_data in email_reports.items():
    print(f"Email Report for RM: {rm_name}\n")
    print(f"Dear {rm_name},\n")
    print("Here are the leads you need to pursue:\n")
    
    for report in report_data:
        print(report)
    
    print("Best Regards,\nYour Sales Team\n")
    print("------------------------------------\n")


# Print email for the manager
print(f"Email Report for Virtual Lead Manager\n")
print(f"Dear Virtual Lead Manager,\n")

print("Below are the leads that could not be paired:\n")
for entry in unpaired_leads:
    print(f"Lead Name: {entry['lead']['name']} - Reason: {entry['reason']}")

print("Below are the availability of all RMs:\n")
for entry in rm_list:
    print(f"RM Name: {entry['name']} - Availability: {entry['availability_score']}/10")
print("------------------------------------\n")
