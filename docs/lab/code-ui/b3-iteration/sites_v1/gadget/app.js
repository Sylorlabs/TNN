"use strict";
const yearEl = document.getElementById("year");
yearEl.textContent = new Date().getFullYear().toString();
class Counter {
    constructor() {
        this.count = 0;
    }
    change(d) {
        this.count = this.count + d;
        return this.count;
    }
}
const counter = new Counter();
const cval = document.getElementById("cval");
const cinc = document.getElementById("cinc");
const cdec = document.getElementById("cdec");
cinc.addEventListener("click", () => {
    cval.textContent = counter.change(1).toString();
});
cdec.addEventListener("click", () => {
    cval.textContent = counter.change(-1).toString();
});
const accItems = document.querySelectorAll(".acc-item");
accItems.forEach((it) => {
    const btn = it.querySelector(".acc-q");
    btn.addEventListener("click", () => {
        it.classList.toggle("open");
    });
});
const tabBtns = document.querySelectorAll(".tab-btn");
const tabPanes = document.querySelectorAll(".tab-pane");
tabBtns.forEach((b) => {
    b.addEventListener("click", () => {
        tabBtns.forEach((x) => x.classList.remove("on"));
        tabPanes.forEach((x) => x.classList.remove("on"));
        b.classList.add("on");
        const pane = document.getElementById(b.getAttribute("data-tab"));
        pane.classList.add("on");
    });
});
const todoInput = document.getElementById("tin");
const todoAdd = document.getElementById("tadd");
const todoList = document.getElementById("tlist");
todoAdd.addEventListener("click", () => {
    const text = todoInput.value.trim();
    if (text.length === 0) {
        return;
    }
    const li = document.createElement("li");
    li.textContent = text;
    todoList.appendChild(li);
    todoInput.value = "";
});
