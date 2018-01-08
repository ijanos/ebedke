function remove_hidden() {
  const hidden = new Set(decodeURIComponent(window.location.hash || '=').split('=')[1].split(';'));
  const sections = document.querySelectorAll(".menu > section");
  sections.forEach(function(section) {
    if (hidden.has(section.querySelector("span.close").dataset.name)) {
      section.remove();
      document.querySelector('body > header > a').style.display = "block";
    }
  });
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
}

main();