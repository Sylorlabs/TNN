// domshim.js — minimal DOM runtime for executing DOM tasks under node.
// Type checking stays against the real lib.dom; this only provides runtime values.
function makeEl(tag, text) {
  return {
    tagName: (tag || "div").toUpperCase(),
    textContent: text === undefined ? "" : text,
    children: [],
    appendChild: function (c) { this.children.push(c); return c; },
  };
}
var store = {
  title: makeEl("h1", ""),
  app: makeEl("div", ""),
};
var liStore = [makeEl("li", "a"), makeEl("li", "b")];
var document = {
  getElementById: function (id) {
    if (id === "title") return store.title;
    if (id === "app") return store.app;
    return null;
  },
  createElement: function (tag) { return makeEl(tag, ""); },
  querySelectorAll: function (sel) {
    if (sel === "li") return liStore.slice();
    return [];
  },
};
if (typeof module !== "undefined") { module.exports = { document: document }; }
