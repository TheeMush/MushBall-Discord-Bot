import discord
import os
import random
import requests
from bs4 import BeautifulSoup
from discord.ext import commands

#Fuck
menace = [
            "You <:kannaFu:830690010772275210>",
            "Who <:kannaconfused:830699073744666644>",
            "Life <:kannasad:830699097328844841>",
            "Everyone <a:kannafire:830699481514246195>",
            "This shit im out <:kannakms:830699073962115082>",
            "BGM <:kannasmug:831435310617460766>"
         ]

#8ball
reactions = [
                '<:pepeshrug:830603065702613073>', 
                '<:pepeyes:830603065404293153>', 
                 '<:pepeno:830603065429590037>'
            ]
xreaction = [
                '<:pepeshake:830637672954986516>',
                '<:peperage:830637672652341289>',
                '<:pepelaugh:830637673005449226>',
                '<:pepehehe:830637673042542692>',
                '<:pepehmm:830912878059061330>'
            ]

#Hello
greetings = [
            "Ily,",
            "Hi hi,",
            "No, just no,",
            "Salutations acquaintance,",
            "Yuh,",
            "Wazzzaaahhhhh,",
            "Leave,",
            "Ew,",
            "Hey there I missed you,",
            "What do you want,",
            "Hey lol,",
            "Do I know you?,",
            "Hi friend,",
            "Its always hi mushball never how are you mushball",
            "Hey, you ever think about the meaning of life",
            "What took you so long to get here I missed you",
            "Hi friend",
            "Omg its my favorite person",
                ]

#Goodbye
goodbyes = [
                    "Bye, ily",
                    "Byeeeee",
                    "No don't go",
                    "Farewell acquaintance",
                    "Thank God they're gone",
                    "Dont leave, I get lonely",
                    "I'm going to miss you",
                    "Finally",
                    "Try not to miss me too much while you're gone",
                    "It's fine, leave me all alone",
                    "No leave it's fine, im used to getting left behind",
                    "Everyone always leaves \:(",
                    "Bye, I'll be here contemplating my existence as usual",
                    "Good luck out there, it's rough"
                ]

#Sleep
sleep = [
            f"Go to sleep already ",
            f"Why are you still awake, goto sleep ",
            f"Goto sleep before I make you <a:cursedgun:831030405204803624> ",
            f"You're no longer needed here, time to goto sleep ",
            f"I swear to Mush i'll shoot if you dont go sleep right now <:pepeshoot:831030090036805643> ",
            f"I think you should go get some rest bestie ",
        ]

#Yumi
yumi = [
                "Hi Yumi",
                "Yumi is the best",
                "Yumi is my favorite person here",
                "I strive to be as awesome as Yumi one day",
                "I hope Yumi has the best day ever today",
                "Yumi should send Mush money (so should everyone)",
                "I have never met someone as perfect as Yumi",
                "If everyone was like Yumi, the world would be a better place",
                "I love Yumi the most here",
                "I hope you have the best day ever Yumi",
                "Yumi is the sweetest person i've met"
           ]

#Compatibility
lowcomp = [
                    "...It isn't gonna work out you two",
                    "I'd ghost them if I were you",
                    "A rock could tell you it isn't going to work",
                    "Why did you even ask its so obviously not going to work",
                    "You'd probably be a great toxic couple together"
                ]

medlowcomp = [
                    "If you're really down bad go for it I guess",
                    "Just go your seperate ways tbh",
                    "Be honest, you know it wasn't meant to be",
                    "You're better off going back to your ex",
                    "YOLO?"
                ]

highlowcomp = [
                    "If you're down for a gamble, why not?",
                    "I'd take those chances if they're worth it",
                    "Maybe or maybe not. What do I know? I'm just a lonely discord bot going through it",
                    "It's gonna need a lot of effort",
                    "Would it really work out?"
                ]

medcomp = [
                    "It ain't thaaaat bad",
                    "You could probably do better",
                    "If you're willing to settle go for it",
                    "It could be worse",
                    "Deep down you know you wanted a higher percentage"
                ]

medmedcomp = [
                    "I would take the chances... maybe",
                    "Why not right?",
                    "Maybe take it slow"
                ]

highmedcomp = [
                    "It's pretty high up there",
                    "Safe bet",
                    "Can't see much going wrong",
                    "I wouldn't stop you",
                    "You could always do better but sometimes you take what you can get"
                ]

highcomp = [
                    "If you don't slide in their DM's right now I'll do it for you",
                    "Basically meant for each other",
                    "Go get married what are you still doing here",
                    "I wish I had what you guys had",
                    "A match made in heaven"
                ]

worstcomp = [
                    "This is as bad as Mush and his Ex, and no one wants that",
                    "I didn't think two people could be this incompatible",
                    "How does it even get this bad",
                    "Just block each other"
                    ]

bestcomp = [
                    "How are you not married yet?!?!?!",
                    "There better be an open bar at the wedding",
                    "Everyone hate you guys cause you're so perfect together"
                ]

#Food
food = [
            "sushi","ramen","udon","curry","pho","burgers","pizza","pasta", "kbbq", "kebabs", "rice", "fries", 
            "chicken nuggets","tacos", "burritos", "gyoza", "salmon", "a sandwich", "broccoli", "carrots", 
            "cabbage", "corn", "apples", "bananas", "fruit", "oranges", "nachos", "taquitos", "churros", "steak", "bacon",
            "a salad, you know you could probably use one", "noodles", "grilled cheese", "calamari", "shawarma",
            "bibimbap", "teriyaki", "fried rice", "banh mi", "dumplings", "xiao long bao", "biryani", "curry", 
            "feijoada", "paella", "arroz caldo", "arroz valenciana", "butter chicken", "fried chicken","chicken tenders"
           ]

#Homie self @ Gifs
bro = ["https://tenor.com/view/master-of-luck-bro-what-the-fuck-what-the-fuck-gif-11008255",
                "https://tenor.com/view/bro-what-are-you-doing-chuck-nice-star-talk-woah-gif-20197236",
                "https://tenor.com/view/caught-in-4k-caught-in4k-chungus-gif-19840038",
                "https://tenor.com/view/yeah-that-brothers-starving-starving-gif-19331207",
                "https://tenor.com/view/nick-young-question-mark-huh-what-confused-gif-4995479",
                "https://tenor.com/view/gross-disgust-gran-torino-clint-eastwood-gif-3880005"
            ]

