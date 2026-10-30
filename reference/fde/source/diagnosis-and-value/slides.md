# Diagnosis And Value — redacted presentation / 匿名化スライド

- **Use:** background reading; operating skills use the distilled method pages instead.
- **Edition:** slide order and original language are retained; formatting is reconstructed for Markdown.
- **Redaction:** organization, product, trainer, participant, customer, and contact identities are removed.
- **Diagrams:** image-only material is described explicitly as a manual diagram transcription.
- **Evidence:** historical figures and fictional case figures are teaching examples, not current capability or value claims.
- **Notes:** [accompanying notes](notes.md).

## Slide 1

- FDE WORKSHOP · SESSION 2 Customer dialogue

## Slide 2

- LAST WEEK · 4 MIN Last week: the behaviour your table rated lowest
- PAIRS · 2 MIN
- PAIRS
- ROOM · 2 MIN
- Which one was it?
- Why is it low?
- Two pairs share
- One reason. Is it skill, time, or the way work is set up here?
- Last week we looked at what you value most. Today we start from what is weakest.
- Write down the behaviour your table rated lowest last week. If you were not here, pick the one you think [identity redacted]  is weakest at.

## Slide 3

- LAST WEEK · 2 MIN Your murderboards
- Hands up if your murderboard is booked: a date,
- three reviewers, three hard questions
- Run one already? Tell me at the break which question was hardest.
- Hand in your W1 commitment card
- FDE-only: hand in your Configure / Extend / Invent
- split on the card provided

## Slide 4

- TODAY What we will do today, and what you will leave with
- 1 Section 1: finding the number
- You leave with:
- Find the cause of a problem, find what it costs, and turn that into KPIs you can propose to a customer.
- 1. A steerco design for one live account
- 2 Break · 5 minutes
- 2. A first draft of [identity redacted] 's escalation rule
- 3 Section 2: getting it in front of the right people
- The steering committee with the customer, and escalation inside [identity redacted] .

## Slide 5

- SECTION 1 Finding the number

## Slide 6

- A STORY
- 300 users
- A chemical maker. A supply crisis on the car production lines. From 0 to 300 users in under 12 hours.

## Slide 7

- SECTION 1 · WHAT AND WHY What this section is for
- 1 Customers tell you about symptoms
- By the break you will have:
- "It is slow." "The numbers are wrong." "We need a report."
- 2 To fix it, find the cause
- A why chain for one of your accounts
- This is the engineering skill. We use Five Whys, on a real [identity redacted]  incident.
- Three KPIs you could propose next week
- 3 To get it valued, find what it costs
- This is the skill customers pay for. We use the why chain, on your own account.
- 4 Then turn that into KPIs
- Numbers you can propose to the customer, instead of waiting for them to choose.

## Slide 8

- TWO DIRECTIONS Two directions from one problem
- Going up: what it costs …which delays something a manager is
- responsible for
- Going down finds what to fix. Engineers usually go this way.
- …a number a senior person is measured on
- The problem someone tells you about
- Going up finds why it matters, and to whom. This is where budgets are decided.
- …because of this step
- We do down first, because you already know it. Then up.
- …because of this decision or gap Going down: the cause

## Slide 9

- GOING DOWN · FIVE WHYS Where Five Whys comes from
- ORIGIN
- USE TOD AY
- KNOWN LIMITS
- Beyond factories
- Two weaknesses
- It can stop at one cause when
- there are several
- It is only as good as what the
- Lean manufacturing, quality teams, and software teams reviewing incidents after an outage.
- people asking know
- Developed by [identity redacted]  and used inside [identity redacted] . [identity redacted]  made it part of the [identity redacted]  Production System and described it in his 1978 book.

## Slide 10

- GOING DOWN · FIVE WHYS [identity redacted]'s example: a machine that stopped
- A welding robot stops. Why? An overload blew the
- fuse.
- Replace the fuse, and the machine stops again next month.
- Why the overload? The bearing was not lubricated
- enough.
- Fit the filter, and it does not.
- Why? The lubrication pump was not pumping
- enough.
- Why? The pump shaft was worn.
- Why? There was no filter, so metal scrap got in.

## Slide 11

- GOING DOWN · FIVE WHYS How to do Five Whys well
- Check each answer
- Follow each cause separately
- Process, not person
- Stop at something you can change
- Five is not a rule. Stop when the fix is clear, or when the next answer is outside anyone's control.
- Each 'because' should be something you saw in a log, a record or the system, not something that sounds right.
- Real incidents usually have several causes: a technical one, a decision, a check that missed it. Ask down each one.
- 'Someone made a mistake' is never the last answer. Ask why the system let the mistake through.

