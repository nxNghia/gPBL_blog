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


$(".unlikee").click(function(){
    var csrf_token = "{{ csrf_token() }}";
    url = $(this).attr("path")
    var className = ".countLike-" + $(this).attr("action") 
    id = $(this).attr("action")

    $.ajaxSetup({
        headers: {
            "X-CSRF-TOKEN": csrf_token,
        },
    });
    $.ajax({
        url: url,
        type: "POST",
        data: {
        },
        success: function (data) {
            $(className).text(parseInt($(className).text()) + 1)
            $(".icon-like-"+ id).show()
            $(".unlike-" + id).hide()
        },
        error: function () {
            alert("Something wrong please try again!");
        },
    });
});


$(".detail-follow").click(function(){
    var csrf_token = "{{ csrf_token() }}";
    url = $(this).attr("path")

    $.ajaxSetup({
        headers: {
            "X-CSRF-TOKEN": csrf_token,
        },
    });
    $.ajax({
        url: url,
        type: "POST",
        data: {},
        success: function (data) {
            
            $(".detail-follow" ).hide();
            $(".detail-unfollow" ).show();
        },
        error: function () {
            alert("Something wrong please try again!");
        },
    });
});

$(".detail-unfollow").click(function(){
    var csrf_token = "{{ csrf_token() }}";
    url = $(this).attr("path")

    $.ajaxSetup({
        headers: {
            "X-CSRF-TOKEN": csrf_token,
        },
    });
    $.ajax({
        url: url,
        type: "DELETE",
        data: {},
        success: function (data) {
            
            $(".detail-follow" ).show();
            $(".detail-unfollow" ).hide();
        },
        error: function () {
            alert("Something wrong please try again!");
        },
    });
});

// signup
$(".tag-1").on("change", function(){
    var csrf_token = "{{ csrf_token() }}";
    url = $(this).attr("path")
    url = url + "?tag_id=" + $(this).val()
    if ($(".option-tag-1").attr("name") != "")
        name1 = $(".option-tag-1").attr("name")
    else  name1 = $(".tag-1").attr("name")
    $(".option-tag-1").children(".optiontag-1").remove()

    $.ajaxSetup({
        headers: {
            "X-CSRF-TOKEN": csrf_token,
        },
    });
    $.ajax({
        url: url,
        type: "GET",
        data: {},
        success: function (data) {
            html = ""
            if (data.length == 0) { 
                $(".tag-1").attr("name", name1) 
                $(".option-tag-1").attr("name", "") 
            } else {
                for (let i = 0 ; i< data.length ; i++) {
                    html = html + `
                    <option class="optiontag-1" value="` + data[i]["id"]+`">`+ data[i]['name']+`</option>`
                }
                $(".tag-1").attr("name", "") 
                $(".option-tag-1").attr("name", name1) 
                $(".option-tag-1").append(html)
            } 
        },
        error: function () {
            alert("Something wrong please try again!");
        },
    });
});

$(".tag-2").on("change", function(){
    var csrf_token = "{{ csrf_token() }}";
    url = $(this).attr("path")
    url = url + "?tag_id=" + $(this).val()
    if ($(".option-tag-2").attr("name") != "")
        name1 = $(".option-tag-2").attr("name")
    else  name1 = $(".tag-2").attr("name")
    $(".option-tag-2").children(".optiontag-2").remove()

    $.ajaxSetup({
        headers: {
            "X-CSRF-TOKEN": csrf_token,
        },
    });
    $.ajax({
        url: url,
        type: "GET",
        data: {},
        success: function (data) {
            html = ""
            if (data.length == 0) { 
                $(".tag-2").attr("name", name1) 
                $(".option-tag-2").attr("name", "") 
            } else {
                for (let i = 0 ; i< data.length ; i++) {
                    html = html + `
                    <option class="optiontag-2" value="` + data[i]["id"]+`">`+ data[i]['name']+`</option>`
                }
                $(".tag-2").attr("name", "") 
                $(".option-tag-2").attr("name", name1) 
                $(".option-tag-2").append(html)
            } 
        },
        error: function () {
            alert("Something wrong please try again!");
        },
    });
});

$(".tag-3").on("change", function(){
    var csrf_token = "{{ csrf_token() }}";
    url = $(this).attr("path")
    url = url + "?tag_id=" + $(this).val()
    if ($(".option-tag-3").attr("name") != "")
        name1 = $(".option-tag-3").attr("name")
    else  name1 = $(".tag-3").attr("name")
    $(".option-tag-3").children(".optiontag-3").remove()

    $.ajaxSetup({
        headers: {
            "X-CSRF-TOKEN": csrf_token,
        },
    });
    $.ajax({
        url: url,
        type: "GET",
        data: {},
        success: function (data) {
            html = ""
            if (data.length == 0) { 
                $(".tag-3").attr("name", name1) 
                $(".option-tag-3").attr("name", "") 
            } else {
                for (let i = 0 ; i< data.length ; i++) {
                    html = html + `
                    <option class="optiontag-3" value="` + data[i]["id"]+`">`+ data[i]['name']+`</option>`
                }
                $(".tag-3").attr("name", "") 
                $(".option-tag-3").attr("name", name1) 
                $(".option-tag-3").append(html)
            } 
        },
        error: function () {
            alert("Something wrong please try again!");
        },
    });
});

//edit-comment
$(".edit-comment").on("click", function(){
    id = $(this).attr("id")
    $(this).hide()
    $(".delete-comment-" + id).hide()
    $(".save-comment-" + id).show()
    $(".input-comment-" +id).val($(".content-" + id).text())
    $(".content-" + id).hide()
    $(".input-comment-" +id).show()
});

$(".save-comment ").on("click", function(){
    var csrf_token = "{{ csrf_token() }}";
    url = $(this).attr("path")
    id =  $(this).attr("id")
    content = $(".input-comment-" +id).val()

    $.ajaxSetup({
        headers: {
            "X-CSRF-TOKEN": csrf_token,
        },
    });
    $.ajax({
        url: url,
        type: "POST",
        data: {
            'content' : content
        },
        success: function (data) {
            $(".delete-comment-" + id).show()
            $(".edit-comment-" + id).show()
            $(".save-comment-" + id).hide()
            $(".content-" +id).text(content)
            $(".input-comment-" +id).hide()
            $(".content-" + id).show()
        },
        error: function () {
            alert("Something wrong please try again!");
        },
    });
});


$(".delete-comment ").on("click", function(){
    var csrf_token = "{{ csrf_token() }}";
    url = $(this).attr("path")
    id =  $(this).attr("id")

    $.ajaxSetup({
        headers: {
            "X-CSRF-TOKEN": csrf_token,
        },
    });
    if (confirm('Are you sure you want to delete this?')) {
        $.ajax({
            url: url,
            type: "DELETE",
            data: {
            },
            success: function (data) {
            $(".block-comment-" +id).remove()
            },
            error: function () {
                alert("Something wrong please try again!");
            },
        });
    }
});

