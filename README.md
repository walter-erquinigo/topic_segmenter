# Topic Segmenter

## What is it?

It's a tool that segments messages in group chat into several conversations, each one about a certain topic, hence the name 'Topic Segmenter'. See below for an example.

Following there's a short explanation of the algorithm, which assumes knowledge of NLP and Neural Networks.

## Considerations

The messages belonging to the same group might not necessarily be sequential. For example, there could this order of topics: *cake*, *trip*, *cake*, *family*. This means that the topic *cake* was treated twice, thus
we have to group up those messages into a single non-sequential group.

Regarding a single topic *T*, there could be a lengthy conversation (e.g. > 50 messages). We could safely assume that in most of the cases this conversation treats several subtopics of *T*, thus we expect that no
group is big unless very special cases.

There a considerable amount of messages that are simply reply messages (e.g. 'Ok. let's do it', 'I agree', 'Mine is better', etc.) which don't contribute to the topic but are part of the same topic. Semantically,
these messages by themselves carry no meaning unless they belong to a bigger topic. We call these message **reply objects**, and we treat them as a particular case. According to the paper [Topic Detection in Group 
Chat Based on Implicit Reply](http://link.springer.com/chapter/10.1007%2F978-3-319-42911-3_56) more than 90% of the messages are reply objects in a group conversation.

The topics can be latent. For example, in the messages ['Hey, did you like it?', 'Yes, a lot.'] the topic is not explicit, they might be talking about a cake, therefore the topic is latent.

## How it works?

1. It uses the *nltk* to tokenize each message removing stop words (e.g. 'to', 'and', 'a') and puctuation signs, except in cases like "It's", where the aposthrophe is necessary. The we use a *Snowball stemmer* to reduce each word
to its root form (e.g. 'agrees' and 'agreed' to 'agree'). Now we have a simplified vector text for each message.
2. Then we use a *Word2Vec* model to convert each word into an *n*-dimensional vector (by default *n* is 100). The advtange of this model is that algebraic operations on these vector carry semantic meaning (e.g. vector('king') - vector('man') ~= vector('queen') - vector('woman')). We use the whole set of messages as the training data of the model.
3. Then we use *POS* (part-of-speech) analysis from *nltk* to discover if a message is a semantic object. For example, messages that start with conjugations (e.g. 'but') or special possesive pronouns (e.g. 'mine', theirs') are very likely reply objects. They are marked accordingly.
4. Then we iteratively, maintain a window of the last 3 topics. When processing message *i*, our window has at most the last 3 topics up to message *i - 1*. If the current message is a reply object, then we attach it to the last topic. IF not, we find the similarity distance (we'll talk about this later) of this message to all the messages from the topics in the window. If this distance is greater than a given threshold (default is 0.8) we attach this message to that topic, otherwise, we create a new topic from this message.
5. As a post-step, if there are groups of 1 or 2 messages that are surrounded by messages belonging to the same topic, the bigger topic absorbs the tiny one. This happens when one or two messages are short and so grammatically incoherent that it's not possible to related them to any existing topic.

## Similarity distance

The similarity distance of two messages is comprised of two calculations. The first one is the euclidean distance of the centroids of the vector-set representation of the messages using Word2Vec. The centroid of a set of points
carries an average semantic meaning of the source points. When two messages are too long, the points representing them are too spread and thus the centroid loses semantic meaning, in this cases we have a sliding window of size 10 for each message, then we double iterate on these two windows finding the corresponding centroid and the distances between them. We pick the smallest distance, thus this being the distance between the closest related submessages.

The second calculation is the cosine similarity of these vectors.

There's one additional consideration, we use a decay function (base 0.993) for both the euclidean distance and the cosine similarity. With this, if two messages are semantically similar but they are too far away (e.g. messages 100 and 200), the decay function is applied as a penalty, hence minimizing the likelihood of two distant groups being merged because they talk about similar topics, but when the timespan between them is large, it's very likely that the latent topics are different.

When we want to find the similarity distance between two messages, we first find, from all the pairs of windows, the smallest 5% by euclidean distance, and from them we pick the pair with the greatest cosine similarity. We do this because it can happen that two windows are very close in the euclidean metric by they are orthogonal (unrelated semantically) and thus the similarity is 0.

## Sample Run
`python Runner.py ./samplegeneral.json`

## Sample Output:

== Topic ==

- 2:    In addition, because none of this is associated with our university addresses, we are not subject to FOIAs, so we can say dumb things without the threat of being taken down for it.
- 4:    yeo!
- 5:    we can share the codes `inline = rnorm(1,1,1)` and in blocks ``` blocks = rnorm(100, 1, 1) ```
- 6:    And, things stay in places that make sense.
- 7:    There are presently two additional channels to keep things straight. <#C16S81202> and <#C16RM7TD2> “subscribe" to those if you haven’t.
- 8:    Also, the phone and desktop clients are nice.
- 11:    sup <@U16S9N0LE>
- 12:    sup <@U16RAECF5>
- 14:    Another thought… because who doesn’t have time for more thoughts…
- 15:    There is a lot of working being done right now about evaluating the “gender tone” of job posts, resumes, etc. For example, work being done by <https://textio.com/> that is running things past a sentiment and gender filter on a bag of words. Possible for ballots when they come out? Candidate position statements? This is non-expermiental work, and probably just mostly sensational work that would be headed for the news cycle not a journal, but it is pretty low-hanging fruit.
- 16:    I bet that we could even get them to task an intern onto collecting the corpus of text for us as well.
- 19:    Not for this election. That would have to be scraped, unfortunately. The Making Electoral Democracy Work project has press releases for campaigns in Britain and Canada for the last few elections but that corpus probably isn’t as interesting.


== Topic ==

- 17:    My first thought was to use this to examine candidate press releases. I wonder about the extent to which the gender tone of these statement varies across parties and/or according to the gender of the candidate.
- 18:    Does a current corpus exist? Would love to know how Trump comes out in a mysogeny (sp???) score.
- 20:    I dunno, Trudeau’s campaign was pretty awesome.
- 21:    <@U16RAECF5>: we doing that evidence review today?
- 22:    yrp. I just finished a review, I'm going to give Devesh a quick call, then get on it.


== Topic ==

- 23:    k. i’m there too...
- 24:    Is anybody mailing stamps to all-mail states? Perhaps for the general election the feds are taking care of postage, but for primaries people still have to pay postage (because it is not _strictly_ federal elections). Dammit, we should have done that.
- 25:    That would have been a sweet intervention.
- 26:    Wait. It is still necessary to buy postage for mail in ballots in the general election.
- 27:    <http://about.usps.com/election-mail/election-mail-dmm-sheet.pdf>
- 28:    So, mailing addresses, Oregon, GOTV messages, stamps.


== Topic ==

- 29:    I’m with you here except for Oregon. Why Oregon?
- 30:    All mail state.
- 31:    So there is no selection into who is mailing and who is going in person.


== Topic ==

- 32:    Wow. I didn’t know that.
- 33:    Address from voting files?
- 34:    *addresses


== Topic ==

- 35:    Yup. Those are going to be HELLA high fidelity because they are an all mail state.
- 36:    Additional treatment condition: mailing 2x the postage that is necessary, building in an explicit spillover on co-residents.
- 37:    That would be dope. No one has done this in the past? Seems like something Green/Gerber would have stumbled on at some point. If not, it is pretty sweet. No possible harms that I can imagine.
- 42:    Yeah, that’s a short review. It is a shame that one of us doesn’t know Green, Gerber, or Sinclair. They would probably know.


== Topic ==

- 38:    I dunno. Seems so low hanging. SO low hanging.
- 39:    Here’s the closest I can find. From 2015. A natural experiment in Switzerland.
- 40:    <http://www.econstor.eu/bitstream/10419/123257/1/cesifo_wp5617.pdf>
- 41:    Doesn’t have any citations to work that have manipulated postage. But, it doesn’t look exactly exhaustive.
- 43:    I know both Green and Sinclair well enough that they would answer my emails.
- 44:    Ah, I shouldn’t have assumed. Might be something to run by them.
- 45:    <http://bmchealthservres.biomedcentral.com/articles/10.1186/1472-6963-4-16>
- 46:    But, I should be writing a dissertation...


== Topic ==

- 47:    You and me both...
- 48:    Still, the simplicity is attractive. Plus, I always wanted to do a GOTV experiment
- 49:    But yeah - dissertation
- 50:    Difference is that my defense is in 14 days... and I’ve got chapters to go still.
- 51:    Fair point.
- 52:    Wow; that study you linked to is some BULLSHIT.
- 53:    (Congrats on being so close!)
- 54:    Yeah
- 55:    I’ll take your congrats when it is in the rearview mirror. Until then, I’m “working” hard.
- 56:    Gotcha
- 57:    Heh - <http://weblogs.sun-sentinel.com/news/politics/broward/blog/2012/03/is_a_postage_stamp_just_like_a_1.html>
- 58:    Sweet
- 60:    a really interesting piece on design of experiments, courtesy of devesh: <https://www.povertyactionlab.org/sites/default/files/publications/20160401handbookExperimentalDesign.pdf>
- 61:    This looks awesome! Thanks, Micah!


== Topic ==

- 62:    Hey <@U16RAECF5> I’m working on that Pol Behavior submission today, are you around for questions?
- 63:    <@U16RLTH3N>: yepski. give me a call whenevs.


== Topic ==

- 64:    Aight, or we can iterate in here a little bit to support the changes that I’m making in the file in Dropbox. You’re probably seeing it ping around right now.
- 65:    I’ll put this talk in <#C1H66683U> for today, and then we can just remove it tomorrow when we submit.


== Topic ==

- 66:    Mute this topic bitch
- 68:    Im sorry. It's the sudafed


== Topic ==

- 69:    Lookin’ a bit like Ahab there.
- 70:    Sudafed*:wine_glass:
- 71:    I'm working on it
- 72:    Preparin’ for those Ann Arbor winters, eh?
- 73:    My razors are packed already
- 74:    Not sure if a razor is going to make it through that wicket...
- 75:    It is pretty impressive.


== Topic ==

- 76:    2.5 months Apperantly
- 77:    Alex!!!!
- 78:    MR_PINK and I are harassing MR_WHITE on another channel. It's Alex's fault
- 79:    <@U16RLTH3N>: !!!!!!!!!!
- 80:    Clearly.


== Topic ==

- 81:    I like this app
- 82:    <@U16TY5M6F>: How did that USAID boondoggle in Haiti end up going for you?
- 83:    And, um... congratulations to each of you for discovering the effect of penis names on responses to requests for information. Wang Dong!


== Topic ==

- 84:    Thanks Alex. We think that this finding makes several contributions and has obvious familial implications. That is, parents shouldn't name their kid Richard.
- 85:    you guys are actually fucked in the head. here's something of value: <http://stanford.edu/~dbroock/stanford-berkeley-opinion-survey/Stanford-Berkeley_Survey_of_Public_Opinion/Stanford-Berkeley_Opinion_Survey.html>
- 86:    People – can I please have the basic citation on parental influence? Is it Converse? Please excavation point?
- 87:    Campbell, Converse, Miller, and Stokes. 1960. The American voter. New York: John Wiley &amp; Sons, Inc.
- 88:    Haiti project is humming right along
- 89:    I’m jealous. <@U16RAECF5> and I have nothing but *hard* sandbagging by our Mission contacts...
- 90:    That seems the norm
- 91:    <@U16TY5M6F>: can we use any of this data to build the IRT ranking model?
- 92:    Probably. What's the underlying concept?
- 93:    <@U1CCHNQ3V>: Where you at bro? In SD this week, so is Chris, so is Micah. Sup with it?
- 94:    <@U16RLTH3N>: I need to download the app on my phone so I get these messages instantly. But I'm gonna get some drinks with <@U16RAECF5>
- 95:    Hey <@U16RAECF5> and <@U1CCHNQ3V>: Try this out for a recommendation when you get your beers. The story about how it was made is linked, and the recommender is at the bottom of the linked page. <http://willnetsky.github.io/Beer-Recommender/>
- 96:    It’s a pretty simple recommender -- seems to just key on most descriptive word. This is a little tough, because while there are a lot of nerds who rate beer, there are a lot of bros who know like 4 beer words: “dank”, “fruit”, “sour”, ... . And, this sort of mainlines the recommendations. I think a little filtering would help clean this up.
- 97:    Also, some rankings.
- 98:    Checked it out. I'm into it.
- 99:    Two syllabi that my be of interest: Matt Blackwell: <http://www.mattblackwell.org/files/teaching/gov2002-15f-syllabus.pdf> and Danny Hidalgo: <http://www.mit.edu/~dhidalgo/syllabi/17_802_syll2014.pdf>. MR_WHITE pointed out that Hidalgo is more interested in observational data. Nice bibliography between the two.
- 100:    <@U16RY7PR6>: Can I share the PSU irb material --- specifically the short part where you dared PSU to not grant exempt status --- with <@U16RAECF5> and <@U1CCHNQ3V>? <@U1CCHNQ3V> is putting together an encouragement design intervention right now.
- 101:    I bet he’ll share back his completed documents, too?
- 102:    <@U16RY7PR6>: <@U16RLTH3N> <@U16RAECF5> and I would be happy to share the completed documents
- 103:    <@U16RLTH3N>: <@U16RAECF5> <@U1CCHNQ3V> Totally! I have a folder full of IRBs and you are welcome to any of them. I think that one that MR_WHITE has probably contains the sharpest language.
- 105:    <@U1CCHNQ3V>: I just uploaded the doc I’m sending to Berkelye.
- 106:    On helping people understand the value of experimental research: I've been thinking a lot about the push back that MR_WHITE and I got in designing a useful intervention. Today again I was talking to someone who has the opportunity to learn about a program's effectiveness, but instead is waving their hands talking nonsense. Has anyone seen a good attempt at explaining the value of experimental research to a non-technical audience?


== Topic ==
- 107:    <@U16RAECF5>: Unfortunately, no. I looked for something like this when I was reviewing a proposal for the National Opinion Research Center but couldn’t find anything like it. The proposed intervention was sooooooooooooooooo bad.
- 108:    <@U16RAECF5>: Also, I’m working out responses to your emails. One of them is almost perfectly in line with something that I just spoke with Matt Golder about earlier today. It was like you read my mind. Spooky.
- 109:    :grinning:
- 110:    squad! anyone interested in sharing a room in Philly?
- 111:    <@U16RAECF5>: Just got your voicemail, I was in a faculty meeting. Holler at me if you’re otherwise undisposed.
- 112:    This study is that _straight_ dope. But I want a <@U16TY5M6F> viewpoint on their model. In particular, they’re interpreting their item difficulty parameters in a _really_ literal sense (literally the probability that a traffic stop will occur). I’d love to read closely and talk with anyone who has also read it closely, though I know that you are all probably at APSA right now.
- 113:    <https://5harad.com/papers/threshold-test.pdf>
- 114:    Here’s the git repo to their work.
- 115:    <https://github.com/5harad/threshold-test>
- 116:    holy crap. this shit is good. I'd also be really interested to hear Chris's take
- 117:    In particular, the core of their result hinges on a literal interpretation of the item-difficulty parameters that they estimate. I’m not deep enough into this type of model to know if that is warrented.
- 118:    *warranted.
- 119:    I’m bringing it to the central list... because those fools in <#C16S81202|bureaucrats> weren’t paying attention!
- 120:    I’ve got a three way interaction that I’ve got to interpret -- two conditioning factors and a treatment -- and there is no way that that journal I’m sending this to (California Journal of Politics and Policy) is going to let me get away with that.
- 121:    So, I’ve got to simplify the presentation somehow. Here was my thought: just present treatment effects (that is the first-difference on the treatment factor), in a `2x3` table where the dimensions on the table are the conditioning factors (one which has two levels and one which has three levels).
- 122:    The models that go into these estimates are the following: ``` m1 = glm(yvar ~ treatment, family = “binomial”) # this is going to be in black m2 = glm(yvar ~ treatment * structural, family = “binomial”) # in grey column m3 = glm(yvar ~ treatment * realized, family = “binomial”) # in grey row m4 = glm(yvar ~ treatment * realized * structural, family = “binomial”) # internal cells ```
- 124:    <@U16RY7PR6> <@U16RLTH3N> <@U16S9N0LE> - so do we know of anyone who has data on the race of state leg.s? If not, how about the idea of using the facial recognition software tools we were looking at earlier to pull legislator race from publicly available pictures (FB profiles, pics on state web pages, etc.)?
- 125:    <@U16RAECF5> We could perhaps do that. Why state leg.s? I wonder if Adam (<http://adamdynes.com/>) might have info on municipal officials from his survey.
- 126:    <@U16RY7PR6> unless I'm mistaken there is a very low cost follow-on paper to our state legislator experiment in which we determine whether the race of state legislators impacts response rates.
- 127:    <@U16RAECF5> Gotcha. I would agree with that. I wonder what the state of the art is with name recognition software - since we already have the names of all the representatives. Or maybe we just MTurk the whole thing. We might be able to get urls for individual legislators from Sunlight Foundation. We could then ask MTurkers to load the pages and identify the representative’s race. Have each MTurker do each legislator at least once. Some back of the envelope calculations suggest that it would take around 250 hours to identify each one once this way. At 8 an hour, that is 2,000 plus Amazon fees. Of course, that is only for one coder.
- 128:    ok. i'm going to look into bringing someone on who might take care of these tasks. will get back to the group when I hear.
- 129:    The name software is pretty good these days, but we can know (by querying @nk in the the other channel) where it is specifically. He was on the team at IBM that wrote some of the name \rightarrow ethnicity software that IBM uses.
- 130:    Anyone have 2 minutes to talk about blocking and matching as a way to get at a heterogeneous treatment effect. I’m spinning my wheels now.
- 131:    OK - Jason S., new in Pol. Sci. at UGA, formerly at Berkeley, informs me that his facial recognition tool is ready to go, and could turn profile or other photos into an estimate of the race of state leg.s, and also a distance metric relative to a racial category. I think this would be a very straightforward, solid publication. I'll be meeting with him in a couple of weeks to talk through the specifics. In the meantime, if folks on the team could think about how we might get the photos together, that would be helpful.
- 132:    Here is something for the Congress, which we probably already knew existed? <https://www.gpo.gov/fdsys/browse/collection.action?collectionCode=GPO&amp;browsePath=Congressional+Pictorial+Directory>
- 134:    I’m asking my research librarian if he knows of other such resources. One possibility is the Congressional YellowBook.
- 135:    <@U16RAECF5>: You want to change our legal status to domestic partner so we can both apply at UT? That way one of us can get the spouse hire for the other?
- 136:    I do.
- 137:    Ok. But I cook better than I wash dishes, just so we know what the trade-off is.
- 138:    IIA. Btw, I think we do know about the photobook bc. some hngers were doing a project. The win here would be to get race for state leg.s, bc. there is a really valuable observational part. We can wrap that into the secondary analysis of the experiment, and together with the data and the tool, we have a fucking phatty pub.


== Topic ==
- 139:    I’ll let you know what is out there when my librarian gets back with me. If Leadership Directories has put it together for us already, it would be _the_ dope.
- 140:    (BTW: I don’t know what IIA is...)
- 141:    Also, ask and you shall receive. I bring forth the data, or at least a demonstration that we can has the data.
- 144:    The question I continue to have is, what we’re pointing this variable at. We can’t assess electoral consequences of this unless we undertake the _bonkers_ task of finding a standardized picture of every candidate for office that lost.
- 145:    That shit jus aint gonna happen.
- 146:    So, we’re left with a bunch of unobserved selection into office, then a classifier that tells us something that we might already know (since we have that data series from these Quorum folks), and ...
- 147:    OK. first response, there is a kid at Berkely who has put something together: <http://www.christiandphillips.com/research-1/> From his website - "...new data containing district and candidate demographic information for every state legislative general election from 1996-2015". So we would be generating a competing data set, using a different approach. <@U16RLTH3N>, the answer to your question is very simple. This is an HTE that people care about. Period. That's what gets published in pol sci journals. If we don't do this follow up, somebody else will.
- 148:    Do we know how Christian sourced his data? Is there benefit to be had in a dataset (just as a dataset) that is produced in a different fashion, that covers 10% of an existing data set? To me, the data _qua_ data contribution here feels a little slender, especially if someone else already has it. _Adding_ the skin-tone based racial assessment makes it a bit more sexy, but I don’t think it overcomes the hurdle that this fellow has the drop on us.
- 149:    Having the data for our own purposes, to test the HTE, to me feels like a good justification. And I think you’re right that we should look at this either in this paper, or in a followup paper to this experiment.
- 150:    Does anybody have an in either at Pew or the NCSL? I wonder because they’ve published a _Stateline_ series, which at least has the ethnicity data that MR_BROWN and MR_ORANGE were thinking about. I’ve been warned that if I scrape the data from the group that I had posted about last week, that the group would shut down campus access and I would be persona non grata.
- 151:    <@U16RY7PR6> and <@U16TY5M6F> I’ll be in A2 Monday October 3. Let me know if you’re available and we can work on some of this boondoggle in person again.
- 152:    <@U16RLTH3N> I’m available all day except from 12-3. It’d be great to get together.
- 153:    Woot! Maybe in the morning? I haven’t been on campus in Ann Arbor in a while...
- 154:    Totally! Do you have a place to stay?
- 155:    <!channel>: One of my co-authors is building a topic classifier that is functioning on Slack data. I want to export this and give it to the student/co-author.
- 156:    Would this make you sad? Would this violate your rights? Would this give away trade secrets?


[[2, 4, 5, 6, 7, 8, 11, 12, 14, 15, 16, 19], [17, 18, 20], [23, 24, 25, 26, 27, 28], [29, 30, 31], [32, 33, 34], [35, 36, 37, 42], [38, 39, 40, 41, 43, 44, 45], [47, 48, 49, 50, 51, 52, 53, 54, 55, 56], [62, 63], [64, 65], [66, 68], [69, 70, 71, 72, 73], [76, 77, 78, 79, 80], [81, 82, 83], [84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97], [107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 124, 125, 126, 127, 128, 129, 130, 131, 132, 134], [139, 140, 141, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154]]