## Slide 12

- EXERCISE · HOW IT WORKS A real case: [identity redacted] , 26 August
- A temporary workflow, added to production just
- Ask, don't guess.
- before a customer demo, overloaded a shared service for almost five hours
- If the answer is "not in the report", that is a finding too.
- Several customers' apps slowed or failed. The
- Process, not person.
- demo could not be held. Stopping the workflow took most of the afternoon
- The internal report sets out the facts.
- Countermeasures were left for later
- Each table gets one starting question. One person
- holds the facts and answers only what you ask

## Slide 13

- 10
- SHORT EXERCISE 1 · FIVE WHYS Ask your way down to the causes
- min
- Tables of four · one starting question each · one fact holder per table
- OUTPUT
- 6'
- Ask the fact holder questions. Write each 'because' and how you know it. A: Why was the load so high? B: Why was the change made then? C: Why did nobody know the impact? D: Why could it not be stopped?
- One chain per table, ending at something [identity redacted]  can change.
- 3' Share: one line per table. Which causes already have a fix? Which do not?
- YOU NEED
- 1' Last question: what did it cost, and who would know?
- Fact pack (holder only). Chain sheet. Pen.

## Slide 14

- 2 6 AUGUST · THE FULL PICTURE What happened on 26 August
- Time What happened
- Morning Production change for a speed-up that was not a required deliverable, just before a customer demo
- 09:48 to 10:11 New column added. Temporary workflow trialled on 178, then 200 groups. The rest handed to a background agent
- 10:22 to 11:58 Connection drops trigger resends and retries: 12 run requests for the same job, overlapping
- 10:42 Shared service slows. Typical response 0.25 s becomes 17 to 33 s
- 13:37 Workflow identified as the source of the load
- 13:59 to 14:01 A different workflow is disabled by mistake (name mix-up). Then the right one is disabled, but runs continue
- 14:34 Customer demo cancelled
- 15:12 to 15:29 A new run starts even after access is removed. Workflow emptied at 15:22. Load ends 15:29
- 6 to 7 Sept Code fixes merged: stop checks, limits on duplicate runs, a stop function
- Source: [identity redacted]  internal incident report, 15 to 16 September. Customer names removed.

## Slide 15

- AFTER THE EXERCISE What happens to your answers
- [identity redacted]  photographs each table's sheet
- We send them to the report's author, as input to the countermeasures still to be written
- Notice what nobody could answer: what the incident cost. That is the next part

## Slide 16

- GOING UP What staff ask for, and what their manager cares about
- What the customer's staff asked for What their manager actually cares about
- "Search across our contracts takes forever" Legal review is the bottleneck on every deal; quarter-end deals slip
- "The summary misses details sometimes" Someone still rechecks everything, so no time is saved
- "Can it read handwritten forms?" Branch paperwork delays onboarding, and new customers drop out
- "Can we get a weekly report?" My director asks every Monday and I have nothing to show
- Going up means asking what each request is really for, until you reach something a manager is measured on.

## Slide 17

- GOING UP · EXAMPLE Example: "we keep running out of parts"
- 1 Start: "We run out of parts, and reordering is slow"
- Heard: from maintenance staff at a defence customer. They asked for inventory management.
- 2 Going down: why do they run out?
- Funding rules for common parts, default schedules nobody follows, no predictive maintenance.
- 3 So the wrong parts are bought and stockpiled
- Expensive parts nobody uses. Data: stock levels against actual use.
- 4 So over ¥700 million a year goes on parts never used
- Data: a year of orders.
- 5 Top: a budget a senior officer is responsible for
- Money that could move to the parts that run out. Heard: from that officer.
- They ran out of what they needed while stockpiling what they didn't. The request was inventory management; the number was over ¥700 million a year.

## Slide 18

- GOING UP Five rules for going up
- 1 Ask "what happens if this is not fixed?" and "who notices?"
- Not "why?". In Japanese, なぜcan sound like blame. These two questions get the same answer without it.
- 2 Each step names a person and a number
- If you cannot say who cares and how much, the step is not finished.
- 3 Stop at a number on a senior person's scorecard
- A profit and loss line, a mid-term plan target, a regulatory deadline.
- 4 Label every step: heard, seen in data, or assumed
- An assumed step is a question for next week, not a fact for the slides.
- 5 Read it back with "so that"
- If one step does not follow from the one below, something is missing.

## Slide 19

