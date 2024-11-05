/**@odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
const { Component } = owl;
const actionRegistry = registry.category("actions");
var session = require('web.session');


class SaleDashboard extends Component {
   setup() {
         super.setup()
         this.orm = useService('orm')
         this.user = useService('user');
         this.selection = false
         this.chart,this.chart_2,this.chart_3,this.chart_4,this.chart_5,this.chart_6,this.chart_7 = null;
         this._fetch_data()
   }
   _onchange_selection(){
        this.selection = true
        this._fetch_data()
   }
   async _fetch_data(){
       var is_admin = this.user.isAdmin
       console.log(is_admin)
       var user_id = this.user.userId

       var selection_val = $('.filter_selection').val()
       if (this.selection == true){
            this.chart.destroy()
            this.chart_2.destroy()
            this.chart_3.destroy()
            this.chart_4.destroy()
            this.chart_5.destroy()
            this.chart_6.destroy()
            this.chart_7.destroy()
       }

//------------------------------------------------- Sales by sales team Bar chart
       const team = await this.orm.call("sale.order", "get_sale_by_team", [selection_val,is_admin,user_id])
       this.chart = new Chart("sales_team_chart", {
            type: "bar",
            data: {
                labels: Object.keys(team),
                datasets: [{
                    backgroundColor: ["black","green","blue"],
                    label: Object.keys(team)[0],
                    data: Object.values(team),
                    },{
                        backgroundColor: ["black","green"],
                        label: Object.keys(team)[1],
                }]
            },
            options: {}
      });


//-------------------------------------------------Sales by sales person Pie chart
       const sales_person = await this.orm.call("sale.order", "get_sale_by_sales_person", [selection_val,is_admin,user_id])
       this.chart_2 = new Chart("sales_person_chart", {
            type: "pie",
            data: {
                labels: Object.keys(sales_person),
                datasets: [{
                    backgroundColor: ["blue","black","red"],
                    data: Object.values(sales_person),
                }]
            },
            options: {}
      });


//-------------------------------------------------Top 10 customers Doughnut chart
       const top_customer = await this.orm.call("sale.order", "get_sale_by_top_customer", [selection_val,is_admin,user_id])
       this.chart_3 = new Chart("top_customer_chart", {
            type: "doughnut",
            data: {
                labels: Object.keys(top_customer),
                datasets: [{
                    backgroundColor: ["red","black","blue","green","yellow"],
                    data: Object.values(top_customer),
                }]
            },
            options: {}
      });


//-------------------------------------------------Lowest selling products Line chart
       const lowest_selling = await this.orm.call("sale.order", "get_sale_by_lowest_selling", [selection_val,is_admin,user_id])
       this.chart_4 = new Chart("lowest_selling_chart", {
            type: "line",
            data: {
                labels: Object.keys(lowest_selling),
                datasets: [{
                    pointBackgroundColor: ["blue","black","red","green","yellow"],
                    data: Object.values(lowest_selling),
                }]
            },
            options: {}
      });


//-------------------------------------------------Highest selling products Line chart
       const highest_selling = await this.orm.call("sale.order", "get_sale_by_highest_selling", [selection_val,is_admin,user_id])
       this.chart_5 = new Chart("highest_selling_chart", {
            type: "line",
            data: {
                labels: Object.keys(highest_selling),
                datasets: [{
                    pointBackgroundColor: ["blue","black","red","green","yellow"],
                    data: Object.values(highest_selling),
                }]
            },
            options: {}
      });


//-------------------------------------------------Order status Bar chart
       const order_status = await this.orm.call("sale.order", "get_sale_by_order_status", [selection_val,is_admin,user_id])
       this.chart_6 = new Chart("order_status_chart", {
            type: "bar",
            data: {
                labels: Object.keys(order_status),
                datasets: [{
                    backgroundColor: ["green","yellow","blue"],
                    data: Object.values(order_status),
                }]
            },
            options: {}
      });


//-------------------------------------------------Invoice status Bar chart
       const invoice_status = await this.orm.call("sale.order", "get_sale_by_invoice_status", [selection_val,is_admin,user_id])
       this.chart_7 = new Chart("invoice_status_chart", {
            type: "bar",
            data: {
                labels: Object.keys(invoice_status),
                datasets: [{
                    backgroundColor: ["green","yellow","blue"],
                    data: Object.values(invoice_status),
                }]
            },
            options: {}
      });
   }
}


SaleDashboard.template = "sales_dashboard.SalesDashboard";
actionRegistry.add("sales_dashboard_tag", SaleDashboard);






















//       var len = Object.getOwnPropertyNames(team).length
