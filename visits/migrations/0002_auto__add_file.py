# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'File'
        db.create_table(u'visits_file', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('visit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['visits.Visit'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'visits', ['File'])


    def backwards(self, orm):
        # Deleting model 'File'
        db.delete_table(u'visits_file')


    models = {
        u'visits.file': {
            'Meta': {'object_name': 'File'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'visit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['visits.Visit']"})
        },
        u'visits.provider': {
            'Meta': {'unique_together': "(('first_name', 'last_name'),)", 'object_name': 'Provider'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'visits': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['visits.Visit']", 'symmetrical': 'False'})
        },
        u'visits.visit': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Visit'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['visits']