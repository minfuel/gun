import pytest
from gundb.backends.resolvers import *


@pytest.fixture
def resolved_graph():
    return {
            'author://1': {
                '_': {
                    '#': 'author://1'
                    },
                'book': "SICP",
                'food': {
                    '_': {
                        '#': 'pasta'
                    },
                    'sauce': 'white',
                    'size': 'medium'
                    },
                'location': {
                    '_': {
                        '#': 'cairo'
                    },
                    'population': '3000',
                    'description': 'extra noisy',
                    'temprature': {
                        '_': {
                            '#': 'temp'
                            },
                        'kelvin': "400",
                        'celsius': "55"
                        },
                    'list_neighbors': {
                        '_': {
                            '#': 'neighbors'
                        },
                        'random_key1': 'Mansoura',
                        'random_key2': 'Giza',
                        'random_key3': 'Helwan'
                        },
                    'list_landmarks': {
                        '_': {
                            '#': 'landmarks'
                        },
                        'random_key1': {
                            '_': {
                                '#': 'AlfMaskan'
                                },
                            'name': 'Alf Maskan',
                            'description': 'Where I live'
                            },
                        'random_key2': {
                            '_': {
                                '#': 'Ahram'
                                },
                            'name': 'Ahram',
                            'description': 'The great pyramids of giza'
                            }
                        }
                    }
                },
            'pasta': {
                '_': {
                    '#': 'pasta'
                },
                'sauce': 'white',
                'size':  'medium'
                },
            'cairo': {
                '_': {
                    '#': 'cairo'
                    },
                'population': '3000',
                'description': 'extra noisy',
                'temprature': {
                    '_': {
                        '#': 'temp'
                        },
                    'kelvin': "400",
                    'celsius': "55"
                    },
                'list_neighbors': {
                    '_': {
                        '#': 'neighbors'
                        },
                    'random_key1': 'Mansoura',
                    'random_key2': 'Giza',
                    'random_key3': 'Helwan'
                    },
                'list_landmarks': {
                    '_': {
                        '#': 'landmarks'
                    },
                    'random_key1': {
                        '_': {
                            '#': 'AlfMaskan'
                            },
                        'name': 'Alf Maskan',
                        'description': 'Where I live'
                        },
                    'random_key2': {
                        '_': {
                            '#': 'Ahram'
                            },
                        'name': 'Ahram',
                        'description': 'The great pyramids of giza'
                        }
                    }
                },
            'temp': {
                '_': {
                    '#': 'temp'
                    },
                'kelvin': "400",
                'celsius': "55"
                },
            'neighbors': {
                '_': {
                    '#': 'neighbors'
                    },
                'random_key1': 'Mansoura',
                'random_key2': 'Giza',
                'random_key3': 'Helwan'
                },
            'landmarks': {
                '_': {
                    '#': 'landmarks'
                    },
                'random_key1': {
                    '_': {
                        '#': 'AlfMaskan'
                    },
                    'name': 'Alf Maskan',
                    'description': 'Where I live'
                    },
                'random_key2': {
                    '_': {
                        '#': 'Ahram'
                        },
                    'name': 'Ahram',
                    'description': 'The great pyramids of giza'
                    }
                },
            'AlfMaskan': {
                '_': {
                    '#': 'AlfMaskan'
                    },
                'name': 'Alf Maskan',
                'description': 'Where I live'
                },
            'Ahram': {
                '_': {
                    '#': 'Ahram'
                    },
                'name': 'Ahram',
                'description': 'The great pyramids of giza'
                }
        }

@pytest.fixture
def graph():
    return {
            'author://1': {
                '_': {
                    '#': 'author://1'
                    },
                'book': "SICP",
                'food': {'#': 'pasta'},
                'location': {'#': 'cairo'}
                },
            'pasta': {
                '_': {
                    '#': 'pasta'
                    },
                'sauce': 'white',
                'size':  'medium'
                },
            'cairo': {
                '_': {
                    '#': 'cairo'
                    },
                'population': '3000',
                'description': 'extra noisy',
                'temprature': {'#': 'temp'},
                'list_neighbors': {'#': 'neighbors'},
                'list_landmarks': {'#': 'landmarks'}
                },
            'temp': {
                '_': {
                    '#': 'temp'
                    },
                'kelvin': "400",
                'celsius': "55"
                },
            'neighbors': {
                '_': {
                    '#': 'neighbors'
                    },
                'random_key1': 'Mansoura',
                'random_key2': 'Giza',
                'random_key3': 'Helwan'
                },
            'landmarks': {
                '_': {
                    '#': 'landmarks'
                    },
                'random_key1': {'#': 'AlfMaskan'},
                'random_key2': {'#': 'Ahram'},
                },
            'AlfMaskan': {
                '_': {
                    '#': 'AlfMaskan'
                    },
                'name': 'Alf Maskan',
                'description': 'Where I live'
                },
            'Ahram': {
                '_': {
                    '#': 'Ahram'
                    },
                'name': 'Ahram',
                'description': 'The great pyramids of giza'
                }
        }


def test_resolve_v_primitive(graph):
    assert resolve_v('hello', graph) == 'hello'


def test_resolve_v_direct_reference(graph, resolved_graph):
    assert resolve_v({'#': 'pasta'}, graph) == resolved_graph['pasta']


def test_resolve_v_deep_reference(graph, resolved_graph):
    assert(resolve_v({'#': 'cairo'}, graph) == resolved_graph['cairo'])


def test_desolve(graph, resolved_graph):
    import json
    print(json.dumps(desolve(resolved_graph), indent=4))
    print(json.dumps(defaultify(graph), indent=4))
    assert(desolve(resolved_graph)) ==  defaultify(graph)


def test_resolve_v_copy_not_ref(graph, resolved_graph):
    result = resolve_v({'#': 'cairo'}, graph)
    result['poupulation'] = "1"
    result['temprature']['kelvin'] = "-1"
    result['list_landmarks']['random_key1']['name'] = "Giza"
    assert resolve_v({'#': 'cairo'}, graph) == resolved_graph['cairo']

    result['temprature'] = "1"
    result['list_landmarks']['random_key1'] = "Modification"
    assert resolve_v({'#': 'cairo'}, graph) == resolved_graph['cairo']


def test_search(graph):
    assert search('temp', graph) == 'author://1'
    assert search('AlfMaskan', graph) == 'author://1'
    assert search('pasta', graph) == 'author://1'
