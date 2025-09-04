function updatePrivileges() {
  let result = 0

  document.querySelectorAll('input[type="checkbox"][name="privilege"]:checked').forEach(cb => {
    result += Number(cb.value)
  })

  document.querySelector('#privileges_value').value = result
  document.querySelector('#privileges-group').value = result
}

function groupUpdated() {
  const groupSelect = document.querySelector('#privileges-group')
  const privileges = Number(groupSelect.value)

  if (privileges > -1) {
    document.querySelectorAll('input[type="checkbox"][name="privilege"]').forEach(cb => {
      cb.checked = (Number(cb.value) & privileges) > 0
    })
  }

  updatePrivileges()
}

window.updatePrivileges = updatePrivileges
window.groupUpdated = groupUpdated