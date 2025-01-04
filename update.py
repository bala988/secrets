import http.client
import json
import ssl
import os
import dicttoxml  # Install this package to convert JSON to XML

# Configuration
firewall_ip = "192.168.1.50"
api_key = "LUFRPT1MbUtJL2hSWFg4ZCtBMTAvUHFYUkorSGwvREU9MkEzM3lDRzVYWkFmSW5Jd0JIdzFuYlA3bjVZVDExZWxVM0VaOGdqWWVLcDBYcWNqQUpqcXJ0L1lmNHhRVEZMNQ=="
json_file_path = r'C:\Users\DELL\Desktop\output\firewall_security_rules.json'  # Path to JSON file
xml_file_path = r'C:\Users\DELL\Desktop\output\firewall_security_rules.xml'    # Path to XML file

# Ensure the JSON file exists
if not os.path.exists(json_file_path):
    print(f"File not found: {json_file_path}")
    exit(1)

# Read the modified JSON data from the file
with open(json_file_path, 'r') as file:
    json_data = json.load(file)

# Convert JSON to XML using dicttoxml
xml_data = dicttoxml.dicttoxml(json_data, custom_root='root', ids=False)

# Ensure the output directory for XML file exists
os.makedirs(os.path.dirname(xml_file_path), exist_ok=True)

# Write the XML data to a file (optional step, you can remove this if you don't need it)
with open(xml_file_path, 'wb') as xml_file:
    xml_file.write(xml_data)

# Create an unverified SSL context
context = ssl._create_unverified_context()

# Send the PUT request to the firewall
conn = http.client.HTTPSConnection(firewall_ip, context=context)
headers = {
    'Content-Type': 'application/xml',  # Changed to XML content type
    'Accept': 'application/xml',
    'X-PAN-Key': api_key
}

try:
    # Sending the PUT request with XML data
    conn.request("PUT", "/restapi/v11.1/Policies/SecurityRules", xml_data, headers)
    res = conn.getresponse()

    # Read the response
    response_data = res.read().decode('utf-8')
    if res.status == 200:
        print("Successfully uploaded the modified security rules to the firewall.")
        print("Response:", response_data)
    else:
        print(f"Failed to upload the security rules. Status: {res.status}")
        print("Response:", response_data)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    conn.close()
