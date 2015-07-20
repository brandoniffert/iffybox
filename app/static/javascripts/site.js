var Iffybox = (function (request) {

  var self = {};

  var bindUI = function () {
    document.querySelector('.btn-reload').addEventListener('click', function (e) {
      document.location.reload(true);
    });
  };

  var setupRemote = function () {
    var $form = document.querySelector('.form-remote');

    $form.addEventListener('click', function (e) {
      if (e.target && (e.target.getAttribute('data-action') || e.target.parentNode.getAttribute('data-action'))) {
        var action = e.target.getAttribute('data-action') || e.target.parentNode.getAttribute('data-action');

        request
          .post($form.getAttribute('action'))
          .type('form')
          .send({ action: action })
          .end();
      }
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
        .send({ message: $form.message.value })
        .end(function (err, res) {
          $form.querySelector('input[type=text]').value = '';
          $submit.removeAttribute('disabled');
        });
    });
  };

  self.init = function () {
    bindUI();
    setupRemote();
    setupSay();
  };

  return self;

})(window.superagent);

window.onload = function () {
  FastClick.attach(document.body);
  Iffybox.init();
};
