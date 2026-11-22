"""Shared HTML for the small homepage instrument and the full rollout rehearsal."""

ROUTE = "/lab/rollout-rehearsal/"
NOTE = "/field-notes/two-clean-trials/"


def instrument(full=False):
    packet = '''<label class="instrument-choice" for="packet">Evidence packet</label><select data-control hidden id="packet" data-packet>
<option value="day">Day rehearsals only</option><option value="late">Add a late night reply</option><option value="timely">Add an in-time night reply</option></select>''' if full else ''
    owner = '''<div class="signoff"><div><span class="slip-label">Product owner</span><p data-owner>Awaiting the research check.</p></div>
<button type="button" data-sign data-control hidden disabled>Authorize this pilot</button></div>''' if full else ''
    link = f'<a class="instrument-link" href="{NOTE}">Read the experiment record <span aria-hidden="true">↗</span></a>' if full else f'<a class="instrument-link" href="{ROUTE}">Open the full rehearsal <span aria-hidden="true">↗</span></a>'
    return f'''<section class="instrument" data-rollout aria-label="Interactive shift-swap rehearsal">
<div class="instrument-top"><span class="instrument-label">Decision rehearsal</span><span class="fixture-indicator">Synthetic</span></div>
<h2>Who gets the pilot?</h2><p class="instrument-intro">A shift swap expires after 20 minutes. Both day rehearsals finished in time. Which crews can the team include?</p>
<div class="instrument-settings"><div><span class="instrument-choice" id="scope-title">Pilot scope</span><div class="switch" role="group" aria-labelledby="scope-title" data-control hidden>
<button data-scope="day" aria-pressed="false" type="button">Day crew</button><button data-scope="both" aria-pressed="true" type="button">Both crews</button></div></div><div>{packet}</div></div>
<table class="evidence-table"><caption class="sr-only">Evidence checked against the selected pilot scope</caption><thead><tr><th>Record</th><th>Crew</th><th>Reply</th><th>Check</th></tr></thead>
<tbody data-rows><tr><td>D-01</td><td>Day</td><td>8 min</td><td>In time</td></tr><tr><td>D-02</td><td>Day</td><td>14 min</td><td>In time</td></tr><tr><td>Pending</td><td>Night</td><td>No record</td><td>Missing</td></tr></tbody></table>
<div class="result-slip" data-outcome data-route="collect" role="status" aria-live="polite" aria-atomic="true"><div class="slip-header"><span class="slip-label">Next action</span><span class="stamp" data-mark>Gap</span></div><h3 data-title>Collect a night rehearsal</h3><p data-reason>The pilot includes the night crew. The packet contains only day rehearsals.</p></div>{owner}{link}
<noscript><p class="instrument-noscript">This is the initial result. The experiment record describes every outcome.</p></noscript></section>'''


def rehearsal():
    return f'''<div class="wrap"><header class="section-intro lab-intro"><div><a class="back-link" href="/lab/">Lab</a><h1>The rollout rehearsal</h1><p class="standfirst">Two clean trials can support a narrow pilot. Widen the decision and the same evidence can send the work back.</p></div><p class="lab-context">A browser-based study of evidence coverage, handoffs and decision rights. All records are fictional. The rule runs locally.</p></header>
<div class="rehearsal-grid"><div>{instrument(True)}</div><aside class="protocol"><p class="section-label">How to run the study</p><h2>Separate three jobs.</h2>
<ol><li><strong>Frame the decision.</strong> Act as the researcher. Choose which crews the pilot would cover. Keep the 20-minute expiry fixed.</li>
<li><strong>Check the record.</strong> The rule matches each crew to a rehearsal and flags late replies. Try the two alternative night records.</li>
<li><strong>Authorize a bounded pilot.</strong> Take the product owner’s role. Only an explicit click signs the current packet. Change either input and that signature expires.</li></ol>
<h3>What would break the inference?</h3><p>A recorded reply could arrive in time while the worker is unable to act on it. The rule cannot discover that omission. Someone must question the criterion itself.</p>
<a class="text-link" href="/assets/rollout-model.js" download="rollout-model.js">Inspect the records and rule</a></aside></div>
<div class="lab-after"><h2>What this study establishes</h2><div><p>A fixed check can route the same evidence differently when the proposed commitment changes. The signature belongs to a particular scope and packet. The result establishes how this mechanism behaves on its fixtures. Staffing policy and research validity require evidence from actual workers and decision owners.</p><a class="text-link" href="{NOTE}">Reproduce the three outcomes</a></div></div></div>'''
