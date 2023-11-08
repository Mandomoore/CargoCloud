import time
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import pandas as pd
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from uszipcode import SearchEngine
import re
import requests
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup


import tkinterweb
from tkinterweb import HtmlFrame

profiles_click = 'profiles'
Database = "!!!!PATH TO DATABASE FOLDER"
profiles = "PATH TO PROFILES FOLDER!!!!"
# Rate Analysis Tab
    # RA_tab = ttk.Frame(tab_control)
    # tab_control.add(RA_tab, text='Rate Analysis')
    #
    # frame = HtmlFrame(RA_tab, messages_enabled=False)
    # frame.load_website("https://rates.truckstop.com/")
    # frame.pack(fill="both", expand=True)
lane_url =[]

# Create the main window
root = tk.Tk()
root.title('CargoCloud')
root.geometry('1500x800')

# Create the tabs
tab_control = ttk.Notebook(root)

# DATA INPUT TAB #######################################################################################################
data_input_tab = ttk.Frame(tab_control)
tab_control.add(data_input_tab, text='Data Input')

# Create the widgets for the Data Input tab
origin_label = ttk.Label(data_input_tab, text='Origin')
origin_entry = ttk.Entry(data_input_tab)

destination_label = ttk.Label(data_input_tab, text='Destination')
destination_entry = ttk.Entry(data_input_tab)

miles_label = ttk.Label(data_input_tab, text='Miles')
miles_entry = ttk.Entry(data_input_tab)

equipment_label = ttk.Label(data_input_tab, text='Equipment')
equipment_dropdown = ttk.Combobox(data_input_tab, values=['None', 'Flat', 'Reefer', 'Van'])

commodity_label = ttk.Label(data_input_tab, text='Commodity')
commodity_dropdown = ttk.Combobox(data_input_tab, values=['A-Frame', 'Yogurt'])

# Place widgets in grid
origin_label.grid(column=0, row=0, padx=5, pady=5, sticky='w')
origin_entry.grid(column=1, row=0, padx=5, pady=5)

destination_label.grid(column=0, row=1, padx=5, pady=5, sticky='w')
destination_entry.grid(column=1, row=1, padx=5, pady=5)

miles_label.grid(column=0, row=2, padx=5, pady=5, sticky='w')
miles_entry.grid(column=1, row=2, padx=5, pady=5)

equipment_label.grid(column=0, row=3, padx=5, pady=5, sticky='w')
equipment_dropdown.grid(column=1, row=3, padx=5, pady=5)

commodity_label.grid(column=0, row=4, padx=5, pady=5, sticky='w')
commodity_dropdown.grid(column=1, row=4, padx=5, pady=5)

def autofill_zip(zipcode):
    search = SearchEngine()
    zipcode_data = search.by_zipcode(zipcode)
    city = zipcode_data.major_city
    state = zipcode_data.state_abbr
    return f"{zipcode}, {city}, {state}"

# Get the input values from the GUI
def run_ra():
    origin = origin_entry.get()
    destination = destination_entry.get()
    miles = miles_entry.get()
    equipment = equipment_dropdown.get()
    commodity = commodity_dropdown.get()
###################################################   FOR USE IN DEVELOPMENT ENVIRONMENT ONLY SECURE BEFORE PRODUCTION ###################################################
    username = '!!ENTER USERNAME!!'
    pwrd = '!!ENTER PASSWORD!!'
################################################### ^^^ FOR USE IN DEVELOPMENT ENVIRONMENT ONLY!! SECURE BEFORE PRODUCTION ^^^ ###################################################
# Open a Chrome browser to a specific URL
    driver = webdriver.Chrome()
    driver.get('https://rates.truckstop.com/')
    time.sleep(1)

# Credentials
    username_input = driver.find_element("id", 'UserName')
    username_input.send_keys(username)
    pwrd_input = driver.find_element("id", 'Password')
    pwrd_input.send_keys(pwrd)
    login = driver.find_element("xpath", '/html/body/div/div[1]/div[1]/form/div/div[2]/div[1]/input')
    login.click()
