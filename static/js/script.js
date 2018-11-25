'use strict';
const SEPARATOR= '-';

function loadstate() {
  const settings = localStorage.getItem("settings_v1");
  const main = $("main");
  const element_map = new Map();

  $("main section").each(function() {
    const id = $(this).data('id');
    element_map.set(id, $(this).detach());
  });

  $.each(settings.split(SEPARATOR), function(idx, item) {
    const id = item.slice(0, -1);
    const enabled = item.slice(-1) == '1';
    var element;
    if (element_map.has(id)) {
      element = element_map.get(id);
    } else {
      return;
    };
    if (!enabled) {
      element.hide(0);
      element.find("input[type='checkbox']").get(0).checked = false;
    };
    main.append(element);
    element_map.delete(id);
  });

  element_map.forEach(function(element, id) {
    main.append(element);
  });
}

function save_state() {
  var settings = $("main section").map(function() {
    var id = $(this).data('id');
    var enabled = $(this).find("input[type='checkbox']").get(0).checked ? 1 : 0;
    return id + enabled;
  }).get().join(SEPARATOR);

  localStorage.setItem("settings_v1", settings);
}

$(document).ready(function() {
  if (localStorage.getItem("settings_v1") !== null) {
    loadstate();
  }

  $('main,footer').css('display', 'flex');
});

$(".left-controls input[type='checkbox']").change(function(){
  save_state();
});

$("#settings").click(function(){
  $("section").has("input[type='checkbox']:not(:checked)").slideToggle(350);
  $("section a,.left-controls").toggle();
  $(".right-controls,#reset").fadeToggle(350);
  $("#settings").toggleClass("settings-active");
});

$(".right-controls button").click(function(){
  const item = $(this).parents("section");
  const fadeintime = 540;
  const fadeouttime = 460;

  if (this.className == "up" && item.prev().length > 0) {
    item.fadeOut(fadeouttime, function() {
      item.insertBefore(item.prev()).addClass("fade").fadeIn(fadeintime, function(){
        item.removeClass('fade');
        save_state();
      });
    });
  } else if(this.className == "down" && item.next().length > 0) {
    item.fadeOut(fadeouttime, function() {
      item.insertAfter(item.next()).addClass("fade").fadeIn(fadeintime, function(){
        item.removeClass('fade');
        save_state();
      });
    });
  };
});

$("#reset").click(function(){
  localStorage.removeItem("settings_v1");
  location.reload();
});