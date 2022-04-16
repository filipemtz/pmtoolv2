
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


function append_new_empty_task(task_list_id, bottom_or_top) {
    $.ajax({
        method: "POST",
        url: "new_empty_task",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            'task_list_id': task_list_id,
            'bottom_or_top': bottom_or_top,
        }
    }).done(function (data) {
        form_name = "#task_list_" + task_list_id;
        $(form_name).find("#instructions").remove();
        if (bottom_or_top == 'bottom') {
            $(form_name).find("#tasks").append(data);
        }
        else {
            $(form_name).find("#tasks").prepend(data);
        }
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    });
}


function update_task_list_from_modal(modal_name, task_list_id) {
    $.ajax({
        method: "POST",
        url: "update_task_list",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            'task_list_id': task_list_id,
            'name': $(modal_name).find('#name').val(),
            'start_date': $(modal_name).find('#date_start_' + task_list_id).val(),
            'end_date': $(modal_name).find('#date_end_' + task_list_id).val(),
            'observation': $(modal_name).find("#observation").val(),
            'toggle_archived': 'false',
        }
    }).done(function (data) {
        form_name = "#task_list_" + task_list_id;
        $(form_name).replaceWith(data);
        make_task_lists_sortable();
        make_div_dates_pickable(form_name);
        page_alert('saved', SUCCESS_CLASS, fadeOutTime = 0.5);
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    });
}


function update_task_list_from_row(task_list_id, toggle_archived) {
    form_name = "#task_list_" + task_list_id;

    $.ajax({
        method: "POST",
        url: "update_task_list",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            'task_list_id': task_list_id,
            'name': $(form_name).find('#name').val(),
            'start_date': $(form_name).find('#date_start_' + task_list_id).val(),
            'end_date': $(form_name).find('#date_end_' + task_list_id).val(),
            'toggle_archived': toggle_archived,
        }
    }).done(function (data) {
        $(form_name).replaceWith(data);
        make_task_lists_sortable();
        make_div_dates_pickable(form_name);
        page_alert('saved', SUCCESS_CLASS, fadeOutTime = 0.5);
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    });
}


function update_task_list(task_list_id, toggle_archived) {
    modal_name = "#task_list_details_" + task_list_id;

    // if the modal is visible, get the task information from it. 
    if ($(modal_name).is(":visible")) {
        update_task_list_from_modal(modal_name, task_list_id);
    }
    else {
        update_task_list_from_row(task_list_id, toggle_archived);
    }

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
    if (items.length < 1)
        return;

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


function show_burndown_graph(task_list_id) {
    $.ajax({
        method: "POST",
        url: "burndown",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            'task_list_id': task_list_id,
        }
    }).done(function (data) {
        $("#burndown-chart-modal-image").html(data);
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    });
}


function show_task_list_details_form(task_list_id) {
    $.ajax({
        method: "POST",
        url: "task_list_details_form",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            'task_list_id': task_list_id,
        }
    }).done(function (data) {
        $("#details-form-placeholder").html(data);
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
    });
}


function make_dates_pickable() {
    $(".task-list-date").each(function (index) {
        $(this).datepicker({
            dateFormat: "yy-mm-dd"
        })
    });
}


function make_div_dates_pickable(div_id) {
    $(div_id).find(".task-list-date").each(function (index) {
        $(this).datepicker({
            dateFormat: "yy-mm-dd"
        })
    });
}