#    cancel_click = driver.find_element("xpath", '/html/body/div[1]/div/div/div/div[3]/input[2]')
#    cancel_click.click()
    time.sleep(.5)

# Autofill the origin input
    origin_zip = origin.split(',')[0].strip()
    origin_autofill = autofill_zip(origin_zip)
    origin_input = driver.find_element("xpath", '//*[@id="leftMenuRateSearch"]/div[1]/ra-input-location/span/input')
    origin_input.send_keys(origin_autofill)
    time.sleep(.5)
    origin_input.send_keys(Keys.ENTER)

# Autofill the Destination input
    destination_zip = destination.split(',')[0].strip()
    destination_autofill = autofill_zip(destination_zip)
    destination_input = driver.find_element("xpath", '//*[@id="leftMenuRateSearch"]/div[5]/ra-input-location/span/input')
    destination_input.send_keys(destination_autofill)
    time.sleep(.5)
    destination_input.send_keys(Keys.ENTER)

#Fill in Equipment Option
    equipment_options = driver.find_element("xpath", '//*[@id="etrates"]')
    equipment_none = driver.find_element("xpath", '//*[@id="etrates"]/option[1]')
    equipment_flat = driver.find_element("xpath", '//*[@id="etrates"]/option[2]')
    equipment_refer = driver.find_element("xpath", '//*[@id="etrates"]/option[3]')
    equipment_van = driver.find_element("xpath", '//*[@id="etrates"]/option[4]')

    for option in equipment:
        if equipment == 'None':
            equipment_none.click()
        elif equipment == 'Flat':
            equipment_flat.click()
        elif equipment == 'Refer':
            equipment_refer.click()
        elif equipment == 'Van':
            equipment_van.click()
        break
    time.sleep(1)

# Fill in Commodity Option
    #**********ADD LATER*************
# Run Lane Analysis
    run_lane = driver.find_element('xpath', '//*[@id="addLane-RunAnaly"]')
    run_lane.click()
    time.sleep(2)
    lane_url.append(driver.current_url)
    driver.implicitly_wait()
    # got_miles = driver.find_element('xpath', )
    # got_fuel = driver.find_element('xpath', )
    # got_fuelrpm = driver.find_element('xpath', )
    # got_air = driver.find_element('xpath', )
    # got_cons = driver.find_element('xpath', )
    # got_consrpm = driver.find_element('xpath', )

di_submit_button = ttk.Button(data_input_tab, text='Submit', command=run_ra)
di_submit_button.grid(column=0, row=5, columnspan=2, padx=5, pady=5)

# ra_data = {
#     'Origin':origin_entry.get(),
#     'Destination':destination_entry.get(),
#     'Miles':got_miles,
#     'Equip':equipment_dropdown.get(),
#     'Avg Fuel(FLAT)':got_fuel,
#     'Avg Fuel (RPM)':got_fuelrpm,
#     'All In Rate (FLAT)':got_air,
#     'Consumer Rate (FLAT)':got_cons,
#     'Consumer Rate (RPM)':got_consrpm
# }

# Create the table for the Rate Analysis tab
# RA_columns = ['Origin', 'Destination', 'Miles', 'Equip', 'Avg Fuel(FLAT)', "Avg Fuel (RPM)", "All In Rate (FLAT)", "Consumer Rate (FLAT)", "Consumer Rate (RPM)"]
# ra_table = ttk.Treeview(RA_tab, columns=RA_columns, show='headings')
#
# for col in RA_columns:
#     ra_table.heading(col, text=col)
#
# ra_table.column('Origin', width=100)
# ra_table.column('Destination', width=100)
# ra_table.column('Miles', width=75)
# ra_table.column('Equip', width=100)
# ra_table.column('Avg Fuel(FLAT)', width=100)
# ra_table.column('Avg Fuel (RPM)', width=100)
# ra_table.column('All In Rate (FLAT)', width=175)
# ra_table.column('Consumer Rate (FLAT)', width=175)
# ra_table.column('Consumer Rate (RPM)', width=100)
#
# ra_table.config(height=10)
# ra_table.pack(fill='both')

