function w3_open() {
    document.getElementById("mySidebar").style.display = "block";
    document.getElementById("iconSidebar").style.display = "none";
}
  
function w3_close() {
    document.getElementById("mySidebar").style.display = "none";
    document.getElementById("iconSidebar").style.display = "block";
}

$( ".update-icon" ).click(function() {
    $(".user-display-info").hide()
    $(".update-info").show()
});

$( ".edit-cancel" ).click(function() {
    $(".user-display-info").show()
    $(".update-info").hide()
});

$(".create-select-type").on("change", function(){
    if ($(this).val() == 0)
        $(".create-post-date").show();
    else $(".create-post-date").hide();
});