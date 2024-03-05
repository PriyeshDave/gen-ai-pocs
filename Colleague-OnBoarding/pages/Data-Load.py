import streamlit as st
import os
import json
from datetime import datetime
import pandas as pd

data_bank_folder = "data-bank"

class SessionState:
    def __init__(self):
        self.submitted = False

st.set_page_config(page_title="Colleague On-Boarding Application", page_icon="assets/images/favicon.png", layout="wide", initial_sidebar_state='collapsed')        

col_main_1, col_main_2, col_main_3 = st.columns([1,5,1])

with col_main_2:
    st.markdown("# **Data Setup for Colleague On-Boarding Application**")
    st.markdown(
        """
        Upload Colleague and Organisational data in the given tabs.  
        """
    )


def main():
    # Create tabs
    tabs = ["Employee Data Form", "Data Bank File Upload"]
    #selected_tab = st.sidebar.radio("Select Tab", tabs)
    emp_col, data_col = st.tabs(tabs)
    print (emp_col,data_col)

    with emp_col:
        st.header("Colleague Data Load Form")
        show_employee_data_form()
    with data_col:
        st.header("Organisational Data Load Form")
        show_data_bank_file_upload()


    # if selected_tab == "Employee Data Form":
    #     show_employee_data_form()
    # elif selected_tab == "Data Bank File Upload":
    #     show_data_bank_file_upload()

def show_employee_data_form():
    st.title("Enter the Colleague Details")

    # Create a form to encapsulate the input fields
    with st.form("user_input_form", clear_on_submit=True):
        user_name = st.text_input("Colleague Name:")
        user_phone = st.text_input("Colleague Phone:")
        user_email = st.text_input("Colleague Email:")
        user_address = st.text_input("Colleague Address:")
        user_photo = st.file_uploader("Upload Colleague Photo (jpg or png):", type=["jpg", "png", "jpeg"])
        user_lkdn_url = st.text_input("LinkedIn URL:")
        user_git_url = st.text_input("GitHub URL:")

        submit_button = st.form_submit_button("Submit")

        # Get the session state
        state = get_session_state()

        # Check if the form is submitted
        if submit_button:
            # Capture data to dictionary
            user_data = {
                "SubmissionID": get_timestamp(),
                "Name": user_name,
                "Phone": user_phone,
                "Email": user_email,
                "Address": user_address,
                "User Photo": save_uploaded_file(user_photo, user_name),
                "Entered Lkdn URL": user_lkdn_url,
                "Entered Git URL": user_git_url,
            }

            # Save data to JSON file
            save_to_json(user_data)

            # Change the session state to mark the form as submitted
            state.submitted = True

        # Display informational message at the end
        if state.submitted:
            st.info("Thank you for submitting the form!")

def show_data_bank_file_upload(data_bank_folder="data-bank"):
    st.title("Data Bank File Upload")

    # Create a folder for data bank if it doesn't exist
    os.makedirs(data_bank_folder, exist_ok=True)

    # File upload functionality
    uploaded_file = st.file_uploader("Upload File:", type=["txt", "rtf", "pdf", "doc", "docx", "csv", "xlsx", "ppt"])

    if uploaded_file:
        # Save the uploaded file to the data bank folder
        filename = os.path.join(data_bank_folder, uploaded_file.name)
        with open(filename, "wb") as f:
            f.write(uploaded_file.getvalue())
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")

    # Display the list of files and folders in the data bank folder
    st.subheader("Data Bank Files:")
    data_bank_contents = os.listdir(data_bank_folder)

    if len(data_bank_contents) != 0:
        # Create a DataFrame to organize file information
        files_data = []
        for file_name in data_bank_contents:
            file_path = os.path.join(data_bank_folder, file_name)
            file_size = os.path.getsize(file_path)
            file_kind = file_name.split('.')[-1].upper()
            date_added = datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
            files_data.append({"File Name": file_name, "Size": file_size, "Kind": file_kind, "Date Added": date_added})

        files_df = pd.DataFrame(files_data)
        st.table(files_df)

    else:
        st.write("No files to display!")

def get_timestamp():
    return datetime.now().strftime("%Y%m%d%H%M%S")

def save_uploaded_file(file, user_name,default_img='./img/user_img.png'):
    if file:
        upload_folder = "img"
        os.makedirs(upload_folder, exist_ok=True)
        filename = f"{user_name}_{get_timestamp()}_{file.name}"
        filepath = os.path.abspath(os.path.join(upload_folder, filename))
        with open(filepath, "wb") as f:
            f.write(file.getvalue())
        return filepath
    else :
        filepath=default_img
    return filepath 

def save_to_json(data):
    user_data_dir = "./user-data"
    os.makedirs(user_data_dir, exist_ok=True)  # Create the directory if it doesn't exist

    file_path = os.path.join(user_data_dir, f"user_data_{get_timestamp()}.json")

    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=2)    

def get_session_state():
    session_state = st.session_state
    if not hasattr(session_state, "state"):
        session_state.state = SessionState()
    return session_state.state

if __name__ == "__main__":
    main()
