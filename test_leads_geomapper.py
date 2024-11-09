import pytest
from leads_geomapper import pair_entities


def test_multiple_leads_for_one_rm():
    # Sample data for testing
    leads = [
        {'name': 'Alice', 'lat': 40.7128, 'lon': -74.0060, 'lead_channel': 'branch', 'product_to_pitch': 'insurance', 'last_active': '2024-10-11', 'preferred_time_of_day': 'morning', 'preferred_day_of_week': 'mon,wed', 'propensity_score': 0.5, 'is_high_net_worth': True},
        {'name': 'Bob', 'lat': 34.0522, 'lon': -118.2437, 'lead_channel': 'online', 'product_to_pitch': 'loans', 'last_active': '2024-10-15', 'preferred_time_of_day': 'afternoon', 'preferred_day_of_week': 'tue,thu', 'propensity_score': 0.7, 'is_high_net_worth': False},
    ]

    rms = [
        {'name':'Charlie','lat':41.8781,'lon':-87.6298,'lead_conversion_rate':0.3,'product_expertise':['insurance','loans','credit cards','personal banking'],'availability_score':6},
        {'name':'David','lat':37.7749,'lon':-122.4194,'lead_conversion_rate':0.5,'product_expertise':['investments','insurance'],'availability_score':8},
    ]

    matched_pairs, unpaired_leads = pair_entities(leads, rms)
    
    assert any(pair['lead']['name'] == "Alice" and pair['rm']['name'] == "Charlie" for pair in matched_pairs)
    assert any(pair['lead']['name'] == "Bob" and pair['rm']['name'] == "Charlie" for pair in matched_pairs)

def test_unpaired_leads():
    unpaired_leads_data = [
        {'name':'Frank','lat':39.7392,'lon':-104.9903,'lead_channel':'email','product_to_pitch':'stocks','last_active':'2024-10-09','preferred_time_of_day':'morning','preferred_day_of_week':'mon,fri','propensity_score':0.3,'is_high_net_worth':True},
    ]
    
    rms_with_no_expertise = [
        {'name':'Jack','lat':40.7128,'lon':-74.0060,'lead_conversion_rate':0,'product_expertise':['real estate'],'availability_score':0}, 
    ]
    
    matched_pairs, unpaired_leads = pair_entities(unpaired_leads_data, rms_with_no_expertise)
    
    assert any(u['lead']['name'] == "Frank" for u in unpaired_leads)

def test_specific_matches_per_lead():
    leads = [
        {'name': 'Alice', 'lat': 40.7128, 'lon': -74.0060, 'lead_channel': 'branch', 'product_to_pitch': 'insurance', 'last_active': '2024-10-11', 'preferred_time_of_day': 'morning', 'preferred_day_of_week': 'mon,wed', 'propensity_score': 0.5, 'is_high_net_worth': True},
        {'name': 'Bob', 'lat': 34.0522, 'lon': -118.2437, 'lead_channel': 'online', 'product_to_pitch': 'loans', 'last_active': '2024-10-15', 'preferred_time_of_day': 'afternoon', 'preferred_day_of_week': 'tue,thu', 'propensity_score': 0.7, 'is_high_net_worth': False},
        {'name': 'Catherine', 'lat': 37.7749, 'lon': -122.4194, 'lead_channel': 'referral', 'product_to_pitch': 'credit cards', 'last_active': '2024-10-12', 'preferred_time_of_day': 'evening', 'preferred_day_of_week': 'mon,fri', 'propensity_score': 0.8, 'is_high_net_worth': True},
        {'name': 'David', 'lat': 41.8781, 'lon': -87.6298, 'lead_channel': 'event', 'product_to_pitch': 'investments', 'last_active': '2024-10-14', 'preferred_time_of_day': 'morning', 'preferred_day_of_week': 'wed,sat', 'propensity_score': 0.6, 'is_high_net_worth': False},
        {'name':'Eva','lat':30.2672,'lon':-97.7431,'lead_channel':'social media','product_to_pitch':'personal banking','last_active':'2024-10-13','preferred_time_of_day':'afternoon','preferred_day_of_week':'tue,thu','propensity_score':0.4,'is_high_net_worth':False},
        {'name':'Frank','lat':39.7392,'lon':-104.9903,'lead_channel':'email','product_to_pitch':'loans','last_active':'2024-10-09','preferred_time_of_day':'morning','preferred_day_of_week':'mon,fri','propensity_score':0.3,'is_high_net_worth':True},
        {'name':'Grace','lat':38.9072,'lon':-77.0369,'lead_channel':'branch','product_to_pitch':'insurance','last_active':'2024-10-08','preferred_time_of_day':'evening','preferred_day_of_week':'wed,sun','propensity_score':0.5,'is_high_net_worth':False},
        {'name':'Henry','lat':36.1699,'lon':-115.1398,'lead_channel':'online','product_to_pitch':'credit cards','last_active':'2024-10-07','preferred_time_of_day':'afternoon','preferred_day_of_week':'mon,sat','propensity_score':0.6,'is_high_net_worth':True},
        {'name':'Isabel','lat':42.3601,'lon':-71.0589,'lead_channel':'referral','product_to_pitch':'investments','last_active':'2024-10-06','preferred_time_of_day':'morning','preferred_day_of_week':'tue,fri','propensity_score':0.7,'is_high_net_worth':False},
        {'name':'Jack','lat':33.4484,'lon':-112.0740,'lead_channel':'event','product_to_pitch':'personal banking','last_active':'2024-10-05','preferred_time_of_day':'evening','preferred_day_of_week':'wed,sun','propensity_score':0.5,'is_high_net_worth':True}

    ]

    rms = [
        {'name':'Charlie','lat':41.8781,'lon':-87.6298,'lead_conversion_rate':0.3,'product_expertise':['insurance','loans','personal banking'],'availability_score':5},
        # {'name':'Golaith','lat':37.7749,'lon':-122.4194,'lead_conversion_rate':0.5,'product_expertise':['investments','insurance'],'availability_score':8},
        # {'name':'Emily','lat':34.0522,'lon':-118.2437,'lead_conversion_rate':0.4,'product_expertise':['loans','credit cards'],'availability_score':7},
        # {'name':'Hank','lat':40.7128,'lon':-74.0060,'lead_conversion_rate':0.6,'product_expertise':['personal banking','insurance'],'availability_score':5}
    ]

    matched_pairs, unpaired_leads = pair_entities(leads, rms)
    
    assert any(pair['rm']['name'] == "Charlie" and pair['lead']['name'] == "Alice" and 'insurance' in pair['rm']['product_expertise'] for pair in matched_pairs)
    assert any(pair['rm']['name'] == "Charlie" and pair['lead']['name'] == "Grace" for pair in matched_pairs)
    assert any(pair['rm']['name'] == "Charlie" and pair['lead']['name'] == "Bob" for pair in matched_pairs)
    assert any(pair['rm']['name'] == "Charlie" and pair['lead']['name'] == "Frank" for pair in matched_pairs)

    assert len(matched_pairs) == 5
    assert rms[0]['availability_score'] == 0

    assert any(u['lead']['name'] == "Henry" for u in unpaired_leads)


# To run the tests use: pytest test_pairing_module.py