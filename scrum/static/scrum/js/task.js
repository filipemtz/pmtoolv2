
function save_task_from_row(task_id) {
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


function save_task_from_modal(moodal_name, task_id) {
    form_name = "#task_" + task_id;

    $.ajax({
        method: "POST",
        url: "update_task",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            'task_id': task_id,
            'name': $(moodal_name).find('#name').val(),
            'workload': $(moodal_name).find('#workload').val(),
            'status': $(moodal_name).find('#status').val(),
            'observation': $(moodal_name).find("#observation").val(),
        }
    }).done(function (data) {
        $(form_name).replaceWith(data);
        page_alert('saved', SUCCESS_CLASS, fadeOutTime = 0.5);
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    });
}


function save_task(task_id) {
    modal_name = "#task_details_" + task_id;

    // if the modal is visible, get the task information from it. 
    if ($(modal_name).is(":visible")) {
        save_task_from_modal(modal_name, task_id);
    }
    else {
        save_task_from_row(task_id);
    }
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

function show_details_form(task_id) {
    $.ajax({
        method: "POST",
        url: "task_details_form",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            'task_id': task_id,
        }
    }).done(function (data) {
        $("#details-form-placeholder").html(data);
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    });
}