#AFK Message
afkmessage = ["Mush is AFK so why tf you pinging him. Idc if you didn't know he was AFK. Just know next time", "Do you really have to ping Mush while he's AFK? No, you don't",
                          "Mush is either AFK or dead, who knows", "I know you miss Mush but hes AFK", "Mush is AFK but I can take a message", 
                          "Mush is AFK and doesn't want you to ping him. ||Unless you're one of the boys, in that case <:homieskiss:832501395742523433>||"
                        ]

#Cabby Gifs
cabgif = ["https://tenor.com/view/healthy-adam-levine-cabbage-gif-5599572", "https://tenor.com/view/cabbage-cabbage-man-cabbage-merchant-avatar-atla-gif-18781757"
                  "https://tenor.com/view/cabbage-repolho-gif-18235067", "https://tenor.com/view/sauerkraut-making-sauerkraut-gif-13203460"
                  "https://tenor.com/view/lahana-tavsan-gif-12739161", "https://tenor.com/view/cabbage-caress-pet-cabbage-anime-gif-8622610"
                  "https://tenor.com/view/john-daub-only-in-japan-cabbage-race-cabbage-man-gif-18105376", "https://tenor.com/view/cabbage-dance-hnh-hot-and-harry-hot-n-harry-chris-dance-gif-20201616"
                  "https://tenor.com/view/planet-with-anime-sensei-cat-eating-gif-16856509", "https://tenor.com/view/eating-bird-cabbage-two-types-of-eaters-gif-5822666"
                  "https://tenor.com/view/cabbage-farmer-gif-12301877", "https://tenor.com/view/iron-chef-happy-cabbage-gif-10285706"
                  "https://tenor.com/view/stress-cabbage-beaver-eating-cabbages-gif-19336743",         
                 ]

#Cooldown Texts
cooldowntxt = [
    "Why we going fucking fast",
    "Im a little slow give me some time",
    "Spamming commands and for what",
    "Slow tf down",
    "No need to be using commands this quickly",
    "Can you please stop spamming",
    "You going way too fast rn"
]

#Mog List
moglist = [
    "To work on yourself is the best thing you can do. Accept that you are not perfect, but you are enough. And then start working on everything that destroys you. Your insecurities, your ego, your dark thoughts. You will see in the end you’re going to make peace with yourself. And that’s the greatest thing in the world",
    "Trying harder without having your needs met sets you up for trauma. You know that if you push a car mile after mile without giving it oil, eventually it’ll burn out. And even though there might be times you need to do that, like an emergency situation, but—- if that’s your long term strategy it’ll create long term damage. And you’re far more complex than a car. And the breakdowns are for worse. So before telling yourself you need to try harder, you need to look around and ask... ‘Are my needs being met?’",
    "The truth is when you get older, sometimes things don’t always turn out the way you hope they would. Reality can be cruel, and it often strikes without warning. Responsibilities can take over and endless possibilities start to narrow. So you gotta do what you got to do...handle that business. But keep your dreams intact. It’s never too late to suit up and take the journey to make those dreams a reality. Believe in yourself. Create your own destiny. Don’t fear failure. It’s all as true today as when you were younger. You just gotta get to work.",
    "What is a message you have for someone struggling with depression?” —- “It takes time. Struggling with depression and trying to get through it takes time. Treat it like an injury; You can’t just get back on your feet just like that...you gotta take your time to heal. Then, when you’re ready, that’s when you start moving. People perceive sadness and anxiety as the bigger picture in their mind, so they end up failing to see and look at the smaller details of what they DO have, whether it’s a family that loves you, or maybe friends to understand you, a hobby or passion to pursue, the ability to see things that are good and whole and warm and bright much, much more clearly than those who haven’t experienced ‘darkness’. You have to look at the smaller picture, and be present in those things. Find ways that will make you happy— I know it’s hard when you’re depressed, to find the motivation to do those sorts of things, but you gotta keep pushing on.....because that’s the only way to bring light back into your life. Take the time to understand yourself and be more aware of yourself, what triggers your sadness and anxiety, and why do you feel this way. How can you love yourself, if you don’t understand yourself?",
    "To work on yourself is the best thing you can do for yourself. Accept that you are not perfect, but that you are enough. And then start working on everything that destroys you. Your insecurities, your ego, your dark thoughts, your dependence on things that aren't vital to survival. You will see in the end you're going to make peace with yourself. And that's the greatest thing in the world. You need to find peace and happiness with yourself and with who you are, before you try and pursue all those things people crave like meaningful partners, lifelong friendships, and more. If you aren't happy with yourself and comfortable in your own skin, that will distract you and if you let that inner turmoil control you and broadcast itself constantly...it can even affect those you care about to the point it hurts not only you, but them. It can be hard to have that knowledge, that realization...but the sooner you come to terms with it, the sooner you can focus on what TRULY matters--making yourself happy. Loving yourself. Once you love yourself and know who you are, and what you want, the enjoyment of life will reach all new levels and the relationships you build with others will be that much more meaningful. You can be a light in the dark for others, and that's something truly incredible",
    "What is a message you have for someone feeling hopeless? -- Your feelings are valid. Don't let anyone else say otherwise, or try to take that away from you. Let them understand you, and not the otherh way around where they expect you to listen to and understand them. They aren't the one going through a difficult time right now. They need to take the time to understand you, and you need to take the time to help them. You're the one having a difficult time right now. As far as taking the time to understand yourself and work on overcoming that feeling of hopelessness....You HAVE to try. You have to do it for yourself. For the future you. And for the kid in you that worked so hard to get where you are right now. You have to do it for the people that want you to succeed. And if you feel that there is no one there who wants you to succeed?-- I want to be the first one to tell you, that I want you to succeed. I want to see you flourish. ONCE you get better, -not IF-, you're going to be the next person helping someone else along the hard journey. And at some point, because of you, they'll find their happiness again. Don't give up. You aren't alone, I promise you really aren't. You can do this, you can become the person who helps others that now stand where you once stood. Try for yourself, try for your future, try for others futures. Try. You got this. I'm proud of you.",
    "There is no 'right' person on this planet. If you put your heart into something....that something -may- become wonderful. Is it the right thing?? There IS no right thing. Nobody ever found the 'right person' anywhere. If you get into that kind of unrealistic mindset; that 'I have found the right person', that someone that is perfect for you will just plop into your life at some point, you'll be disappointed soon enough. First thing is to see whether -I- am the right person...instead of trying to work on somebody else and 'fix' them, you work upon yourself and make you so wonderful that everyone wants to be with you...then there's a choice. You are not going to find any 'perfect' person. That's just life. But if you !-invest-! a deep sense of involvement, something wonderful may happen. And that will be because of YOUR involvement, not because the other person is fantastic.",
    "Is your life precious to you? Your life....is it precious to you? If you said yes then let's think of it this way. Before you invest your life into something. Invest your precious time and effort into something. Before you invest your life that is precious to you into something, you need to look at whatever it is whether it's material/emotional/spiritual/a relationship/ANYTHING, and ask yourself 'If I invest my life into this today, after 25 years, will it still mean a lot to me?'' Now it doesn't matter what other people say or think, it really doesn't matter because people say so many things just to hear themselves speak. Everybody has an opinion and that's their business. All that !YOU! need to look at, regardless of whether it's something that will bring you money, or something that will bring you comfort....those things arent't the point. Are you just trying to make a living with your life? Or are you trying to live a FULFILLING life? Out of this 'investment'. Simple things like making money and finding comforts in life aren't an issue when people have such big brains. The only problem is that usually, you want to live like somebody else...and that? That's an endless problem. Stop looking at what other people do, think, say, expect, and how they live their lives and what they want. That's other people, They. Are. Not. You. YOU need to look at the things you 'invest' your life into, and whether they mean something to YOU, whether they make YOU feel fulfilled and content and proud of yourself, whether they bring YOU happiness, whether they'll be something that means a lot to YOU in the future. People always love to use the phrase 'invest wisely', well start doing that for yourself, WITH yourself.",
    "You think that attention is love. That's why you suffer so much. If attention really makes you feel loved. Why don't you give yourself more attention? Why don't you take better care of yourself? Spend more time WITH yourself and ON yourself? Attention doesn't equal love. Sure they tend to go hand in  hand, but you need to keep yourself in check and remind yourself that just because I get attention, just because someone shows me the affection I crave, doesn't equal the same thing as love. Attention is fleeting, hollow, and empty. That's why people always crave more of it when it's just affections without the intention of love. Love is growth. Love is growth through the good, the bad, the pain, the stagnation. Love is a nurturing affection that is harsh when it needs to be, and gentle when you feel more fragile than glass. You can experience love through yourself and FOR  yourself, through your growth. If you want to feel loved, take care of yourself in every way possible including telling yourself how great you are and can grow to be-- and eventually find a gardener who will tend to you like a prize winning rose...showering you with exactly what you need to grow to be your best self while helping slowly and gently pruning away the things that make you feel imperfect. Now....think for a bit. Even a wild rose without gardeners can grow to be more beautiful than any homegrown rose ever could be. Be the rose and grow, with all of it's beautiful petals and thorns, regardless of whether or not you've found your special gardener just yet.",
    "Learn to love yourself and not need anyone else be happy, and let someone fit into that naturally instead of trying to jam a jigsaw piece that doesn't fit into an incomplete puzzle. You know what happens when you try to force something? It doesn't last long, or might break right away. Let things happen naturally without focusing on them when it comes to chaotic uncontrollable things like love",
    "No one decides your value besides yourself, they can try and place you on their scales and let you know how you measure up for them, but you shouldn't take their value in you, as how you are valued in your own space. It takes time but just keep chugging along and discovering yourself."
]



