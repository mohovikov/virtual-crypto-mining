document.addEventListener("DOMContentLoaded", function () {
  // Toast уведомления
  document.querySelectorAll('.toast').forEach(function (toastEl) {
    new bootstrap.Toast(toastEl).show();
  });

  const timeElements = document.querySelectorAll("time.js-datetime[data-utc]");

  timeElements.forEach(el => {
    const utcString = el.dataset.utc;
    if (!utcString) return;

    const isoString = utcString.replace(" ", "T") + "Z";
    const date = new Date(isoString);

    if (isNaN(date)) {
        el.textContent = "Неверная дата";
        return;
    }

    // Локальное отображение (на экране)
    const options = {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
    };
    el.setAttribute("datetime", date.toISOString());

    if (typeof timeAgo !== "undefined") {
      el.textContent = timeago.format(date, "ru")
      el.setAttribute("title", date.toLocaleString(undefined, options))
    } else {
      el.textContent = date.toLocaleString(undefined, options);
    }
  });

  document.querySelectorAll(".js-currency").forEach(el => {
    const raw = el.dataset.price;
    el.textContent = formatCurrencyRUB(raw);
  });
});

function formatCurrencyRUB(value) {
    if (value === null || value === undefined || isNaN(value)) return '—';

    const number = parseFloat(value);
    return new Intl.NumberFormat("ru-RU", {
      style: "currency",
      currency: "RUB",
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(number);
  }

function updatePrivileges() {
  var result = 0;
  $("input:checkbox[name=privilege]:checked").each(function(){
    result = Number(result) + Number($(this).val());
  });

  const UserSponsor = 4
  const UserNormal = 2
  const UserPublic = 1

  var selectValue;
  if (result !== (UserSponsor | UserNormal | UserPublic) ) {
    selectValue = result & ~UserSponsor
  } else {
    selectValue = result;
  }

  $("#privileges-value").val(result);
  $("#privileges-group").val(selectValue);
}

function groupUpdated() {
  var privileges = $("#privileges-group option:selected").val();
  if (privileges > -1) {
    $("input:checkbox[name=privilege]").each(function(){
      if (($(this).val() & privileges) > 0) {
        $(this).prop("checked", true);
      } else {
        $(this).prop("checked", false);
      }
    });
  }
  updatePrivileges();
}