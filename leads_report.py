import folium
import json
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


print("Generate Map with locations\n")

def generate_map_reports(pairs):
    # Create a map centered at a specific location
    map_center = [19.107434, 72.890345]  # Coordinates for Mumbai
    leads_map = folium.Map(location=map_center, zoom_start=12)

    #Darw a connecting line from RM to Lead
    for pair in pairs:
        lead = pair['lead']
        rm = pair['rm']
        distance = pair['distance']
        maps_link = pair['maps_link']
        reason = pair['reason']

        popup_content = f"""
            <div style="display: flex;align-items: center; flex-direction: column;margin: 5px;align-items: center;">
                <span>Distance ~ {round(distance)} kms</span>
                <a href="{maps_link}">Direction <i class="fa-solid fa-diamond-turn-right"></i></a>
                <span>{reason}</span>
            </div>
        """
        
        folium.PolyLine(
            locations=[[rm['lat'], rm['lon']], [lead['lat'], lead['lon']]],
            color='gray',
            popup= folium.Popup(popup_content, max_width=250),
            weight=4,
            opacity=0.7
        ).add_to(leads_map)

    all_pins = defaultdict(list)
    for rm in rm_list:
        pin = {
                "name" : rm['name'],
                "coordinates": [rm['lat'], rm['lon']],
                "image": f"https://avatar.iran.liara.run/username?username={rm['name']}",
                "description": [f"Availability: {rm['availability_score']}/10", f"Expertise: {rm['product_expertise']}"]
            }
        all_pins["rm"].append(pin)

    for lead in leads_list:
        pin = {
                "name" : lead['name'],
                "coordinates": [lead['lat'], lead['lon']],
                "image": f"https://avatar.iran.liara.run/username?username={lead['name']}",
                "description": [f"Propensity: {lead['propensity_score']}", f"Product Pitch: {lead['product_to_pitch']}"]
            }
        all_pins["lead"].append(pin)


    #print(f"all_pins : {json.dumps(all_pins)}")

    # Add pins to the map with rich content
    for pin_type, pin_list in all_pins.items():
        for pin in pin_list:

            popup_description = ""
            for item in pin['description']:
                popup_description += f"<span>{item}</span>"

            popup_content = f"""
            <div style="display:flex">   
                <div style="display: flex;align-items: center; flex-direction: column;margin: 5px;align-items: center;">
                    <img src="{pin['image']}" alt="{pin['name']}" style="width: 40px;height:auto;">
                    <strong>{pin['name']}</strong> 
                </div>
                <div style="flex-grow: 1; display:flex; flex-direction:column; align-items:flex-start;"> 
                    <strong>[{pin_type}]</strong>
                    {popup_description}
                </div>
            </div>
            """
            
            if pin_type == "rm":
                folium.Marker(
                    location=pin["coordinates"],
                    popup=folium.Popup(popup_content, max_width=300),
                    icon=folium.Icon(color="darkred", prefix="fa", icon="handshake")
                ).add_to(leads_map)
            else:
                folium.Marker(
                    location=pin["coordinates"],
                    popup=folium.Popup(popup_content, max_width=300),
                    icon=folium.Icon(color="green", prefix="fa", icon="user")
                ).add_to(leads_map)
    
        # # Define the coordinates for the polygon (area selection)
        # polygon_coordinates = [
        #     [37.7749, -122.4294],  # Top-left corner
        #     [37.7849, -122.4294],  # Top-right corner
        #     [37.7849, -122.4094],  # Bottom-right corner
        #     [37.7749, -122.4094],  # Bottom-left corner
        # ]

        # # Add the polygon to the map
        # folium.Polygon(
        #     locations=polygon_coordinates,
        #     color='green',
        #     fill=True,
        #     fill_color='green',
        #     fill_opacity=0.5,
        #     popup='Selected Area'
        # ).add_to(leads_map)

        # Save the map to an HTML file
    leads_map.save("report/map_with_area_selection.html")
    print("Done Map Report")

generate_map_reports(matched_pairs)
