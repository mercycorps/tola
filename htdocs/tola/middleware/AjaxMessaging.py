import json

from django.contrib import messages

class AjaxMessaging(object):
    def process_response(self, request, response):
        if request.is_ajax():
            print("ajax done: %s" % response['Content-Type'])
            if response['Content-Type'] in ["application/javascript", "application/json"]:
                try:
                    content = json.loads(response.content)
                except ValueError as e:
                    print("Error has occured: %s" % e)
                    return response

                django_messages = []

                for message in messages.get_messages(request):
                    django_messages.append({
                        "level": message.level,
                        "message": message.message,
                        "extra_tags": message.tags,
                    })

                content['django_messages'] = django_messages

                response.content = json.dumps(content)
        #print("Ajax middleware returning response")
        #print(response)
        return response