
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
        page_alert('saved', SUCCESS_CLASS, fadeOutTime = 0.5);
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
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
        page_alert('deleted', SUCCESS_CLASS, fadeOutTime = 0.5);
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    });
}
