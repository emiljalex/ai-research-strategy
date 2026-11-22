/* The fixture and rule are intentionally deterministic and inspectable. */
(function (root) {
  "use strict";
  const categories = Object.freeze({
    entrance: { label: "Finding the entrance", action: "Test an entrance cue in the pickup notice." },
    hours: { label: "Opening hours", action: "Ask when readers can collect their holds." },
    expiry: { label: "Hold expiration", action: "Test a clearer reminder before a hold expires." }
  });
  const accounts = Object.freeze([
    { id: "A", quote: "I came back twice because the pickup notice didn’t say which entrance to use.", initial: "entrance" },
    { id: "B", quote: "I found the entrance. I still left because I could only come after six.", initial: "entrance" },
    { id: "C", quote: "The side desk was open, but my hold had already expired.", initial: "expiry" }
  ]);
  const initial = () => accounts.map(account => account.initial);
  function summarize(labels) {
    const counts = Object.fromEntries(Object.keys(categories).map(key => [key, 0]));
    for (const key of labels) counts[key] += 1;
    const highest = Math.max(...Object.values(counts));
    const leaders = Object.keys(categories).filter(key => counts[key] === highest);
    const leader = leaders.length === 1 ? leaders[0] : null;
    return { counts, leader, action: leader ? categories[leader].action : "Collect another account before choosing a change." };
  }
  function revise(labels, index, value) {
    if (!Number.isInteger(index) || index < 0 || index >= accounts.length || !Object.hasOwn(categories, value)) {
      throw new RangeError("Choose an account and one of the available labels.");
    }
    if (labels[index] === value) return null;
    const next = labels.slice();
    next[index] = value;
    return { next, previous: labels.slice(), account: accounts[index].id, from: labels[index], to: value };
  }
  const model = { categories, accounts, initial, summarize, revise };
  if (typeof module !== "undefined" && module.exports) module.exports = model;
  else root.InterventionModel = model;
}(typeof window === "undefined" ? this : window));
