import * as bootstrap from 'bootstrap'
import { showToast } from '../toast'

function initDeleteWithModal(modalId) {
  const modal = document.getElementById(modalId)
  if (!modal) return

  const deleteTypeSpan = modal.querySelector("#delete-type")
  const confirmBtn = modal.querySelector("#confirmDeleteBtn")

  let deleteUrl = null
  let rowId = null

  modal.addEventListener("show.bs.modal", (event) => {
    const button = event.relatedTarget
    deleteUrl = button.getAttribute("data-url")
    rowId = button.getAttribute("data-row")

    deleteTypeSpan.textContent =
      rowId === "row-avatar" ? "аватар" : "фон"
  })

  confirmBtn.addEventListener("click", () => {
    fetch(deleteUrl, {
      method: "POST",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json"
      }
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        document.getElementById(rowId)?.remove()

        const modalInstance = bootstrap.Modal.getInstance(modal)
        modalInstance.hide()

        showToast(data.message, data.category)
      } else {
        showToast(data.message, data.category)
      }
    })
    .catch((err) => {
      console.error("Ошибка fetch:", err);
      showToast("Ошибка сети, попробуйте снова", "warning")
    })
  })
}

window.initDeleteWithModal = initDeleteWithModal