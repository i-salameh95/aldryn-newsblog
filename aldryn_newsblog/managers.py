# -*- coding: utf-8 -*-

from __future__ import unicode_literals

try:
    from collections import Counter
except ImportError:
    from backport_collections import Counter

import datetime
from operator import attrgetter

from django.db import models
from django.utils import timezone

from aldryn_apphooks_config.managers.base import ManagerMixin, QuerySetMixin
from aldryn_people.models import Person
from parler.managers import TranslatableManager, TranslatableQuerySet
from taggit.models import Tag, TaggedItem


class ArticleQuerySet(QuerySetMixin, TranslatableQuerySet):
    def published(self):
        """
        Returns articles that are published AND have a publishing_date that
        has actually passed.
        """
        return self.filter(is_published=True).filter(
            publishing_date__lte=timezone.now
        )


class RelatedManager(ManagerMixin, TranslatableManager):
    def get_query_set(self):
        qs = ArticleQuerySet(self.model, using=self.db)
        return qs.select_related('featured_image')

    def published(self):
        return self.get_query_set().published()

    def get_months(self, namespace):
        """
        Get months and years with articles count for given namespace string.
        This means how many articles there are in each month.

        Return list of dictionaries ordered by article publishing date of the
        following format:
        [
            {
                'date': date(YEAR, MONTH, ARBITRARY_DAY),
                'num_articles': NUM_ARTICLES
            },
            ...
        ]
        """

        # TODO: check if this limitation still exists in Django 1.6+
        # This is done in a naive way as Django is having tough time while
        # aggregating on date fields
        articles = self.published().namespace(namespace)
        dates = articles.values_list('publishing_date', flat=True)
        dates = [(x.year, x.month) for x in dates]
        date_counter = Counter(dates)
        dates = set(dates)
        dates = sorted(dates, reverse=True)
        months = [
            # Use day=3 to make sure timezone won't affect this hacks'
            # month value. There are UTC+14 and UTC-12 timezones!
            {'date': datetime.date(year=year, month=month, day=3),
             'num_articles': date_counter[(year, month)]}
            for year, month in dates]
        return months

    def get_authors(self, namespace):
        """
        Get authors with articles count for given namespace string.

        Return Person queryset annotated with and ordered by 'num_articles'.
        """

        # This methods relies on the fact that Article.app_config.namespace
        # is effectively unique for Article models
        return Person.objects.filter(
            article__app_config__namespace=namespace,
            article__is_published=True).annotate(
                num_articles=models.Count('article')).order_by('-num_articles')

    def get_tags(self, namespace):
        """
        Get tags with articles count for given namespace string.

        Return list of Tag objects ordered by custom 'num_articles' attribute.
        """

        articles = self.published().namespace(namespace)
        if not articles:
            # return empty iterable early not to perform useless requests
            return []
        kwargs = TaggedItem.bulk_lookup_kwargs(articles)

        # aggregate and sort
        counted_tags = dict(TaggedItem.objects
                            .filter(**kwargs)
                            .values('tag')
                            .annotate(tag_count=models.Count('tag'))
                            .values_list('tag', 'tag_count'))

        # and finally get the results
        tags = Tag.objects.filter(pk__in=counted_tags.keys())
        for tag in tags:
            tag.num_articles = counted_tags[tag.pk]
        return sorted(tags, key=attrgetter('num_articles'), reverse=True)
