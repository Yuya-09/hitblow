"""大小ヒント機能"""


def hint(secret, guess):
    """入力値が正解より大きいか小さいかを返す"""

    secret_num = int(secret)
    guess_num = int(guess)

    if guess_num < secret_num:
        return "正解はもっと大きい数字です。"
    elif guess_num > secret_num:
        return "正解はもっと小さい数字です。"