import sys
sys.path.insert(0, "/tmp/ailf")
from engine import WHITE, GOLD, ORANGE, SKY
from engine2 import render

PH = "nine, oh, eight... three, three, two... nine, three, three, oh"
SITE = "A-I Lead Finders dot com"
MAYA = ("Maya", "AI Lead Finders"); DAN = ("Daniel", "AI Lead Finders")

V = {}
# 1 — realtors: in a meeting, the phone rings
V["v1_missed_call"] = [
    dict(scene="meeting", spk="F", say="You're in the middle of a listing presentation... and your phone starts buzzing.", cap="Mid-meeting. Phone rings.", p=dict(state="ring")),
    dict(scene="meeting", spk="F", say="You can't pick up. So it goes to voicemail.", cap="Straight to voicemail.", p=dict(state="missed", title="Missed call · Seller", sub="No answer · 9:04 PM")),
    dict(scene="slam", spk="M", say="And that seller? They're already calling the next agent.", cap="They call the next agent.", p=dict(lines=["LISTING", "LOST."], colors=[WHITE, ORANGE])),
    dict(scene="presenter", spk="F", say="That's exactly why we built A-I Lead Finders. Our A-I answers every call, in seconds... day or night.", cap="Every call answered. 24/7.", p=dict(who="maya", name=MAYA, card="Never miss a call")),
    dict(scene="contact", spk="F", say=f"Want to hear it for yourself? Call us at {PH}.", min=3.6, p=dict(head="Hear it live", sub="Call and talk to our AI")),
    dict(scene="slam", spk="M", say="Now picture this. Every caller... qualified, and booked.", cap="Every caller qualified.", p=dict(lines=["QUALIFIED.", "BOOKED."], colors=[WHITE, GOLD], stagger=0.5)),
    dict(scene="qualify", spk="M", say="Timeline, price range, the address... done. Appointment's on your calendar.", cap="On your calendar.", min=4.0,
         p=dict(items=["Timeline: listing this spring", "Price range confirmed", "Address: Cranford, NJ"], appt="Listing appt · Booked by AI")),
    dict(scene="drone", spk="M", say="More appointments means more listings... right in your neighborhood.", cap="More listings in your area", min=4.2,
         p=dict(tags=["Listing appt", "New listing", "Just sold"], title="More listings", place="CRANFORD, NJ")),
    dict(scene="checks", spk="F", say="And more commission checks coming in.", cap="More closings. More commissions.", min=3.4,
         p=dict(title="Commissions coming in", memos=["Commission · 48 Oak Ave", "Commission · 12 Elm St", "Commission · 7 Birch Ln"])),
    dict(scene="presenter", spk="M", say="So stop losing listings to voicemail.", cap="Stop losing listings.", p=dict(who="daniel", name=DAN)),
    dict(scene="end", spk="M", say=f"Book your strategy call at {SITE}. Or call {PH}.", min=5.8, pad=0.8),
]
# 2 — wholesalers: talking-head host
V["v2_motivated_sellers"] = [
    dict(scene="presenter", spk="M", say="Hey wholesalers... real quick. How many hours did you spend cold calling this week?", cap="How many hours this week?", p=dict(who="daniel", name=DAN, card="Wholesalers")),
    dict(scene="slam", spk="M", say="Yeah. Way too many. I get it.", p=dict(lines=["WAY TOO", "MANY."], colors=[WHITE, ORANGE]), min=2.0),
    dict(scene="drone", spk="F", say="A-I Lead Finders finds motivated sellers in your market. Pre-foreclosures, probate, tired landlords, vacant homes.", cap="Motivated sellers, found for you", min=4.8,
         p=dict(tags=["Pre-foreclosure", "Probate", "Tired landlord", "Vacant"], title="Motivated sellers near you", place="UNION COUNTY, NJ")),
    dict(scene="contact", spk="F", say=f"Want to see who's selling in your area? Call {PH}.", min=3.6, p=dict(head="See your market", sub="Book your strategy call")),
    dict(scene="presenter", spk="F", say="But here's the part nobody talks about... the follow-up.", cap="The real secret: follow-up", p=dict(who="maya", name=MAYA, card="The follow-up")),
    dict(scene="sms", spk="F", say="Our A-I texts them, calls them, and keeps the conversation going. Instantly.", cap="Text + voice, instantly", min=4.6,
         p=dict(who="Maria · Seller · Elm St", stop=True, step=0.9, msgs=[("me", "Hi Maria, it's Mike's assistant. Still thinking about selling the Elm St house?"),
              ("them", "Maybe. Depends on the offer."), ("me", "Totally fair. Quick call Thursday at 11?"), ("them", "Thursday works.")])),
    dict(scene="pipeline", spk="M", say="And when they're ready to talk numbers? They land right on your calendar.", cap="Ready sellers, on your calendar", min=3.4, p=dict(card="Maria · Elm St")),
    dict(scene="inventory", spk="F", say="Picture your pipeline... always full of deals.", cap="A pipeline that stays full", min=3.4, p=dict(title="Your deal pipeline")),
    dict(scene="checks", spk="M", say="And those assignment fees? They start rolling in.", cap="Assignment fees rolling in", min=3.4,
         p=dict(title="Assignment fees", memos=["Assignment fee · 12 Elm St", "Assignment fee · 230 Maple Dr", "Assignment fee · 66 River St"])),
    dict(scene="slam", spk="M", say="You just show up... and make the offer.", p=dict(lines=["YOU MAKE", "THE OFFER."], colors=[WHITE, GOLD]), min=2.4),
    dict(scene="end", spk="F", say=f"Book your strategy call at {SITE}, or call {PH}.", min=5.8, pad=0.8, p=dict(sub="Wholesalers · Investors · Realtors")),
]
# 3 — buyers at night on the couch, then the demo
V["v3_inquiry_to_booked"] = [
    dict(scene="couch", spk="F", say="It's ten forty-seven at night. This couple just found their dream home online.", cap="10:47 PM. They found the one.", p=dict(clock="10:47 PM")),
    dict(scene="form", spk="F", say="So they fill out your form... and wait.", cap="They fill out your form…", min=2.8),
    dict(scene="slam", spk="M", say="Most agents reply the next day. By then? They've moved on.", cap="Next day is too late.", p=dict(lines=["NEXT DAY?", "TOO LATE."], colors=[WHITE, ORANGE])),
    dict(scene="contact", spk="M", say=f"Not with A-I Lead Finders. Call {PH}.", min=3.2, p=dict(head="Reply in seconds", sub="Book your strategy call")),
    dict(scene="sms", spk="F", say="Our A-I texts them back in about four seconds.", cap="Texted back in 4 seconds", min=3.0,
         p=dict(who="Jordan · Buyer", stop=True, step=0.6, timer=(2, 4), tdur=0.8, msgs=[("them", "Hi, interested in homes in Union County."), ("me", "Hi Jordan! Happy to help. What price range are you thinking?")])),
    dict(scene="chips", spk="M", say="It asks about budget, timeline, neighborhood... just like a great assistant would.", cap="Qualified like a pro", min=4.0,
         p=dict(title="Qualifying…", items=[("Budget", "$450k – $500k"), ("Timeline", "Moving in 60 days"), ("Area", "Cranford · Westfield")], timer=(5, 98), tdur=3.6)),
    dict(scene="qualify", spk="F", say="Then it books the showing. Saturday, eleven A-M. Under two minutes.", cap="Booked in under 2 minutes", min=3.6,
         p=dict(items=[], day="SATURDAY", slot=2, appt="Showing · Jordan · 11 AM", timer=(112, 112), stopped=True)),
    dict(scene="drone", spk="M", say="From one late-night inquiry... all the way to the closing table.", cap="Inquiry to closing table", min=4.0,
         p=dict(tags=["Showing · Sat 11 AM", "Under contract"], title="From inquiry to keys", place="WESTFIELD, NJ", push=False)),
    dict(scene="presenter", spk="F", say="Want this working for you... tonight?", cap="Working for you tonight", p=dict(who="maya", name=MAYA, card="Tonight?")),
    dict(scene="end", spk="F", say=f"Go to {SITE}, or call {PH}.", min=5.4, pad=0.8),
]
# 4 — brand: two hosts trade lines
V["v4_stop_chasing"] = [
    dict(scene="presenter", spk="F", say="Okay, be honest... how much of your day goes to chasing people who never call back?", cap="How much time do you chase?", p=dict(who="maya", name=MAYA)),
    dict(scene="slam", spk="M", say="Stop chasing.", p=dict(lines=["STOP", "CHASING."], colors=[WHITE, ORANGE]), min=1.8),
    dict(scene="presenter", spk="M", say="A-I Lead Finders is your A-I prospecting team. And it never clocks out.", cap="Your AI prospecting team", p=dict(who="daniel", name=DAN, card="Works 24/7")),
    dict(scene="drone", spk="F", say="It finds motivated sellers, and serious buyers...", cap="Finds sellers + buyers", min=3.4, p=dict(tags=["Seller", "Buyer", "Investor"], place="NEW JERSEY")),
    dict(scene="channels", spk="M", say="follows up by text, by voice, by email...", cap="Follows up everywhere", min=2.8, p=dict(words=["TEXT", "VOICE", "EMAIL"], step=0.5)),
    dict(scene="contact", spk="F", say=f"Questions? Call us. {PH}.", min=3.2, p=dict(head="Talk to us", sub="Book your strategy call")),
    dict(scene="week", spk="M", say="and fills your week with qualified appointments.", cap="A week full of appointments", min=3.0, p=dict(title="Your week", dur=2.2)),
    dict(scene="inventory", spk="F", say="More inventory. More deals.", cap="More inventory. More deals.", min=2.8, p=dict(title="More inventory", step=0.25)),
    dict(scene="checks", spk="M", say="More checks.", cap="More checks.", min=2.6, p=dict(title="More checks", step=0.4)),
    dict(scene="slam", spk="F", say="So you can do what you're actually great at. Closing.", p=dict(lines=["START", "CLOSING."], colors=[WHITE, GOLD], stagger=0.6), min=3.0),
    dict(scene="end", spk="M", say=f"Book your strategy call at {SITE}.", min=5.0, pad=0.8),
]
# 5 — quick direct response, both hosts
V["v5_book_a_call"] = [
    dict(scene="presenter", spk="M", say="Realtors... wholesalers... quick question.", cap="Quick question.", p=dict(who="daniel", name=DAN)),
    dict(scene="presenter", spk="F", say="What would a few more appointments a week do for your business?", cap="A few more appointments a week?", p=dict(who="maya", name=MAYA, card="More appointments?")),
    dict(scene="contact", spk="M", say=f"Let's talk. Call {PH}.", min=3.0, p=dict(head="Let's talk", sub="30-min strategy call")),
    dict(scene="book", spk="F", say="Or grab a quick thirty-minute strategy call online.", cap="30-min strategy call", min=2.6),
    dict(scene="chips", spk="M", say="We'll show you exactly how A-I finds, follows up, and books... for you.", cap="We map it out for you", min=3.6,
         p=dict(items=[("Find", "Motivated sellers + buyers"), ("Follow up", "Text + voice, in seconds"), ("Book", "Straight to your calendar")])),
    dict(scene="drone", spk="F", say="More appointments. More deals.", cap="More appointments. More deals.", min=2.8, p=dict(tags=["Appointment", "Deal"], place="NEW JERSEY")),
    dict(scene="end", spk="F", say=f"{SITE}. Talk soon!", min=4.4, pad=0.8, p=dict(head=["Book your", "strategy call"])),
]

if __name__ == "__main__":
    for k in sys.argv[1:]:
        out, total = render(k, V[k]); print(k, round(total, 1), out, flush=True)
