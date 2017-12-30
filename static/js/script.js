function remove_hidden() {
  const hidden = new Set(decodeURIComponent(window.location.hash || '=').split('=')[1].split(';'));
  const sections = document.querySelectorAll(".menu > section");
  sections.forEach(function(section) {
    if (hidden.has(section.querySelector("span").dataset.name)) {
      section.remove();
      document.querySelector('body > header > a').style.display = "block";
    }
  });
}

function init_header() {
  const today = new Date();
  const options = { weekday: "long", year: "numeric", month: "numeric", day: "numeric" };
  const [date, day] = today.toLocaleDateString('hu-HU', options).split(', ');
  document.querySelector("body > header h1").innerText = day;
  document.querySelector("body > header span").innerText = date;
  document.querySelector("body > header").style.display = "flex";
}

function add_close_listeners() {
  const spans = document.querySelectorAll(".close");
  spans.forEach(function(element) {
    element.addEventListener('click', function() {
      name = this.dataset.name;
      this.parentElement.parentElement.remove();
      window.location.hash = `${ window.location.hash || "hide=" }${ name };`
      document.querySelector('body > header > a').style.display = "block";
    });
  });
}

function main() {
  remove_hidden();
  add_close_listeners();
  init_header();
}

main();