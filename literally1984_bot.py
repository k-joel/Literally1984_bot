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
    "Big Brother is Watching You.",
    "If you want a picture of the future, imagine a boot stamping on a human face—for ever.",
    "But if thought corrupts language, language can also corrupt thought.",
    "Doublethink means the power of holding two contradictory beliefs in one's mind simultaneously, and accepting both of them.",
    "Until they become conscious they will never rebel, and until after they have rebelled they cannot become conscious.",
    "Power is in tearing human minds to pieces and putting them together again in new shapes of your own choosing.",
    "Reality exists in the human mind, and nowhere else.",
    "One does not establish a dictatorship in order to safeguard a revolution; one makes the revolution in order to establish the dictatorship.",
    "We know that no one ever seizes power with the intention of relinquishing it.",
    "Don't you see that the whole aim of Newspeak is to narrow the range of thought? In the end we shall make thoughtcrime literally impossible, because there will be no words in which to express it.",
    "I enjoy talking to you. Your mind appeals to me. It resembles my own mind except that you happen to be insane.",
    "The masses never revolt of their own accord, and they never revolt merely because they are oppressed. Indeed, so long as they are not permitted to have standards of comparison, they never even become aware that they are oppressed.",
    "The essential act of war is destruction, not necessarily of human lives, but of the products of human labour. War is a way of shattering to pieces, or pouring into the stratosphere, or sinking in the depths of the sea, materials which might otherwise be used to make the masses too comfortable, and hence, in the long run, too intelligent.",
    "Perhaps one did not want to be loved so much as to be understood.",
    "Who controls the past controls the future. Who controls the present controls the past.",
    "The Ministry of Peace concerns itself with war, the Ministry of Truth with lies, the Ministry of Love with torture and the Ministry of Plenty with starvation. These contradictions are not accidental, nor do they result from from ordinary hypocrisy: they are deliberate exercises in doublethink",
    "What can you do against the lunatic who is more intelligent than yourself, who gives your arguments a fair hearing and then simply persists in his lunacy?",
    "The choice for mankind lies between freedom and happiness and for the great bulk of mankind, happiness is better.",
    "You will be hollow. We shall squeeze you empty, and then we shall fill you with ourselves.",
    "The past was alterable. The past never had been altered. Oceania was at war with Eastasia. Oceania had always been at war with Eastasia.",
    "The best books...  are those that tell you what you know already.",
]

COOLDOWN = 300


class QuoteGen:
    def __init__(self):
        self.index = 0

    def get_next_quote(self):
        quote = QUOTES[self.index]
        self.index = (self.index + 1) % len(QUOTES)
        return quote

    def get_rand_quote(self):
        while True:
            index = random.randint(0, len(QUOTES) - 1)
            if self.index != index:
                self.index = index
                break
        return QUOTES[index]


class UserCooldown:
    def __init__(self):
        self.users = dict()

    def is_user_ready(self, name):
        # remove if cooldown has expired
        curr_time = time.time()
        to_del = []
        for user, prev_time in self.users.items():
            if curr_time - prev_time >= COOLDOWN:
                to_del.append(user)
        for user in to_del:
            del self.users[user]

        if name in self.users:
            return False
        self.users[name] = curr_time
        return True


def requested_quote(body):
    return body[0] == '!' and len(body) >= len(QUOTE_COMMAND) and body[:len(QUOTE_COMMAND)] == QUOTE_COMMAND


def requested_reply(body):
    return len(body) >= len(SEARCH_TEXT) and SEARCH_TEXT in body.lower()


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

    qg = QuoteGen()
    uc = UserCooldown()

    for comment in subreddits.stream.comments(pause_after=10, skip_existing=True):
        if comment == None:
            continue

        if comment.author.name in IGNORED_USERS:
            logging.info('Skipping user: ' + comment.author.name)
            continue

        if requested_quote(comment.body):
            if not uc.is_user_ready(comment.author.name):
                logging.info('User on cooldown: ' + comment.author.name)
                continue
            comments_count += 1
            logging.info('#%s: Quote requested by u/%s in r/%s.' %
                         (str(comments_count), comment.author.name, comment.subreddit.display_name))
            quote = qg.get_next_quote()
            comment.reply("\'" + quote + "\'")
        elif requested_reply(comment.body):
            if not uc.is_user_ready(comment.author.name):
                logging.info('User on cooldown: ' + comment.author.name)
                continue
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


def test_quotes():
    qg = QuoteGen()
    for _ in range(10):
        print(qg.get_next_quote())
    print("---")
    for _ in range(10):
        print(qg.get_rand_quote())


def test_cooldowns():
    uc = UserCooldown()
    for i in range(20):
        n = random.choice(("Alice", "Bob", "Steve"))
        print(i, n, uc.is_user_ready(n))
        time.sleep(1)


if __name__ == "__main__":
    main_ex()
