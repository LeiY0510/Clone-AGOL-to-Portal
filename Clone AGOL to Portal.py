from arcgis.gis import GIS

# Specify the URL and credential of the origin ArcGIS Online account. 
username_1 = input("Enter username for source organization: ")
password_1 = input("Enter password for source organization: ")

# For ArcGIS Online
gis1 = GIS(url="https://austindss.maps.arcgis.com", username=username_1, password=password_1)

# Specify the OAuth token for the target ArcGIS Portal account
oauth_token = input("Enter the OAuth token: ")  # Insert the OAuth token ID

# For Portal for ArcGIS using OAuth
gis2 = GIS(r"https://portviews.porthouston.com/portal", token=oauth_token)

# Get a specific item using item id
itemid = input("Enter the Item ID to copy: ")  # Insert the item id
items = gis1.content.search(itemid)

print(str(len(items)) + " items will be cloned. See the list below: ")
for item in items:
    print(f"- {item.title} (ID: {item.id})")

# Specify the target folder in the portal
folder_name = input("Enter the name of the target folder in the portal (leave blank for root): ")

# Get the target folder object if it exists
target_folder = None
if folder_name:
    for folder in gis2.content.get_folders():
        if folder.title == folder_name:
            target_folder = folder
            break

if target_folder:
    print(f"Cloning will be done in the folder: {target_folder.title}")
else:
    print("Target folder not found. Cloning will be done in the root content.")

def deep_copy_content(input_list):
    for item in input_list:
        try:
            print("Cloning " + item.title)
            copy_list = [item]
            
            # Clone items to the specified folder, if it exists
            if target_folder:
                gis2.content.clone_items(copy_list, copy_data=True, search_existing_items=True, folder=target_folder.id)
            else:
                gis2.content.clone_items(copy_list, copy_data=True, search_existing_items=True)

            print("Successfully cloned " + item.title)
        except Exception as e:
            print(f"Error cloning {item.title}: {e}")
    print("The function has completed")

deep_copy_content(items)
