# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date


class SaleOrders(models.Model):
    _inherit = 'sale.order'

    @api.model
    def get_sale_by_team(self,selection_val,is_admin,user_id):
        """Returns data to the graph of dashboard"""
        custom_filter = ""
        if selection_val == "this_year":
            custom_filter = "AND EXTRACT('YEAR' FROM so.date_order) = EXTRACT('YEAR'FROM CURRENT_DATE)"
        if selection_val == "this_month":
            custom_filter = "AND EXTRACT('MONTH' FROM so.date_order) = EXTRACT('MONTH'FROM CURRENT_DATE)"
        if selection_val == "this_week":
            custom_filter = "AND EXTRACT('WEEK' FROM so.date_order) = EXTRACT('WEEK'FROM CURRENT_DATE)"
        if selection_val == "this_day":
            custom_filter = " AND EXTRACT('DAY' FROM so.date_order) = EXTRACT('DAY'FROM CURRENT_DATE)"

        if (is_admin):
            query = f"""SELECT team.name->>'en_US' AS team_name,
                        COUNT(so.id) AS order_count
                        FROM sale_order AS so
                        INNER JOIN crm_team AS team ON team.id = so.team_id
                        WHERE 1=1 {custom_filter}
                        GROUP BY team.id, team.name->>'en_US'
                        ORDER BY COUNT(DISTINCT so.id) ASC;"""
        if (not is_admin):
            query = f"""SELECT team.name->>'en_US' AS team_name,
                        COUNT(so.id) AS order_count
                        FROM sale_order AS so
                        INNER JOIN crm_team AS team ON team.id = so.team_id
                        WHERE 1=1 {custom_filter} AND so.user_id = {user_id}
                        GROUP BY team.id, team.name->>'en_US'
                        ORDER BY COUNT(DISTINCT so.id) ASC;"""

        self.env.cr.execute(query)
        report_1 = self.env.cr.dictfetchall()
        team = {}
        for rec in report_1:
            team[rec["team_name"]] = rec['order_count']
        return team

    @api.model
    def get_sale_by_sales_person(self,selection_val,is_admin,user_id):
        """Returns data to the graph of dashboard"""
        custom_filter = ""
        if selection_val == "this_year":
            custom_filter = "AND EXTRACT('YEAR' FROM so.date_order) = EXTRACT('YEAR'FROM CURRENT_DATE)"
        if selection_val == "this_month":
            custom_filter = "AND EXTRACT('MONTH' FROM so.date_order) = EXTRACT('MONTH'FROM CURRENT_DATE)"
        if selection_val == "this_week":
            custom_filter = "AND EXTRACT('WEEK' FROM so.date_order) = EXTRACT('WEEK'FROM CURRENT_DATE)"
        if selection_val == "this_day":
            custom_filter = " AND EXTRACT('DAY' FROM so.date_order) = EXTRACT('DAY'FROM CURRENT_DATE)"
        if (is_admin):
            query = f"""SELECT partner.name,COUNT(so.id) AS order_count FROM sale_order AS so
                       INNER JOIN res_users AS res ON res.id = so.user_id
                       INNER JOIN res_partner AS partner ON partner.id = res.partner_id
                       WHERE 1=1 {custom_filter}
                       GROUP BY so.user_id, partner.name
                       ORDER BY COUNT(DISTINCT so.id) ASC;"""
        if (not is_admin):
            query = f"""SELECT partner.name,COUNT(so.id) AS order_count FROM sale_order AS so
                                  INNER JOIN res_users AS res ON res.id = so.user_id
                                  INNER JOIN res_partner AS partner ON partner.id = res.partner_id
                                  WHERE 1=1 {custom_filter} AND so.user_id = {user_id}
                                  GROUP BY so.user_id, partner.name
                                  ORDER BY COUNT(DISTINCT so.id) ASC;"""
        self.env.cr.execute(query)
        report_2 = self.env.cr.dictfetchall()
        sales_person = {}
        for rec in report_2:
            sales_person[rec["name"]] = rec['order_count']
        return sales_person

    @api.model
    def get_sale_by_top_customer(self,selection_val,is_admin,user_id):
        """Returns data to the graph of dashboard"""
        custom_filter = ""
        if selection_val == "this_year":
            custom_filter = "AND EXTRACT('YEAR' FROM so.date_order) = EXTRACT('YEAR'FROM CURRENT_DATE)"
        if selection_val == "this_month":
            custom_filter = "AND EXTRACT('MONTH' FROM so.date_order) = EXTRACT('MONTH'FROM CURRENT_DATE)"
        if selection_val == "this_week":
            custom_filter = "AND EXTRACT('WEEK' FROM so.date_order) = EXTRACT('WEEK'FROM CURRENT_DATE)"
        if selection_val == "this_day":
            custom_filter = " AND EXTRACT('DAY' FROM so.date_order) = EXTRACT('DAY'FROM CURRENT_DATE)"
        if (is_admin):
            query = f"""SELECT partner.name,COUNT(so.id) AS order_count
                       FROM sale_order AS so
                       INNER JOIN res_partner AS partner ON partner.id = so.partner_id
                       WHERE 1=1 {custom_filter}
                       GROUP BY so.partner_id, partner.name
                       ORDER BY COUNT(DISTINCT so.id) ASC;"""
        if (not is_admin):
            query = f"""SELECT partner.name,COUNT(so.id) AS order_count
                                   FROM sale_order AS so
                                   INNER JOIN res_partner AS partner ON partner.id = so.partner_id
                                   WHERE 1=1 {custom_filter} AND so.user_id = {user_id}
                                   GROUP BY so.partner_id, partner.name
                                   ORDER BY COUNT(DISTINCT so.id) ASC;"""
        self.env.cr.execute(query)
        report_3 = self.env.cr.dictfetchall()
        top_customer = {}
        for rec in report_3:
            top_customer[rec["name"]] = rec['order_count']
        return top_customer

    @api.model
    def get_sale_by_lowest_selling(self,selection_val,is_admin,user_id):
        """Returns data to the graph of dashboard"""
        custom_filter = ""
        if selection_val == "this_year":
            custom_filter = "AND EXTRACT('YEAR' FROM so.date_order) = EXTRACT('YEAR'FROM CURRENT_DATE)"
        if selection_val == "this_month":
            custom_filter = "AND EXTRACT('MONTH' FROM so.date_order) = EXTRACT('MONTH'FROM CURRENT_DATE)"
        if selection_val == "this_week":
            custom_filter = "AND EXTRACT('WEEK' FROM so.date_order) = EXTRACT('WEEK'FROM CURRENT_DATE)"
        if selection_val == "this_day":
            custom_filter = " AND EXTRACT('DAY' FROM so.date_order) = EXTRACT('DAY'FROM CURRENT_DATE)"
        if (is_admin):
            query = f"""SELECT p.name->>'en_US' AS product_name,
                       COUNT(DISTINCT so.id) AS order_count
                       FROM sale_order AS so
                       INNER JOIN sale_order_line AS ol ON ol.order_id = so.id
                       INNER JOIN product_template AS p ON ol.product_id = p.id
                       WHERE 1=1 {custom_filter}
                       GROUP BY p.name->>'en_US'
                       ORDER BY COUNT(DISTINCT so.id) ASC;"""
        if (not is_admin):
            query = f"""SELECT p.name->>'en_US' AS product_name,
                       COUNT(DISTINCT so.id) AS order_count
                       FROM sale_order AS so
                       INNER JOIN sale_order_line AS ol ON ol.order_id = so.id
                       INNER JOIN product_template AS p ON ol.product_id = p.id
                       WHERE 1=1 {custom_filter} AND so.user_id = {user_id}
                       GROUP BY p.name->>'en_US'
                       ORDER BY COUNT(DISTINCT so.id) ASC;"""
        self.env.cr.execute(query)
        report_4 = self.env.cr.dictfetchall()
        lowest_selling = {}
        for rec in report_4:
            lowest_selling[rec["product_name"]] = rec['order_count']
        return lowest_selling

    @api.model
    def get_sale_by_highest_selling(self,selection_val,is_admin,user_id):
        """Returns data to the graph of dashboard"""
        custom_filter = ""
        if selection_val == "this_year":
            custom_filter = "AND EXTRACT('YEAR' FROM so.date_order) = EXTRACT('YEAR'FROM CURRENT_DATE)"
        if selection_val == "this_month":
            custom_filter = "AND EXTRACT('MONTH' FROM so.date_order) = EXTRACT('MONTH'FROM CURRENT_DATE)"
        if selection_val == "this_week":
            custom_filter = "AND EXTRACT('WEEK' FROM so.date_order) = EXTRACT('WEEK'FROM CURRENT_DATE)"
        if selection_val == "this_day":
            custom_filter = " AND EXTRACT('DAY' FROM so.date_order) = EXTRACT('DAY'FROM CURRENT_DATE)"
        if (is_admin):
            query = f"""SELECT p.name->>'en_US' AS product_name,
                          COUNT(DISTINCT so.id) AS order_count
                          FROM sale_order AS so
                          INNER JOIN sale_order_line AS ol ON ol.order_id = so.id
                          INNER JOIN product_template AS p ON ol.product_id = p.id
                          WHERE 1=1 {custom_filter} 
                          GROUP BY p.name->>'en_US'
                          ORDER BY COUNT(DISTINCT so.id) DESC;""" 
        if (not is_admin):
            query = f"""SELECT p.name->>'en_US' AS product_name,
                          COUNT(DISTINCT so.id) AS order_count
                          FROM sale_order AS so
                          INNER JOIN sale_order_line AS ol ON ol.order_id = so.id
                          INNER JOIN product_template AS p ON ol.product_id = p.id
                          WHERE 1=1 {custom_filter} AND so.user_id = {user_id}
                          GROUP BY p.name->>'en_US'
                          ORDER BY COUNT(DISTINCT so.id) DESC;"""
        self.env.cr.execute(query)
        report_5 = self.env.cr.dictfetchall()
        highest_selling = {}
        for rec in report_5:
            highest_selling[rec["product_name"]] = rec['order_count']
        return highest_selling

    @api.model
    def get_sale_by_order_status(self,selection_val,is_admin,user_id):
        """Returns data to the graph of dashboard"""
        custom_filter = ""
        if selection_val == "this_year":
            custom_filter = "AND EXTRACT('YEAR' FROM so.date_order) = EXTRACT('YEAR'FROM CURRENT_DATE)"
        if selection_val == "this_month":
            custom_filter = "AND EXTRACT('MONTH' FROM so.date_order) = EXTRACT('MONTH'FROM CURRENT_DATE)"
        if selection_val == "this_week":
            custom_filter = "AND EXTRACT('WEEK' FROM so.date_order) = EXTRACT('WEEK'FROM CURRENT_DATE)"
        if selection_val == "this_day":
            custom_filter = " AND EXTRACT('DAY' FROM so.date_order) = EXTRACT('DAY'FROM CURRENT_DATE)"
        if (is_admin):
            query = f"""SELECT so.state ,
                       COUNT(DISTINCT so.id) AS order_count
                       FROM sale_order AS so
                       WHERE 1=1 {custom_filter}
                       GROUP BY so.state
                       ORDER BY COUNT(DISTINCT so.id) DESC;"""
        if ( not is_admin):
            query = f"""SELECT so.state ,
                       COUNT(DISTINCT so.id) AS order_count
                       FROM sale_order AS so
                       WHERE 1=1 {custom_filter} AND so.user_id = {user_id}
                       GROUP BY so.state
                       ORDER BY COUNT(DISTINCT so.id) DESC;"""
        self.env.cr.execute(query)
        report_6 = self.env.cr.dictfetchall()
        order_status = {}
        for rec in report_6:
            order_status[rec["state"]] = rec['order_count']
        return (order_status)

    @api.model
    def get_sale_by_invoice_status(self,selection_val,is_admin,user_id):
        """Returns data to the graph of dashboard"""
        custom_filter = ""
        if selection_val == "this_year":
            custom_filter = "AND EXTRACT('YEAR' FROM so.date_order) = EXTRACT('YEAR'FROM CURRENT_DATE)"
        if selection_val == "this_month":
            custom_filter = "AND EXTRACT('MONTH' FROM so.date_order) = EXTRACT('MONTH'FROM CURRENT_DATE)"
        if selection_val == "this_week":
            custom_filter = "AND EXTRACT('WEEK' FROM so.date_order) = EXTRACT('WEEK'FROM CURRENT_DATE)"
        if selection_val == "this_day":
            custom_filter = " AND EXTRACT('DAY' FROM so.date_order) = EXTRACT('DAY'FROM CURRENT_DATE)"
        if (is_admin):
            query = f"""SELECT so.invoice_status ,
                       COUNT(DISTINCT so.id) AS order_count
                       FROM sale_order AS so
                       WHERE 1=1 {custom_filter}
                       GROUP BY so.invoice_status
                       ORDER BY COUNT(DISTINCT so.id) DESC;"""
        if ( not is_admin):
            query = f"""SELECT so.invoice_status ,
                       COUNT(DISTINCT so.id) AS order_count
                       FROM sale_order AS so
                       WHERE 1=1 {custom_filter} AND so.user_id = {user_id}
                       GROUP BY so.invoice_status
                       ORDER BY COUNT(DISTINCT so.id) DESC;"""
        self.env.cr.execute(query)
        report_7 = self.env.cr.dictfetchall()
        invoice_status = {}
        for rec in report_7:
            invoice_status[rec["invoice_status"]] = rec['order_count']
        return invoice_status



