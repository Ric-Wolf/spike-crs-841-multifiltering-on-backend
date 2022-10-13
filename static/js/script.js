$(document).ready(function () {
  // dropdown box
  $("#dp0").change(function () {
    $.getJSON("/_dp", {
      call: "member",
      member: $("#dp0").val(),
      lang: $("#dp1").val(),
      country: $("#dp2").val(),
    }).success(function (data) {
      // $('#dp0').html(data.dp_data[0]),
      $("#dp1").html(data.dp_data[1]),
        $("#dp2").html(data.dp_data[2]),
        $("#dp1_lab").css("color", "red"),
        $("#dp2_lab").css("color", "red");
    });
  });
  //end dp

  //dropdown box
  $("#dp1").change(function () {
    $.getJSON("/_dp", {
      call: "language",
      member: $("#dp0").val(),
      language: $("#dp1").val(),
      country: $("#dp2").val(),
    }).success(function (data) {
      $("#dp0").html(data.dp_data[0]),
        // $('#dp1').html(data.dp_data[1]),
        $("#dp2").html(data.dp_data[2]),
        $("#dp0_lab").css("color", "red"),
        $("#dp2_lab").css("color", "red");
    });
  });
  //end dp

  //dropdown box
  $("#dp2").change(function () {
    $.getJSON("/_dp", {
      call: "country",
      member: $("#dp0").val(),
      lang: $("#dp1").val(),
      country: $("#dp2").val(),
    }).success(function (data) {
      $("#dp0").html(data.dp_data[0]),
        $("#dp1").html(data.dp_data[1]),
        //$("#dp2").html(data.dp_data[2]),
        $("#dp0_lab").css("color", "red"),
        $("#dp1_lab").css("color", "red");
    });
  });
  //end dp

  //reset button
  $("#reset_btn").click(function () {
    $.getJSON("_dp", {
      call: "reset",
    }).success(function (data) {
      $("#dp0").html(data.dp_data[0]),
        $("#dp1").html(data.dp_data[1]),
        $("#dp2").html(data.dp_data[2]),
        $("#dp0_lab").css("color", "black"),
        $("#dp1_lab").css("color", "black"),
        $("#dp2_lab").css("color", "black"),
        $("#print_txt").text(
          "Here we display some output based on the selection"
        );
    });
  });
  //end

  // implementar no colorear lo que activo un filtro

  //print button
  $("#print_btn").on("click", function () {
    $.getJSON("/_dp", { call: "print" }).success(function (result) {
      $("#print_txt").text(result.print_txt);
    });
  });
  //end
});
