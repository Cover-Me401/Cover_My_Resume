import pytest
# from fix import issue here
from django.test import Client
from django.template import loader
from django.test import TestCase

template = loader.get_template('base.html')
rendered_html = template.render()


def test_home_link(client):
    response = client.get('/home/')
    assert response.status_code == 200
    assert response.url == '/home/'



def test_about_link(client):
    response = client.get('/about/')
    assert response.status_code == 200
    assert response.url == '/about/'
