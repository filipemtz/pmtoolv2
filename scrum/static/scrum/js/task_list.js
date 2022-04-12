
function append_new_empty_task(task_list_id) {
    $.ajax({
        method: "POST",
        url: "new_empty_task",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            'task_list_id': task_list_id,
        }
    }).done(function (data) {
        form_name = "#task_list_" + task_list_id;
        $(form_name).find("#instructions").remove();
        $(form_name).find("#tasks").append(data);
        //make_all_tasks_dragable();
    }).fail(function (data) {
        $("#error").html(data);
        $("#error").show();
        $("#error").fadeOut(start = 5);
    });
}

function update_task_list(task_list_id, toggle_archived) {
    form_name = "#task_list_" + task_list_id;

    $.ajax({
        method: "POST",
        url: "update_task_list",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            'task_list_id': task_list_id,
            'name': $(form_name).find('#name').val(),
            'toggle_archived': toggle_archived,
        }
    }).done(function (data) {
        $(form_name).replaceWith(data);
    }).fail(function (data) {
        $("#error").html(data);
        $("#error").show();
    });
}

function delete_task_list(task_list_id) {
    alert("Not implemented yet.")
    /*
    form_name = "#task_list_" + task_list_id;

    $.ajax({
        method: "POST",
        url: "delete_task_list",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            'task_list_id': task_list_id,
        }
    }).done(function (data) {
        $(form_name).remove();
    }).fail(function (data) {
        $("#error").html(data);
        $("#error").show();
    });
    */
}

function make_task_lists_sortable() {
    $("#tasks").sortable({
        update: function (event, ui) {
            update_task_priorities($(this).sortable("toArray"));
        }
    });
}