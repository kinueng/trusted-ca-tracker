from bs4 import BeautifulSoup
import urllib2

jsonLocalTrustStore = []
jsonRemoteTrustStore = []

# Parse out the table column labels and make them the keys for the json values
localTableHeader = []
remoteTableHeader = []

# Read the local trust store
localTrustStore = open("/System/Library/Security/Certificates.bundle/Contents/Resources/TrustStore.html", "r")
localSoup = BeautifulSoup(localTrustStore)
htmlTables = localSoup.findAll("table")


# Convert the tables into json for easier comparison
for tables in htmlTables:
    for row in tables("tr"):
        th = row.findAll("th")
        if(len(th) > 0):
            # We found the table header
            # The table headers will become the key for every row
            localTableHeader = [cell.text.strip() for cell in row("th")]
        else:
            # Parse the each certificate authority
            localTableData = [cell.text.strip() for cell in row("td")]
            jsonLocalTrustStore = dict(zip(localTableHeader, localTableData))

# Convert the tables into json for easier comparison
remoteTrustStore = urllib2.urlopen("https://support.apple.com/en-us/HT207189").read()
remoteSoup = BeautifulSoup(remoteTrustStore)
remoteHtmlTables = remoteSoup.findAll("table")
for tables in remoteHtmlTables:
    for row in tables("tr"):
        th = row.findAll("th")
        if(len(th) > 0):
            # We found the table header
            # The table headers will become the key for every row
            remoteTableHeader = [cell.text.strip() for cell in row("th")]
        else:
            # Parse the each certificate authority
            remoteTableData = [cell.text.strip() for cell in row("td")]
            jsonRemoteTrustStore = dict(zip(remoteTableHeader, remoteTableData))

# Start comparing local and remote certificate authorities
if(len(jsonRemoteTrustStore) != len(jsonLocalTrustStore)):
    print "Not equal size!"
    # TODO: Log and alert user

if(jsonRemoteTrustStore != jsonLocalTrustStore):
    print "Not the same list of CAs!"
    # TODO: Log and alert user