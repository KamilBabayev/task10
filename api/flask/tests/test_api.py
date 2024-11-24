import pytest
import requests

test_api_url = 'http://localhost:5000'

def test_index_page():
    res = requests.get(test_api_url)
    assert res.status_code == 200
    assert res.json()['page'] == 'index'

def test_add_new_note():
    note = {'name': 'test_note01', 'desc': 'test note01 description'}
    req = requests.post(test_api_url + '/api/v1/notes', json=note)
    assert req.status_code == 200
    assert req.json()['msg'].split()[-2:] == ['added', 'successfully']

def test_get_specific_note():
    req = requests.get(test_api_url + '/api/v1/notes')
    test_note_id = [ i for i in req.json()['Notes'] if i['name'] == 
                     'test_note01'][0]['id']
    r = requests.get(test_api_url + '/api/v1/notes' + '/' + str(test_note_id))
    assert r.json()['note']['note_name'] == 'test_note01'


def test_delete_note():
    req = requests.get(test_api_url + '/api/v1/notes')
    test_note_id = [ i for i in req.json()['Notes'] if i['name'] == 
                     'test_note01'][0]['id']
    r = requests.delete(test_api_url + '/api/v1/notes' + '/' + str(test_note_id))
    assert r.json()['msg'].split()[-2:] == ['deleted', 'successfully']
    
    
