const yearEl = document.getElementById("year")!;
yearEl.textContent = new Date().getFullYear().toString();


const fBtns = document.querySelectorAll(".fbtn");
const fCards = document.querySelectorAll(".ccard");
fBtns.forEach((b) => {
  b.addEventListener("click", () => {
    const f = b.getAttribute("data-f")!;
    fBtns.forEach((x) => x.classList.remove("on"));
    b.classList.add("on");
    fCards.forEach((c) => {
      const show = f === "all" || c.getAttribute("data-h") === f;
      c.classList.toggle("hidden", !show);
    });
  });
});


const moonph = document.getElementById("moonph")!;
const day: number = new Date().getDate();
const phase: string = day < 8 ? "waxing crescent" : day < 15 ? "full" : day < 23 ? "waning" : "new";
moonph.textContent = phase;

