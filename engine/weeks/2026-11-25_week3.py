import sys
sys.path.insert(0, "/tmp/ailf")
from engine import WHITE, GOLD, ORANGE, SKY
from engine2 import render

PH = "nine, oh, eight... three, three, two... nine, three, three, oh"
SITE = "A-I Lead Finders dot com"
MAYA = ("Maya", "AI Lead Finders"); DAN = ("Daniel", "AI Lead Finders")

V = {}
# 2026-11-25 — realtors · AI voice agent: driving to see family, phone rings
V["w3_on_the_road"] = [
    dict(scene="presenter", spk="F", say="Realtors... tomorrow's Thanksgiving. You're on the Turnpike, car packed... and your phone rings.", cap="Holiday drive. Phone rings.", p=dict(who="maya", name=MAYA, card="On the road?")),
    dict(scene="call", spk="M", say="A seller. Asking about your listing. And you're doing seventy in traffic.", cap="A seller is calling…", min=3.2, p=dict(state="ring", who="Seller · Your listing", sub="Incoming call · 4:12 PM")),
    dict(scene="presenter", spk="M", say="So let our A-I voice agent pick up. It answers 24/7, asks the right questions... and takes care of them.", cap="AI voice agent answers 24/7", p=dict(who="daniel", name=DAN, card="We pick up")),
    dict(scene="contact", spk="F", say=f"Want to hear it before you leave town? Call {PH}.", min=3.6, p=dict(head="Hear it today", sub="Call and talk to our AI")),
    dict(scene="slam", spk="M", say="Now here's what you get when you park the car...", cap="When you park the car…", p=dict(lines=["EYES ON", "THE ROAD."], colors=[WHITE, GOLD], stagger=0.5), min=2.4),
    dict(scene="qualify", spk="F", say="A quick summary... and a listing consult already on your calendar.", cap="Listing consult, booked", min=3.8,
         p=dict(items=["Wants to sell after New Year's", "Asked about your listing"], day="MONDAY", slot=2, appt="Listing consult · Booked by AI")),
    dict(scene="drone", spk="M", say="Your phone keeps working... while you're with your family.", cap="Working while you're away", min=3.8,
         p=dict(tags=["Seller call", "Consult booked"], title="Your phone, covered", place="MONMOUTH COUNTY, NJ")),
    dict(scene="presenter", spk="F", say="Drive safe. We've got your calls.", cap="Drive safe. We've got it.", p=dict(who="maya", name=MAYA)),
    dict(scene="end", spk="F", say=f"Book your strategy call at {SITE}. Or call {PH}.", min=5.8, pad=0.8),
]
# 2026-11-26 — realtors + wholesalers · AI appointment setting: Thanksgiving "thankful"
V["w3_thankful"] = [
    dict(scene="presenter", spk="M", say="Happy Thanksgiving! Quick question... what would you be thankful for next year?", cap="What will you be thankful for?", p=dict(who="daniel", name=DAN, card="Happy Thanksgiving")),
    dict(scene="slam", spk="F", say="How about... a calendar that fills itself?", p=dict(lines=["A CALENDAR", "THAT FILLS."], colors=[WHITE, GOLD], stagger=0.5), min=2.6),
    dict(scene="chips", spk="F", say="Our A-I reaches out, has the first conversation... and books the ones who are ready.", cap="AI appointment setting", min=4.4,
         p=dict(title="Appointments, set for you", items=[("Reach out", "Sellers + buyers"), ("Talk", "First conversation, by AI"), ("Book", "Right on your calendar")])),
    dict(scene="contact", spk="F", say=f"Let's set it up before the new year. Call {PH}.", min=3.6, p=dict(head="Start the new year", sub="Book your strategy call")),
    dict(scene="week", spk="M", say="So... picture your first week of January.", cap="Your first week of January", min=2.6, p=dict(title="First week of January", empty=True)),
    dict(scene="week", spk="F", say="Appointments already waiting... before you even get back to the office.", cap="Appointments waiting for you", min=3.6, p=dict(title="First week of January", dur=2.6)),
    dict(scene="inventory", spk="M", say="Listings for realtors... deals for wholesalers. Same system.", cap="Realtors + wholesalers", min=3.8, p=dict(title="Your pipeline",
         items=[("22 Elm St", "Listing"), ("9 Ridge Rd", "New seller"), ("140 Grove St", "Appointment"), ("31 Bay Ave", "Under contract"), ("6 Fern Ln", "Showing"), ("88 Hill St", "Appointment")])),
    dict(scene="presenter", spk="F", say="Enjoy the turkey. We'll handle the calendar.", cap="Enjoy the turkey.", p=dict(who="maya", name=MAYA, card="We've got it")),
    dict(scene="end", spk="M", say=f"Book your strategy call at {SITE}, or call {PH}.", min=5.8, pad=0.8),
]
# 2026-11-27 — wholesalers · motivated seller prospecting: Black Friday deal hunting
V["w3_black_friday"] = [
    dict(scene="presenter", spk="M", say="Black Friday. Everybody's out hunting for deals... but wholesalers? Your best deals aren't at the mall.", cap="Hunting for deals today?", p=dict(who="daniel", name=DAN, card="Black Friday")),
    dict(scene="slam", spk="M", say="They're in your county.", p=dict(lines=["REAL DEALS?", "YOUR COUNTY."], colors=[WHITE, GOLD], stagger=0.5), min=2.2),
    dict(scene="drone", spk="F", say="A-I Lead Finders finds motivated sellers for you... tax delinquent, code violations, out-of-state owners.", cap="Motivated sellers, found for you", min=4.8,
         p=dict(tags=["Tax delinquent", "Code violation", "Out-of-state owner"], title="Sellers in your market", place="ESSEX COUNTY, NJ")),
    dict(scene="contact", spk="F", say=f"Want a look at your market? Call {PH}.", min=3.6, p=dict(head="Look at your market", sub="Book your strategy call")),
    dict(scene="slam", spk="M", say="And no... you don't have to wait in line for this one.", cap="No lines. No doorbusters.", p=dict(lines=["NO LINES.", "NO STAMPEDE."], colors=[WHITE, ORANGE], stagger=0.5)),
    dict(scene="pipeline", spk="F", say="Our A-I follows up and moves each seller along... until they're ready to talk numbers.", cap="Followed up until they're ready", min=4.2, p=dict(card="Gary · Seller")),
    dict(scene="checks", spk="M", say="That's where your assignment fees come from.", cap="Where assignment fees come from", min=3.4,
         p=dict(title="Assignment fees", memos=["Assignment fee · 17 Court St", "Assignment fee · 250 Clinton Ave", "Assignment fee · 4 Hawthorne Pl"])),
    dict(scene="presenter", spk="F", say="Skip the doorbusters. Go find real deals.", cap="Skip the doorbusters.", p=dict(who="maya", name=MAYA, card="Real deals")),
    dict(scene="end", spk="F", say=f"Book your strategy call at {SITE}. Or call {PH}.", min=5.8, pad=0.8, p=dict(sub="Wholesalers · Investors · Realtors")),
]
# 2026-11-28 — realtors · SMS follow-up (opted-in): leftovers + listing browsing (couch story)
V["w3_leftovers_scroll"] = [
    dict(scene="couch", spk="F", say="Saturday night. Leftovers... and they're scrolling homes for sale. Again.", cap="Leftovers + listings", p=dict(clock="9:15 PM")),
    dict(scene="form", spk="F", say="So they ask for more info on one of yours... and they check the box to get texts.", cap="They ask for info…", min=3.4),
    dict(scene="slam", spk="M", say="Then what? Do they hear from you Monday? Tuesday?", cap="Monday? Tuesday?", p=dict(lines=["MONDAY?", "TUESDAY?"], colors=[WHITE, ORANGE], stagger=0.5)),
    dict(scene="contact", spk="F", say=f"Or tonight. Call {PH}.", min=3.4, p=dict(head="Reply tonight", sub="Book your strategy call")),
    dict(scene="sms", spk="F", say="Our A-I texts them back right away... friendly, helpful, and only to people who opted in.", cap="Opted-in texts, right away", min=5.6,
         p=dict(who="Priya · Buyer", stop=True, step=1.0, msgs=[("them", "Hi! Is the house on Linden Ave still available?"),
              ("me", "Hi Priya! It is. Want to see it this week?"), ("them", "Yes! Maybe Wednesday evening?"), ("me", "Done. Wednesday at 6 with Jen.")])),
    dict(scene="slam", spk="M", say="See that? Nobody waited until Monday.", cap="Nobody waited.", p=dict(lines=["NOBODY", "WAITED."], colors=[WHITE, GOLD]), min=2.2),
    dict(scene="inventory", spk="M", say="And your showings line up... one after another.", cap="Showings, lined up", min=3.6, p=dict(title="Your showings", deals=False,
         items=[("12 Linden Ave", "Showing"), ("40 Maple St", "Appointment"), ("7 Brook Ln", "Showing"), ("215 Oak St", "Listing"), ("9 Pearl Ct", "Showing"), ("33 Elm Ave", "Appointment")])),
    dict(scene="presenter", spk="M", say="They're browsing tonight. Be the one who answers.", cap="Be the one who answers.", p=dict(who="daniel", name=DAN, card="Answer tonight")),
    dict(scene="end", spk="F", say=f"Book your strategy call at {SITE}. Or call {PH}.", min=5.8, pad=0.8),
]
# 2026-11-29 — investors · CRM + pipeline setup: sticky notes and year-end (meeting story)
V["w3_sticky_notes"] = [
    dict(scene="meeting", spk="M", say="You're meeting with your partner about next year... and a seller calls back from three weeks ago.", cap="A seller calls back…", p=dict(state="ring", title="Callback · Seller", sub="Duplex · Elizabeth, NJ")),
    dict(scene="meeting", spk="M", say="Wait... which one was that? Where are the notes? Uh oh...", cap="Which one was that?", p=dict(state="missed", title="Notes · Not found", sub="Sticky note? Spreadsheet?")),
    dict(scene="presenter", spk="F", say="Investors... sticky notes don't scale. We set up your C-R-M and pipeline, so every seller has a history and a next step.", cap="CRM + pipeline, set up for you", p=dict(who="maya", name=MAYA, card="No more sticky notes")),
    dict(scene="contact", spk="F", say=f"Start the year organized. Call {PH}.", min=3.6, p=dict(head="Get organized", sub="Book your strategy call")),
    dict(scene="slam", spk="M", say="So what changes? Everything's in one place.", cap="Everything in one place.", p=dict(lines=["ONE PLACE.", "EVERY DEAL."], colors=[WHITE, GOLD], stagger=0.5)),
    dict(scene="pipeline", spk="F", say="New... contacted... qualified... appointment. You always know where each deal stands.", cap="Know where every deal stands", min=4.2, p=dict(card="Duplex · Elizabeth", title="Your pipeline")),
    dict(scene="inventory", spk="M", say="Rentals, flips, two-families... all tracked.", cap="Every deal, tracked", min=3.6, p=dict(title="Your deal pipeline",
         items=[("2-fam · Bayonne", "New seller"), ("Ranch · Kenilworth", "Appointment"), ("Duplex · Elizabeth", "Under contract"), ("Cape · Roselle", "New seller"), ("Colonial · Hillside", "Appointment"), ("3-fam · Newark", "Under contract")])),
    dict(scene="presenter", spk="M", say="Next year... no deal gets lost in a notebook.", cap="No deal lost in a notebook.", p=dict(who="daniel", name=DAN)),
    dict(scene="end", spk="M", say=f"Book your strategy call at {SITE}, or call {PH}.", min=5.8, pad=0.8, p=dict(sub="Investors · Buy-and-hold · Flippers")),
]
# 2026-11-30 — wholesalers · done-for-you ads and outreach: Cyber Monday, everyone's online
V["w3_cyber_monday"] = [
    dict(scene="presenter", spk="F", say="Cyber Monday. Everybody's online today... including homeowners thinking about selling.", cap="Everyone's online today", p=dict(who="maya", name=MAYA, card="Cyber Monday")),
    dict(scene="slam", spk="M", say="So... are they seeing you?", p=dict(lines=["ARE THEY", "SEEING YOU?"], colors=[WHITE, ORANGE], stagger=0.5), min=2.2),
    dict(scene="presenter", spk="M", say="Wholesalers, we run your ads and outreach for you. Then our A-I follows up with every lead that comes in.", cap="Ads + outreach, done for you", p=dict(who="daniel", name=DAN, card="Done for you")),
    dict(scene="contact", spk="F", say=f"Want us to run it? Call {PH}.", min=3.4, p=dict(head="We run it for you", sub="Book your strategy call")),
    dict(scene="slam", spk="M", say="Here's the thing... clicks don't pay you. Conversations do.", cap="Clicks don't pay. Conversations do.", p=dict(lines=["CLICKS?", "CONVERSATIONS."], colors=[WHITE, GOLD], stagger=0.5)),
    dict(scene="channels", spk="F", say="Ad... text... call... booked.", cap="Ad, text, call, booked", min=2.8, p=dict(words=["AD", "TEXT", "CALL", "BOOKED"], step=0.4)),
    dict(scene="checks", spk="M", say="And booked conversations are how assignment fees happen.", cap="Conversations into contracts", min=3.4,
         p=dict(title="Assignment fees", memos=["Assignment fee · 63 Spruce St", "Assignment fee · 9 Front St", "Assignment fee · 118 Lincoln Ave"])),
    dict(scene="presenter", spk="F", say="Let us handle the marketing. You handle the deals.", cap="You handle the deals.", p=dict(who="maya", name=MAYA)),
    dict(scene="end", spk="F", say=f"Book your strategy call at {SITE}. Or call {PH}.", min=5.8, pad=0.8, p=dict(sub="Wholesalers · Investors · Realtors")),
]
# 2026-12-01 — realtors · motivated seller prospecting: December listing talk (meeting story)
V["w3_december_sellers"] = [
    dict(scene="meeting", spk="F", say="December first. You're at the office, planning next year... and you're asking yourself, where do the listings come from?", cap="Where will the listings come from?", p=dict(state="ring", title="Planning · Next year", sub="Listings needed")),
    dict(scene="presenter", spk="M", say="Realtors... a lot of homeowners start thinking about selling over the winter. The question is, who talks to them first?", cap="Who talks to them first?", p=dict(who="daniel", name=DAN, card="Who's first?")),
    dict(scene="drone", spk="F", say="A-I Lead Finders finds likely sellers in your farm area... long-time owners, expired listings, landlords ready to sell.", cap="Likely sellers in your farm", min=4.8,
         p=dict(tags=["Long-time owner", "Expired listing", "Landlord"], title="Your farm area", place="BERGEN COUNTY, NJ")),
    dict(scene="contact", spk="F", say=f"Want to see your farm area? Call {PH}.", min=3.6, p=dict(head="See your farm", sub="Book your strategy call")),
    dict(scene="slam", spk="M", say="And then... we start the conversation for you.", cap="We start the conversation.", p=dict(lines=["WE START", "THE TALK."], colors=[WHITE, GOLD], stagger=0.5)),
    dict(scene="qualify", spk="F", say="Timing, the property, what they need... and a listing consult on your calendar.", cap="Listing consult, booked", min=4.0,
         p=dict(items=["Thinking about spring", "Moving for work", "Wants a home value review"], day="THURSDAY", slot=1, appt="Listing consult · Booked by AI")),
    dict(scene="checks", spk="M", say="Listings today... commission checks down the road.", cap="Listings into commissions", min=3.4,
         p=dict(title="Commissions", memos=["Commission · 14 Prospect St", "Commission · 72 Glen Ave", "Commission · 5 Orchard Rd"])),
    dict(scene="presenter", spk="F", say="Plan the year... with sellers already talking to you.", cap="Sellers already talking to you.", p=dict(who="maya", name=MAYA, card="Plan the year")),
    dict(scene="end", spk="F", say=f"Book your strategy call at {SITE}. Or call {PH}.", min=5.8, pad=0.8),
]

if __name__ == "__main__":
    for k in sys.argv[1:]:
        out, total = render(k, V[k]); print(k, round(total, 1), out, flush=True)
