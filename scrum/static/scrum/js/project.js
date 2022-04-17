
function add_team_member(project_id) {
    $.ajax({
        method: "POST",
        url: "add_team_member",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            'project_id': project_id,
            'username': $("#new_team_member").val(),
        }
    }).done(function (data) {
        $("#team").append("<div class='team-member'>" + data + "</div>");
        page_alert('saved', SUCCESS_CLASS, fadeOutTime = 0.5);
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    });
}


function remove_user_from_team(project_id, user_id) {
    $.ajax({
        method: "POST",
        url: "remove_team_member",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            'project_id': project_id,
            'user_id': user_id,
        }
    }).done(function (data) {
        $("#user_" + user_id).remove();
        page_alert('removed', SUCCESS_CLASS, fadeOutTime = 0.5);
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    });
}


function add_new_empty_project() {
    $.ajax({
        method: "POST",
        url: "project/new",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {}
    }).done(function (data) {
        $("#project-list").append(data);
        page_alert('removed', SUCCESS_CLASS, fadeOutTime = 0.5);
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    });
}


function save_project(project_id) {
    $.ajax({
        method: "POST",
        url: "update",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            "project_id": project_id,
            "name": $("#name").val(),
        }
    }).done(function (data) {
        page_alert('saved', SUCCESS_CLASS, fadeOutTime = 0.5);
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    });
}


function remove_project(project_id) {
    if (confirm("Are you sure that you want to remove the project and all of its data? This action can't be undone!!")) {
        $.ajax({
            method: "POST",
            url: "project/remove",
            mode: 'same-origin', // Do not send CSRF token to another domain.
            data: {
                "project_id": project_id,
            }
        }).done(function (data) {
            $("#project_" + project_id).remove();
            page_alert('removed', SUCCESS_CLASS, fadeOutTime = 0.5);
        }).fail(function (data) {
            page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
        });
    }
}