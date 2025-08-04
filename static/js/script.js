document.addEventListener("DOMContentLoaded", function () {
  // Toast уведомления
  document.querySelectorAll('.toast').forEach(function (toastEl) {
    new bootstrap.Toast(toastEl).show();
  });
});