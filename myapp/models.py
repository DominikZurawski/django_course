from django.db import models

class KRSCompany(models.Model):
    name = models.CharField(max_length=255)
    krs_number = models.CharField(max_length=10, unique=True)
    nip = models.CharField(max_length=15, blank=True, null=True)
    regon = models.CharField(max_length=14, blank=True, null=True)
    legal_form = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)

    @property
    def address(self):
        return f"{self.city} {self.street_address}".strip() if self.city and self.street_address else None


    website = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.krs_number})"
