// Dawn — demo countdown. Deterministic: fixed 25-minute demo, 1s tick.
(function () {
  var DURATION = 25 * 60;
  var remaining = DURATION;
  var running = false;
  var timer = null;
  var timeEl = document.getElementById("demo-time");
  var statusEl = document.getElementById("demo-status");
  var btn = document.getElementById("demo-btn");

  function fmt(s) {
    var m = Math.floor(s / 60), sec = s % 60;
    return (m < 10 ? "0" + m : "" + m) + ":" + (sec < 10 ? "0" + sec : "" + sec);
  }
  function render() { timeEl.textContent = fmt(remaining); }
  function tick() {
    if (remaining > 0) { remaining -= 1; render(); }
    if (remaining === 0) {
      clearInterval(timer); running = false;
      statusEl.textContent = "session complete — well done";
      btn.textContent = "Start again";
    }
  }
  btn.addEventListener("click", function () {
    if (running) {
      clearInterval(timer); running = false;
      statusEl.textContent = "paused — press the button to resume";
      btn.textContent = "Resume timer";
      return;
    }
    if (remaining === 0) { remaining = DURATION; }
    running = true;
    statusEl.textContent = "focusing… stay with it";
    btn.textContent = "Pause timer";
    timer = setInterval(tick, 1000);
  });
  render();
})();
