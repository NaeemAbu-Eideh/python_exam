def flush_session(request):
    request.session.flush()