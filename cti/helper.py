from .models import History


def compare_two_faults(request, previous_version, actual_version):
    if previous_version.handler != actual_version.handler:
        history = History(fault_id=actual_version.id,
                          changer_id=request.user.id,
                          changed_at=actual_version.updated_at,
                          changed_field='handler',
                          previous_version=str(previous_version.handler),
                          actual_version=str(actual_version.handler))
        history.save()
    if previous_version.object_number != actual_version.object_number:
        history = History(fault_id=actual_version.id,
                          changer_id=request.user.id,
                          changed_at=actual_version.updated_at,
                          changed_field='object_number',
                          previous_version=str(previous_version.object_number),
                          actual_version=str(actual_version.object_number))
        history.save()
    if previous_version.topic != actual_version.topic:
        history = History(fault_id=actual_version.id,
                          changer_id=request.user.id,
                          changed_at=actual_version.updated_at,
                          changed_field='topic',
                          previous_version=str(previous_version.topic),
                          actual_version=str(actual_version.topic))
        history.save()
    if previous_version.description != actual_version.description:
        history = History(fault_id=actual_version.id,
                          changer_id=request.user.id,
                          changed_at=actual_version.updated_at,
                          changed_field='description',
                          previous_version=str(previous_version.description),
                          actual_version=str(actual_version.description))
        history.save()
    if previous_version.phone_number != actual_version.phone_number:
        history = History(fault_id=actual_version.id,
                          changer_id=request.user.id,
                          changed_at=actual_version.updated_at,
                          changed_field='phone_number',
                          previous_version=str(previous_version.phone_number),
                          actual_version=str(actual_version.phone_number))
        history.save()
    if previous_version.status != actual_version.status:
        history = History(fault_id=actual_version.id,
                          changer_id=request.user.id,
                          changed_at=actual_version.updated_at,
                          changed_field='status',
                          previous_version=str(previous_version.status),
                          actual_version=str(actual_version.status))
        history.save()
    if previous_version.priority != actual_version.priority:
        history = History(fault_id=actual_version.id,
                          changer_id=request.user.id,
                          changed_at=actual_version.updated_at,
                          changed_field='priority',
                          previous_version=str(previous_version.priority),
                          actual_version=str(actual_version.priority))
        history.save()
    if previous_version.is_visible != actual_version.is_visible:
        history = History(fault_id=actual_version.id,
                          changer_id=request.user.id,
                          changed_at=actual_version.updated_at,
                          changed_field='is_visible',
                          previous_version=str(previous_version.is_visible),
                          actual_version=str(actual_version.is_visible))
        history.save()
    if previous_version.watchers != actual_version.watchers:
        history = History(fault_id=actual_version.id,
                          changer_id=request.user.id,
                          changed_at=actual_version.updated_at,
                          changed_field='watchers',
                          previous_version=str(previous_version.watchers),
                          actual_version=str(actual_version.watchers))
        history.save()
