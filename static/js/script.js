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