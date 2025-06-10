import streamlit as st
import json
import os

FILENAME = 'contacts.json'

# Load contacts from file
if os.path.exists(FILENAME):
    with open(FILENAME, 'r') as f:
        phone = json.load(f)
else:
    phone = []

# Save contacts to file
def save_contacts():
    with open(FILENAME, 'w') as f:
        json.dump(phone, f, indent=4)

# UI
st.title("Smart Contact Book")

menu = ["Add Contact", "Search Contact", "View Contacts", "Update Contact", "Delete Contact"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Contact":
    st.subheader("Add a New Contact")
    name = st.text_input("Name")
    phone_number = st.text_input("Phone Number")
    notes = st.text_area("Notes")
    if st.button("Add"):
        if name and phone_number:
            phone.append({"Name": name, "Phone Number": phone_number, "Notes": notes})
            save_contacts()
            st.success("Contact added successfully!")
        else:
            st.warning("Name and Phone Number are required.")

elif choice == "Search Contact":
    st.subheader("Search Contact")
    search_by = st.radio("Search by", ["Name", "Phone Number"])
    query = st.text_input("Enter search query")
    if st.button("Search"):
        found = False
        for idx, contact in enumerate(phone, start=1):
            if (search_by == "Name" and contact["Name"].lower() == query.lower()) or \
               (search_by == "Phone Number" and contact["Phone Number"] == query):
                st.info(f"{idx}. Name: {contact['Name']} | Phone: {contact['Phone Number']} | Notes: {contact['Notes']}")
                found = True
        if not found:
            st.warning("No contact found.")

elif choice == "View Contacts":
    st.subheader("All Contacts")
    if not phone:
        st.warning("No contacts saved yet.")
    else:
        for idx, contact in enumerate(phone, start=1):
            st.text(f"{idx}. Name: {contact['Name']} | Phone: {contact['Phone Number']} | Notes: {contact['Notes']}")

elif choice == "Update Contact":
    st.subheader("Update Contact")
    name_input = st.text_input("Enter the name of the contact to update")
    if st.button("Find Contact"):
        contact_found = next((c for c in phone if c['Name'].lower() == name_input.lower()), None)
        if contact_found:
            new_name = st.text_input("New Name", value=contact_found['Name'])
            new_phone = st.text_input("New Phone Number", value=contact_found['Phone Number'])
            new_notes = st.text_area("New Notes", value=contact_found['Notes'])
            if st.button("Update"):
                contact_found['Name'] = new_name
                contact_found['Phone Number'] = new_phone
                contact_found['Notes'] = new_notes
                save_contacts()
                st.success("Contact updated successfully!")
        else:
            st.warning("Contact not found.")

elif choice == "Delete Contact":
    st.subheader("Delete Contact")
    name_to_delete = st.text_input("Enter the name of the contact to delete")
    if st.button("Delete"):
        for contact in phone:
            if contact['Name'].lower() == name_to_delete.lower():
                phone.remove(contact)
                save_contacts()
                st.success("Contact deleted successfully!")
                break
        else:
            st.warning("Contact not found.")
