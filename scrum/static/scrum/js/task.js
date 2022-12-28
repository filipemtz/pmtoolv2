
function save_task_from_row(task_id) {
    form_name = "#task_" + task_id;

    $('#spinner-modal').modal('show');
    $.ajax({
        method: "POST",
        url: "/scrum/update_task",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            'task_id': task_id,
            'name': $(form_name).find('#name').val(),
            'workload': $(form_name).find('#workload').val(),
            'status': $(form_name).find('#status').val(),
            'responsible': $(form_name).find('#responsible').val(),
        }
    }).done(function (data) {
        $(form_name).replaceWith(data);
        page_alert('saved', SUCCESS_CLASS, fadeOutTime = 0.5);
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    }).always(function (data) {
        $('#spinner-modal').modal('hide');
    });
}


function save_task_from_modal(modal_name, task_id) {
    form_name = "#task_" + task_id;

    $('#spinner-modal').modal('show');
    $.ajax({
        method: "POST",
        url: "/scrum/update_task",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            'task_id': task_id,
            'name': $(modal_name).find('#name').val(),
            'workload': $(modal_name).find('#workload').val(),
            'status': $(modal_name).find('#status').val(),
            'observation': $(modal_name).find("#observation").val(),
            'responsible': $(modal_name).find("#responsible").val(),
        }
    }).done(function (data) {
        $(form_name).replaceWith(data);
        page_alert('saved', SUCCESS_CLASS, fadeOutTime = 0.5);
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    }).always(function (data) {
        $('#spinner-modal').modal('hide');
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

    $('#spinner-modal').modal('show');
    $.ajax({
        method: "POST",
        url: "/scrum/delete_task",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            'task_id': task_id,
        }
    }).done(function (data) {
        $(form_name).remove();
        page_alert('deleted', SUCCESS_CLASS, fadeOutTime = 0.5);
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    }).always(function (data) {
        $('#spinner-modal').modal('hide');
    });
}

function show_details_form(task_id) {
    $.ajax({
        method: "POST",
        url: "/scrum/task_details_form",
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

function toogleTaskStatusButton(task_id) {
    $("#status_task_" + task_id + " #current").toggle();
    $("#status_task_" + task_id + " #alternate").toggle();
}

function toogleTaskStatus(task_id) {
    //$('#spinner-modal').modal('show');
    $.ajax({
        method: "POST",
        url: "/scrum/task/" + task_id + "/toggle_status",
        mode: 'same-origin', // Do not send CSRF token to another domain.
    }).done(function (data) {
        $("#status_task_" + task_id + " #current").html(data);
        page_alert('success', SUCCESS_CLASS, fadeOutTime = 0.5);
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    }).always(function (data) {
        //$('#spinner-modal').modal('hide');
    });
}

function remove_task_tag(task_id, tag_id) {
    $.ajax({
        method: "POST",
        url: "/scrum/task/" + task_id + "/tag/" + tag_id + "/remove",
        mode: 'same-origin', // Do not send CSRF token to another domain.
    }).done(function (data) {
        page_alert('success', SUCCESS_CLASS, fadeOutTime = 0.5);
        $("#tag_" + task_id + "_" + tag_id).remove();
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    });
}