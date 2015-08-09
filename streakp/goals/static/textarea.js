$(function(){
    $("textarea.visib").hide()
})

$(".current-notes").click(function(){
    $(".visib").toggle()
    $("textarea.visib").focus()
})

$("textarea.visib").blur(function() {
    $(".visib").toggle()
})


$(".notes").keydown(function (e) {
    if (e.keyCode == 13) {
        if (e.shiftKey) {

        }
        else {
            update_notes()
            return false
        }
    }
});

function update_notes() {
    new_value = $("textarea.visib").val()
    $.post( "update_notes/", {notes: new_value})
      .done(function(data) {
        $(".current-notes").html(data)
        $("textarea.visib").blur()
      });
}