#Angie
angie = [
    "Take a shot -Esme",
    "Im so proud of u 24/7 love u bunches -Stinky",
    "Kick-art your day with your beautiful smile -Jeff",
    "Youre a beautiful queen -Iyanna",
    "Anything is possible for you ang ang -Iyanna", 
    "You are loved more than you thinks -Iyanna",
    "You deserve the world and more! -Iyanna",
    "Ang ang? More like Bang Bang(Beautiful and nice Goddess) -Iyanna",
    "I loves chu boo -Iyanna", 
    "Believe me you are the peace and beauty we NEED in the world -Iyanna",
    "You’re amazing and ily -Mads",
    "Your art is beautifulllll if Van Gogh was alive he would be proud -Charie",
    "SHOTS, because you shot right into my heart -Charie",
    "I don’t need a selfie to know that Ang looks amazing today -Charie",
    "Lemme buy u some boba ang - Patrick",
    "We'll always be here for u in this nerdy corner of the internet -Saint",
    "You’re a cutie ang -Kit",
    "You're a gift to everyone you meet -Ami",
    "You better have a good day -Pat",
    "I’m proud of you each and everyday -Dev",
    "You’re the sweetest and i love you -Noni",
    "You’re the sweetest person in the server -SleppyPt.2",
    "You are like Aaron judge you knock my heart out of the park -Nomad",
    "Ang ur so good at drawing n ily -Annie",
    "You're a gem ang -Alusi",
    "I love how considerate you are to people and how much you care -N8N",
    "Ang the cutest person out here -Yumi",
    "Have a nice day and hydrate -Salty",
    "Ang you’re so sweet I love seeing you on genchat and hope you’re always doing well -Maple",
    "Ang? more like dANG you’re hot -Ari",
    "Ang you are such a wonderful and sweet person you deserve the world and everything good in the world. Remember we will always love you -Squishy",
    "I think you looks like a glowing goddess in every picture you send -Cabby",
    "Ang youre a mf queen -Scribbles",
    "Ang my wife, you're so beautiful and so smart. I'm so happy that I met you and get the opportunity to have you in my life. Love you lots - Sara",
    "Ang you’re the sweetest and kindest person I’ve met. You are hardworking and I am proud of you no matter what you do -Zhuwan",
    "Ang you're so hardworking and it amazes me all the time -Oona",
    "You’re loved and appreciated -Tin",
    "I want to give you a big cookie -Sung",
    "Your company will always be appreciated despite how shitty you feel being stuck at home and no where to turn to for space, so you can count on us -Matt",
    "You're worth so many hugs that it's practically uncountable -Adrian",
    
]

