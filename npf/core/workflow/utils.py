def is_customer(user, memo=None):
    if memo:
        if memo.current_participant and user == memo.current_participant.user:
            return False
    return True


def get_task_performer(task_template, process_instance):
    users = task_template.user_group.user_set.all()
    if task_template.automatic_assignment and users:
        return users.order_by('?').first()
    return process_instance.assignment_responsible
