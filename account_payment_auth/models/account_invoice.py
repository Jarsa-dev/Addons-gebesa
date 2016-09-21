# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def _get_domain_groups_id(self):
        ids = self.env.ref('account_payment_auth.group_aut_pagos_super').ids
        return [('groups_id.id', '=', ids)]

    aut_estatus_pago = fields.Selection(
        [('none', _('None')),
         ('proposed', _('Proposed')),
         ('authorized', _('Authorized')),
         ('rejected', _('Rejected'))],
        string=_("Payment authorization status"),
        track_visibility='onchange',
        default='none',
    )
    authorizes_id = fields.Many2one(
        'res.users',
        string='Authorizes',
        domain=_get_domain_groups_id
    )

    @api.multi
    def action_payment_auth_request(self):
        for invoice in self:
            if not invoice.authorizes_id.id:
                raise ValidationError(_("Error!\nField Authorized it's not \
                                      valid"))
            invoice.aut_estatus_pago = 'proposed'
        return True

    @api.multi
    def action_payment_auth(self):
        for invoice in self:
            if self.env.uid != invoice.authorizes_id.id:
                raise ValidationError(_("Error!\nYou may not authorize this \
                                      payment is not assigned to you"))
            invoice.aut_estatus_pago = 'authorized'
        return True

    @api.multi
    def action_refuse_payment(self):
        for invoice in self:
            if self.env.uid != invoice.authorizes_id.id:
                raise ValidationError(_("Error!\nYou can not refuse this \
                                      payment is not assigned to you"))
            invoice.aut_estatus_pago = 'rejected'
        return True