- GOING UP Common mistakes when going up
- Skipping steps
- Stopping at the team
- Inventing the number
- Selling, not understanding
- "The team saves time" is not money until someone decides what to do with the time.
- The chain is for finding out what matters to them, not for justifying what you built.
- "Better OCR accuracy" straight to "more revenue". Nobody can check it, so nobody believes it.
- A made-up figure is found out in one question, and after that nothing you say is believed.

## Slide 20

- 6
- SHORT EXERCISE 2 · GOING UP Build a why chain for your own account
- min
- DS + FDE pairs where you can · one account per pair: one you will keep using through DS3
- OUTPUT
- 1' Write one thing the customer's staff complain about, in their words.
- One why chain, every step labelled. Keep it: the KPI exercise starts from it.
- 4' Go up one step at a time until you reach a number someone senior is measured on. Label every step: heard, data, assumed.
- YOU NEED
- Why-chain card
- 1' Hands up: whose top step is "assumed"?

## Slide 21

- KPI s · WHAT AND WHY Next: turning your why chain into KPIs
- 1 Why KPIs matter
- Without agreed measures, a steering committee has nothing to report, and a renewal is decided on feelings.
- You will finish with a KPI sheet for your account: three KPIs, each with a data source, a starting value and an owner.
- 2 Why we propose them
- Customers rarely set KPIs before a project starts. If we wait, nobody sets them.
- 3 What we will do
- Three levels of KPI, how to find numbers nobody is tracking, and what your platform's usage data already gives you.

## Slide 22

- KPI s Three levels of KPI
- Impact The number a senior person is measured on. The top of your why chain.
- Look at your card. You already have all three levels.
- Agree all three with the customer before kickoff.
- Outcome What changes in how the work gets done. The middle of your chain.
- Activity What people do with the system: users, runs, documents processed. The bottom of your chain.

## Slide 23

- BACK TO THE STORY The 300 users story, at three KPI levels
- Impact
- The customer measured activity and outcome.
- Over €90M: the contract cost of production stopping, for the customers we chose to prioritise who did not run out
- Outcome Decisions made, and orders filled
- The impact number was already in the system: the contract cost of a stopped line, on every order.
- Activity From 0 to 300+ users in under 12 hours

## Slide 24

- CHECK Which level are our own KPIs?
- Speed: from finished requirements to ready for
- delivery
- Hands: activity, outcome or impact?
- Tests: bugs and test cases passed at the final test
- What would the customer's senior people ask about?
- Communication: was DS and FDE communication
- smooth?

## Slide 25

- FINDING KPI s Propose KPIs to the customer
- Asking a Japanese customer to define KPIs before a project often puts them on the
- spot
- Look at the process and usage data yourself
- Bring a hypothesis with a number and a range
- Convert weekly savings to a year: senior people think in years

## Slide 26

- FINDING KPI s Four ways to find a KPI nobody asked for
- Look at the decision
- Find what nobody tracks
- Question the source data
- Use the data twice
- The stated goal is rarely where the waste is.
- They ask for a screen. Ask what decision the screen is for.
- Data collected for one purpose often answers a more valuable question.
- When the numbers disagree, the disagreement is often the finding.
- 26 August is an example of the second: nobody was tracking what it cost.

## Slide 27

- FIND WHAT NOBODY TRACKS
- Back to the parts example
- Nobody was tracking parts that were bought and never used. That was the ¥700 million.

## Slide 28

- USE THE DATA TWICE
- The bill of materials
- Collected for carbon reporting. It also contained the costs.

## Slide 29

- BACK TO 2 6 AUGUST What did the incident cost?
- The report says the total impact has not been determined
- 90 seconds: which one impact KPI would have told us the cost?
- Who at [identity redacted]  would own that number?

## Slide 30

- A NOTE Activity numbers still matter
- Users and runs move first, before outcomes and impact
- You need them to explain the impact number
- Keep the 300 users. Report them alongside the €90M, not instead of it

## Slide 31

- KPI s FROM USAGE DATA Your platform already records the activity level
- WHAT THE LOGS GIVE YOU
- AN ILLUSTR AT IVE SUM
- THEN
- Activity
- To a yearly range
- Ask the outcome question
- 1,800 runs a month × 12
- What did the 360 hours turn into? That is the outcome level, and only the customer can tell you.
- minutes saved = 360 hours a month
- × ¥4,000 an hour ≈ ¥1.4M a
- Runs per month
- Active users by team
- Time per task
- Edit rate: how often people
- month
- ≈ ¥12M to ¥20M a year,
- change the output
- Hand-backs to a person
- depending on edit rate

