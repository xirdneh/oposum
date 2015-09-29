from django.db import models
from oPOSum.libs import utils as pos_utils
from django.utils.translation import ugettext as _
from decimal import Decimal
from django.core.validators import RegexValidator

# Create your models here.
class Client(models.Model):
    first_name = models.CharField(_("First Name"), max_length=100, blank=False)
    last_name = models.CharField(_("Last Name"), max_length = 512, blank=False)
    phonenumber = models.CharField(_("Phone Number"), 
                  max_length=512, blank=True, unique=False, null=True, 
                validators = [
                    RegexValidator(r'[0-9]{3}\-?[0-9]{3}\-?[0-9]{4}', 
                                   'Format: 834-117-1086', 
                                   'phone_format_error')
                    ]
                )
    address = models.TextField(_("Address"), max_length=1024, blank=True)
    id_type = models.CharField(_("ID Type"), max_length=50, blank=True, default='IFE',
              choices=(
                ('IFE', 'IFE (Credencial de Elector'),
                ('LICENCIA', 'Licencia de conducir'),
                ('PASAPORTE', 'Pasaporte'),
                ('OTRO', 'Otro'),
              ))
    id_number = models.CharField(_("Identification Number"), max_length=255, blank=True)
    email = models.EmailField(_("Email"), max_length = 255, blank=True, unique=False)

    class Meta:
        unique_together = (('first_name', 'last_name', 'phonenumber', 'email'))
        verbose_name = "client"
        verbose_name_plural = "clients"

    def __unicode__(self):
        return u"{0} {1}. {2}, {3}".format(self.first_name, self.last_name, self.phonenumber, self.email)

    def as_json(self):
        return dict(
            id = self.id,
            first_name = self.first_name.encode('latin-1'),
            last_name = self.last_name.encode('latin-1'),
            phonenumber = self.phonenumber,
            address = self.address.encode('latin-1'),
            id_type = self.id_type,
            id_number = self.id_number,
            email = self.email
        )

    def get_total_debt(self):
        apps = pos_utils.get_installed_oposum_apps()
        ret = Decimal(0)
        if 'layaway' in apps:
            from oPOSum.apps.layaway.models import Layaway
            ret += Layaway.objects.get_total_debt_amount(self)
        if 'repairshop' in apps:
            from oPOSum.apps.repairshop.models import RepairTicket
            ret += RepairTicket.objects.get_total_debt_amount(self)
        return ret

    def get_layaway_debt(self):
        apps = pos_utils.get_installed_oposum_apps()
        ret = Decimal(0)
        if 'layway' in apps:
            from oPOSum.apps.layaway.models import Layaway
            ret += Layaway.objects.get_total_debt_amount(self)
        return ret

    def get_repairshop_debt(self):
        apps = pos_utils.get_installed_oposum_apps()
        ret = Decimal(0)
        if 'repairshop' in apps:
            from oPOSum.apps.repairshop.models import RepairTicket
            ret += RepairTicket.objects.get_total_debt_amount(self)
        return ret

    def get_repairshop_pending_tickets(self):
        #TODO get pending tickets
        return 0

    def save(self, *args, **kwargs):
        if not self.pk:
            self.phonenumber = self.phonenumber.replace("-", "")
        super(Client, self).save(*args, **kwargs)
