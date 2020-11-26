from odoo import models, fields, api
from odoo.exceptions import MissingError
from datetime import datetime
import numpy as np

class wizard(models.TransientModel):
    _name = 'warranty.wizard'

    product = fields.Many2many('product.product', string='Warranty Products')
    # request_date = fields.Date("Current Date", default=datetime.today())
    from_date = fields.Date('From')
    to_date = fields.Date('To')



    def Print_pdf(self):
        global product_detail, invoice_name, partner_name, warranty_ids
        products = []
        products_name = []
        if self.product:
            if self.product and self.from_date and self.to_date:
                for rec in self.product:
                    products_name.append(rec.name)
                for rec in self.product:
                    products.append(rec.id)
                    products_list = tuple(products)
                self.env.cr.execute(
                    "SELECT * FROM product_warranty_product_warranty WHERE "
                    "product in %s AND current_date >= %s ""AND current_date <= ""%s ",
                    (products_list, self.from_date, self.to_date,))
                warranty_ids = self.env.cr.fetchall()
                print('warranty_ids', warranty_ids)

            # (1,1,0)
            elif self.from_date and not self.to_date:
                for rec in self.product:
                    products.append(rec.id)
                    products_list = tuple(products)
                self.env.cr.execute("SELECT * FROM product_warranty_product_warranty WHERE product in %s AND current_date >= %s",
                                    (products_list, self.from_date))
                warranty_ids = self.env.cr.fetchall()
                print(warranty_ids)


            # (1,0,1)
            elif not self.from_date and self.to_date:
                for rec in self.product:
                    products.append(rec.id)
                    products_list = tuple(products)
                self.env.cr.execute("SELECT * FROM product_warranty_product_warranty WHERE product in %s AND current_date <= %s",
                                    (products_list, self.to_date))
                warranty_ids = self.env.cr.fetchall()
                print(warranty_ids)

            # (1,0,0)
            else:
                for rec in self.product_name:
                    products.append(rec.id)
                    products_list = tuple(products)
                self.env.cr.execute("SELECT * FROM product_warranty_product_warranty WHERE product in %s",
                                    (products_list,))
                warranty_ids = self.env.cr.fetchall()
                print(warranty_ids)

        elif self.from_date:
            # (0,1,1)
            if self.to_date:
                self.env.cr.execute("SELECT * FROM product_warranty_product_warranty WHERE current_date >= %s AND "
                                    "current_date <= %s",
                                    (self.from_date, self.to_date))
                warranty_ids = self.env.cr.fetchall()
                print(warranty_ids)


            # (0,1,0)
            else:
                self.env.cr.execute("SELECT * FROM product_warranty_product_warranty WHERE current_date >= %s",
                                    (self.from_date,))
                warranty_ids = self.env.cr.fetchall()
                print(warranty_ids)


        else:
            # (0,1,0)
            if self.to_date:
                self.env.cr.execute("SELECT * FROM product_warranty_product_warranty WHERE current_date <= %s",
                                    (self.to_date,))
                warranty_ids = self.env.cr.fetchall()
                print(warranty_ids)

            else:
                # (0,0,0)
                self.env.cr.execute("SELECT * FROM product_warranty_product_warranty")
                warranty_ids = self.env.cr.fetchall()

        if not warranty_ids:
            raise MissingError("No warranty request had been found ")

        else:
            warranty = []
            product = []

            for product_warranty_product_warranty in warranty_ids:
                product.append(product_warranty_product_warranty[16])
                product_list =np.unique(product)

            for record  in product_list:
                print("record",record)

                vals=[]

                for product_warranty_product_warranty in warranty_ids:
                    if product_warranty_product_warranty[16] ==record:
                       self.env.cr.execute("SELECT name FROM product_template WHERE id in (SELECT "
                                        "product_tmpl_id FROM product_product WHERE id in (SELECT product FROM "
                                        "product_warranty_product_warranty WHERE product= %s))",
                                        (product_warranty_product_warranty[16],))
                       product_detail = self.env.cr.fetchall()
                       print("product", product_detail)


                       self.env.cr.execute("SELECT invoice_payment_ref FROM account_move WHERE id in (SELECT "
                                        "invoice FROM product_warranty_product_warranty WHERE invoice = %s)",
                                        (product_warranty_product_warranty[17],))
                       invoice_name = self.env.cr.fetchall()


                       self.env.cr.execute('SELECT name FROM res_partner WHERE id in (SELECT '
                                        'partner FROM product_warranty_product_warranty WHERE partner = %s)',
                                        (product_warranty_product_warranty[18],))
                       partner_name = self.env.cr.fetchall()


                       product = product_detail[0][0]
                       invoice = invoice_name [0] [0]
                       customer = partner_name[0][0]
                       expiry = product_warranty_product_warranty[9]
                       status = product_warranty_product_warranty[10]

                       vals.append({
                       'invoice': invoice,
                       'customer': customer,
                       'expiry': expiry,
                       'status': status
                    })
            warranty.append({
                'product': product_detail[0][0],
                'warranty_details': vals
            })



        data = {'model': 'warranty.wizard',

                        'from_date': self.from_date,
                        'to_date': self.to_date,
                        'warranty_ids': warranty}

        return self.env.ref('product_warranty.warranty_report_details').report_action(self, data=data)

    def Print_xls(self):
        global product_detail, invoice_name, partner_name, warranty_ids
        products = []
        products_name = []
        if self.product:
            if self.product and self.from_date and self.to_date:
                for rec in self.product:
                    products_name.append(rec.name)

                for rec in self.product:
                    products.append(rec.id)
                    products_list = tuple(products)

                self.env.cr.execute(
                    "SELECT * FROM product_warranty_product_warranty WHERE "
                    "product in %s AND current_date >= %s ""AND current_date <= ""%s ",
                    (products_list, self.from_date, self.to_date,))
                warranty_ids = self.env.cr.fetchall()
                print("warranty_ids", warranty_ids)

            # (1,1,0)
            elif self.from_date and not self.to_date:
                for rec in self.product:
                    products.append(rec.id)
                    products_list = tuple(products)
                self.env.cr.execute("SELECT * FROM product_warranty_product_warranty WHERE product in %s"
                                    " AND current_date >= %s",
                                    (products_list, self.from_date))
                warranty_ids = self.env.cr.fetchall()
                print(warranty_ids)


            # (1,0,1)
            elif not self.from_date and self.to_date:
                for rec in self.product:
                    products.append(rec.id)
                    products_list = tuple(products)
                self.env.cr.execute("SELECT * FROM product_warranty_product_warranty WHERE product in %s "
                                    "AND current_date <= %s",
                                    (products_list, self.to_date))
                warranty_ids = self.env.cr.fetchall()
                print(warranty_ids)

            # (1,0,0)
            else:
                for rec in self.product_name:
                    products.append(rec.id)
                    products_list = tuple(products)
                self.env.cr.execute("SELECT * FROM product_warranty_product_warranty WHERE product in %s",
                                    (products_list,))
                warranty_ids = self.env.cr.fetchall()
                print(warranty_ids)

        elif self.from_date:
            # (0,1,1)
            if self.to_date:
                self.env.cr.execute("SELECT * FROM product_warranty_product_warranty WHERE current_date >= %s AND "
                                    "current_date <= %s",
                                    (self.from_date, self.to_date))
                warranty_ids = self.env.cr.fetchall()
                print(warranty_ids)


            # (0,1,0)
            else:
                self.env.cr.execute("SELECT * FROM product_warranty_product_warranty WHERE current_date >= %s",
                                    (self.from_date,))
                warranty_ids = self.env.cr.fetchall()
                print(warranty_ids)


        else:
            # (0,1,0)
            if self.to_date:
                self.env.cr.execute("SELECT * FROM product_warranty_product_warranty WHERE current_date <= %s",
                                    (self.to_date,))
                warranty_ids = self.env.cr.fetchall()
                print(warranty_ids)

            else:
                # (0,0,0)
                self.env.cr.execute("SELECT * FROM product_warranty_product_warranty")
                warranty_ids = self.env.cr.fetchall()

        p_name = []
        for id in warranty_ids:
            p_name.append(id[16])
        names = np.unique(p_name)
        pro = []
        for rec in names:
            print("pro ", rec)
            leaves = []
            for id in warranty_ids:
                if id[16] == rec:
                    self.env.cr.execute("SELECT name FROM product_template WHERE id in "
                                        "(SELECT product_tmpl_id FROM product_product WHERE id in "
                                        "(SELECT product FROM product_warranty_product_warranty"
                                        " WHERE product = %s))",
                                        (id[16],))
                    products = self.env.cr.fetchall()
                    print(products)
                    self.env.cr.execute("SELECT invoice_payment_ref FROM account_move WHERE id in "

                                        "(SELECT invoice FROM product_warranty_product_warranty "
                                        "WHERE invoice = %s)", (id[17],))
                    invoice = self.env.cr.fetchall()
                    print(invoice)
                    self.env.cr.execute("SELECT name FROM res_partner WHERE id in"
                                        "(SELECT partner FROM product_warranty_product_warranty"
                                        " WHERE partner= %s)",
                                        (id[18],))
                    customer = self.env.cr.fetchall()
                    product = products
                    invoice = invoice[0][0]
                    customer = customer
                    expiry = id[9]
                    status = id[10]
                    leaves.append({
                        'invoice': invoice,
                        'customer': customer[0][0],
                        'expiry': expiry,
                        'status': status
                    })

            pro.append({
                'product': products[0][0],
                'details': leaves
            })

        data = {'model': 'warranty.wizard',

                'from_date': self.from_date,
                'to_date': self.to_date,
                'warranty_ids': pro}

        return self.env.ref('product_warranty.warranty_report_details_xls').report_action(self, data)
