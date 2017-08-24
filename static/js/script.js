function add_menu(menujson) {
    const menu = document.querySelector('.menu');
    var items;
    if (window.location.hash) {
      items = new Set(window.location.href.split('=')[1].split(';'));
    } else {
      items = new Set()
    }
    menujson.map(function(restaurant) {
      if (!items.has(restaurant['name'])) {
        var section = document.createElement('section');
        var content = `<header><h2><a href="${ restaurant['url'] }">${ restaurant['name'] }</a></h2><span class="close" data-name="${ restaurant['name'] }">❌</span></header><p>${ restaurant['menu'] }</p><hr>`;
        section.innerHTML = content;
        menu.appendChild(section);
      }
    });
    if (window.location.hash) {
        var section = document.createElement('section');
        section.innerHTML = '<a href="/">mutass mindent</a>';
        menu.appendChild(section)
    }
}

function get_menu() {
    fetch(new Request('/menu'))
      .then(function(response) {
        return response.json()
      }).then(function(json) {
        add_menu(json)
      }).then(function() {
        init_close();
        document.querySelector('.loading').remove();
      }).catch(function(ex) {
        document.querySelector('.loading').innerText = "Valami elromlott :("
        console.log('parsing failed', ex)
      });
}

function close_func() {
  name = this.dataset.name;
  this.parentElement.parentElement.remove();
  if (window.location.hash) {
    window.location.hash += `;${ name }`
  } else {
    window.location.hash = `hide=${ name }`
  }
}

function init_close() {
  var Xes = document.getElementsByClassName("close");
  Array.from(Xes).forEach(function(element) {
    element.addEventListener('click', close_func);
  });
}

get_menu();