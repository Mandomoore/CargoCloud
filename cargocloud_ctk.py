import customtkinter as ctk
from customtkinter import ARC, CENTER, E, END, INSERT, LEFT, N, NS, ON, S, SE, SEL, SW, W, WORD, Y
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from uszipcode import SearchEngine
import re
import requests
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import sqlite3
from PIL import Image, ImageTk
from modules import zip_search


conn = sqlite3.connect('carrier-data/cargo_cloud.db')
cursor = conn.cursor()

lane_url = []

# Create the main window
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")
root = ctk.CTk()
root.title('CargoCloud')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")

# Create the tabs
tab_control = ttk.Notebook(root)

# RATE ANALYSIS DATA INPUT TAB ########################################################################################
data_input_tab = ctk.CTkFrame(tab_control)
tab_control.add(data_input_tab, text='Rate Analysis')

# Create the widgets for the Data Input tab
origin_label = ctk.CTkLabel(data_input_tab, text='Origin Zip')
origin_entry = ctk.CTkEntry(data_input_tab)

destination_label = ctk.CTkLabel(data_input_tab, text='Destination Zip')
destination_entry = ctk.CTkEntry(data_input_tab)

miles_label = ctk.CTkLabel(data_input_tab, text='Miles')
miles_entry = ctk.CTkEntry(data_input_tab)

equipment_label = ctk.CTkLabel(data_input_tab, text='Equipment')
equipment_dropdown = ttk.Combobox(data_input_tab, values=['None', 'Flat', 'Reefer', 'Van'])

commodity_label = ctk.CTkLabel(data_input_tab, text='Commodity')
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

# Get the input values from the GUI
def autofill_zip(zipcode):
    search = SearchEngine()
    zipcode_data = search.by_zipcode(zipcode)
    city = zipcode_data.major_city
    state = zipcode_data.state_abbr
    return f"{zipcode}, {city}, {state}"

def run_ra():

    origin = origin_entry.get()
    destination = destination_entry.get()
    miles = miles_entry.get()
    equipment = equipment_dropdown.get()
    commodity = commodity_dropdown.get()
    ###################################################   FOR USE IN DEVELOPMENT ENVIRONMENT ONLY!! SECURE BEFORE PRODUCTION ###################################################
    username = '!!ENTER USERNAME!!'
    pwrd = '!!ENTER PASSWORD!!'
    ################################################### ^^^ FOR USE IN DEVELOPMENT ENVIRONMENT ONLY!! SECURE BEFORE PRODUCTION ^^^ ###################################################
    # Open a Chrome browser to a specific URL
    driver = webdriver.Chrome()
    driver.get('https://rates.truckstop.com/')
    time.sleep(5)

    # Credentials
    username_input = driver.find_element("id", 'UserName')
    username_input.send_keys(username)
    time.sleep(2)
    pwrd_input = driver.find_element("id", 'Password')
    pwrd_input.send_keys(pwrd)
    time.sleep(2)
    login = driver.find_element("xpath", '/html/body/div/div[1]/div[1]/form/div/div[2]/div[1]/input')
    login.click()
    #    cancel_click = driver.find_element("xpath", '/html/body/div[1]/div/div/div/div[3]/input[2]')
    #    cancel_click.click()
    time.sleep(10)

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
    destination_input = driver.find_element("xpath",
                                            '//*[@id="leftMenuRateSearch"]/div[5]/ra-input-location/span/input')
    destination_input.send_keys(destination_autofill)
    time.sleep(.5)
    destination_input.send_keys(Keys.ENTER)

    # Fill in Equipment Option
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
    # **********ADD LATER*************
    # Run Lane Analysis
    run_lane = driver.find_element('xpath', '//*[@id="addLane-RunAnaly"]')
    run_lane.click()
    time.sleep(2)
    lane_url.append(driver.current_url)
    driver.implicitly_wait(.5)

di_submit_button = ctk.CTkButton(data_input_tab, text='Submit', command=lambda: run_ra())
di_submit_button.grid(column=0, row=5, columnspan=2, padx=5, pady=5)


# CARRIER CLOUD TAB ####################################################################################################
CarrierCloud_tab = ctk.CTkFrame(tab_control)
tab_control.add(CarrierCloud_tab, text='CarrierCloud')

#Buttons-----------------------------------------
#Add Carrier Button
AddButton = ctk.CTkButton(CarrierCloud_tab, text="Add Carrier", command=lambda: add_carrier_popup())
AddButton.grid(column=0, row=0)

#Refresh Button
script_dir = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(script_dir, "config", "refresh.png")
original_image = Image.open(img_path)
resized_image = original_image.resize((25, 25), Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.BICUBIC)
refresh_img = ImageTk.PhotoImage(resized_image)
RefreshButton_frame = ctk.CTkFrame(CarrierCloud_tab)
RefreshButton = ctk.CTkButton(RefreshButton_frame, image=refresh_img, text="Refresh", command=lambda: update_carrier_table())
RefreshButton_frame.grid(column=0, row=0, sticky='e')
RefreshButton.grid(column=1, row=0, sticky='e')

#View Profile Button
view_profile_button = ctk.CTkButton(RefreshButton_frame, text="View Profile", command=lambda: view_profile(cc_table.item(cc_table.selection())['values'][0]))
view_profile_button.grid(column=0, row=0, sticky='w')

#Search Entry & Search Button
search_frame = ctk.CTkFrame(CarrierCloud_tab)
search_frame.grid(row=0, column=0, padx=5, pady=5, sticky='w')
search_dropdown = ttk.Combobox(search_frame, values=["All", "Zip Code ('zipcode:miles')", "Insurance ('amount')"])
search_dropdown.set("All")
search_label = ctk.CTkLabel(search_frame, text="Search:")
search_entry = ctk.CTkEntry(search_frame)
search_button = ctk.CTkButton(search_frame, text="Search", command=lambda: search_carrier())
search_dropdown.grid(column=0, row=0, padx=5, pady=5, sticky='w')
search_label.grid(column=1, row=0, padx=5, pady=5, sticky='w')
search_entry.grid(column=2, row=0, padx=5, pady=5, sticky='w')
search_button.grid(column=3, row=0, padx=5, pady=5, sticky='w')


