bulk_ttl_update
======================

An example script that that updates the TTL value for a list of hostnames. The input is through a CSV file containing the zone, owner, record type and new TTL (see example.csv). This script requires the [UltraDNS REST API Client](https://github.com/ultradns/python_rest_api_client) library.

```
$ python bulk_ttl_update.py help
Expected use: python bulk_ttl_update.py username password example.csv [url]
Argument 1:
        bulk_ttl_update.py -- The name of your python file
Argument 2:
        username -- Username of the UltraDNS account
Argument 3:
        password -- UltraDNS account password
Argument 4:
        example.csv -- The CSV file containing your update information (see example.csv)
Argument 5 (optional):
        url -- The url of your test environment (Example: https://test-restapi.ultradns.com)
```
