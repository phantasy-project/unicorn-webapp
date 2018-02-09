$(function() {
    // edit function
    $(".btn-edit-function").click(function() {
        var name = $(this).data('name');
        var args = $(this).data('args');
        var code = $(this).data('code');
        var url  = $(this).data('url');
        var desc = $(this).data('desc');
        $(".modal-body #name").val(name);
        $(".modal-body #args").val(args);
        $(".modal-body #code").val(code);
        $(".modal-body #url").val(url);
        $(".modal-body #description").val(desc);
    });

    // submit update function
    $(".submit-update-function").click(function() {
        var name = $(".modal-body #name").val();
        var args = $(".modal-body #args").val();
        var code = $(".modal-body #code").val();
        var desc = $(".modal-body #description").val();
        var url  = $(".modal-body #url").val();
        var data = {'name': name, 'args': args, 'description': desc,
                    'code': code};

        $.ajax({
            type: "PUT",
            url: url,
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            success: function() {
                alert("Function Updated");
                location.reload();
            },
            error: function() {
                alert("Update Failed");
            }
        });
    });
    
    // run function
    $(".btn-run-function").click(function() {
        var name   = $(this).data('name');
        var apiurl = $(this).data('apiurl');
        var json_input_args = $("#func-input-args").val();
        var data = JSON.parse(json_input_args);

        $.ajax({
            type: "GET",
            url: apiurl,
            data: data,
            contentType: "application/json; charset=utf-8",
            success: function(data) {
                $("#func-output").val(data['result']);
                location.reload();
            },
            error: function() {
                alert("Evaluation Failed!")
            }
        });
    });
});
