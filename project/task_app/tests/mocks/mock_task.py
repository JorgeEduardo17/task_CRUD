from task_app.models import TaskUser


def mock_task(
        name='task_test',
        user=None,
        description='Test make test',
        reason='reason of accept',
):
    task = TaskUser.objects.create(
        user=user,
        name=name,
        description=description,
        reason=reason,
    )

    return task