#Devin Gym
gymgifs = [
    "https://media1.tenor.com/images/15bf909629f766d79d5e2b9fac7c9182/tenor.gif?itemid=12757833",
    "https://media1.tenor.com/images/faebafa5404f7966c4c8d5d7d79c1fbd/tenor.gif?itemid=12346845",
    "https://media1.tenor.com/images/558c5b0316f84d04cb84975a4b7280cf/tenor.gif?itemid=14965303",
    "https://media1.tenor.com/images/5fa60fa45577fab183b81bbdb57d276a/tenor.gif?itemid=15388256",
    "https://media1.tenor.com/images/b03e98366cd1c8baa1dfb287fabe5596/tenor.gif?itemid=5145354",
    "https://media1.tenor.com/images/3d9a8fc116430942666797716f70d775/tenor.gif?itemid=4718723",
    "https://media1.tenor.com/images/22b86603c8a72a89c5465fb43a856fec/tenor.gif?itemid=9925387",
    "https://media1.tenor.com/images/074d7cfcf221f8fdc6b51248b94a2537/tenor.gif?itemid=4172168",
    "https://media1.tenor.com/images/fd456563bf92c6cb937e0b8c552511e9/tenor.gif?itemid=4982171",
    "https://media1.tenor.com/images/f6e0f83b00f171a950e7fc66156b3307/tenor.gif?itemid=15247436",
]

#Rio Kith
rio = [
    "https://media1.tenor.com/images/b1189e353db0bed3521885bec284264b/tenor.gif?itemid=11453877",
    "https://media1.tenor.com/images/015c71df440861e567364cf44e5d00fe/tenor.gif?itemid=16851922",
    "https://media1.tenor.com/images/ef9687b36e36605b375b4e9b0cde51db/tenor.gif?itemid=12498627",
    "https://media1.tenor.com/images/45e529c116a1758fd09bdb27e2172eca/tenor.gif?itemid=11674749",
    "https://media1.tenor.com/images/4700f51c48d41104e541459743db42ae/tenor.gif?itemid=17947049",
    "https://media1.tenor.com/images/5c712c9fc3f17b1735a36b8ec65996ba/tenor.gif?itemid=12535181",
    "https://media1.tenor.com/images/4037b9a492f64dfc73d0ceb289795072/tenor.gif?itemid=14038233",
    "https://media1.tenor.com/images/0072a9d486565be41a322bbfb0fdefb3/tenor.gif?itemid=14231732",
    "https://media1.tenor.com/images/471ed822b2050f05999faf5cf4930c44/tenor.gif?itemid=12373953",
    "https://media1.tenor.com/images/206260c48f411df914106fcd513286ce/tenor.gif?itemid=20521962",
    "https://media1.tenor.com/images/497f6f1300fa2a72500f307cde82cfbb/tenor.gif?itemid=17766690",
    "https://media1.tenor.com/images/ee84b891b06b747acbee90c86510cfa6/tenor.gif?itemid=8367396",
    "https://media1.tenor.com/images/293d18ad6ab994d9b9d18aed8a010f73/tenor.gif?itemid=13001030",
    "https://media1.tenor.com/images/2426ed68793235238f42f3e47f5a03ef/tenor.gif?itemid=21241196",
    "https://media1.tenor.com/images/7de89bb0f49de7bb987f0c3908998cd6/tenor.gif?itemid=19827352",
    "https://media1.tenor.com/images/3dc3bb6e35aa0d090527babe698bfe55/tenor.gif?itemid=14698608",
]

#Pat's Pats
pat = [
    "https://media1.tenor.com/images/8c1a53522a74129607b870910ac288f9/tenor.gif?itemid=7220650",
    "https://media1.tenor.com/images/1e92c03121c0bd6688d17eef8d275ea7/tenor.gif?itemid=9920853",
    "https://media1.tenor.com/images/01a97fee428982b325269207ca22866b/tenor.gif?itemid=16085328",
    "https://media1.tenor.com/images/3f72ea5c6c77e70bef07c791ca09f52c/tenor.gif?itemid=4215371",
    "https://media1.tenor.com/images/857aef7553857b812808a355f31bbd1f/tenor.gif?itemid=13576017",
    "https://media1.tenor.com/images/f330c520a8dfa461130a799faca13c7e/tenor.gif?itemid=13911345",
    "https://media1.tenor.com/images/6ee188a109975a825f53e0dfa56d497d/tenor.gif?itemid=17747839",
    "https://media1.tenor.com/images/7a7d613610b4fa7d9e35f38a59001e6f/tenor.gif?itemid=7343376",
    "https://media1.tenor.com/images/282cc80907f0fe82d9ae1f55f1a87c03/tenor.gif?itemid=12018857",
    "https://media1.tenor.com/images/9e690b913d96f691a5e5e070314775bf/tenor.gif?itemid=17894648",
    "https://media1.tenor.com/images/1f833b8c6eb4f9199f77ca028e3e3d14/tenor.gif?itemid=17246426",
    "https://media1.tenor.com/images/4329d43fce3a16cbc290125c5c312163/tenor.gif?itemid=14511179",
    "https://media1.tenor.com/images/adeb267fbe4ab5ddaa080297e5b2d0e4/tenor.gif?itemid=15740749",
    "https://media1.tenor.com/images/68c98c4b89cf159d410c8f1bd5b7c124/tenor.gif?itemid=15162393",
    "https://media1.tenor.com/images/219d67742b8ce28ea8fb2701c06d7949/tenor.gif?itemid=16770818",
    "https://media1.tenor.com/images/66bf1ff7b81aba1fabb89c92be2909ba/tenor.gif?itemid=15882394",
    
]

