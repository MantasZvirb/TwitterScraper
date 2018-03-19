import urllib2
import time
import sys

def ScrapTweets(Txt,OutArray):
	Index = 0;
	ContainerHeader = "<tr class=\x22tweet-container\x22>"
	TextDataHeader = "<div class=\x22dir-ltr\x22 dir=\x22ltr\x22>"
	while(1):
		BlockContainer = Txt.find(ContainerHeader,Index);
		if(BlockContainer == -1):
			break
		Index=BlockContainer+1
		TextIndex = Txt.find(TextDataHeader,BlockContainer) + len(TextDataHeader)
		i1 = 0
		TextData = ""
		while(Txt[i1+TextIndex] != "<"):
			TextData+= Txt[i1+TextIndex]
			i1+=1
		if(TextData != " " or TextData !=""):
			TextData.replace("&amp;","&");
			TextData.replace("&quot;","\x22");
			OutArray.append(TextData)

def FindOlderTweetLink(Txt):
	Indx = Txt.find("Load older Tweets")
	if(Indx == -1):
		return -1
	Dta = ""
	while(Txt[Indx] != "\x22"):
		Indx-=1
	Indx-=1
	while(Txt[Indx] != "\x22"):
		Indx-=1
	Indx+=1
	while(Txt[Indx] != "\x22"):
		Dta+=Txt[Indx]
		Indx+=1
	
	return Dta
	
def ScrapAllTweets(OutTweetArray,UserStr):
	twitterdomain = "https://mobile.twitter.com"
	NextDomain = UserStr
	Indx = 0
	while(NextDomain != -1):
		try:
			contents = urllib2.urlopen(twitterdomain+NextDomain).read()
		except urllib2.URLError:
			break
		ScrapTweets(contents,OutTweetArray)
		NextDomain = FindOlderTweetLink(contents)
		time.sleep(0.3)

def GetWords(TextArray,OutWordArray):
	for Data in TextArray:
		Word = ""
		for c in Data:
			if(c != " "):
				Word+=c;
			else:
				if(Word != ""):
					OutWordArray.append(Word)
					Word = ""
		if(Word != ""):
			OutWordArray.append(Word)
#Entry
TweetArray = []
WordArray = []

UserNameString = "/";

if(len(sys.argv) == 2):
	UserNameString+= sys.argv[1]
else:
	print "Arg1:Twitter username"
	sys.exit()

ScrapAllTweets(TweetArray,UserNameString)
for i in TweetArray:
	print i
		