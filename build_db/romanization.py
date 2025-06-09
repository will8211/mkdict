#!/usr/bin/env python3

import re


def poj_convert(s):

    end = r"([-\s\)\*\.\?,\/]|$)"  # [ - SPACE ) * . ? , ] OR string-end
    start = r"(^|[-\s\(\/])"  # string-start OR [ - SPACE ( ]

    s_numbers = re.sub(r"\*", r"nn", s)
    s_numbers = re.sub(r"\+", r"o", s_numbers)
    # Move numbers to the end:
    s_numbers = re.sub(r"([2-9])([a-zA-Z]*)" + end, r"\2\1\3", s_numbers)
    # Add unmarked 1st and 4th tones:
    unmarked = start + r"([a-zA-Z]+)" + end
    while re.search(unmarked, s_numbers):  # because start and end might overlap
        s_numbers = re.sub(unmarked, r"\g<1>\g<2>1\g<3>", s_numbers)
    s_numbers = re.sub(r"([aeiou])([ptkh])1", r"\g<1>\g<2>4", s_numbers)

    s_search = re.sub(r"[1-9]", r"", s_numbers)

    s = s.replace("2", "\u0301")
    s = s.replace("3", "\u0300")
    s = s.replace("5", "\u0302")
    s = s.replace("7", "\u0304")
    s = s.replace("8", "\u030D")
    # s = s.replace('+', '\u0358') #Combining character
    s = s.replace("+", "·")  # Non-combining character
    s = s.replace("*", "ⁿ")

    return s, s_search, s_numbers


def trs_convert(s):

    end = r"([-\s\)\*\.\?,\/]|$)"
    start = r"(^|[-\s\(\/])"

    s = s.replace("ch", "ts")
    s = s.replace("Ch", "Ts")
    s = re.sub(r"e([2-8]*)k", r"i\1k", s)
    s = re.sub(r"E([2-8]*)k", r"I\1k", s)
    s = re.sub(r"e([2-8]*)ng", r"i\1ng", s)
    s = re.sub(r"E([2-8]*)ng", r"I\1ng", s)
    s = re.sub(r"o([2-8]*)([ea])", r"u\1\2", s)
    s = re.sub(r"O([2-8]*)([ea])", r"U\1\2", s)
    s_numbers = re.sub(r"\*", r"nn", s)
    s_numbers = re.sub(r"\+", r"o", s_numbers)
    # Move numbers to the end:
    s_numbers = re.sub(r"([2-9])([a-zA-Z]*)" + end, r"\2\1\3", s_numbers)
    unmarked = start + r"([a-zA-Z]+)" + end
    while re.search(unmarked, s_numbers):  # because start and end might overlap
        s_numbers = re.sub(unmarked, r"\g<1>\g<2>1\g<3>", s_numbers)
    s_numbers = re.sub(r"([aeiou])([ptkh])1", r"\g<1>\g<2>4", s_numbers)

    s_search = re.sub(r"[1-9]", r"", s_numbers)

    s = s.replace("2", "\u0301")
    s = s.replace("3", "\u0300")
    s = s.replace("5", "\u0302")
    s = s.replace("7", "\u0304")
    s = s.replace("8", "\u030D")
    s = s.replace("+", "o")
    s = s.replace("*", "nn")

    return s, s_search, s_numbers


