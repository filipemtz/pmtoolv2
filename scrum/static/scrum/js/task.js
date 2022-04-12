
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

function update_task_priorities(items) {
    $.ajax({
        method: "POST",
        url: "update_priorities",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            'sorted_tasks': items,
        }
    }).fail(function (data) {
        $("#error").html(data);
        $("#error").show();
    });

}

function task_handleDragStart(e) {
    this.style.opacity = '0.4';
}

function task_handleDragEnd(e) {
    this.style.opacity = '1';

    let items = document.querySelectorAll('.task-view');
    items.forEach(function (item) {
        item.classList.remove('over');
    });
}


function task_handleDragOver(e) {
    if (e.preventDefault) {
        e.preventDefault();
    }

    return false;
}

function task_handleDragEnter(e) {
    this.classList.add('over');
}

function task_handleDragLeave(e) {
    this.classList.remove('over');
}

function task_handleDrop(e) {
    e.stopPropagation(); // stops the browser from redirecting.
    return false;
}

function make_all_tasks_dragable() {
    let items = document.querySelectorAll('.task-view');
    items.forEach(function (item) {
        make_task_dragable(item);
    });
}

function make_task_dragable(item) {
    item.addEventListener('dragstart', task_handleDragStart);
    item.addEventListener('dragover', task_handleDragOver);
    item.addEventListener('dragenter', task_handleDragEnter);
    item.addEventListener('dragleave', task_handleDragLeave);
    item.addEventListener('dragend', task_handleDragEnd);
    item.addEventListener('drop', task_handleDrop);
}
