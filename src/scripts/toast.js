import * as bootstrap from 'bootstrap'

document.querySelectorAll('.toast').forEach(function (toastEl, index) {
  let delay = 3000 + (index * 500)
  let toast = new bootstrap.Toast(toastEl, { delay: delay })
  toast.show()
})

export function showToast(message, type = "success") {
  const container = document.querySelector(".toast-container")
  if (!container) return

  // Словарь категорий как в шаблоне
  const categories = {
    success: { icon: "fa-circle-check", title: "Успех" },
    info:    { icon: "fa-info-circle", title: "Информация" },
    danger:  { icon: "fa-triangle-exclamation", title: "Ошибка" },
    warning: { icon: "fa-exclamation-triangle", title: "Внимание" }
  }

  const { icon, title } = categories[type] || categories.info

  const toastEl = document.createElement("div")
  toastEl.className = `toast text-bg-${type}`
  toastEl.setAttribute("role", "alert")
  toastEl.setAttribute("aria-live", "assertive")
  toastEl.setAttribute("aria-atomic", "true")

  toastEl.innerHTML = `
    <div class="toast-header">
      <i class="fa-solid ${icon} me-2"></i>
      <strong class="me-auto">${title}</strong>
      <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
    <div class="toast-body">${message}</div>
  `

  container.append(toastEl)

  const toast = new bootstrap.Toast(toastEl, { delay: 5000 })
  toast.show()

  toastEl.addEventListener("hidden.bs.toast", () => {
    toastEl.remove()
  })
}
