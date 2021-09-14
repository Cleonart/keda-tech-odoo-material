# -*- coding: utf-8 -*-
{
    'name' : 'Material Management Module',
    'version' : '1.0',
    'summary' : 'Material Management Module',
    'sequence' : 10,
    'description' : """Material Management Module""",
    'category' : 'Productivity',
    'website' : '',
    'depends' : [],
    'data' : [
        'security/ir.model.access.csv',
        'views/server.xml',
        'views/material_new.xml',
        'views/material.xml',
        'views/supplier.xml'
    ],
    'demo' : [],
    'qweb' : [],
    'installable' : True,
    'application' : True,
    'auto_install' : False
}
