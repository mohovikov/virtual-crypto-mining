import * as bootstrap from 'bootstrap'
import { format, register } from "timeago.js"
import ru from "timeago.js/lib/lang/ru"

register('ru', ru)

function initTimeago() {
  document.querySelectorAll('time.js-timeago').forEach(el => {
    let utcDateTime = el.dataset.utc
    if (!utcDateTime) return

    let isoString = utcDateTime.replace(' ', 'T').split('.')[0] + 'Z'
    let datetime = new Date(isoString)

    el.innerText = format(datetime, 'ru')

    const tooltip = new bootstrap.Tooltip(el, {
      title: datetime.toLocaleString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
        hour12: false,
        timeZoneName: 'short'
      }),
      trigger: 'hover'
    })

    tooltip.enable()
  })
}

window.initTimeago = initTimeago