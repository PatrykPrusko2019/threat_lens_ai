def event_to_features(event):
    return [
        len(event.event_type),      # event type length
        len(event.severity),        # severity length
        1 if event.source_ip else 0, # if is IP    
    ]