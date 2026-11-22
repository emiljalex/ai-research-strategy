/* Mount once per visit, including offline review navigation. */
function mountInterventionLab() {
  "use strict";
  const panel = document.getElementById("workbench");
  if (!panel || panel.dataset.ready) return;
  panel.dataset.ready = "true";
  const { categories, accounts, initial, summarize, revise } = window.InterventionModel;
  const field = id => panel.querySelector("#" + id);
  let labels = initial();
  let history = [];
  const accountSelect = field("account");
  const labelSelect = field("interpretation");
  const form = field("revision");
  const undo = field("undo");
  const reset = field("reset");
  const announce = message => { field("lab-status").textContent = message; };
  function readAccount() {
    const index = Number(accountSelect.value);
    field("account-quote").textContent = "“" + accounts[index].quote + "”";
    field("current-label").textContent = categories[labels[index]].label;
    labelSelect.value = labels[index];
    field("apply").disabled = true;
  }
  function refresh() {
    const result = summarize(labels);
    field("lab-action").textContent = result.action;
    field("lab-reason").textContent = result.leader ?
      "One interpretation has a unique lead." : "The interpretations are tied.";
    for (const [key, count] of Object.entries(result.counts)) {
      const row = field("count-" + key);
      row.querySelector("output").textContent = count;
      row.querySelector(".meter").style.setProperty("--count", count);
    }
    const log = field("history-list");
    log.replaceChildren();
    for (const entry of [...history].reverse()) {
      const li = document.createElement("li");
      li.textContent = "Account " + entry.account + " · " + categories[entry.from].label + " → " + categories[entry.to].label;
      log.appendChild(li);
    }
    field("empty-log").hidden = history.length > 0;
    undo.disabled = reset.disabled = history.length === 0;
    readAccount();
  }
  accountSelect.addEventListener("change", () => { readAccount(); announce("Inspecting Account " + accounts[Number(accountSelect.value)].id + "."); });
  labelSelect.addEventListener("change", () => {
    field("apply").disabled = labelSelect.value === labels[Number(accountSelect.value)];
  });
  form.addEventListener("submit", event => {
    event.preventDefault();
    const entry = revise(labels, Number(accountSelect.value), labelSelect.value);
    if (!entry) return;
    labels = entry.next;
    history.push(entry);
    refresh();
    announce("Account " + entry.account + " revised. " + summarize(labels).action);
  });
  undo.addEventListener("click", () => {
    const entry = history.pop();
    if (!entry) return;
    labels = entry.previous;
    refresh();
    announce("Undid the change to Account " + entry.account + ". " + summarize(labels).action);
    if (undo.disabled) accountSelect.focus();
  });
  reset.addEventListener("click", () => {
    labels = initial();
    history = [];
    accountSelect.value = "1";
    refresh();
    announce("Restored the original labels and recommendation.");
    accountSelect.focus();
  });
  panel.querySelector(".workbench-controls").hidden = false;
  refresh();
}
mountInterventionLab();