#Carrier Table-------------------------------------
cc_table_height = 30

CC_Columns = ['MC#', 'Carrier Name', 'Phone Number', 'Homebase Zip', 'Equip Len', 'Equip Type',
              'Insurance Coverage Amount', 'Role', 'Hazmat', 'US Citizen', 'Rating']

cc_table = ttk.Treeview(CarrierCloud_tab, columns=CC_Columns, show='headings', height=cc_table_height)

# Set column weights for cc_table
for col in CC_Columns:
    cc_table.column(col, anchor=tk.CENTER)
    cc_table.heading(col, text=col)

# Grid layout for cc_table
cc_table.grid(column=0, row=1, sticky=(tk.N, tk.S, tk.W, tk.E))

# Configure column weights for cc_table
for col in CC_Columns:
    CarrierCloud_tab.grid_columnconfigure(CC_Columns.index(col), weight=1)

for col in CC_Columns:
    cc_table.heading(col, text=col)

# Set the width of each column
cc_table.column(0, width=85)   # MC #
cc_table.column(1, width=150)  # Carrier Name
cc_table.column(2, width=100)  # Phone Number
cc_table.column(3, width=100)  # Homebase Zip
cc_table.column(4, width=85)   # Equip Len
cc_table.column(5, width=100)  # Equip Type
cc_table.column(6, width=150)  # Insurance Coverage Amount
cc_table.column(7, width=100)  # Role
cc_table.column(8, width=75)   # Hazmat
cc_table.column(9, width=75)   # US Citizen
cc_table.column(10, width=75)  # Rating

equip_options = ['Flatbed', 'Dry Van', 'Dry Van LG', 'RGN', 'Hot Shot', 'Box Truck', 'Box Truck LG', 'Step Deck',
                 'Step Deck LR', 'Reefer', 'Conestoga']

role_options = ['Driver', 'Dispatch', 'Owner/Op']

cc_table.heading("Equip Type", text="Equip Type")
cc_table['show'] = 'headings'
cc_table.grid(row=1, column=0, padx=5, pady=5, ipadx=0)

def on_select(event):
    selected = event.widget.get()
    print(selected)

def calculate_weighted_total_rating(english, communication, reachability, punctuality, macropoint, blacklist):
    return english * 0.15 + communication * 0.15 + reachability * 0.30 + punctuality * 0.30 + macropoint * 10 + blacklist * -100

def update_carrier_table():
    cc_table.delete(*cc_table.get_children())  # Clear existing entries in the table

    # Fetch data from the carrier_info and carrier_rating tables
    cursor.execute('''
        SELECT ci.mc_number, ci.carrier_name, ci.phone_number, ci.homebase_zip, ci.equip_length, ci.equip_type,
               ci.insurance_amount, ci.role, ci.hazmat, ci.us_citizen, AVG(cr.total_rating) as average_rating
        FROM carrier_info ci
        LEFT JOIN carrier_rating cr ON ci.mc_number = cr.mc_number
        GROUP BY ci.mc_number
        ORDER BY average_rating DESC
    ''')

    # Fetch the data and store it in the 'data' variable
    data = cursor.fetchall()

    # Sort the data by Rating (average_rating)
    # data.sort(key=lambda x: x[-1], reverse=True)
    data.sort(key=lambda x: x[-1] if x[-1] is not None else float('-inf'), reverse=True)

    for row in data:
        (mc_number, carrier_name, phone_number, homebase_zip, equip_length, equip_type, insurance_amount, role, hazmat,
         us_citizen, average_rating) = row

        # Check if average_rating is None and provide a default value
        average_rating = average_rating if average_rating is not None else 0.0

        # Update the average_rating in the carrier_info table
        cursor.execute('''
                    UPDATE carrier_info
                    SET rating = ?
                    WHERE mc_number = ?
                ''', (average_rating, mc_number))

        # Check if mc_number is in the blacklist
        cursor.execute("SELECT COUNT(*) FROM blacklist WHERE mc_number = ?", (mc_number,))
        is_blacklisted = cursor.fetchone()[0]

        # Set a tag for each row based on the blacklist condition
        tag = 'red' if is_blacklisted else ''

        cc_table.insert('', 'end', values=(mc_number, carrier_name, phone_number, homebase_zip, equip_length,
                                           equip_type, insurance_amount, role, hazmat, us_citizen,
                                           f"{average_rating:.2f}"), tags=(tag,))
        cc_table.tag_configure('red', foreground='red')
    conn.commit()

update_carrier_table()

# Create Right Click Menu for CarrierCloud tab
def cc_right_click(event):
    row_ids = cc_table.selection()

    if row_ids:
        rc_menu = tk.Menu(CarrierCloud_tab, tearoff=0)
        rc_menu.add_command(label="Rate", command=lambda: rate_carrier(cc_table.item(row_ids)['values'][0]))
        rc_menu.add_separator()
        rc_menu.add_command(label="Edit", command=lambda: edit_carrier_info(cc_table.item(row_ids)['values'][0]))
        rc_menu.add_command(label="Delete", command=lambda: confirm_delete_carrier(cc_table.item(row_ids)['values'][0]))
        rc_menu.add_separator()
        rc_menu.add_command(label="Cancel")
        rc_menu.post(event.x_root, event.y_root)

