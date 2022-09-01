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
            edit_url = "?comment_id=" + data['id']
            var html = `
            <div class="block-comment-`+ data['id'] +`">
            <div class="d-flex">
                <div class="avatar col-3 d-flex flex-column text-center align-items-center">
                    <img class="avatar-comment" src="`+ $('.avatar-comment').attr("src") +`" alt="avatar" />
                    <span class="mt-3 px-5 py-1">`+ data['username'] +`</span>
                </div>
                <div class="content p-2 col-9">
                    <p class="content-`+ data['id'] +`">`+ data['content'] +`</p>
                    <textarea class="input-comment-`+ data['id'] +`" rows="4" style="display: none;" cols="80"></textarea>
                </div>                       
            </div>
                <div class="d-flex justify-content-end mb-3">
                    <a href="javascript:void()" path="`+ $('.btn-edit-comment').attr("path")+ edit_url +`" style="display: none;" id="`+ data['id'] +`" class="save-comment save-comment-`+ data['id'] +`" >保存</a>
                    <a href="javascript:void()"  style="margin-right: 20px;" id="`+ data['id'] +`" class="edit-comment edit-comment-`+ data['id'] +`" >編集</a>
                    <a href="javascript:void()" id="`+ data['id'] +`" path="`+ $('.btn-delete-comment').attr("path")+ edit_url +`" class="delete-comment delete-comment-`+ data['id'] +`">削除</a>
                </div>
            </div>
            `;
            $(".text-comment" ).append(html);
            $(".input-comment").val("");
        },
        error: function () {
            alert("エラーが発生しました!");
        },
    });
});


$(".unlikee").click(function(){
    var csrf_token = "{{ csrf_token() }}";
    url = $(this).attr("path")
    var className = ".countLike-" + $(this).attr("action") 
    id1 =  "#countLike-" + $(this).attr("action") 
    id = $(this).attr("action")
    count = parseInt($(id1).val()) + parseInt(1)

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
            $(className).text(count)
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
            alert("エラーが発生しました!");
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
            alert("エラーが発生しました!");
        },
    });
});

// signup
$(".tag-1").on("change", function(){
    var csrf_token = "{{ csrf_token() }}";
    url = $(this).attr("path")
    url = url + "?tag_id=" + $(this).val()
    console.log(url)
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
            console.log(data)
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
            alert("エラーが発生しました!");
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
            alert("エラーが発生しました!");
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
            alert("エラーが発生しました!");
        },
    });
});

//edit-comment
$(document).on("click", ".edit-comment", function (event) {
    id = $(this).attr("id")
    $(this).hide()
    $(".delete-comment-" + id).hide()
    $(".save-comment-" + id).show()
    $(".input-comment-" +id).val($(".content-" + id).text())
    $(".content-" + id).hide()
    $(".input-comment-" +id).show()
});

$(document).on("click", ".save-comment", function (event) {
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
            alert("エラーが発生しました!");
        },
    });
});


$(document).on("click", ".delete-comment", function (event) {
    var csrf_token = "{{ csrf_token() }}";
    url = $(this).attr("path")
    id =  $(this).attr("id")

    $.ajaxSetup({
        headers: {
            "X-CSRF-TOKEN": csrf_token,
        },
    });
    if (confirm('削除しますか?')) {
        $.ajax({
            url: url,
            type: "DELETE",
            data: {
            },
            success: function (data) {
            $(".block-comment-" +id).remove()
            },
            error: function () {
                alert("エラーが発生しました!");
            },
        });
    }
});

$(".form-check input ").on("change", function(){
    if ($('input[name=radio-post]:checked').val() == 1) {
        $(".post-created-at").show()
        $(".post-point").hide()
    } else {
        $(".post-created-at").hide()
        $(".post-point").show()
    } 
});

$(".change-status-task input ").on("change", function(){
    if ($('input[name=task-status]:checked').val() == 1) {
        $(".task-notcomplete").show()
        $(".task-complete").hide()
    } else {
        $(".task-notcomplete").hide()
        $(".task-complete").show()
    } 
});


$(document).on("change", ".checkbox-task", function (event) {

    id = $(this).attr("id")
    url = $(this).attr("path")
    var csrf_token = "{{ csrf_token() }}";
    var point = $("#user-point").val()

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
            $(".task-" + id).remove()
            html = `
            <div class="row task-`+ data["id"] +`">
                <div class="task-title">
                    `+ data["title"] +`
                </div>
                <div class="deadline">
                    `+ data["deadline"] +`
                </div>
            </div>
            `
            $(".task-complete").append(html)
            var newPoint = parseInt(point) + parseInt(data.point)
            $(".user-point-info").text(newPoint)
            $("#user-point").val(newPoint)
        },
        error: function () {
            alert("エラーが発生しました!");
        },
    });
});

$(document).on("change", ".create-tag-select", function (event) {
    var csrf_token = "{{ csrf_token() }}";
    url = $(this).attr("path")
    url = url + "?tag_id=" + $(this).val()
    name2 = $(".create-tag-select").attr("name")
    if ($(".option-create").attr("name") != "")
        name2 = $(".option-create").attr("name")

    $(".option-create").children(".post-create-option").remove()

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
                $(".create-tag-select").attr("name", name2) 
                $(".option-create").attr("name", "") 
            } else {
                for (let i = 0 ; i< data.length ; i++) {
                    html = html + `
                    <option class="post-create-option" value="` + data[i]["id"]+`">`+ data[i]['name']+`</option>`
                }
                $(".create-tag-select").attr("name", "") 
                $(".option-create").attr("name", name2) 
                $(".option-create").append(html)
            } 
        },
        error: function () {
            alert("エラーが発生しました!");
        },
    });
});