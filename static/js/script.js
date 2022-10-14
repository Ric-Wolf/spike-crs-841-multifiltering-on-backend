$(document).ready(function () {
  // dropdown box
  $("#dp0").change(function () {
    $.getJSON("/_dp", getDictForPython("member")).success(function (result) {
      updateDropdowns(result), applyColorDropdowns(result);
    });
  });
  //end dp

  //dropdown box
  $("#dp1").change(function () {
    $.getJSON("/_dp", getDictForPython("language")).success(function (result) {
      updateDropdowns(result), applyColorDropdowns(result);
    });
  });
  //end dp

  //dropdown box
  $("#dp2").change(function () {
    $.getJSON("/_dp", getDictForPython("country")).success(function (result) {
      updateDropdowns(result), applyColorDropdowns(result);
    });
  });
  //end dp

  //reset button
  $("#reset_btn").click(function () {
    $.getJSON("/_dp", getDictForPython("reset")).success(function (result) {
      updateDropdowns(result), applyColorDropdowns(result), updateTXT(result);
    });
  });
  //end

  //print button
  $("#print_btn").on("click", function () {
    $.getJSON("/_dp", getDictForPython("print")).success(function (result) {
      updateTXT(result);
    });
  });
  //end
});

function getDictForPython(dpName) {
  return {
    call: dpName,
    member: $("#dp0").val(),
    language: $("#dp1").val(),
    country: $("#dp2").val(),
  };
}

function updateTXT(result) {
  $("#print_members").text(result.printFilter["member"]),
    $("#print_languages").text(result.printFilter["language"]),
    $("#print_countries").text(result.printFilter["country"]);
}

function updateDropdowns(result) {
  $("#dp0").html(result.dpData["member"]),
    $("#dp1").html(result.dpData["language"]),
    $("#dp2").html(result.dpData["country"]);
}

const filteredMany = "IndianRed";
const filteredOne = "grey";
const filter = "#DAF7A6";
const noFilter = "white";

function applyBackgroundColor(elementID, colorConst) {
  $(elementID).css({ "background-color": colorConst });
}

function applyColorByState(state, elementID, allConstant) {
  if (state == 1) {
    if ($(elementID).val() == allConstant) {
      applyBackgroundColor(elementID, filteredMany);
    } else {
      applyBackgroundColor(elementID, filteredOne);
    }
  } else if (state == -1) {
    applyBackgroundColor(elementID, filter);
  } else {
    applyBackgroundColor(elementID, noFilter);
  }
}

function applyColorDropdowns(result) {
  applyColorByState(result.state["member"], "#dp0", result.allConst),
    applyColorByState(result.state["language"], "#dp1", result.allConst),
    applyColorByState(result.state["country"], "#dp2", result.allConst);
}
