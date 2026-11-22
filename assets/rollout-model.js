/* A deterministic rehearsal. Every row and role belongs to a fictional shift-swap pilot. */
(function (scope) {
  "use strict";
  const windowMinutes = 20;
  const dayRows = [
    { id: "D-01", crew: "Day", minutes: 8 },
    { id: "D-02", crew: "Day", minutes: 14 }
  ];
  const packets = {
    day: dayRows,
    late: [...dayRows, { id: "N-01", crew: "Night", minutes: 34 }],
    timely: [...dayRows, { id: "N-02", crew: "Night", minutes: 12 }]
  };

  function evaluate(scopeName, packet) {
    if (!["day", "both"].includes(scopeName) || !Object.hasOwn(packets, packet)) {
      throw new RangeError("Unknown pilot scope or evidence packet");
    }
    const crews = scopeName === "both" ? ["Day", "Night"] : ["Day"];
    const rows = packets[packet].map(row => ({ ...row, inScope: crews.includes(row.crew) }));
    const missing = crews.filter(crew => !rows.some(row => row.crew === crew));
    const late = rows.filter(row => row.inScope && row.minutes > windowMinutes);
    const route = late.length ? "revise" : missing.length ? "collect" : "owner";
    return { crews, rows, missing, late, route };
  }

  function change(state, scopeName, packet) {
    evaluate(scopeName, packet);
    if (state.scope === scopeName && state.packet === packet) return state;
    return { scope: scopeName, packet, signed: false };
  }

  function authorize(state) {
    return evaluate(state.scope, state.packet).route === "owner" ? { ...state, signed: true } : state;
  }

  const model = { windowMinutes, evaluate, change, authorize };
  if (typeof module !== "undefined" && module.exports) module.exports = model;
  else scope.RolloutModel = model;
})(typeof globalThis !== "undefined" ? globalThis : this);