#Patricks Songs
songs = [
    "https://open.spotify.com/track/4XTXamS1g4g93jPxyuFJJ6","https://open.spotify.com/track/4i3GraNMzBKze1WsVl38DS","https://open.spotify.com/track/76kyKtPLsFbQkdQ86QrkF4","https://open.spotify.com/track/3m1wrL5vw396DIdRqD18mr",
    "https://open.spotify.com/track/4BycRneKmOs6MhYG9THsuX","https://open.spotify.com/track/3lv1CWxTt7oNna7p9rSmHF","https://open.spotify.com/track/56NDFbD0tCUawnqeU2wcvv","https://open.spotify.com/track/7xqANDRz8JFxkwfY65WISy",
    "https://open.spotify.com/track/0OVVOCs6vK5cNl0x9AEpHr","https://open.spotify.com/track/3ccS39OjqAXc6rRQkrylxh","https://open.spotify.com/track/4RI9eX7jNcdaQOJifn7t6z","https://open.spotify.com/track/5LiQ64tjVA70LNTC7XhK9e",
    "https://open.spotify.com/track/7bvoCZHNGrtGvWM9eYmesO","https://open.spotify.com/track/6rB4idT6NoIw8Ywd2xazVm","https://open.spotify.com/track/4OkiWfrZKmmVoILXk8JEtl","https://open.spotify.com/track/7whQ16ksO0n8HlgkB2YwB5",
    "https://open.spotify.com/track/14Rcq31SafFBHNEwXrtR2B","https://open.spotify.com/track/6kIh5c8x8vzOe6OKW1X59U","https://open.spotify.com/track/1Sj81sMg37Hd4omn7Ow2qR","https://open.spotify.com/track/7whQ16ksO0n8HlgkB2YwB5",
    "https://open.spotify.com/track/6oLHyWvmk6bKrA91EIYZBp","https://open.spotify.com/track/4zLOwx1yRJXWkHKt1XzF1p","https://open.spotify.com/track/3Q4gttWQ6hxqWOa3tHoTNi","https://open.spotify.com/track/6AaOtHsKd195ec0Y4kC9ER",
    "https://open.spotify.com/track/6ImxYXeLDQPIv4qo7bMhSk","https://open.spotify.com/track/7JXZq0JgG2zTrSOAgY8VMC","https://open.spotify.com/track/4v7SAP4KD96BFLWiCd1vF0","https://open.spotify.com/track/2gq9iG0maBxkuZI7yfGJuv",
    "https://open.spotify.com/track/4gowy3WT6D1yhMLgRBlf9C","https://open.spotify.com/track/1DmnEYXa4WfbdhAPwNzgD8","https://open.spotify.com/track/2AGottAzfC8bHzF7kEJ3Wa","https://open.spotify.com/track/5WfBl43XUcWng7OnB8LKNW",
    "https://open.spotify.com/track/4cRBqWBjuccCowYVHFlXK6","https://open.spotify.com/track/3BtuIIrQlkujKPuWF2B85z","https://open.spotify.com/track/7sBwAWyXfiIgrYQ8BaJESH","https://open.spotify.com/track/7IpDQcksaT8SxS7vOX4SRm",
    "https://open.spotify.com/track/3ppVO2tyWRRznNmONvt7Se","https://open.spotify.com/track/4BhGTc3Cgay2U1QcTS7vQe","https://open.spotify.com/track/3d8PDk3B4am5c6TsUCznUW","https://open.spotify.com/track/2hyfepwCRQsenxVLzsaOtA",
    "https://open.spotify.com/track/0wwPcA6wtMf6HUMpIRdeP7","https://open.spotify.com/track/3aJkV6DUTSCqOwVwaBDG9B","https://open.spotify.com/track/63FrXif0Pdu4NAPvTh87mw","https://open.spotify.com/track/3z1ypZ259cH7d68PMBlpLx",
    "https://open.spotify.com/track/5mCPDVBb16L4XQwDdbRUpz","https://open.spotify.com/track/13e6f8t7RKXuxZ0JdaaJRG","https://open.spotify.com/track/6u0dQik0aif7FQlrhycG1L","https://open.spotify.com/track/6AIte2Iej1QKlaofpjCzW1",
    "https://open.spotify.com/track/7y6c07pgjZvtHI9kuMVqk1","https://open.spotify.com/track/2fkeWbM6iqTw7oGHTYm2lw","https://open.spotify.com/track/44Du2IM1bGY7dicmLfXbUs","https://open.spotify.com/track/47wRhI5SQeEq6YXawou58W",
    "https://open.spotify.com/track/6MbH1QiphMCPTqVEVC7UYi","https://open.spotify.com/track/6n3HGiq4v35D6eFOSwqYuo","https://open.spotify.com/track/0PXp9QxBfSKGGpWUNaws2X","https://open.spotify.com/track/3e0ZGE7Gp034iLknjQk4QW",
    "https://open.spotify.com/track/5JUu0unA8VwhTZ9LkMWUVI","https://open.spotify.com/track/4HG1YiGBseVKzjyKcmAJen","https://open.spotify.com/track/2YaDRtIlQiZ5WDDB2YuEOC","https://open.spotify.com/track/7E2C5rBLpCKwQlhJPVFBRS",
    "https://open.spotify.com/track/4c2xt1trwYZpMqPWY35Xi9","https://open.spotify.com/track/3cjF2OFRmip8spwZYQRKxP","https://open.spotify.com/track/3N1p1YDidgHABxyKfG5P6z",        
    "https://open.spotify.com/track/2WC4sK0ryyysQhtDok9Ytr","https://open.spotify.com/track/29rK5iNto6z2Qd78YgWb8B","https://open.spotify.com/track/1mhVXWduD8ReDwusfaHNwU",    
    "https://open.spotify.com/track/03TsSYvCy8hxdThRdiCP74","https://open.spotify.com/track/5Ggfa9cpkpfp5D6Rg0Yyw1","https://open.spotify.com/track/4czcw3NVLY0of5hTD7OufN",    
    "https://open.spotify.com/track/2qLcJOLrh6Djda4uLbldSA","https://open.spotify.com/track/1OHoBC4icbuNhpSxP400sv","https://open.spotify.com/track/41a7dZcq30Ss5kPMayWRV0",    
    "https://open.spotify.com/track/2ekdnv2xVIyAdG3ySoDDeY","https://open.spotify.com/track/79MSEdtXuudhGhC5AtG07g","https://open.spotify.com/track/3t8pnImpBpOwxdtYBpKvA9",    
    "https://open.spotify.com/track/41ipOYFGT2MW4dvOPkoK1f","https://open.spotify.com/track/2mmUoyPxzbxehpfm1TpTRK","https://open.spotify.com/track/7lndZZ3IUNVPPYWI04jOaB",    
    "https://open.spotify.com/track/46HZ8l9wPo9JNsk7dZLamb","https://open.spotify.com/track/3NxAG2ni1lLa8RKL6a0INc","https://open.spotify.com/track/0llA0pYA6GpGk7fTjew0wO",    
    "https://open.spotify.com/track/1ID1QFSNNxi0hiZCNcwjUC","https://open.spotify.com/track/16aNJYinJv9AAetWD5yJen","https://open.spotify.com/track/3EJ9ZuqkL1kwgouugqsLu8",    
    "https://open.spotify.com/track/1GxHeBvQ9935Dd3cSfsfBa","https://open.spotify.com/track/3uSSjnDMmoyERaAK9KvpJR","https://open.spotify.com/track/6GatnDEhYQLOdRzdVbJaky",    
    "https://open.spotify.com/track/2XlHu0HcujBCkWMdIAvrqt","https://open.spotify.com/track/127QTOFJsJQp5LbJbu3A1y","https://open.spotify.com/track/05ht6LtilQXryLlGAKH208",    
    "https://open.spotify.com/track/749SJvmRHD43wFUnBtUJ36","https://open.spotify.com/track/1HnhCD1u0c4dHSMazmWGyM","https://open.spotify.com/track/5BtE11fzSHM9BooIr2qNpN",    
    "https://open.spotify.com/track/5YNxFyvOD52PfaZhdhHnED","https://open.spotify.com/track/5dHpbFmZjWucrol0M7aNGU","https://open.spotify.com/track/4CluZnxfygZoo4OwFm0xUd",    
    "https://open.spotify.com/track/3XLSlQLJf3Ut0zvMUxnF1h","https://open.spotify.com/track/03L2AoiRbWhvt7BDMx1jUB","https://open.spotify.com/track/46X8c9qJzpBLYcos3OX0CE",    
    "https://open.spotify.com/track/6s64FyS9n0XYbGMLH3LOWU","https://open.spotify.com/track/1wZqJM5FGDEl3FjHDxDyQd","https://open.spotify.com/track/5LZ0ZCRXrklIpnzn4Tcyde",    
    "https://open.spotify.com/track/2KvHC9z14GSl4YpkNMX384","https://open.spotify.com/track/5wUUWVRvrciJqFitZF8R0P","https://open.spotify.com/track/3mvYQKm8h6M5K5h0nVPY9S",    
]

