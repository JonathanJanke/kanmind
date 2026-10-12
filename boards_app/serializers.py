from rest_framework import serializers


class BoardSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    member_count = serializers.IntegerField()
    ticket_count = serializers.IntegerField()
    tasks_to_do_count = serializers.IntegerField()
    tasks_high_prio_count = serializers.IntegerField()
    owner_id = serializers.IntegerField()

    def get_response(self, obj):
        
        return {
            "id": obj.id,
            "title": obj.title,
            "member_count": obj.member_count,
            "ticket_count": obj.ticket_count,
            "tasks_to_do_count": obj.tasks_to_do_count,
            "tasks_high_prio_count": obj.tasks_high_prio_count,
            "owner_id": obj.owner_id
            }