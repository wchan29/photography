document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".collapse-button").forEach((btn) => {
    btn.addEventListener("click", () => {
      const controlsId = btn.getAttribute("aria-controls");
      const content = document.getElementById(controlsId);
      const expanded = btn.getAttribute("aria-expanded") === "true";

      btn.setAttribute("aria-expanded", String(!expanded));

      if (content) {
        content.classList.toggle("is-collapsed", expanded);
      }
    });
  });
});