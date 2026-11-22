---
title: Two clean trials. One unsupported rollout.
description: Two fictional shift swaps cleared a deadline. Widen the proposed pilot by one crew and watch what happens to the recommendation.
kind: Experiment record
status: example
order: 50
series: The rollout rehearsal
---
A product team is considering a shift-swap service. A worker asks a colleague to take a shift. A supervisor has twenty minutes to confirm before the opening expires. In two day-crew rehearsals, the supervisor replied after eight and fourteen minutes. Both swaps met the deadline.

Give those results to a rule and ask whether the day crew can try a pilot. The evidence goes forward to the product owner. Change a single word in the decision, from *day* to *both*. Every source record stays exactly the same. Now the work goes back to the researcher.

This note records a reproducible change in the browser study. The staffing service, people and records are invented. You can inspect every input and replay the difference. [Open the rollout rehearsal.](/lab/rollout-rehearsal/)

## Hold the evidence still

Choose **Day crew** and **Day rehearsals only**. The rule checks whether every crew in the proposed pilot appears in the packet and whether each reply for those crews arrived within twenty minutes. D-01 and D-02 both qualify. The first result is *Ready for the product owner*. It is possible to sign. Simply arriving at this state leaves the pilot unsigned.

Now choose **Both crews**. The engine still reads eight and fourteen minutes. A new row appears for the night crew with no source record. The result becomes *Collect a night rehearsal*. If you had signed the narrow pilot, the signature expires. Switch back to **Day crew** and the earlier signature stays expired. A decision owner has to act again.

That last detail matters. A signature authorizes a particular version of the question. Treat it as a reusable property of the project and a narrow approval can silently become permission for a wider commitment.

## Supply two different night records

Keep **Both crews** selected. Choose **Add a late night reply**. The night crew now appears in the packet. Its reply took thirty-four minutes. The rule sends the work to *Revise the approval step*. Gathering another rehearsal and changing the approval mechanism have different owners and costs. A single red status would erase that distinction.

Next choose **Add an in-time night reply**. This replaces the late alternative with a twelve-minute reply. D-01, D-02 and N-02 now meet the stated condition. The packet can go to the product owner. Press **Authorize this pilot** to see exactly where the human commitment enters the sequence. These alternative packets represent different hypothetical runs. They do not accumulate into a history of the same workers.

One more control is worth trying. Limit the pilot to **Day crew** while retaining the late night record. The night row remains inspectable and reads *Outside scope*. A conspicuous negative observation should neither disappear nor automatically veto an unrelated commitment. The boundary of the decision determines which job that observation can do.

## The unanswered question inside a green result

The rule assumes an in-time supervisory reply is a meaningful proxy for a usable swap. Suppose the worker spends the whole shift away from the device that receives the confirmation. A response at minute twelve could still leave that worker without a workable arrangement. The procedure would pass its tests while the study asked an inadequate question.

A researcher could observe how a worker learns the swap has cleared, whether the colleague can still accept it, and who absorbs the cost when confirmation arrives too late. Those observations might lead the team to measure the worker’s ability to act on a confirmed swap. That would be a change to the research criterion. Switching a packet in this exercise leaves the criterion fixed.

## What carries into real work

The repeatable result is limited and useful. Scope alone can change a handoff. The presence of a record and its suitability are different checks. A human authorization can expire when either its scope or its supporting packet changes. The code and the rows are small enough to inspect independently. [Read the decision rule.](/assets/rollout-model.js)

Whether this arrangement improves a team’s decisions remains an open research question. A field comparison would require real owners, comparable commitments and permission to observe what happens after a recommendation. It would also have to capture the cost of returning work. A system that sends everything back may avoid premature approvals while making a pilot impossible to start. That trade-off belongs in the evaluation.
