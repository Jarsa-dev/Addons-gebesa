# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class AccountAccountType(models.Model):
    _inherit = 'account.account.type'

    is_expense = fields.Boolean(
        string='Is expense',
    )