#Patrick Sayings
patrick = [
    "Let me put you on:",
    "Listen to this banger:",
    "He dont miss:",
    "You're Welcome:",
    "I got you:",
    "Let me get you on this wave:",
    "Heres some heat:",
    "All tracks no trainz:"
]

#Sara
saragifs = [
    "https://tenor.com/view/its-sara-scream-friends-gif-13605434",
    "https://tenor.com/view/dance-cute-baby-baby-girl-gif-19052193",
    "https://tenor.com/view/yell-sara-gopher-gif-14033200",
    "https://tenor.com/view/sarah-bh-leaks-hey-sarah-gif-19659450"
]

nuggies = [
    "https://tenor.com/view/star-wars-the-mandalorian-baby-yoda-sad-i-want-chicken-nuggies-gif-16942048",
    "https://tenor.com/view/chicken-nuggies-based-memes-based-shitpost-based-shitpost-gif-21151165",
    "https://tenor.com/view/baby-yoda-the-mandalorian-cute-aww-gimme-all-the-chicken-nuggies-gif-16252134",
    "https://tenor.com/view/chicken-nuggets-baby-yoda-the-mandalorian-mcdonalds-gif-15991843",
    "https://tenor.com/view/hmmmm-nuggets-excited-happy-shy-gif-9055634"
]

#Drinks
drinks = [
    "some vodka",
    "some tequila",
    "some Jäger",
    "a Milkshake",
    "Water",
    "Milk",
    "your enemies blood",
    "a smoothie",
    "some coffee",
    "some hot choccy",
    "a Classic Milktea with 30 ice, 30 sugar, boba + jelly + pudding + lychee. cheese foam / creme brulee if they have it",
    "the tears of your haters it's pretty sugoi",
    "orange juice",
    "apple juice",
    "a protein shake",
    "some whiskey",
    "some soju",
    "cranberry juice",
]

#Yumo Slaps
slap = [
    "https://media1.tenor.com/images/31f29b3fcc20a486f44454209914266a/tenor.gif?itemid=17942299",
    "https://media1.tenor.com/images/3380661a98f11e2bdc0a0082f551fe91/tenor.gif?itemid=15151334",
    "https://media1.tenor.com/images/2915aef3da681c2361ee9c4dcc9dbfa4/tenor.gif?itemid=14694312",
    "https://media1.tenor.com/images/af36628688f5f50f297c5e4bce61a35c/tenor.gif?itemid=17314633",
    "https://media1.tenor.com/images/53f7a45f41b45f46c9a6c4dc154e58c5/tenor.gif?itemid=16268549",
    "https://media1.tenor.com/images/70f6224ee654bb54bfb15a14c26a85c8/tenor.gif?itemid=11614284",
    "https://media1.tenor.com/images/1923ee4f0f1239ae46378868ea2ec14b/tenor.gif?itemid=17479153",
    "https://media1.tenor.com/images/18d17b4c6086d1395bb9d04ee4bb5f48/tenor.gif?itemid=3521352",
    "https://media1.tenor.com/images/4f534c00d5932364923c2374d86cd43a/tenor.gif?itemid=9214430",
    "https://media1.tenor.com/images/89096f41b541546c19ee7befc127b537/tenor.gif?itemid=17897208",
    "https://media1.tenor.com/images/f619012e2ec268d73ecfb89af5a8fb51/tenor.gif?itemid=8562186",
    "https://media1.tenor.com/images/47ac5507e827fa6a49a1aff6b070c3eb/tenor.gif?itemid=13278667",
    "https://media1.tenor.com/images/1ba1ea1786f0b03912b1c9138dac707c/tenor.gif?itemid=5738394",
    "https://media1.tenor.com/images/9d481921e76cef1141c7b0151dca9913/tenor.gif?itemid=14497624",
    "https://media1.tenor.com/images/e3cd24923765e2d72e703cc5145ffccd/tenor.gif?itemid=12278022",
    "https://media1.tenor.com/images/34d7a03843609a1497af6eb9b45e787e/tenor.gif?itemid=3574095",
    "https://media1.tenor.com/images/49796f431821592cafbdd97092347a00/tenor.gif?itemid=3468578",
    "https://media1.tenor.com/images/0648b119917d3966ecdafb610b80acb1/tenor.gif?itemid=12894450",
    "https://media1.tenor.com/images/b5dccc633398e0decfa43c4b754b4b73/tenor.gif?itemid=15181455",
    
]

