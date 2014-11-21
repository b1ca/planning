# coding=utf-8
from __future__ import unicode_literals


def get_extjs_element(self, tag, extjs_locator):
    driver = self.driver
    """@type: WebDriver"""
    js_code_get_id = """
        var caption = '%s';
        var classElem = Ext.get(Ext.dom.Query.select('.'+caption)[0]);
        var idElem = (Ext.ComponentQuery.query('#'+caption)[0]);
        if( idElem && idElem.getId() ){
        var id = idElem.getId();
        } else if (classElem && classElem.id){
        var id = classElem.id;
        }
        return id
    """ % extjs_locator

    extjs_element_id = driver.execute_script(js_code_get_id)
    extjs_element_css = '%s[id*=%s]' % (tag, extjs_element_id)
    return driver.find_element_by_css_selector(extjs_element_css)