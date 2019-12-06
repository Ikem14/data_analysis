import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from uszipcode import SearchEngine

search = SearchEngine(simple_zipcode=True)

# MAIN MENU
def main_menu():
    # Load ---> PART D <--- prescriber(provider) data into a DataFrame
    try:
        provider_data = pd.read_table('data/provider_data.txt', sep='\t') #creates a DataFrame 
        print("provider_data \n", provider_data[['npi', 'drug_name', 'generic_name', 'total_claim_count', 'total_30_day_fill_count', 'total_day_supply','total_drug_cost']]) #displays provider data
        
        # (provider_data['generic_name'] == 'OXYCODONE HCL/ACETAMINOPHEN').sum() #will get the total count of oxy prescribed 
    except:
        print("ERROR READING prescriber data FILE: ", sys.exc_info())

    try:
        choice = input("Enter (1) For Individual Location Drug Analysis \nEnter (2) To Compare Multiple Locations \nEnter (0) To Exit: ")
        while choice != 0:
            if choice == "1":
                try:
                    state = input("Enter State: ")
                    city = input("Enter City: ")
                    drug = input("Enter Drug: ")
                    display_type = input("Enter (1) For a Basic Description of the selected data \nEnter (2) For Scatter plot \nEnter (3) To Create a Map By State \nEnter (4) for ALL: ")
                    if display_type == '1':
                        try:
                            describe_data(provider_data, state, city, drug)
                            choice = input("Enter (1) For Individual Location Drug Analysis \nEnter (2) To Compare Multiple Locations \nEnter (0) To Exit: ")
                        except:
                            print("ERROR IN DESCRIBING DATA")
                        
                    elif display_type == '2':
                        try:
                            create_scatter(provider_data, state, city, drug)
                            choice = input("Enter (1) For Individual Location Drug Analysis \nEnter (2) To Compare Multiple Locations \nEnter (0) To Exit: ")
                        except:
                            print("ERROR IN CREATION OF SCATTER PLOT")
                    elif display_type == '3':
                        try:
                            create_map(provider_data, state, city, drug)
                            choice = input("Enter (1) For Individual Location Drug Analysis \nEnter (2) To Compare Multiple Locations \nEnter (0) To Exit: ")
                        except:
                            print("ERROR IN MAPPING DATA")
                    elif display_type == '4':
                        try:
                            describe_data(provider_data, state, city, drug)
                        except:
                            print("ERROR IN DESCRIBING DATA")
                        try:
                            create_scatter(provider_data, state, city, drug)
                        except:
                            print("ERROR IN CREATION OF SCATTER PLOT")
                        try:
                            create_map(provider_data, state, drug)
                        except:
                            print("ERROR IN MAPPING DATA")
                        choice = input("Enter (1) For Individual Location Drug Analysis \nEnter (2) To Compare Multiple Locations \nEnter (0) To Exit: ")
                    else:
                        print("INVALID SELECTION")
                except:
                    print("ERROR In Individual Drug Analysis")
            elif choice == "2":
                try:
                    print("choice 2")
                except:
                    print("Error in choice 2")
            elif choice == '0':
                break
        else:
            print("INVALID SELECTION")
    except:
        print("ERROR IN MENU")
    
    
