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
    if ($(this).val() == 0) {
        $(".posting-content").hide();
        $(".create-post-date").show();
    }

    else {
        $(".create-post-date").hide();
        $(".posting-content").show()
    }
});

$(".btn-comment").click(function(){
    var csrf_token = "{{ csrf_token() }}";
    url = $(this).attr("path")
    content = $(".input-comment").val()

    $.ajaxSetup({
        headers: {
            "X-CSRF-TOKEN": csrf_token,
        },
    });
    $.ajax({
        url: url,
        type: "POST",
        data: {
            "content" : content
        },
        success: function (data) {
            var html = `
            <div class="d-flex mb-5">
                        <div class="avatar col-3 d-flex flex-column text-center align-items-center">
                            <img src="`+ $('.avatar-comment').attr("src") +`">
                            <span class="mt-3 px-5 py-1">` + data['username'] +`</span>
                        </div>
                        <div class="content p-2 col-9">
                            `+ data['content'] +`
                        </div>
                    </div>
            `;
            $(".text-comment" ).append(html);
            $(".input-comment").val("");
        },
        error: function () {
            alert("Something wrong please try again!");
        },
    });
});
