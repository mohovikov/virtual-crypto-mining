document.querySelectorAll('.js-datetime').forEach(el => {
  let utcStr = el.dataset.utc

  let isoStr = utcStr.replace(' ', 'T').replace(/\.\d+$/, '') + 'Z'
  let date = new Date(isoStr)

  let options = {
      year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit', second: '2-digit'
  }
  el.textContent = date.toLocaleString(undefined, options)
})