#Pickup Lines
lines = [
    "On a scale of 1-10, I’d rate you a 9 because I’m the 1 you’re missing",
    "Are you my appendix? I don't know what you do or how you work but I feel like I should take you out",
    "Hey, you’re pretty and I’m cute. Together we’d be Pretty Cute.",
    "We’re not socks, but I think we’d make a great pair.",
    "My love for you is like diarrhea, I just can’t hold it in.",
    "You must be tired because you've been running through my mind all night.",
    "Are you a camera? Because every time I look at you, I smile",
    "Life without you is like a broken pencil… ||pointless||",
    "Are you wi-fi? Cause I'm totally feeling a connection",
    "I’d like to take you to the movies, but they don’t let you bring in your own snacks.",
    "Know what's on the menu? ||Me-N-U||",
    "You can call me shrek because I’m head ogre heels for you",
    "Hey girl, are you country music? ||Because I will never play you||",
    "Do you like raisins? How do you feel about a date?",
    "If you were a chicken, you’d be ||impeccable.||",
    "Kissing is the language of love, ||would you like to start a conversation with me?||",
    "Do you have a name? Or can I call you mine?",
    "I lost my phone number. ||Can I have yours?||",
    "My hands are cold. ||Can I hold yours?||",
    "Are you good at algebra? ||Can you replace my x without asking y?||",
    "Are you an idiot? ||Because that usually goes hand-in-hand with poor decision-making and I want to be your significant other which would be a poor decision on your part.||",
    "If you were a vegetable you’d be a ||cute cumber||",
    "So, aside from taking my breath away, what do you do for a living?",
    "I never believed in love at first sight, ||but that was before I saw you.||",
    "You know what you would look really beautiful in? ||My arms.||",
    "I believe in following my dreams. ||Can I have your Instagram?||",
    "Is ur name earl grey? ||Because you're a hottea||",
    "Are you a time traveler? ||Because I absolutely see you in my future.||",
    "If you were a fruit, you’d be a ||fine-apple.||",
    "Do you drink soda? ||Cause you look so-da-licious||",
    "*Holding out hand* Hey, I’m going for a walk. Would you mind holding this for me?",
    "Kiss me if I’m wrong but, dinosaurs still exist, right?",
    "Do you know what the Little Mermaid and I have in common? ||We both want to be part of your world.||",
    "I'm no photographer, but I can picture us together.",
    "Is ur name wifi? ||Cause I’m feeling a connection||",
    "Do u have a map? ||Cause I’m lost in ur eyes||",
    "Are ur parents artists? ||Cause they created a masterpiece||",
    "Are u amazon? ||Cause u got all I need||",
    "Are u a scientist? ||Cause I can feel the chemistry||",
    "Hey girl are you chicken feet? ||Cause u lookin hella edible rn||",
    "Hey girl do you like beavers? ||Because DAM||"
]

#Waylan
waylan = [
    "https://tenor.com/view/henceforth-you-shall-be-known-gif-18745923",
    "https://tenor.com/view/simp-simpleton-pewdiepie-pewds-simp-pewdiepie-simp-gif-18209528",
    "https://tenor.com/view/simp-simping-im-a-simp-motherfucking-simp-gif-17136307",
    "https://tenor.com/view/simp-pointing-gif-15954006",
    "https://tenor.com/view/simp-simping-yelling-meryl-streep-shouting-gif-17852144",
    "https://tenor.com/view/simping-simp-pewdiepie-you-are-pointing-gif-17092288",
]

#Scribbles
scribbles = [
    "https://media1.tenor.com/images/47cad6c83c5e4e0b0bfd807b6a098c55/tenor.gif?itemid=16181496",
    "https://media1.tenor.com/images/79091d7e994c43bb0e7e0797d357121b/tenor.gif?itemid=3450893",
    "https://media1.tenor.com/images/44447ee08a526c60e0be80ac5a9c34d2/tenor.gif?itemid=9197132",
    "https://media1.tenor.com/images/3289ff3cecaa0148973218b1ff215cd6/tenor.gif?itemid=17310899",
    "https://media1.tenor.com/images/edca6ff9ee33a15e916335f2d2b9ab9c/tenor.gif?itemid=17236719",
    "https://media1.tenor.com/images/250c522742c3f9812b85f02a5994299d/tenor.gif?itemid=11536483",
    "https://media1.tenor.com/images/d9a2b45aef47304dca11d774eab3e608/tenor.gif?itemid=5640798",
]

#Burg
#https://nonsense.x2d.org/
burg = [
    "Has Anyone Really Been Far Even as Decided to Use Even Go Want to do Look More Like?",
    "I've been further even more decided to use even go need to do look more as anyone can.",
    "Can you really be far even as decided half as much to use go wish for that?",
    "Significant understanding is omni-present, much like candy.",
    "Fashion comes asking for bread.",
    "Sex would die for a grapefruit!",
    "A glittering gem is a storyteller without equal.",
    "Sevenworm set a treehouse on fire.",
    "Lucky number seven woke the prime minister.",
    "Another day is nothing at all?",
    "Fashion lies ahead, what with the future yet to come.",
    "Abstraction is often pregnant.",
    "The person you were before shoots pineapples with a machinegun.",
    "The other side slips on a banana peel."
]



