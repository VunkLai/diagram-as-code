from diagrams import cloud_architecture as diagram


def teardown_function():
    diagram.CloudArchitecture.reset()


class Captcha(list):

    def __call__(self, output: str):
        """Capture output"""
        self.append(output)

    @property
    def length(self):
        return len(self)


def test_node_nad_group():
    node = diagram.Node("node")
    assert isinstance(node, diagram.Graph)
    assert hasattr(node, "render")
    assert hasattr(node, "parent")

    group = diagram.Group("group")
    assert isinstance(group, diagram.Graph)
    assert hasattr(node, "render")
    assert hasattr(node, "parent")


def test_edge():
    node = diagram.Node("node")
    assert isinstance(node.edges, diagram.Edge)
    assert node.edges.render() == ""

    node.edges.connect(diagram.Node("foo"), diagram.Node("bar"))
    assert node.edges.render() == "node > foo, bar"

    captcha = Captcha()
    diagram.CloudArchitecture.draw(captcha)
    assert node.edges.render() in captcha


def test_properties():
    node = diagram.Node("node")
    assert isinstance(node.properties, diagram.Properties)
    assert node.properties.render() == ""

    instance = diagram.Node("instance", icon="aws-instance")
    assert instance.properties.render() == "[icon: aws-instance]"

    vpc = diagram.Group("vpc", color="green")
    assert vpc.properties.render() == "[color: green]"

    subnet = diagram.Group("subnet", color="blue", icon="aws-public-subnet")
    assert subnet.properties.render() == "[icon: aws-public-subnet, color: blue]"

    captcha = Captcha()
    diagram.CloudArchitecture.draw(captcha)
    assert node.render() in captcha
    assert instance.render() in captcha
    assert vpc.render() in captcha
    assert subnet.render() in captcha


def test_draw_nodes():
    proxy = diagram.Node("proxy")
    service = diagram.Node("service")

    captcha = Captcha()
    diagram.CloudArchitecture.draw(captcha)

    assert captcha.length == 2
    assert proxy.render() in captcha
    assert service.render() in captcha


def test_draw_groups():
    vpc = diagram.Group("vpc")
    subnet = diagram.Group("subnet")
    vpc.append(subnet)

    captcha = Captcha()
    diagram.CloudArchitecture.draw(captcha)

    assert captcha.length == 1
    assert vpc.render() in captcha
    assert subnet.render() not in captcha, "sub-group should be rendered by parent"