## Slide 32

- 12
- EXERCISE A · KPI s Propose three KPIs for your account
- min
- Same pairs · same account · start from your why chain
- OUTPUT
- 7' KPI sheet: one KPI per level. For each, write the data source, today's value and who owns it at the customer. No value yet? Write how you would get it.
- A KPI sheet you would show the customer next week. A weak why chain shows up here, when the KPI built on it is questioned.
- 5' 60-second proposal to the pair next to you, who play the customer. They ask one hard question. Then swap.
- YOU NEED
- Why-chain card, KPI sheet

## Slide 33

- DEBRIEF · 4 MIN What did the proposals show?
- WHAT?
- SO WHAT?
- NOW WHAT?
- Which KPIs had no starting value or no data source?
- Who at the customer owns the impact number, and have you met them?
- Write the one question you will ask the customer next week.
- Keep the KPI sheet. Section 2 uses it.

## Slide 34

- BREAK Five minutes
- Keep your KPI sheet. Section 2 starts from it.

## Slide 35

- SECTION 2 Getting it in front of the right people

## Slide 36

- A STORY
- The account that would not grow
- A German chemical company. A big early win. Happy users. And for years, the spend barely moved.

## Slide 37

- SECTION 2 · WHAT AND WHY What this section is for
- 1 A number nobody senior sees changes nothing
- You will finish with:
- Your KPIs only matter if the people who decide budgets see them regularly.
- A steerco design for one live account
- 2 With the customer: the steering committee
- A first draft of [identity redacted] 's escalation rule
- A regular meeting where the senior owner sees results and makes decisions.
- 3 Inside [identity redacted] : escalation
- How problems and opportunities reach the right person early, instead of late.

## Slide 38

- OPERATORS AND MANAGERS Operators and managers judge the work differently
- Operators see the tool
- Managers see the budget
- Training does not fix this
- A regular meeting with the senior owner in the room does.
- They judge it by whether today's work got easier. They are often right, and they rarely hold a budget.
- They judge it by the number they are measured on. They will not hear about your work unless someone shows them.
- The German account grew once we reached people who cared about the bigger picture, and could explain it in their terms.

## Slide 39

- THE STEERING COMMITTEE What a steering committee is
- HOW OFTEN
- CONTENT
- WHO AT TENDS
- WHO PRESENTS
- Monthly
- The customer
- Live demo and KPIs
- The most senior owner
- Not a status report. The system working on their data, and the three KPI levels moving.
- When their own people say it saved time, it is believed. When we say it, it sounds like sales.
- Separate from the weekly working meeting with operators, which is where day-to-day problems come up.
- Their presence changes the meeting, and brings out problems you would never hear from operators.
- Example: a hospital's daily bed meeting, run live in the tool. Then the requests started coming in.

## Slide 40

- THE STEERING COMMITTEE A 45-minute agenda
- Minutes Item Who
- 5 Results against the three KPIs DS
- 10 Live demo, run by a customer user Customer champion, with the FDE beside them
- 15 Decisions needed from this meeting Senior owner
- 10 Next month: what we will deliver and measure DS and FDE
- 5 Risks and requests DS
- A third of the time is for decisions. If there is nothing to decide, it is only a status update.

## Slide 41

- THE STEERING COMMITTEE How to get the senior owner to attend
- 1 Produce a result the operator wants to report upwards
- They tell their manager before you do.
- 2 Ask the customer's champion to introduce you
- Give them the key points and the numbers to use.
- 3 根回しbefore the meeting
- The decision taken in the meeting should already be agreed in conversations the week before.
- DS3 on 16 October covers this in detail, including how decisions are really made inside the customer.

## Slide 42

- ESCALATION Escalating early is part of ownership
- W1's two failure modes: building only what you are told, and holding everything yourself
- Holding everything feels responsible. It is often how a problem reaches the customer
- before it reaches your DS

## Slide 43

- ESCALATION Two kinds of escalation: problems and opportunities
- APROBLEM
- WHAT IT WAS
- AN OPPORTUNITY
- The numbers did not match
- Checked against payroll
- Something bigger than your scope
- These are escalations too. Example in three slides.
- The system did not match the customer's staffing spreadsheet for one location. The customer said the system was wrong, so the FDE added a filter to make the numbers match.
- A site that was not yet open, and should have had only maintenance staff, was double- staffed. About 100 salaries were misallocated and available for use elsewhere.
- What would you have done?
- The mismatch was the finding.

## Slide 44

