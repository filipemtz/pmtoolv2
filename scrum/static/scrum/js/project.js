
function add_team_member(project_id) {
    $('#spinner-modal').modal('show');

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
    }).always(function (data) {
        $('#spinner-modal').modal('hide');
    });
}


function remove_user_from_team(project_id, user_id) {
    $('#spinner-modal').modal('show');
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
    }).always(function (data) {
        $('#spinner-modal').modal('hide');
    });
}


function add_new_empty_project() {
    $('#spinner-modal').modal('show');
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
    }).always(function (data) {
        $('#spinner-modal').modal('hide');
    });
}


function save_project(project_id) {
    $('#spinner-modal').modal('show');
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
    }).always(function (data) {
        $('#spinner-modal').modal('hide');
    });
}


function remove_project(project_id) {
    if (confirm("Are you sure that you want to remove the project and all of its data? This action can't be undone!!")) {
        $('#spinner-modal').modal('show');
        $.ajax({
            method: "POST",
            url: "/scrum/project/remove",
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
        }).always(function (data) {
            $('#spinner-modal').modal('hide');
        });
    }
}

function show_project_editor_form(project_id) {
    $('#spinner-modal').modal('show');
    $.ajax({
        method: "POST",
        url: "/scrum/project_details_form",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            'project_id': project_id,
        }
    }).done(function (data) {
        $("#details-form-placeholder").html(data);
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    }).always(function (data) {
        $('#spinner-modal').modal('hide');
    });
}

function show_team_speed_chart(project_id) {
    $("#burndown-chart-modal-image").html("");
    $('#spinner-modal').modal('show');
    $.ajax({
        method: "POST",
        url: "/scrum/speed_chart",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            'project_id': project_id,
        }
    }).done(function (data) {
        $("#burndown-chart-modal-image").html(data);
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    }).always(function (data) {
        $('#spinner-modal').modal('hide');
    });
}

function show_project_notes_editor(project_id) {
    $.ajax({
        method: "GET",
        url: "/scrum/project/" + project_id + "/notes",
        mode: 'same-origin', // Do not send CSRF token to another domain.
    }).done(function (data) {
        // refactor the modal name
        $("#details-form-placeholder").html(data);
        $("#project_notes_textarea").focus();
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    }).always(function (data) {
    });
}


function save_project_notes(project_id) {
    notes = $("#project_notes_textarea").val();
    $.ajax({
        method: "POST",
        url: "/scrum/project/" + project_id + "/notes",
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            'notes': notes,
        }
    }).done(function (data) {
        page_alert('saved', SUCCESS_CLASS, fadeOutTime = 0.5);
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    }).always(function (data) {
    });
}