#FUNCTION THAT CREATES MAP
def create_map(provider_data, state, city, drug):
    query = 'nppes_provider_state == "' + state + '" and generic_name == "' + drug + '"'
    print("Query: ", query)
    result = provider_data.query(query)
    # print("Result: ", result)
    group = result.groupby('nppes_provider_city')
    city_query = group.sum()
    city_list = city_query.index
    zip_code = []
    track_city = ""
    #Create list of zipcodes
    for index in range(len(city_list)):
        res = search.by_city_and_state(city_list[index], state)
        if len(res) > 0:
            if city_list[index] == city:
                zip = res[0]
                zip_code.append(zip.zipcode)
                track_city = zip.zipcode
            else:
                zip = res[0]
                zip_code.append(zip.zipcode)
        else:
            zip_code.append('55555')
    print("ZIPCODES: ", zip_code)
    print("TRACK: ",  track_city)
    
    # CREATE MAP
    N = len(city_list)
    c = np.random.randint(1, N, N)
    s = city_query['total_claim_count']
    # plt.axes(xscale='log')
    fig, ax = plt.subplots()

    ax.set_xlabel("Cities", fontsize=15)
    ax.set_ylabel('Total Claim Count', fontsize=15)
    ax.set_title(drug + ' PRESCRIPTION DISTRIBUTION IN ' + state)
    ax.grid(True)
    ax.set_xticklabels([])
    ax.autoscale(enable=True, axis='x', tight=True)
    scatter = ax.scatter(zip_code, city_query['total_claim_count'], c=c, s=s)
    label_list = [city]
    for i, txt in enumerate(label_list):
        if txt == city:
            # query = 'nppes_provider_city == "'+ city + '"'
            # track_city_claim = group.query(query)
            ax.annotate(txt, (track_city, 20001))
    # produce a legend with the unique colors from the scatter
    # legend1 = ax.legend(*scatter.legend_elements(), loc="upper right", title="CITIES")
    # legend1 = ax.legend(city_list, loc="upper right", title="CITIES")
    # ax.add_artist(legend1)

    # # produce a legend with a cross section of sizes from the scatter
    # handles, labels = scatter.legend_elements(prop="sizes", alpha=0.6, color="magenta")
    # legend2 = ax.legend(handles, labels, loc="upper right", labelspacing=1.0, title="Sizes ~ Total claim count")
        

    plt.show()       
    
# FUNCTION THAT DESCRIBES DATA
def describe_data(provider_data, state, city, drug):
    try:
        #Create query
        query  = 'generic_name == "'+ drug + '"'
        query = query + ' and nppes_provider_state == '
        query = query + '"' + state + '"'
        query = query + ' and nppes_provider_city == '
        query = query + '"' + city + '"'
        print("QUERY: ", query)
        provider_query = provider_data.query(query)

        print("\n\n\n" + city + ", " + state + ": \n", provider_query[['bene_count', 'total_claim_count', 'total_30_day_fill_count', 'total_day_supply','total_drug_cost', 'bene_count_ge65']].describe())
    except:
        print("ERROR IN DESCRIBING DATA", sys.exc_info())


# FUNCTION THAT CREATES SCATTERPLOT
def create_scatter(provider_data, state, city, drug):
    try:
        #Create query
        query  = 'generic_name == "'+ drug + '"'
        query = query + ' and nppes_provider_state == '
        query = query + '"' + state + '"'
        query = query + ' and nppes_provider_city == '
        query = query + '"' + city + '"'
        print("QUERY: ", query)
        provider_query = provider_data.query(query)
        N = len(provider_query) #get total amount of drug prescribed
        s = provider_query['total_claim_count']

        fig, ax = plt.subplots()

        ax.set_xlabel("NPI", fontsize=15)
        ax.set_ylabel('Total claim count', fontsize=15)
        ax.set_title(drug + ' PRESCRIPTION DISTRIBUTION IN ' + city + ', ' + state)
        ax.grid(True)
        scatter = ax.scatter(provider_query['npi'], provider_query['total_claim_count'], s=s)
        

        plt.show()        
    except:
        print("ERROR IN CREATION OF TRACING SCATTERPLOT", sys.exc_info())


# RUN THE PROGRAM
try:
    main_menu()
except:
    print("STARTUP ERROR!!!")




# #plot a scatterplot of oxy in COLUMBIA, MD
# try:
#     # Get scatterplot of oxy in COLUMBIA, MD
#     provider_query = provider_data.query('generic_name == "OXYCODONE HCL" and nppes_provider_state == "MD" and nppes_provider_city == "COLUMBIA"')
#     print("\n\n\nCOLUMBIA, MD: \n", provider_query.describe())
#     N = len(provider_query) #get total amount of oxy prescribed
#     # x, y = np.random.rand(2, N)
#     # c = np.random.randint(1, 5, size=N)
#     # width = 0.1
#     s = provider_query['total_claim_count']
#     # s = [100, 200, 400, 600, 800]
#     try:
#         table = go.Figure(data=[go.Table(header=dict(values=provider_query.columns), 
#                                             cells=dict(values=[provider_query.describe()]))])
#     except:
#         print("ERROR IN TABLE GENERATION")
#     try:
#         table.show()
#     except:
#         print("ERROR IN TABLE DISPLAY")
    

