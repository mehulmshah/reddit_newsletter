#! python3
# Uses JSON to obtain reddi posts
import requests

subreddits = input('Please enter subreddits separated by a space: ').split()
numPosts = int(input('How Many Posts(1-10): '))
titles, urls,top_comments,top_comments_author = [],[],[],[]
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
        comment_link = 'https://reddit.com' + j['data']['children'][i]['data']['permalink'] + '.json'
        r_c = requests.get(comment_link, headers={'User-agent': 'simple scraper by u/melonmeli23'})
        j_c = r_c.json()
        while j_c[1]['data']['children'][sticky_comment]['data']['stickied']:
            sticky_comment += 1
        top_comments.append(j_c[1]['data']['children'][sticky_comment]['data']['body'])
        top_comments_author.append(j_c[1]['data']['children'][sticky_comment]['data']['author'])
for i in range(numPosts*len(subreddits)):
    post = titles[i] + ":\n" + urls[i] + "\n" + top_comments_author[i] + " -- " + top_comments[i]
    print(post)
    print('\n')
