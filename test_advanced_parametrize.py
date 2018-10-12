import pytest


@pytest.fixture
def xy():
    return "xy"


#@pytest.mark.usefixtures("extra_context")
@pytest.mark.parametrize("expected", [
    pytest.param(2, marks=pytest.mark.parametrize("a,b", [(1, 1), (0, 2)])),
    pytest.param(3, marks=[
        pytest.mark.parametrize("a,b", [
            (1, 2),
            pytest.param(2, 1, marks=pytest.mark.skip),
        ]),
        pytest.mark.usefixtures("xy"),
    ]),
])
def test_advanced_parametrize(request, a, b, expected):
    """Call the cookiecutter API to generate a new project from a
    template.
    """
    assert a + b == expected
    print(request.fixturenames)
    print(a)
    print(b)
    print(expected)
    #result = cookies.bake(extra_context=context)

    #assert result.exit_code == 0
    #assert result.exception is None
    #assert result.project.isdir()


@pytest.fixture(params=["z1", "z2"])
def zz(request):
    return request.param


@pytest.fixture(params=["xx", "yz", pytest.param("zz", marks=pytest.mark.usefixtures("zz"))])
def x(request):
    return request.param


@pytest.fixture(params=["y1", "y2"], scope="module")
def y(request):
    return request.param


@pytest.fixture
def z():
    return "z"


@pytest.fixture
def ccc():
    return "ccc"


def pytest_generate_tests(metafunc):
    print("pytest_generate_tests")
    print(metafunc._calls)
    print(metafunc.definition.name)
    print(metafunc.definition.own_markers)
    print(metafunc.definition.fixturenames)
    print(metafunc.function)


@pytest.fixture(params=["xyz1", "xyz2"])
def xyz(request):
    return request.param


#@pytest.mark.skip("xyz")
@pytest.mark.parametrize(("expected_fixturenames",), [
    pytest.param(["ccc", "request", "xyz", "expected_fixturenames"]),
    pytest.param(["ccc", "request", "xyz", "expected_fixturenames", "x", "y"], marks=pytest.mark.usefixtures("x", "y")),
    pytest.param(["ccc", "request", "xyz", "expected_fixturenames", "z", "y"], marks=[pytest.mark.usefixtures("z", "y"), pytest.mark.skip("bbb")]),
    pytest.param(["ccc", "request", "xyz", "expected_fixturenames"], marks=pytest.mark.skip("xyz")),
])
@pytest.mark.usefixtures("ccc")
def test_advanced_usefixtures(request, xyz, expected_fixturenames):
    """Call the cookiecutter API to generate a new project from a
    template.
    """
    print(request.fixturenames)
    assert not set(expected_fixturenames).difference(set(request.fixturenames))
