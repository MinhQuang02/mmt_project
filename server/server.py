import socket
import os
import threading
import csv
import datetime
import random

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
UPLOAD_FOLDER = "mmt_project-main/server/uploads"
PATH = "PATH"

# All file path
file_path_all_files = PATH + 'mmt_project-main/server/data_users/all_file.csv'
file_path_recycle_bin = PATH + 'mmt_project-main/server/data_users/recycle_bin.csv'
file_path_starred_files = PATH + 'mmt_project-main/server/data_users/starred_file.csv'
file_path_users_login = PATH + 'mmt_project-main/server/data_users/users_login.csv'

# Create folder to store uploaded files if not existed
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Change all file and user login csv files to string
def csv_to_string(file_path):
    result = ""
    with open(file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            account, password = row
            result += f"{account}:{password}|"
    return result

# Change recycle bin and starred files csv files to string
def extract_user_info(file_path, user_name):
    result = ""
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[0] == user_name:
                for i in range(1, len(row), 2):
                    if i+1 < len(row):
                        result += f"{row[i]}:{row[i+1]}|"
                break
    return result

# Add new row to csv file by id and info
def add_new_row(file_path, new_id, new_info):
    rows = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        rows.append(headers)

        for row in csv_reader:
            rows.append(row)
    
    # Create new row with id and info
    new_row = [new_id, new_info]
    rows.append(new_row)
    
    # Change csv file with new info
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(rows)

# Add new row to csv file by username
def add_new_user(file_path, new_user):
    rows = []
    
    # Read all rows in file
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            rows.append(row)
    
    # Create new row with username
    new_row = [new_user]
    rows.append(new_row)
    
    # Write new row to file
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(rows)

# Restore file from recycle bin
def del_one_id_in_one_row(file_path, user_name, id_to_del):
    rows = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        rows.append(headers)

        for row in csv_reader:
            if row[0] == user_name:
                # Find and remove the required format pair for all rows
                for i in range(1, len(row), 2):
                    if row[i] == id_to_del:
                        row[i] = ''
                        row[i+1] = ''
                # Remove empty columns
                row = [item for item in row if item]
            rows.append(row)
    
    # Write new row to file
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(rows)

# Remove id from starred file
def remove_id_from_starred(file_path, id_to_remove):
    rows = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        rows.append(headers)

        for row in csv_reader:
            # Find and remove the required format pair for all rows
            for i in range(1, len(row), 2):
                if row[i] == id_to_remove:
                    row[i] = ''
                    row[i+1] = ''
            # Remove empty columns  
            row = [item for item in row if item]
            rows.append(row)
    
    # Write new row to file
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(rows)
        
# Find and remove row by id    
def remove_row_by_id(file_path, id_to_remove):
    rows = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        rows.append(headers)

        for row in csv_reader:
            # Only add row if id is not equal to id_to_remove
            if row[0] != id_to_remove:
                rows.append(row)
    
    # Change csv file with new info
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(rows)
        
# Add new info to 1 row in csv file
def add_info_to_user(file_path, target_user, new_id, new_account_info):
    rows = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        rows.append(headers)

        for row in csv_reader:
            if row[0] == target_user:
                row.extend([new_id, new_account_info])
            rows.append(row)
    
    # Change csv file with new info
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(rows)
        
# Change password of user
def change_password(file_path, user_name, new_password):
    rows = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        rows.append(headers)

        for row in csv_reader:
            if row[0] == user_name:
                row[1] = new_password
            rows.append(row)
    
    # Change csv file with new info
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(rows)
        
# Check if id is existed in csv file
def check_id_existed(file_path, id_to_check):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[0] == id_to_check:
                return True
    return False

# File extension
def file_extension(file_info):
    parts = file_info.split(' - ')
    filename = parts[2]
    extension = filename.split('.')[-1]
    return extension

# Handle client function
def handle_client(client_socket, received, new_id):
    try:
        # Get file name and file size
        received, user_name = received.split("|")
        filename, filesize = received.split(SEPARATOR)
        filename = os.path.basename(filename)
        filesize = int(filesize)

        # Create new file
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        print(f"Receiving file {filepath} with size {filesize} bytes")
        
        # Receive file from client
        with open(filepath, "wb") as f:
            while True:
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:    
                    break
                f.write(bytes_read)
        print(f"File {filename} received successfully")
        
        # Add new row to all files csv file
        filename = user_name + " - " + filename + " - " + datetime.datetime.now().strftime("%d/%m/%Y")
        add_new_row(file_path_all_files, str(new_id), filename)
        
        # Get name of new file
        new_filename = str(new_id)
        name, extension = os.path.splitext(filepath)
        new_filename += extension
        
        # Rename file
        new_filepath = os.path.join(UPLOAD_FOLDER, new_filename)
        os.rename(filepath, new_filepath)
    finally:
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
    
    while True:
        client_socket, address = server_socket.accept()
        print(f"[+] {address} is connected.")

        signal = client_socket.recv(BUFFER_SIZE).decode()
        print(f"Received signal: {signal}")
        
        data = "None"
        if signal == "user": # Get all user login
            data = csv_to_string(file_path_users_login)
        elif signal == "asf": # Get all server files
            data = csv_to_string(file_path_all_files)
        elif signal[-3:] == "|ds": # Get all starred files by user
            name_user = signal[:-3]
            data = extract_user_info(file_path_starred_files, name_user)
            if data == "":
                data = "None"
        elif signal[-3:] == "|rb": # Get all recycle bin by user
            name_user = signal[:-3]
            data = extract_user_info(file_path_recycle_bin, name_user)
            if data == "":
                data = "None"
        elif signal[-3:] == "|uu": # Add new user
            # Get new user and password
            user_and_pass = signal[:-3]
            new_user = user_and_pass.split("|")[0]
            new_pass = user_and_pass.split("|")[1]
            
            # Add new user to all files
            add_new_row(file_path_users_login, new_user, new_pass)
            add_new_user(file_path_starred_files, new_user)
            add_new_user(file_path_recycle_bin, new_user)
        elif signal[-3:] == "|rm": # Remove file
            # Get user and id to remove
            user_and_id = signal[:-3]
            user_info = user_and_id.split("|")[1]
            id_to_remove = user_and_id.split("|")[0]
            name_user = user_info.split("-")[0]
            name_user = name_user[:-1]
            
            # Remove file from all files and starred files
            remove_id_from_starred(file_path_starred_files, id_to_remove)
            remove_row_by_id(file_path_all_files, id_to_remove)
            add_info_to_user(file_path_recycle_bin, name_user, id_to_remove, user_info)
        elif signal[-3:] == "|rs": # Restore file
            # Get user and id to restore
            user_and_id = signal[:-3]
            user_info = user_and_id.split("|")[1]
            id_to_restore = user_and_id.split("|")[0]
            name_user = user_info.split("-")[0]
            name_user = name_user[:-1]
            
            # Restore file from recycle bin
            del_one_id_in_one_row(file_path_recycle_bin, name_user, id_to_restore)
            add_new_row(file_path_all_files, id_to_restore, user_info)
        elif signal[-3:] == "|df": # Delete file
            # Get user and id to delete
            user_and_id = signal[:-3]
            user_info = user_and_id.split("|")[1]
            id_to_delete = user_and_id.split("|")[0]
            name_user = user_info.split("-")[0]
            name_user = name_user[:-1]
            
            # Delete file from recycle bin
            del_one_id_in_one_row(file_path_recycle_bin, name_user, id_to_delete)
            
            # Delete file from server by id
            id_to_delete = id_to_delete + "." + file_extension(id_to_delete + " - " + user_info)
            os.remove(PATH + "mmt_project-main/server/uploads/" + id_to_delete)
        elif signal[-3:] == "|sf": # Starred file
            # Get user and id to starred
            user_and_info = signal[:-3]
            info = user_and_info.split("|")[1]
            user = user_and_info.split("|")[0]
            id_user = info.split("-")[0]
            id_user = id_user[:-1]
            another_info = info[7:]
            
            # Add file to starred files
            add_info_to_user(file_path_starred_files, user, id_user, another_info)
        elif signal[-3:] == "|uf": # Unstarred file
            # Get user and id to unstarred
            user_and_info = signal[:-3]
            info = user_and_info.split("|")[1]
            user = user_and_info.split("|")[0]
            id_user = info.split("-")[0]
            id_user = id_user[:-1]
            
            # Remove file from starred files
            del_one_id_in_one_row(file_path_starred_files, user, id_user)
        elif signal[-3:] == "|cp": # Change password
            # Get user and new password
            user_and_pass = signal[:-3]
            user = user_and_pass.split("|")[0]
            password = user_and_pass.split("|")[1]
            
            # Change password of user
            change_password(file_path_users_login, user, password)
        elif signal[-3:] == "|dl": # Download
            signal = signal[:-3]
            filepath = os.path.join(UPLOAD_FOLDER, signal)
            
            # Send file to client
            with open(filepath, 'rb') as file:
                while True:
                    bytes_read = file.read(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    try:
                        client_socket.sendall(bytes_read)
                    except ConnectionResetError:
                        print("Connection reset by peer")
                        return
                    
            client_socket.close()
            continue
        else: # Upload
            # Generate new id for new file
            new_id = random.randint(1000, 9999)
            while check_id_existed(file_path_all_files, str(new_id)):
                new_id = random.randint(1000, 9999)
                
            # Handle client
            client_handler = threading.Thread(target=handle_client, args=(client_socket, signal, new_id))
            client_handler.start()
            data = str(new_id)
            
        # Send data to client
        client_socket.sendall(data.encode())

if __name__ == "__main__":
    start_server()
