from django.shortcuts import render_to_response


def index(request, *a, **kw):
    return render_to_response("hp_home/index.html", {})
