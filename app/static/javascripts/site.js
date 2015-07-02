var Iffybox = (function ($) {

  var self = {};

  var bindUI = function () {
    $('.site-tabs a').on('click', function (e) {
      e.preventDefault();
      $(this).tab('show');
    });

    $('.btn-reload').on('click', function (e) {
      document.location.reload(true);
    });
  };

  var setupRemote = function () {
    var $form = $('.form-remote');

    $form.on('click', 'button', function (e) {
      var $button = $(this);
      var action = $button.data('action');

      $.ajax({
        type: 'post',
        url: $form.prop('action'),
        data: { action: action },
        dataType: 'json',
        beforeSend: function () {
          $button.button('loading');
        },
        complete: function () {
          $button.button('reset');
        }
      });
    });
  };

  var setupSay = function () {
    var $form = $('.form-say');
    var $submit = $form.find('button');

    $form.on('submit', function (e) {
      e.preventDefault();

      $.ajax({
        type: 'post',
        url: $form.prop('action'),
        data: $form.serialize(),
        dataType: 'json',
        beforeSend: function () {
          $submit.button('loading');
        },
        complete: function () {
          $form.find('input').val('');
          $submit.button('reset');
        }
      });
    });
  };

  self.init = function () {
    bindUI();
    setupRemote();
    setupSay();
  };

  return self;

})(window.jQuery);

$(function () {
  FastClick.attach(document.body);
  Iffybox.init();
});
