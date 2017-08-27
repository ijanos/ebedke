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
        var section = document.createElement('section');
        section.innerHTML = '<a href="/">mutass mindent</a>';
        menu.appendChild(section)
    }
}

function add_close_listeners() {
  const spans = document.querySelectorAll(".close");
  spans.forEach(function(element) {
    element.addEventListener('click', function() {
      name = this.dataset.name;
      this.parentElement.parentElement.remove();
      window.location.hash = `${ window.location.hash || "hide=" }${ name };`
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
    }).catch(function(ex) {
      infobox.innerText = "Valami elromlott :("
      console.log('parsing failed', ex)
    });
}

main();