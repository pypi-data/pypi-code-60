# -*- coding: utf-8 -*-
import pytest
from bs4 import BeautifulSoup
from zwutils import htmlutils

def test_find_soup_parent():
    htmlstr = '''
    <table class="myclass otherclass">
    <thead></thead>
    <tbody>
        <tr><td id="a"></td></tr>
        <tr></tr>
    </tbody>
    </table>
    '''
    el = BeautifulSoup(htmlstr, features='lxml')
    el = el.find(id='a')
    r = htmlutils.find_soup_parent(el, tagnm='table')
    assert r and r.name == 'table'

    r = htmlutils.find_soup_parent(el, attrs={'class': 'myclass'})
    assert r and r.name == 'table'

    r = htmlutils.find_soup_parent(el, tagnm='table', attrs={'class': 'myclass'})
    assert r and r.name == 'table'

def test_find_soup_next_sibling():
    htmlstr = '''
    <table>
    <thead></thead>
    <tbody>
        <tr><td id="a">label</td><td>text1</td><td class="myclass otherclass">text2</td></tr>
        <tr></tr>
    </tbody>
    </table>
    '''
    el = BeautifulSoup(htmlstr, features='lxml')
    el = el.find(id='a')
    r = htmlutils.find_soup_next_sibling(el, tagnm='td')
    assert r and r.text == 'text1'

    r = htmlutils.find_soup_next_sibling(el, attrs={'class': 'myclass'})
    assert r and r.text == 'text2'

    r = htmlutils.find_soup_next_sibling(el, tagnm='td', attrs={'class': 'myclass'})
    assert r and r.text == 'text2'
