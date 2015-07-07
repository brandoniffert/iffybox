var Iffybox = (function (request) {

  var self = {};

  var bindUI = function () {
    document.querySelector('.btn-reload').addEventListener('click', function (e) {
      console.log('here');
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
    var $form = document.querySelector('.form-say');
    var $submit = $form.querySelector('button[type=submit]');

    $form.addEventListener('submit', function (e) {
      e.preventDefault();

      if ($form.message.value === '') return;

      $submit.setAttribute('disabled', true);

      request
        .post($form.getAttribute('action'))
        .type('form')
        .send({ message: $form.message.value, voice: $form.voice.value })
        .end(function (err, res) {
          $form.querySelector('input[type=text]').value = '';
          $submit.removeAttribute('disabled');
        });
    });
  };

  self.init = function () {
    bindUI();
    // setupRemote();
    setupSay();
  };

  return self;

})(window.superagent);

window.onload = function () {
  FastClick.attach(document.body);
  Iffybox.init();
};
