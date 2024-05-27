from utca.implementation.schemas import RequestsHTML

def test_requests_html():
    p = RequestsHTML(
        js_rendering=True
    )

    o = p.run({"url": "https://knowledgator.com"})
    assert o["text"]
    assert o["links"]
