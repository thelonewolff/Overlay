import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from simple_salesforce import Salesforce

# Read the Excel file
df = pd.read_excel('input_file.xlsx')

# Salesforce authentication
sf = Salesforce(username='your_username', password='your_password', security_token='your_security_token')

# Function to overlay images
def overlay_images(background_path, overlay_url):
    # Open the background image
    background = Image.open(background_path).convert("RGBA")

    # Get the overlay image from the URL
    response = requests.get(overlay_url)
    overlay = Image.open(BytesIO(response.content)).convert("RGBA")

    # Resize overlay image to match the background (optional, if needed)
    overlay = overlay.resize(background.size, Image.ANTIALIAS)

    # Overlay the images
    combined = Image.alpha_composite(background, overlay)
    
    return combined

# Function to upload image to Salesforce
def upload_image_to_salesforce(image, record_id):
    # Save the combined image to a byte stream
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    # Create the document in Salesforce
    response = sf.Document.create({
        'Name': f'Overlayed_Image_{record_id}.png',
        'FolderId': 'your_folder_id',  # Replace with your actual Folder ID
        'Body': img_byte_arr.encode('base64'),  # Encoding the image to base64
        'ContentType': 'image/png',
        'Type': 'png'
    })
    
    return response

# Path to the background image
background_path = 'background.png'

# Iterate through the DataFrame
for index, row in df.iterrows():
    record_id = row['recordID']
    overlay_url = row['URL']

    # Overlay the images
    combined_image = overlay_images(background_path, overlay_url)
    
    # Upload to Salesforce
    response = upload_image_to_salesforce(combined_image, record_id)
    print(f'Uploaded image for record ID {record_id}: {response}')

print("Processing complete.")
