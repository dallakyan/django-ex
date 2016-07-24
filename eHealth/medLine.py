import urllib, urllib2
import xmltodict
import re



def med_query(search_terms):
    root_url = 'https://wsearch.nlm.nih.gov/ws/query'
    source = 'healthTopics'

    query = urllib.quote(search_terms)


    #Spaces may be replaced by '+' signs, which represent the AND operator.
    query = query.replace('%2B','+')
    #send a query as a phrase, enclose the phrase in quotes using %22 to represent quotation marks.
    query = query.replace('%27','%22')
    
    search_url = "{0}?db={1}&term={2}".format(
        root_url,
        source,
        query
    )
       
    results = []
       
    try:
        response = urllib2.urlopen(search_url).read()
        response = xmltodict.parse(response)
        
        for result in response['nlmSearchResult']['list']['document']:
            results.append({
                'title':re.sub('\<.*?\>','', result['content'][0]['#text']),
                'url':result['@url'],
                'summary':re.sub('\<.*?\>','', result['content'][-1]['#text']),
                'source':'MedLine'
                })
            

    except urllib2.URLError as e:
        print "Error when querying the MedLine API: ", e
        
    return results