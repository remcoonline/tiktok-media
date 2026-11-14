import sys
sys.path.insert(0, "/tmp/ailf")
from engine import WHITE, GOLD, ORANGE, SKY
from engine2 import render

PH = "nine, oh, eight... three, three, two... nine, three, three, oh"
SITE = "A-I Lead Finders dot com"
MAYA = ("Maya", "AI Lead Finders"); DAN = ("Daniel", "AI Lead Finders")

V = {}
# 2026-11-18 — realtors · CRM + pipeline setup: the spreadsheet graveyard
V["w2_lead_graveyard"] = [
    dict(scene="presenter", spk="F", say="Okay, realtors... be honest. How many leads are sitting in a spreadsheet you haven't opened since summer?", cap="Leads stuck in a spreadsheet?", p=dict(who="maya", name=MAYA, card="Old leads?")),
    dict(scene="slam", spk="M", say="Yeah... that's a lead graveyard.", p=dict(lines=["LEAD", "GRAVEYARD."], colors=[WHITE, ORANGE]), min=2.2),
    dict(scene="pipeline", spk="M", say="We set up your C-R-M and pipeline for you. Every lead gets a stage... a next step... and a follow-up.", cap="CRM + pipeline, set up for you", min=4.6, p=dict(card="Dana · Seller", title="Your pipeline")),
    dict(scene="contact", spk="F", say=f"Want us to look at yours? Call {PH}.", min=3.6, p=dict(head="Free pipeline look", sub="Book your strategy call")),
    dict(scene="slam", spk="M", say="Now... what if those old leads actually woke back up?", cap="What if they woke up?", p=dict(lines=["OLD LEADS?", "WAKE UP."], colors=[WHITE, GOLD], stagger=0.5)),
    dict(scene="sms", spk="F", say="Our A-I checks in with the contacts who opted in. Friendly, quick, and right on time.", cap="Opted-in follow-up, by text", min=4.6,
         p=dict(who="Dana · Past lead", stop=True, step=0.9, msgs=[("me", "Hi Dana, it's Sarah's assistant. Still thinking about selling this spring?"),
              ("them", "Actually, yes. We've been talking about it."), ("me", "Great! Want a quick call with Sarah Tuesday at 10?"), ("them", "Tuesday works.")])),
    dict(scene="inventory", spk="M", say="One by one, they turn into listing appointments.", cap="Back in your pipeline", min=3.6, p=dict(title="Your listing pipeline", deals=False,
         items=[("14 Oak Ave", "Appointment"), ("7 Pine St", "Listing"), ("92 Lake Dr", "Showing"), ("3 Hill Rd", "Appointment"), ("58 Main St", "Listing"), ("21 Park Pl", "Appointment")])),
    dict(scene="presenter", spk="F", say="Your leads aren't dead. They just need a system.", cap="They just need a system.", p=dict(who="maya", name=MAYA)),
    dict(scene="end", spk="F", say=f"Book your strategy call at {SITE}. Or call {PH}.", min=5.8, pad=0.8),
]
# 2026-11-19 — wholesalers · motivated seller prospecting: the holiday slowdown
V["w2_holiday_slowdown"] = [
    dict(scene="presenter", spk="M", say="Wholesalers... a lot of people slow down over the holidays. Here's why you shouldn't.", cap="Slowing down for the holidays?", p=dict(who="daniel", name=DAN, card="Holiday slowdown?")),
    dict(scene="slam", spk="M", say="They slow down. You don't.", p=dict(lines=["THEY SLOW DOWN.", "YOU DON'T."], colors=[WHITE, GOLD], stagger=0.5), min=2.4),
    dict(scene="drone", spk="F", say="A-I Lead Finders finds motivated sellers in your market... inherited homes, vacant properties, absentee owners.", cap="Motivated sellers, found for you", min=4.8,
         p=dict(tags=["Inherited", "Vacant", "Absentee owner"], title="Sellers in your market", place="MIDDLESEX COUNTY, NJ")),
    dict(scene="contact", spk="F", say=f"Want to see what's out there in your county? Call {PH}.", min=3.6, p=dict(head="See your county", sub="Book your strategy call")),
    dict(scene="slam", spk="M", say="But let's be real... a list by itself doesn't close anything.", cap="A list isn't a deal.", p=dict(lines=["A LIST", "ISN'T A DEAL."], colors=[WHITE, ORANGE])),
    dict(scene="channels", spk="F", say="So our A-I follows up. Text... voice... and it books the call for you.", cap="Follow-up that books calls", min=3.4, p=dict(words=["TEXT", "VOICE", "BOOKED"], step=0.5)),
    dict(scene="checks", spk="M", say="That's how conversations turn into assignment fees.", cap="Conversations into contracts", min=3.4,
         p=dict(title="Assignment fees", memos=["Assignment fee · 19 Ash St", "Assignment fee · 404 Grove Ave", "Assignment fee · 8 Mill Rd"])),
    dict(scene="presenter", spk="F", say="So while everybody else takes December off... your pipeline keeps moving.", cap="Your pipeline keeps moving.", p=dict(who="maya", name=MAYA, card="Keep moving")),
    dict(scene="end", spk="M", say=f"Book your strategy call at {SITE}, or call {PH}.", min=5.8, pad=0.8, p=dict(sub="Wholesalers · Investors · Realtors")),
]
# 2026-11-20 — realtors · AI voice agent: the Sunday-night sign call (couch story)
V["w2_sign_call"] = [
    dict(scene="couch", spk="F", say="Sunday night. This couple drove past your yard sign today... and they can't stop thinking about it.", cap="Sunday night. They saw your sign.", p=dict(clock="8:52 PM")),
    dict(scene="call", spk="F", say="So they call the number on the sign.", cap="They call your number…", min=2.6, p=dict(state="ring", who="Buyer · Yard sign", sub="Incoming call · 8:52 PM")),
    dict(scene="slam", spk="M", say="And you? You're at dinner with your family.", cap="You're at dinner.", p=dict(lines=["YOU'RE AT", "DINNER."], colors=[WHITE, ORANGE])),
    dict(scene="presenter", spk="M", say="That's fine. Our A-I voice agent picks up, answers their questions, and keeps them interested.", cap="AI voice agent picks up. 24/7.", p=dict(who="daniel", name=DAN, card="Answers 24/7")),
    dict(scene="contact", spk="F", say=f"Want to hear what it sounds like? Call {PH}.", min=3.6, p=dict(head="Hear it live", sub="Call and talk to our AI")),
    dict(scene="slam", spk="M", say="And here's the part you'll love...", cap="Here's the best part…", p=dict(lines=["THE BEST", "PART?"], colors=[WHITE, GOLD]), min=2.2),
    dict(scene="qualify", spk="F", say="It asks what they're looking for... and books the showing right on your calendar.", cap="Showing booked for you", min=4.2,
         p=dict(items=["Pre-approved: yes", "Wants 3 bedrooms", "Saw the sign on Elm St"], day="MONDAY", slot=1, appt="Showing · Booked by AI")),
    dict(scene="drone", spk="M", say="Every sign... every call... working for you around the clock.", cap="Every sign working for you", min=3.8,
         p=dict(tags=["Sign call", "Showing", "Offer"], title="Every sign, working", place="SCOTCH PLAINS, NJ")),
    dict(scene="presenter", spk="F", say="Go enjoy dinner. We've got the phone.", cap="Enjoy dinner. We've got it.", p=dict(who="maya", name=MAYA)),
    dict(scene="end", spk="F", say=f"Book your strategy call at {SITE}. Or call {PH}.", min=5.8, pad=0.8),
]
# 2026-11-21 — investors · AI appointment setting: deals, not dials
V["w2_deals_not_dials"] = [
    dict(scene="presenter", spk="F", say="Investors... quick one. Do you want more phone calls? Or more deals?", cap="More calls… or more deals?", p=dict(who="maya", name=MAYA, card="Investors")),
    dict(scene="slam", spk="M", say="Less dialing. More deals.", p=dict(lines=["LESS DIALING.", "MORE DEALS."], colors=[WHITE, GOLD], stagger=0.5), min=2.4),
    dict(scene="chips", spk="M", say="Our A-I finds the sellers, has the first conversation, and only books the ones who are ready to talk.", cap="Only ready sellers get booked", min=4.6,
         p=dict(title="AI appointment setting", items=[("Find", "Off-market sellers"), ("Talk", "First conversation, by AI"), ("Book", "Ready sellers only")])),
    dict(scene="contact", spk="F", say=f"Let's map it out for your market. Call {PH}.", min=3.6, p=dict(head="Let's map it out", sub="30-min strategy call")),
    dict(scene="week", spk="M", say="So... what does your calendar look like right now?", cap="What's your week look like?", min=2.6, p=dict(title="Your week", empty=True)),
    dict(scene="week", spk="F", say="Now picture it filling up with seller appointments... while you're out walking properties.", cap="Seller appointments, booked for you", min=3.6, p=dict(title="Your week", dur=2.6)),
    dict(scene="inventory", spk="M", say="Duplexes, single families, fixer-uppers... all in one pipeline.", cap="Deals in one pipeline", min=3.8, p=dict(title="Your deal pipeline",
         items=[("Duplex · Elizabeth", "New seller"), ("2-fam · Rahway", "Appointment"), ("Ranch · Edison", "Under contract"), ("Cape · Clark", "New seller"), ("Colonial · Linden", "Appointment"), ("Duplex · Union", "Under contract")])),
    dict(scene="presenter", spk="M", say="You make the offers. We'll fill the calendar.", cap="You make the offers.", p=dict(who="daniel", name=DAN, card="We fill the calendar")),
    dict(scene="end", spk="M", say=f"Book your strategy call at {SITE}, or call {PH}.", min=5.8, pad=0.8, p=dict(sub="Investors · Buy-and-hold · Flippers")),
]
# 2026-11-22 — realtors + wholesalers · done-for-you ads and outreach (meeting story)
V["w2_ads_while_you_work"] = [
    dict(scene="meeting", spk="M", say="You're sitting with a client... and meanwhile, your ad just brought in a new lead.", cap="You're busy. A new lead comes in.", p=dict(state="ring", title="New lead · Your ad", sub="Seller · Linden, NJ")),
    dict(scene="meeting", spk="M", say="Who's following up? Not you. You're busy.", cap="Who's following up?", p=dict(state="missed", title="New lead · Waiting", sub="No reply yet · 2:15 PM")),
    dict(scene="presenter", spk="F", say="That's where we come in. We run your ads and outreach... and our A-I follows up with every lead.", cap="Ads + outreach, done for you", p=dict(who="maya", name=MAYA, card="Done for you")),
    dict(scene="channels", spk="M", say="Ads. Text. Voice. Email.", cap="Ads, text, voice, email", min=2.8, p=dict(words=["ADS", "TEXT", "VOICE", "EMAIL"], step=0.4)),
    dict(scene="contact", spk="F", say=f"Want us to run it for you? Call {PH}.", min=3.6, p=dict(head="We run it for you", sub="Book your strategy call")),
    dict(scene="slam", spk="M", say="So here's how it works now. You close... we keep it full.", cap="You close. We keep it full.", p=dict(lines=["YOU CLOSE.", "WE FILL IT."], colors=[WHITE, GOLD], stagger=0.5)),
    dict(scene="drone", spk="F", say="Sellers, buyers, investors... showing up from your own market.", cap="Leads from your own market", min=3.8,
         p=dict(tags=["New seller", "Buyer lead", "Investor"], title="Your market, working", place="UNION COUNTY, NJ")),
    dict(scene="checks", spk="M", say="Commissions... assignment fees... whatever your business runs on.", cap="Commissions or assignment fees", min=3.6),
    dict(scene="presenter", spk="M", say="Realtor or wholesaler... let us handle the marketing.", cap="Let us handle the marketing.", p=dict(who="daniel", name=DAN)),
    dict(scene="end", spk="F", say=f"Book your strategy call at {SITE}. Or call {PH}.", min=5.8, pad=0.8),
]
# 2026-11-23 — wholesalers · SMS follow-up (opted-in): "call me after the holidays"
V["w2_after_the_holidays"] = [
    dict(scene="presenter", spk="F", say="Wholesalers... ever had a seller tell you, 'call me after the holidays'... and then you just... forgot?", cap="“Call me after the holidays.”", p=dict(who="maya", name=MAYA, card="After the holidays?")),
    dict(scene="slam", spk="M", say="We've all been there.", p=dict(lines=["FORGOTTEN", "FOLLOW-UP."], colors=[WHITE, ORANGE]), min=2.0),
    dict(scene="sms", spk="F", say="Our A-I remembers for you. It follows up by text with sellers who opted in... right when they asked.", cap="Follow-up, right on time", min=6.0,
         p=dict(who="Frank · Seller · Main St", stop=True, step=1.1, msgs=[("them", "Call me after the holidays."), ("me", "Will do, Frank! Enjoy the holidays."),
              ("me", "Hi Frank, checking back like you asked. Still thinking about selling the Main St house?"), ("them", "Yes. Let's talk.")])),
    dict(scene="contact", spk="F", say=f"Want follow-up that never forgets? Call {PH}.", min=3.6, p=dict(head="Never forget a seller", sub="Book your strategy call")),
    dict(scene="slam", spk="M", say="Here's the thing... the seller didn't go cold. The follow-up did.", cap="The follow-up went cold.", p=dict(lines=["THEY DIDN'T", "GO COLD."], colors=[WHITE, GOLD], stagger=0.5)),
    dict(scene="pipeline", spk="M", say="Now Frank moves from 'later'... to a booked appointment.", cap="From 'later' to booked", min=3.4, p=dict(card="Frank · Seller")),
    dict(scene="checks", spk="F", say="And that's how 'call me later' turns into an assignment fee.", cap="'Later' into assignment fees", min=3.4,
         p=dict(title="Assignment fees", memos=["Assignment fee · 5 Main St", "Assignment fee · 77 Union Ave", "Assignment fee · 310 Pine St"])),
    dict(scene="presenter", spk="M", say="Never lose a seller to 'call me later' again.", cap="Never lose a seller to 'later'.", p=dict(who="daniel", name=DAN, card="Never forget")),
    dict(scene="end", spk="M", say=f"Book your strategy call at {SITE}, or call {PH}.", min=5.8, pad=0.8, p=dict(sub="Wholesalers · Investors · Realtors")),
]
# 2026-11-24 — realtors · Thanksgiving week: "we should sell the house" (couch story)
V["w2_thanksgiving_table"] = [
    dict(scene="couch", spk="F", say="Thanksgiving week. Families get together... and somebody always says, 'You know, we should sell the house.'", cap="“We should sell the house.”", p=dict(clock="9:40 PM")),
    dict(scene="sms", spk="F", say="So later that night... they reach out.", cap="They reach out that night.", min=3.4,
         p=dict(who="Linda · Homeowner", stop=True, step=1.0, msgs=[("them", "Hi, we're thinking about selling in the spring. Can we talk?"), ("me", "Absolutely, Linda! Would Monday at 10 work for a quick consult?")])),
    dict(scene="presenter", spk="M", say="Will you answer? Because A-I Lead Finders does... holiday or not. Calls and texts, right away.", cap="Answered right away. Holiday or not.", p=dict(who="daniel", name=DAN, card="Holiday or not")),
    dict(scene="contact", spk="F", say=f"Get set up before the holidays. Call {PH}.", min=3.6, p=dict(head="Ready for the holidays", sub="Book your strategy call")),
    dict(scene="slam", spk="M", say="So while you're carving the turkey...", cap="While you're carving the turkey…", p=dict(lines=["CARVE THE", "TURKEY."], colors=[WHITE, GOLD]), min=2.4),
    dict(scene="qualify", spk="M", say="your listing consults are getting booked.", cap="Listing consults, booked", min=3.6,
         p=dict(items=["Selling in the spring", "Wants a home value review"], day="MONDAY", slot=1, appt="Listing consult · Booked by AI")),
    dict(scene="drone", spk="F", say="Holiday conversations today... spring listings tomorrow.", cap="Holiday talk. Spring listings.", min=3.8,
         p=dict(tags=["Listing consult", "Spring listing"], title="Spring listings start now", place="SUMMIT, NJ", push=False)),
    dict(scene="presenter", spk="F", say="Enjoy the holiday. Let A-I handle the follow-up.", cap="Enjoy the holiday.", p=dict(who="maya", name=MAYA)),
    dict(scene="end", spk="F", say=f"Book your strategy call at {SITE}. Or call {PH}.", min=5.8, pad=0.8),
]

if __name__ == "__main__":
    for k in sys.argv[1:]:
        out, total = render(k, V[k]); print(k, round(total, 1), out, flush=True)
