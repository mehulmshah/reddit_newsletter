#! python3
# Uses JSON to obtain reddi posts
import requests
import requests.auth
# Obtain OAuth2 for scraping all subreddits and preferences from personal username (melonmeli23)
client_auth = requests.auth.HTTPBasicAuth('eSf70mLdSY8ZnQ', 'Uvucu7ut5wuOMBe6suu2kiCIjSo')
post_data = {"grant_type": "password", "username": "melonmeli23", "password": "chicago1"}
GetTokenHeaders = {"User-Agent": "RedditNewsletter/0.1 by melonmeli23"}
response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=GetTokenHeaders)
auth_data = response.json()
access_token = auth_data['access_token']
UseTokenHeaders = {"Authorization": "bearer "+access_token, "User-Agent": "RedditNewsletter/0.1 by melonmeli23"}
response = requests.get("https://oauth.reddit.com/api/v1/me", headers=UseTokenHeaders)

# Begin actual parsing of reddit JSON data
subreddits = input('Please enter subreddits separated by a space: ').split()
numPosts = int(input('How Many Posts(1-10): '))
titles, urls,top_comments,top_comments_author,selftext = [],[],[],[],[]
headers={'User-agent': 'simple scraper by u/melonmeli23'}
# go to each subreddit requested
for sub in subreddits:
    link = 'https://reddit.com/r/%s.json' % sub
    r = requests.get(link, headers={'User-agent': 'simple scraper by u/melonmeli23'})
    try:
        r.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % (exc))
    j = r.json()
    afterSticky = 0
    # go through each post except stickied ones
    while j['data']['children'][afterSticky]['data']['stickied']:
        afterSticky += 1
    for i in range(afterSticky,numPosts+afterSticky):
        sticky_comment = 0
        titles.append(j['data']['children'][i]['data']['title'])
        urls.append(j['data']['children'][i]['data']['url'])
        has_no_comments = j['data']['children'][i]['data']['num_comments'] == 0
        is_self_post = j['data']['children'][i]['data']['selftext'] != ''
        if has_no_comments:
            top_comments.append('no comments')
            top_comments_author.append('no comments')
            continue
        if is_self_post:
            selftext.append(j['data']['children'][i]['data']['selftext'])
        else:
            selftext.append('none')
        comment_link = 'https://reddit.com' + j['data']['children'][i]['data']['permalink'] + '.json'
        r_c = requests.get(comment_link, headers={'User-agent': 'simple scraper by u/melonmeli23'})
        j_c = r_c.json()
        #while j_c[1]['data']['children'][sticky_comment]['data']['stickied']:
        #    sticky_comment += 1
        top_comments.append(j_c[1]['data']['children'][0]['data']['body'])
        top_comments_author.append(j_c[1]['data']['children'][0]['data']['author'])
for i in range(numPosts*len(subreddits)):
    post = titles[i] + ":\n" + urls[i] + "\n" + top_comments_author[i] + " -- " + top_comments[i]
    print(post)
    print('\n')
