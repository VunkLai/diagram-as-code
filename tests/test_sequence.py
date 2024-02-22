from diagrams import sequence as diagram


def teardown_function():
    diagram.Sequence.reset()


class Captcha(list):

    def __call__(self, output: str):
        """Capture output"""
        self.append(output)

    @property
    def length(self):
        return len(self)


def test_nodes():
    proxy = diagram.Node("proxy")
    service = diagram.Node("service")
    proxy.request("GET /", service)
    service.response("200", proxy)

    captcha = Captcha()
    diagram.Sequence.draw(captcha)

    assert len(captcha) == 4
    assert proxy.render() in captcha
    assert service.render() in captcha
    assert "proxy > service : GET /" in captcha
    assert "service > proxy : 200" in captcha
