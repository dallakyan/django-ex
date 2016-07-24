import urllib2
import json
from eHealth.keys import HEALTH_API_KEY

def health_query(search_terms):
    root_url = 'http://healthfinder.gov/developer/Search.json'

    #sets the headers for the URL by accepting a request object
    query = urllib2.quote(search_terms)


    search_url = "{0}?api_key={1}&keyword={2}".format(
        root_url,
        HEALTH_API_KEY,
        query
    )

    results = []

    try:
        response = urllib2.urlopen(search_url).read()

        json_response = json.loads(response)


        for result in json_response["Result"]["Topics"]:
            results.append({
                'title':result["Title"],
                'url':result["AccessibleVersion"],
                'summary':result["Sections"][0]["Description"]
            })


    except urllib2.URLError as e:
        print "Error when querying the HealthFinder API: ", e

    return results
