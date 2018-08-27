var SHOW_SETTINGS = false;
const SEPARATOR= '-';

function loadstate(cookie) {
  const settings = decodeURIComponent(cookie);
  var main = $("main");
  var element_map = new Map();

  $("main section").each(function() {
    var id = $(this).data('id');
    element_map.set(id, $(this).detach());
  });

  $.each(settings.split(SEPARATOR), function(idx, item) {
    const id = item.slice(0,2);
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

  element_map.forEach((element, id) => {
    main.append(element);
  });
}

function save_state() {
  var settings = $("main section").map(function() {
    var id = $(this).data('id');
    var enabled = $(this).find("input[type='checkbox']").get(0).checked ? 1 : 0;
    return id + enabled;
  }).get().join(SEPARATOR);

  settings = encodeURIComponent(settings);
  document.cookie = "settings=" + settings;
}


$(document).ready(function() {
  const settings_cookie = document.cookie.replace(/(?:(?:^|.*;\s*)settings\s*\=\s*([^;]*).*$)|^.*$/, "$1");
  if (settings_cookie) {
    loadstate(settings_cookie);
  }
});

$("input[type='checkbox']").change(function(){
  save_state();
});

$("#settings").click(function(){
  SHOW_SETTINGS = !SHOW_SETTINGS;
  if (SHOW_SETTINGS) {
    $("section").slideDown(350);
    $(".controls").fadeIn(350);
  } else {
    $("section").has("input[type='checkbox']:not(:checked)").slideUp(350);
    $(".controls").fadeOut(350);
  };
});

$("section .controls button").click(function(){
  const item = $(this).parents("section");
  const animtime = 180;
  if (this.className == "up") {
    item.prev().slideUp(animtime);
    item.slideUp(animtime, function() {
    item.insertBefore(item.prev());
      item.slideDown(animtime);
      item.next().slideDown(animtime);
      save_state();
    });
  } else {
    item.next().slideUp(animtime);
    item.slideUp(animtime, function() {
    item.insertAfter(item.next());
      item.slideDown(animtime);
      item.prev().slideDown(animtime);
      save_state();
    });
  };
});