# ra_table.insert('', 'end', values=[ra_data['Origin'], ra_data['Destination'], ra_data['Miles'], ra_data['Equip'], ra_data['Avg Fuel(FLAT)'], ra_data['Avg Fuel (RPM)'], ra_data['All In Rate (FLAT)'], ra_data['Consumer Rate (FLAT)'], ra_data['Consumer Rate (RPM)']])

# CARRIER CLOUD TAB ####################################################################################################
CarrierCloud_tab = ttk.Frame(tab_control)
tab_control.add(CarrierCloud_tab, text='Carrier Cloud')

df= pd.read_csv("C:/Users/danie/OneDrive/Desktop/FinderBot/CarrierDatabase_Main.csv")

CC_Columns = ['Carrier Name', 'Phone Number', 'MC #', 'P/U Zip', 'DEL Zip', 'Equip Length', 'Equip Type', 'Insurance Coverage Amount', 'Role', 'Hazmat' ]
cc_table = ttk.Treeview(CarrierCloud_tab, columns=CC_Columns, show='headings')

for col in CC_Columns:
    cc_table.heading(col, text=col)

# Set the width of each column
cc_table.column("Carrier Name", width=150)
cc_table.column("Phone Number", width=150)
cc_table.column("MC #", width=150)
cc_table.column("P/U Zip", width=100)
cc_table.column("DEL Zip", width=100)
cc_table.column("Equip Length", width=85)
cc_table.column("Equip Type", width=75)
cc_table.column("Insurance Coverage Amount", width=150)
cc_table.column("Role", width=100)
cc_table.column("Hazmat", width=75)

# Add a dropdown menu to the Equip Type column
equip_options = ['Flatbed', 'Dry Van', 'Dry Van LG', 'RGN', 'Hot Shot', 'Box Truck', 'Box Truck LG', 'Step Deck','Step Deck LR' ,'Reefer']
def on_select(event):
    selected = event.widget.get()
    print(selected)
cc_table.column("Equip Type", width=100, anchor="center")
cc_table.heading("Equip Type", text="Equip Type")
cc_table.column("Equip Type", width=100, anchor="center")
cc_table['show'] = 'headings'

for index, row in df.iterrows():
    values = [row[column] for column in CC_Columns]
    cc_table.insert("", index, values=values)

cc_table.grid(row=0, column=0, padx=5, pady=5, ipadx=0)

# Create Right Click Menu for CarrierCloud tab

def cc_right_click(event):
    row_ids = cc_table.selection()

    if row_ids:
        rc_menu = tk.Menu(CarrierCloud_tab, tearoff=0)
        rc_menu.add_command(label="Edit", command=lambda: show_carrier_profile(os.path.join(profiles, cc_table.item(row_ids)['values'][0] + '.txt')))
        rc_menu.add_command(label="Delete")
        rc_menu.add_separator()
        rc_menu.add_command(label="Cancel")
        rc_menu.post(event.x_root, event.y_root)

cc_table.bind("<Button-3>", cc_right_click)

# Create Carrier Profile
def create_carrier_profile(filename):
    output_dir = profiles
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            filename = os.path.join(output_dir, row[0] + '.txt')
            with open(filename, 'w') as textfile:
                textfile.write('\n'.join(row[0:]))

