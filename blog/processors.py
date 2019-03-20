from preferences import preferences


def settings_processor(request):
    metatag_data = None
    if hasattr(request, 'metatag_data'):
        metatag_data = getattr(request, 'metatag_data')

    config = preferences.Config

    metatag = {}
    if metatag_data:
        whois = metatag_data.get('whois')

        title = getattr(config, '%s_title_pattern' % whois) or ''
        keywords = getattr(config, '%s_keywords_pattern' % whois) or ''
        description = getattr(config, '%s_description_pattern' % whois) or ''

        metatag['title'] = title.replace('__V__', metatag_data['title'])
        metatag['keywords'] = keywords.replace(
            '__V__',
            metatag_data['keywords']
        )
        metatag['description'] = description.replace(
            '__V__',
            metatag_data['description']
        )

    return {
        'metatag': metatag,
        'head_injection': config.head_injection or '',
        'body_injection': config.body_injection or '',
    }