#Carrier Rating Window & Logic-----------------------------
def rate_carrier(mc_number):
    rate_popup = ctk.CTkToplevel(root)
    rate_popup.title(f"Rate Carrier {mc_number}")
    rate_popup.geometry("400x450")

    ctk.CTkLabel(rate_popup, text="Pro #:").grid(row=0, column=0, padx=5, pady=5)
    pro_num_entry = ctk.CTkEntry(rate_popup)
    pro_num_entry.grid(row=0, column=1, padx=5, pady=5)

    eng_frame = ctk.CTkFrame(rate_popup)
    eng_rate = ctk.CTkSlider(eng_frame, orientation='horizontal', from_=1, to=10, width=200)
    eng_frame.grid(column=0, row=1, padx=5, pady=5)

    eng_rate.grid(row=1, column=0, padx=5, pady=5)

    comm_rate = ctk.CTkSlider(rate_popup, orient='horizontal', from_=1, to=10, label="Communication", length=200)
    comm_rate.grid(row=2, column=0, padx=5, pady=5)

    reach = ctk.CTkSlider(rate_popup, orient='horizontal', from_=1, to=10, label="Reachability", length=200)
    reach.grid(row=3, column=0, padx=5, pady=5)

    punct = ctk.CTkSlider(rate_popup, orient='horizontal', from_=1, to=10, label="Punctuality", length=200)
    punct.grid(row=4, column=0, padx=5, pady=5)

    ctk.CTkLabel(rate_popup, text="MacroPoint Tracking Accepted?").grid(row=5, column=0, padx=5, pady=5)
    macro_val = tk.BooleanVar()
    macro = ctk.CTkCheckBox(rate_popup, variable=macro_val, offvalue="No")
    macro.grid(row=5, column=1, padx=5, pady=5)

    ctk.CTkLabel(rate_popup, text="Blacklist Carrier?").grid(row=6, column=0, padx=5, pady=5)
    blacklist_val = tk.BooleanVar()
    blacklist = ctk.CTkCheckBox(rate_popup, variable=blacklist_val, offvalue="No")
    blacklist.grid(row=6, column=1, padx=5, pady=5)

    def submit_rating():
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect('carrier-data/cargo_cloud.db')
            cursor = conn.cursor()

            # Get values from widgets
            pro_num = pro_num_entry.get()
            english = eng_rate.get()
            communication = comm_rate.get()
            reachability = reach.get()
            punctuality = punct.get()
            macropoint = 1 if macro_val.get() else 0
            blacklist = 1 if blacklist_val.get() else 0

            # Calculate the total_rating based on your weighting logic
            total_rating = calculate_weighted_total_rating(english, communication, reachability, punctuality,
                                                           macropoint, blacklist)

            # Insert or update the rating in the carrier_rating table
            cursor.execute('''
                            INSERT OR REPLACE INTO carrier_rating (mc_number, pro_number, english, communication, 
                            reachability, punctuality, macropoint, blacklist, total_rating)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
            mc_number, pro_num, english, communication, reachability, punctuality, macropoint, blacklist, total_rating))

            if blacklist == 1:
                cursor.execute("INSERT INTO blacklist (mc_number) VALUES (?)", (mc_number,))

            # Commit the changes and close the connection
            conn.commit()
            conn.close()

            # Show success message
            messagebox.showinfo("Success", "Rating submitted successfully!")
            update_carrier_table()
            rate_popup.destroy()

        except Exception as e:
            # Handle exceptions, log errors, etc.
            print(f"Error: {e}")
            messagebox.showerror("Error", "An error occurred while submitting the rating.")

    submit_button = ctk.CTkButton(rate_popup, text="Submit Rating", command=submit_rating)
    submit_button.grid(row=7, column=0, columnspan=2, pady=5)

def confirm_delete_carrier(mc_number):
    confirmation = messagebox.askyesno("Confirmation", f"Do you want to delete the carrier with MC #: {mc_number}")
    if confirmation:
        delete_carrier(mc_number)

def delete_carrier(mc_number):
    result = messagebox.askquestion("Delete Carrier", "Are you sure you want to delete this carrier?", icon='warning')
    if result == 'yes':
        try:
            # Delete from carrier_info table
            cursor.execute('DELETE FROM carrier_info WHERE mc_number = ?', (mc_number,))

            # Delete from carrier_notes table
            cursor.execute('DELETE FROM carrier_notes WHERE mc_number = ?', (mc_number,))

            cursor.execute('DELETE FROM carrier_rating WHERE mc_number = ?', (mc_number,))

            cursor.execute('DELETE FROM carrier_phone2 WHERE mc_number = ?', (mc_number,))

            cursor.execute('DELETE FROM blacklist WHERE mc_number = ?', (mc_number,))

            conn.commit()
            update_carrier_table()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error deleting carrier: {e}")

cc_table.bind("<Button-3>", cc_right_click)


#ADD CARRIER INFO ---------------------------------------
# Create a pop up window for Carrier Entry
def add_carrier_popup():
    # role_options = ['Driver', 'Dispatch', 'Owner/Op']

    # Create the pop-up window
    add_popup = ctk.CTkToplevel(root)
    add_popup.title("Enter Carrier information")
    add_popup.geometry("850x550")

    ctk.CTkLabel(add_popup, text="MC #:").grid(row=0, column=0, padx=5, pady=5)
    mc_entry = ctk.CTkEntry(add_popup)
    mc_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(add_popup, text="Carrier Name:").grid(row=1, column=0, padx=5, pady=5)
    name_entry = ctk.CTkEntry(add_popup)
    name_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(add_popup, text="Phone Number 1:").grid(row=2, column=0, padx=5, pady=5)
    phone1_entry = ctk.CTkEntry(add_popup)
    phone1_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(add_popup, text="Phone Number 2:").grid(row=3, column=0, padx=5, pady=5)
    phone2_entry = ctk.CTkEntry(add_popup)
    phone2_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(add_popup, text="Homebase Zip:").grid(row=4, column=0, padx=5, pady=5)
    homebase_zip = ctk.CTkEntry(add_popup)
    homebase_zip.grid(row=4, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(add_popup, text="Equipment Length:").grid(row=5, column=0, padx=5, pady=5)
    equip_len_entry = ctk.CTkEntry(add_popup)
    equip_len_entry.grid(row=5, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(add_popup, text="Equipment Type:").grid(row=6, column=0, padx=5, pady=5)
    equip_type_entry = ttk.Combobox(add_popup, values=equip_options)
    equip_type_entry.grid(row=6, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(add_popup, text="Insurance Coverage Amount:").grid(row=7, column=0, padx=5, pady=5)
    ins_entry = ctk.CTkEntry(add_popup)
    ins_entry.grid(row=7, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(add_popup, text="Role:").grid(row=8, column=0, padx=5, pady=5)
    role_entry = ttk.Combobox(add_popup, values=role_options)
    role_entry.grid(row=8, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(add_popup, text="Hazmat Endorsement?:").grid(row=9, column=0, padx=5, pady=5)
    haz_var = tk.BooleanVar()
    haz_entry = ctk.CTkCheckBox(add_popup, variable=haz_var, offvalue="No")
    haz_entry.grid(row=9, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(add_popup, text="U.S. Citizen?:").grid(row=10, column=0, padx=5, pady=5)
    us_cit = tk.BooleanVar()
    us_cit_entry = ctk.CTkCheckBox(add_popup, variable=us_cit, offvalue="No")
    us_cit_entry.grid(row=10, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(add_popup, text="Notes:").grid(row=11, column=0, padx=5, pady=5)
    note_entry = ctk.CTkTextbox(add_popup, height=10, width=80, font=('Calibri', 10))
    note_entry.grid(row=11, column=1, padx=5, pady=5, sticky='w')

    def submit_form():
        # Get the values from the entry fields
        mc_number = mc_entry.get()
        carrier_name = name_entry.get()
        phone1 = phone1_entry.get()
        phone2 = phone2_entry.get()
        home_zip = homebase_zip.get()
        equip_len = equip_len_entry.get()
        equip_type = equip_type_entry.get()
        insurance = ins_entry.get()
        role = role_entry.get()
        hazmat = "Yes" if haz_var.get() else "No"
        citizen = "Yes" if us_cit.get() else "No"
        note = note_entry.get("1.0", tk.END).strip()

        # Apply formatting to the values
        updated_phone1 = ''.join(filter(str.isdigit, phone1))
        formatted_phone1 = f"({updated_phone1[:3]}) {updated_phone1[3:6]}-{updated_phone1[6:]}"
        updated_phone2 = ''.join(filter(str.isdigit, phone2))
        formatted_phone2 = f"({updated_phone2[:3]}) {updated_phone2[3:6]}-{updated_phone2[6:]}"
        formatted_equip_len = f"{equip_len}' "
        formatted_insurance = f"${int(insurance):,}"
        name_parts = carrier_name.split(' ')
        first_name = name_parts[0].capitalize()
        last_name = ' '.join([name_part.capitalize() for name_part in name_parts[1:]])
        formatted_name = f"{first_name} {last_name}"
        # Handle the exception for "RGN" equipment type
        if equip_type.upper() == "RGN":
            formatted_equip_len = f"{equip_len}\" "
        else:
            formatted_equip_len = f"{equip_len}' "

        # Combine the formatted first and last name

        # Create a dictionary with the values
        data = {'MC #': mc_number,
                'Carrier Name': formatted_name,
                'Phone Number': formatted_phone1,
                'Phone Number 2': formatted_phone2,
                'Homebase Zip': home_zip,
                'Equip Length': formatted_equip_len,
                'Equip Type': equip_type,
                'Insurance Coverage Amount': formatted_insurance,
                'Role': role,
                'Hazmat': hazmat,
                'U.S. Citizen': citizen}

        try:
            cursor.execute('''
                    INSERT INTO carrier_info (mc_number, carrier_name, phone_number, homebase_zip, 
                    equip_length, equip_type, insurance_amount, role, hazmat, us_citizen)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (mc_number, formatted_name, formatted_phone1, home_zip, formatted_equip_len, equip_type,
                      formatted_insurance, role, hazmat, citizen ))
            cursor.execute('''
                    INSERT INTO carrier_notes (mc_number, note)
                    VALUES (?, ?)
                ''', (mc_number, note))

            cursor.execute('''
                            INSERT INTO carrier_phone2 (mc_number, phone2)
                            VALUES (?, ?)
                        ''', (mc_number, formatted_phone2))

            conn.commit()
            update_carrier_table()
            add_popup.destroy()

        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", "Carrier with matching MC# is already in the database")

        # Create the submit button

    submit_button = ctk.CTkButton(add_popup, text="Submit", command=submit_form)
    submit_button.grid(row=21, column=1, padx=5, pady=5, sticky='s')


