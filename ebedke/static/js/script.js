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
  if(!localStorage_available) {
    $("#settings").hide();
  } else {
    if (localStorage.getItem("settings_v1") !== null) {
      loadstate();
    }
  }
  $('main,footer').css('display', 'flex');
  $.ajaxSetup({ cache: true });
  $.getScript('https://connect.facebook.net/hu_HU/sdk.js', function() {
    FB.init({
      appId: '1478465105546610',
      version: 'v7.0'
    });
    initFacebookPlugins(false);
  }).fail(function() {
    initFacebookPlugins(true);
  });
});

function initFacebookPlugins(noFB) {
  var noFBparagraph = $('<p class="noFBwarning">A böngésződ nem tölti be a beágyazott facebook tartalmakat. Ezt okozhatja átlagosnál szigorúbb biztonsági beállítás vagy egy reklámblokkoló is. Az étterem facebook oldalát eléred a nevére kattintva.</p>');
  $("main section").each(function() {
    const a = $("a", this).get(0);
    const isFacebookPage = a.host == "www.facebook.com";
    if (isFacebookPage) {
      const section = $(this);
      const href = a.href;
      const text = a.text;
      var fbdiv = $('<div class="fb-frame"><div class="fb-page" data-href=' + href + '" data-tabs="timeline" data-width="500" data-height="" data-small-header="true" data-adapt-container-width="true" data-hide-cover="true" data-show-facepile="false" data-hide-cta="false"><blockquote cite="' + href + '" class="fb-xfbml-parse-ignore"><a href="'+ href +'">' + text + '</a></blockquote></div></div>').hide();
      var button = $('<button>facebook oldal betöltése</button>').click(function() {
        if (noFB) {
          section.append(noFBparagraph.clone());
        } else {
          section.append(fbdiv);
          fbdiv.slideToggle()
          FB.XFBML.parse(fbdiv.get(0));
        }
        $(this).remove();
      });
      section.append(button);
    }
  });
}

$(".left-controls input[type='checkbox']").change(function(){
  save_state();
});

$("#settings").click(function(){
  $("section").has("input[type='checkbox']:not(:checked)").slideToggle(350);
  $("section a,.left-controls").toggle();
  $(".right-controls,#reset").fadeToggle(350);
  $("#settings").toggleClass("settings-active");
  var text = $('#settings').text();
  $('#settings').text(text == "⇕ Átrendezés" ? "Kész" : "⇕ Átrendezés");
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

function localStorage_available() {
  try {
      var storage = window[localStorage],
          x = '__storage_test__';
      storage.setItem(x, x);
      storage.removeItem(x);
      return true;
  }
  catch(e) {
      return false;
  }
}