#     fig, ax = plt.subplots()

#     # scatter = ax.scatter(x, y, c=c, s=s)
#     ax.set_xlabel("NPI", fontsize=15)
#     ax.set_ylabel('Total claim count', fontsize=15)
#     ax.set_title('OXYCODONE HCL PRESCRIPTION DISTRIBUTION IN COLUMBIA, MD')
#     ax.grid(True)
#     scatter = ax.scatter(provider_query['npi'], provider_query['total_claim_count'], s=s)
    

#     plt.show()
    
# except:
#     print("ERROR IN CREATION OF TRACING SCATTERPLOT", sys.exc_info())

# #plot a scatterplot of oxy in BALTIMORE, MD
# try:
#     # Get scatterplot of oxy in BALTIMORE, MD
#     provider_query = provider_data.query('generic_name == "OXYCODONE HCL" and nppes_provider_state == "MD" and nppes_provider_city == "BALTIMORE"')
#     print("\n\n\nBALTIMORE, MD: \n", provider_query.describe())
#     N = len(provider_query) #get total amount of oxy prescribed
#     # x, y = np.random.rand(2, N)
#     # c = np.random.randint(1, 5, size=N)
#     s = provider_query['total_claim_count']

#     fig, ax = plt.subplots()

#     # scatter = ax.scatter(x, y, c=c, s=s)
#     ax.set_xlabel("NPI", fontsize=15)
#     ax.set_ylabel('Total claim count', fontsize=15)
#     ax.set_title('OXYCODONE HCL PRESCRIPTION DISTRIBUTION IN BALTIMORE, MD')
#     ax.grid(True)
#     scatter = ax.scatter(provider_query['npi'], provider_query['total_claim_count'], s=s)
    

#     plt.show()
# except:
#     print("ERROR IN CREATION OF TRACING SCATTERPLOT", sys.exc_info())

# #plot a scatterplot of oxy in WALDORF, MD
# try:
#     # Get scatterplot of oxy in WALDORF, MD
#     provider_query = provider_data.query('generic_name == "OXYCODONE HCL" and nppes_provider_state == "MD" and nppes_provider_city == "WALDORF"')
#     print("\n\n\nWALDORF, MD: \n", provider_query.describe())
#     N = len(provider_query) #get total amount of oxy prescribed
#     # x, y = np.random.rand(2, N)
#     # c = np.random.randint(1, 5, size=N)
#     s = provider_query['total_claim_count']

#     fig, ax = plt.subplots()

#     # scatter = ax.scatter(x, y, c=c, s=s)
#     ax.set_xlabel("NPI", fontsize=15)
#     ax.set_ylabel('Total claim count', fontsize=15)
#     ax.set_title('OXYCODONE HCL PRESCRIPTION DISTRIBUTION IN WALDORF, MD')
#     ax.grid(True)
#     scatter = ax.scatter(provider_query['npi'], provider_query['total_claim_count'], s=s)
    

#     plt.show()
# except:
#     print("ERROR IN CREATION OF TRACING SCATTERPLOT", sys.exc_info())

# #plot a scatterplot of oxy in SILVER SPRING, MD
# try:
#     # Get scatterplot of oxy in SILVER SPRING, MD
#     provider_query = provider_data.query('generic_name == "OXYCODONE HCL" and nppes_provider_state == "MD" and nppes_provider_city == "SILVER SPRING"')
#     print("\n\n\nSILVER SPRING, MD: \n", provider_query.describe())
#     N = len(provider_query) #get total amount of oxy prescribed
#     # x, y = np.random.rand(2, N)
#     # c = np.random.randint(1, 5, size=N)
#     s = provider_query['total_claim_count']

#     fig, ax = plt.subplots()

#     # scatter = ax.scatter(x, y, c=c, s=s)
#     ax.set_xlabel("NPI", fontsize=15)
#     ax.set_ylabel('Total claim count', fontsize=15)
#     ax.set_title('OXYCODONE HCL PRESCRIPTION DISTRIBUTION IN SILVER SPRING, MD')
#     ax.grid(True)
#     scatter = ax.scatter(provider_query['npi'], provider_query['total_claim_count'], s=s)
    

