from django.db import models

# Create your models here.
class smetkoplan(models.Model):
        smetka=models.IntegerField(null=True, blank=True)
        opisanie=models.CharField(max_length=100, null=True, blank=True)
        n_saldo_dt=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
        n_saldo_kt=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
        k_saldo_dt=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
        k_saldo_kt=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
        spare=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


        
class vedomost(models.Model):
        first_f=models.CharField(max_length=100, null=True, blank=True)
        doc=models.CharField(max_length=100, null=True, blank=True)
        date=models.CharField(max_length=100, null=True, blank=True)
        nomer=models.CharField(max_length=100, null=True, blank=True)
        firma=models.CharField(max_length=100, null=True, blank=True)
        buls=models.CharField(max_length=100, null=True, blank=True)
        opisanie=models.TextField( null=True, blank=True)
        suma=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
        debit=models.IntegerField(null=True, blank=True)
        credit=models.IntegerField(null=True, blank=True)

        def __str__(self):
                return self.first_f
