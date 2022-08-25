from datasette import hookimpl


@hookimpl
def extra_body_script():
    return {
        "script": '</script><script async defer data-website-id="8fe29870-5d8b-40e8-b8cc-1421b994b077" src="https://analytics.berkeley.place/civic.js"></script>'
    }