# Create a pop up window for Carrier Entry
def open_popup():
    role_options = ['Driver', 'Dispatch']

    # Create the pop-up window
    popup = tk.Toplevel(root)
    popup.title("Enter Carrier information")

    # Create the entry form
    tk.Label(popup, text="Carrier Name:").grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(popup)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(popup, text="Phone Number 1:").grid(row=1, column=0, padx=5, pady=5)
    phone1_entry = tk.Entry(popup)
    phone1_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(popup, text="Phone Number 2:").grid(row=2, column=0, padx=5, pady=5)
    phone2_entry = tk.Entry(popup)
    phone2_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(popup, text="MC #:").grid(row=3, column=0, padx=5, pady=5)
    mc_entry = tk.Entry(popup)
    mc_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(popup, text="P/U Zip:").grid(row=4, column=0, padx=5, pady=5)
    pu_zip = tk.Entry(popup)
    pu_zip.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(popup, text="DEL Zip:").grid(row=5, column=0, padx=5, pady=5)
    del_zip = tk.Entry(popup)
    del_zip.grid(row=5, column=1, padx=5, pady=5)

    tk.Label(popup, text="Equipment Length:").grid(row=6, column=0, padx=5, pady=5)
    equip_len_entry = tk.Entry(popup)
    equip_len_entry.grid(row=6, column=1, padx=5, pady=5)

    tk.Label(popup, text="Equipment Type:").grid(row=7, column=0, padx=5, pady=5)
    equip_type_entry = ttk.Combobox(popup, values=equip_options)
    equip_type_entry.grid(row=7, column=1, padx=5, pady=5)

    tk.Label(popup, text="Insurance Coverage Amount:").grid(row=8, column=0, padx=5, pady=5)
    ins_entry = tk.Entry(popup)
    ins_entry.grid(row=8, column=1, padx=5, pady=5)

    tk.Label(popup, text="Role:").grid(row=9, column=0, padx=5, pady=5)
    role_entry = ttk.Combobox(popup, values=role_options)
    role_entry.grid(row=9, column=1, padx=5, pady=5)

    tk.Label(popup, text="Hazmat Endorsement?:").grid(row=10, column=0, padx=5, pady=5)
    haz_entry = ttk.Checkbutton(popup, offvalue="No")
    haz_entry.grid(row=10, column=1, padx=5, pady=5)


    def submit_form():
        # Get the values from the entry fields
        carrier_name = name_entry.get()
        phone1 = phone1_entry.get()
        phone2 = phone2_entry.get()
        equip_len = equip_len_entry.get()
        equip_type = equip_type_entry.get()
        insurance = ins_entry.get()
        role = role_entry.get()
        haz_var = tk.BooleanVar()
        # haz_entry = tk.Checkbutton(popup, text="Hazmat", variable=haz_var)
        hazmat = "Yes" if haz_var.get() else "No"

        # Apply formatting to the values
        formatted_phone = f"({phone1[:3]}) {phone1[3:6]}-{phone1[6:]} {phone2}"
        formatted_equip_len = f"{equip_len}' "
        formatted_insurance = f"${int(insurance):,}"
        # Name Formatting
        name_parts = carrier_name.split(' ')
        first_name = name_parts[0].capitalize()
        last_name = ' '.join([name_part.capitalize() for name_part in name_parts[1:]])

        # Combine the formatted first and last name
        formatted_name = f"{first_name} {last_name}"

        # Create a dictionary with the values
        data = {'Carrier Name': formatted_name,
                'Phone Number': formatted_phone,
                'MC #': mc_entry.get(),
                'P/U Zip': pu_zip.get(),
                'DEL Zip': del_zip.get(),
                'Equip Length': formatted_equip_len,
                'Equip Type': equip_type_entry.get(),
                'Insurance Coverage Amount': formatted_insurance,
                'Role': role_entry.get(),
                'Hazmat': hazmat}

        # Add the new row to the table
        cc_table.insert('', 'end', values=[data['Carrier Name'], data['Phone Number'], data['MC #'], data['P/U Zip'], data['DEL Zip'] , data['Equip Length'],
                                           data['Equip Type'], data['Insurance Coverage Amount'], data['Role'], data['Hazmat'],
                                           ])
        with open("C:/Users/danie/OneDrive/Desktop/FinderBot/CarrierDatabase_Main.csv", 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data.values())
        create_carrier_profile(Database)
        popup.destroy()

        # Create the submit button
    submit_button = tk.Button(popup, text="Submit", command=submit_form)
    submit_button.grid(row=11, column=1, padx=5, pady=5)

create_carrier_profile(Database)
AddButton = Button(CarrierCloud_tab, text="Add Carrier", command=open_popup)
AddButton.grid(column=0, row=4)