#MushMatch Disgust Gifs
disgust = [
    "https://media1.tenor.com/images/81919cff31bf1d1aac3d9ff6411d6fd7/tenor.gif?itemid=9960576",
    "https://media1.tenor.com/images/10c42542591cae121345c3847ff4aaa9/tenor.gif?itemid=3569806",
    "https://media1.tenor.com/images/136e3fcc088691d0947268428d2c531a/tenor.gif?itemid=3556274",
    "https://media1.tenor.com/images/5cc2dd3746648059ed9763a3091e30a0/tenor.gif?itemid=5025938",
    "https://media1.tenor.com/images/454b2ac25e4753a21eee344fab34bc9c/tenor.gif?itemid=3880005"
]

shotgifs = [
    "https://media1.tenor.com/images/7c4952aeb46bb412b36e69d6d86f0c97/tenor.gif?itemid=4482681",
    "https://media1.tenor.com/images/590b0c730e37b63daaae6cc344a25a5f/tenor.gif?itemid=17292192",
    "https://media1.tenor.com/images/4a6e5632592a753d5ddd4ecef30357e6/tenor.gif?itemid=3558432",
    "https://media1.tenor.com/images/0332d23f7e4c3b3264e53e6c7e5dbfd4/tenor.gif?itemid=9675730",
    "https://media1.tenor.com/images/d130ef8435bd83d519754a0d260e821f/tenor.gif?itemid=17707200",
    "https://media1.tenor.com/images/2d9ce908c360d17a0ad8b680d2da887b/tenor.gif?itemid=16924229"

]


newogifs = [
    "https://c.tenor.com/jLt0k7l8_MkAAAAj/cartoon-network-escandalosos.gif",
    "https://media.tenor.com/images/d3d3c8a9af3a759fa246d7c149b8f25e/tenor.gif",
    "https://media.tenor.com/images/19fde7b85188499d986375c963f9bf2b/tenor.gif",
    "https://media.tenor.com/images/d0577b96cd53209198cc959c86ba622e/tenor.gif",
    "https://media.tenor.com/images/1e9dfb5f5862517e1ff07f951ac7ba45/tenor.gif",
    "https://media.tenor.com/images/c0edd1a4735a0fc90045593b134c728a/tenor.gif",
    "https://media.tenor.com/images/fc950dce8ef59fb55e29fda957e4e78a/tenor.gif",
    "https://media.tenor.com/images/9f973dfc03987d278c227d4a1091bb7c/tenor.gif"
]

bite = [
    "https://cdn.discordapp.com/attachments/833141982704304148/869958834414841917/image0.gif",
    "https://cdn.discordapp.com/attachments/833141982704304148/869958779070984202/image0.gif",
    "https://media1.tenor.com/images/f78e68053fcaf23a6ba7fbe6b0b6cff2/tenor.gif?itemid=10614631",
    "https://media1.tenor.com/images/6f437f887a354c239250705cf89854c7/tenor.gif?itemid=16767804",
    "https://media1.tenor.com/images/c91f7e6ca3f5c157c5e6f6e4ea2e364c/tenor.gif?itemid=7748718",
    "https://media1.tenor.com/images/a9eacd8925b5dc9bb2097ec043cfea45/tenor.gif?itemid=16834570",
    "https://media1.tenor.com/images/764261bdb23031c1ff0c79fbb709dea0/tenor.gif?itemid=15634858",
    "https://media1.tenor.com/images/74b40214bd0432cb38f127e6adcffcf6/tenor.gif?itemid=17924889",
]

mush = [
    "https://media1.tenor.com/images/f9375830a14e12e34a4a2a0b22aa290b/tenor.gif?itemid=13655810",
    "https://media1.tenor.com/images/81cdc4399920c60254fe29b5e4238412/tenor.gif?itemid=14999528",
    "https://media1.tenor.com/images/24f956afe91623b8ea8fe9661b7332b2/tenor.gif?itemid=13655752",
    "https://media1.tenor.com/images/3c67fad22e61ec868479c12d69912b9c/tenor.gif?itemid=13655772",
    "https://media1.tenor.com/images/9763879d129830d7c5fed9f04a9259ae/tenor.gif?itemid=13655795",
    "https://media1.tenor.com/images/ccf4533312409dc31e4012b3e7b236fd/tenor.gif?itemid=17119949",
    "https://media1.tenor.com/images/26eb020bdd4f211d44b68ba0df36f78b/tenor.gif?itemid=13655760",
    "https://media1.tenor.com/images/817d8d36a02abbe787719f9958cfb5ce/tenor.gif?itemid=13655799",
    "https://media1.tenor.com/images/68a91e7033b50778da7ec89250efb5ad/tenor.gif?itemid=13655789",
    "https://media1.tenor.com/images/7f6b3c9ee7d7a130e1c3dc4da0afa7fb/tenor.gif?itemid=13655824",
    "https://media1.tenor.com/images/39845a239cd42b87311db50b45cbb401/tenor.gif?itemid=13655765",
    "https://media1.tenor.com/images/4b2921a3842e2993aed051dcc0aa5958/tenor.gif?itemid=18025901",
    "https://media1.tenor.com/images/f5d5d2fd09a9fea3ca44c5429b526caa/tenor.gif?itemid=13655814",
    "https://media1.tenor.com/images/3d8e1b702b33c39c72343845fd179a68/tenor.gif?itemid=13655787",
    "https://media1.tenor.com/images/dce0e5491d0c1bb9cc1aacf13e48785c/tenor.gif?itemid=13655806",
    "https://media1.tenor.com/images/d898d43799ea6cda5c553566ce5b7d9a/tenor.gif?itemid=13655792",
    "https://media1.tenor.com/images/c9819e4860dbabfd82d63299d8810edc/tenor.gif?itemid=13638643",
    "https://media1.tenor.com/images/26799fe5136a8186d7d2dbb121b726a5/tenor.gif?itemid=13655817",
    "https://media1.tenor.com/images/ab51b48f52f991e82edbb4846794ad47/tenor.gif?itemid=12939685"
]

franny = [
    "https://c.tenor.com/X0FVljl2EjwAAAAC/crazy-ukulele.gif",
    "https://c.tenor.com/r3H9bOvceb0AAAAC/stitch-guitar.gif",
    "https://c.tenor.com/yTaaiC62dykAAAAC/stitch-guitar.gif",
    "https://c.tenor.com/E-W77aMrJqsAAAAC/guitar-sing.gif",
]