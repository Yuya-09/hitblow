"""AIとの対戦モード（1機能=1ファイルのルールに準拠）"""

import random
from itertools import permutations
from .core import judge

def play_vs_ai(secret, digits):
    print(f"\n 【AI対戦モード】 先に {digits} 桁当てた方の勝ちです！")
    print("\n ヒントの説明: hint 数字 と入力すると、正解がその数字より大きいか小さいか分かります。")
    
    # AIの初期候補リスト（例：3桁なら012〜987の全組み合わせ）
    candidates = ["".join(p) for p in permutations("0123456789", digits)]
    hint_count = 0
    max_hints = digits
    tries = 0
    while True:
        # =====  プレイヤーのターン =====
        guess = input("\nあなたの予想 > ").strip()

        from .hint import hint
        if guess.startswith("hint "):
            parts = guess.split()

            if len(parts) != 2:
                print(f"使い方: hint {'0'*digits}")
                continue

            if hint_count >= max_hints:
                print("ヒントはもう使えません。")
                continue

            print(f"ヒント({hint_count + 1}/{max_hints}): {hint(secret, parts[1])}")

            hint_count += 1

            continue
        if len(guess) != digits or not guess.isdigit():
            print(f"{digits} 桁の数字で入力してね")
            continue
        
        tries += 1
        hit, blow = judge(secret, guess)
        print(f"   あなた: Hit={hit}  Blow={blow}")
        
        if hit == digits:
            print(f"\n あなたの勝利！ {tries} 回で当たり（答え {secret}）")
            break
            
        # =====  AIのターン =====
        # AIは残った候補の中からランダムに1つ選んで予想する
        ai_guess = random.choice(candidates)
        print(f"AIの予想     > {ai_guess}")
        
        ai_hit, ai_blow = judge(secret, ai_guess)
        print(f"   AI: Hit={ai_hit}  Blow={ai_blow}")
        
        if ai_hit == digits:
            print(f"\nAIの勝利... あなたの負けです（答え {secret}）")
            break
            
        # 💡 AIの学習ロジック（core.pyのjudgeを再利用）
        # 「もし候補cが正解だとしたら、今回の予想(ai_guess)と同じHit/Blowになるはず」
        # という条件で、矛盾する候補をリストから除外して絞り込む
        candidates = [c for c in candidates if judge(c, ai_guess) == (ai_hit, ai_blow)]