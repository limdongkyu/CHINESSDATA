#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
한국어문회 기준 급수별 JSON 생성 스크립트
default_8.json ~ default_4.json (언더스코어 형식)
8급 50자, 7급 150자, 6급 300자, 5급 500자, 4급 1000자
"""

import json
import sys

# generate_grade7 모듈에서 7급 데이터 import
from generate_grade7 import GRADE7_DATA, build_categories


def to_entry(item):
    """GRADE7_DATA 형식 → JSON 엔트리 변환"""
    char, meaning, sound, strokes, words = item
    return {
        "character": char,
        "meaning": meaning,
        "sound": sound,
        "strokeCount": strokes,
        "words": [{"hanja": w[0], "reading": w[1], "meaning": w[2]} for w in words]
    }


def make_simple_entry(char, meaning, sound, strokes):
    """간략 데이터용 엔트리 생성"""
    return {
        "character": char,
        "meaning": meaning,
        "sound": sound,
        "strokeCount": strokes,
        "words": [
            {"hanja": f"{char}字", "reading": f"{sound}자", "meaning": f"{meaning} 글자"},
            {"hanja": f"{char}文", "reading": f"{sound}문", "meaning": f"{meaning} 글"},
            {"hanja": f"{char}語", "reading": f"{sound}어", "meaning": f"{meaning} 말"},
            {"hanja": f"{char}學", "reading": f"{sound}학", "meaning": f"{meaning} 배움"},
            {"hanja": f"{char}業", "reading": f"{sound}업", "meaning": f"{meaning} 업"},
        ]
    }


def main():
    # 8급: GRADE7_DATA 첫 50자
    data_8 = [to_entry(x) for x in GRADE7_DATA[:50]]
    write_json("default_8.json", data_8, "8급")

    # 7급: GRADE7_DATA 전체 150자
    data_7 = [to_entry(x) for x in GRADE7_DATA]
    write_json("default_7.json", data_7, "7급")

    # 6급: 7급 150 + 준6급·6급 150
    from generate_grade6 import GRADE6_NEW_DATA
    data_6 = data_7.copy()
    for item in GRADE6_NEW_DATA:
        data_6.append(to_entry(item))
    write_json("default_6.json", data_6, "6급")

    # 5급: 6급 300 + 준5급·5급 200
    from generate_grade5 import GRADE5_NEW_DATA
    data_5 = data_6.copy()
    for item in GRADE5_NEW_DATA:
        data_5.append(to_entry(item))
    write_json("default_5.json", data_5, "5급")
    write_json("default_5_2.json", data_5[:400], "5급II(준5급)")

    # 4급: 5급 500 + 준4급·4급 500
    from generate_grade4 import GRADE4_DATA, GRADE4_CHARS_SIMPLE, make_entry as make_entry_4
    data_4 = data_5.copy()
    for item in GRADE4_DATA:
        data_4.append(make_entry_4(item[0], item[1], item[2], item[3], item[4]))
    for char, meaning, sound, strokes in GRADE4_CHARS_SIMPLE:
        data_4.append(make_simple_entry(char, meaning, sound, strokes))
    write_json("default_4.json", data_4, "4급")
    write_json("default_4_2.json", data_4[:750], "4급II(준4급)")

    print("\n한국어문회 기준 default_8.json ~ default_4.json + 준급 생성 완료")


def write_json(fname, data, label):
    """JSON 파일 저장"""
    categories = build_categories(data)
    result = {"version": "0.5", "data": data, "categories": categories}
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"{fname} 생성 완료: {label} {len(data)}자")


if __name__ == "__main__":
    main()
