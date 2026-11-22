function mountRollout() {
  "use strict";
  const node = document.querySelector("[data-rollout]");
  if (!node || node.dataset.mounted) return;
  node.dataset.mounted = "true";
  const model = window.RolloutModel;
  let state = { scope: "both", packet: "day", signed: false };
  const choices = [...node.querySelectorAll("[data-scope]")];
  const picker = node.querySelector("[data-packet]");
  const signature = node.querySelector("[data-sign]");
  const titles = { collect: "Collect a night rehearsal", revise: "Revise the approval step", owner: "Ready for the product owner" };
  const reasons = {
    collect: "The pilot includes the night crew. The packet contains only day rehearsals.",
    revise: "The night reply took 34 minutes. The swap had already closed at 20.",
    owner: "Every crew in scope has a rehearsal inside the 20-minute window. The owner can now decide."
  };
  function paint() {
    const result = model.evaluate(state.scope, state.packet);
    choices.forEach(button => button.setAttribute("aria-pressed", String(button.dataset.scope === state.scope)));
    node.querySelector("[data-title]").textContent = state.signed ? "Pilot authorized in this rehearsal" : titles[result.route];
    node.querySelector("[data-reason]").textContent = state.signed ? "The product owner accepted this scope and evidence packet. Changing either reopens the decision." : reasons[result.route];
    node.querySelector("[data-outcome]").dataset.route = state.signed ? "signed" : result.route;
    const marker = node.querySelector("[data-mark]");
    marker.textContent = state.signed ? "Signed" : { collect: "Gap", revise: "Late", owner: "Ready" }[result.route];
    const rows = node.querySelector("[data-rows]");
    rows.replaceChildren();
    function append(cells) {
      const row = document.createElement("tr");
      cells.forEach(value => { const cell = document.createElement("td"); cell.textContent = value; row.append(cell); });
      rows.append(row);
    }
    result.rows.forEach(row => append([row.id, row.crew, row.minutes + " min", !row.inScope ? "Outside scope" : row.minutes > model.windowMinutes ? "Too late" : "In time"]));
    result.missing.forEach(crew => append(["Pending", crew, "No record", "Missing"]));
    if (signature) {
      signature.disabled = result.route !== "owner" || state.signed;
      node.querySelector("[data-owner]").textContent = state.signed ? "Authorization recorded for this run." : result.route === "owner" ? "Awaiting an explicit human decision." : "Awaiting the research check.";
    }
  }
  choices.forEach(button => button.addEventListener("click", () => { state = model.change(state, button.dataset.scope, state.packet); paint(); }));
  if (picker) picker.addEventListener("change", () => { state = model.change(state, state.scope, picker.value); paint(); });
  if (signature) signature.addEventListener("click", () => { state = model.authorize(state); paint(); });
  node.querySelectorAll("[data-control]").forEach(control => { control.hidden = false; });
  paint();
}
if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mountRollout);
else mountRollout();
