
function save_task(task_id) {
    form_name = "#task_" + task_id;

    $.ajax({
        method: "POST",
        url: "update_task",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            'task_id': task_id,
            'name': $(form_name).find('#name').val(),
            'workload': $(form_name).find('#workload').val(),
            'status': $(form_name).find('#status').val(),
        }
    }).done(function (data) {
        $(form_name).replaceWith(data);
    }).fail(function (data) {
        $("#error").html(data);
        $("#error").show();
    });
}

function delete_task(task_id) {
    form_name = "#task_" + task_id;

    $.ajax({
        method: "POST",
        url: "delete_task",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            'task_id': task_id,
        }
    }).done(function (data) {
        $(form_name).remove();
    }).fail(function (data) {
        $("#error").html(data);
        $("#error").show();
    });
}
