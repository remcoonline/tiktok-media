import sys
sys.path.insert(0, "/tmp/ailf")
from engine import WHITE, GOLD, ORANGE, SKY
from engine2 import render

PH = "nine, oh, eight... three, three, two... nine, three, three, oh"
SITE = "A-I Lead Finders dot com"
MAYA = ("Maya", "AI Lead Finders"); DAN = ("Daniel", "AI Lead Finders")

V = {}
# 2026-12-02 — realtors · AI voice agent: the office holiday party (meeting story)
V["w4_holiday_party"] = [
    dict(scene="meeting", spk="F", say="It's holiday party season. You're finally relaxing with the team... and your phone is buzzing in your coat pocket.", cap="Party's on. Phone's buzzing.", p=dict(state="ring", title="Incoming · Seller", sub="Holiday party · 7:40 PM")),
    dict(scene="presenter", spk="M", say="Realtors... do you step outside and take it? Or let it ring? Here's a third option.", cap="Take it? Or let it ring?", p=dict(who="daniel", name=DAN, card="Option three")),
    dict(scene="presenter", spk="F", say="Our A-I voice agent picks up for you, 24/7. It's friendly, it asks the right questions... and it books the appointment.", cap="AI voice agent answers 24/7", p=dict(who="maya", name=MAYA, card="We pick up")),
    dict(scene="contact", spk="F", say=f"Want to hear how it sounds? Call {PH}.", min=3.6, p=dict(head="Hear it live", sub="Call and talk to our AI")),
    dict(scene="slam", spk="M", say="So what's waiting for you after the party?", cap="What's waiting after the party?", p=dict(lines=["AFTER THE", "PARTY..."], colors=[WHITE, GOLD], stagger=0.5), min=2.4),
    dict(scene="qualify", spk="F", say="A short summary of the call... and a listing consult already on the calendar.", cap="Listing consult, booked", min=3.8,
         p=dict(items=["Selling a colonial in spring", "Wants a pricing talk"], day="TUESDAY", slot=2, appt="Listing consult · Booked by AI")),
    dict(scene="drone", spk="M", say="Sellers in your area get an answer... even while you're off the clock.", cap="Answered while you're off", min=3.8,
         p=dict(tags=["Seller call", "Consult booked"], title="Your area, covered", place="MORRIS COUNTY, NJ")),
    dict(scene="presenter", spk="M", say="Enjoy the party. Seriously. We've got the phone.", cap="Enjoy the party.", p=dict(who="daniel", name=DAN, card="We've got it")),
    dict(scene="end", spk="F", say=f"Book your strategy call at {SITE}. Or call {PH}.", min=5.8, pad=0.8),
]
# 2026-12-03 — wholesalers · SMS follow-up (opted-in): the 11:40 PM seller (couch story)
V["w4_late_night_seller"] = [
    dict(scene="couch", spk="M", say="Wholesalers... when does a seller finally decide to reach out? Hint... it's not two P-M on a Tuesday.", cap="When do sellers reach out?", p=dict(clock="11:40 PM")),
    dict(scene="couch", spk="F", say="They inherited a house they can't keep up with... and they just asked for an offer online.", cap="They just asked for an offer", p=dict(clock="11:40 PM")),
    dict(scene="presenter", spk="M", say="They checked the box to get texts. So our A-I texts them back right away... not tomorrow afternoon.", cap="Opted-in SMS, right away", p=dict(who="daniel", name=DAN, card="Text back now")),
    dict(scene="contact", spk="F", say=f"Want that set up? Call {PH}.", min=3.4, p=dict(head="Reply tonight", sub="Book your strategy call")),
    dict(scene="slam", spk="M", say="Here's what that conversation looks like...", cap="Here's the conversation…", p=dict(lines=["11:41 PM", "REPLIED."], colors=[WHITE, GOLD], stagger=0.5), min=2.4),
    dict(scene="sms", spk="F", say="Friendly, simple, and they can reply STOP anytime. Then it finds a time to talk.", cap="Opted-in · Reply STOP anytime", min=5.6,
         p=dict(who="Denise · Seller", stop=True, step=1.0, msgs=[("them", "Hi, I asked about an offer on my mom's house"),
              ("me", "Hi Denise, thanks for reaching out. Is now a bad time?"), ("them", "Tomorrow is better. After 5?"), ("me", "Perfect. 5:30 call with Mike.")])),
    dict(scene="checks", spk="M", say="Conversations like that... are where assignment fees start.", cap="Conversations into contracts", min=3.6,
         p=dict(title="Assignment fees", memos=["Assignment fee · 21 Locust St", "Assignment fee · 8 Vine Ave", "Assignment fee · 160 Park Ave"])),
    dict(scene="presenter", spk="F", say="Sellers don't keep office hours. Your follow-up shouldn't either.", cap="Sellers don't keep office hours.", p=dict(who="maya", name=MAYA)),
    dict(scene="end", spk="F", say=f"Book your strategy call at {SITE}. Or call {PH}.", min=5.8, pad=0.8, p=dict(sub="Wholesalers · Investors · Realtors")),
]
# 2026-12-04 — realtors · CRM + pipeline setup: past clients lost in your phone (meeting story)
V["w4_past_clients"] = [
    dict(scene="presenter", spk="F", say="Realtors... quick question. Where are your past clients right now? Like... actually?", cap="Where are your past clients?", p=dict(who="maya", name=MAYA, card="Quick question")),
    dict(scene="meeting", spk="M", say="A past client calls. They're thinking about moving up... and you can't remember a single detail.", cap="A past client calls…", p=dict(state="ring", title="Past client · Calling", sub="Bought with you in 2021")),
    dict(scene="presenter", spk="M", say="We fix that. We set up your C-R-M and pipeline... so every contact has notes and a next step.", cap="CRM + pipeline, set up for you", p=dict(who="daniel", name=DAN, card="Set up for you")),
    dict(scene="contact", spk="F", say=f"Let's get it organized before January. Call {PH}.", min=3.8, p=dict(head="Get organized", sub="Book your strategy call")),
    dict(scene="slam", spk="M", say="Now... what if your next listing is already in your phone?", cap="Your next listing, already in your phone?", p=dict(lines=["ALREADY IN", "YOUR PHONE."], colors=[WHITE, GOLD], stagger=0.5)),
    dict(scene="pipeline", spk="F", say="Past clients, sphere, new leads... each one in the right stage.", cap="Every contact, the right stage", min=4.2, p=dict(card="Kim · Past client", title="Your pipeline")),
    dict(scene="inventory", spk="M", say="And you can see your whole business... in one place.", cap="Your business, in one place", min=3.6, p=dict(title="Your pipeline", deals=False,
         items=[("4 Laurel Dr", "Listing"), ("19 Union Ave", "Appointment"), ("52 King St", "New seller"), ("7 Sage Ct", "Showing"), ("300 Main St", "Listing"), ("11 Pine Ter", "Appointment")])),
    dict(scene="presenter", spk="F", say="Your past clients remember you. Make sure you remember them.", cap="Remember your past clients.", p=dict(who="maya", name=MAYA)),
    dict(scene="end", spk="M", say=f"Book your strategy call at {SITE}, or call {PH}.", min=5.8, pad=0.8),
]
# 2026-12-05 — investors · motivated seller prospecting: driving for dollars in the cold
V["w4_cold_drive"] = [
    dict(scene="presenter", spk="M", say="Investors... driving for dollars in December? Heater on full blast, coffee's cold... and you're squinting at porches.", cap="Driving for dollars in December?", p=dict(who="daniel", name=DAN, card="Brr.")),
    dict(scene="slam", spk="F", say="What if you could see the whole map from the warm car?", cap="See the whole map instead", p=dict(lines=["STAY", "WARM."], colors=[WHITE, GOLD], stagger=0.5), min=2.4),
    dict(scene="drone", spk="F", say="A-I Lead Finders finds motivated sellers for you... vacant homes, tired landlords, owners who moved out of state.", cap="Motivated sellers, found for you", min=4.8,
         p=dict(tags=["Vacant", "Tired landlord", "Out-of-state owner"], title="Your target area", place="UNION COUNTY, NJ")),
    dict(scene="contact", spk="F", say=f"Want to see your area? Call {PH}.", min=3.6, p=dict(head="See your area", sub="Book your strategy call")),
    dict(scene="slam", spk="M", say="But a list alone doesn't buy houses... right?", cap="A list doesn't buy houses.", p=dict(lines=["A LIST?", "OR A DEAL?"], colors=[WHITE, ORANGE], stagger=0.5), min=2.4),
    dict(scene="qualify", spk="F", say="So our A-I reaches out, finds out who's actually ready... and puts them on your calendar.", cap="Ready sellers, on your calendar", min=4.0,
         p=dict(items=["Rental is vacant", "Owner lives in Florida", "Open to an offer"], day="WEDNESDAY", slot=1, appt="Seller call · Booked by AI")),
    dict(scene="inventory", spk="M", say="Rentals, fixers, multi-families... lined up for you to look at.", cap="Deals lined up for review", min=3.6, p=dict(title="Your deal pipeline",
         items=[("2-fam · Linden", "New seller"), ("Cape · Rahway", "Appointment"), ("Ranch · Union", "Under contract"), ("3-fam · Elizabeth", "New seller"), ("Split · Clark", "Appointment"), ("Duplex · Roselle", "Under contract")])),
    dict(scene="presenter", spk="F", say="Keep the heater on. Let us do the driving.", cap="Let us do the driving.", p=dict(who="maya", name=MAYA, card="We do the driving")),
    dict(scene="end", spk="M", say=f"Book your strategy call at {SITE}, or call {PH}.", min=5.8, pad=0.8, p=dict(sub="Investors · Buy-and-hold · Flippers")),
]
# 2026-12-06 — realtors + wholesalers · AI appointment setting: the Sunday-night calendar check
V["w4_sunday_calendar"] = [
    dict(scene="presenter", spk="F", say="Sunday night. You open your calendar for the week... and it's looking a little... empty.", cap="Sunday night calendar check", p=dict(who="maya", name=MAYA, card="Sunday night")),
    dict(scene="week", spk="M", say="Sound familiar?", cap="Sound familiar?", min=2.4, p=dict(title="This week", empty=True)),
    dict(scene="chips", spk="F", say="Our A-I reaches out to your leads, has the first conversation... and books the ones who are ready to talk.", cap="AI appointment setting", min=4.6,
         p=dict(title="Appointments, set for you", items=[("Reach out", "Your leads, every day"), ("Talk", "First conversation, by AI"), ("Book", "Straight to your calendar")])),
    dict(scene="contact", spk="F", say=f"Want a fuller week? Call {PH}.", min=3.4, p=dict(head="Fill your week", sub="Book your strategy call")),
    dict(scene="slam", spk="M", say="Now... picture next Sunday.", cap="Now picture next Sunday.", p=dict(lines=["NEXT", "SUNDAY."], colors=[WHITE, GOLD], stagger=0.5), min=2.2),
    dict(scene="week", spk="F", say="Appointments already set... before Monday even starts.", cap="Booked before Monday", min=3.4, p=dict(title="Next week", dur=2.4)),
    dict(scene="inventory", spk="M", say="Listing consults for realtors... seller calls for wholesalers. One system.", cap="Realtors + wholesalers", min=3.8, p=dict(title="Your week ahead",
         items=[("8 Willow St", "Appointment"), ("27 Oak Ln", "New seller"), ("140 Main St", "Listing"), ("5 Grant Ave", "Appointment"), ("61 Cherry St", "Showing"), ("9 Mill Rd", "Under contract")])),
    dict(scene="presenter", spk="M", say="Close the laptop. Your week's already handled.", cap="Your week's handled.", p=dict(who="daniel", name=DAN, card="Handled")),
    dict(scene="end", spk="F", say=f"Book your strategy call at {SITE}. Or call {PH}.", min=5.8, pad=0.8),
]
# 2026-12-07 — wholesalers · done-for-you ads and outreach: wearing three hats
V["w4_three_hats"] = [
    dict(scene="presenter", spk="M", say="Wholesalers... let me guess. You're the marketer, the follow-up guy... and the one making offers. All in one day.", cap="Three jobs, one person?", p=dict(who="daniel", name=DAN, card="Three hats?")),
    dict(scene="slam", spk="F", say="That's a lot of hats.", p=dict(lines=["MARKETER.", "FOLLOW-UP.", "CLOSER."], colors=[WHITE, SKY, GOLD], stagger=0.4, size=130), min=2.6),
    dict(scene="presenter", spk="F", say="So let us take two of them. We run your ads and outreach... and our A-I follows up with every lead.", cap="Ads + outreach, done for you", p=dict(who="maya", name=MAYA, card="Done for you")),
    dict(scene="contact", spk="F", say=f"Ready to drop a hat? Call {PH}.", min=3.4, p=dict(head="We run it", sub="Book your strategy call")),
    dict(scene="slam", spk="M", say="Which leaves you with... the fun part.", cap="You keep the fun part.", p=dict(lines=["YOU KEEP", "THE FUN PART."], colors=[WHITE, GOLD], stagger=0.5), min=2.4),
    dict(scene="channels", spk="F", say="Ad... text... call... booked.", cap="Ad, text, call, booked", min=2.8, p=dict(words=["AD", "TEXT", "CALL", "BOOKED"], step=0.4)),
    dict(scene="checks", spk="M", say="You show up, make the offer... and work toward the assignment fee.", cap="You make the offer", min=3.4,
         p=dict(title="Assignment fees", memos=["Assignment fee · 77 Ward St", "Assignment fee · 3 Chestnut Pl", "Assignment fee · 210 Broad St"])),
    dict(scene="presenter", spk="M", say="One hat. The one that closes deals.", cap="Wear the closer hat.", p=dict(who="daniel", name=DAN, card="One hat")),
    dict(scene="end", spk="F", say=f"Book your strategy call at {SITE}. Or call {PH}.", min=5.8, pad=0.8, p=dict(sub="Wholesalers · Investors · Realtors")),
]
# 2026-12-08 — realtors · SMS follow-up (opted-in): showings cancelled, buyers still browsing
V["w4_snow_day"] = [
    dict(scene="presenter", spk="F", say="Realtors... cold, snowy day. Showings get pushed. Everybody stays in.", cap="Snowy day. Showings pushed.", p=dict(who="maya", name=MAYA, card="Snow day")),
    dict(scene="slam", spk="M", say="But buyers? They're still browsing. From the couch.", cap="Buyers are still browsing", p=dict(lines=["STILL", "BROWSING."], colors=[WHITE, GOLD], stagger=0.5), min=2.4),
    dict(scene="form", spk="F", say="One of them asks about your listing... and checks the box to get texts.", cap="They ask about your listing", min=3.4),
    dict(scene="contact", spk="F", say=f"Want them answered today? Call {PH}.", min=3.6, p=dict(head="Answer today", sub="Book your strategy call")),
    dict(scene="presenter", spk="M", say="Here's the thing... the snow cancels the showing. It shouldn't cancel the conversation.", cap="Keep the conversation going", p=dict(who="daniel", name=DAN, card="Keep talking")),
    dict(scene="sms", spk="F", say="Our A-I texts back right away... only people who opted in, and they can reply STOP anytime.", cap="Opted-in · Reply STOP anytime", min=5.6,
         p=dict(who="Marcus · Buyer", stop=True, step=1.0, msgs=[("them", "Is the Cedar St house still available?"),
              ("me", "It is! Want to see it once the roads clear?"), ("them", "Yes. Saturday morning?"), ("me", "Saturday at 10 with Lisa. Done.")])),
    dict(scene="inventory", spk="M", say="And when the roads clear... your showings are lined up.", cap="Showings lined up", min=3.6, p=dict(title="Your showings", deals=False,
         items=[("18 Cedar St", "Showing"), ("6 Hillside Ave", "Appointment"), ("95 Spring St", "Showing"), ("2 Ivy Ct", "Listing"), ("44 Beech St", "Showing"), ("71 Lake Dr", "Appointment")])),
    dict(scene="presenter", spk="F", say="Stay warm. Keep the conversations going.", cap="Stay warm. Keep talking.", p=dict(who="maya", name=MAYA)),
    dict(scene="end", spk="F", say=f"Book your strategy call at {SITE}. Or call {PH}.", min=5.8, pad=0.8),
]

if __name__ == "__main__":
    for k in sys.argv[1:]:
        out, total = render(k, V[k]); print(k, round(total, 1), out, flush=True)