- ESCALATION Writing a status that gets you help
- Status that hides the problem Status that gets help
- No progress this week Waiting for the customer's decision on X since 1 Oct. Need the DS to chase it by Friday
- Investigating data issue Numbers do not match their spreadsheet. Checked against source; need 30 minutes with their payroll owner
- Stopped the workflow Stopped workflow 'Duplicate flag v2' (ID ...). Please confirm this is the one causing the load
- On 26 August, the wrong workflow was stopped because of a name mix-up. Under pressure, exact names save hours.

## Slide 45

- ESCALATION · DRAFT Who to escalate to, when, and how (draft)
- WHO
- WHEN
- HOW
- Time limits
- Six parts
- By the kind of problem
- Customer, scope, priorities:
- Stuck for 2 working days: tell
- your DS
- Technical, design: EM or tech
- your DS
- Stuck for 5: tell the EM
- Anything bigger than the
- lead
- Missing product feature:
- scope: your DS within a week
- Situation
- What I tried
- What I need
- From whom
- By when
- What happens if not
- platform team
- Commercial opportunity:
- account owner

## Slide 46

- ESCALATION · OPPORTUNITY Escalating an opportunity: an example
- WHAT HAPPENED
- HOW IT WAS CAUGHT
- WHAT TO DO
- "Out of scope"
- In a 1:1
- Three steps
- Build a why chain for it
- Tell your DS within a week
- The DS takes it to the account
- plan or the next steering committee
- The team forecasting where vaccine would be needed asked an FDE to help move their model onto the platform and connect it to live data. He said it was out of scope and sent them an export.
- Holding the source data and calculations for that national decision on our platform, with its heaviest users, was worth far more than the original scope. We assigned people to it as an investment.

## Slide 47

- 9
- EXERCISE B 1 · STEERING COMMITTEE Design a steering committee for one live account
- min
- Tables of four · one account per table
- OUTPUT
- 2' Pick the account. Copy the three KPIs from the best KPI sheet at your table.
- Artefact 1: a steering committee design for one real account, ready for your DS to propose.
- 4' Fill in the canvas: who attends, how often, the first agenda, and who you talk to beforehand.
- YOU NEED
- Steerco canvas, KPI sheets
- 3' Write the one decision you want from the senior owner at the first meeting.

## Slide 48

- 8
- EXERCISE B 2 · ESCALATION RULE Draft [identity redacted] 's escalation rule
- min
- Whole room · [identity redacted]  types on screen
- OUTPUT
- 3' Edit the draft: who, time limits, the six parts. What is wrong for [identity redacted] ?
- 2' Test it on 26 August: would it have prevented the wrong workflow being stopped?
- Artefact 2: the first draft of [identity redacted] 's escalation rule, covering problems and opportunities.
- 2' Test it on a real week from this room where work was stuck. Would it have come out sooner?
- 1' [identity redacted]  and a DS manager: accept it as a first draft?

## Slide 49

- COMMITMENTS · 5 MIN What you will do before 22 October
- Check your why chain with the real customer, and
- propose one KPI
- Write yours on the card. About 15 seconds each to say it out loud.
- Send your steering committee proposal to your DS
- Homework: rewrite your own last "no progress"
- week as an escalation, using the six parts

## Slide 50

- NEXT Tomorrow, and 22 October
- DS attendees: at DS1 tomorrow, you explain today's escalation rule to colleagues who
- were not here
- W3 on 22 October builds a decide, consult or stop guide on top of today's rule
- Keep the account you used today. We come back to it in DS2 and DS3

## Slide 51

- SUMMARY Summary of today
- Going down finds the cause. Check each answer, and follow each cause separately
- Going up finds what it costs and who cares. That is where KPIs come from
- Propose three levels of KPI. Do not wait for the customer to define them
- Show the numbers to the senior owner every month, in a steering committee
- Escalate problems and opportunities early, in writing, to the right person

## Slide 52

- BACKUP · IF THE 2 6 AUGUST CASE CANNOT BE USED A fictional case: [identity redacted] , a Monday morning
- An AI agent drafts and sends payment reminders
- This case is fictional.
- for a trading company's credit control team
- At 07:00 on Monday, 2,412 customers receive
- reminders. 1,180 receive two. 640 had already paid
- Complaints start at 08:30. Sending is only stopped
- A: Why did customers get two emails? B: Why were customers who had paid chased? C: Why was it released that week? D: Why did it take until 11:15 to stop?
- at 11:15
- Each table gets one starting question. One person
- holds the facts and answers only what you ask
