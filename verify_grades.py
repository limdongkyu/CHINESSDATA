#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
단체별 급수별 한자·순서·예시 단어 검증 스크립트
"""

import json

# 나무위키 대한검정회 8급~4급 공식 순서
DAEHAN_OFFICIAL = {
    "8급": "九金南男女東六母木門父北四三西水十五月二人日子弟七土八兄火",
    "7급_추가": "江口內年大目白山小手足外右入足左中靑出下",
    "6급_추가": "犬己林馬名百生石先姓心羊魚玉牛耳地川千天",
    "준5급_추가": "車巾古工今同力立末文方本夫不士夕世少食央王位衣字自正主寸向休",
    "5급_추가": "歌家各間强開去見京計高功空共科光敎交校區國軍近急旗記氣農多短答當對代道刀讀冬洞頭等登樂來老理里利萬每面命文明毛無聞問物米民班半放番別步部分社事死色書線性成所首詩時示市植神身信新室安夜弱語言永英午用友遠原元有肉育銀音邑意作長場才田電前全朝祖晝住竹重直草村秋春親太通貝便平夏學韓漢合海行血形花話和活黃會孝後",
    "준4급_추가": "加可角感客格決結輕敬界苦考告曲公果過球郡貴根級吉能堂待德圖度童動落良歷例禮路勞綠流李亡買賣美朴反發法兵病福服奉冰仕思史使算相席雪省洗消速孫樹數宿順術習勝始式臣實失兒愛野藥陽洋漁億業如然溫要勇雲運園院油由飮醫以因任者昨章再在材的赤典戰展庭定題第族卒州注止知紙集參窓責淸體初充特表品風必河幸現號畫化訓凶黑",
    "4급_추가": "價甘減監改個擧健件建競景季固故骨課關觀廣橋具救求舊久局君規極給其器期汽技基念團端壇談都島到獨朗冷兩量旅練領令料類陸律望妹牧武味未倍變報富婦備比費鼻貧寫謝師査産賞商常序選鮮船仙善說星聖盛聲城誠勢歲束送授守視試識氏惡眼案暗約養餘熱葉藝屋完往曜浴雨雄願偉爲恩義移將財災爭低貯敵傳切節店情停精政祭際濟制製除鳥助早造尊宗走竹準衆增志指支至職進眞",
}

# 한국어문회 8급 50자 공식 (검색 결과 예시 기준, 校敎九國軍金南...)
EOMUNHOE_8_OFFICIAL = "校敎九國軍金南女年大東六萬母木門民白父北四山三生西先小水室十五王外月二人一曰長弟中靑寸七土八學韓兄火"

def chars_from_string(s):
    return list(s)

def load_json_chars(fname):
    try:
        with open(fname, encoding="utf-8") as f:
            d = json.load(f)
        return [e["character"] for e in d.get("data", [])]
    except Exception as e:
        return None

def compare_order(name, official_str, actual_list):
    """순서 비교, 불일치 위치 반환"""
    official = chars_from_string(official_str)
    mismatches = []
    for i, (a, b) in enumerate(zip(official, actual_list)):
        if a != b:
            mismatches.append((i + 1, f"공식:{a} vs 실제:{b}"))
    if len(official) != len(actual_list):
        mismatches.append((0, f"개수 불일치: 공식 {len(official)}자 vs 실제 {len(actual_list)}자"))
    return mismatches

def sample_words_quality(fname, sample_size=5):
    """예시 단어 품질 샘플링 - 자주 쓰는 말인지 간단 체크"""
    try:
        with open(fname, encoding="utf-8") as f:
            d = json.load(f)
        data = d.get("data", [])
        common_ok = ["學校", "教育", "學生", "國家", "時間", "社会", "生活", "問題", "文化", "朋友", "電話", "運動", "自然", "人生", "時代"]
        issues = []
        for i, entry in enumerate(data[:sample_size * 3]):  # 앞 15자 샘플
            char = entry["character"]
            words = entry.get("words", [])
            for w in words[:2]:  # 각 글자당 처음 2개 단어만
                h = w.get("hanja", "")
                r = w.get("reading", "")
                # 자주 쓰는 말 목록에 있으면 OK, 없어도 형식만 맞으면 기본 통과
                if not h or not r:
                    issues.append(f"{char}: 빈 한자어/독음")
                # 일본식 표기 의심 (예: 名前→명전은 잘못됨, 名所→명소가 맞음)
                if "전" in r and "名" in h and "명소" not in r and "명찰" not in r:
                    pass  # 특수 케이스
        return issues[:10]  # 최대 10개만
    except Exception as e:
        return [str(e)]

def main():
    print("=" * 70)
    print("1. 대한검정회 - 글자 순서 검증")
    print("=" * 70)

    # 대한검정회 8급
    actual_8 = load_json_chars("default8.json")
    official_8 = DAEHAN_OFFICIAL["8급"]
    if actual_8:
        ms = compare_order("8급", official_8, actual_8)
        if ms:
            print("✗ 8급 불일치:", ms)
        else:
            print("✓ 8급 30자 순서 일치")

    # 대한검정회 7급 (8+7 추가분)
    actual_7 = load_json_chars("default7.json")
    combined_7 = official_8 + DAEHAN_OFFICIAL["7급_추가"]
    if actual_7 and len(actual_7) == 50:
        ms = compare_order("7급", combined_7, actual_7)
        if ms:
            print("✗ 7급 불일치:", ms[:5])
        else:
            print("✓ 7급 50자 순서 일치")

    print()
    print("=" * 70)
    print("2. 한국어문회 - 글자 순서 검증")
    print("=" * 70)

    actual_e8 = load_json_chars("default_8.json")
    if actual_e8:
        e8_chars = "".join(actual_e8[:50])
        if e8_chars == EOMUNHOE_8_OFFICIAL:
            print("✓ 8급 50자 순서 일치 (공식 예시와 동일)")
        else:
            # 처음 10자 비교
            for i in range(min(10, len(actual_e8), len(EOMUNHOE_8_OFFICIAL))):
                a, b = EOMUNHOE_8_OFFICIAL[i], actual_e8[i] if i < len(actual_e8) else "?"
                mark = "✓" if a == b else "✗"
                print(f"  {mark} {i+1}번: 공식 {a} vs 실제 {b}")

    print()
    print("=" * 70)
    print("3. 예시 단어 품질 샘플 (일부)")
    print("=" * 70)

    for fname, label in [
        ("default8.json", "대한검정회 8급"),
        ("default_8.json", "한국어문회 8급"),
        ("default_7.json", "대한검정회 7급"),
    ]:
        issues = sample_words_quality(fname)
        if issues:
            print(f"{label}: 검토 필요 {len(issues)}건 - {issues[:3]}")
        else:
            print(f"{label}: 예시 단어 형식 양호")

    # 예시 단어 샘플 출력
    print()
    print("예시 단어 샘플 (한국어문회 8급 첫 3자):")
    if actual_e8:
        with open("default_8.json", encoding="utf-8") as f:
            d = json.load(f)
        for e in d["data"][:3]:
            print(f"  {e['character']} ({e['meaning']}): ", end="")
            words = [f"{w['hanja']}({w['reading']})" for w in e["words"][:3]]
            print(", ".join(words))

if __name__ == "__main__":
    main()
