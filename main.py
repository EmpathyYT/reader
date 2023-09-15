import os
import random
import json


class IGMessageReader:
    def __init__(self, mpath: str, save: bool):
        self.path = mpath
        self.save = save

    def stastisticer(self, name, messagecount, wordcount, contactnumber) -> str:
        return (f"Contact Name: {name}\nMessage Count: {messagecount}\nWordCount: {wordcount}\nContact Count: {contactnumber}\n\n"
                f"<--------------------------------------------------------------------------------->\n\n")

    def textsaver(self, textsaver, save: bool) -> None:
        if save:
            file = open("text.txt", "w", encoding="utf-8")
            file.write(textsaver)
            file.close()

    def wordcounter(self, text) -> int:
        counter = 0
        for message in text['messages']:
            content = 0 if "content" not in message else message['content'].split()
            counter += len(content) if content != 0 else 0
        return counter
       
       

    def messagereader(self):
        statistics = {}
        textsaver = ""
        mpath = f"{self.path}/inbox"
        mlist = os.listdir(mpath)
        i = 0
        messagecount = 0
        totalwordcount = 0
        for contact in mlist:
            messages = os.listdir(str(os.path.join(mpath, contact)))
            for messagebox in messages:
                if ".json" in messagebox:
                    dynamicpath = str(os.path.join(mpath, contact)) + "\\" + messagebox
                    file = json.load(open(dynamicpath, "r"))
                    name = "-".join([x['name'] for x in file['participants']])
                    singlemessagecount = len(file['messages'])
                    wordcount = self.wordcounter(file)
                    messagecount += singlemessagecount
                    totalwordcount += wordcount
                    statistics.update({name: f"{singlemessagecount} {wordcount}"})

            i += 1
            stastic = self.stastisticer(name, singlemessagecount, wordcount, i)
            textsaver += stastic
            print(stastic)

        print("Total Message Count: ", messagecount)
        textsaver += (f"Total Message Count: {messagecount}\n\n"
                      f"<--------------------------------------------------------------------------------->\n\n")
        sortedstats = dict(sorted(statistics.items(), key= lambda item: item[1].split()[0], reverse=True))
        topnums = "Top 50 contacts:\n\n"
        i = 0
        while i < 50:
            topnums += f"{i + 1}. Contact Name: {list(sortedstats.keys())[i]} || Message Count: {list(sortedstats.values())[i].split()[0]} || Word Count: {list(sortedstats.values())[i].split()[1]}\n"
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
