const { test } = require("node:test");
const assert = require("node:assert/strict");
const { accounts, categories, initial, revise, summarize } = require("../assets/lab-model.js");

test("the bench note can be replayed and undone from the fixture", () => {
  const starting = initial();
  assert.equal(summarize(starting).leader, "entrance");
  const revision = revise(starting, 1, "hours");
  assert.equal(revision.account, "B");
  assert.deepEqual(summarize(revision.next).counts, { entrance: 1, hours: 1, expiry: 1 });
  assert.equal(summarize(revision.next).action, "Collect another account before choosing a change.");
  assert.deepEqual(revision.previous, initial());
  assert.deepEqual(starting, initial());
});

test("the declared rule holds for every possible labeling of the fixture", () => {
  const keys = Object.keys(categories);
  for (const a of keys) for (const b of keys) for (const c of keys) {
    const labels = [a, b, c];
    const { counts, leader } = summarize(labels);
    const uniqueLead = labels.find(key => labels.filter(item => item === key).length >= 2);
    assert.equal(leader, uniqueLead || null);
    assert.equal(Object.values(counts).reduce((total, n) => total + n, 0), accounts.length);
  }
});

test("an unchanged edit has no history entry and a second edit preserves the intermediate state", () => {
  assert.equal(revise(initial(), 0, "entrance"), null);
  const first = revise(initial(), 1, "hours");
  const second = revise(first.next, 0, "expiry");
  assert.equal(summarize(second.next).leader, "expiry");
  assert.deepEqual(second.previous, first.next);
  assert.throws(() => revise(initial(), 6, "expiry"), RangeError);
});
