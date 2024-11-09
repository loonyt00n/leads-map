import json
from geo_distance import haversine_distance

# Function to pair entities based on proximity and additional criteria
def pair_entities(leads_list, rm_list):
    print(f'START: Leads GeoMapper Pairing Process')
    print("------------------------------------\n")

    pairs = []
    unpaired_leads = []
    
    for lead in leads_list:
        closest_rm = None
        closest_distance = float('inf')
        
        # Loop through RMs to find the closest matching RM
        for rm in rm_list:
            # Check if RM has expertise in the product to pitch and is available
            if lead['product_to_pitch'] not in rm['product_expertise'] or rm['availability_score'] <= 0:
                print(f'NO_MATCH: For lead {lead['name']} and product {lead['product_to_pitch']}, RM {rm['name']} with expertise {rm['product_expertise']} and availability {rm['availability_score']}')
                continue
            
            distance = haversine_distance(lead['lat'], lead['lon'], rm['lat'], rm['lon'])

            print(f'MATCH: For lead {lead['name']} and product {lead['product_to_pitch']}, RM {rm['name']} is at distance of {distance} with expertise {rm['product_expertise']} and availability {rm['availability_score']}')

             # Check if this RM is closer than previously found
            if distance < closest_distance:
                # Reduce the availability of the new match
                rm['availability_score'] -= 1

                # Restore previous RM's availability if it existed
                if closest_rm is not None:
                    closest_rm['availability_score'] += 1 
                    print(f'PAIR: For lead {lead['name']}, RM {rm['name']} at distance {distance} is paired, new availability is {rm['availability_score']}')
                    print(f'UN-PAIR: For lead {lead['name']}, RM {closest_rm['name']} at distance {closest_distance} is un-paired, new availability is {closest_rm['availability_score']}')
                    
                else:
                    print(f'PAIR: For lead {lead['name']}, RM {rm['name']} at distance {distance} is paired, new availability is {rm['availability_score']}')
                
                # update the new rm and distance
                closest_distance = distance
                closest_rm = rm
        
        
        # If a closest RM is found, pair it and reduce availability
        if closest_rm:
            pairs.append({
                'lead': lead,
                'rm': closest_rm,
                'distance': closest_distance,
                'maps_link': f"https://www.google.com/maps/dir/?api=1&origin={lead['lat']},{lead['lon']}&destination={closest_rm['lat']},{closest_rm['lon']}",
                'reason': f"Lead {lead['name']} is looking for product {lead['product_to_pitch']} and is the closest to RM {closest_rm['name']} at about {round(closest_distance)} kms away and an availability of {closest_rm['availability_score']}/10."
            })
            
        else:
            unpaired_leads.append({
                'lead': lead,
                'reason': f"Lead {lead['name']} looking for product {lead['product_to_pitch']} has no available RM with expertise nearby"
            })

    print(f'END: Leads GeoMapper Pairing Process - Pairs {len(pairs)}, UnPaired {len(unpaired_leads)}\n')
    return pairs, unpaired_leads

