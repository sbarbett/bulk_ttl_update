import csv, ultra_rest_client, json, sys, time

if len(sys.argv) == 2 and sys.argv[1].lower() == "help":
    sys.exit("Expected use: python bulk_ttl_update.py username password example.csv [use_http host:port]\nArgument 1:\n\tbulk_ttl_update.py -- The name of your python file\nArgument 2:\n\tusername -- Username of the UltraDNS account\nArgument 3:\n\tpassword -- UltraDNS account password\nArgument 4:\n\texample.csv -- The CSV file containing your update information (see example.csv).\nArguments 5 and 6 (optional):\n\tuse_http -- Specify this value as 'True' if you wish to use a test environment\n\thost:port -- The hostname and port of your test environment (Example: test-restapi.ultradns.com:443)\n")
    
if len(sys.argv) != 6 and len(sys.argv) != 4:
    raise Exception("Expected use: python bulk_ttl_update.py username password example.csv [use_http host:port]\n\nType 'python bulk_ttl_update.py help' for more information.\n")

username = sys.argv[1]
password = sys.argv[2]
# Check file extension
if sys.argv[3].endswith(".csv") is not True:
    raise Exception("File must be a CSV.")
input_file = csv.reader(open(sys.argv[3], "rb"))
use_http = 'False'
domain = 'restapi.ultradns.com'
# This is for pointing at a test environment
if len(sys.argv) == 6:
    use_http = sys.argv[4]
    domain = sys.argv[5]
  
# Establish an API connection
c = ultra_rest_client.RestApiClient(username, password, 'True' == use_http, domain)

# Add trailing dot
def check_trailing_dot(z):
    if z.endswith(".") is False:
        return z + "."
    else:
        return z
        
output_file = "results_" + str(int(time.time())) + ".csv"
with open(output_file, "w") as csv_output:
    # Set output CSV headers
    writer = csv.DictWriter(csv_output, fieldnames=['Zone', 'TTL update response'])
    writer.writeheader()
    # Skip fheader row of input file
    first_row = True
    for row in input_file:
        if first_row:
            first_row = False
            continue
        # Set variables
        if len(row) < 1:
            continue
        # Set variables
        zone = check_trailing_dot(row[0])
        hostname = check_trailing_dot(row[1])
        rtype = row[2]
        ttl = json.dumps({"ttl": row[3]})
        patch_msg = None
        
        # PATCH the rrset
        patch_response = c.rest_api_connection.patch("/v1/zones/" + zone + "/rrsets/" + rtype + "/" + hostname, ttl)
        print json.dumps(patch_response)
        if isinstance(patch_response, list) and 'errorMessage' in patch_response[0]:
            patch_msg = patch_response[0]['errorMessage']
        elif 'errorMessage' in patch_response:
            patch_msg = patch_response['errorMessage']
        else:
            patch_msg = patch_response['message']
            
        # Write results to CSV
        writer.writerow({'Zone': zone, 'TTL update response': patch_msg})
        
    # Close file
    print "Script complete. Saving results to %s" % output_file
    csv_output.close()