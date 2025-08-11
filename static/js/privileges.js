function updatePrivileges() {
  var result = 0
  $("input:checkbox[name=privilege]:checked").each(function(){
    result = Number(result) + Number($(this).val())
  })

  var UserSponsor = 4
  var UserNormal = 2
  var UserPublic = 1

  // Remove donor if needed
  var selectValue
  if (result != UserSponsor | UserNormal | UserPublic) {
    selectValue = result & ~UserSponsor
  } else {
    selectValue = result
  }

  $("#privileges_value").val(result)
  $("#privileges-group").val(selectValue)
}

function groupUpdated() {
  var privileges = $("#privileges-group option:selected").val()
  if (privileges > -1) {
    $("input:checkbox[name=privilege]").each(function(){
      if ( ($(this).val() & privileges) > 0) {
        $(this).prop("checked", true)
      } else {
        $(this).prop("checked", false)
      }
    })
  }
  updatePrivileges();
}