# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WorkshopTicket'
        db.create_table(u'workshop_workshopticket', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(related_name='branch_set', to=orm['branches.Branch'])),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['client.Client'], null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_time_end', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('folio_number', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True)),
            ('workshop', self.gf('django.db.models.fields.related.ForeignKey')(related_name='workshop_set', to=orm['branches.Branch'])),
            ('total_cost', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=10, decimal_places=2)),
            ('time_to_complete', self.gf('django.db.models.fields.PositiveIntegerField')(default=5)),
            ('current_location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='current_location_set', to=orm['branches.Branch'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'workshop', ['WorkshopTicket'])

        # Adding model 'WorkshopPayment'
        db.create_table(u'workshop_workshoppayment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['branches.Branch'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('ticket', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workshop.WorkshopTicket'])),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=10, decimal_places=2)),
            ('payment_tye', self.gf('django.db.models.fields.CharField')(default='Cash', max_length=255)),
        ))
        db.send_create_signal(u'workshop', ['WorkshopPayment'])

        # Adding model 'WorkshopStatus'
        db.create_table(u'workshop_workshopstatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['branches.Branch'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('ticket', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workshop.WorkshopTicket'])),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default='Description')),
            ('is_current', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'workshop', ['WorkshopStatus'])

        # Adding model 'WorkshopServices'
        db.create_table(u'workshop_workshopservices', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['branches.Branch'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('ticket', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workshop.WorkshopTicket'])),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default='Description')),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=10, decimal_places=2)),
        ))
        db.send_create_signal(u'workshop', ['WorkshopServices'])

        # Adding model 'WorkshopProduct'
        db.create_table(u'workshop_workshopproduct', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['branches.Branch'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('ticket', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workshop.WorkshopTicket'])),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Product'])),
            ('qty', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'workshop', ['WorkshopProduct'])


    def backwards(self, orm):
        # Deleting model 'WorkshopTicket'
        db.delete_table(u'workshop_workshopticket')

        # Deleting model 'WorkshopPayment'
        db.delete_table(u'workshop_workshoppayment')

        # Deleting model 'WorkshopStatus'
        db.delete_table(u'workshop_workshopstatus')

        # Deleting model 'WorkshopServices'
        db.delete_table(u'workshop_workshopservices')

        # Deleting model 'WorkshopProduct'
        db.delete_table(u'workshop_workshopproduct')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'branches.branch': {
            'Meta': {'object_name': 'Branch'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['branches.BranchDetail']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'branch name'", 'max_length': '50'}),
            'slug': ('django.db.models.fields.CharField', [], {'default': "'branch'", 'unique': 'True', 'max_length': '50', 'primary_key': 'True'}),
            'ticket_post': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ticket_pre': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['branches.BranchType']"})
        },
        u'branches.branchdetail': {
            'Meta': {'object_name': 'BranchDetail'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'branches.branchtype': {
            'Meta': {'object_name': 'BranchType'},
            'description': ('django.db.models.fields.CharField', [], {'default': "'type description'", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'branch type'", 'unique': 'True', 'max_length': '255'})
        },
        u'client.client': {
            'Meta': {'unique_together': "(('first_name', 'last_name'),)", 'object_name': 'Client'},
            'address': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id_type': ('django.db.models.fields.CharField', [], {'default': "'IFE'", 'max_length': '50', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'phonenumber': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'products.product': {
            'Meta': {'object_name': 'Product'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['products.ProductCategory']", 'symmetrical': 'False', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '512', 'blank': 'True'}),
            'details': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['products.ProductDetail']", 'symmetrical': 'False', 'blank': 'True'}),
            'equivalency': ('django.db.models.fields.DecimalField', [], {'default': "'1.00'", 'max_digits': '10', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.ProductLine']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Provider']"}),
            'regular_price': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'blank': 'True'})
        },
        u'products.productcategory': {
            'Meta': {'object_name': 'ProductCategory'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child'", 'null': 'True', 'to': u"orm['products.ProductCategory']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'products.productdetail': {
            'Meta': {'object_name': 'ProductDetail'},
            'description': ('django.db.models.fields.CharField', [], {'default': "'detail description'", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'detail name'", 'max_length': '255'})
        },
        u'products.productline': {
            'Meta': {'object_name': 'ProductLine'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'products.provider': {
            'Meta': {'object_name': 'Provider'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['products.ProviderDetail']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'nombre'", 'max_length': '255'}),
            'sku': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'telephone1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'telephone2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'products.providerdetail': {
            'Meta': {'object_name': 'ProviderDetail'},
            'description': ('django.db.models.fields.CharField', [], {'default': "'detail description'", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'detail name'", 'max_length': '255'})
        },
        u'workshop.workshoppayment': {
            'Meta': {'object_name': 'WorkshopPayment'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '2'}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['branches.Branch']"}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_tye': ('django.db.models.fields.CharField', [], {'default': "'Cash'", 'max_length': '255'}),
            'ticket': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workshop.WorkshopTicket']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'workshop.workshopproduct': {
            'Meta': {'object_name': 'WorkshopProduct'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['branches.Branch']"}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Product']"}),
            'qty': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'ticket': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workshop.WorkshopTicket']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'workshop.workshopservices': {
            'Meta': {'object_name': 'WorkshopServices'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '2'}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['branches.Branch']"}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "'Description'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ticket': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workshop.WorkshopTicket']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'workshop.workshopstatus': {
            'Meta': {'object_name': 'WorkshopStatus'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['branches.Branch']"}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "'Description'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_current': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ticket': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workshop.WorkshopTicket']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'workshop.workshopticket': {
            'Meta': {'object_name': 'WorkshopTicket'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'branch_set'", 'to': u"orm['branches.Branch']"}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['client.Client']", 'null': 'True'}),
            'current_location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'current_location_set'", 'to': u"orm['branches.Branch']"}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_time_end': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'folio_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'time_to_complete': ('django.db.models.fields.PositiveIntegerField', [], {'default': '5'}),
            'total_cost': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '2'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'workshop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'workshop_set'", 'to': u"orm['branches.Branch']"})
        }
    }

    complete_apps = ['workshop']