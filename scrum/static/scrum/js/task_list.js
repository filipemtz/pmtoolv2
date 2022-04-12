
function append_new_empty_task_list(project_id) {
    $.ajax({
        method: "POST",
        url: "empty_task_list",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            'project_id': project_id,
        }
    }).done(function (data) {
        $("#task_lists").prepend(data);
        make_task_lists_sortable();
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    });
}


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
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
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
        make_task_lists_sortable();
        page_alert('saved', SUCCESS_CLASS, fadeOutTime = 0.5);
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    });
}

function delete_task_list(task_list_id) {
    if (confirm("Tem certeza que deseja remover a lista de tarefas e todas as suas subtarefas?")) {
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
            page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
        });
    }
}


function update_task_priorities(items) {
    task_list = $("#" + items[0]).parent().parent().attr("id");

    $.ajax({
        method: "POST",
        url: "update_priorities",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            'task_list_id': task_list,
            'sorted_tasks': items,
        }
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    });
}


function make_task_lists_sortable() {
    $(".tasks").each(function (index) {
        $(this).sortable({
            connectWith: ".tasks",
            update: function (event, ui) {
                update_task_priorities($(this).sortable("toArray"));
            }
        })
        $(this).disableSelection();
    });
}
