# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ProductPrice'
        db.delete_table(u'products_productprice')

        # Adding model 'ProductLine'
        db.create_table(u'products_productline', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
        ))
        db.send_create_signal(u'products', ['ProductLine'])

        # Deleting field 'Product.price'
        db.delete_column(u'products_product', 'price_id')

        # Adding field 'Product.line'
        db.add_column(u'products_product', 'line',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.ProductLine'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Product.regular_price'
        db.add_column(u'products_product', 'regular_price',
                      self.gf('django.db.models.fields.DecimalField')(default='0.00', null=True, max_digits=10, decimal_places=2, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'ProductPrice'
        db.create_table(u'products_productprice', (
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
        ))
        db.send_create_signal(u'products', ['ProductPrice'])

        # Deleting model 'ProductLine'
        db.delete_table(u'products_productline')


        # User chose to not deal with backwards NULL issues for 'Product.price'
        raise RuntimeError("Cannot reverse this migration. 'Product.price' and its values cannot be restored.")
        # Deleting field 'Product.line'
        db.delete_column(u'products_product', 'line_id')

        # Deleting field 'Product.regular_price'
        db.delete_column(u'products_product', 'regular_price')


    models = {
        u'products.product': {
            'Meta': {'object_name': 'Product'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'categories'", 'blank': 'True', 'to': u"orm['products.ProductCategory']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '512', 'blank': 'True'}),
            'details': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'extra_details'", 'symmetrical': 'False', 'to': u"orm['products.ProductDetail']"}),
            'equivalency': ('django.db.models.fields.DecimalField', [], {'default': "'1.00'", 'max_digits': '10', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.ProductLine']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Provider']"}),
            'regular_price': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'products.productcategory': {
            'Meta': {'object_name': 'ProductCategory'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child'", 'null': 'True', 'to': u"orm['products.ProductCategory']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
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
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'products.provider': {
            'Meta': {'object_name': 'Provider'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'extra_details'", 'symmetrical': 'False', 'to': u"orm['products.ProviderDetail']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'nombre'", 'max_length': '255'}),
            'sku': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'telephone1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'telephone2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'products.providerdetail': {
            'Meta': {'object_name': 'ProviderDetail'},
            'description': ('django.db.models.fields.CharField', [], {'default': "'detail description'", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'detail name'", 'max_length': '255'})
        }
    }

    complete_apps = ['products']