#     plt.show()
# except:
#     print("ERROR IN CREATION OF TRACING SCATTERPLOT", sys.exc_info())

# #plot a scatterplot of oxy in COLUMBIA, BALTIMORE, WALDORF, SILVER SPRING
# try:
#     # Get scatterplot of oxy in SILVER SPRING, MD
#     columbia_query = provider_data.query('generic_name == "OXYCODONE HCL" and nppes_provider_state == "MD" and nppes_provider_city == "COLUMBIA"')
#     baltimore_query = provider_data.query('generic_name == "OXYCODONE HCL" and nppes_provider_state == "MD" and nppes_provider_city == "BALTIMORE"')
#     waldorf_query = provider_data.query('generic_name == "OXYCODONE HCL" and nppes_provider_state == "MD" and nppes_provider_city == "WALDORF"')
#     silver_query = provider_data.query('generic_name == "OXYCODONE HCL" and nppes_provider_state == "MD" and nppes_provider_city == "SILVER SPRING"')
#     N = len(provider_query) #get total amount of oxy prescribed
    

#     fig, ax = plt.subplots()
#     color = ['blue', 'red', 'green', 'orange']
#     for city in ['Columbia', 'Baltimore', 'Waldorf', 'Silver Spring']:
#         if city == 'Columbia':
#             x = columbia_query['npi']
#             y = columbia_query['total_claim_count']
#             c=color[0]
#         elif city == 'Baltimore':
#             x = baltimore_query['npi']
#             y = baltimore_query['total_claim_count']
#             c=color[1]
#         elif city == 'Waldorf':
#             x = waldorf_query['npi']
#             y = waldorf_query['total_claim_count']
#             c=color[2]
#         elif city == 'Silver Spring':
#             x = silver_query['npi']
#             y = silver_query['total_claim_count']
#             c=color[3]
        
#         scale = baltimore_query['total_claim_count']
#         ax.scatter(x, y, c=c, s=scale, label=city, alpha=0.4, edgecolors='green')

#     ax.set_xlabel("NPI", fontsize=15)
#     ax.set_ylabel('Total claim count', fontsize=15)
#     ax.set_title('OXYCODONE HCL PRESCRIPTION DISTRIBUTION IN COLUMBIA, BALTIMORE, WALDORF & SILVER SPRING')
#     ax.legend(labelspacing=2.0, title="Cities")
#     ax.grid(True)


#     plt.show()
# except:
#     print("ERROR IN CREATION OF SCATTERPLOT", sys.exc_info())



# # #plot a scatterplot of oxy in COLUMBIA, MD
# # try:
# #     # Get scatterplot of oxy in COLUMBIA, MD
# #     provider_query = provider_data.query('generic_name == "OXYCODONE HCL/ACETAMINOPHEN" and nppes_provider_state == "MD" and nppes_provider_city == "COLUMBIA"')
# #     N = len(provider_query) #get total amount of oxy prescribed
# #     # x, y = np.random.rand(2, N)
# #     # c = np.random.randint(1, 5, size=N)
# #     c = np.random.randint(1, N, len(provider_query['npi']))
# #     s = provider_query['total_claim_count']
# #     # s = [100, 200, 400, 600, 800]

# #     fig, ax = plt.subplots()

# #     # scatter = ax.scatter(x, y, c=c, s=s)
# #     ax.set_xlabel("NPI", fontsize=15)
# #     ax.set_ylabel('Total claim count', fontsize=15)
# #     ax.set_title('OXYCODONE HCL/ACETAMINOPHEN PRESCRIPTION DISTRIBUTION IN COLUMBIA, MD')
# #     ax.grid(True)
# #     scatter = ax.scatter(provider_query['npi'], provider_query['total_claim_count'], s=s)
    

# #     # produce a legend with the unique colors from the scatter
# #     # legend1 = ax.legend(*scatter.legend_elements(), loc="lower left", title="DRUGS")
# #     # ax.add_artist(legend1)

