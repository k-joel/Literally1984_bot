import praw
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

ANSWER_TEXT = """
    ⠀⠀⠀⠀⠀⠀⠀⣠⡀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠤⠤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⢀⣾⣟⠳⢦⡀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠉⠉⠉⠉⠉⠒⣲⡄⠀
    ⠀⠀⠀⠀⠀⣿⣿⣿⡇⡇⡱⠲⢤⣀⠀⠀⠀⢸⠀⠀1984⠀⠀⣠⠴⠊⢹⠁
    ⠀⠀⠀⠀⠀⠘⢻⠓⠀⠉⣥⣀⣠⠞⠀⠀⠀⢸⠀⠀⠀⠀⢀⡴⠋⠀⠀⠀⢸⠀⠀
    ⠀⠀⠀⠀⢀⣀⡾⣄⠀⠀⢳⠀⠀⠀⠀⠀⠀⢸⢠⡄⢀⡴⠁⠀2022⠀⡞⠀⠀
    ⠀⠀⠀⣠⢎⡉⢦⡀⠀⠀⡸⠀⠀⠀⠀⠀⢀⡼⣣⠧⡼⠀⠀⠀⠀⠀⠀⢠⠇⠀⠀
    ⠀⢀⡔⠁⠀⠙⠢⢭⣢⡚⢣⠀⠀⠀⠀⠀⢀⣇⠁⢸⠁⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀
    ⠀⡞⠀⠀⠀⠀⠀⠀⠈⢫⡉⠀⠀⠀⠀⢠⢮⠈⡦⠋⠀⠀⠀⠀⠀⠀⠀⠀⣸⠀⠀⠀
    ⢀⠇⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡀⣀⡴⠃⠀⡷⡇⢀⡴⠋⠉⠉⠙⠓⠒⠃⠀⠀
    ⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⡼⠀⣷⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⡞⠀⠀⠀⠀⠀⠀⠀⣄⠀⠀⠀⠀⠀⠀⡰⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⢧⠀⠀⠀⠀⠀⠀⠀⠈⠣⣀⠀⠀⡰⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

QUOTE_COMMAND = "!quote 1984"
QUOTE_FILENAME = "quotes.txt"

COOLDOWN = 300

class QuoteGen:
    def __init__(self, filename):
        self.index = 0
        self.quotes = []
        with open(filename) as file:
            self.quotes = [line.strip() for line in file]

    def get_next_quote(self):
        quote = self.quotes[self.index]
        self.index = (self.index + 1) % len(self.quotes)
        return quote

    def get_rand_quote(self):
        while True:
            index = random.randint(0, len(self.quotes) - 1)
            if self.index != index:
                self.index = index
                break
        return self.quotes[index]


class UserCooldown:
    def __init__(self, cooldown):
        self.users = dict()
        self.cooldown = cooldown

    def reset(self):
        self.users.clear()

    def is_user_ready(self, name):
        # remove if cooldown has expired
        curr_time = time.time()
        to_del = []
        for user, prev_time in self.users.items():
            if curr_time - prev_time >= self.cooldown:
                to_del.append(user)
        for user in to_del:
            del self.users[user]

        if name in self.users:
            return False
        self.users[name] = curr_time
        return True


def requested_quote(body, command):
    return body[0] == '!' and len(body) >= len(command) and body[:len(command)] == command


def requested_reply(body, trigger):
    return len(body) >= len(trigger) and trigger in body.lower()


class Bot:
    def __init__(self):
        self.qg = QuoteGen(QUOTE_FILENAME)
        self.uc = UserCooldown(COOLDOWN)

    def run(self):
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

        # reset cooldowns
        self.uc.reset()

        for comment in subreddits.stream.comments(pause_after=10, skip_existing=True):
            if comment == None:
                continue

            if comment.author.name in IGNORED_USERS:
                logging.info('User ignored: ' + comment.author.name)
                continue            

            if requested_quote(comment.body, QUOTE_COMMAND):
                if not self.uc.is_user_ready(comment.author.name):
                    logging.info('User on cooldown: ' + comment.author.name)
                    continue
                comments_count += 1
                logging.info('#%s: Quote requested by u/%s in r/%s.' %
                             (str(comments_count), comment.author.name, comment.subreddit.display_name))
                quote = self.qg.get_next_quote()
                if quote and len(quote) != 0:
                    comment.reply(body = "\'" + quote + "\'")
            elif requested_reply(comment.body, SEARCH_TEXT):
                if not self.uc.is_user_ready(comment.author.name):
                    logging.info('User on cooldown: ' + comment.author.name)
                    continue
                comments_count += 1
                logging.info('#%s: Replying to u/%s in r/%s.' %
                             (str(comments_count), comment.author.name, comment.subreddit.display_name))
                comment.reply(body = ANSWER_TEXT)


def main():
    # setup logger
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)-8s %(message)s', level=logging.INFO)

    bot = Bot()
    while True:
        try:
            logging.info('--- Literally 1984 bot started ---')
            bot.run()
        except Exception as e:
            logging.critical('!!Exception raised!!\n' + str(e))
            logging.info('--- Literally 1984 bot stopped ---')
            logging.info('Restarting in 30 seconds...')
            time.sleep(30)
        else:
            break


def test_quotes():
    qg = QuoteGen(QUOTE_FILENAME)
    for _ in range(10):
        print(qg.get_next_quote())
    print("---")
    for _ in range(10):
        print(qg.get_rand_quote())


def test_cooldowns():
    uc = UserCooldown(5)
    for i in range(20):
        n = random.choice(("Alice", "Bob", "Steve"))
        print(i, n, uc.is_user_ready(n))
        time.sleep(1)


if __name__ == "__main__":
    main()