#EDIT CARRIER INFORMATION-----------------------------
def edit_carrier_info(mc_number):
    # role_options = ['Driver', 'Dispatch', 'Owner/Op']

    # Fetch current data for the given MC number
    cursor.execute('SELECT * FROM carrier_info WHERE mc_number = ?', (mc_number,))
    current_data = cursor.fetchone()

    cursor.execute('SELECT note FROM carrier_notes WHERE mc_number = ?', (mc_number,))
    existing_note = cursor.fetchone()

    cursor.execute('SELECT phone2 FROM carrier_phone2 WHERE mc_number = ?', (mc_number,))
    carrier_phone2 = cursor.fetchone()

    # Create an edit popup window
    edit_popup = ctk.CTkToplevel(root)
    edit_popup.title(f"Edit Carrier Information - {mc_number}")
    edit_popup.geometry("850x550")

    # Create and place entry fields with current data
    ctk.CTkLabel(edit_popup, text="MC #:").grid(row=0, column=0, padx=5, pady=5)
    mc_entry = ctk.CTkEntry(edit_popup)
    mc_entry.insert(0, current_data[0])
    mc_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(edit_popup, text="Carrier Name:").grid(row=1, column=0, padx=5, pady=5)
    name_entry = ctk.CTkEntry(edit_popup)
    name_entry.insert(0, current_data[1])
    name_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(edit_popup, text="Phone Number 1:").grid(row=2, column=0, padx=5, pady=5)
    phone1_entry = ctk.CTkEntry(edit_popup)
    phone1_entry.insert(0, current_data[2])
    phone1_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(edit_popup, text="Phone Number 2:").grid(row=3, column=0, padx=5, pady=5)
    phone2_entry = ctk.CTkEntry(edit_popup)
    phone2_entry.insert(0, carrier_phone2[0])
    phone2_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(edit_popup, text="Homebase Zip:").grid(row=4, column=0, padx=5, pady=5)
    home_zip = ctk.CTkEntry(edit_popup)
    home_zip.insert(0, current_data[3])
    home_zip.grid(row=4, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(edit_popup, text="Equipment Length:").grid(row=5, column=0, padx=5, pady=5)
    equip_len_entry = ctk.CTkEntry(edit_popup)
    equip_len_entry.insert(0, current_data[4])
    equip_len_entry.grid(row=5, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(edit_popup, text="Equipment Type:").grid(row=6, column=0, padx=5, pady=5)
    equip_type_entry = ttk.Combobox(edit_popup, values=equip_options)
    equip_type_entry.insert(0, current_data[5])
    equip_type_entry.grid(row=6, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(edit_popup, text="Insurance Coverage Amount:").grid(row=7, column=0, padx=5, pady=5)
    ins_entry = ctk.CTkEntry(edit_popup)
    ins_entry.insert(0, current_data[6])
    ins_entry.grid(row=7, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(edit_popup, text="Role:").grid(row=8, column=0, padx=5, pady=5)
    role_entry = ttk.Combobox(edit_popup, values=role_options)
    role_entry.insert(0, current_data[7])
    role_entry.grid(row=8, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(edit_popup, text="Hazmat Endorsement?:").grid(row=9, column=0, padx=5, pady=5)
    haz_var = tk.BooleanVar()
    haz_value = current_data[8]
    haz_var.set(haz_value == "Yes")
    haz_entry = ctk.CTkCheckBox(edit_popup, variable=haz_var, offvalue="No")
    haz_entry.grid(row=9, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(edit_popup, text="U.S. Citizen?:").grid(row=10, column=0, padx=5, pady=5)
    us_cit = tk.BooleanVar()
    cit_val = current_data[9]
    us_cit.set(cit_val == "Yes")
    us_cit_entry = ctk.CTkCheckBox(edit_popup, variable=us_cit, offvalue="No")
    us_cit_entry.grid(row=10, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(edit_popup, text="Notes:").grid(row=11, column=0, padx=5, pady=5)
    note_entry = ctk.CTkTextbox(edit_popup, height=10, width=80, font=('Calibri', 10))
    # note_entry.insert(tk.END, existing_note[0] if existing_note else "")
    note_entry.grid(row=11, column=1, padx=5, pady=5, sticky='w')

    if existing_note:
        note_entry.insert(tk.END, existing_note[0])

    def submit_edit():
        # Get updated values from entry fields
        updated_mc = mc_entry.get
        updated_name = name_entry.get()
        updated_phone1 = phone1_entry.get()
        updated_phone2 = phone2_entry.get()
        updated_home_zip = home_zip.get()
        updated_equip_len = ''.join(filter(str.isdigit, equip_len_entry.get()))
        updated_equip_type = equip_type_entry.get()
        updated_ins = ins_entry.get().replace('$', '').replace(',', '')
        updated_role = role_entry.get()
        updated_haz = "Yes" if haz_var.get() else "No"
        updated_cit = "Yes" if us_cit.get() else "No"
        existing_notes = note_entry.get("1.0", tk.END).strip()

        #Entry Formatting
        updated_phone1 = ''.join(filter(str.isdigit, updated_phone1))
        formatted_phone = f"({updated_phone1[:3]}) {updated_phone1[3:6]}-{updated_phone1[6:]}"
        updated_phone2 = ''.join(filter(str.isdigit, updated_phone2))
        formatted_phone2 = f"({updated_phone2[:3]}) {updated_phone2[3:6]}-{updated_phone2[6:]}"
        formatted_equip_len = f"{updated_equip_len}' "
        formatted_insurance = f"${int(updated_ins):,}"
        name_parts = updated_name.split(' ')
        first_name = name_parts[0].capitalize()
        last_name = ' '.join([name_part.capitalize() for name_part in name_parts[1:]])
        # Handle the exception for "RGN" equipment type
        if updated_equip_type.upper() == "RGN":
            formatted_equip_len = f"{updated_equip_len}\" "
        else:
            formatted_equip_len = f"{updated_equip_len}' "

        # Combine the formatted first and last name
        formatted_name = f"{first_name} {last_name}"

        data = {'MC #': mc_number,
                'Carrier Name': formatted_name,
                'Phone Number': formatted_phone,
                'Phone Number 2': formatted_phone2,
                'Homebase Zip': updated_home_zip,
                'Equip Length': formatted_equip_len,
                'Equip Type': updated_equip_type,
                'Insurance Coverage Amount': formatted_insurance,
                'Role': updated_role,
                'Hazmat': updated_haz,
                'U.S. Citizen': updated_cit,
                'Notes': existing_notes}

        # Update the database
        try:
            # Update existing row in the carrier_info table
            cursor.execute('''
                            UPDATE carrier_info SET
                                carrier_name = ?,
                                phone_number = ?,
                                homebase_zip = ?,
                                equip_length = ?,
                                equip_type = ?,
                                insurance_amount = ?,
                                role = ?,
                                hazmat = ?,
                                us_citizen = ?
                            WHERE mc_number = ?
                        ''', (formatted_name, formatted_phone, updated_home_zip, formatted_equip_len,
                              updated_equip_type, formatted_insurance, updated_role, updated_haz, updated_cit, mc_number))

            # Insert or update the carrier note in the carrier_notes table
            cursor.execute('''
                        INSERT OR REPLACE INTO carrier_notes (mc_number, note)
                        VALUES (?, ?)
                    ''', (mc_number, existing_notes))

            cursor.execute('''
                            INSERT OR REPLACE INTO carrier_phone2 (mc_number, phone2)
                            VALUES (?, ?)
                        ''', (mc_number, formatted_phone2))
            conn.commit()

            update_carrier_table()
            edit_popup.destroy()

        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", "Carrier with matching MC# is already in the database")

    submit_button = ctk.CTkButton(edit_popup, text="Submit", command=submit_edit)
    submit_button.grid(row=21, column=1, padx=5, pady=5, sticky='s')












#View Profile----------------------------------------
def view_profile(mc_number):
    profile_popup = ctk.CTkToplevel(root)
    profile_popup.geometry("1500x1000")

    # Fetch data from carrier_info table
    cursor.execute('SELECT * FROM carrier_info WHERE mc_number = ?', (mc_number,))
    current_data = cursor.fetchone()

    # Fetch data from carrier_phone2 table
    cursor.execute('SELECT phone2 FROM carrier_phone2 WHERE mc_number = ?', (mc_number,))
    carrier_phone2 = cursor.fetchone()

    # Fetch data from carrier_notes table
    cursor.execute('SELECT note FROM carrier_notes WHERE mc_number = ?', (mc_number,))
    existing_note = cursor.fetchone()

    # Fetch data from carrier_rating table
    cursor.execute('SELECT * FROM carrier_rating WHERE mc_number = ?', (mc_number,))
    carrier_rating_data = cursor.fetchall()

    # Title for the popup
    profile_popup.title(f"{current_data[1]} - MC#{mc_number}")

    # Entry fields for carrier_info
    ctk.CTkLabel(profile_popup, text="MC #:").grid(row=0, column=0, padx=5, pady=5)
    mc_entry = ctk.CTkEntry(profile_popup)
    mc_entry.insert(0, current_data[0])
    mc_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(profile_popup, text="Carrier Name:").grid(row=1, column=0, padx=5, pady=5)
    name_entry = ctk.CTkEntry(profile_popup)
    name_entry.insert(0, current_data[1])
    name_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(profile_popup, text="Phone Number 1:").grid(row=2, column=0, padx=5, pady=5)
    phone1_entry = ctk.CTkEntry(profile_popup)
    phone1_entry.insert(0, current_data[2])
    phone1_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(profile_popup, text="Phone Number 2:").grid(row=3, column=0, padx=5, pady=5)
    phone2_entry = ctk.CTkEntry(profile_popup)
    phone2_entry.insert(0, carrier_phone2[0] if carrier_phone2 else "")
    phone2_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(profile_popup, text="Homebase Zip:").grid(row=4, column=0, padx=5, pady=5)
    home_zip = ctk.CTkEntry(profile_popup)
    home_zip.insert(0, current_data[3])
    home_zip.grid(row=4, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(profile_popup, text="Equipment Length:").grid(row=5, column=0, padx=5, pady=5)
    equip_len_entry = ctk.CTkEntry(profile_popup)
    equip_len_entry.insert(0, current_data[4])
    equip_len_entry.grid(row=5, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(profile_popup, text="Equipment Type:").grid(row=6, column=0, padx=5, pady=5)
    equip_type_entry = ttk.Combobox(profile_popup, values=equip_options)
    equip_type_entry.insert(0, current_data[5])
    equip_type_entry.grid(row=6, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(profile_popup, text="Insurance Coverage Amount:").grid(row=7, column=0, padx=5, pady=5)
    ins_entry = ctk.CTkEntry(profile_popup)
    ins_entry.insert(0, current_data[6])
    ins_entry.grid(row=7, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(profile_popup, text="Role:").grid(row=8, column=0, padx=5, pady=5)
    role_entry = ttk.Combobox(profile_popup, values=role_options)
    role_entry.insert(0, current_data[7])
    role_entry.grid(row=8, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(profile_popup, text="Hazmat Endorsement?:").grid(row=9, column=0, padx=5, pady=5)
    haz_var = tk.BooleanVar()
    haz_value = current_data[8]
    haz_var.set(haz_value == "Yes")
    haz_entry = ctk.CTkCheckBox(profile_popup, variable=haz_var, offvalue="No")
    haz_entry.grid(row=9, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(profile_popup, text="U.S. Citizen?:").grid(row=10, column=0, padx=5, pady=5)
    us_cit = tk.BooleanVar()
    cit_val = current_data[9]
    us_cit.set(cit_val == "Yes")
    us_cit_entry = ctk.CTkCheckBox(profile_popup, variable=us_cit, offvalue="No")
    us_cit_entry.grid(row=10, column=1, padx=5, pady=5, sticky='w')

    note_frame = ctk.CTkFrame(profile_popup)
    # note_frame.grid(column=3, row=1)
    ctk.CTkLabel(note_frame, text="Notes:").grid(row=1, column=3, padx=5, pady=5)
    note_entry = ctk.CTkTextbox(note_frame, height=10, width=80, font=('Calibri', 10))
    note_entry.insert(tk.END, existing_note[0] if existing_note else "")
    note_entry.grid(row=1, column=4, padx=5, pady=5, sticky='w')

    # Table for carrier ratings
    rating_frame = ctk.CTkFrame(profile_popup)
    rating_frame.grid(column=1, row=1)
    rating_table_height = 10
    Rating_Columns = ['Pro #', 'English', 'Communication', 'Reachability', 'Punctuality', 'MacroPoint', 'Blacklist', 'Total Rating']
    rating_table = ctk.CTkTreeview(rating_frame, columns=Rating_Columns, show='headings', height=rating_table_height)

    # Set column weights for rating_table
    for col in Rating_Columns:
        rating_table.column(col, anchor=tk.CENTER)
        rating_table.heading(col, text=col)

    # Configure column weights for rating_table
    for col in Rating_Columns:
        rating_frame.grid_columnconfigure(Rating_Columns.index(col), weight=1)

    # Function to update the rating table based on the selected carrier
    def update_rating_table():
        # Clear existing entries in the rating table
        rating_table.delete(*rating_table.get_children())

        # Fetch rating data for the selected carrier
        for row in carrier_rating_data:
            pro_number, english, communication, reachability, punctuality, macropoint, blacklist, total_rating = row

            # Set a tag for each row based on the blacklist condition
            tag = 'red' if blacklist else ''

            rating_table.insert('', 'end', values=(pro_number, english, communication, reachability, punctuality,
                                                   macropoint, blacklist, f"{total_rating:.2f}"), tags=(tag,))
            rating_table.tag_configure('red', foreground='red')

    # Call the function to populate the rating table
    update_rating_table()























# SEARCH BAR/LOGIC -------------------------------------------------
warning_label = ctk.CTkLabel(search_frame, text="Please allow up to 30 seconds...", fg_color="blue")
def clear_label_text():
    warning_label.configure(text="")

def search_carrier():
    selected_option = search_dropdown.get()
    search_query = search_entry.get().lower()  # Get the search query and convert to lowercase for case-insensitive search
    # search_query = ''.join(filter(str.isdigit, search_query))
    cc_table.delete(*cc_table.get_children())
    if selected_option == "All":
        if search_query == "hazmat":
            cursor.execute('SELECT * FROM carrier_info WHERE hazmat = "Yes"')
        elif search_query == "citizen":
            cursor.execute('SELECT * FROM carrier_info WHERE us_citizen = "Yes"')
        else:
            cursor.execute('''
                SELECT * FROM carrier_info 
                WHERE 
                    mc_number IN (
                        SELECT mc_number FROM carrier_phone2 WHERE lower(phone2) LIKE ?
                    ) OR
                    lower(mc_number) LIKE ? OR 
                    lower(carrier_name) LIKE ? OR 
                    lower(phone_number) LIKE ? OR
                    lower(homebase_zip) LIKE ? OR
                    lower(equip_length) LIKE ? OR
                    lower(equip_type) LIKE ? OR
                    lower(insurance_amount) LIKE ? OR
                    lower(role) LIKE ? OR
                    lower(hazmat) LIKE ? OR
                    lower(us_citizen) LIKE ?
            ''', tuple(['%' + search_query + '%'] * 11)) # Use tuple to repeat the search query for each column

            data = cursor.fetchall()

            # Clear existing entries in the table
            cc_table.delete(*cc_table.get_children())

            # Sort the data by Rating (average_rating)
            data.sort(key=lambda x: x[-1], reverse=True)

            # Repopulate the GUI table with the fetched data
            for row in data:
                (mc_number, carrier_name, phone_number, homebase_zip, equip_length, equip_type, insurance_amount, role,
                 hazmat,
                 us_citizen, average_rating) = row

                # Check if average_rating is None and provide a default value
                average_rating = average_rating if average_rating is not None else 0.0

                # Check if mc_number is in the blacklist
                cursor.execute("SELECT COUNT(*) FROM blacklist WHERE mc_number = ?", (mc_number,))
                is_blacklisted = cursor.fetchone()[0]

                # Set a tag for each row based on the blacklist condition
                tag = 'red' if is_blacklisted else ''

                cc_table.insert('', 'end', values=(mc_number, carrier_name, phone_number, homebase_zip, equip_length,
                                                   equip_type, insurance_amount, role, hazmat, us_citizen,
                                                   f"{average_rating:.2f}"), tags=(tag,))
                cc_table.tag_configure('red', foreground='red')

    elif selected_option == "Zip Code ('zipcode:miles')":
        cc_table.delete(*cc_table.get_children())
        warning_label.configure(text="Please allow up to 30 seconds...", fg_color="blue")
        warning_label.grid(column=4, row=0, padx=5, pady=5, sticky='w')
        search_values = search_query.split(':')

        # Extract zipcode and miles
        zipcode = search_values[0].strip()
        miles = search_values[1].strip() if len(search_values) > 1 else "50"

        # Call find_zip_codes and wait for 20 seconds
        found_zips = zip_search.find_zip_codes(zipcode, miles)
        cc_table.after(20000, lambda: search_table(found_zips))

        def search_table(zips):
            zip_list = found_zips.split(',')

            for zip_code in zip_list:
                cursor.execute('SELECT * FROM carrier_info WHERE lower(homebase_zip) LIKE ?', ('%' + zip_code.strip() + '%',))

                data = cursor.fetchall()

                data.sort(key=lambda x: x[-1], reverse=True)

                # Repopulate the GUI table with the fetched data
                for row in data:
                    (mc_number, carrier_name, phone_number, homebase_zip, equip_length, equip_type, insurance_amount, role,
                     hazmat,
                     us_citizen, average_rating) = row

                    # Check if average_rating is None and provide a default value
                    average_rating = average_rating if average_rating is not None else 0.0

                    # Check if mc_number is in the blacklist
                    cursor.execute("SELECT COUNT(*) FROM blacklist WHERE mc_number = ?", (mc_number,))
                    is_blacklisted = cursor.fetchone()[0]

                    # Set a tag for each row based on the blacklist condition
                    tag = 'red' if is_blacklisted else ''

                    cc_table.insert('', 'end', values=(mc_number, carrier_name, phone_number, homebase_zip, equip_length,
                                                       equip_type, insurance_amount, role, hazmat, us_citizen,
                                                       f"{average_rating:.2f}"), tags=(tag,))
                    cc_table.tag_configure('red', foreground='red')

                clear_label_text()

    elif selected_option == "Insurance ('amount')":
        search_query_value = ''.join(filter(str.isdigit, search_query))
        cursor.execute("SELECT * FROM carrier_info WHERE CAST(REPLACE(REPLACE(insurance_amount, ',', ''), '$', '') AS INTEGER) >= CAST(? AS INTEGER)", (search_query_value,))

        data = cursor.fetchall()

        # Clear existing entries in the table
        cc_table.delete(*cc_table.get_children())

        # Sort the data by Rating (average_rating)
        data.sort(key=lambda x: x[-1], reverse=True)

        # Repopulate the GUI table with the fetched data
        for row in data:
            (mc_number, carrier_name, phone_number, homebase_zip, equip_length, equip_type, insurance_amount, role,
             hazmat,
             us_citizen, average_rating) = row

            # Check if average_rating is None and provide a default value
            average_rating = average_rating if average_rating is not None else 0.0

            # Check if mc_number is in the blacklist
            cursor.execute("SELECT COUNT(*) FROM blacklist WHERE mc_number = ?", (mc_number,))
            is_blacklisted = cursor.fetchone()[0]

            # Set a tag for each row based on the blacklist condition
            tag = 'red' if is_blacklisted else ''

            cc_table.insert('', 'end', values=(mc_number, carrier_name, phone_number, homebase_zip, equip_length,
                                               equip_type, insurance_amount, role, hazmat, us_citizen,
                                               f"{average_rating:.2f}"), tags=(tag,))
            cc_table.tag_configure('red', foreground='red')

def on_enter(event):
    search_carrier()

search_entry.bind('<Return>', on_enter)
search_button.bind('<Return>', on_enter)


#Carrier Rating Table----------------------------------
rating_table_height = 10

Rating_Columns = ['Pro #', 'English', 'Communication', 'Reachability', 'Punctuality', 'MacroPoint', 'Blacklist', 'Total Rating']

rating_table = ttk.Treeview(CarrierCloud_tab, columns=Rating_Columns, show='headings', height=rating_table_height)

# Set column weights for rating_table
for col in Rating_Columns:
    rating_table.column(col, anchor=tk.CENTER)
    rating_table.heading(col, text=col)

# Grid layout for rating_table
rating_table.grid(column=0, row=2, sticky=(tk.N, tk.S, tk.W, tk.E))

# Configure column weights for rating_table
for col in Rating_Columns:
    CarrierCloud_tab.grid_columnconfigure(Rating_Columns.index(col), weight=1)

# Function to update the rating table based on the selected carrier
def update_rating_table(mc_number):
    # Clear existing entries in the rating table
    rating_table.delete(*rating_table.get_children())

    # Fetch rating data for the selected carrier
    cursor.execute('''
        SELECT pro_number, english, communication, reachability, punctuality, macropoint, blacklist, total_rating
        FROM carrier_rating
        WHERE mc_number = ?
    ''', (mc_number,))

    # Fetch the data and store it in the 'data' variable
    data = cursor.fetchall()

    for row in data:
        pro_number, english, communication, reachability, punctuality, macropoint, blacklist, total_rating = row

        # Set a tag for each row based on the blacklist condition
        tag = 'red' if blacklist else ''

        rating_table.insert('', 'end', values=(pro_number, english, communication, reachability, punctuality,
                                               macropoint, blacklist, f"{total_rating:.2f}"), tags=(tag,))
        rating_table.tag_configure('red', foreground='red')


cc_table.bind('<ButtonRelease-1>', lambda event: (update_rating_table(cc_table.item(cc_table.selection())['values'][0]), update_note_table(cc_table.item(cc_table.selection())['values'][0])))

#Carrier Note Window--------------------------------------
font=ctk.CTkFont("Calibri",12)
note_table = ctk.CTkTextbox(CarrierCloud_tab, wrap=tk.WORD, width=30, font=font)
note_table.grid(column=1, row=1, sticky=(tk.N, tk.S, tk.W, tk.E))
def update_note_table(mc_number):
    note_table.delete("1.0", tk.END)

    cursor.execute(''' SELECT note FROM carrier_notes WHERE mc_number = ?''', (mc_number,))

    data = cursor.fetchall()

    if data and data[0]:
        # Assuming the 'note' column is the second column in the result
        notes = data[0][0]  # Access the first column of the first row
        note_table.insert(tk.END, notes)

def save_notes(mc_number):
    # Get the text from the Text widget
    notes_text = note_table.get("1.0", tk.END)

    # Update or insert the notes into the database
    cursor.execute("INSERT OR REPLACE INTO carrier_notes (mc_number, note) VALUES (?, ?)", (mc_number, notes_text))
    conn.commit()

# Create a button that triggers the save_notes function
save_notes_button = ctk.CTkButton(CarrierCloud_tab, text="Save Notes", command=lambda: save_notes(cc_table.item(cc_table.selection())['values'][0]))
save_notes_button.grid(column=1, row=0, padx=5, pady=5)

# Bind the function to the <Configure> event of cc_table for proportional width
def update_rating_table_width(event):
    cc_table_width = cc_table.winfo_width()
    rating_table.column('#0', width=cc_table_width)
    for col in Rating_Columns:
        rating_table.column(col, width=cc_table_width // len(Rating_Columns))

cc_table.bind('<Configure>', update_rating_table_width)



# FINDER BOT TAB #######################################################################################################
finderbot_tab = ctk.CTkFrame(tab_control)
tab_control.add(finderbot_tab, text='Finder Bot')


# FINDER BOT--------------------------------
def FinderBot_Scraper3():
    # Read in list of URLs from CSV file
    urls_df = pd.read_csv("C:/Users/danie/OneDrive/Desktop/FinderBot/urls.csv")
    urls = urls_df["URL"].tolist()

    unscraped = deque(urls)

    scraped = set()

    emails = set()
    email_count = 0  # Counter for number of emails found

    while len(unscraped) and email_count < 250:  # Stop program when "x" emails have been found
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

keyword_label = ctk.CTkLabel(finderbot_tab, text="Keyword/Industry Type:")
keyword_entry = ctk.CTkEntry(finderbot_tab)
keyword_label.grid(column=0, row=0)
keyword_entry.grid(column=1, row=0)

zip_label = ctk.CTkLabel(finderbot_tab, text="Zip Code:")
zip_entry = ctk.CTkEntry(finderbot_tab)
zip_label.grid(column=0, row=1)
zip_entry.grid(column=1, row=1)

distance_label = ctk.CTkLabel(finderbot_tab, text="Distance (Miles):")
distance_entry = ttk.Combobox(finderbot_tab, values=["25", "50", "75", "100", "200"])
distance_label.grid(column=0, row=2)
distance_entry.grid(column=1, row=2)

Run_Button = ctk.CTkButton(finderbot_tab, text="Not Yet Available")#, command=FinderBot_Scraper3)
Run_Button.grid(column=0, row=3)

tab_control.pack(expand=1, fill='both')
root.mainloop()
