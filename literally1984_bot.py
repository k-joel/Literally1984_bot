import praw
import prawcore
import time
import logging
import random

ACTIVE_SUBREDDITS = [
    'PoliticalCompassMemes',
]

SEARCH_TEXT = "literally 1984"

ANSWER_TEXT = """
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


BOOK = """
        __________________   ___________________
    .-/|                  \ /                   |\-.
    ||||                   |   War is peace.    ||||
    ||||                   |                    ||||
    ||||       1984        | Freedom is slavery ||||
    ||||                   |                    ||||
    ||||                   |    Ignorance is    ||||
    ||||                   |      strength      ||||
    ||||                   |                    ||||
    ||||__________________ | ___________________||||
    ||/===================\|/====================\||
    `--------------------~___~--------------------''
"""


BOOK2 = """
        __________________   __________________
    .-/|                  \ /                  |\-.
    ||||  One does not     |  one makes the    ||||
    ||||  establish a      |  revolution in    ||||
    ||||  dictatorship     |  order to         ||||
    ||||  in order to      |  establish the    ||||
    ||||  safeguard a      |  dictatorship.    ||||
    ||||  revolution...    |                   ||||
    ||||                   |                   ||||
    ||||__________________ | __________________||||
    ||/===================\|/===================\||
    `--------------------~___~-------------------''
"""

BOOK3 = """
        __________________   __________________
    .-/|                  \ /                  |\-.
    ||||                   | Power is in       ||||
    ||||                   | tearing human     ||||
    ||||       1984        | minds to pieces   ||||
    ||||                   | and putting them  ||||
    ||||                   | together again    ||||
    ||||                   | in new shapes of  ||||
    ||||                   | your own choosing ||||
    ||||__________________ | __________________||||
    ||/===================\|/===================\||
    `--------------------~___~-------------------''
"""

BOOK4 = """
        __________________   __________________
    .-/|                  \ /                  |\-.
    ||||                   | We know that      ||||
    ||||                   | no one ever       ||||
    ||||       1984        | seizes power      ||||
    ||||                   | with the          ||||
    ||||                   | intention of      ||||
    ||||                   | relinquishing it  ||||
    ||||                   |                   ||||
    ||||__________________ | __________________||||
    ||/===================\|/===================\||
    `--------------------~___~-------------------''
"""

REPLIES = [ANSWER_TEXT] * 3 + [BOOK, BOOK2, BOOK3]
REPLY_INDEX = 0


def get_next_reply():
    global REPLY_INDEX
    reply = REPLIES[REPLY_INDEX]
    REPLY_INDEX = (REPLY_INDEX + 1) % len(REPLIES)
    return reply


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
        if comment == None:  # or comment.author == reddit.user.me():
            continue
        if len(comment.body) < len(SEARCH_TEXT) or SEARCH_TEXT not in comment.body.lower():
            continue
        if comment.author.name == 'basedcount_bot':
            logging.info('Skipping reply to u/basedcount_bot')
            continue
        comments_count += 1
        logging.info('Replying to u/%s in r/%s. Comment #%s' %
                     (comment.author.name, comment.subreddit.display_name, str(comments_count)))
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
