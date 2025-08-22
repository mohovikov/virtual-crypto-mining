const { format } = timeago

document.querySelectorAll('.toast').forEach(function (toastEl, index) {
    let delay = 3000 + (index * 500)
    let toast = new bootstrap.Toast(toastEl, { delay: delay })
    toast.show()
})

document.querySelectorAll('time.js-datetime').forEach(el => {
  let utcStr = el.dataset.utc

  let isoStr = utcStr.replace(' ', 'T').split('.')[0] + 'Z'
  let date = new Date(isoStr)

  let options = {
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit'
  }
  el.textContent = date.toLocaleString(undefined, options)
})

document.querySelectorAll('time.js-timeago').forEach(el => {
  let utcStr = el.dataset.utc
  if (!utcStr) return

  let isoString = utcStr.replace(' ', 'T').split('.')[0] + 'Z'
  let date = new Date(isoString)

  el.textContent = format(date, 'ru')
})

document.querySelectorAll('span.js-price').forEach(el => {
  const price = parseFloat(el.dataset.price)

  el.textContent = price.toLocaleString("ru-RU", {
    style: "currency",
    currency: "RUB"
  })
})

$(function() {
  function updateOutput() {
    const bbcode = $("#userpage").val()
    const html = bbcodeToHtml(bbcode)
    $("#userpage-preview").html(html)
  }

  // Первичная инициализация
  updateOutput()

  // Автообновление при вводе
  $("#userpage").on("input", updateOutput)
})

async function loadChart(url) {
  const response = await fetch(url)
  const data = await response.json()

  const labels = data.map(item => {
    let isoStr = item.timestamp.replace(' ', 'T').split('.')[0] + 'Z'
    let date = new Date(isoStr)
    let options = {
      year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit', second: '2-digit'
    }
    return date.toLocaleString(undefined, options)
  })
  const prices = data.map(item => item.price)

  const ctx = document.getElementById("priceChart").getContext("2d")
  new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [{
        label: "Цена",
        data: prices,
        borderColor: "blue",
        borderWidth: 2,
        fill: false,
        tension: 0.1
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: true },
        title: {
          display: true,
          text: 'График курса валюты'
        }
      },
      scales: {
        x: { title: { display: true, text: "Время" }},
        y: { title: { display: true, text: "Стоимость" }}
      }
    }
  })
}