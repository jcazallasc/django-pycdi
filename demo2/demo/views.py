from random import random

from django.http import HttpRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from pycdi import Inject, Producer
from pycdi.core import CDIContainer
from pycdi.utils import Singleton


@Singleton()
class MySingleton(object):
    pass


@Producer(float)
def produce_random():
    return random()


def without_injection(request, *args, **kwargs):
    return render(request, 'debug.html', locals())


@Inject(url=basestring, _context='data')
@Inject(singleton=MySingleton, random_number=float)
def with_injection(request, data, url, singleton, **kwargs):
    return render(request, 'debug.html', locals())


@Inject(HttpRequest, singleton=MySingleton, random_number=float)
def with_request_injection(request, singleton, random_number):
    return render(request, 'debug.html', locals())


@Inject(container=CDIContainer, number=float)
def container_inject(request, container, number):
    singleton = container.produce(MySingleton)
    return render(request, 'debug.html', locals())


@method_decorator(Inject(container=CDIContainer, number=float), name='dispatch')
class GenericView(View):
    def get(self, request, container, number):
        other_number = container.produce(float)
        singleton = container.produce(MySingleton)
        return render(request, 'debug.html', locals())
