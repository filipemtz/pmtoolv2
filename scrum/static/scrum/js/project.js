
function add_team_member(project_id) {
    $.ajax({
        method: "POST",
        url: "/scrum/project/add_team_member",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            'project_id': project_id,
            'username': $("#new_team_member").val(),
        }
    }).done(function (data) {
        $("#team").append(data);
        page_alert('saved', SUCCESS_CLASS, fadeOutTime = 0.5);
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    });
}


function remove_user_from_team(project_id, user_id) {
    $.ajax({
        method: "POST",
        url: "/scrum/project/remove_team_member",
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
    new_name = $("#project_editor_form").find("#name").val();
    $.ajax({
        method: "POST",
        url: "/scrum/project/update",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            "project_id": project_id,
            "name": new_name,
        }
    }).done(function (data) {
        $("#project").find("option:selected").text(new_name);
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
            //page_alert('removed', SUCCESS_CLASS, fadeOutTime = 0.5);
            window.location.replace("/scrum");
        }).fail(function (data) {
            page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
        });
    }
}


function show_project_editor_form(project_id) {
    $.ajax({
        method: "POST",
        url: "project_details_form",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            'project_id': project_id,
        }
    }).done(function (data) {
        $("#details-form-placeholder").html(data);
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    });
}