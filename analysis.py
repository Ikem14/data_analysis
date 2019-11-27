import sys
import pandas as pd

#load ---> PART D <--- prescriber(provider) data into a DataFrame
try:
    provider_data = pd.read_table('data/provider_data.txt', sep='\t') #creates a DataFrame 
    print("provider_data \n", provider_data[['npi', 'drug_name', 'generic_name', 'total_claim_count', 'total_30_day_fill_count', 'total_day_supply','total_drug_cost']]) #displays provider data
    # (provider_data['generic_name'] == 'OXYCODONE HCL/ACETAMINOPHEN').value_counts() #will get the total count of oxy prescribed 
except:
    print("ERROR READING prescriber data FILE: ", sys.exc_info())

#load prescriber summary
try:
    provider_summary = pd.read_table('data/provider_summary.txt', sep='\t')
    print('provider_summary data \n', provider_summary)
except:
    print("ERROR READING prescriber_summary data FILE: ", sys.exc_info())


#load --> PART A <--- inpatient payment data into a DataFrame
try:
    inpatient_data = pd.read_csv('data/inpatient_charge.csv') #creates a DataFrame
    print("\n\ninpatient_data \n", inpatient_data)
    inpatient_describe = inpatient_data[['Total Discharges', 'Average Covered Charges', 'Average Total Payments', 'Average Medicare Payments']].describe()
    print("\n\ninpatient_describe \n", inpatient_describe) #displays inpatient_data
except:
    print("ERROR READING inpatient FILE: ", sys.exc_info())

#load --> PART A <--- outpatient payment data into a DataFrame
try:
    outpatient_data = pd.read_csv('data/outpatient_charge.csv') #creates a DataFrame
    print("\n\noutpatient_data \n", outpatient_data) #displays outpatient_data
    outpatient_describe = outpatient_data[['Average_Total_Submitted_Charges', 'Average_Medicare_Allowed_Amount', 'Average_Medicare_Payment_Amount']].describe()
    print("Describing outpatient_data: \n", outpatient_describe) #display info
except:
    print("ERROR READING outpatient FILE: ", sys.exc_info())

# try:
#     dmepos_data = pd.read_table('data/dmepos_data.txt', sep='\t')
#     print("dmepos_data \n", dmepos_data)
# except:
#     print("ERROR READING DMEPOS data FILE: ", sys.exc_info())


