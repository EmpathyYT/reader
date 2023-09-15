import os
import re
from functools import reduce
import random


class IGMessageReader:
    def __init__(self, mpath: str, save: bool):
        self.path = mpath
        self.save = save

    def stastisticer(self, name, messagecount, contactnumber) -> str:
        return (f"Contact Name: {name}\nMessage Count: {messagecount}\nContact Count: {contactnumber}\n\n"
                f"<--------------------------------------------------------------------------------->\n\n")

    def textsaver(self, textsaver, save: bool) -> None:
        if save:
            file = open("text.txt", "w")
            file.write(textsaver)
            file.close()

    def wordcounter(self, text):
        counter = 0
        texttosearchfor = '<div class="_3-95 _a6-p"><div><div></div><div>'
        messagestart = reduce(lambda x, y: x + [y.start()], re.finditer(texttosearchfor, text), [])
        messageend = reduce(lambda x, y: x + [y.start()], re.finditer("</div><div></div><div></div>", text), [])
        messages = dict(zip(messagestart, messageend))
        for indexstart, indexend in messages.items():
            print(text[indexstart + len(texttosearchfor): indexstart + len(texttosearchfor) + 7])
            if text[indexstart + len(texttosearchfor): indexstart + len(texttosearchfor) + 6] != "</div>":
                counter += 1

    def messagereader(self):
        statistics = {}
        textsaver = ""
        mpath = f"{self.path}/inbox"
        mlist = os.listdir(mpath)
        i = 0
        messagecount = 0
        for contact in mlist:
            messages = os.listdir(str(os.path.join(mpath, contact)))
            for messagebox in messages:
                if ".html" in messagebox:
                    dynamicpath = str(os.path.join(mpath, contact)) + "\\" + messagebox
                    file = open(dynamicpath, "r")
                    name = file.name[file.name.find("/inbox") + 7: file.name.find("_", file.name.find("/inbox"))]
                    name = str(random.randint(1, 100000)) if "\\message" in name else name
                    filereader = file.read()
                    singlemessagecount = filereader.count("pam _3-95 _2ph- _a6-g uiBoxWhite noborder")
                    messagecount += singlemessagecount
                    statistics.update({name: singlemessagecount})

            i += 1
            stastic = self.stastisticer(name, singlemessagecount, i)
            textsaver += stastic
            print(stastic)

        print("Total Message Count: ", messagecount)
        textsaver += (f"Total Message Count: {messagecount}\n\n"
                      f"<--------------------------------------------------------------------------------->\n\n")
        sortedstats = dict(sorted(statistics.items(), key=lambda item: item[1], reverse=True))
        topnums = "Top 50 contacts:\n\n"
        i = 0
        while i < 50:
            topnums += f"{i + 1}. Contact Name: {list(sortedstats.keys())[i]} || Message Count: {list(sortedstats.values())[i]}\n"
            i += 1
        print(topnums)
        textsaver += topnums
        self.textsaver(textsaver, self.save)


if __name__ == "__main__":
    path = input('Please enter the full path to your messages folder: ').strip()
    saver = input("Do you want to save the results? (T/F): ").strip()
    saver = True if saver == "T" or "t" else False
    reader = IGMessageReader(path, saver)
    reader.messagereader()
