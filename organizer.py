import os
import shutil   # For moving files
import hashlib  # For generating unique file hash


# 📂 Main folder path (change according to your system)
folder_path = "C:/Users/Ankit/Downloads"


# 📁 Categories (folders to create)
folders = ["Images", "Documents", "Videos", "Music", "Apps", "Others"]

# Create folders if not exist
for folder in folders:
    path = os.path.join(folder_path, folder)
    if not os.path.exists(path):
        os.makedirs(path)


# 📄 File type classification
images = [".jpg", ".png", ".jpeg"]
documents = [".pdf", ".docx", ".txt"]
music = [".mp3", ".wav"]
videos = [".mp4", ".mkv"]


# 🔑 Function: Generate hash (unique identity of file)
def get_file_hash(file_path):
    hasher = hashlib.md5()

    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            hasher.update(chunk)

    return hasher.hexdigest()


# 🧠 Sets to track duplicates
seen_names = set()   # (folder, filename)
seen_hashes = set()  # file content


# 📌 Load existing files (already sorted folders)
for folder in folders:
    folder_path_full = os.path.join(folder_path, folder)

    for f in os.listdir(folder_path_full):
        full_path = os.path.join(folder_path_full, f)

        if os.path.isfile(full_path):
            file_hash = get_file_hash(full_path)

            # Store existing file info
            seen_hashes.add(file_hash)
            seen_names.add((folder, f))


# 📂 Get all files from main folder
files = os.listdir(folder_path)


# 🔄 Main loop: process each file
for file in files:
    file_path = os.path.join(folder_path, file)

    # Skip if it's a folder
    if not os.path.isfile(file_path):
        continue     # skip folders is folder


    # 🔍 Generate hash for duplicate detection
    file_hash = get_file_hash(file_path)

    # ❌ Case 1: Same content already exists → skip
    if file_hash in seen_hashes:
        print(f"Duplicate content found: {file}, skipping...")
        continue


    # 📌 Decide destination folder
    if file.lower().endswith(tuple(images)):
        destination_folder = "Images"

    elif file.lower().endswith(tuple(documents)):
        destination_folder = "Documents"

    elif file.lower().endswith(tuple(music)):
        destination_folder = "Music"

    elif file.lower().endswith(tuple(videos)):
        destination_folder = "Videos"

    elif file.lower().endswith(".exe"):
        destination_folder = "Apps"

    else:
        destination_folder = "Others"


    # 📍 Destination path
    destination = os.path.join(folder_path, destination_folder, file)


    # 🔁 Case 2: Same name but different content → rename
    if (destination_folder, file) in seen_names:
        base, ext = os.path.splitext(file)
        count = 1

        new_name = f"{base}_{count}{ext}"
        new_destination = os.path.join(folder_path, destination_folder, new_name)

        # Keep increasing count until unique name found
        while os.path.exists(new_destination):
            count += 1
            new_name = f"{base}_{count}{ext}"
            new_destination = os.path.join(folder_path, destination_folder, new_name)

        destination = new_destination
        print(f"Renamed: {file} → {new_name}")

    else:
        # Store new file info
        seen_names.add((destination_folder, file))
        seen_hashes.add(file_hash)


    # 🚚 Move file
    if not os.path.exists(destination):
        shutil.move(file_path, destination)
        print(f"Moved: {file} → {destination_folder}")
    else:
        print(f"{file} already exists, skipping...")