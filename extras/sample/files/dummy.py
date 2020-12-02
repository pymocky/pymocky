from pymocky.models.mapping_request import MappingRequest


def run(data):
    if isinstance(data, dict):
        request = data["request"]

        if isinstance(request, MappingRequest):
            form_fields = request.form_fields
            username = form_fields["username"]
            body = '{{"message": "Hello from Python!", "username": "{0}"}}'.format(
                username
            )

            return {
                "status": 200,
                "body": body,
                "headers": {
                    "Content-Type": "application/json",
                },
            }

    return {"status": 500}