def dt_convert(s):

    # Reject multi-word strings
    if re.search(r"[\w\+\*]\s[a-zA-Z]", s):  # '\w' is an alphanumeric
        return ("", "", "")

    initials = [
        ("p", "b"),
        ("b", "bh"),
        ("ph", "p"),
        ("t", "d"),
        ("th", "t"),
        ("k", "g"),
        ("g", "gh"),
        ("kh", "k"),
        ("ch", "z"),
        ("j", "r"),
        ("chh", "c"),
        ("P", "B"),
        ("B", "Bh"),
        ("Ph", "P"),
        ("T", "D"),
        ("Th", "T"),
        ("K", "G"),
        ("G", "Gh"),
        ("Kh", "K"),
        ("Ch", "Z"),
        ("J", "R"),
        ("Chh", "C"),
    ]
    # ('chi', 'zi'), ('ji', 'ri'), ('chhi', 'ci'),
    # ('Chi', 'Zi'), ('Ji', 'Ri'), ('Chhi', 'Ci'),
    # ('Ji', 'Ri')/('ji', 'ri') might be just 'R'/'r'

    finals = [
        ("o([2-8]*)", r"o\1r"),
        ("o([2-8]*)h", r"o\1rh"),
        ("e([2-8]*)ng", r"i\1ng"),
        ("e([2-8]*)k", r"i\1k"),
        ("o([2-8]*)a", r"u\1a"),
        ("o([2-8]*)e", r"u\1e"),
        ("o([2-8]*)ai", r"u\1ai"),
        ("o([2-8]*)an", r"u\1an"),
        ("o([2-8]*)ang", r"u\1ang"),
        ("O([2-8]*)", r"O\1r"),
        ("O([2-8]*)h", r"O\1rh"),
        ("E([2-8]*)ng", r"I\1ng"),
        ("E([2-8]*)k", r"I\1k"),
        ("O([2-8]*)a", r"U\1a"),
        ("O([2-8]*)e", r"U\1e"),
        ("O([2-8]*)ai", r"U\1ai"),
        ("O([2-8]*)an", r"U\1an"),
        ("O([2-8]*)ang", r"U\1ang"),
    ]

    # Sort by length, longest items first

    initials.sort(key=lambda item: len(item[0]), reverse=True)
    finals.sort(key=lambda item: len(item[0]), reverse=True)

    # Apply changes
    # (The '$' sign stops initials/ finals from being detected twice)

    start = r"(^|[-\s\(\/])"
    for item in initials:
        s = re.sub(start + item[0], r"\1$" + item[1], s)
    s = s.replace("$", "")

    end = r"([-\s\)\*\.\?,\/]|$)"
    for item in finals:
        s = re.sub(item[0] + end, item[1] + r"$\2", s)
    s = s.replace("$", "")

    s = s.replace("*", "ⁿ")
    s = s.replace("+", "")

    # Tone Sandhi

    s = re.sub(r"2(.*-)", r"$\1", s)  # 2-->1* (1 is unmarked--$ is placeholder)

    s = re.sub(r"3(.*-)", r"2\1", s)  # 3-->2

    s = re.sub(r"7(.*-)", r"3\1", s)  # 7-->3

    # The tricky 1*-->7
    s = re.sub(
        r"(^|[-\s\(])([a-zA-Z]*)([aeiouAEIOU])([ⁿmngr]*|gh)-",
        r"\g<1>\g<2>\g<3>7\g<4>-",
        s,
    )
    # g1(start) g2(any/no letter) g3(vowel) ADD 7 g4(any/no ⁿmngr OR gh) dash
    # The 'gh' is so not to match a single terminal h

    # 1-->7 on a voweless syllable
    s = re.sub(r"(^|[-\s\(])(m|M|ng|Ng|sng|Sng|mng|Mng)-", r"\g<1>\g<2>7-", s)

    s = re.sub(r"([aeiou])([ptkh])", r"\g<1>2\g<2>", s)  # \g<1> == \1
    # 4**-->2 (4 is unmarked ap ak ah...)

    s = re.sub(r"5(.*-)", r"7\1", s)  # 5-->7

    s = re.sub(r"8(.*-)", r"3\1", s)  # 8-->3

    s = s.replace("$", "")

    # Searchable and numbered version

    s_numbers = re.sub(r"ⁿ", r"nn", s)
    s_numbers = re.sub(r"([1-9])([a-zA-Z]*)" + end, r"\2\1\3", s_numbers)
    s_search = re.sub(r"[1-9]", r"", s_numbers)

    # Apply diacritics

    s = re.sub(r"([aeiou])([ptkh])", r"\g<1>4\g<2>", s)  # \g<1> == \1
    s = s.replace("2", "\u0300")
    s = s.replace("3", "\u0302")
    s = s.replace("4", "\u0304")
    s = s.replace("5", "\u030C")
    s = s.replace("7", "\u0304")
    s = s.replace("8", "")

    return s, s_search, s_numbers
