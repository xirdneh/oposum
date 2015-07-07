# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Layaway.type'
        db.add_column(u'layaway_layaway', 'type',
                      self.gf('django.db.models.fields.IntegerField')(default=30),
                      keep_default=False)


        # Changing field 'Layaway.date_time'
        db.alter_column(u'layaway_layaway', 'date_time', self.gf('django.db.models.fields.DateTimeField')())

    def backwards(self, orm):
        # Deleting field 'Layaway.type'
        db.delete_column(u'layaway_layaway', 'type')


        # Changing field 'Layaway.date_time'
        db.alter_column(u'layaway_layaway', 'date_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

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
        u'layaway.layaway': {
            'Meta': {'object_name': 'Layaway'},
            'amount_to_pay': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['branches.Branch']"}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['client.Client']"}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'folio_number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['products.Product']", 'symmetrical': 'False'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'layaway.layawayhistory': {
            'Meta': {'object_name': 'LayawayHistory'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['branches.Branch']"}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'folio_number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layaway': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['layaway.Layaway']"})
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
        }
    }

    complete_apps = ['layaway']