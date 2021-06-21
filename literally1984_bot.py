import praw
import prawcore
import time
import logging

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
        comments_count += 1
        logging.info('Replying to u/%s in r/%s. Comment #%s' %
                     (str(comment.author), str(comment.subreddit), str(comments_count)))
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