# Display Carrier Profile
# Bind the name column to the pop-up window function
def show_carrier_profile(filename):
    with open(filename, 'r') as textfile:
        contents = textfile.read()
    messagebox.showinfo("Carrier Profile", contents)

cc_table.tag_bind('Carrier Name', '<Button-1>', show_carrier_profile)

# Carrier Profile Index
# cpi_tab = ttk.Frame(tab_control)
# tab_control.add(cpi_tab, text='Carrier Profile Index')
# cpi_columns = ["Name", "Date Modified"]
# cpi_treeview = ttk.Treeview(cpi_tab, columns=cpi_columns, show='headings' )
#
# def show_files():
#     folder_path = profiles
#     files = os.listdir(folder_path)
#     for file in files:
#         file_path = os.path.join(folder_path, file)
#         mod_time = os.path.getmtime(file_path)
#         cpi_treeview.insert("", "end", values=(file, mod_time))
#
# # add columns to the treeview
# cpi_treeview.heading("Name", text="Name")
# cpi_treeview.heading("Date Modified", text="Date Modified")
#
# # display files in the treeview
# show_files()
#
# # pack the treeview in the "Index" tab
# cpi_treeview.pack(fill=tk.BOTH, expand=True)

# FINDER BOT TAB #######################################################################################################
finderbot_tab = ttk.Frame(tab_control)
tab_control.add(finderbot_tab, text='Finder Bot')

#FINDER BOT#############################################################################################################
def FinderBot_Scraper3():
    # Read in list of URLs from CSV file
    urls_df = pd.read_csv("C:/Users/danie/OneDrive/Desktop/FinderBot/urls.csv")
    urls = urls_df["URL"].tolist()

    unscraped = deque(urls)

    scraped = set()

    emails = set()
    email_count = 0  # Counter for number of emails found

    while len(unscraped) and email_count < 250:  # Stop program when 10 emails have been found
        url = unscraped.popleft()
        scraped.add(url)

        parts = urlsplit(url)

        base_url = "{0.scheme}://{0.netloc}".format(parts)
        if '/' in parts.path:
            path = url[:url.rfind('/') + 1]
        else:
            path = url

        print("Crawling URL %s" % url, email_count)
        try:
            response = requests.get(url, timeout=25)  # Set timeout to 25 seconds
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            continue

        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", response.text, re.I))
        emails.update(new_emails)
        email_count += len(new_emails)  # Increment email count by number of new emails found

        soup = BeautifulSoup(response.text, 'lxml')

        for anchor in soup.find_all("a"):
            if "href" in anchor.attrs:
                link = anchor.attrs["href"]
            else:
                link = ''

            if link.startswith('/'):
                link = base_url + link

            elif not link.startswith('http'):
                link = path + link

            if not link.endswith(".gz") and not link.endswith(".jpg") and not link.endswith(
                    ".jpeg") and not link.endswith(".png") and not link.endswith(".gif") and not link.endswith(".pdf"):
                if not link in unscraped and not link in scraped:
                    unscraped.append(link)

    df = pd.DataFrame(emails, columns=["Email"])
    df.to_csv('C:/Users/danie/OneDrive/Desktop/FinderBot/FoundEmails.csv', index=False)

keyword_label = ttk.Label(finderbot_tab, text="Keyword/Industry Type:")
keyword_entry = ttk.Entry(finderbot_tab)
keyword_label.grid(column=0, row=0)
keyword_entry.grid(column=1, row=0)

zip_label = ttk.Label(finderbot_tab, text="Zip Code:")
zip_entry = ttk.Entry(finderbot_tab)
zip_label.grid(column=0, row=1)
zip_entry.grid(column=1, row=1)

distance_label = ttk.Label(finderbot_tab, text="Distance (Miles):")
distance_entry = ttk.Combobox(finderbot_tab, values=["25", "50", "75", "100", "200"])
distance_label.grid(column=0, row=2)
distance_entry.grid(column=1, row=2)

Run_Button = Button(finderbot_tab, text="Run", command=FinderBot_Scraper3)
Run_Button.grid(column=0, row=3)


tab_control.pack(expand=1, fill='both')
root.mainloop()