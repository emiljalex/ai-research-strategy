const { test } = require("node:test");
const assert = require("node:assert/strict");
const { evaluate, change, authorize } = require("../assets/rollout-model.js");

test("every scope and packet has the documented route", () => {
  const expected = { day: ["owner", "owner", "owner"], both: ["collect", "revise", "owner"] };
  for (const scope of Object.keys(expected)) {
    assert.deepEqual(["day", "late", "timely"].map(packet => evaluate(scope, packet).route), expected[scope]);
  }
  assert.deepEqual(evaluate("both", "day").missing, ["Night"]);
  assert.deepEqual(evaluate("both", "late").late.map(r => r.id), ["N-01"]);
});

test("narrowing preserves the out-of-scope record and never mutates its source", () => {
  const row = evaluate("day", "late").rows[2];
  assert.deepEqual(row, { id: "N-01", crew: "Night", minutes: 34, inScope: false });
  row.minutes = 1;
  assert.equal(evaluate("both", "late").rows[2].minutes, 34);
});

test("a passing packet requires a separate human action and a change clears it", () => {
  const initial = { scope: "day", packet: "day", signed: false };
  const signed = authorize(initial);
  assert.equal(initial.signed, false);
  assert.equal(signed.signed, true);
  assert.equal(change(signed, "day", "day"), signed);
  for (const [scope, packet] of [["both", "day"], ["day", "late"]]) {
    const changed = change(signed, scope, packet);
    assert.equal(changed.signed, false);
    assert.equal(change(changed, "day", "day").signed, false);
  }
});

test("incomplete or late evidence cannot be authorized and unknown inputs are rejected", () => {
  for (const packet of ["day", "late"]) assert.equal(authorize({ scope: "both", packet, signed: false }).signed, false);
  assert.throws(() => evaluate("all", "day"), RangeError);
  assert.throws(() => evaluate("day", "__proto__"), RangeError);
});
