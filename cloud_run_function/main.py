import functions_framework
import requests
import json
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

@functions_framework.http
def hello_http(request):

    request_args = request.args
    print("Got request: " + str(request))

    if request_args and 'feed' in request_args:
        feed = request_args['feed']
        print("Got feed: " + feed)
        if feed == 'secops':
            return generate_rss('google-security-operations-2'), 200, {'Content-Type': 'application/xml; charset=utf-8'}
        elif feed == 'gti':
            return generate_rss('google-threat-intelligence-3'), 200, {'Content-Type': 'application/xml; charset=utf-8'}
        elif feed == 'scc':
            return generate_rss('security-command-center-4'), 200, {'Content-Type': 'application/xml; charset=utf-8'}
        elif feed == 'validation':
            return generate_rss('security-validation-5'), 200, {'Content-Type': 'application/xml; charset=utf-8'}
        elif feed == 'recaptcha':
            return generate_rss('recaptcha-6'), 200, {'Content-Type': 'application/xml; charset=utf-8'}
        elif feed == 'foundation':
            return generate_rss('cloud-security-foundation-7'), 200, {'Content-Type': 'application/xml; charset=utf-8'}
        else:
            return generate_rss('google-security-operations-2'), 200, {'Content-Type': 'application/xml; charset=utf-8'}
    else:
        print("No feed provided. Defaulting to secops")
        return generate_rss('google-security-operations-2'), 200, {'Content-Type': 'application/xml; charset=utf-8'}

def generate_rss(forum):
    FORUM_URL = 'https://security.googlecloudcommunity.com/' + forum
    resp = requests.get(FORUM_URL)
    soup = BeautifulSoup(resp.text, 'html.parser')

    all_topics = soup.find_all('div', attrs={'data-preact': 'destination/modules/Content/TopicList/TopicListItem'})

    # Initialize the FeedGenerator
    fg = FeedGenerator()

    main_title_tag = soup.find('h1')
    main_title_text = main_title_tag.get_text()
    main_description = main_title_tag = soup.find('p')
    fg.title(main_title_text)
    fg.link(href=FORUM_URL, rel='alternate')
    fg.description(main_description.get_text())


    # 3. Loop through each topic and extract the details
    for topic in all_topics:

        json_string = topic['data-props']

        data = json.loads(json_string)

        # Create a feed entry
        fe = fg.add_entry()
        fe.title(data['topic']['title'])
        fe.link(href=data['topic']['topicUrl']['destination'])
        fe.pubDate(data['topic']['publishedAt'])
        fe.guid(data['topic']['topicUrl']['destination'], permalink=True)
        fe.description(data['topic']['content'])

    # Generate the RSS feed as a string
    rss_feed = fg.rss_str(pretty=True)

    return(rss_feed.decode('utf-8'))
