# -*- coding: utf-8 -*-
{
    'name': "sales_dashboard",

    'description': """
            Detailed dashboard of sales module
                    """,

    'version': '16.0.1.0.0',
    'auto_install' : True,
    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
       'data/dashboard_menu.xml'
    ],
    'assets': {
       'web.assets_backend': [
           'sales_dashboard/static/src/xml/sale_dashboard.xml',
           'sales_dashboard/static/src/js/sales_dashboard.js',
           'https://cdn.jsdelivr.net/npm/chart.js'
       ],
    },
}

