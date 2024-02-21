import os
import json
import matplotlib.pyplot as plt
import random


class IGMessageReader:
    def __init__(self, mpath: str, save: bool, matplotli: bool):
        self.path = mpath
        self.save = save
        self.plot = matplotli

    def stastisticer(self, name, messagecount, wordcount, reelcount, contactnumber) -> str:
        return (
            f"Contact Name: {name}\nMessage Count: {messagecount}\nWordCount: {wordcount}\nReelCount: {reelcount}\nContact Count: {contactnumber}\n\n"
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

    def plotter(self, data, plot: bool):
        if plot:
            i = 0
            x = 8 if len(list(data.items())) >= 8 else len(list(data.items()))
            newdata = {}
            while i < x:
                key, value = list(data.items())[i]
                newdata.update({key: value})
                i += 1

            newdatayaxis = [x[0] for x in list(newdata.values())]
            fig, ax = plt.subplots()
            hbars = ax.barh(list(newdata.keys()), newdatayaxis, align='center')
            ax.set_yticks(list(newdata.keys()), labels=list(newdata.keys()))
            ax.invert_yaxis()
            ax.set_xlabel('Message Count')
            ax.set_title('Top 8 Contacts by Message Count')
            ax.bar_label(hbars)
            ax.set_xlim(right=newdatayaxis[0] + newdatayaxis[0] / 5)
            plt.tight_layout()
            fig.savefig(f"messagecountfig{random.randint(1, 2000)}")

            wordcountsorteddata = dict(sorted(data.items(), key=lambda item: item[1][1], reverse=True))

            i = 0
            x = 8 if len(list(wordcountsorteddata.items())) >= 8 else len(list(wordcountsorteddata.items()))

            newdata = {}
            while i < x:
                key, value = list(wordcountsorteddata.items())[i]
                newdata.update({key: value})
                i += 1

            newdatayaxis = [x[1] for x in list(newdata.values())]
            fig, ax = plt.subplots()
            hbars = ax.barh(list(newdata.keys()), newdatayaxis, align='center')
            ax.set_yticks(list(newdata.keys()), labels=list(newdata.keys()))
            ax.invert_yaxis()
            ax.set_xlabel('Word Count')
            ax.set_title('Top 8 Contacts by Word Count')
            ax.bar_label(hbars)
            ax.set_xlim(right=newdatayaxis[0] + newdatayaxis[0] / 5)
            plt.tight_layout()
            fig.savefig(f"wordcountfig{random.randint(1, 2000)}")

            reelcountsorteddata = dict(sorted(data.items(), key=lambda item: item[1][2], reverse=True))

            i = 0
            x = 8 if len(list(reelcountsorteddata.items())) > 8 else len(list(reelcountsorteddata.items()))

            newdata = {}
            while i < x:
                key, value = list(reelcountsorteddata.items())[i]
                newdata.update({key: value})
                i += 1

            newdatayaxis = [x[2] for x in list(newdata.values())]
            fig, ax = plt.subplots()
            hbars = ax.barh(list(newdata.keys()), newdatayaxis, align='center')
            ax.set_yticks(list(newdata.keys()), labels=list(newdata.keys()))
            ax.invert_yaxis()
            ax.set_xlabel('Reel Count')
            ax.set_title('Top 8 Contacts by Reel Count')
            ax.bar_label(hbars)
            ax.set_xlim(right=newdatayaxis[0] + newdatayaxis[0] / 5)
            plt.tight_layout()
            fig.savefig(f"reelcountfig{random.randint(1, 2000)}")

    def messagereader(self):
        statistics = {}
        textsaver = ""
        mpath = f"{self.path}/inbox"
        mlist = os.listdir(mpath)
        i = 0
        messagecount = 0
        totalwordcount = 0
        totalreelcount = 0
        for contact in mlist:
            messages = os.listdir(str(os.path.join(mpath, contact)))
            contactmessages = 0
            contactwordcount = 0
            contactreelcount = 0
            for messagebox in messages:
                if ".json" in messagebox:
                    dynamicpath = str(os.path.join(mpath, contact)) + "\\" + messagebox
                    filewithoutjson = (open(dynamicpath, "r"))
                    file = json.load(filewithoutjson)
                    name = filewithoutjson.name[filewithoutjson.name.find("/inbox") + 7: \
                                                filewithoutjson.name.find("_", filewithoutjson.name.find("/inbox"))]
                    singlemessagecount = len(file['messages'])
                    contactmessages += singlemessagecount
                    wordcount = self.wordcounter(file)
                    contactwordcount += wordcount
                    messagecount += singlemessagecount
                    totalwordcount += wordcount
                    for message in file['messages']:
                        if "share" in message:
                            contactreelcount += 1

                    totalreelcount += contactreelcount

            statistics.update({name: [contactmessages, contactwordcount, contactreelcount]})

            i += 1
            statistic = self.stastisticer(name, contactmessages, contactwordcount, contactreelcount, i)
            textsaver += statistic
            print(statistic)

            statistics.update({name: [contactmessages, contactwordcount, contactreelcount]})

        print(
            f"Total Message Count: {messagecount} || Total Word Count: {totalwordcount} || Total Reel Count: {totalreelcount}")
        textsaver += (
            f"Total Message Count: {messagecount} || Total Word Count: {totalwordcount} || Total Reel Count: {totalreelcount}\n\n"
            f"<--------------------------------------------------------------------------------->\n\n")
        sortedstats = dict(sorted(statistics.items(), key=lambda item: item[1][0], reverse=True))
        #
        topnums = "Top 50 contacts:\n\n"
        i = 0
        x = 50 if len(list(sortedstats.keys())) >= 50 else len(list(sortedstats.keys()))
        while i < x:
            topnums += f"{i + 1}. Contact Name: {list(sortedstats.keys())[i]} || Message Count: {list(sortedstats.values())[i][0]} || Word Count: {list(sortedstats.values())[i][1]} || Reel Count: {list(sortedstats.values())[i][2]}\n"
            i += 1
        print(topnums)
        textsaver += topnums
        self.textsaver(textsaver, self.save)
        self.plotter(sortedstats, self.plot)


if __name__ == "__main__":
    path = input('Please enter the full path to your messages folder: ').strip()
    saver = input("Do you want to save the results? (T/F): ").strip()
    matplotlibspt = input("Do you want to generate plots? (T/F): ").strip()
    saver = True if saver == "T" or "t" else False
    matplotlibspt = True if matplotlibspt == "T" or "t" else False
    reader = IGMessageReader(path, saver, matplotlibspt)
    reader.messagereader()
