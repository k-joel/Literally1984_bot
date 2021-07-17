import praw
import prawcore
import time
import logging
import random

ACTIVE_SUBREDDITS = [
    'testingground4bots',
    'PoliticalCompassMemes',
    'reclassified',
]

IGNORED_USERS = [
    'basedcount_bot'
]

SEARCH_TEXT = "literally 1984"

ANSWER_TEXT_OLD = """
    ⠀⠀⠀⠀⠀⠀⠀⣠⡀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠤⠤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀ 
    ⠀⠀⠀⠀⠀⢀⣾⣟⠳⢦⡀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠉⠉⠉⠉⠉⠒⣲⡄ 
    ⠀⠀⠀⠀⠀⣿⣿⣿⡇⡇⡱⠲⢤⣀⠀⠀⠀⢸.⠀1984⠀⣠⠴⠊⢹⠁ 
    ⠀⠀⠀⠀⠀⠘⢻⠓⠀⠉⣥⣀⣠⠞⠀⠀⠀⢸.  ⠀⢀⡴⠋⠀⠀⠀⢸⠀ 
    ⠀⠀⠀⠀⢀⣀⡾⣄⠀⠀⢳⠀⠀⠀⠀⠀⠀⢸⢠⡄⢀⡴⠁2021⠀⡞⠀ 
    ⠀⠀⠀⣠⢎⡉⢦⡀⠀⠀⡸⠀⠀⠀⠀⠀⢀⡼⣣⠧⡼⠀⠀⠀⠀⠀⠀⢠⠇⠀ 
    ⠀⢀⡔⠁⠀⠙⠢⢭⣢⡚⢣⠀⠀⠀⠀⠀⢀⣇⠁⢸⠁⠀⠀⠀⠀⠀⠀⢸⠀⠀ 
    ⠀⡞⠀⠀⠀⠀⠀⠀⠈⢫⡉⠀⠀⠀⠀⢠⢮⠈⡦⠋⠀⠀⠀⠀⠀⠀⠀⣸⠀⠀ 
    ⢀⠇⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡀⣀⡴⠃⠀⡷⡇⢀⡴⠋⠉⠉⠙⠓⠒⠃
    ⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⡼⠀⣷⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⡞⠀⠀⠀⠀⠀⠀⠀⣄⠀⠀⠀⠀⠀⠀⡰⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⢧⠀⠀⠀⠀⠀⠀⠀⠈⠣⣀⠀⠀⡰⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

ANSWER_TEXT = """
    ⠀⠀⠀⠀⠀⠀⠀⣠⡀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠤⠤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀ 
    ⠀⠀⠀⠀⠀⢀⣾⣟⠳⢦⡀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠉⠉⠉⠉⠉⠒⣲⡄ 
    ⠀⠀⠀⠀⠀⣿⣿⣿⡇⡇⡱⠲⢤⣀⠀⠀⠀⢸⠀⠀⠀1984⠀⣠⠴⠊⢹⠁ 
    ⠀⠀⠀⠀⠀⠘⢻⠓⠀⠉⣥⣀⣠⠞⠀⠀⠀⢸⠀⠀⠀⠀⢀⡴⠋⠀⠀⠀⢸⠀ 
    ⠀⠀⠀⠀⢀⣀⡾⣄⠀⠀⢳⠀⠀⠀⠀⠀⠀⢸⢠⡄⢀⡴⠁ 2021⠀⡞⠀ 
    ⠀⠀⠀⣠⢎⡉⢦⡀⠀⠀⡸⠀⠀⠀⠀⠀⢀⡼⣣⠧⡼⠀⠀⠀⠀⠀⠀⢠⠇⠀ 
    ⠀⢀⡔⠁⠀⠙⠢⢭⣢⡚⢣⠀⠀⠀⠀⠀⢀⣇⠁⢸⠁⠀⠀⠀⠀⠀⠀⢸⠀⠀ 
    ⠀⡞⠀⠀⠀⠀⠀⠀⠈⢫⡉⠀⠀⠀⠀⢠⢮⠈⡦⠋⠀⠀⠀⠀⠀⠀⠀⣸⠀⠀ 
    ⢀⠇⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡀⣀⡴⠃⠀⡷⡇⢀⡴⠋⠉⠉⠙⠓⠒⠃⠀⠀ 
    ⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⡼⠀⣷⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
    ⡞⠀⠀⠀⠀⠀⠀⠀⣄⠀⠀⠀⠀⠀⠀⡰⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
    ⢧⠀⠀⠀⠀⠀⠀⠀⠈⠣⣀⠀⠀⡰⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

QUOTE_COMMAND = "!quote 1984"

QUOTES = [
    "War is peace. Freedom is slavery. Ignorance is strength.",
    "If you want a picture of the future, imagine a boot stamping on a human face—for ever.",
    "But if thought corrupts language, language can also corrupt thought.",
    "Doublethink means the power of holding two contradictory beliefs in one's mind simultaneously, and accepting both of them.",
    "Until they become conscious they will never rebel, and until after they have rebelled they cannot become conscious.",
    "Power is in tearing human minds to pieces and putting them together again in new shapes of your own choosing.",
    "Big Brother is Watching You.",
    "Reality exists in the human mind, and nowhere else.",
    "The best books...  are those that tell you what you know already.",
    "One does not establish a dictatorship in order to safeguard a revolution; one makes the revolution in order to establish the dictatorship.",
    "We know that no one ever seizes power with the intention of relinquishing it.",
    "Don't you see that the whole aim of Newspeak is to narrow the range of thought? In the end we shall make thoughtcrime literally impossible, because there will be no words in which to express it."
]


def get_random_quote():
    index = random.randint(0, len(QUOTES) - 1)
    return QUOTES[index]


def main():
    # setup logger
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)-8s %(message)s', level=logging.INFO)
    logging.info('--- Literally 1984 bot started ---')
    # make the reddit instance
    reddit = praw.Reddit("Literally1984_bot", config_interpolation="basic")
    # build subreddits
    subreddit_string = reddit.user.me().subreddit.display_name
    if len(ACTIVE_SUBREDDITS):
        subreddit_string += '+' + '+'.join(ACTIVE_SUBREDDITS)
    subreddits = reddit.subreddit(subreddit_string)
    # poll subreddits
    comments_count = 0
    logging.info('Polling /r/' + subreddit_string)
    for comment in subreddits.stream.comments(pause_after=10, skip_existing=True):
        if comment == None:
            continue
        if comment.author.name in IGNORED_USERS:
            logging.info('Skipping user: ' + comment.author.name)
            continue
        if comment.body[0] == '!' and len(comment.body) >= len(QUOTE_COMMAND) and comment.body[:len(QUOTE_COMMAND)] == QUOTE_COMMAND:
            comments_count += 1
            logging.info('#%s: Quote requested by u/%s in r/%s.' %
                         (str(comments_count), comment.author.name, comment.subreddit.display_name))
            quote = get_random_quote()
            comment.reply(quote)
        elif len(comment.body) >= len(SEARCH_TEXT) and SEARCH_TEXT in comment.body.lower():
            comments_count += 1
            logging.info('#%s: Replying to u/%s in r/%s.' %
                         (str(comments_count), comment.author.name, comment.subreddit.display_name))
            comment.reply(ANSWER_TEXT)


def main_ex():
    while True:
        try:
            main()
        except Exception as e:
            logging.critical('!!Exception raised!!\n' + str(e))
            logging.critical('Restarting in 30 seconds...')
            time.sleep(30)
        else:
            logging.info('--- Literally 1984 bot stopped ---')
            break


if __name__ == "__main__":
    main_ex()
