function add_menu(menujson) {
    const menu = document.querySelector('.menu');
    const hidden = new Set(decodeURIComponent(window.location.hash || '=').split('=')[1].split(';'));
    menujson.map(function(restaurant) {
      if (!hidden.has(restaurant.name)) {
        let section = document.createElement('section');
        section.innerHTML = `<header>
           <h2><a href="${ restaurant.url }">${ restaurant.name }</a></h2>
           <span class="close" data-name="${ restaurant.name }">✕</span>
           </header>
           <p>${ restaurant.menu }</p><hr>`;
        menu.appendChild(section);
      }
    });
    if (window.location.hash) {
      document.querySelector('body > header > a').style.display = "block";
    }
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
  let infobox = document.querySelector('.loading');
  fetch(new Request('/menu'))
    .then(function(response) {
      return response.json()
    }).then(function(json) {
      add_menu(json)
    }).then(function() {
      add_close_listeners();
      infobox.remove();
      init_header();
    }).catch(function(ex) {
      infobox.innerText = "Valami elromlott :("
      console.log('parsing failed', ex)
    });
}

main();