# #     # produce a legend with a cross section of sizes from the scatter
# #     handles, labels = scatter.legend_elements(prop="sizes", alpha=0.6, color="magenta")
# #     legend2 = ax.legend(handles, labels, loc="upper right", labelspacing=1.0, title="Sizes ~ Total claim count")

# #     plt.show()
# # except:
# #     print("ERROR IN CREATION OF TRACING SCATTERPLOT", sys.exc_info())



# # #plot a scatterplot of oxy in COLUMBIA, MD
# # try:
# #     # Get scatterplot of oxy in COLUMBIA, MD
# #     provider_query = provider_data.query('generic_name == "OXYCODONE HCL/ACETAMINOPHEN" and nppes_provider_state == "MD" and nppes_provider_city == "COLUMBIA"')
# #     N = len(provider_query) #get total amount of oxy prescribed
# #     # x, y = np.random.rand(2, N)
# #     # c = np.random.randint(1, 5, size=N)
# #     c = np.random.randint(1, N, len(provider_query['npi']))
# #     # c = provider_query['npi']
# #     # s = np.random.randint(10, 220, size=N)
# #     s = provider_query['total_claim_count']
# #     # s = [100, 200, 400, 600, 800]

# #     fig, ax = plt.subplots()

# #     # scatter = ax.scatter(x, y, c=c, s=s)
# #     ax.set_xlabel("NPI", fontsize=15)
# #     ax.set_ylabel('Total claim count', fontsize=15)
# #     ax.set_title('OXYCODONE HCL/ACETAMINOPHEN PRESCRIPTION DISTRIBUTION IN COLUMBIA, MD')
# #     ax.grid(True)
# #     scatter = ax.scatter(provider_query['npi'], provider_query['total_claim_count'], c=c, s=s) #c=c
    

# #     # produce a legend with the unique colors from the scatter
# #     # legend1 = ax.legend(*scatter.legend_elements(), loc="lower left", title="DRUGS")
# #     # ax.add_artist(legend1)

# #     # produce a legend with a cross section of sizes from the scatter
# #     handles, labels = scatter.legend_elements(prop="sizes", alpha=0.6)
# #     legend2 = ax.legend(handles, labels, loc="upper right", labelspacing=1.0, title="Sizes ~ Total claim count")

# #     plt.show()
# # except:
# #     print("ERROR IN CREATION OF TRACING SCATTERPLOT", sys.exc_info())



# #load prescriber summary
# # try:
# #     provider_summary = pd.read_table('data/provider_summary.txt', sep='\t')
# #     print('provider_summary data \n', provider_summary)
# #     print(plt.plot(provider_summary))
# # except:
# #     print("ERROR READING prescriber_summary data FILE: ", sys.exc_info())


# # #load --> PART A <--- inpatient payment data into a DataFrame
# # try:
# #     inpatient_data = pd.read_csv('data/inpatient_charge.csv') #creates a DataFrame
# #     print("\n\ninpatient_data \n", inpatient_data)
# #     inpatient_describe = inpatient_data[['Total Discharges', 'Average Covered Charges', 'Average Total Payments', 'Average Medicare Payments']].describe()
# #     print("\n\ninpatient_describe \n", inpatient_describe) #displays inpatient_data
# # except:
# #     print("ERROR READING inpatient FILE: ", sys.exc_info())

# # #load --> PART A <--- outpatient payment data into a DataFrame
# # try:
# #     outpatient_data = pd.read_csv('data/outpatient_charge.csv') #creates a DataFrame
# #     print("\n\noutpatient_data \n", outpatient_data) #displays outpatient_data
# #     outpatient_describe = outpatient_data[['Average_Total_Submitted_Charges', 'Average_Medicare_Allowed_Amount', 'Average_Medicare_Payment_Amount']].describe()
# #     print("Describing outpatient_data: \n", outpatient_describe) #display info
# # except:
# #     print("ERROR READING outpatient FILE: ", sys.exc_info())

# # try:
# #     dmepos_data = pd.read_table('data/dmepos_data.txt', sep='\t')
# #     print("dmepos_data \n", dmepos_data)
# # except:
# #     print("ERROR READING DMEPOS data FILE: ", sys.exc_info())


